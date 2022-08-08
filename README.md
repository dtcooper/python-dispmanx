<h1 align="center">
  <a href="https://dtcooper.github.io/python-dispmanx/">DispmanX Bindings for Python</a>
</h1>

<p align="center">
  <a href="https://dtcooper.github.io/python-dispmanx/">Documentation</a> |
  <a href="https://pypi.org/project/dispmanx/">Python Package Index</a>
</p>

## Usage

Install with pip,

```bash
pip install dispmanx
```

Then see the [Quickstart section in the docs][quickstart].

## TODO List

- [x] Publish package to PyPI
- [x] Add API docs using MkDocs, Material for MkDocs, mkdocstrings
- [x] Call destroy functions in bcm_host.h
- [x] Support additional pixel types
- [ ] Allow multiple layers, and different displays
- [ ] Support custom dimensions and offsets – API supports it, but requires weird
    multiples of 16 or 32, [as documented here][picamera-overlay-docs]. This
    requires testing, because anecdotally it seems to work with smaller multiples.
- [ ] Tests run over SSH onto my home pi (github runners won't do)

[picamera-overlay-docs]: https://picamera.readthedocs.io/en/release-1.13/api_renderers.html#picamera.PiOverlayRenderer
[quickstart]: https://dtcooper.github.io/python-dispmanx/#quickstart
