---
title: Intro
nav_title: fuck
---

!!! danger "A Word of Caution"
    Currently, **Python DispmanX is under active development**. This
    documentation may not reflect the latest changes, or may include changes
    that are not yet available on [PyPI]. _Beware!_

    Until the API stabilizes, it's recommended that you install the latest
    version from source, described below in the [installation][installation]
    section.

# Welcome to Python DispmanX

Hello and welcome to the documentation for Python DispmanX, a pure Python[^1]
library for interacting with the Raspberry Pi's low-level video API. My hope is
that you find it useful for creating all sorts of different apps, widgets, and
graphical overlays for your Pi. I hope you have as much using it as I did
writing it!

## Quickstart

Follow the steps below to install the [DispmanX package][dispmanx-pypi] and run
your first program using this library!

### Installation

!!! note "Installation"

    To install the [DispmanX package][dispmanx-pypi] from the
    [Python Package Index (PyPI)][pypi], type the following at the command line,

    === "With NumPy support"
        ```bash
        # Install DispmanX with optional (and recommended) NumPy support
        pip install dispmanx[numpy]
        ```

        !!! danger "Installing From Source Recommended"
            Until the API stabilizes, it's recommended that you install the
            latest version from source, described in the _"From Source With
            NumPy"_ content tab.
    === "From Source with NumPy"
        ```bash
        # Or install directly from the latest developmental sources with NumPy support
        pip install git+https://github.com/dtcooper/python-dispmanx.git#egg=dispmanx[numpy]
        ```
    === "Without NumPy"
        ```bash
        # Install DispmanX without NumPy
        pip install dispmanx
        ```
    === "From Source Without NumPy"
        ```bash
        # Or install directly from the latest developmental sources without NumPy
        pip install git+https://github.com/dtcooper/python-dispmanx.git
        ```

### [pygame] Example

To get going with your first [pygame] program, first install the library,

```bash
pip install pygame
```

Then try this out,

```python title="pygame_test.py"
--8<-- "pygame_test.py"
```

More examples are available on the [recipes](recipes.md) page.

## Use Cases

You may be asking why this library, when you could just [pygame]? Here are some
potential use cases.

* [pygame] using its underlying [SDL] library requires either X11 or fbcon
    drivers. X11 is great, but it requires a desktop environment on your Pi. And
    fbcon appears to no longer supported by [pygame] version 2. This library
    allows you to use familiar [pygame] idioms with the Raspberry Pi's native
    DispmanX layer.
* You may want to your program to have **transparent overlays.** [pygame] and
    [SDL] do not support them by default. With this package, you can do write
    something that does just that![^2]
* You may want to directly interact with [NumPy][numpy] arrays of RGBA (or RGB)
    pixels with arbitrary imaging tool kits like [Pillow] or [Cairo][pycairo].

My use case is retro style CRT TV hooked up to a Pi using the Pi-specific video
player [omxplayer][omxplayer] complete with and semi-transparent overlays for
menus, "channels," and subtitles[^3].

## What's Next?

* Check out some [code recipes](recipes.md) that will show you how to use
    DispmanX with [pygame], [Pillow], and [Pycairo].
* Head over to the [API documentation](api.md) and read about the
    [DispmanX class][dispmanx.DispmanX], the main entrypoint for this package.
* Check out some [additional information](info.md) about this package.

[^1]: I say "pure Python" however this package uses Python's included [ctypes][]
    library perform "foreign function calls" to `bcm_host.so` &mdash; a C
    library included with Raspberry Pi OS to interface with the DispmanX layer
    directly.
[^2]: Fun fact, transparent overlays is the reason I wrote this package.
[^3]: While [omxplayer] does supports subtitle, but they
    [don't seem to be working on the Raspberry Pi 4B][omxplayer-subtitles-bug].
    And anyways, I wanted to render custom subtitles anyway.

[dispmanx-pypi]: https://pypi.org/project/dispmanx/
[omxplayer-subtitles-bug]: https://github.com/popcornmix/omxplayer/issues/736
[omxplayer]: https://github.com/popcornmix/omxplayer
[pi-os]: https://www.raspberrypi.com/software/
[pillow]: https://pillow.readthedocs.io/
[pip]: https://pip.pypa.io/
[pycairo]: https://pycairo.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
[pypi]: https://pypi.org/
[sdl]: https://www.libsdl.org/
