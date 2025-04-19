from pynput.keyboard import Controller, Key 
from pynput.mouse import Controller as MouseController, Button

import tkinter as tk
import threading
import pyautogui
import time

# Controller
keyboard = Controller()
mouse = MouseController()

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
    pyautogui.click()
    
def mouse_click(duration):
    mouse.click(Button.left, 1)
    time.sleep(duration)
    mouse.release(Button.left)    

def click_center_screen():
    screen_width, screen_height = pyautogui.size()
    
    # Center of the screen
    x = int(screen_width * 0.5)
    y = int(screen_height * 0.5)
    
    pyautogui.moveTo(x, y)
    time.sleep(0.3)
    pyautogui.click()
# Globals
# Globals
# Globals
running_event = threading.Event()
current_mode = None 

def stop_action():
    status_label.config(text="Please select a mode to begin.")

def anti_afk_loop():
    global current_mode
    status_label.config(text="Running...")  
  
    while running_event.is_set() and current_mode == "anti_afk":
        press_key_for_seconds(Key.enter, 1)  
        time.sleep(10)
    
def anti_afk_and_drop():
    global current_mode
        
    status_label.config(text="Running...")  
    
    while running_event.is_set() and current_mode == "drop_gun":
        # Press and hold left button
        click_center_screen()
        mouse_click(2)
        
        press_key_for_seconds('g', 1)
        press_key_for_seconds(Key.enter, 1)
        press_key_for_seconds('g', 1)
        press_key_for_seconds(Key.enter, 1)
        press_key_for_seconds('g', 1)
        
        # Press and hold left button
        mouse_click(2)
        
        time.sleep(2)
        click_ready_button()
        click_center_screen()
        time.sleep(2)
    
def auto_fire():
    global current_mode
    
    shots = 0
    shot_count = 5
    while running_event.is_set() and current_mode == "auto_fire":
        # mouse_click(2)
        # status_label.config(text=f"{shots} shots fired!")
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        mouse.click(Button.left, 1)
        time.sleep(0.3)
        
        
        shots += shot_count
        time.sleep(3)
        click_ready_button()

def on_radio_select():
    global current_mode

    selected = mode.get()
    if selected == current_mode:
        return

    # Stop any currently running thread
    running_event.clear()
    time.sleep(0.2)  # give the previous thread time to exit

    current_mode = selected  # set the new mode

    if selected != "no_action":
        for i in range(5, 0, -1):
            status_label.config(text=f"Starts in {i} seconds, move to your game now.")
            app.update()
            time.sleep(1)

    if selected == "no_action":
        status_label.config(text="Please select a mode to begin.")
        return

    # Start a new thread
    running_event.set()
    if selected == "anti_afk":
        threading.Thread(target=anti_afk_loop, daemon=True).start()
    elif selected == "drop_gun":
        threading.Thread(target=anti_afk_and_drop, daemon=True).start()
    elif selected == "auto_fire":
        threading.Thread(target=auto_fire, daemon=True).start()

def on_closing():
    try:
        running_event.clear()
        app.destroy()
    except:
        pass  # Ignore errors if already closed


# UI Setup
# UI Setup
# UI Setup
# UI Setup
app = tk.Tk()
app.title("Kruzpayr Anti AFK Tool")
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
    text="Welcome! Please select a mode to begin.",
    fg="black",
    font=("Arial", 16),
    wraplength=300,
    justify="center"
)
status_label.pack(pady=10)

def open_link(event):
    import webbrowser
    webbrowser.open_new("https://wilhelmus.vercel.app?ref=anti_afk")  # Replace with your link

dev_label = tk.Label(
    app,
    text="Developed by TC.666",
    fg="red",
    cursor="hand2",
    font=("Arial", 14, "underline")
)
dev_label.pack(side="bottom", pady=10)
dev_label.bind("<Button-1>", open_link)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()




