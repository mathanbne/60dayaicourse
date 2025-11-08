import pyautogui
import time

# Safety feature - move mouse to corner to stop the script
pyautogui.FAILSAFE = True

# Pause between actions (in seconds)
pyautogui.PAUSE = 1

def main():
    print("Starting automation in 3 seconds...")
    time.sleep(3)
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size: {screen_width}x{screen_height}")
    
    # Get current mouse position
    current_x, current_y = pyautogui.position()
    print(f"Current mouse position: {current_x}, {current_y}")
    
    # Move mouse to specific coordinates
    pyautogui.moveTo(100, 100, duration=1)
    
    # Click at current position
    pyautogui.click()
    
    # Double click
    pyautogui.doubleClick()
    
    # Type some text
    pyautogui.write('Hello from PyAutoGUI!', interval=0.1)
    
    # Press specific keys
    pyautogui.press('enter')
    
    # Keyboard shortcuts
    pyautogui.hotkey('ctrl', 'a')  # Select all
    
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    print("Screenshot saved!")
    
    # Locate an image on screen (optional - requires a reference image)
    # location = pyautogui.locateOnScreen('button.png')
    # if location:
    #     pyautogui.click(location)

if __name__ == "__main__":
    main()