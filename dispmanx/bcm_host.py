import ctypes as ct
from ctypes.util import find_library
import enum
import sys


_lib_path = find_library("bcm_host")
if _lib_path is None:
    print("Unable to locate bcm_host library. Are you sure the libraspberrypi-bin package is installed?")
    sys.exit(1)


class Enum(enum.IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)


_lib = ct.CDLL(_lib_path)

# Constants
TV_MAX_ATTACHED_DISPLAYS = 16
DISPMANX_NO_HANDLE = 0
DISPMANX_NO_ROTATE = 0
DISPMANX_PROTECTION_NONE = 0
VC_IMAGE_RGB888 = 5
VC_IMAGE_RGBA32 = 15
DISPMANX_FLAGS_ALPHA_FROM_SOURCE = 0
DISPMANX_FLAGS_ALPHA_FIXED_ALL_PIXELS = 1

# Simple Types
DISPMANX_DISPLAY_HANDLE_T = ct.c_uint32
DISPMANX_ELEMENT_HANDLE_T = ct.c_uint32
DISPMANX_PROTECTION_T = ct.c_uint32
DISPMANX_RESOURCE_HANDLE_T = ct.c_uint32
DISPMANX_UPDATE_HANDLE_T = ct.c_uint32


# Enums
class VC_IMAGE_TYPE_T(Enum):
    VC_IMAGE_MIN = 0
    VC_IMAGE_RGB565 = 1
    VC_IMAGE_1BPP = 2
    VC_IMAGE_YUV420 = 3
    VC_IMAGE_48BPP = 4
    VC_IMAGE_RGB888 = 5
    VC_IMAGE_8BPP = 6
    VC_IMAGE_4BPP = 7
    VC_IMAGE_3D32 = 8
    VC_IMAGE_3D32B = 9
    VC_IMAGE_3D32MAT = 10
    VC_IMAGE_RGB2X9 = 11
    VC_IMAGE_RGB666 = 12
    VC_IMAGE_PAL4_OBSOLETE = 13
    VC_IMAGE_PAL8_OBSOLETE = 14
    VC_IMAGE_RGBA32 = 15
    VC_IMAGE_YUV422 = 16
    VC_IMAGE_RGBA565 = 17
    VC_IMAGE_RGBA16 = 18
    VC_IMAGE_YUV_UV = 19
    VC_IMAGE_TF_RGBA32 = 20
    VC_IMAGE_TF_RGBX32 = 21
    VC_IMAGE_TF_FLOAT = 22
    VC_IMAGE_TF_RGBA16 = 23
    VC_IMAGE_TF_RGBA5551 = 24
    VC_IMAGE_TF_RGB565 = 25
    VC_IMAGE_TF_YA88 = 26
    VC_IMAGE_TF_BYTE = 27
    VC_IMAGE_TF_PAL8 = 28
    VC_IMAGE_TF_PAL4 = 29
    VC_IMAGE_TF_ETC1 = 30
    VC_IMAGE_BGR888 = 31
    VC_IMAGE_BGR888_NP = 32
    VC_IMAGE_BAYER = 33
    VC_IMAGE_CODEC = 34
    VC_IMAGE_YUV_UV32 = 35
    VC_IMAGE_TF_Y8 = 36
    VC_IMAGE_TF_A8 = 37
    VC_IMAGE_TF_SHORT = 38
    VC_IMAGE_TF_1BPP = 39
    VC_IMAGE_OPENGL = 40
    VC_IMAGE_YUV444I = 41
    VC_IMAGE_YUV422PLANAR = 42
    VC_IMAGE_ARGB8888 = 43
    VC_IMAGE_XRGB8888 = 44
    VC_IMAGE_YUV422YUYV = 45
    VC_IMAGE_YUV422YVYU = 46
    VC_IMAGE_YUV422UYVY = 47
    VC_IMAGE_YUV422VYUY = 48
    VC_IMAGE_RGBX32 = 49
    VC_IMAGE_RGBX8888 = 50
    VC_IMAGE_BGRX8888 = 51
    VC_IMAGE_YUV420SP = 52
    VC_IMAGE_YUV444PLANAR = 53
    VC_IMAGE_TF_U8 = 54
    VC_IMAGE_TF_V8 = 55
    VC_IMAGE_YUV420_16 = 56
    VC_IMAGE_YUV_UV_16 = 57
    VC_IMAGE_YUV420_S = 58
    VC_IMAGE_YUV10COL = 59
    VC_IMAGE_RGBA1010102 = 60
    VC_IMAGE_MAX = 61
    VC_IMAGE_FORCE_ENUM_16BIT = 0xFFFF


class DISPMANX_FLAGS_ALPHA_T(Enum):
    DISPMANX_FLAGS_ALPHA_FROM_SOURCE = 0
    DISPMANX_FLAGS_ALPHA_FIXED_ALL_PIXELS = 1
    DISPMANX_FLAGS_ALPHA_FIXED_NON_ZERO = 2
    DISPMANX_FLAGS_ALPHA_FIXED_EXCEED_0X07 = 3
    DISPMANX_FLAGS_ALPHA_PREMULT = 1 << 16
    DISPMANX_FLAGS_ALPHA_MIX = 1 << 17
    DISPMANX_FLAGS_ALPHA_DISCARD_LOWER_LAYERS = 1 << 18


class DISPMANX_FLAGS_CLAMP_T(Enum):
    DISPMANX_FLAGS_CLAMP_NONE = 0
    DISPMANX_FLAGS_CLAMP_LUMA_TRANSPARENT = 1
    DISPMANX_FLAGS_CLAMP_TRANSPARENT = 2
    DISPMANX_FLAGS_CLAMP_REPLACE = 3


class DISPMANX_FLAGS_KEYMASK_T(Enum):
    DISPMANX_FLAGS_KEYMASK_OVERRIDE = 1
    DISPMANX_FLAGS_KEYMASK_SMOOTH = 1 << 1
    DISPMANX_FLAGS_KEYMASK_CR_INV = 1 << 2
    DISPMANX_FLAGS_KEYMASK_CB_INV = 1 << 3
    DISPMANX_FLAGS_KEYMASK_YY_INV = 1 << 4


class DISPMANX_TRANSFORM_T(Enum):
    DISPMANX_NO_ROTATE = 0
    DISPMANX_ROTATE_90 = 1
    DISPMANX_ROTATE_180 = 2
    DISPMANX_ROTATE_270 = 3
    DISPMANX_FLIP_HRIZ = 1 << 16
    DISPMANX_FLIP_VERT = 1 << 17
    DISPMANX_STEREOSCOPIC_INVERT = 1 << 19
    DISPMANX_STEREOSCOPIC_NONE = 0 << 20
    DISPMANX_STEREOSCOPIC_MONO = 1 << 20
    DISPMANX_STEREOSCOPIC_SBS = 2 << 20
    DISPMANX_STEREOSCOPIC_TB = 3 << 20
    DISPMANX_STEREOSCOPIC_MASK = 15 << 20
    DISPMANX_SNAPSHOT_NO_YUV = 1 << 24
    DISPMANX_SNAPSHOT_NO_RGB = 1 << 25
    DISPMANX_SNAPSHOT_FILL = 1 << 26
    DISPMANX_SNAPSHOT_SWAP_RED_BLUE = 1 << 27
    DISPMANX_SNAPSHOT_PACK = 1 << 28


# Structures
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


class VC_RECT_T(ct.Structure):
    _fields_ = [
        ("x", ct.c_int32),
        ("y", ct.c_int32),
        ("width", ct.c_int32),
        ("height", ct.c_int32),
    ]


class VC_DISPMANX_ALPHA_T(ct.Structure):
    _fields_ = [
        ("flags", ct.c_uint32),  # DISPMANX_FLAGS_ALPHA_T
        ("opacity", ct.c_uint32),
        ("mask", DISPMANX_RESOURCE_HANDLE_T),
    ]


# Functions
bcm_host_init = _lib.bcm_host_init
bcm_host_init.argtypes = ()
bcm_host_init.restype = None

graphics_get_display_size = _lib.graphics_get_display_size
graphics_get_display_size.argtypes = (ct.c_uint16, ct.POINTER(ct.c_uint32), ct.POINTER(ct.c_uint32))
graphics_get_display_size.restype = ct.c_int32

vc_tv_get_attached_devices = _lib.vc_tv_get_attached_devices
vc_tv_get_attached_devices.argtypes = (ct.POINTER(TV_ATTACHED_DEVICES_T),)
vc_tv_get_attached_devices.restype = ct.c_int

vc_dispmanx_resource_create = _lib.vc_dispmanx_resource_create
vc_dispmanx_resource_create.argtypes = (VC_IMAGE_TYPE_T, ct.c_uint32, ct.c_uint32, ct.POINTER(ct.c_uint32))
vc_dispmanx_resource_create.restype = DISPMANX_RESOURCE_HANDLE_T

vc_dispmanx_rect_set = _lib.vc_dispmanx_rect_set
vc_dispmanx_rect_set.argtypes = (ct.POINTER(VC_RECT_T), ct.c_uint32, ct.c_uint32, ct.c_uint32, ct.c_uint32)
vc_dispmanx_rect_set.restype = ct.c_int

vc_dispmanx_update_start = _lib.vc_dispmanx_update_start
vc_dispmanx_update_start.argtypes = (ct.c_int32,)
vc_dispmanx_update_start.restype = DISPMANX_UPDATE_HANDLE_T

vc_dispmanx_element_add = _lib.vc_dispmanx_element_add
vc_dispmanx_element_add.argtypes = (
    DISPMANX_UPDATE_HANDLE_T,
    DISPMANX_DISPLAY_HANDLE_T,
    ct.c_int32,
    ct.POINTER(VC_RECT_T),
    DISPMANX_RESOURCE_HANDLE_T,
    ct.POINTER(VC_RECT_T),
    DISPMANX_PROTECTION_T,
    ct.POINTER(VC_DISPMANX_ALPHA_T),
    ct.c_void_p,
    DISPMANX_TRANSFORM_T,
)
vc_dispmanx_element_add.restype = DISPMANX_ELEMENT_HANDLE_T

vc_dispmanx_update_submit_sync = _lib.vc_dispmanx_update_submit_sync
vc_dispmanx_update_submit_sync.argtypes = (DISPMANX_UPDATE_HANDLE_T,)
vc_dispmanx_update_submit_sync.restype = ct.c_int

vc_dispmanx_rect_set = _lib.vc_dispmanx_rect_set
vc_dispmanx_rect_set.argtypes = [ct.POINTER(VC_RECT_T), ct.c_uint32, ct.c_uint32, ct.c_uint32, ct.c_uint32]
vc_dispmanx_rect_set.restype = ct.c_int

vc_dispmanx_resource_write_data = _lib.vc_dispmanx_resource_write_data
vc_dispmanx_resource_write_data.argtypes = [
    DISPMANX_RESOURCE_HANDLE_T,
    VC_IMAGE_TYPE_T,
    ct.c_int,
    ct.c_void_p,
    ct.POINTER(VC_RECT_T),
]
vc_dispmanx_resource_write_data.restype = ct.c_int

vc_dispmanx_element_modified = _lib.vc_dispmanx_element_modified
vc_dispmanx_element_modified.argtypes = [DISPMANX_UPDATE_HANDLE_T, DISPMANX_ELEMENT_HANDLE_T, ct.POINTER(VC_RECT_T)]
vc_dispmanx_element_modified.restype = ct.c_int


# New
vc_dispmanx_display_open = _lib.vc_dispmanx_display_open
vc_dispmanx_display_open.argtypes = (ct.c_uint32,)
vc_dispmanx_display_open.restype = ct.c_uint32
