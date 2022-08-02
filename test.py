import os
import random


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402

from dispmanx import DispmanX  # noqa: E402


def random_color():
    return tuple(random.randint(0, 0xFF) for _ in range(3))


print("Found displays:")
for display in DispmanX.list_displays():
    print(f" * #{display.device_id} ({display.name}) - {display.size.width}x{display.size.height}")
print()

dispmanx = DispmanX()
print(
    f"Using display #{dispmanx.display.device_id} - {dispmanx.size.width}x{dispmanx.size.height} with"
    f" {dispmanx.format} format"
)
print("Running demo...")

width, height = dispmanx.size
surface = pygame.image.frombuffer(dispmanx.buffer, dispmanx.size, dispmanx.format)

bg_color = random_color()
circle_color = random_color()
x_color = random_color()

square_length = 60
circle_radius = 100
line_width = 25

clock = pygame.time.Clock()

for fade_out in (False, True) * 10:
    for opacity in reversed(range(0, 256)) if fade_out else range(0, 256):
        surface.fill(bg_color + (opacity,))

        pygame.draw.line(surface, x_color, (0, height - 1), (width - 1, 0), line_width)
        pygame.draw.line(surface, x_color, (0, 0), (width - 1, height - 1), line_width)
        pygame.draw.circle(surface, circle_color, (width / 2, height / 2), circle_radius, line_width)
        dispmanx.update()
        clock.tick(150)
    if fade_out:
        bg_color = random_color()
    print(f"FPS: {clock.get_fps()}")

print("Demo complete. Exiting")
