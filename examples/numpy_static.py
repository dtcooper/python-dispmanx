import numpy
from dispmanx import DispmanX

display = DispmanX(pixel_format="RGB565")

dtype, size, shape = display.buffer.dtype, display.buffer.size, display.buffer.shape
random_high = numpy.iinfo(dtype).max + 1

while True:
    # Generate random colors, simulating static
    static = numpy.random.randint(0, random_high, size=size, dtype=dtype).reshape(shape)
    numpy.copyto(display.buffer, static)
    display.update()
