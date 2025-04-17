import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Key  # <-- Make sure Key is imported
from pynput.mouse import Controller as MouseController, Button
import threading
import time

# Mouse Controller
keyboard = Controller()
mouse = MouseController()

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
def press_key_for_seconds(key, duration):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

# Globals
# Globals
# Globals
running = False
current_mode = None 

def stop_action():
    global running
    running = False
    status_label.config(text="...")

def anti_afk_loop():
  global running
  status_label.config(text="anti_afk_loop")  
  
  while running:
      press_key_for_seconds(Key.enter, 1)  
      time.sleep(10)
    
def anti_afk_and_drop():
  global running
  status_label.config(text="anti_afk_and_drop")  
  
  while running:
      press_key_for_seconds(Key.enter, 1)
      time.sleep(1)
      press_key_for_seconds('g', 1)
      time.sleep(9)
    
def auto_fire():
  global running
  status_label.config(text="auto_fire")
  
  while running:
    mouse.click(Button.left, 1)
    time.sleep(1)
    mouse.click(Button.left, 1)
    time.sleep(1)
    mouse.click(Button.left, 1)
    time.sleep(1)
    mouse.click(Button.left, 1)
    time.sleep(1)

def on_radio_select():
  global running, current_mode
  running = True
  selected = mode.get()
  
  if selected == current_mode:
    return  
  
  running = False  # Stop any previously running thread
  time.sleep(0.5)  # Give it a moment to stop cleanly

  current_mode = selected  # Update current mode
  running = True
  
  for i in range(5, 0, -1):
    status_label.config(text=f"Starts in {i} seconds, move to your game now")
    app.update()
    time.sleep(1)      
  
  if selected == "no_action":
        threading.Thread(target=stop_action).start()
  elif selected == "anti_afk":
        threading.Thread(target=anti_afk_loop).start()
  elif selected == "drop_gun":
        threading.Thread(target=anti_afk_and_drop).start()
  elif selected == "auto_fire":
        threading.Thread(target=auto_fire).start()

def on_closing():
    global running
    running = False  # Stop any background threads
    app.destroy()    # Close the window

# UI Setup
# UI Setup
# UI Setup
# UI Setup
app = tk.Tk()
app.title("AFK Tool")
app.geometry("400x400")

mode = tk.StringVar()
mode.set("no_action")

tk.Label(app, text="Select a Mode:", font=("Arial", 14)).pack(pady=10)

tk.Radiobutton(app, text="1. No Action", variable=mode, value="no_action", command=on_radio_select).pack(anchor='w')

# 2
tk.Radiobutton(app, text="2. ANTI AFK", variable=mode, value="anti_afk", command=on_radio_select).pack(anchor='w')
tk.Label(
    app,
    text="Simulates pressing the 'Enter' key every 10 seconds to avoid being idle.",
    fg="gray",
    wraplength=300,  
    justify="left"
).pack(anchor='w', padx=20)

# 3 
tk.Radiobutton(app, text="3. ANTI AFK + Drop Gun", variable=mode, value="drop_gun", command=on_radio_select).pack(anchor='w')
tk.Label(app, text="Presses 'Enter' and 'G' key every few seconds to simulate activity and drop your gun.", fg="gray", wraplength=300,  
    justify="left").pack(anchor='w', padx=20)

# 4
tk.Radiobutton(app, text="4. Auto Fire (for self boosting)", variable=mode, value="auto_fire", command=on_radio_select).pack(anchor='w')
tk.Label(app, text="triggers left mouse clicks for self-boosting or repeated attacks.", fg="gray", wraplength=300,  
    justify="left").pack(anchor='w', padx=20)


# 
# 
# 
status_label = tk.Label(
    app,
    text="...",
    fg="black",
    font=("Arial", 16),
    wraplength=300,
    justify="center"
)
status_label.pack(pady=10)

app.mainloop()





app.protocol("WM_DELETE_WINDOW", on_closing)




