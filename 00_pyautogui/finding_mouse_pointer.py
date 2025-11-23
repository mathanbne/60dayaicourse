import pyautogui
import time

time.sleep(5)
x, y = pyautogui.position()
print(f"Current Mouse Position: X={x} Y={y}")

