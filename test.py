import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame

from dispmanx import Dispmanx


print("Found displays:")
for display in Dispmanx.list_displays():
    print(f" * #{display.device_id} ({display.name}) - {display.size.width}x{display.size.height}")
print()

dispmanx = Dispmanx()
print(
    f"Using display #{dispmanx.display.device_id} - {dispmanx.size.width}x{dispmanx.size.height} with"
    f" {dispmanx.format} format"
)
print("Running demo...")

width, height = dispmanx.size
surface = pygame.image.frombuffer(dispmanx.buffer, dispmanx.size, dispmanx.format)

bg_color = (0xFF, 0xEE, 0x00)
circle_color = (0x5F, 0xE8, 0xFF)
x_color = (0xFC, 0x49, 0xAB)
square_length = 50
circle_radius = 100
line_width = 10

clock = pygame.time.Clock()

for opacity in reversed(range(0, 256)):
    surface.fill(bg_color + (opacity,))

    pygame.draw.circle(surface, circle_color, (width / 2, height / 2), circle_radius, line_width)
    pygame.draw.line(surface, x_color, (0, height - 1), (width - 1, 0), line_width)
    pygame.draw.line(surface, x_color, (0, 0), (width - 1, height - 1), line_width)

    dispmanx.update()
    clock.tick(24)

print("Demo complete. Exiting")
