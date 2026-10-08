import unittest
import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TestDDMMSSite(unittest.TestCase):
    def setUp(self):
        self.html_files = [
            "index.html",
            "publications.html",
            "about.html",
            "people.html",
            "research.html",
            "code.html"
        ]

    def test_html_files_exist_and_non_empty(self):
        for fname in self.html_files:
            p = BASE_DIR / fname
            self.assertTrue(p.exists(), f"{fname} does not exist")
            self.assertGreater(p.stat().st_size, 1000, f"{fname} is suspiciously small")

    def test_required_nav_menu_items(self):
        required_items = ["about", "people", "research", "publications", "code"]
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8").lower()
            for item in required_items:
                self.assertIn(item, content, f"Menu item '{item}' missing from {fname}")

    def test_mobile_friendly_viewport(self):
        viewport_regex = re.compile(r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*width=device-width[^"\']*["\']', re.IGNORECASE)
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertRegex(content, viewport_regex, f"Viewport meta tag missing or invalid in {fname}")

    def test_logo_files_exist(self):
        expected_logos = [
            "ddmms_for_light_modes.svg",
            "ddmms_for_dark_modes.svg",
            "ddmms_for_light_modes-with-text.svg",
            "ddmms_for_dark_modes-with-text.svg",
            "ddmms.svg"
        ]
        logos_dir = BASE_DIR / "assets" / "logos"
        for logo in expected_logos:
            p = logos_dir / logo
            self.assertTrue(p.exists(), f"Logo {logo} missing in {logos_dir}")

    def test_publications_json_validity(self):
        p = BASE_DIR / "publications.json"
        self.assertTrue(p.exists(), "publications.json does not exist")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "No publications in publications.json")

    def test_embedded_publications_script_in_publications_page(self):
        content = (BASE_DIR / "publications.html").read_text(encoding="utf-8")
        match = re.search(r'<script\s+id="publications-data"\s+type="application/json">\s*([\s\S]*?)\s*</script>', content)
        self.assertIsNotNone(match, "Embedded publications-data script missing in publications.html")
        data = json.loads(match.group(1))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_codes_showcase_in_code_page(self):
        code_content = (BASE_DIR / "code.html").read_text(encoding="utf-8").lower()
        expected_codes = ["janus-core", "aiida-mlip", "ml-peg", "goldilocks"]
        for c in expected_codes:
            self.assertIn(c, code_content, f"Expected code '{c}' not found in code.html")

    def test_goldilocks_ac_uk_and_psdi_presence(self):
        code_html = (BASE_DIR / "code.html").read_text(encoding="utf-8")
        about_html = (BASE_DIR / "about.html").read_text(encoding="utf-8")
        self.assertIn("goldilocks.ac.uk", code_html, "goldilocks.ac.uk not found in code.html")
        self.assertIn("psdi", about_html.lower(), "PSDI reference missing in about.html")
        self.assertIn("data to knowledge", about_html.lower(), "Data to Knowledge missing in about.html")

    def test_separate_navigation_links(self):
        for fname in self.html_files:
            content = (BASE_DIR / "fname" if False else BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('href="about.html"', content, f"Separate link about.html missing in {fname}")
            self.assertIn('href="people.html"', content, f"Separate link people.html missing in {fname}")
            self.assertIn('href="research.html"', content, f"Separate link research.html missing in {fname}")
            self.assertIn('href="publications.html"', content, f"Separate link publications.html missing in {fname}")
            self.assertIn('href="code.html"', content, f"Separate link code.html missing in {fname}")

    def test_css_and_js_assets_exist(self):
        self.assertTrue((BASE_DIR / "assets" / "css" / "style.css").exists())
        self.assertTrue((BASE_DIR / "assets" / "js" / "main.js").exists())
        self.assertTrue((BASE_DIR / "assets" / "js" / "publications.js").exists())

    def test_people_page_sections(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8").lower()
        self.assertIn("core members", people_html)
        self.assertIn("former members", people_html)
        self.assertIn("collaborator", people_html)
        self.assertIn("visitor", people_html)

    def test_people_page_collaborators_and_visitors_content(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn("Gilberto Teobaldi", people_html, "Collaborator Dr. Gilberto Teobaldi missing")
        self.assertIn("Matteo Salvalaglio", people_html, "Visitor Prof. Matteo Salvalaglio missing")
        self.assertIn("Jacob Wilkins", people_html, "Former member Dr. Jacob Wilkins missing")

    def test_people_subnav_anchors(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn('id="core-team"', people_html)
        self.assertIn('id="former-members"', people_html)
        self.assertIn('id="collaborators"', people_html)
        self.assertIn('id="visitors"', people_html)
        self.assertIn('id="contact"', people_html)


if __name__ == "__main__":
    unittest.main()

