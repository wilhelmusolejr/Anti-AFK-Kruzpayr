# Shared state variable
# Shared state variable
# Shared state variable
current_state = None
previous_state = None

user_type = "shooter" # shooter, bot, earner
did_walk = False
sleeping_time = 5

from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from play import parse_macro, run_macro
from image_analysis import state, isPlayerValidWalk

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
  did_walk = True

# ----------------------
def handle_ingame():
  global did_walk
  
  if user_type == "shooter":
      if not did_walk:
          print("🚶 Walking to location...")
          ready_to_walk()
        
      print("🔫 Starting firing loop...")
      ready_to_fire()
    
  elif user_type == "bot":
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
    global current_state, did_walk, previous_state, sleeping_time

    # When we last entered ingame
    ingame_start_time = None

    while True:
        new_state = detect_state()
        print(f"[STATE CHECK] Current state: {new_state}")
        previous_state = current_state
        current_state = new_state

        # Reset if we enter lobby
        if new_state == "inlobby":
            did_walk = False
            ingame_start_time = None
            sleeping_time = 5

        elif new_state == "ingameresult":
            ingame_start_time = None
            sleeping_time = 5

        elif new_state == "ingame":
            if previous_state in ["inlobby", "inwaitinggame"]:
                ingame_start_time = time.time()
                
                time.sleep(120)
                
                if isPlayerValidWalk():
                  sleeping_time = 690 - 120
                else:
                  if user_type == "bot":
                    press_key_for_seconds(Key.esc, 1)
                    time.sleep(1)
                    press_key_for_seconds(Key.enter, 1)
                    time.sleep(1)
                    press_key_for_seconds(Key.enter, 1)
                    sleeping_time = 5

            elif ingame_start_time:
                elapsed = time.time() - ingame_start_time
                if elapsed >= 690:
                    sleeping_time = 5  # Recheck quickly at the end
                else:
                    # Wait remaining time before entering fast-check mode
                    sleeping_time = max(690 - elapsed, 5)

        else:
            ingame_start_time = None
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
    handle_lobby()

  elif current_state == "ingame":
    handle_ingame()
        
  time.sleep(1)