import ctypes
import time
import os

from ctypes import wintypes
from app import get_object_location, get_screenshot

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

# Structures
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

def move_mouse_by_delta(dx, dy, steps=20, delay_ms=5):
    step_dx = dx / steps
    step_dy = dy / steps
    for _ in range(steps):
        send_mouse_move(int(step_dx), int(step_dy))
        time.sleep(delay_ms / 1000.0)
# Example usage
object_result = get_object_location()

if object_result:
    cx, cy = object_result["center"]

    # 🧠 Get screen size
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    # 🎯 Calculate delta from center
    dx = cx - screen_center_x
    dy = cy - screen_center_y

    # 💡 Move mouse by delta
    move_mouse_by_delta(dx, dy)

    # Save raw screenshot
    # Take screenshot and convert to OpenCV format
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    pil_image = get_screenshot()

    # Save raw screenshot
    os.makedirs("screenshots", exist_ok=True)
    raw_path = f"screenshots/screenshot_{timestamp}output.png"
    pil_image.save(raw_path)
    
