import numpy
from dispmanx import DispmanX

display = DispmanX(pixel_format="RGB565")

buffer = display.buffer
high = numpy.iinfo(buffer.dtype).max + 1

while True:
    # Generate random colors, simulating static
    static = numpy.random.randint(0, high, buffer.size, buffer.dtype).reshape(buffer.shape)
    numpy.copyto(buffer, static)
    display.update()
