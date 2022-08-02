<h1 align="center">
  <a href="https://dtcooper.github.io/python-dispmanx/">DispmanX Bindings for Python</a>
</h1>

<p align="center">
  <a href="https://dtcooper.github.io/python-dispmanx/">Documentation</a> |
  <a href="https://pypi.org/project/dispmanx/">Python Package Index</a>
</p>

This is a Python library for interacting with the Raspberry Pi's DispmanX video
API. Some use cases for this are,

  * Directly writing to the lowlevel graphics layer of your Pi with relatively
    high performance (for Python). There's no need to install X11.
  * Small [pygame][pygame] or [Pillow][pillow]-based applications can be overlayed
    onto the screen, with full support for transparency.

This library uses [ctypes][ctypes] to directly interact with your Raspberry Pi's
`bcm_host.so` library.

## Usage

See the [Quickstart section in the docs][quickstart].

## TODO List

- [x] Publish package to [PyPI][pypi]
- [ ] Add API docs using [MkDocs][mkdocs], [Material for MkDocs][mkdocs-material],
    and [mkdocstrings][mkdocstrings]
- [ ] Allow multiple layers
- [ ] Support additional pixel types
- [ ] Support custom dimensions and offsets – API supports it, but requires weird
    multiples of 16 or 32, [as documented here](picamera-overlay-docs). This
    requires testing, because anecdotally it seems to work with smaller multiples.
- [ ] Test run over SSH onto my home pi


[ctypes]: https://docs.python.org/3/library/ctypes.html
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mkdocs]: https://www.mkdocs.org/
[mkdocstrings]: https://mkdocstrings.github.io/
[picamera-overlay-docs]: https://picamera.readthedocs.io/en/release-1.13/api_renderers.html#picamera.PiOverlayRenderer
[pillow]: https://pillow.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
[pypi]: https://pypi.org/
[quickstart]: https://dtcooper.github.io/python-dispmanx/#quickstart
