# tests/test_live_darkmode.py
import sys
import time
from playwright.sync_api import sync_playwright

def verify_live_dark_mode():
    url = "https://akhilkarwal.com"
    print(f"Connecting to live site: {url} using Playwright...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(url, timeout=20000)
            print("Loaded homepage successfully.")
            
            # 1. Inspect initial theme attribute on <html> element
            initial_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
            print(f"Initial theme state in DOM: '{initial_theme}'")
            
            # 2. Find the theme toggle checkbox
            toggle = page.locator('#theme-toggle')
            if toggle.count() == 0:
                print("[FAIL] Could not find #theme-toggle checkbox in DOM!")
                sys.exit(1)
                
            print("Found #theme-toggle checkbox.")
            
            # Verify if it is checked
            initial_checked = toggle.is_checked()
            print(f"Checkbox initial checked status: {initial_checked}")
            
            # 3. Trigger click directly on the checkbox overlay
            print("Clicking theme toggle checkbox...")
            toggle.click(force=True)
            
            # Wait for transition/animation
            time.sleep(1)
            
            # 4. Inspect new theme attribute on <html>
            new_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
            new_checked = toggle.is_checked()
            print(f"New theme state in DOM: '{new_theme}'")
            
            # Verify status
            if new_theme != initial_theme and new_checked != initial_checked:
                print(f"[SUCCESS] Theme toggle is FULLY FUNCTIONAL! Switched from '{initial_theme}' to '{new_theme}'!")
                # Toggle back to original state to clean up local storage context
                toggle.click(force=True)
                browser.close()
                return True
            else:
                print(f"[FAIL] Click did not toggle theme state correctly! Initial: '{initial_theme}', New: '{new_theme}'")
                browser.close()
                sys.exit(1)
                
        except Exception as e:
            print(f"[ERROR] Verification failed: {e}")
            browser.close()
            sys.exit(1)

if __name__ == "__main__":
    verify_live_dark_mode()
