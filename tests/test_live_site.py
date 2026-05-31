import unittest
import requests
import re

class TestLiveSiteFunctionality(unittest.TestCase):
    BASE_URL = "https://akhilkarwal.com"

    def setUp(self):
        self.session = requests.Session()

    def test_home_page_status_and_content(self):
        """Verify the homepage loads and contains the developer's name."""
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Akhil Karwal", response.text)
            print("[PASS] Homepage loaded and verified.")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Live site unreachable: {e}")

    def test_projects_page_status_and_content(self):
        """Verify the projects page loads successfully."""
        url = f"{self.BASE_URL}/projects/"
        try:
            response = self.session.get(url, timeout=10)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Projects", response.text)
            print("[PASS] Projects page loaded and verified.")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Live site unreachable: {e}")

    def test_contact_page_honeypot_present(self):
        """Verify the contact page loads and contains the bot spam honeypot input."""
        url = f"{self.BASE_URL}/contact/"
        try:
            response = self.session.get(url, timeout=10)
            self.assertEqual(response.status_code, 200)
            # The honeypot input tag should be present in the contact page source
            self.assertIn('name="honeypot"', response.text)
            self.assertIn('style="display: none; visibility: hidden;"', response.text)
            print("[PASS] Contact page and honeypot field verified.")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Live site unreachable: {e}")

    def test_security_headers_and_https_redirection(self):
        """Verify that HTTP redirects to HTTPS, and recommended security headers exist."""
        http_url = self.BASE_URL.replace("https://", "http://")
        try:
            # Test SSL Redirection
            http_response = self.session.get(http_url, timeout=10, allow_redirects=False)
            self.assertIn(http_response.status_code, [301, 302])
            self.assertTrue(http_response.headers.get('Location', '').startswith('https://'))

            # Test HTTPS production security headers (HSTS)
            https_response = self.session.get(self.BASE_URL, timeout=10)
            self.assertIn('Strict-Transport-Security', https_response.headers)
            print("[PASS] HTTPS redirection and security headers verified.")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Live site unreachable: {e}")

    def test_static_asset_caching(self):
        """Verify static CSS is served with optimal caching headers."""
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            # Parse stylesheet link
            style_matches = re.findall(r'href="([^"]+style\.css[^"]*)"', response.text)
            if style_matches:
                style_url = style_matches[0]
                if style_url.startswith('/'):
                    style_url = f"{self.BASE_URL}{style_url}"
                
                style_response = self.session.get(style_url, timeout=10)
                self.assertEqual(style_response.status_code, 200)
                
                cache_control = style_response.headers.get('Cache-Control', '')
                self.assertIn('max-age', cache_control)
                
                max_age_match = re.search(r'max-age=(\d+)', cache_control)
                if max_age_match:
                    max_age = int(max_age_match.group(1))
                    # Optimizations should have set max-age to at least 1 hour (3600) or 1 year (31536000)
                    self.assertTrue(max_age >= 3600, f"Cache duration is too low: {max_age}")
                print("[PASS] Static asset cache-control headers verified.")
            else:
                self.skipTest("No style.css link found on homepage to verify.")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Live site unreachable: {e}")

if __name__ == "__main__":
    unittest.main()
