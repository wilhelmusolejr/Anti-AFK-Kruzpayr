# Shared state variable
# Shared state variable
# Shared state variable
current_state = None
previous_state = None
notified_user = False
did_walk = False
take_screenshot_on_total = False
sleeping_time = 5

client_id = "154.26.137.12"
user_type = "bot" # shooter, bot, earner

# Shared state variable
# Shared state variable
# Shared state variable

from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from datetime import datetime

import threading
import pyautogui
import threading
import time
import random

pyautogui.FAILSAFE = False

import ctypes
import time
import random
import os

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

# Controller
keyboard = Controller()
mouse = MouseController()

def saveScreenshot():
  folder = "screenshots"
  os.makedirs(folder, exist_ok=True)  # create folder if not exists

  # Timestamp filename
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = os.path.join(folder, f"screenshot_{timestamp}.png")

  # Take screenshot and save
  screenshot = pyautogui.screenshot()
  screenshot.save(filename)

  print(f"✅ Screenshot saved: {filename}")
    

# Define the necessary structures for SendInput
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)))

class INPUT(ctypes.Structure):
    _fields_ = (("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT))

def send_mouse_move(dx, dy):
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, mi)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def move_mouse_smooth(total_steps, dx_per_step, delay_ms):
    for _ in range(total_steps):
        dx = -dx_per_step  # ❗ Make it negative to move left
        dy = 0  # Only horizontal movement
        send_mouse_move(dx, dy)
        time.sleep(delay_ms / 1000.0)

# FUNCTIIONS
# FUNCTIIONS
# FUNCTIIONS
def press_key_for_seconds(key, duration):
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)    

# ----------------------
def ready_to_walk():
  time.sleep(3)
  press_key_for_seconds('3', 0.5)
  press_key_for_seconds('d', 4)
  press_key_for_seconds('w', 2)
  press_key_for_seconds('a', 0.5)
  press_key_for_seconds('w', 0.5)
  press_key_for_seconds('d', 0.5)
  press_key_for_seconds('w', 3)
  press_key_for_seconds('a', 0.6)
  press_key_for_seconds('w', 6)
  press_key_for_seconds('d', 3)
  press_key_for_seconds('w', 5)
  press_key_for_seconds('a', 1)
  time.sleep(0.5)
  press_key_for_seconds('w', 0.6)
  time.sleep(0.5)
  press_key_for_seconds('d', 0.85)
  time.sleep(0.5)
  press_key_for_seconds('w', 0.3)
  
  time.sleep(1)

ready_to_walk()
time.sleep(1)
total_steps = 265  
dx_per_step = 50   
delay_ms = 0 
move_mouse_smooth(total_steps, dx_per_step, delay_ms)