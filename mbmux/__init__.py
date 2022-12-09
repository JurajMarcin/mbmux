from argparse import ArgumentParser
import asyncio
import logging
from os.path import isdir
from sys import stderr

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.async_io import StartAsyncTcpServer
from tomlconfig import ConfigError, parse

from .config import Config
from .handler import MuxHandler
from .link import Link


_logger = logging.getLogger(__name__)


def main() -> None:
    parser = ArgumentParser("Modbus multiplexer")
    parser.add_argument("--debug", help="show debug output on stderr",
                        action="store_true", default=False)
    parser.add_argument("--config",
                        help="load config from the file CONFIG or load config "
                        "from files in the directory CONFIG in alphabetical "
                        "order",
                        default="/etc/mbmux")
    args = parser.parse_args()

    try:
        config = parse(Config, conf_d_path=args.config) \
            if isdir(args.config) else parse(Config, conf_path=args.config)
    except FileNotFoundError as ex:
        raise ConfigError("No configuration!") from ex
    if args.debug:
        config.debug = True

    log_handler = logging.StreamHandler(stderr)
    log_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"),
    )
    _logger.addHandler(log_handler)
    _logger.setLevel(logging.DEBUG if config.debug else logging.INFO)

    for link_config in config.link:
        link = Link(link_config)
        for slave_id in link.slave_map:
            MuxHandler.links[slave_id] = link

    _logger.info("Starting ModbusTCP server listening on %s:%s",
                 config.address, config.port)
    identity = ModbusDeviceIdentification(info_name={
        "VendorName": "JurajMarcin",
        "ProductCode": "MX",
        "VendorUrl": "https://github.com/JurajMarcin/mbmux/",
        "ProductName": "mbmux",
        "ModelName": "mbmux",
        "MajorMinorRevision": "1.0.0",
    })
    asyncio.run(StartAsyncTcpServer(identity=identity,
                                    address=(config.address, config.port),
                                    handler=MuxHandler,
                                    allow_reuse_address=True),
                debug=config.debug)
