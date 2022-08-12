import time
import numpy
from dispmanx import DispmanX

import numpy

display = DispmanX(pixel_format="RGB565", buffer_type="numpy")
high = numpy.iinfo(display.buffer.dtype).max + 1  # white pixel
rng = numpy.random.default_rng()

while True:
    static = rng.integers(low=0, high=high, size=display.buffer.shape, dtype=display.buffer.dtype)
    numpy.copyto(display.buffer, static)  # Simulates TV static
    display.update()
    time.sleep(0.0135)
