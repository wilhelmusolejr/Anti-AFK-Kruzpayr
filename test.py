from pynput.mouse import Controller

x = 620
y = 316

mouse = Controller()
mouse.position = (x, y)  # This does not raise a fail-safe
