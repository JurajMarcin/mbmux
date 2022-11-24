from dataclasses import field

from pymodbus.constants import Defaults

from tomlconfig import configclass


@configclass
class TcpClientConfig:
    rtu: bool = False
    host: str = ""
    port: int = Defaults.TcpPort


@configclass
class SerialClientConfig:
    port: str = ""
    ascii: bool = False
    baudrate: int = Defaults.Baudrate
    bytesize: int = Defaults.Bytesize
    parity: str = Defaults.Parity
    stopbits: int = Defaults.Stopbits
    handle_local_echo: bool = Defaults.HandleLocalEcho


@configclass
class LinkConfig:
    timeout: int = Defaults.Timeout
    retries: int = Defaults.Retries
    tcp: TcpClientConfig = TcpClientConfig()
    serial: SerialClientConfig = SerialClientConfig()
    slave_map: dict[int, int] = {}


@configclass
class LinksConfigs:
    link: list[LinkConfig] = field(default_factory=list)


@configclass
class Config:
    address: str = "0.0.0.0"
    port: int = Defaults.TcpPort
    debug: bool = False
