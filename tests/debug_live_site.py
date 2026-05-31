# tests/debug_live_site.py
import sys
import os
from playwright.sync_api import sync_playwright

def debug_live():
    url = "https://akhilkarwal.com"
    screenshot_path = r"C:\Users\Akhil Karwal\.gemini\antigravity-cli\brain\8816b624-ff01-4a50-9c2f-ab48dfdf2159\live_site.png"
    print(f"Loading {url} and capturing debug data...")
    
    console_logs = []
    errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Listen to console logs and errors
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"Page Error: {err.message}"))
        
        try:
            response = page.goto(url, timeout=30000)
            print(f"Response status: {response.status}")
            
            # Wait for content to render
            page.wait_for_timeout(2000)
            
            # Take screenshot
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            # Print document element attribute
            html_theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
            print(f"HTML element data-theme attribute: '{html_theme}'")
            
            # Check toggle presence and checked state
            toggle_count = page.locator('#theme-toggle').count()
            if toggle_count > 0:
                toggle_checked = page.locator('#theme-toggle').is_checked()
                print(f"Toggle found: Yes, Checked: {toggle_checked}")
            else:
                print("Toggle found: No")
                
            # Print parsed style tags
            stylesheets = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('link[rel="stylesheet"]')).map(el => el.href);
            }""")
            print("Loaded Stylesheets:")
            for sheet in stylesheets:
                print(f" - {sheet}")
                
            print("\nConsole Logs:")
            for log in console_logs:
                print(log)
                
            print("\nPage Errors:")
            for err in errors:
                print(err)
                
        except Exception as e:
            print(f"Error during debug execution: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    debug_live()
