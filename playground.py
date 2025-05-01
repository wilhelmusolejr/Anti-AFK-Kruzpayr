# FRAMEWORKS
# FRAMEWORKS
# FRAMEWORKS
from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button

import threading
import pyautogui
import time
import random
import os

# Controller
# Controller
# Controller
keyboard = Controller()
mouse = MouseController()
state_lock = threading.Lock()  

while True:
  mouse.click(Button.left, 1)
  time.sleep(1)
  