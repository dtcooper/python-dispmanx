from contextlib import contextmanager
import ctypes
from functools import wraps
import logging
from typing import Any, ClassVar, Generator, Literal, NamedTuple, Union


try:
    import numpy
    import numpy.typing
except ImportError:
    HAVE_NUMPY = False
else:
    HAVE_NUMPY = True

from . import bcm_host
from .exceptions import DispmanXError, DispmanXRuntimeError


logger = logging.getLogger("dispmanx")


class Size(NamedTuple):
    """
    Returned by various interactions with the [DismpanX][dispmanx.DispmanX]
    and [Display][dispmanx.dispmanx.Display] classes.

    Not instantiated directly.

    Attribute:
        width int: The width component
        height int: The height component
    """

    width: int
    height: int


class Display(NamedTuple):
    """Returned by various interactions with the [DispmanX][dispmanx.DispmanX] class.

    Not instantiated directly.

    Attributes:
        device_id int:
            The numeric ID associated with this display. You can use this to
            instantiate a [DispmanX][dispmanx.DispmanX] for this display.
        name str: The string representation of this display, for example
            `"Main LCD"`, `"HDMI 0"`, or `"Composite"` to name a few.
        size Size: The size of this display.
    """

    device_id: int
    name: str
    size: Size


class PixelFormat(NamedTuple):
    format: Literal["RGB", "ARGB", "RGBA", "RGBX", "XRGB", "RGBA16", "RGB565"]
    byte_width: int
    vc_image_type: int
    numpy_dtype: Any = numpy.uint8 if HAVE_NUMPY else None


def only_if_not_destroyed(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self._destroyed:
            raise DispmanXError(f"{self.__class__.__name__} object has already been destroyed.")
        return func(self, *args, **kwargs)

    return wrapped


PIXEL_FORMATS = {
    "RGB": PixelFormat("RGB", 3, bcm_host.VC_IMAGE_RGB888),
    "ARGB": PixelFormat("ARGB", 4, bcm_host.VC_IMAGE_ARGB8888),
    "RGBA": PixelFormat("RGBA", 4, bcm_host.VC_IMAGE_RGBA32),
    "RGBX": PixelFormat("RGBX", 4, bcm_host.VC_IMAGE_RGBX8888),
    "XRGB": PixelFormat("XRGB", 4, bcm_host.VC_IMAGE_XRGB8888),
    "RGB565": PixelFormat("RGB565", 2, bcm_host.VC_IMAGE_RGB565, numpy.uint16 if HAVE_NUMPY else None),
    "RGBA16": PixelFormat("RGBA16", 2, bcm_host.VC_IMAGE_RGBA16, numpy.uint16 if HAVE_NUMPY else None)
}


class DispmanX:
    _buffer: Any
    _display_handle: int
    _display: Display
    _has_initialized: ClassVar[bool] = False
    _layer: int
    _pixel_format: PixelFormat
    _surface_element_handle: int
    _video_resource_handle: int

    @classmethod
    def _bcm_host_init(cls) -> None:
        if not cls._has_initialized:
            logger.debug("Initialized bcm_host")
            bcm_host.bcm_host_init()
            cls._has_initialized = True

    def __init__(
        self,
        layer: int = 0,
        display: Union[None, int, Display] = None,
        pixel_format: Literal["RGB", "ARGB", "RGBA", "RGBX", "XRGB", "RGBA16", "RGB565"] = "RGBA",
        buffer_type: Literal["auto", "numpy", "ctypes"] = "auto",
    ):
        """The DispmanX Class

        You can use this class via the following,

        ```python
        from dispmanx import DispmanX

        display = DispmanX()
        ```

        Arguments:
            layer: What layer to choose. For example, the default layer of
                Raspberry Pi OS Lite's terminal is `-127`, while omxplayer is
                `0`.

            display: Which display to use. Choices:

                * `None` &mdash; the default display as returned by
                    [get_default_display()][dispmanx.DispmanX.get_default_display]
                * An [int][] device number of a specific display
                * A [Display][dispmanx.dispmanx.Display] object, for example,
                    returned by [list_displays()][dispmanx.DispmanX.list_displays])

            pixel_format: Pixel format for the object. Choices:

                * `'RGB'` &mdash; 24-bit red, green, and blue
                * `'ARGB'` &mdash; 32-bit alpha, red, green, and blue
                * `'RGBA'` &mdash; 32-bit red, green, blue, and alpha
                * `'RGBX'` &mdash; 32-bit red, green, blue and an unused (`X`) byte
                * `'XRGB'` &mdash; 32-bit an unused (`X`) byte red, green, and blue
                * `'RGBA16'` &mdash; 16-bit red, green, blue and alpha packed as
                    4 bits per channel (represented as unsigned 16-bit integers
                    when using [NumPy][numpy])
                * `'RGB565'` &mdash; 16-bit red, green, blue packed as follows:
                    5 bits red, 6 bits green, 5 bits green (represented as unsigned
                    16-bit integers when using [NumPy][numpy])

            buffer_type: Type of buffer to write to the display from. Choices:

                * `'auto'` &mdash; defaults to a [NumPy array][numpy.array] if
                    [NumPy][numpy] is available, otherwise a [ctypes][]
                    [Array][ctypes.Array] of [c_char][ctypes.c_char] as
                    described below
                * `'numpy'` &mdash; a [NumPy array][numpy.array]
                * `'ctypes` &mdash; a [ctypes][] [Array][ctypes.Array] of
                    [c_char][ctypes.c_char] created with
                    [create_string_buffer()][ctypes.create_string_buffer]

        Raises:
            DispmanXError: A user error occured by specifying an incorrect
                argument.
            DispmanXRuntimeError: A serious error occured with the underlying
                DispmanX layer on your PI.

        Attributes:
            buffer: A buffer representing underlying raw pixel data. It will be
                a [NumPy array][numpy.array] or [ctypes][] [Array][ctypes.Array]
                of [c_char][ctypes.c_char] depending on the value of the
                `buffer_type` argument.
            display Display: The display for which this object is attached to
            pixel_format str: The pixel format for this object.
            size Size: The dimensions of the current display
            width int: The width of the current display
            height int: The height of the current display
        """
        self._destroyed = False
        self._layer = layer
        pixel_format_obj = PIXEL_FORMATS.get(pixel_format)

        if pixel_format_obj is None:
            raise DispmanXError(f"Invalid pixel format: {format}")
        self._pixel_format = pixel_format_obj

        if buffer_type not in ("numpy", "ctypes", "auto"):
            raise DispmanXError(f"Invalid buffer type: {buffer_type}")
        elif buffer_type == "numpy" and not HAVE_NUMPY:
            raise DispmanXError("numpy buffer type requested, but numpy not found!")
        elif buffer_type == "auto":
            buffer_type = "numpy" if HAVE_NUMPY else "ctypes"

        device_id = display.device_id if isinstance(display, Display) else display

        self._bcm_host_init()

        # Select a display (first one by default)
        if device_id is None:
            self._display = self.get_default_display()
        else:
            displays = self.list_displays()

            for display in displays:
                if display.device_id == device_id:
                    self._display = display
                    break
            else:
                raise DispmanXError(f"No display with device ID #{device_id} found!")

        logger.debug(
            f"Using device ID #{self._display.device_id} with resolution"
            f" {self._display.size.width}x{self._display.size.height}"
        )

        handle = bcm_host.vc_dispmanx_display_open(self._display.device_id)
        if handle == 0:
            raise DispmanXRuntimeError(f"Error opening device ID #{self._display.device_id}")
        logger.debug(f"Got display handle: {handle}")
        self._display_handle = handle

        buffer_size = self._display.size.width * self._display.size.height * self._pixel_format.byte_width
        if buffer_type == "numpy":
            pixel_shape = self._pixel_format.byte_width // self._pixel_format.numpy_dtype().nbytes
            array_shape = (self._display.size.height, self._display.size.width, pixel_shape)
            self._buffer = numpy.zeros(shape=array_shape, dtype=self._pixel_format.numpy_dtype)
        else:
            self._buffer = ctypes.create_string_buffer(buffer_size)
        logger.debug(f"Allocated buffer of size {buffer_size} bytes")

        self._create_video_resource_handle()
        self._create_surface_element()

    def __del__(self):
        self.destroy()

    @property  # type: ignore
    @only_if_not_destroyed
    def display(self) -> Display:
        return self._display

    @property  # type: ignore
    @only_if_not_destroyed
    def size(self) -> Size:
        return self._display.size

    @property  # type: ignore
    @only_if_not_destroyed
    def width(self) -> int:
        return self._display.size.width

    @property  # type: ignore
    @only_if_not_destroyed
    def height(self) -> int:
        return self._display.size.height

    @property  # type: ignore
    @only_if_not_destroyed
    def buffer(self) -> Any:
        return self._buffer

    @property  # type: ignore
    @only_if_not_destroyed
    def pixel_format(self) -> Literal["RGB", "ARGB", "RGBA", "RGBX", "XRGB", "RGBA16", "RGB565"]:
        return self._pixel_format.format

    def _create_video_resource_handle(self) -> None:
        self._bcm_host_init()

        unused = ctypes.c_uint32()
        handle = bcm_host.vc_dispmanx_resource_create(
            self._pixel_format.vc_image_type,
            self._display.size.width,
            self._display.size.height,
            ctypes.byref(unused),
        )
        if handle == 0:
            raise DispmanXRuntimeError("Error creating image resource")

        self._video_resource_handle = handle
        logger.debug(f"Created video resource handle: {handle}")

    def _create_surface_element(self) -> None:
        src_width, src_height = self.display.size.width << 16, self.display.size.height << 16
        src_rect = bcm_host.VC_RECT_T(width=src_width, height=src_height, x=0, y=0)
        self._dest_rect = bcm_host.VC_RECT_T(width=self.display.size.width, height=self.display.size.height, x=0, y=0)
        alpha = bcm_host.VC_DISPMANX_ALPHA_T(flags=bcm_host.DISPMANX_FLAGS_ALPHA_FROM_SOURCE, opacity=255, mask=0)

        with self._start_and_submit_update() as update_handle:
            self._surface_element_handle = bcm_host.vc_dispmanx_element_add(
                update_handle,
                self._display_handle,
                self._layer,
                ctypes.byref(self._dest_rect),
                self._video_resource_handle,
                ctypes.byref(src_rect),
                bcm_host.DISPMANX_PROTECTION_NONE,
                ctypes.byref(alpha),
                None,
                bcm_host.DISPMANX_NO_ROTATE,
            )
            if self._surface_element_handle == 0:
                raise DispmanXRuntimeError("Couldn't create surface element")
            logger.debug(f"Got surface element handle: {self._surface_element_handle}")

    @only_if_not_destroyed
    def update(self) -> None:
        """Update the pixels based on what's in the buffer

        Raises:
            DispmanXRuntimeError: Raises if there's an error writing to the
                video memory
        """

        if HAVE_NUMPY:
            buffer = numpy.ctypeslib.as_ctypes(self._buffer)
        else:
            buffer = ctypes.byref(self._buffer)

        if (
            bcm_host.vc_dispmanx_resource_write_data(
                self._video_resource_handle,
                self._pixel_format.vc_image_type,
                self.display.size.width * self._pixel_format.byte_width,
                buffer,
                ctypes.byref(self._dest_rect),
            )
            != 0
        ):
            raise DispmanXRuntimeError("Error writing buffer to video memory")

        with self._start_and_submit_update():
            pass

    @contextmanager
    def _start_and_submit_update(self) -> Generator[int, None, None]:
        update_handle = bcm_host.vc_dispmanx_update_start(0)

        if update_handle == bcm_host.DISPMANX_NO_HANDLE:
            raise DispmanXRuntimeError("Couldn't get update handle")

        yield update_handle

        if bcm_host.vc_dispmanx_update_submit_sync(update_handle) != 0:
            raise DispmanXRuntimeError("Error submitting update")

    @classmethod
    def list_displays(cls) -> list[Display]:
        """Get a list of available [Displays][dispmanx.dispmanx.Display].

        Example:
            ```python
            for display in DispmanX.list_display():
                print(f"{display.device_id}: {display.name}")
            ```

        Returns:
            List of available [Displays][dispmanx.dispmanx.Display].

        Raises:
            DispmanXRuntimeError: Raised if no devices are found, or there's an
                error while getting the list of displays.
        """
        cls._bcm_host_init()
        devices = bcm_host.TV_ATTACHED_DEVICES_T()

        if bcm_host.vc_tv_get_attached_devices(ctypes.byref(devices)) != 0:
            raise DispmanXRuntimeError("Error getting attached devices")

        response = []

        for i in range(devices.num_attached):
            display_id = devices.display_number[i]
            size = cls._get_display_size(display_id)
            response.append(Display(display_id, devices.get_display_text(display_id), size))

        return response

    @classmethod
    def get_default_display(cls) -> Display:
        """Get the default [Display][dispmanx.dispmanx.Display].

        This is both the first display returned by DispmanX layer, and the one
        used when creating [DispmanX][dispmanx.DispmanX] objects by default.

        Returns:
            The default [Display][dispmanx.dispmanx.Display].
        """
        displays = cls.list_displays()
        if len(displays) == 0:
            raise DispmanXRuntimeError("No displays found!")
        return displays[0]

    @classmethod
    def _get_display_size(cls, display_id) -> Size:
        cls._bcm_host_init()
        width, height = ctypes.c_uint32(), ctypes.c_uint32()
        if bcm_host.graphics_get_display_size(display_id, ctypes.byref(width), ctypes.byref(height)) < 0:
            raise DispmanXRuntimeError(f"Error getting display #{display_id} size")

        return Size(width.value, height.value)

    def destroy(self) -> None:
        """Destroy this DispmanX object

        Raises:
            DispmanXRuntimeError: Raised if there's an error destroying any of
                the underlying resources for the object
        """
        if not self._destroyed:
            with self._start_and_submit_update() as update_handle:
                if bcm_host.vc_dispmanx_element_remove(update_handle, self._surface_element_handle) != 0:
                    raise DispmanXRuntimeError("Couldn't destroy surface element")

            if bcm_host.vc_dispmanx_resource_delete(self._video_resource_handle) != 0:
                raise DispmanXRuntimeError("Error destroying image resource")

            self._destroyed = True
