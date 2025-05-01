import requests
import time

BOT_ID = input("Bot ID: ")
API_URL = "http://localhost:8000"

while True:
    # Set your actual bot state here (e.g., based on game logic)
    state = input(f"Enter state for {BOT_ID}: ")

    try:
        response = requests.post(f"{API_URL}/update", json={"bot_id": BOT_ID, "state": state})
        print(response.json())
    except Exception as e:
        print("❌ Failed to update:", e)

    time.sleep(1)
