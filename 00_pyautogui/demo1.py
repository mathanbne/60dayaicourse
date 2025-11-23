import pyautogui
import time
import webbrowser

# Enable PyAutoGUI's failsafe feature (move mouse to top-left corner to abort)
pyautogui.FAILSAFE = True

# Add a delay to give you time to prepare
print("Script will start in 3 seconds...")
print("Move mouse to top-left corner to abort anytime!")
time.sleep(3)

print("Step 1: Opening browser...")
# Open default browser with Google
webbrowser.open('https://www.google.com')

# Wait for browser to open and load
print("Waiting for browser to load...")
time.sleep(4)

print("Step 2: Clicking on search box...")
# Click on the search box (adjust coordinates if needed)
# This clicks in the middle-top area where Google search box usually is
pyautogui.click(x=702, y=468)
time.sleep(1)

print("Step 3: Typing search query...")
# Type the search query
pyautogui.typewrite('India Vs Australia t20 match score', interval=0.1)
time.sleep(1)

print("Step 4: Pressing Enter...")
# Press Enter to search
pyautogui.press('enter')
time.sleep(3)

print("Step 5: Clicking first result...")
# Click on first search result (approximate position)
# Adjust y-coordinate based on your screen resolution
pyautogui.click(x=500, y=350)

print("Done! Browser should show the cricket score.")
print("\nNote: If clicks were in wrong positions, you may need to adjust coordinates.")