import time
from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button

from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from play import parse_macro, run_macro
from image_analysis import state, isPlayerValidWalk
from telebram import sendMessage, sendScreenshot
from datetime import datetime

import threading
import pyautogui
import threading
import time
import random

# Controller
keyboard = Controller()
mouse = MouseController()

def press_key_for_seconds(key, duration):
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)    

def click_ready_button():
  screen_width, screen_height = pyautogui.size()

  # Relative coordinates (based on your screen ratio)
  rel_x = 0.91666
  rel_y = 0.7245

  # Add small natural jitter
  jitter_x = random.randint(-4, 4)
  jitter_y = random.randint(-4, 4)

  # Final target position
  x = int(screen_width * rel_x) + jitter_x
  y = int(screen_height * rel_y) + jitter_y

  # Smooth movement duration and delay before click
  pyautogui.moveTo(x, y, duration=random.uniform(0.25, 0.45))
  time.sleep(random.uniform(0.1, 0.25))

  # Click with slight hesitation
  mouse.click(Button.left, 1)


time.sleep(3)
while True:
  click_ready_button()
  time.sleep(1)
  press_key_for_seconds("w", 2)
  time.sleep(1)
  press_key_for_seconds("a", 2)
  