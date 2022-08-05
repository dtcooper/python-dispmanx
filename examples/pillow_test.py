import time
from random import randint
import numpy
from PIL import Image, ImageDraw
from dispmanx import DispmanX

def random_color_with_alpha():
    return tuple(randint(0, 0xFF) for _ in range(3)) + (randint(0x44, 0xFF),)

display = DispmanX(format="RGBA", buffer_type="numpy")
image = Image.new(mode=display.format, size=display.size)
draw = ImageDraw.Draw(image)

for _ in range(20):
    draw.rectangle(((0, 0), (image.size)), fill=random_color_with_alpha())
    numpy.copyto(display.buffer, image)
    display.update()
    time.sleep(0.5)
