import numpy
from dispmanx import DispmanX

display = DispmanX(pixel_format="RGB565")

buf = display.buffer
high = numpy.iinfo(buf.dtype).max + 1

while True:
    # Generate random colors, simulating static
    static = numpy.random.randint(0, high, size=buf.size, dtype=buf.dtype).reshape(buf.shape)
    numpy.copyto(buf, static)
    display.update()
