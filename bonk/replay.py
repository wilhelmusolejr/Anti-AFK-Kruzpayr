# replay_keys.py
from pynput.keyboard import Controller, Key
import json
import time
import ast

keyboard = Controller()

with open("key_log.json", "r") as f:
    events = json.load(f)

start_time = events[0]["time"]

for i, event in enumerate(events):
    key = event["key"]
    if "Key." in key:
        # Handle special keys
        key = getattr(Key, key.split(".")[1])
    else:
        # Convert from string like "'w'" to 'w'
        key = ast.literal_eval(key)

    # Wait until the correct time
    delay = event["time"] - start_time
    if i > 0:
        time.sleep(delay - (events[i-1]["time"] - start_time))

    if event["event"] == "press":
        keyboard.press(key)
    elif event["event"] == "release":
        keyboard.release(key)
