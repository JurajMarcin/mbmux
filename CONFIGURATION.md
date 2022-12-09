# Configuration

Some defaults depend on the [PyModbus library](https://pymodbus.readthedocs.io/en/latest/source/library/pymodbus.constants.html).

## Main Configuration

    address: str = "0.0.0.0"

Address the Modbus/TCP server binds to.

    port: int = Defaults.TcpPort

Port the Modbus/TCP server binds to.

    debug: bool = False

Print debug information to `stderr`.

    link: list[LinkConfig] = []

List of link configurations.

## `LinkConfig`

Configuration of a single link.

    timeout: int = Defaults.Timeout

Timeout of the client in seconds.

    retries: int = Defaults.Retries

Number of retries the client should try before failing

    tcp: TcpClientConfig = TcpClientConfig()

Configuration of the TCP client

    serial: SerialClientConfig = SerialClientConfig()

Configuration of the Serial client.
If both TCP and Serial client are defined, TCP client is used.

    slave_map: dict[int, int] = {}

Map of Modbus slave ids.
Id in the incoming request is used as key and id in the outgoing request is
value from the map.
If the id is not found in the map, it is left intact.

### `TcpClientConfig`

    rtu: bool = False

Use RTU over TCP.

    host: str = ""

Address of the target Modbus device.

    port: int = Defaults.TcpPort

Port on the target Modbus device.

### `SerialClientConfig`

    port: str = ""

Serial port path.

    ascii: bool = False

Use Serial ASCII.

    baudrate: int = Defaults.Baudrate
    bytesize: int = Defaults.Bytesize

Number of bits per byte (7 - 8).

    parity: str = Defaults.Parity

Parity checks (`"E"`ven, `"O"`dd or `"N"`one).

    stopbits: int = Defaults.Stopbits

Number of stop bits (0 - 2).

    handle_local_echo: bool = Defaults.HandleLocalEcho

Discard local echo.
