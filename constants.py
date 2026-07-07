import ctypes
from ctypes import wintypes
from typing import Callable, List, Tuple, Union, NamedTuple


DIV60FPS = .01666666666666666666666666666667

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG), ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]
    
    
class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [("BlendOp", ctypes.c_byte), ("BlendFlags", ctypes.c_byte),
                ("SourceConstantAlpha", ctypes.c_byte), ("AlphaFormat", ctypes.c_byte)]
    
MenuItem = Union[Tuple[str, Callable], Tuple[str, List['MenuItem']]]


class Rect(NamedTuple):
    left: float
    top: float
    width: float
    height: float

    def __repr__(self):
        return f"Rect({self.left}, {self.top}, {self.width}, {self.height})"

    def __getitem__(self, index):
        return (self.left, self.top, self.width, self.height)[index]