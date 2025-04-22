from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(f"🖱️ Mouse clicked at ({x}, {y}) with {button}")

# Start listening
with Listener(on_click=on_click) as listener:
    print("🎯 Listening for mouse clicks... Press Ctrl+C to stop.")
    listener.join()
