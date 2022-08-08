---
title: Recipes
---

# Code Recipes

Below are a few code recipes for [pygame], [Pillow], and [Pycairo] to get you
started. If you need help installing the library, check out the
[Quickstart][quickstart] section!

## [pygame] Example

First install [pygame],

```bash
pip install pygame
```

Then run this program,

```python title="pillow_test.py"
--8<-- "pygame_test.py"
```

## [Pillow] Example

!!! tip "[NumPy] Required"
    For this example to work correctly, ensure you've installed
    [NumPy][]. The easiest way to do that with [pip] is:
    `#!bash pip install dispmanx[numpy]`

First install [Pillow],

```bash
pip install Pillow
```

Then run this program,

```python title="pillow_test.py"
--8<-- "pillow_test.py"
```

!!! warning "A Note About Performance"
    This example includes copying an RGBA array of pixels from a Pillow
    rendering, rather than editing an array in-place like the other examples.
    This is inherently slow, so you're not going to get as high frame rates as
    in the [pygame] example.

    If you know a way to do in-place modification of numpy arrays with Pillow, open
    let me know by filing a GitHub issue!

## [Pycairo] Example

First install [Pycairo],

```bash
pip install pycairo
```

Then run this program,

```python title="pycairo_test.py"
--8<-- "pycairo_test.py"
```

## What's Next?

Now that you're an expert, check out the [API documentation](api.md).

[numpy]: https://numpy.org/doc/stable/
[pillow]: https://pillow.readthedocs.io/
[pip]: https://pip.pypa.io/
[pycairo]: https://pycairo.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
