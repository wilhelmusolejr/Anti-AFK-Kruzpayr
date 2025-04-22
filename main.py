from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from play import parse_macro, run_macro

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
user_type = "shooter" # shooter, bot

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
def press_key_for_seconds(key, duration):
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)    
  

# Getting state from the game
def detect_state():
    # return random.choice(['inlobby', 'ingame'])
    return 'ingame'

# Function to check the state
def state_checker():
    global current_state
    while True:
        new_state = detect_state()
        print(f"[STATE CHECK] Current state: {new_state}")
        current_state = new_state
        time.sleep(10)

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
          time.sleep(0.5)
          
    if(current_state == "inlobby"):
      print("user pressed ready button")
      time.sleep(9)
    
    time.sleep(1)