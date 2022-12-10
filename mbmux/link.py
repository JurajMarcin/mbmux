from asyncio.locks import Lock
import logging
from typing import Any

from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.framer.ascii_framer import ModbusAsciiFramer
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.framer.socket_framer import ModbusSocketFramer
from pymodbus.pdu import ModbusRequest, ModbusResponse

from .config import LinkConfig


_logger = logging.getLogger(__name__)


def _get_client_args(config: LinkConfig) -> dict[str, Any]:
    return {
        "timeout": config.timeout,
        "retries": config.retries,
    }


def _create_client(config: LinkConfig) \
        -> AsyncModbusTcpClient | AsyncModbusSerialClient:
    if config.tcp is not None:
        return AsyncModbusTcpClient(
            config.tcp.address,
            port=config.tcp.port,
            framer=ModbusRtuFramer if config.tcp.rtu else ModbusSocketFramer,
            **_get_client_args(config)
        )
    if config.serial is not None:
        return AsyncModbusSerialClient(
            config.port,
            framer=ModbusAsciiFramer if config.ascii else ModbusRtuFramer,
            baudrate=config.baudrate,
            bytesize=config.bytesize,
            parity=config.parity,
            stopbits=config.stopbits,
            handle_local_echo=config.handle_local_echo,
        )
    raise ValueError("Invalid client type")


class Link:
    """Class representing a single Modbus link"""
    def __init__(self, config: LinkConfig):
        self.client = _create_client(config)
        self.slave_map = config.slave_map
        self.lock = Lock()

    async def execute(self, request: ModbusRequest) -> ModbusResponse:
        """Sends a request to the connected Modbus link"""
        await self.lock.acquire()
        try:
            await self.client.connect()
            old_unit_id: int = request.unit_id
            if old_unit_id in self.slave_map:
                request.unit_id = self.slave_map[old_unit_id]
            _logger.debug("Forwarding request %r to slave %r on %r", request,
                          request.unit_id, self.client)
            result: ModbusResponse = await self.client.execute(request)
            _logger.debug("Received response %r from slave %r on %r", result,
                          request.unit_id, self.client)
            result.unit_id = old_unit_id
            return result
        finally:
            await self.client.close()
            self.lock.release()

    def __str__(self) -> str:
        return f"Link<{self.client}>"
