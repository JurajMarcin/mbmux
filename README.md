# mbmux

Software multiplexer of Modbus TCP and RTU.

## Installing and Running

To install mbmux and its dependencies run:
```sh
pip install -U .
```

It will also create an entrypoint that can be used to run mbmux from any
directory like this
```sh
mbmux [OPTIONS]
```

## Options

`-h`, `--help`

- show help message and exit

`--debug`

- show debug output on stderr

`--config CONFIG`

- load config from the file `CONFIG` or load config from files in the directory
  `CONFIG` in alphabetical order

## Configuration

By default, config is loaded from files in the directory `/etc/mbmux/` in
alphabetical order.

See `config.toml` for more information about options that can be configured.
