import ctypes as ct
from ctypes.util import find_library
import enum
import sys
import os

_lib_path = find_library("bcm_host")
if _lib_path is None:
    if len(sys.argv) < 1 or os.path.basename(sys.argv[0]) != 'mkdocs':
        print(
            "Unable to locate bcm_host library. Are you sure the libraspberrypi0 package is installed? Try running:\n"
            "    $ sudo apt-get install -y --no-install-recommends libraspberrypi0"
        )
        sys.exit(1)

else:
    class Enum(enum.IntEnum):
        @classmethod
        def from_param(cls, obj):
            return int(obj)


    _lib = ct.CDLL(_lib_path)

    DISPMANX_FLAGS_ALPHA_FROM_SOURCE = 0
    DISPMANX_NO_HANDLE = 0
    DISPMANX_NO_ROTATE = 0
    DISPMANX_PROTECTION_NONE = 0
    TV_MAX_ATTACHED_DISPLAYS = 16
    VC_IMAGE_RGB888 = 5
    VC_IMAGE_RGBA32 = 15
    VC_IMAGE_TF_RGBX32 = 21
    VC_IMAGE_ARGB8888 = 43


    class VC_RECT_T(ct.Structure):
        _fields_ = (
            ("x", ct.c_int32),
            ("y", ct.c_int32),
            ("width", ct.c_int32),
            ("height", ct.c_int32),
        )


    class VC_DISPMANX_ALPHA_T(ct.Structure):
        _fields_ = (
            ("flags", ct.c_uint32),
            ("opacity", ct.c_uint32),
            ("mask", ct.c_uint32),
        )


    class TV_ATTACHED_DEVICES_T(ct.Structure):
        TV_ATTACHED_DEVICES_DISPLAY_TO_TEXT_UNKNOWN = "Unknown"
        TV_ATTACHED_DEVICES_DISPLAY_TO_TEXT = (
            "Main LCD",
            "Auxiliary LCD",
            "HDMI 0",
            "Composite",
            "Forced LCD",
            "Forced TV",
            "Forced Other",
            "HDMI 1",
            "Forced TV2",
        )

        _fields_ = (
            ("num_attached", ct.c_int32),
            ("display_number", ct.c_uint8 * TV_MAX_ATTACHED_DISPLAYS),
        )

        @classmethod
        def get_display_text(cls, display_number):
            if display_number < len(cls.TV_ATTACHED_DEVICES_DISPLAY_TO_TEXT):
                return cls.TV_ATTACHED_DEVICES_DISPLAY_TO_TEXT[display_number]
            return cls.TV_ATTACHED_DEVICES_DISPLAY_TO_TEXT_UNKNOWN


    bcm_host_init = _lib.bcm_host_init
    bcm_host_init.argtypes = ()
    bcm_host_init.restype = None

    vc_dispmanx_display_open = _lib.vc_dispmanx_display_open
    vc_dispmanx_display_open.argtypes = (ct.c_uint32,)
    vc_dispmanx_display_open.restype = ct.c_uint32

    vc_dispmanx_resource_create = _lib.vc_dispmanx_resource_create
    vc_dispmanx_resource_create.argtypes = (ct.c_uint32, ct.c_uint32, ct.c_uint32, ct.POINTER(ct.c_uint32))
    vc_dispmanx_resource_create.restype = ct.c_uint32

    vc_dispmanx_element_add = _lib.vc_dispmanx_element_add
    vc_dispmanx_element_add.argtypes = (
        ct.c_uint32,
        ct.c_uint32,
        ct.c_int32,
        ct.POINTER(VC_RECT_T),
        ct.c_uint32,
        ct.POINTER(VC_RECT_T),
        ct.c_uint32,
        ct.POINTER(VC_DISPMANX_ALPHA_T),
        ct.c_void_p,
        ct.c_uint32,
    )
    vc_dispmanx_element_add.restype = ct.c_uint32

    vc_dispmanx_resource_write_data = _lib.vc_dispmanx_resource_write_data
    vc_dispmanx_resource_write_data.argtypes = [
        ct.c_uint32,
        ct.c_uint32,
        ct.c_int,
        ct.c_void_p,
        ct.POINTER(VC_RECT_T),
    ]
    vc_dispmanx_resource_write_data.restype = ct.c_int

    vc_dispmanx_update_submit_sync = _lib.vc_dispmanx_update_submit_sync
    vc_dispmanx_update_submit_sync.argtypes = (ct.c_uint32,)
    vc_dispmanx_update_submit_sync.restype = ct.c_int

    vc_dispmanx_update_start = _lib.vc_dispmanx_update_start
    vc_dispmanx_update_start.argtypes = (ct.c_int32,)
    vc_dispmanx_update_start.restype = ct.c_uint32

    graphics_get_display_size = _lib.graphics_get_display_size
    graphics_get_display_size.argtypes = (ct.c_uint16, ct.POINTER(ct.c_uint32), ct.POINTER(ct.c_uint32))
    graphics_get_display_size.restype = ct.c_int32

    vc_tv_get_attached_devices = _lib.vc_tv_get_attached_devices
    vc_tv_get_attached_devices.argtypes = (ct.POINTER(TV_ATTACHED_DEVICES_T),)
    vc_tv_get_attached_devices.restype = ct.c_int
