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

- load config from the file `CONFIG` or use the directory `CONFIG` as a config
  prefix (i.e. if `CONFIG` is a directory, `CONFIG/config.toml` and files in
  `CONFIG/config.d/` will be loaded)

## Configuration

By default, config is loaded from files in the directory `/etc/mbmux/` in
alphabetical order.

See `CONFIGURATION.md` for all description of all config options or `config.tml`
for a simple example.
