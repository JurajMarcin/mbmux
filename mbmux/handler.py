from asyncio.exceptions import CancelledError
from asyncio.queues import Queue, QueueEmpty
import logging

from pymodbus.pdu import ModbusRequest
from pymodbus.server.async_io import ModbusConnectedRequestHandler, ModbusTcpServer

from .link import Link


_logger = logging.getLogger(__name__)


class MuxHandler(ModbusConnectedRequestHandler):
    """Class handling incoming Modbus connections and multiplexing requests"""
    links: dict[int, Link] = {}

    def __init__(self, owner: ModbusTcpServer) -> None:
        super().__init__(owner)
        self.queue: Queue[ModbusRequest] = Queue()

    def _callback(self, request: ModbusRequest) -> None:
        self.queue.put_nowait(request)

    async def handle(self) -> None:
        while self.running:
            try:
                data = await self.receive_queue.get()

                self.framer.processIncomingPacket(data=data,
                                                  callback=self._callback,
                                                  unit=list(self.links.keys()))
                request = self.queue.get_nowait()
                old_transaction_id = request.transaction_id
                _logger.debug("Received %r from %r", request,
                              self.client_address)
                slave_result = \
                    await self.links[request.unit_id].execute(request)
                slave_result.transaction_id = old_transaction_id
                _logger.debug("Sending %r to %r", slave_result,
                              self.client_address)
                self.send(slave_result)

            except QueueEmpty:
                # Request is not fully received, try next pass
                pass
            except CancelledError:
                # catch and ignore cancellation errors
                self.running = False
            except Exception as ex:
                _logger.error("Unknown exception %r, disconnect from %r", ex,
                              self.client_address)
                self.transport.close()
