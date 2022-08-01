# Python Wrapper for the Raspberry Pi's DispmanX API

This is a Python library for interacting with a buffer using the DispmanX.

## Usage

Documentation forthcoming. For now, test it out on your Pi by running the
following,

```bash
git clone https://github.com/dtcooper/python-dispmanx.git
cd python-dispmanx

# A quick demo using pygame
python test.py
```

## TODO List

- [ ] Publish package to [PyPI][pypi]
- [ ] Add API docs using [MkDocs][mkdocs], [Material for MkDocs][mkdocs-material],
    and [mkdocstrings][mkdocstrings]
- [ ] Allow multiple layers
- [ ] Support additional pixel types
- [ ] Support custom dimensions and offsets – API supports it, but requires weird
    multiples of 16 or 32, [as documented here](picamera-overlay-docs). This
    requires testing, because anecdotally it seems to work with smaller multiples.


[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mkdocs]: https://www.mkdocs.org/
[mkdocstrings]: https://mkdocstrings.github.io/
[picamera-overlay-docs]: https://picamera.readthedocs.io/en/release-1.13/api_renderers.html#picamera.PiOverlayRenderer
[pypi]: https://pypi.org/
