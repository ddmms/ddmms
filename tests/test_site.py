import unittest
import os
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class TestDDMMSSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (BASE_DIR / "index.html").exists():
            import build_site
            build_site.main()

    def setUp(self):
        self.html_files = [
            "index.html",
            "publications.html",
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
        required_items = ["about", "people", "research", "publications", "software"]
        for fname in ["header.html", "_includes/header.html"]:
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
            "ddmms.svg",
            "janus-core.svg",
            "aiida-mlip.svg",
            "janus-core.png",
            "aiida-mlip.png"
        ]
        logos_dir = BASE_DIR / "assets" / "logos"
        for logo in expected_logos:
            p = logos_dir / logo
            self.assertTrue(p.exists(), f"Logo {logo} missing in {logos_dir}")

    def test_code_page_uses_logos_for_janus_core_and_aiida_mlip(self):
        code_html = (BASE_DIR / "code.html").read_text(encoding="utf-8")
        self.assertIn("assets/logos/janus-core.svg", code_html)
        self.assertIn("assets/logos/aiida-mlip.svg", code_html)

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
        expected_codes = ["janus-core", "aiida-mlip", "aiidalab-mlip", "pack-mm", "ml-peg", "goldilocks"]
        for c in expected_codes:
            self.assertIn(c, code_content, f"Expected code '{c}' not found in code.html")

    def test_goldilocks_ac_uk_and_psdi_presence(self):
        code_html = (BASE_DIR / "code.html").read_text(encoding="utf-8")
        footer_html = (BASE_DIR / "footer.html").read_text(encoding="utf-8")
        research_html = (BASE_DIR / "research.html").read_text(encoding="utf-8")
        self.assertIn("goldilocks.ac.uk", code_html, "goldilocks.ac.uk not found in code.html")
        self.assertIn("goldilocks.ac.uk", research_html, "goldilocks.ac.uk not found in research.html")
        self.assertIn("ml-peg", research_html.lower(), "ml-peg not found in research.html")
        self.assertIn("psdi", footer_html.lower(), "PSDI reference missing in footer.html")
        self.assertIn("data to knowledge", footer_html.lower(), "Data to Knowledge missing in footer.html")

    def test_research_cards_include_goldilocks_and_ml_peg(self):
        research_html = (BASE_DIR / "research.html").read_text(encoding="utf-8")
        self.assertIn("Sustainable DFT &amp; k-Point Optimization (Goldilocks)", research_html)
        self.assertIn("Machine Learning Performance and Extrapolation Guide (ML-PEG)", research_html)

    def test_key_facts_card_removed(self):
        index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Key Facts &amp; Infrastructure", index_html)
        self.assertNotIn("Key Facts", index_html)

    def test_no_section_pills_across_site(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn("section-pill", content, f"Found unexpected section-pill in {fname}")

    def test_no_menu_matching_title_on_first_section(self):
        menu_titles = [
            ("index.html", "About"),
            ("people.html", "People"),
            ("research.html", "Research"),
            ("publications.html", "Publications"),
            ("code.html", "Software"),
            ("code.html", "Code"),
        ]
        for fname, title in menu_titles:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn(f'<h1 class="section-title">{title}</h1>', content, f"Found title matching menu name {title} in {fname}")
            self.assertNotIn(f'<h2 class="section-title">{title}</h2>', content, f"Found title matching menu name {title} in {fname}")

    def test_alin_elena_picture_used(self):
        img_path = BASE_DIR / "assets" / "images" / "alin_elena.jpg"
        self.assertTrue(img_path.exists(), "alin_elena.jpg image does not exist")
        self.assertGreater(img_path.stat().st_size, 1000, "alin_elena.jpg file is too small")
        self.assertIn("assets/images/alin_elena.jpg", (BASE_DIR / "people.html").read_text(encoding="utf-8"))

    def test_elliott_kasoar_picture_used(self):
        img_path = BASE_DIR / "assets" / "images" / "elliott_kasoar.jpg"
        self.assertTrue(img_path.exists(), "elliott_kasoar.jpg image does not exist")
        self.assertGreater(img_path.stat().st_size, 1000, "elliott_kasoar.jpg file is too small")
        self.assertIn("assets/images/elliott_kasoar.jpg", (BASE_DIR / "people.html").read_text(encoding="utf-8"))

    def test_junwen_yin_picture_used(self):
        img_path = BASE_DIR / "assets" / "images" / "junwen_yin.jpeg"
        self.assertTrue(img_path.exists(), "junwen_yin.jpeg image does not exist")
        self.assertGreater(img_path.stat().st_size, 1000, "junwen_yin.jpeg file is too small")
        self.assertIn("assets/images/junwen_yin.jpeg", (BASE_DIR / "people.html").read_text(encoding="utf-8"))

    def test_separate_navigation_links(self):
        for fname in ["header.html", "_includes/header.html", "footer.html", "_includes/footer.html"]:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('href="index.html"', content, f"Separate link index.html missing in {fname}")
            self.assertIn('href="people.html"', content, f"Separate link people.html missing in {fname}")
            self.assertIn('href="research.html"', content, f"Separate link research.html missing in {fname}")
            self.assertIn('href="publications.html"', content, f"Separate link publications.html missing in {fname}")
            self.assertIn('href="code.html"', content, f"Separate link code.html missing in {fname}")

    def test_no_software_and_feeds_in_footer(self):
        for fname in ["footer.html", "_includes/footer.html"]:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn("Software &amp; Feeds", content, f"Found Software & Feeds in {fname}")
            self.assertNotIn("Software & Feeds", content, f"Found Software & Feeds in {fname}")

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
        self.assertIn("Collaborator Name", people_html, "Collaborator placeholder missing")
        self.assertIn("Former Member Name", people_html, "Former Member placeholder missing")
        self.assertIn("Visitor Name", people_html, "Visitor placeholder missing")
        # Ensure specific names are removed
        self.assertNotIn("Matteo Salvalaglio", people_html)
        self.assertNotIn("Jacob Wilkins", people_html)
        self.assertNotIn("Francesca Peccati", people_html)
        self.assertNotIn("Alexander Neate", people_html)

    def test_people_subnav_anchors(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn('id="core-team"', people_html)
        self.assertIn('id="former-members"', people_html)
        self.assertIn('id="collaborators"', people_html)
        self.assertIn('id="visitors"', people_html)
        self.assertIn('id="contact"', people_html)

    def test_reusable_footer_file_exists_and_valid(self):
        footer_path = BASE_DIR / "footer.html"
        self.assertTrue(footer_path.exists(), "footer.html does not exist")
        footer_content = footer_path.read_text(encoding="utf-8")
        self.assertIn('<footer class="site-footer">', footer_content)
        self.assertIn("footer-grid", footer_content)
        self.assertIn("footer-links", footer_content)
        self.assertIn("Affiliations", footer_content)

    def test_includes_footer_file_exists(self):
        includes_footer = BASE_DIR / "_includes" / "footer.html"
        self.assertTrue(includes_footer.exists(), "_includes/footer.html does not exist")

    def test_build_site_get_footer_container(self):
        import build_site
        footer = build_site.get_footer()
        self.assertIn('id="site-footer"', footer)
        self.assertIn('data-include-footer', footer)

    def test_all_pages_reuse_footer(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('id="site-footer"', content, f"Footer container missing from {fname}")
            self.assertIn('data-include-footer', content, f"Footer include attribute missing from {fname}")

    def test_no_duplicate_footer_markup_in_pages(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn('<footer class="site-footer">', content, f"Duplicated footer markup found in {fname}")
            self.assertNotIn('<div class="footer-grid">', content, f"Duplicated footer grid found in {fname}")

    def test_reusable_header_file_exists_and_valid(self):
        header_path = BASE_DIR / "header.html"
        self.assertTrue(header_path.exists(), "header.html does not exist")
        header_content = header_path.read_text(encoding="utf-8")
        self.assertIn('<header class="site-header"', header_content)
        self.assertIn("brand-link", header_content)
        self.assertIn("nav-desktop", header_content)
        self.assertIn("mobile-drawer", header_content)

    def test_includes_header_file_exists(self):
        includes_header = BASE_DIR / "_includes" / "header.html"
        self.assertTrue(includes_header.exists(), "_includes/header.html does not exist")

    def test_build_site_get_header_container(self):
        import build_site
        header = build_site.get_header()
        self.assertIn('id="site-header"', header)
        self.assertIn('data-include-header', header)

    def test_all_pages_reuse_header(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('id="site-header"', content, f"Header container missing from {fname}")
            self.assertIn('data-include-header', content, f"Header include attribute missing from {fname}")

    def test_no_duplicate_header_markup_in_pages(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn('<header class="site-header"', content, f"Duplicated header markup found in {fname}")
            self.assertNotIn('<nav class="nav-desktop"', content, f"Duplicated nav desktop found in {fname}")
            self.assertNotIn('<div class="mobile-drawer"', content, f"Duplicated mobile drawer found in {fname}")

    def test_deploy_workflow_actions_upgraded_to_node24(self):
        wf = BASE_DIR / ".github" / "workflows" / "deploy.yml"
        self.assertTrue(wf.exists(), "deploy.yml missing")
        content = wf.read_text(encoding="utf-8")
        self.assertIn("actions/checkout@v7", content)
        self.assertIn("actions/setup-python@v7", content)
        self.assertIn("stefanzweifel/git-auto-commit-action@v7", content)
        self.assertIn("actions/configure-pages@v6", content)
        self.assertIn("actions/upload-pages-artifact@v5", content)
        self.assertIn("actions/deploy-pages@v5", content)
        # Ensure deprecated Node 20 versions are no longer referenced
        self.assertNotIn("actions/checkout@v4", content)
        self.assertNotIn("actions/setup-python@v5", content)
        self.assertNotIn("stefanzweifel/git-auto-commit-action@v5", content)
        self.assertNotIn("actions/configure-pages@v5", content)
        self.assertNotIn("actions/upload-pages-artifact@v3", content)
        self.assertNotIn("actions/deploy-pages@v4", content)

    def test_math_rendering_and_katex_assets(self):
        for fname in self.html_files:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn("katex.min.css", content, f"KaTeX CSS missing from {fname}")
            self.assertIn("katex.min.js", content, f"KaTeX JS missing from {fname}")
            self.assertIn("auto-render.min.js", content, f"KaTeX auto-render missing from {fname}")

        main_js = (BASE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
        self.assertIn("renderAllMath", main_js, "renderAllMath missing from main.js")
        self.assertIn("renderMathFallback", main_js, "renderMathFallback missing from main.js")

        style_css = (BASE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
        self.assertIn(".math-rendered", style_css, ".math-rendered missing from style.css")
        self.assertIn(".katex", style_css, ".katex missing from style.css")

    def test_about_page_highlights_and_landing_page(self):
        index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("Recent Highlights &amp; News", index_html)
        self.assertIn("Work With Us", index_html)
        self.assertIn("Contact the Group", index_html)
        # Ensure Recent Highlights & News appears above Work With Us / Contact
        highlights_pos = index_html.find("Recent Highlights &amp; News")
        contact_pos = index_html.find("Contact the Group")
        self.assertNotEqual(highlights_pos, -1)
        self.assertNotEqual(contact_pos, -1)
        self.assertLess(highlights_pos, contact_pos, "Recent Highlights & News must appear above Contact")

        # Brand links point to index.html as landing page
        for fname in ["header.html", "_includes/header.html"]:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('<a href="index.html" class="brand-link"', content)


if __name__ == "__main__":
    unittest.main()

