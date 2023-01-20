---
title: Intro
---

# Welcome to Python DispmanX

Hello and welcome! Here's the documentation for Python DispmanX, a pure
Python[^1] library for interacting with the Raspberry Pi's low-level video API.
My hope is that you find it useful for creating all sorts of different apps,
widgets, and graphical overlays for your Pi. _I hope you'll have as much fun
using it as I did writing it!_

<!-- I guess the API is stable now?
!!! warning "A Word of Caution"
    Currently, **Python DispmanX is under development**.

    While the API has _mostly_ stabilized, it's recommended that you install the
    latest version from source, described below in the [installation][installation]
    section.

    This documentation may not reflect the latest changes, or may include changes
    that are not yet available on [PyPI]. _Beware!_
-->

## Quickstart

Follow the steps below to install the [DispmanX library][dispmanx-pypi] and run
your first program using this library.

### Installation

!!! note "Installation"

    To install the [DispmanX library][dispmanx-pypi] from the
    [Python Package Index (PyPI)][pypi], type the following at the command line,

    === "With NumPy support"
        ```bash
        # Install DispmanX with optional (and recommended) NumPy support
        pip install dispmanx[numpy]
        ```

        !!! danger "Installing From Source Recommended"
            Until the API stabilizes, it's recommended that you install the
            latest version from source, described in the _"From Source With
            NumPy"_ content tab above.
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

??? failure "If you see a `DispmanXRuntimeError: No displays found!` exception"
    If you run into the following  `DispmanXRuntimeError` running the code
    above,

    ```pycon
    >>> from dispmanx import DispmanX
    >>> display = DispmanX()
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/david/python-dispmanx/dispmanx/dispmanx.py", line 205, in __init__
        self._display = self.get_default_display()
    File "/home/david/python-dispmanx/dispmanx/dispmanx.py", line 421, in get_default_display
        raise DispmanXRuntimeError("No displays found! (Are you using the vc4-kms-v3d driver?)")
    dispmanx.exceptions.DispmanXRuntimeError: No displays found! (Are you using the vc4-kms-v3d driver?)
    ```

    Then you'll need to follow
    [the instructions here][fixing-no-displays-found-exception] to address the
    issue.


More examples are available on the [recipes](recipes.md) page.

## Use Cases

You may be asking why this library, when you could just [pygame]? Here are some
potential use cases:

Transparent iverlays
:   You may want to your program to have **transparent overlays.** [pygame] and
    [SDL] do not support them by default. With this library, you can write code
    that does just that![^2]

Running in a headless environment
:   [pygame] using its underlying [SDL] library requires either X11 or fbcon
    drivers on the Pi. While using the X11 driver works great, it requires a
    full desktop environment on your Pi. Furthermore, the fbcon driver appears
    to no longer be supported by [pygame] version 2. This library allows you to
    use familiar [pygame] idioms with the Raspberry Pi's native DispmanX layer.

Using raw [NumPy arrays][numpy.array]
:   You may want to directly interact with [NumPy arrays][numpy.array] of RGBA
    (or RGB) pixels with arbitrary imaging tool kits like [Pillow] or
    [Cairo][pycairo]. Some examples of using raw [NumPy arrays][numpy.array] are
    available on the [recipes page](recipes.md).

My use case is retro style CRT TV hooked up to a Pi using the Pi-specific video
player [omxplayer][omxplayer] complete with semi-transparent overlays for
menus, "channels," and subtitles[^3].

## What's Next?

* Check out some [code recipes](recipes.md) that will show you how to use
    DispmanX with [pygame], [Pillow], [Pycairo], and plain [NumPy][numpy].
* Head over to the [API documentation](api.md) and read about the
    [DispmanX class][dispmanx.DispmanX], the main entrypoint for this library.
* Read some of the [additional information](more-info.md) about this library.

[^1]: I say "pure Python" however this library uses Python's included [ctypes][]
    library to perform "foreign function calls" to `bcm_host.so` &mdash; a C
    library included with Raspberry Pi OS to interface with the DispmanX layer
    directly.
[^2]: Fun fact, transparent overlays is the reason I wrote this package.
[^3]: While [omxplayer] does technically support subtitles, they
    [don't seem to be working on the Raspberry Pi 4B][omxplayer-subtitles-bug].
    And besides, I wanted to render custom subtitles.


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
