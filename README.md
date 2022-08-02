# Python Wrapper for the Raspberry Pi's DispmanX API

This is a Python library for interacting with the Raspberry Pi's DispmanX video
API. Some use cases for this are,

  * Directly writing to the lowlevel graphics layer of your Pi with relatively
    high performance (for Python). There's no need to install X11.
  * Small [pygame][pygame] or [Pillow][pillow]-based applications can overlayed
    onto the screen, with full support for transparency.

This library uses [ctypes][ctypes] to directly interact with your Raspberry Pi's
`bcm_host.so` library.

## Usage

Documentation forthcoming. For now, test it out on your Pi by running the
following,

```bash
# Download dispmanx, optionally using numpy: pip install dispmanx[numpy]
pip install dispmanx

# Download and run test.py
wget https://raw.githubusercontent.com/dtcooper/python-dispmanx/main/test.py
python test.py
```

## TODO List

- [x] Publish package to [PyPI][pypi]
- [ ] Add API docs using [MkDocs][mkdocs], [Material for MkDocs][mkdocs-material],
    and [mkdocstrings][mkdocstrings]
- [ ] Allow multiple layers
- [ ] Support additional pixel types
- [ ] Support custom dimensions and offsets – API supports it, but requires weird
    multiples of 16 or 32, [as documented here](picamera-overlay-docs). This
    requires testing, because anecdotally it seems to work with smaller multiples.


[ctypes]: https://docs.python.org/3/library/ctypes.html
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mkdocs]: https://www.mkdocs.org/
[mkdocstrings]: https://mkdocstrings.github.io/
[picamera-overlay-docs]: https://picamera.readthedocs.io/en/release-1.13/api_renderers.html#picamera.PiOverlayRenderer
[pillow]: https://pillow.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
[pypi]: https://pypi.org/
