# --------------------------------
# --------------------------------

TIME_LOBBY = 20
TIME_WAITING_GAME = 10
TIME_GAME = 720 # 12 minutes

user_type = "bot" # shooter, bot, earner
did_walk = False

# --------------------------------
# --------------------------------

from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from play import parse_macro, run_macro
from image_analysis import isInLobby

import time 
import random
import pyautogui

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

    # print(f"🎯 Moving to ({x}, {y})")

    # Smooth movement duration and delay before click
    pyautogui.moveTo(x, y, duration=random.uniform(0.25, 0.45))
    time.sleep(random.uniform(0.1, 0.25))

    # Click with slight hesitation
    mouse.click(Button.left, 1)
    # print("✅ Clicked READY")

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
# ----------------------
time.sleep(5)

while True:
  interval = 5
  # INLOBBY
  # INLOBBY
  # INLOBBY
  for i in range(int(TIME_LOBBY/interval)):
    print("Waiting in lobby...")
    
    if user_type == "shooter"  or user_type == "earner":
      click_okay_button()  
      time.sleep(1)
      click_to_right()
      time.sleep(1)
      click_ready_button()
      
    else:
      click_okay_button()  
      time.sleep(1)
      click_ready_button()
      
    time.sleep(interval)
    
  # WAITING GAME
  # WAITING GAME
  # WAITING GAME
  for i in range(TIME_WAITING_GAME):
    print("Waiting for game...")
    time.sleep(1)

  # INGAME
  # INGAME
  # INGAME
  start_time = time.time()
  while time.time() - start_time < TIME_GAME:
    print("Playing...")

    if user_type == "shooter" and not did_walk:
      macro_events = parse_macro("Macro 1.xml")
      run_macro(macro_events)
      press_key_for_seconds('d', 1)
      time.sleep(0.5)
      press_key_for_seconds('w', 0.5)
      did_walk = True
      
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

    if(fireSet < 5):
      mouse.click(Button.right, 1)
      time.sleep(random.uniform(0.5, 1))
    else:
      digit_attack = random.randint(4, 10)  
      for _ in range(random.randint(2, digit_attack)):
        mouse.click(Button.left, 1)
        time.sleep(random.uniform(0.3, 0.8))

  # GAME RESULT
  # GAME RESULT
  # GAME RESULT
  for i in range(10):
    print("Game result")
    time.sleep(1)
    
  did_walk = False