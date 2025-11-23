from playwright.sync_api import sync_playwright
import time

print("=" * 60)
print("CRICKET SCORE SEARCH - PLAYWRIGHT VERSION")
print("=" * 60)
print("\nStarting browser automation...")
print("This is much better than coordinate-based clicking!")
time.sleep(2)

try:
    with sync_playwright() as p:
        print("\nStep 1: Launching browser...")
        # Launch browser (headless=False means you can see it)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("Step 2: Opening Google...")
        # Navigate to Google
        page.goto('https://www.google.com')
        time.sleep(1)
        
        print("Step 3: Finding search box...")
        # Find and click the search box using selector
        # Multiple ways to find it - this is more reliable than coordinates!
        search_box = page.locator('textarea[name="q"]')
        search_box.click()
        time.sleep(0.5)
        
        print("Step 4: Typing search query...")
        # Type the search query
        search_box.fill('India Vs Australia t20 match score')
        time.sleep(1)
        
        print("Step 5: Pressing Enter...")
        # Press Enter to search
        search_box.press('Enter')
        
        print("Step 6: Waiting for results to load...")
        # Wait for search results to appear
        page.wait_for_selector('h3', timeout=5000)
        time.sleep(2)
        
        print("Step 7: Clicking first result...")
        # Click the first search result
        first_result = page.locator('h3').first
        first_result.click()
        
        print("\n✓ Done! Browser should show the cricket score.")
        print("Browser will stay open for 10 seconds...")
        time.sleep(10)
        
        # Close browser
        browser.close()
        print("\nBrowser closed. Script complete!")
        
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    print("\nMake sure Playwright is installed:")
    print("  pip install playwright")
    print("  playwright install chromium")

print("\n" + "=" * 60)
print("SCRIPT FINISHED")
print("=" * 60)