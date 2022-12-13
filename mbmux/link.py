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
        self.config = config
        self.lock = Lock()

    async def execute(self, request: ModbusRequest) -> ModbusResponse:
        """Sends a request to the connected Modbus link"""
        await self.lock.acquire()
        _logger.debug("Aquired lock on %r", self)
        try:
            client = _create_client(self.config)
            await client.connect()
            old_unit_id: int = request.unit_id
            if old_unit_id in self.config.slave_map:
                request.unit_id = self.config.slave_map[old_unit_id]
            _logger.debug("Forwarding request %r to slave %r on %r", request,
                          request.unit_id, self)
            result: ModbusResponse = await client.execute(request)
            _logger.debug("Received response %r from slave %r on %r", result,
                          request.unit_id, self)
            result.unit_id = old_unit_id
            return result
        finally:
            try:
                await client.close()
            finally:
                _logger.debug("Released lock on %r", self)
                self.lock.release()

    def __str__(self) -> str:
        if self.config.tcp is not None:
            return f"Link<{self.config.tcp.address}>"
        if self.config.serial is not None:
            return f"Link<{self.config.serial.port}>"
        return "Link<unknown>"
