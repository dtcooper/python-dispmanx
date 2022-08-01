from contextlib import contextmanager
import ctypes as ct
import logging
from typing import ClassVar, Generator, Literal, NamedTuple


try:
    import numpy
    import numpy.typing
except ImportError:
    HAVE_NUMPY = False
else:
    HAVE_NUMPY = True

from . import bcm_host as bcm


logger = logging.getLogger("dispmanx")


class DispmanxError(Exception):
    pass


class Size(NamedTuple):
    width: int
    height: int


class Display(NamedTuple):
    device_id: int
    name: str
    size: Size


class Dispmanx:
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
        device_id: int = None,
        format: Literal["RGBA", "RGB"] = "RGBA",
    ):
        self._bcm_host_init()
        self._format = format
        self._layer = layer

        if format == "RGBA":
            self._image_type = bcm.VC_IMAGE_RGBA32
            self._pixel_width = 4
        elif format == "RGB":
            self._image_type = bcm.VC_IMAGE_RGB888
            self._pixel_width = 3
        else:
            raise DispmanxError(f"Invalid pixel format: {format}")

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
                raise DispmanxError(f"No display with device ID #{device_id} found!")

        logger.debug(
            f"Using device ID #{self._display.device_id} with resolution"
            f" {self._display.size.width}x{self._display.size.height}"
        )

        handle = bcm.vc_dispmanx_display_open(self._display.device_id)
        if handle == 0:
            raise DispmanxError(f"Error opening device ID #{self._display_id}")
        logger.debug(f"Got display handle: {handle}")
        self._display_handle = handle

        buffer_size = self._display.size.width * self._display.size.height * self._pixel_width
        if HAVE_NUMPY:
            array_shape = (self._display.size.width, self._display.size.height, self._pixel_width)
            self._buffer: numpy.typing.ArrayLike = numpy.zeros(shape=array_shape, dtype=numpy.uint8)
        else:
            self._buffer: ct.c_char = ct.create_string_buffer(buffer_size)
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
    def buffer(self):
        return self._buffer

    @property
    def format(self):
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
            raise DispmanxError("Error creating image resource")

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
                raise DispmanxError("Couldn't create surface element")
            logger.debug(f"Got surface element handle: {self._surface_element_handle}")

    def update(self) -> None:
        if HAVE_NUMPY:
            buffer = numpy.ctypeslib.as_ctypes(self._buffer)
        else:
            buffer = ct.byref(self._buffer)

        response = bcm.vc_dispmanx_resource_write_data(
            self._video_resource_handle,
            self._image_type,
            self.display.size.width * self._pixel_width,
            buffer,
            ct.byref(self._dest_rect),
        )
        if response != 0:
            raise DispmanxError("Error writing buffer to video memory")

        with self._start_and_submit_update():
            pass

    @contextmanager
    def _start_and_submit_update(self) -> Generator[int, None, None]:
        update_handle = bcm.vc_dispmanx_update_start(0)

        if update_handle == bcm.DISPMANX_NO_HANDLE:
            raise DispmanxError("Couldn't get update handle")

        yield update_handle

        response = bcm.vc_dispmanx_update_submit_sync(update_handle)
        if response != 0:
            raise DispmanxError("Error submitting update")

    @classmethod
    def list_displays(cls) -> list[Display]:
        cls._bcm_host_init()
        devices = bcm.TV_ATTACHED_DEVICES_T()

        if bcm.vc_tv_get_attached_devices(ct.byref(devices)) != 0:
            raise DispmanxError("Error getting attached devices")

        response = []

        for i in range(devices.num_attached):
            display_id = devices.display_number[i]
            size = cls._get_display_size(display_id)
            response.append(Display(display_id, devices.get_display_text(display_id), size))

        return response

    @classmethod
    def get_default_display(cls) -> Display:
        displays = cls.list_displays()
        if len(displays) == 0:
            raise DispmanxError("No displays found!")
        return displays[0]

    @classmethod
    def _get_display_size(cls, display_id) -> tuple[int, int]:
        cls._bcm_host_init()
        width, height = ct.c_uint32(), ct.c_uint32()
        if bcm.graphics_get_display_size(display_id, ct.byref(width), ct.byref(height)) < 0:
            raise DispmanxError(f"Error getting display #{display_id} size")

        return Size(width.value, height.value)
