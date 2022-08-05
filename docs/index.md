---
title: Intro
---

!!! danger "A Word of Caution"
    Currently, **Python DispmanX is under active development**. This
    documentation may not reflect the latest changes, or may include changes
    that are not yet available on [PyPI][]. _Beware!_

    It's recommended that you at least install the latest version from
    source, described below in the [installation][installation] section.

# Welcome to Python DispmanX

Hello and welcome to the documentation for Python DispmanX, a pure Python[^1]
package for interacting with the Raspberry Pi's low-level video API. My hope is
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
    === "From source with NumPy"
        ```bash
        # Or install directly from the latest developmental sources with NumPy support
        pip install git+https://github.com/dtcooper/python-dispmanx.git#egg=dispmanx[numpy]
        ```
    === "Without NumPy"
        ```bash
        # Install DispmanX without NumPy
        pip install dispmanx
        ```
    === "From source without NumPy"
        ```bash
        # Or install directly from the latest developmental sources without NumPy
        pip install git+https://github.com/dtcooper/python-dispmanx.git
        ```

### Code Examples

!!! example "Examples"

    Below are a few example programs to get you started using [pygame][],
    [Pillow][], or [Pycairo][].

    === "pygame Example"
        Install [pygame][],

        ```bash
        pip install pygame
        ```

        Then try out this sample program,

        ```python title="pygame_test.py"
        --8<-- "pygame_test.py"
        ```

    === "Pillow example"
        !!! tip "NumPy Required"
            For this example to work correctly, ensure you've installed
            [NumPy][]. The easiest way to do that with [pip] is:
            `#!bash pip install dispmanx[numpy]`

        Install [Pillow][],

        ```bash
        # NumPy is required for this example
        pip install pillow
        ```

        Then try out this sample program,

        ```python title="pillow_test.py"
        --8<-- "pillow_test.py"
        ```

    === "Pycairo Example"
        Install [Pycairo][],

        ```bash
        pip install pycairo
        ```

        Then try out this sample program,

        ```python title="pycairo_test.py"
        --8<-- "pycairo_test.py"
        ```

## Use Cases

You may be asking why this library, when you could just [pygame][]? Here's
some potential use cases.

* [pygame][] using its underlying [SDL][] library requires either X11
    or fbcon drivers. X11 is great, but it requires a desktop environment on
    your Pi. And fbcon appears to no longer supported by [pygame][]
    version 2. This library allows you to use familiar [pygame][] idioms
    with the Raspberry Pi's native DispmanX layer.
* You may want to your program to have **transparent overlays.**
    [pygame][] and [SDL][] do not support them by default. With this
    package, you can do write something that does just that![^2]
* You may want to directly interact with [NumPy][] arrays of RGB or RBGA
    pixels with arbitrary imaging tool kits like [Pillow][] or
    [Cairo][pycairo].

My use case is retro style CRT TV hooked up to a Pi using the Pi-specific video
player [omxplayer][omxplayer] complete with and semi-transparent overlays for
menus, "channels," and subtitles[^3].

## What's Next?

* Check out some [code recipes](recipes.md) that will show you how to use
    DispmanX.

* Head over to the [API documentation](api.md) and read about the
    [dispmanx.DispmanX][] class, the main entrypoint for this package.

* Check out some [additional information](info.md) about this package.

[^1]: I say "pure Python" however this package uses the Python's included
    [ctypes][] library perform "foreign function calls" to `bcm_host.so`
    &mdash; a C library included with Raspberry Pi OS to interface with the
    DispmanX layer directly.
[^2]: Fun fact, transparent overlays is the reason I wrote this package.
[^3]: While [omxplayer][] does supports subtitle, but they
    [don't seem to be working on the Raspberry Pi 4B][omxplayer-subtitles-bug].
    And anyways, I wanted to render custom subtitles anyway.

[dispmanx-pypi]: https://pypi.org/project/dispmanx/
[numpy]: https://numpy.org/doc/stable/
[omxplayer-subtitles-bug]: https://github.com/popcornmix/omxplayer/issues/736
[omxplayer]: https://github.com/popcornmix/omxplayer
[pi-os]: https://www.raspberrypi.com/software/
[pillow]: https://pillow.readthedocs.io/
[pip]: https://pip.pypa.io/
[pycairo]: https://pycairo.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
[pypi]: https://pypi.org/
[sdl]: https://www.libsdl.org/
