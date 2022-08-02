import pygame
from dispmanx import DispmanX


colors = ('#fc49ab', '#5fe8ff', '#c07eec', '#fbbd23', '#ffee00', '#36d399')
display = DispmanX(format="RGBA")
surface = pygame.image.frombuffer(display.buffer, display.size, display.format)
clock = pygame.time.Clock()

for num, color in enumerate(colors, 1):
    # Scale opacity from 0 to 0xFF
    surface.fill(pygame.Color(f'{color}{num * 0xFF // len(colors):x}'))
    display.update()
    clock.tick(2)
