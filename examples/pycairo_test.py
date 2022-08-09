from random import uniform
import time
from cairo import ImageSurface, FORMAT_RGB24, Context
from dispmanx import DispmanX

def random_color():
    return tuple(uniform(0, 1) for _ in range(3))

display = DispmanX(pixel_format="RGBX")
width, height = display.size
surface = ImageSurface.create_for_data(display.buffer, FORMAT_RGB24, width, height)
context = Context(surface)

for _ in range(20):
    context.set_source_rgba(*random_color())
    context.rectangle(0, 0, display.width - 1, display.height - 1)
    context.fill()
    display.update()
    time.sleep(0.5)
