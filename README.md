# tile-operator

## usage

### CLI

#### tile download

```bash
$ python to.py -v download https://tile.openstreetmap.jp/{z}/{x}/{y}.png tests/data/test.geojson 18

Tile Download

 Options:
  tile_url=https://tile.openstreetmap.jp/{z}/{x}/{y}.png
  file_path=tests/data/test.geojson
  zoom_level=18


100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 30/30 [00:05<00:00,  5.11it/s]
```

#### help

```bash
$ python to.py --help        
Usage: to.py [OPTIONS] COMMAND [ARGS]...

  Tile operator v0.0.1

Options:
  --version                 Show the version and exit.
  -v, --verbose             verbose mode
  --help                    Show this message and exit.

Commands:
  operate  Tile Operation
```

### python

- install

```bash
$ pip install tile-operator
```

```python
from tile_operator.operate import TileOperate

to = TileOperate(
    tile_url="https://tile.openstreetmap.jp/{z}/{x}/{y}.png",
    file_path="tests/data/test.geojson",
    zoom_level=18,
)
to.set_tile_list()
to.download_all_tiles()
```

## test

```bash
$ pytest -qs tests
```

## development

### setup

```bash
$ poetry config virtualenvs.in-project true
$ pyenv global 3.9 # Version 3.7 or higher will work, but 3.9 is recommended.
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install --upgrade pip
$ poetry install
$ poetry shell
```

### publish

```bash
$ poetry build
$ poetry publish
```
