import time
import xml.etree.ElementTree as ET
from pynput.keyboard import Controller, Key

keyboard = Controller()

# Razer makecode to key map (expand as needed)
MAKECODE_TO_KEY = {
    4: '3',     # Likely just macro starter
    17: 'w',
    30: 'a',
    32: 'd',
}

def parse_macro(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    macro_events = []

    for event in root.findall(".//MacroEvent"):
        delay_node = event.find("Delay")
        delay = int(delay_node.text) / 1000 if delay_node is not None else 0

        key_event = event.find("KeyEvent")
        makecode = int(key_event.find("Makecode").text)
        state = key_event.find("State")
        is_release = state is not None and state.text == '1'
        key = MAKECODE_TO_KEY.get(makecode)

        if key:
            macro_events.append({
                "delay": delay,
                "key": key,
                "action": "release" if is_release else "press"
            })

    return macro_events

def run_macro(events):
    print("▶️ Running macro in 3 seconds...")
    time.sleep(3)

    for event in events:
        time.sleep(event["delay"])
        if event["action"] == "press":
            keyboard.press(event["key"])
        else:
            keyboard.release(event["key"])
        print(f'{event["action"].capitalize()} {event["key"]}')

