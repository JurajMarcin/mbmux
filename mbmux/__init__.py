import asyncio
import logging

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.async_io import StartAsyncTcpServer

from tomlconfig import parse

from .config import Config, LinksConfigs
from .handler import MuxHandler
from .link import Link


_logger = logging.getLogger(__name__)


def main() -> None:
    identity = ModbusDeviceIdentification(info_name={
        "VendorName": "JurajMarcin",
        "ProductCode": "MX",
        "VendorUrl": "https://github.com/JurajMarcin/mbmux/",
        "ProductName": "mbmux",
        "ModelName": "mbmux",
        "MajorMinorRevision": "1.0.0",
    })

    config = parse(Config, "config.toml")
    links_config = parse(LinksConfigs, "links.toml", "links.d")
    for link_config in links_config.link:
        link = Link(link_config)
        for slave_id in link.slave_map:
            MuxHandler.links[slave_id] = link

    if config.debug:
        _logger.setLevel(logging.DEBUG)

    _logger.info("Starting ModbusTCP server listening on %s:%s",
                 config.address, config.port)
    asyncio.run(StartAsyncTcpServer(identity=identity,
                                    address=(config.address, config.port),
                                    handler=MuxHandler,
                                    allow_reuse_address=True),
                debug=config.debug)


if __name__ == "__main__":
    main()
