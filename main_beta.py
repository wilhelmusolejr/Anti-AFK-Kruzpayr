# ----------------------
current_state = None
previous_state = None
sleeping_time = 5
# ----------------------

# FRAMEWORKS
# FRAMEWORKS
# FRAMEWORKS
from dotenv import load_dotenv
from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button
from image_analysis import state, saveScreenshot, get_screenshot
from telebram import sendMessage, sendScreenshot
from datetime import datetime
from ocr import userRoomStatus, get_exp, get_gp, get_kill

import threading
import pyautogui
import time
import random
import os

# Load environment variables from .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
user_type = os.getenv("USER_TYPE")
is_last_user = os.getenv("IS_LAST_USER", "False").lower() == "true"

# Controller
# Controller
# Controller
keyboard = Controller()
mouse = MouseController()
state_lock = threading.Lock()  

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# ----------------------
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
  shoot = random.randint(10, 30)  # Randomize the number of shots between 1 and 3
  for i in range(shoot):
    mouse.click(Button.right, 1)
    time.sleep(0.2)

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
  press_key_for_seconds('w', 0.6)
  press_key_for_seconds('d', 0.85)
  time.sleep(1)

# THREAD
# THREAD
# THREAD
# THREAD
def get_state():
    global current_state, sleeping_time

    while True:
        temp_state = state()
        if temp_state is not None:
            with state_lock:
                current_state = temp_state
        time.sleep(sleeping_time)
        
# ----------------------
# ----------------------
# ----------------------
# Start the state-checking thread
state_thread = threading.Thread(target=get_state, daemon=True)
state_thread.start()

main_loop = True
notify_user = False

while main_loop:
    chance_to_send = random.randint(1, 1000)  

    with state_lock:
        snapshot_state = current_state  

    if snapshot_state != previous_state:
        print(f"State changed from {previous_state} to {snapshot_state}")
        print(f"[{snapshot_state.upper()}] - START")

        # LOBBY
        if snapshot_state == "inlobby":
            # Record the time when entering lobby
            lobby_enter_time = time.time()  

            click_okay_button()
            time.sleep(1)

            if user_type in ["shooter", "earner"]:
                click_to_right()
                time.sleep(1)

            user_room_status = userRoomStatus()

            while True:
                with state_lock:
                    if current_state != "inlobby":
                        break  # if state changed, exit

                elapsed_time = time.time() - lobby_enter_time
                
                if elapsed_time > 120 and not notify_user:
                    sendMessage(f"⏱️ Client {client_id} has been in the lobby for over 60 seconds. Screenshot saved for review.")
                    saveScreenshot("inlobby/error")
                    time.sleep(1)
                    sendScreenshot()
                    time.sleep(1)
                    lobby_enter_time = time.time()  
                    notify_user = True  # set flag to avoid multiple notifications

                # Update room status
                user_room_status = userRoomStatus()
                
                # If user late to join
                if user_room_status == "join game":
                    click_ready_button()
                    time.sleep(5)

                    click_okay_button()
                    time.sleep(1)

                    click_to_right()
                    time.sleep(1)
                    
                    click_ready_button()
                    time.sleep(1)
                    
                    click_okay_button()
                    time.sleep(1)
                    continue
                
                # To avoid lobby AFK
                if user_room_status == "cancel":
                    click_okay_button()
                    time.sleep(1)
                    
                    continue

                # USER
                if user_room_status == "ready!" and not is_last_user:
                    click_ready_button()
                    time.sleep(1)
                    
                    continue
                
                # HOST
                if user_room_status == "start":
                    click_ready_button()
                    time.sleep(10)
                    continue
                
                # LAST USER
                if is_last_user:
                    if user_room_status == "join game":
                        click_ready_button()
                        time.sleep(10)
                        
                        click_okay_button()
                        time.sleep(1)
                        
                        click_to_right()
                        time.sleep(1)
                        click_ready_button()
                        continue
                
        # GAME
        if snapshot_state == "ingame":
            if user_type == "shooter":
                ready_to_walk()

            while True:
                with state_lock:
                    if current_state != "ingame":
                        break

                if user_type == "shooter":
                    ready_to_fire()

                if user_type == "bot":
                    press_key_for_seconds('a', 2)

                time.sleep(1)

        # GAME RESULT
        if snapshot_state == "ingameresult":
            if chance_to_send == 3:
              saveScreenshot("ingameresult")
              time.sleep(1)
            
            if user_type == "shooter":
              gp = get_gp()
              exp = get_exp()
              kills = get_kill()

              message = (
                  f"💰 GP       =  {gp}\n"
                  f"📈 EXP     =  {exp}\n"
                  f"🔫 KILLS  =  {kills}"
              )
              
              sendMessage(message)
            
            notify_user = False
              
            time.sleep(10) # make all client to prepare for the next phase
          
        # GAME OUTSIDE  
        if snapshot_state == "inoutside":
            sendMessage(f"🚨 ALERT: Client {client_id} is outside the room!")
            time.sleep(1)
            saveScreenshot("inoutside")
            time.sleep(1)
            sendScreenshot()
            time.sleep(1)
            main_loop = False

        previous_state = snapshot_state  # Update after processing

    if chance_to_send == 1:
        saveScreenshot("random")
        time.sleep(2)

    print(f"Current state: {current_state}")

    time.sleep(1)