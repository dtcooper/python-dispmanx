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
