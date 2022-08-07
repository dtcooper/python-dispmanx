from contextlib import contextmanager
import ctypes as ct
import logging
from typing import ClassVar, Generator, Literal, NamedTuple, Union, Optional


try:
    import numpy
    import numpy.typing
except ImportError:
    HAVE_NUMPY = False
else:
    HAVE_NUMPY = True

from . import bcm_host as bcm


logger = logging.getLogger("dispmanx")


class DispmanXRuntimeError(RuntimeError):
    """Raised when an **irrecoverable** error occurs with the underlying DispmanX library.

    Under normal circumstances, you should destroy any [DispmanX][dispmanx.DispmanX]
    objects you've instantiated when one of these occurs. Or, your program should
    cleanly exit.
    """
    pass


class DispmanXError(Exception):
    """Raised when a **recoverable** error occurs with the underlying DispmanX library.

    Likely a programmer error. You can try whatever you were doing again and
    correcting the offending behavior."""
    pass


class Size(NamedTuple):
    width: int
    height: int


class Display(NamedTuple):
    """
    Not instantiated directly. Returned by various methods and classmethods on
    the DispmanX object.

    Attributes:
        device_id int: Test
        name str: Test
        size Size: test
    """
    device_id: int
    name: str
    size: Size


class DispmanX:
    _display_handle: int
    _display: Display
    _layer: int
    _has_initialized: ClassVar[bool] = False
    _surface_element_handle: int
    _video_resource_handle: int

    @classmethod
    def _bcm_host_init(cls) -> None:
        if not cls._has_initialized:
            logger.debug("Initialized bcm_host")
            bcm.bcm_host_init()
            cls._has_initialized = True

    def __init__(
        self,
        layer: int = 0,
        display: Optional[Union[int, Display]] = None,
        format: Literal["RGBA", "RGB", "ARGB", "RGBX"] = "RGBA",
        buffer_type: Literal["numpy", "ctypes", "auto"] = "auto",
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
            format: Pixel format for the object. Choices:

                * `'RGBA'` &mdash; 32-bit red, green, blue, and alpha
                * `'RGB'` &mdash; 24-bit red, green, and blue
                * `'ARGB'` &mdash; 32-bit alpha, red, green, and blue
                * `'RGBX'` &mdash; 32-bit red, green, blue and an unused (`X`) byte

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
            size Size: The dimensions of the current display
            width int: The width of the current display
            height int: The height of the current display
        """
        self._bcm_host_init()
        self._format = format
        self._layer = layer

        if format == "RGBA":
            self._image_type = bcm.VC_IMAGE_RGBA32
            self._pixel_width = 4
        elif format == "ARGB":
            self._image_type = bcm.VC_IMAGE_ARGB8888
            self._pixel_width = 4
        elif format == "RGBX":
            self._image_type = bcm.VC_IMAGE_TF_RGBX32
            self._pixel_width = 4
        elif format == "RGB":
            self._image_type = bcm.VC_IMAGE_RGB888
            self._pixel_width = 3
        else:
            raise DispmanXError(f"Invalid pixel format: {format}")

        if buffer_type not in ("numpy", "ctypes", "auto"):
            raise DispmanXError(f"Invalid buffer type: {buffer_type}")
        elif buffer_type == "numpy" and not HAVE_NUMPY:
            raise DispmanXError("numpy buffer type requested, but numpy not found!")
        elif buffer_type == "auto":
            buffer_type = "numpy" if HAVE_NUMPY else "ctypes"

        device_id = display.device_id if isinstance(display, Display) else display

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

        handle = bcm.vc_dispmanx_display_open(self._display.device_id)
        if handle == 0:
            raise DispmanXRuntimeError(f"Error opening device ID #{self._display.device_id}")
        logger.debug(f"Got display handle: {handle}")
        self._display_handle = handle

        buffer_size = self._display.size.width * self._display.size.height * self._pixel_width
        if buffer_type == "numpy":
            array_shape = (self._display.size.height, self._display.size.width, self._pixel_width)
            self._buffer = numpy.zeros(shape=array_shape, dtype=numpy.uint8)
        else:
            self._buffer = ct.create_string_buffer(buffer_size)
        logger.debug(f"Allocated buffer of size {buffer_size} bytes")

        self._create_video_resource_handle()
        self._create_surface_element()

    @property
    def display(self) -> Display:
        return self._display

    @property
    def size(self) -> Size:
        return self._display.size

    @property
    def width(self) -> int:
        return self._display.size.width

    @property
    def height(self) -> int:
        return self._display.size.height

    @property
    def buffer(self):
        return self._buffer

    @property
    def format(self) -> Literal["RGBA", "RGB", "ARGB", "RGBX"]:
        return self._format

    def _create_video_resource_handle(self) -> None:
        unused = ct.c_uint32()
        handle = bcm.vc_dispmanx_resource_create(
            self._image_type,
            self._display.size.width,
            self._display.size.height,
            ct.byref(unused),
        )
        if handle == 0:
            raise DispmanXRuntimeError("Error creating image resource")

        self._video_resource_handle = handle
        logger.debug(f"Created video resource handle: {handle}")

    def _create_surface_element(self) -> None:
        src_rect = bcm.VC_RECT_T(width=self.display.size.width << 16, height=self.display.size.height << 16, x=0, y=0)
        self._dest_rect = bcm.VC_RECT_T(width=self.display.size.width, height=self.display.size.height, x=0, y=0)
        alpha = bcm.VC_DISPMANX_ALPHA_T(flags=bcm.DISPMANX_FLAGS_ALPHA_FROM_SOURCE, opacity=255, mask=0)

        with self._start_and_submit_update() as update_handle:
            self._surface_element_handle = bcm.vc_dispmanx_element_add(
                update_handle,
                self._display_handle,
                self._layer,
                ct.byref(self._dest_rect),
                self._video_resource_handle,
                ct.byref(src_rect),
                bcm.DISPMANX_PROTECTION_NONE,
                ct.byref(alpha),
                None,
                bcm.DISPMANX_NO_ROTATE,
            )
            if self._surface_element_handle == 0:
                raise DispmanXRuntimeError("Couldn't create surface element")
            logger.debug(f"Got surface element handle: {self._surface_element_handle}")

    def update(self) -> None:
        """Update the pixels based on what's in the buffer

        Raises:
            DispmanXRuntimeError: Raises if there's an error writing to the video
                memory"""
        if HAVE_NUMPY:
            buffer = numpy.ctypeslib.as_ctypes(self._buffer)
        else:
            buffer = ct.byref(self._buffer)

        if (
            bcm.vc_dispmanx_resource_write_data(
                self._video_resource_handle,
                self._image_type,
                self.display.size.width * self._pixel_width,
                buffer,
                ct.byref(self._dest_rect),
            )
            != 0
        ):
            raise DispmanXRuntimeError("Error writing buffer to video memory")

        with self._start_and_submit_update():
            pass

    @contextmanager
    def _start_and_submit_update(self) -> Generator[int, None, None]:
        update_handle = bcm.vc_dispmanx_update_start(0)

        if update_handle == bcm.DISPMANX_NO_HANDLE:
            raise DispmanXRuntimeError("Couldn't get update handle")

        yield update_handle

        if bcm.vc_dispmanx_update_submit_sync(update_handle) != 0:
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
        devices = bcm.TV_ATTACHED_DEVICES_T()

        if bcm.vc_tv_get_attached_devices(ct.byref(devices)) != 0:
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
        width, height = ct.c_uint32(), ct.c_uint32()
        if bcm.graphics_get_display_size(display_id, ct.byref(width), ct.byref(height)) < 0:
            raise DispmanXRuntimeError(f"Error getting display #{display_id} size")

        return Size(width.value, height.value)
