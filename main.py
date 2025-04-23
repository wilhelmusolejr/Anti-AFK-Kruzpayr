from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from play import parse_macro, run_macro
from image_analysis import isInLobby

import tkinter as tk
import threading
import pyautogui
import threading
import time
import random

# Controller
keyboard = Controller()
mouse = MouseController()

# Shared state variable
current_state = "inlobby"
previous_state = "inlobby"
user_type = "bot" # shooter, bot
did_walk = False
sleeping_time = 30

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
def press_key_for_seconds(key, duration):
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)    

def click_ready_button():
    screen_width, screen_height = pyautogui.size()
    
    # Use average ratio from your sample
    rel_x = 0.91666
    rel_y = 0.7245
    
    x = int(screen_width * rel_x)
    y = int(screen_height * rel_y)
    
    pyautogui.moveTo(x, y)
    time.sleep(0.3)
    mouse.click(Button.left, 1)

def click_okay_button():
  x = 463
  y = 363

  pyautogui.moveTo(x, y)
  time.sleep(0.3)
  mouse.click(Button.left, 1)

def click_to_right():
  x = 675
  y = 316

  pyautogui.moveTo(x, y)
  time.sleep(0.3)
  mouse.click(Button.left, 1)
      
# Getting state from the game
def detect_state():
  time.sleep(2)  # Wait for the state thread to start
  screenshot = pyautogui.screenshot()
  isInlobbyBa = isInLobby(screenshot, "lobby.bmp")
  status = None
  
  if isInlobbyBa:
      status = 'inlobby'
  else:
      status = 'ingame'
  
  return status

# Function to check the state
def state_checker():
    global current_state, did_walk

    while True:
        new_state = detect_state()
        print(f"[STATE CHECK] Current state: {new_state}")
        current_state = new_state

        if new_state == "inlobby":
          did_walk = False

        time.sleep(sleeping_time)

# Start the state-checking thread
state_thread = threading.Thread(target=state_checker, daemon=True)
state_thread.start()

# Main thread (for testing)
time.sleep(5)  # Wait for the state thread to start
while True:
    print(f"[MAIN LOOP] Preparing")
    
    print("Previous state: ", previous_state)
    print("Current state: ", current_state)

    if(current_state != previous_state):
      previous_state = current_state
      
      if(current_state == "ingame"):
        if(user_type == "shooter"):
          print('user walk to location')
          macro_events = parse_macro("Macro 1.xml")
          run_macro(macro_events)
          
          while current_state == "ingame":
              print('user pressed fire button')
              mouse.click(Button.left, 1)
              time.sleep(0.3)
        
        if(user_type == "bot"):
          press_key_for_seconds('a', 2)
          press_key_for_seconds(Key.enter, 1)
          time.sleep(0.5)
          
    if(current_state == "inlobby"):
      while current_state == "inlobby":
        print("user pressed ready button")
        if(user_type == "shooter"):
          click_okay_button()
          click_to_right()
          click_ready_button()
        else:
          click_ready_button()
        
        time.sleep(9)
    
    if(current_state == "ingame"):
      if(user_type == "shooter"):
        
        if not did_walk:
          print('user walk to location')
          macro_events = parse_macro("Macro 1.xml")
          run_macro(macro_events)
          did_walk = True

        while current_state == "ingame":
          print('user pressed fire button')
          mouse.click(Button.left, 1)
          time.sleep(0.3)

      if(user_type == "bot"):
        while current_state == "ingame":
          press_key_for_seconds('a', 2)
          time.sleep(0.5)

    time.sleep(1)