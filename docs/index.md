# Welcome to Python DispmanX

This is a Python library for interacting with the Raspberry Pi's DispmanX video
API.

## Quickstart

Install the [dispmanx][dispmanx-pypi] package using [pip][pip],

```bash
pip install pygame dispmanx[numpy]
```

And try this sample program using [pygame][pygame],

```python title="test.py"
--8<-- "test.py"
```

## Use Cases

Some use cases for this library are,

1. Directly writing to the lowlevel graphics layer of your Pi with relatively high
   performance (for Python). There's no need to install X11.
2. Small pygame or Pillow-based applications can be overlayed onto the screen, with
   full support for transparency.

[dispmanx-pypi]: https://pypi.org/project/dispmanx/
[pip]: https://pip.pypa.io/
[pygame]: https://www.pygame.org/docs/
