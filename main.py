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
user_type = "shooter" # shooter, bot, earner

# Shared state variable
# Shared state variable
# Shared state variable

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

pyautogui.FAILSAFE = False

# Controller
keyboard = Controller()
mouse = MouseController()

# FUNCTIIONS
# FUNCTIIONS
# FUNCTIIONS
def press_key_for_seconds(key, duration):
  keyboard.press(key)
  time.sleep(duration)
  keyboard.release(key)    

# ----------------------
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

# ----------------------
def click_okay_button():
  # Add slight randomness for natural feel
  x = 420 + random.randint(-4, 4)
  y = 363 + random.randint(-4, 4)

  # Move mouse smoothly to target
  pyautogui.moveTo(x, y, duration=random.uniform(0.25, 0.45))

  # Pause like a human before clicking
  time.sleep(random.uniform(0.1, 0.25))

  # Click the button
  mouse.click(Button.left, 1)

# ----------------------
def click_to_right():
  x = 620
  y = 316

  pyautogui.moveTo(x, y)
  time.sleep(0.3)
  mouse.click(Button.left, 1)

# ----------------------
def ready_to_fire():
  willJump = random.randint(0, 100)
  willChat = random.randint(0, 100) 
  willSit = random.randint(0, 100)
  willWalk = random.randint(0, 200)
  willSwitch = random.randint(0, 100)
  fireSet = random.randint(0, 50)

  if(willJump < 5):
    press_key_for_seconds(Key.space, 0.3)
    time.sleep(random.uniform(0.3, 0.8))  

  if(willChat < 5):
    all_keys = [Key.f5, Key.f6, Key.f7, Key.f8]
    random_key = random.choice(all_keys)
    press_key_for_seconds(Key.f2, 0.3)
    time.sleep(random.uniform(0.2, 0.5))  
    press_key_for_seconds(random_key, 0.3)
    time.sleep(random.uniform(0.2, 0.5))  

  if(willSit < 5):
    press_key_for_seconds(Key.ctrl, 0.3)
    time.sleep(random.uniform(0.3, 0.8))  

  if(willWalk < 2):
    press_key_for_seconds('a', 0.3)
    time.sleep(random.uniform(0.3, 0.8))  
    press_key_for_seconds('d', 0.5)
    time.sleep(random.uniform(0.3, 0.5))  

  if(willSwitch < 2):
    press_key_for_seconds('1', 0.3)
    time.sleep(random.uniform(0.8, 1))
    mouse.click(Button.left, 1)
    press_key_for_seconds('3', 0.3)
    mouse.click(Button.left, 1)
    time.sleep(random.uniform(0.2, 0.5))

  if(fireSet == 1):
    mouse.click(Button.left, 1)
  else:  
    mouse.click(Button.right, 1)
    time.sleep(0.3)
    mouse.click(Button.right, 1)
    time.sleep(0.3)
    mouse.click(Button.right, 1)
    time.sleep(0.3)

# ----------------------
def ready_to_walk():
  global did_walk
  
  macro_events = parse_macro("Macro 1.xml")
  run_macro(macro_events)
  press_key_for_seconds('w', 0.1)
  did_walk = True

# ----------------------
def open_board():
  x = 777
  y = 14

  pyautogui.moveTo(x, y)
  time.sleep(0.3)
  mouse.click(Button.left, 1)

# ----------------------
def close_board():
  x = 766
  y = 29

  pyautogui.moveTo(x, y)
  time.sleep(0.3)
  mouse.click(Button.left, 1)

# ----------------------
def handle_ingame():
  global did_walk
  
  if user_type == "shooter":
      if not did_walk:
          print("🚶 Walking to location...")
          ready_to_walk()
        
      print("🔫 Starting firing loop...")
      ready_to_fire()
    
  elif user_type in ["bot", "earner"]:
      press_key_for_seconds('a', 2)
      time.sleep(1) 

# ----------------------
def handle_lobby():
  print("Preparing in lobby...")

  click_okay_button()
  time.sleep(1)
  
  if user_type in ["shooter", "earner"]:
    click_to_right()
    time.sleep(1)
    
  click_ready_button()
  time.sleep(9)

# ----------------------
# Getting state from the game
def detect_state():
  detected_state = state()
  return detected_state

# ----------------------
def state_checker():
    global current_state, did_walk, previous_state, sleeping_time, notified_user

    while True:
        new_state = detect_state()
        print(f"[STATE CHECK] Current state: {new_state}")
        previous_state = current_state
        current_state = new_state

        # Reset if we enter lobby
        if new_state == "inlobby":
            did_walk = False
            notified_user = False
            sleeping_time = 5

        elif new_state == "ingameresult":
            sleeping_time = 5

        elif new_state == "ingame":
            if previous_state in ["inlobby", "inwaitinggame"]:
                
                time.sleep(120)
                
                if isPlayerValidWalk():
                  sleeping_time = 30
                else:
                  valid_walk_found = False
                  attempt_num = 20
                  
                  press_key_for_seconds(Key.f2, 1)
                    
                  for i in range(attempt_num):
                    if isPlayerValidWalk():
                      press_key_for_seconds(Key.f5, 1)
                      valid_walk_found = True
                      time.sleep(5)
                      break
                    else:
                      press_key_for_seconds(Key.f6, 1)
                    
                  if not valid_walk_found:
                    sleeping_time = 5
                    
                    if user_type == "bot":
                      press_key_for_seconds(Key.f7, 1)
                      time.sleep(1)
                      press_key_for_seconds(Key.esc, 1)
                      time.sleep(1)
                      press_key_for_seconds(Key.enter, 1)
                      time.sleep(1)
                      press_key_for_seconds(Key.enter, 1)

        else:
            sleeping_time = 5  # fallback

        print(f"🕐 Sleeping for {sleeping_time} seconds...")
        time.sleep(sleeping_time)

# Start the state-checking thread
state_thread = threading.Thread(target=state_checker, daemon=True)
state_thread.start()

# Main thread (for testing)

time.sleep(5)
while True:
  if current_state != previous_state:
    print(f"[STATE CHANGE] {previous_state} → {current_state}")

  print(f"[MAIN LOOP] Current State: {current_state}")
    
  if current_state == "inlobby":
    now = datetime.now()
    if now.hour == 23 and now.minute >= 30 and not take_screenshot_on_total:
      print("Go to board")
      open_board()
      time.sleep(1)
      sendScreenshot()
      time.sleep(1)
      close_board()
      time.sleep(3)
      take_screenshot_on_total = True
    
    if now.hour == 0:
        take_screenshot_on_total = False

    handle_lobby()

  elif current_state == "ingame":
    handle_ingame()
    
  elif current_state == "inoutside":
    if not notified_user:
      sendMessage("In outside: " + str(client_id))
      sendScreenshot()
      time.sleep(2)
      notified_user = True
        
  time.sleep(1)