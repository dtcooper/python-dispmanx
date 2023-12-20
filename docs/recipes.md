---
title: Recipes
---

# Code Recipes

Below are a few code recipes for [pygame], [Pillow], [Pycairo], and
plain [NumPy][numpy] to get you started. If you're unsure how to install this
library, check out the [installation section][installation].

## [pygame] Example

First install [pygame],

```bash
pip install pygame
```

Then run this program,

```python title="pygame_test.py"
--8<-- "pygame_test.py"
```

## [Pillow] Example

!!! tip "[NumPy][numpy] Required"
    For this example to work correctly, ensure you've installed
    [NumPy][numpy]. The easiest way to do that with [pip] is:
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

    If you know a way to do in-place modification of numpy arrays with Pillow,
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

## [NumPy][numpy] Example

All you need is [NumPy][numpy] for this one. First, install it,

```bash
pip install numpy
```

Then run this program to create a fake static effect,

```python title="numpy_static.py"
--8<-- "numpy_static.py"
```

## What's Next?

Now that you're an expert, check out the [API documentation](api.md).

[pillow]: https://pillow.readthedocs.io/
[pip]: https://pip.pypa.io/
[pycairo]: https://pycairo.readthedocs.io/
[pygame]: https://www.pygame.org/docs/
