import ctypes
import time
import random
import math

# ---- Low-Level Mouse Movement Using SendInput ----

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _INPUT)]

def move_mouse_relative(x, y):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx=x, dy=y, mouseData=0,
                    dwFlags=MOUSEEVENTF_MOVE,
                    time=0, dwExtraInfo=ctypes.pointer(extra))
    input_struct = INPUT(type=INPUT_MOUSE, mi=mi)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), ctypes.sizeof(input_struct))

# ---- Realistic Mouse Movement ----

def human_like_mouse_move(total_distance=1600, duration=2.0):
    steps = 320
    base_step = total_distance / steps
    start_time = time.time()
    time.sleep(1)  # buffer before starting

    for i in range(steps):
        # Create a simple ease-in, ease-out motion using a sine curve
        progress = i / steps
        eased = math.sin(progress * math.pi)  # Smooth speed curve

        # Calculate step size with easing and some randomness
        dx = int(base_step * eased + random.uniform(-0.5, 0.5))
        dy = int(random.uniform(-1, 1))  # simulate slight up/down jitter

        move_mouse_relative(dx, dy)

        # Variable delay per step (simulate finger tremors/slightly uneven pace)
        time.sleep(0.005 + random.uniform(0.002, 0.006))

    print("Mouse movement complete in ~{:.2f}s".format(time.time() - start_time))

# ---- Run it ----

human_like_mouse_move()
