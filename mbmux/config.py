from dataclasses import field

from pymodbus.constants import Defaults

from tomlconfig import configclass


@configclass
class TcpClientConfig:
    """Class holding Modbus/TCP config"""
    rtu: bool = False
    address: str = ""
    port: int = Defaults.TcpPort


@configclass
class SerialClientConfig:
    """Class holding Modbus/RTU config"""
    port: str = ""
    ascii: bool = False
    baudrate: int = Defaults.Baudrate
    bytesize: int = Defaults.Bytesize
    parity: str = Defaults.Parity
    stopbits: int = Defaults.Stopbits
    handle_local_echo: bool = Defaults.HandleLocalEcho


@configclass
class LinkConfig:
    """Class holding a single Modbus link config"""
    timeout: int = Defaults.Timeout
    retries: int = Defaults.Retries
    slave_map: dict[int, int] = field(default_factory=dict)
    tcp: TcpClientConfig = field(default_factory=TcpClientConfig)
    serial: SerialClientConfig = field(default_factory=SerialClientConfig)


@configclass
class Config:
    """Class holding the main mbmux config"""
    address: str = "0.0.0.0"
    port: int = Defaults.TcpPort
    debug: bool = False

    link: list[LinkConfig] = field(default_factory=list)
