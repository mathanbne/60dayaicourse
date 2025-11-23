import pyautogui
import time
import webbrowser

# Enable PyAutoGUI's failsafe feature
pyautogui.FAILSAFE = True

print("=" * 60)
print("CRICKET SCORE AUTOMATION SCRIPT")
print("=" * 60)
print("\nIMPORTANT INSTRUCTIONS:")
print("1. Don't move your mouse during execution")
print("2. Move mouse to top-left corner to abort anytime")
print("3. Make sure your screen is visible (not minimized)")
print("\nDetecting your screen size...")

# Get screen size
screen_width, screen_height = pyautogui.size()
print(f"Screen Resolution: {screen_width} x {screen_height}")

# Calculate center positions based on screen size
center_x = screen_width // 2
search_box_y = screen_height // 3  # Search box is usually in upper third

print("\nScript will start in 5 seconds...")
print("Get ready!")
time.sleep(5)

try:
    print("\n[1/6] Opening Google in browser...")
    webbrowser.open('https://www.google.com')
    time.sleep(5)  # Wait for browser to fully load
    
    print("[2/6] Clicking on search box...")
    # Click in the center-upper area where search box should be
    pyautogui.click(x=center_x, y=search_box_y)
    time.sleep(1)
    
    print("[3/6] Typing search query...")
    # Type the search query with a slight delay between characters
    search_query = "India Vs Australia t20 match score"
    pyautogui.write(search_query, interval=0.05)
    time.sleep(1)
    
    print("[4/6] Pressing Enter to search...")
    pyautogui.press('enter')
    time.sleep(4)  # Wait for search results to load
    
    print("[5/6] Clicking first search result...")
    # First result is usually around this position
    first_result_x = center_x - 200
    first_result_y = search_box_y + 150
    pyautogui.click(x=first_result_x, y=first_result_y)
    time.sleep(2)
    
    print("[6/6] ✓ Complete! Check your browser for the cricket score.")
    
except pyautogui.FailSafeException:
    print("\n⚠ Script aborted by user (mouse moved to corner)")
except Exception as e:India Vs Australia t20 match score

    print(f"\n❌ Error occurred: {e}")
    print("You may need to adjust the coordinates for your screen.")

print("\n" + "=" * 60)
print("SCRIPT FINISHED")
print("=" * 60)