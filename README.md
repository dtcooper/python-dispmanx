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

Then try out this sample program using [pygame](https://www.pygame.org/docs/),

```python
from random import randint
import pygame
from dispmanx import DispmanX

def random_color_with_alpha():
    return tuple(randint(0, 0xFF) for _ in range(3)) + (randint(0x44, 0xFF),)

display = DispmanX(pixel_format="RGBA")
surface = pygame.image.frombuffer(display.buffer, display.size, display.pixel_format)
clock = pygame.time.Clock()

for _ in range(20):
    surface.fill(random_color_with_alpha())
    display.update()
    clock.tick(2)

```

Next stop: [the project's documentation](https://dtcooper.github.io/python-dispmanx/).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
&mdash; see the [LICENSE](https://github.com/dtcooper/python-dispmanx/blob/main/LICENSE)
file for details.

## Final Note

**_...and remember kids, have fun!_**
