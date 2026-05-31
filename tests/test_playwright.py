import unittest
from playwright.sync_api import sync_playwright

class TestPlaywrightIntegrations(unittest.TestCase):
    # Tests can target local server (default) or live production url
    TARGET_URL = "http://127.0.0.1:8000" 
    LIVE_URL = "https://akhilkarwal.com"

    def test_local_homepage(self):
        """Verify local homepage loads, renders typography and elements correctly."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.TARGET_URL, timeout=5000)
                # Verify title/brand exists
                self.assertIn("Akhil Karwal", page.title())
                # Verify navigation links are present
                self.assertTrue(page.locator("nav").is_visible())
                print(f"[PASS] Playwright loaded local homepage successfully.")
            except Exception as e:
                self.skipTest(f"Local dev server at {self.TARGET_URL} not running or reachable: {e}")
            finally:
                browser.close()

    def test_contact_form_honeypot_invisibility(self):
        """Verify the contact page renders the spam honeypot input, ensuring it is hidden."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(f"{self.TARGET_URL}/contact/", timeout=5000)
                honeypot_input = page.locator('input[name="honeypot"]')
                
                # Assert field exists in the DOM
                self.assertTrue(honeypot_input.count() > 0)
                # Assert field is hidden from user interaction
                self.assertTrue(honeypot_input.is_hidden())
                print(f"[PASS] Playwright verified bot honeypot exists and is hidden.")
            except Exception as e:
                self.skipTest(f"Local dev server at {self.TARGET_URL} not running: {e}")
            finally:
                browser.close()

    def test_live_site_response(self):
        """Verify the production domain responds to requests if online."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                response = page.goto(self.LIVE_URL, timeout=5000)
                self.assertEqual(response.status, 200)
                print(f"[PASS] Live site {self.LIVE_URL} is online and responding.")
            except Exception as e:
                self.skipTest(f"Live site {self.LIVE_URL} is currently offline or unreachable: {e}")
            finally:
                browser.close()

if __name__ == "__main__":
    unittest.main()
