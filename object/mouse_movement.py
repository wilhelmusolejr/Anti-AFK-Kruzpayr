import ctypes
import time
from ctypes import wintypes  # ✅ Import this!

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

# Define required structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]

def send_mouse_move(dx, dy):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, mi)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def get_mouse_position():
    pt = wintypes.POINT()  # ✅ Fix here
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def move_mouse_to(target_x, target_y, steps=20, delay_ms=5):
    current_x, current_y = get_mouse_position()
    dx = (target_x - current_x) / steps
    dy = (target_y - current_y) / steps
    for _ in range(steps):
        send_mouse_move(int(dx), int(dy))
        time.sleep(delay_ms / 1000.0)

# Example usage
target_x, target_y = 932, 521
move_mouse_to(target_x, target_y)
