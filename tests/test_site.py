import unittest
import os
import json
import re
import sys
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class TestDDMMSSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if (
            not (BASE_DIR / "index.html").exists()
            or not (BASE_DIR / "header.html").exists()
            or not (BASE_DIR / "footer.html").exists()
        ):
            import build_site
            build_site.main()

    def setUp(self):
        self.html_files = [
            "index.html",
            "publications.html",
            "people.html",
            "research.html",
            "code.html",
            "news.html",
            "teaching.html",
            "collaborate.html",
            "talks.html",
            "events.html",
        ]


    def test_html_files_exist_and_non_empty(self):
        for fname in self.html_files:
            p = BASE_DIR / fname
            self.assertTrue(p.exists(), f"{fname} does not exist")
            self.assertGreater(p.stat().st_size, 1000, f"{fname} is suspiciously small")

    def test_required_nav_menu_items(self):
        content = (BASE_DIR / "header.html").read_text(encoding="utf-8")
        content_lower = content.lower()
        # Awards and News have been removed from the navigation menu
        self.assertNotIn("awards.html", content_lower, "awards.html should not be in header.html navigation menu")
        self.assertNotIn("news", content_lower, "news should not be in header.html navigation menu")
        # 5 main entries + sub-items exist in collapsible menu
        main_entries = ["home", "people", "research", "publications", "software"]
        sub_items = ["talks", "teaching", "events"]
        for item in main_entries + sub_items:
            self.assertIn(item, content_lower, f"Menu item '{item}' missing from header.html")
        # Top menu (nav-desktop) is removed; only the collapsible corner menu is retained
        self.assertNotIn("nav-desktop", content, "nav-desktop should be removed in favor of corner menu")
        self.assertIn("corner-menu-btn", content, "corner-menu-btn toggle missing in header.html")
        self.assertIn("corner-menu-panel", content, "corner-menu-panel missing in header.html")

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
            "aiida-mlip.png",
            "pack-mm.svg",
            "pack-mm-light-text.svg",
            "pack-mm-light-notext.svg",
            "pack-mm-dark-text.svg",
            "pack-mm-dark-notext.svg",
        ]
        logos_dir = BASE_DIR / "assets" / "logos"
        for logo in expected_logos:
            p = logos_dir / logo
            self.assertTrue(p.exists(), f"Logo {logo} missing in {logos_dir}")

    def test_code_page_uses_logos_for_janus_core_and_aiida_mlip(self):
        code_html = (BASE_DIR / "code.html").read_text(encoding="utf-8")
        self.assertIn("assets/logos/janus-core.svg", code_html)
        self.assertIn("assets/logos/aiida-mlip.svg", code_html)
        self.assertIn("assets/logos/pack-mm.svg", code_html)

    def test_publications_json_validity(self):
        p = BASE_DIR / "publications.json"
        self.assertTrue(p.exists(), "publications.json does not exist")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "No publications in publications.json")
        for pub in data:
            self.assertIn("authors", pub, f"Missing authors in pub: {pub.get('title')}")
            self.assertIsInstance(pub["authors"], list)
            self.assertGreater(len(pub["authors"]), 0, f"Empty authors list for: {pub.get('title')}")
            # If preprint or arxiv, preprint_doi must be set
            if pub.get("arxiv_id") or (pub.get("doi") and "arxiv" in pub["doi"].lower()) or ("arxiv" in (pub.get("journal") or "").lower() and (not pub.get("doi") or "arxiv" in pub.get("doi", "").lower())):
                self.assertIsNotNone(pub.get("preprint_doi"), f"Missing preprint_doi for preprint: {pub.get('title')}")
                self.assertTrue(pub["preprint_doi"].startswith("10.48550/arXiv."), f"Invalid preprint_doi format: {pub.get('preprint_doi')}")

    def test_awards_completely_removed(self):
        self.assertFalse((BASE_DIR / "data" / "awards.yaml").exists(), "data/awards.yaml should not exist")
        self.assertFalse((BASE_DIR / "src" / "components" / "awards.py").exists(), "src/components/awards.py should not exist")
        self.assertFalse((BASE_DIR / "awards.html").exists(), "awards.html should not exist")
        build_site_py = (BASE_DIR / "src" / "build_site.py").read_text(encoding="utf-8")
        self.assertNotIn("awards", build_site_py.lower(), "src/build_site.py should have no references to awards")

    def test_publications_markdown_has_authors_and_preprint_dois(self):
        pub_md = (BASE_DIR / "PUBLICATIONS.md").read_text(encoding="utf-8")
        self.assertIn(" by ", pub_md, "PUBLICATIONS.md should list authors with 'by'")
        self.assertIn("10.48550/arXiv.", pub_md, "PUBLICATIONS.md should include preprint DOIs")

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
        # Goldilocks pipeline and agent; feature text is one inline span so bold words stay in the sentence
        for pkg in ("goldilocks-data", "goldilocks-ml", "goldilocks-core", "goldilocks-agent"):
            self.assertIn(f"<li><span><strong>{pkg}</strong>", code_html)
        # No install command until one works
        self.assertNotIn("pip install goldilocks", code_html)
        self.assertIn("goldilocks.ac.uk", research_html, "goldilocks.ac.uk not found in research.html")
        self.assertIn("ml-peg", research_html.lower(), "ml-peg not found in research.html")
        self.assertIn("psdi", footer_html.lower(), "PSDI reference missing in footer.html")
        self.assertIn("data to knowledge", footer_html.lower(), "Data to Knowledge missing in footer.html")

    def test_research_cards_include_goldilocks_and_ml_peg(self):
        research_html = (BASE_DIR / "research.html").read_text(encoding="utf-8")
        self.assertIn('<h1 class="page-hero-title">Research Areas</h1>', research_html)
        self.assertNotIn("Research Themes", research_html)
        self.assertIn("Sustainable DFT through Data-Driven Agents (Goldilocks)", research_html)
        self.assertIn("Machine Learning Performance and Extrapolation Guide (ML-PEG)", research_html)

    def test_research_funding_pills(self):
        research_html = (BASE_DIR / "research.html").read_text(encoding="utf-8")
        self.assertIn('class="research-funding"', research_html)
        self.assertIn('class="funding-label"', research_html)
        self.assertIn('class="funding-pill"', research_html)
        self.assertIn("PSDI Data to Knowledge", research_html)
        self.assertIn("EP/X032701/1", research_html)
        self.assertIn("EP/V028537/1", research_html)
        self.assertIn("Ada Lovelace Centre", research_html)
        self.assertIn("STFC Scientific Computing", research_html)

        from components.research import generate_research_html
        # Test string-based funding
        rendered = generate_research_html({
            "themes": [{
                "title": "Quantum ML",
                "description": "Test desc",
                "funding": ["EPSRC EP/TEST1234", "STFC Facility"]
            }]
        })
        self.assertIn("EPSRC EP/TEST1234", rendered)
        self.assertIn("STFC Facility", rendered)
        self.assertIn('class="funding-pill"', rendered)

        # Test dictionary-based funding with URL
        rendered_dict = generate_research_html({
            "themes": [{
                "title": "Quantum ML",
                "funding": [{"programme": "Horizon Europe", "grant": "101010", "url": "https://example.com/grant"}]
            }]
        })
        self.assertIn("Horizon Europe (101010)", rendered_dict)
        self.assertIn('href="https://example.com/grant"', rendered_dict)

    def test_research_images(self):
        research_html = (BASE_DIR / "research.html").read_text(encoding="utf-8")
        self.assertIn('class="research-card has-image"', research_html)
        self.assertIn('class="research-card-media"', research_html)
        self.assertIn('class="research-card-image"', research_html)
        self.assertIn("assets/images/highlights/184110_1_5.0297006.figures.online.f3.jpg", research_html)
        self.assertIn("assets/images/research/mofs.jpg", research_html)
        self.assertIn("assets/images/research/molten_salts.jpg", research_html)
        self.assertIn("assets/images/research/workflows.jpg", research_html)
        self.assertIn("assets/images/research/goldilocks.jpg", research_html)
        self.assertIn("assets/images/research/ml_peg.jpg", research_html)

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

        # Verify personal page uses the new picture while people page retains the current picture
        personal_img = BASE_DIR / "assets" / "images" / "alin_elena_personal.jpg"
        self.assertTrue(personal_img.exists(), "alin_elena_personal.jpg does not exist")
        self.assertGreater(personal_img.stat().st_size, 1000, "alin_elena_personal.jpg is too small")
        alin_page = (BASE_DIR / "alin-marin-elena.html").read_text(encoding="utf-8")
        self.assertIn("assets/images/alin_elena_personal.jpg", alin_page)

        # Verify that profile picture is positioned on the right (details element appears before avatar)
        details_pos = alin_page.find("profile-header-details")
        avatar_pos = alin_page.find("profile-header-avatar-wrap")
        self.assertGreater(avatar_pos, details_pos, "Profile header avatar should be placed on the right of details")

        # Verify bio hyperlinks are properly rendered as HTML anchors
        self.assertIn('href="https://camml.ac.uk"', alin_page)
        self.assertIn('href="https://gtr.ukri.org/person/041472A8-A559-4803-8020-1E0AC0E5D905"', alin_page)
        self.assertNotIn('[CaMML school]', alin_page)

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
        header_content = (BASE_DIR / "header.html").read_text(encoding="utf-8")
        self.assertIn('href="index.html"', header_content, "Separate link index.html missing in header.html")
        self.assertIn('href="people.html"', header_content, "Separate link people.html missing in header.html")
        self.assertIn('href="research.html"', header_content, "Separate link research.html missing in header.html")
        self.assertIn('href="publications.html"', header_content, "Separate link publications.html missing in header.html")
        self.assertIn('href="code.html"', header_content, "Separate link code.html missing in header.html")
        self.assertIn('href="teaching.html"', header_content, "Separate link teaching.html missing in header.html")
        self.assertIn('href="talks.html"', header_content, "Separate link talks.html missing in header.html")
        self.assertIn('href="events.html"', header_content, "Separate link events.html missing in header.html")
        # Neither header nor footer should contain excluded entries outside the menu and submenus
        for fname in ["header.html", "footer.html"]:
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertNotIn('href="awards.html"', content, f"awards.html should not be in navigation {fname}")
            self.assertNotIn('href="news.html"', content, f"news.html should not be in navigation {fname}")
            self.assertNotIn('href="opportunities.html"', content, f"opportunities.html should not be in navigation {fname}")
            self.assertNotIn('href="collaborate.html"', content, f"collaborate.html should not be in navigation {fname}")
            self.assertNotIn('href="index.html#news"', content, f"News section link should not be in navigation {fname}")

    def test_no_software_and_feeds_in_footer(self):
        content = (BASE_DIR / "footer.html").read_text(encoding="utf-8")
        self.assertNotIn("Software &amp; Feeds", content, "Found Software & Feeds in footer.html")
        self.assertNotIn("Software & Feeds", content, "Found Software & Feeds in footer.html")

    def test_css_and_js_assets_exist(self):
        self.assertTrue((BASE_DIR / "assets" / "css" / "style.css").exists())
        self.assertTrue((BASE_DIR / "assets" / "js" / "main.js").exists())
        self.assertTrue((BASE_DIR / "assets" / "js" / "publications.js").exists())

    def test_people_page_sections(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8").lower()
        self.assertIn("members", people_html)
        self.assertNotIn("core members", people_html)
        self.assertIn("former members", people_html)
        self.assertIn("collaborators", people_html)
        # Collaborators, research networks and the contact block live on the Collaborate page
        self.assertNotIn("collaborative research networks", people_html)
        self.assertNotIn("get in touch via email", people_html)

    def test_people_page_has_no_placeholders(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        for placeholder in ("Collaborator Name", "Former Member Name", "Visitor Name", 'href="#"'):
            self.assertNotIn(placeholder, people_html, f"Placeholder {placeholder!r} should not be published")
        # Ensure specific names are removed
        self.assertNotIn("Matteo Salvalaglio", people_html)
        self.assertNotIn("Francesca Peccati", people_html)
        self.assertNotIn("Alexander Neate", people_html)
        self.assertIn("Dr Jacob Wilkins", people_html)

    def test_people_subnav_anchors(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn('id="members"', people_html)
        self.assertIn('id="former-members"', people_html)
        self.assertIn('id="collaborators"', people_html)
        for moved_id in ("contact",):
            self.assertNotIn(f'id="{moved_id}"', people_html)
        # Empty sections (and their jump links) are hidden until members are added
        for empty_id in ("visitors",):
            self.assertNotIn(f'id="{empty_id}"', people_html)
            self.assertNotIn(f'href="#{empty_id}"', people_html)
        # Subnav pills are shown for quick section navigation
        self.assertIn('class="subnav-pills"', people_html)
        self.assertIn('href="#members"', people_html)
        self.assertIn('href="#former-members"', people_html)
        self.assertIn('href="#collaborators"', people_html)

    def test_people_sections_hidden_until_filled(self):
        from components.people import generate_people_html

        rendered = generate_people_html({
            "sections": [
                {"id": "former-members", "title": "Former Members", "members": [
                    {"name": "Real Person", "role": "Postdoc", "affiliation": "STFC"},
                ]},
                {"id": "visitors", "title": "Visitors", "members": []},
            ],
        })
        self.assertIn('id="former-members"', rendered)
        self.assertIn("Real Person", rendered)
        self.assertNotIn('id="visitors"', rendered)
        self.assertNotIn('href="#visitors"', rendered)

    def test_people_uses_short_bio_and_profile_uses_bio(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        alin_html = (BASE_DIR / "alin-marin-elena.html").read_text(encoding="utf-8")

        # people.html uses short_bio
        self.assertIn("Group Leader of DDMMS focusing on machine-learned interatomic potentials", people_html)
        self.assertNotIn("Alin is the scientific secretary of", people_html)

        # Individual profile uses full bio
        self.assertIn("Alin is the scientific secretary of", alin_html)
        self.assertIn("Alin leads the Data Driven Materials and Molecular Science research group.", alin_html)

    def test_reusable_footer_file_exists_and_valid(self):
        footer_path = BASE_DIR / "footer.html"
        self.assertTrue(footer_path.exists(), "footer.html does not exist")
        footer_content = footer_path.read_text(encoding="utf-8")
        self.assertIn('<footer class="site-footer">', footer_content)
        self.assertIn("footer-grid", footer_content)
        self.assertIn("footer-links", footer_content)
        self.assertIn("Affiliations", footer_content)
        # Footer menu is removed since the header menu is always sticky on
        self.assertNotIn("footer-nav-pills", footer_content)

    def test_build_site_get_footer_container(self):
        import build_site
        footer = build_site.get_footer()
        self.assertIn('id="site-footer"', footer)
        self.assertIn('data-include-footer', footer)
        full_footer = build_site.get_footer(full_markup=True)
        self.assertIn('<footer class="site-footer">', full_footer)

    def test_build_site_generate_footer_html(self):
        import build_site
        footer = build_site.generate_footer_html()
        self.assertIn('<footer class="site-footer">', footer)
        self.assertIn("footer-grid", footer)
        self.assertIn("Affiliations", footer)

    def test_footer_template_file_reading(self):
        import build_site
        import tempfile
        template_content = '<footer class="custom-footer">Custom Footer {{ year }}</footer>'
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".html") as tf:
            tf.write(template_content)
            tf_path = Path(tf.name)

        try:
            rendered = build_site.generate_footer_html(template_file=tf_path, year=2099)
            self.assertIn('<footer class="custom-footer">Custom Footer 2099</footer>', rendered)
        finally:
            if tf_path.exists():
                tf_path.unlink()

    def test_footer_template_missing_raises_error(self):
        import build_site
        with self.assertRaises(FileNotFoundError):
            build_site.generate_footer_html(template_file="/nonexistent/footer_template.html")

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
        self.assertNotIn("nav-desktop", header_content)
        self.assertIn("mobile-drawer", header_content)
        self.assertNotIn("subpage-nav-bar", header_content)
        self.assertIn("corner-menu-btn", header_content)
        self.assertIn("corner-menu-panel", header_content)

    def test_build_site_get_header_container(self):
        import build_site
        header = build_site.get_header()
        self.assertIn('id="site-header"', header)
        self.assertIn('data-include-header', header)
        full_header = build_site.get_header(full_markup=True)
        self.assertIn('<header class="site-header"', full_header)

    def test_build_site_generate_header_html(self):
        import build_site
        header = build_site.generate_header_html()
        self.assertIn('<header class="site-header"', header)
        self.assertIn("brand-link", header)
        self.assertNotIn("nav-desktop", header)
        self.assertIn("corner-menu-btn", header)
        self.assertIn("corner-menu-panel", header)

    def test_header_template_file_reading(self):
        import build_site
        import tempfile
        template_content = '<header class="custom-header">Custom Header</header>'
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".html") as tf:
            tf.write(template_content)
            tf_path = Path(tf.name)

        try:
            rendered = build_site.generate_header_html(template_file=tf_path)
            self.assertIn('<header class="custom-header">Custom Header</header>', rendered)
        finally:
            if tf_path.exists():
                tf_path.unlink()

    def test_header_template_missing_raises_error(self):
        import build_site
        with self.assertRaises(FileNotFoundError):
            build_site.generate_header_html(template_file="/nonexistent/header_template.html")

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
        self.assertIn("actions/upload-artifact@v4", content)
        # Ensure deprecated Node 20 versions are no longer referenced
        self.assertNotIn("actions/checkout@v4", content)
        self.assertNotIn("actions/setup-python@v5", content)
        self.assertNotIn("stefanzweifel/git-auto-commit-action@v5", content)
        self.assertNotIn("actions/configure-pages@v5", content)
        self.assertNotIn("actions/upload-pages-artifact@v3", content)
        self.assertNotIn("actions/deploy-pages@v4", content)
        self.assertNotIn("actions/upload-artifact@v3", content)


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
        # Homepage is a single column: no sidebar
        self.assertNotIn('class="about-grid"', index_html)
        # Homepage sections: mission, news, collaborate (opportunities section removed)
        self.assertIn('id="news"', index_html)
        self.assertNotIn('id="opportunities"', index_html)
        self.assertIn('id="collaborate"', index_html)
        self.assertLess(index_html.index('id="mission"'), index_html.index('id="news-section"'))

        # Mission prose contains hyperlinks to CMMS, SCD, STFC, UKRI, Daresbury, Rutherford Appleton
        self.assertIn('href="https://www.sc.stfc.ac.uk/research-and-expertise/computational-materials-and-molecular-science/"', index_html)
        self.assertIn('href="https://www.sc.stfc.ac.uk/"', index_html)
        self.assertIn('href="https://www.ukri.org/councils/stfc/"', index_html)
        self.assertIn('href="https://www.ukri.org/"', index_html)
        self.assertIn('href="https://www.ukri.org/who-we-are/stfc/facilities/daresbury-laboratory/"', index_html)
        self.assertIn('href="https://www.ukri.org/who-we-are/stfc/facilities/rutherford-appleton-laboratory/"', index_html)

        # Brand links point to index.html as landing page
        content = (BASE_DIR / "header.html").read_text(encoding="utf-8")
        self.assertIn('<a href="index.html" class="brand-link"', content)

    def test_load_news_yaml(self):
        import tempfile
        from build_site import load_news

        # Test loading the actual data/news.yaml
        news = load_news()
        self.assertIsInstance(news, list)
        self.assertGreaterEqual(len(news), 4)
        has_linked_item = False
        has_unlinked_item = False
        for item in news:
            self.assertIn("date", item)
            self.assertIn("headline", item)
            self.assertIn("link", item)
            self.assertTrue(item["date"])
            self.assertTrue(item["headline"])
            if item["link"]:
                has_linked_item = True
            else:
                has_unlinked_item = True
        self.assertTrue(has_linked_item, "Expected at least one news item with a link")
        self.assertTrue(has_unlinked_item, "Expected at least one news item without a link")

        # Test custom YAML news loading
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tyf:
            tyf.write("""- date: "2026 YAML Tag"
  headline: "YAML Headline with link"
  link: "https://example.com/yaml"
- date: "2026 YAML Tag 2"
  headline: "YAML Headline without link"
""")
            tyf_path = Path(tyf.name)

        try:
            custom_yaml_news = load_news(tyf_path)
            self.assertEqual(len(custom_yaml_news), 2)
            self.assertEqual(custom_yaml_news[0]["date"], "2026 YAML Tag")
            self.assertEqual(custom_yaml_news[0]["headline"], "YAML Headline with link")
            self.assertEqual(custom_yaml_news[0]["link"], "https://example.com/yaml")
            self.assertEqual(custom_yaml_news[1]["date"], "2026 YAML Tag 2")
            self.assertEqual(custom_yaml_news[1]["link"], "")
        finally:
            if tyf_path.exists():
                tyf_path.unlink()

        # Non-existent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_news(Path("/nonexistent/file.yaml"))

    def test_load_research_yaml(self):
        import tempfile
        from build_site import load_research, generate_research_html

        # Test loading the actual data/research.yaml
        research_data = load_research()
        self.assertIsInstance(research_data, dict)
        self.assertIn("approach", research_data)
        self.assertIn("themes", research_data)
        self.assertGreaterEqual(len(research_data["themes"]), 6)

        # Verify theme structure
        for item in research_data["themes"]:
            self.assertIn("title", item)
            self.assertIn("description", item)
            self.assertTrue(item["title"])
            self.assertTrue(item["description"])

        # Test custom YAML research loading
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as trf:
            trf.write("""approach:
  subtitle: "Custom research approach subtitle"

themes:
  - tag: "Custom Theme"
    title: "Novel Materials Design"
    description: "Custom description text for materials."
    links:
      - text: "Explore &rarr;"
        url: "https://example.com/custom"
""")
            trf_path = Path(trf.name)

        try:
            custom_data = load_research(trf_path)
            self.assertEqual(custom_data["approach"]["subtitle"], "Custom research approach subtitle")
            self.assertEqual(len(custom_data["themes"]), 1)
            self.assertEqual(custom_data["themes"][0]["title"], "Novel Materials Design")

            rendered_html = generate_research_html(custom_data)
            self.assertIn("Custom research approach subtitle", rendered_html)
            self.assertIn("Novel Materials Design", rendered_html)
            self.assertIn("https://example.com/custom", rendered_html)
            # No small uppercase labels above theme titles; a leftover tag is ignored
            self.assertNotIn("Custom Theme", rendered_html)
            self.assertNotIn("research-tag", rendered_html)
        finally:
            if trf_path.exists():
                trf_path.unlink()

        # Non-existent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_research(Path("/nonexistent/file.yaml"))

    def test_load_people_yaml(self):
        import tempfile
        from build_site import load_people, generate_people_html

        # Test loading the actual data/people.yaml
        people_data = load_people()
        self.assertIsInstance(people_data, dict)
        self.assertIn("sections", people_data)
        section_ids = [s["id"] for s in people_data["sections"]]
        self.assertTrue("members" in section_ids or "core-team" in section_ids)
        self.assertIn("former-members", section_ids)
        self.assertIn("alc-phd", section_ids)
        self.assertIn("collaborators", section_ids)
        self.assertIn("visitors", section_ids)

        # Verify members include key researchers
        core_section = next(s for s in people_data["sections"] if s["id"] in ("core-team", "members"))
        names = [m["name"] for m in core_section["members"]]
        self.assertIn("Dr. Alin Marin Elena", names)
        self.assertIn("Elliott Kasoar", names)
        self.assertIn("Dr. Junwen Yin", names)

        # Verify ALC PhD programme members
        phd_section = next(s for s in people_data["sections"] if s["id"] == "alc-phd")
        phd_names = [m["name"] for m in phd_section["members"]]
        self.assertIn("Loki Coward", phd_names)
        self.assertIn("Atharva Anturkar", phd_names)
        self.assertIn("Mueen Taj", phd_names)

        # Verify collaborators include research partners
        collab_section = next(s for s in people_data["sections"] if s["id"] == "collaborators")
        collab_names = [m["name"] for m in collab_section["members"]]
        self.assertIn("Prof Alexander Shluger", collab_names)
        self.assertIn("Dr Keith Butler", collab_names)
        self.assertIn("Dr Jeff Armstrong", collab_names)
        self.assertIn("Prof Gábor Csányi", collab_names)
        self.assertIn("Dr Jacob Wilkins", collab_names)
        self.assertIn("Dr Marco Molinari", collab_names)
        self.assertIn("Prathami Kamath", collab_names)
        self.assertIn("Dr Théo Jaffrelot Inizan", collab_names)
        self.assertIn("Prof Petra Ágota Szilágyi", collab_names)
        for m in collab_section["members"]:
            self.assertTrue(m.get("avatar", "").startswith("assets/images/"))

        # Test custom YAML people loading
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tpf:
            tpf.write("""subtitle: "Custom team description."
sections:
  - id: "custom-group"
    title: "Specialists"
    subtitle: "Custom subgroup"
    members:
      - name: "Alice Wonderland"
        role: "Quantum Architect"
        affiliation: "Wonderland Lab"
        bio: "Exploring rabbit holes in quantum algorithms."
        tags:
          - "Quantum"
        links:
          - text: "Profile"
            url: "https://example.com/alice"
""")
            tpf_path = Path(tpf.name)

        try:
            custom_data = load_people(tpf_path)
            self.assertEqual(custom_data["subtitle"], "Custom team description.")
            self.assertEqual(len(custom_data["sections"]), 1)
            self.assertEqual(custom_data["sections"][0]["members"][0]["name"], "Alice Wonderland")

            rendered_html = generate_people_html(custom_data)
            self.assertIn("Custom team description.", rendered_html)
            self.assertIn("Specialists", rendered_html)
            self.assertIn("Alice Wonderland", rendered_html)
            self.assertIn("https://example.com/alice", rendered_html)
            self.assertNotIn('class="subnav-pills"', rendered_html, "one section needs no jump links")

            two_sections = {"sections": [
                {"id": "a", "title": "A", "members": [{"name": "Person A"}]},
                {"id": "b", "title": "B", "members": [{"name": "Person B"}]},
            ]}
            rendered_html = generate_people_html(two_sections)
            self.assertIn('<a href="#a" class="subnav-pill">A</a>', rendered_html)
            self.assertIn('<a href="#b" class="subnav-pill">B</a>', rendered_html)
        finally:
            if tpf_path.exists():
                tpf_path.unlink()

        # Non-existent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_people(Path("/nonexistent/file.yaml"))

    def test_load_software_yaml(self):
        import tempfile
        from build_site import load_software, generate_code_html

        # Test loading the actual data/software.yaml
        software_data = load_software()
        self.assertIsInstance(software_data, dict)
        self.assertEqual(software_data.get("title"), "Software &amp; Skills")
        self.assertIn("packages", software_data)
        pkg_ids = [p["id"] for p in software_data["packages"]]
        expected_pkgs = ["janus-core", "aiida-mlip", "aiidalab-mlip", "pack-mm", "ml-peg", "goldilocks"]
        for exp in expected_pkgs:
            self.assertIn(exp, pkg_ids)

        code_html = (BASE_DIR / "code.html").read_text(encoding="utf-8")
        self.assertIn("Software &amp; Skills", code_html)
        self.assertNotIn("Software &amp; Tools", code_html)

        # Test custom YAML software loading
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tsf:
            tsf.write("""subtitle: "Custom software tools suite."
packages:
  - id: custom-tool
    name: "custom-tool"
    icon: "🚀"
    badge:
      text: "CLI / HPC"
      style: "background:#eef2ff; color:#4338ca;"
    description: "High speed materials generator."
    install: "pip install custom-tool"
    features:
      - "Ultra fast batching"
    links:
      - text: "Repository"
        url: "https://example.com/custom-tool"
""")
            tsf_path = Path(tsf.name)

        try:
            custom_data = load_software(tsf_path)
            self.assertEqual(custom_data["subtitle"], "Custom software tools suite.")
            self.assertEqual(len(custom_data["packages"]), 1)
            self.assertEqual(custom_data["packages"][0]["name"], "custom-tool")

            rendered_html = generate_code_html(custom_data)
            self.assertIn("Custom software tools suite.", rendered_html)
            self.assertIn("custom-tool", rendered_html)
            self.assertIn("pip install custom-tool", rendered_html)
            self.assertIn("Ultra fast batching", rendered_html)
            self.assertIn("https://example.com/custom-tool", rendered_html)
        finally:
            if tsf_path.exists():
                tsf_path.unlink()

        # Non-existent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_software(Path("/nonexistent/file.yaml"))

    def test_load_mission_yaml(self):
        import tempfile
        from build_site import load_mission, generate_index_html

        # Test loading the actual data/mission.yaml
        mission_data = load_mission()
        self.assertIsInstance(mission_data, dict)
        self.assertIn("title", mission_data)
        self.assertIn("paragraphs", mission_data)
        self.assertEqual(mission_data["title"], "The Group Mission")
        self.assertGreaterEqual(len(mission_data["paragraphs"]), 3)

        # Test custom YAML mission loading
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tmf:
            tmf.write("""title: "Custom Group Vision"
subtitle: "Pioneering atomic intelligence."
paragraphs:
  - "Custom mission paragraph one describing high accuracy simulation."
  - "Custom mission paragraph two detailing open-source pipelines."
""")
            tmf_path = Path(tmf.name)

        try:
            custom_data = load_mission(tmf_path)
            self.assertEqual(custom_data["title"], "Custom Group Vision")
            self.assertEqual(custom_data["subtitle"], "Pioneering atomic intelligence.")
            self.assertEqual(len(custom_data["paragraphs"]), 2)

            rendered_html = generate_index_html(mission=custom_data)
            self.assertIn("Custom Group Vision", rendered_html)
            self.assertIn("Pioneering atomic intelligence.", rendered_html)
            self.assertIn("Custom mission paragraph one describing high accuracy simulation.", rendered_html)
            self.assertIn('<p class="home-lead">', rendered_html)
        finally:
            if tmf_path.exists():
                tmf_path.unlink()

        # Non-existent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_mission(Path("/nonexistent/file.yaml"))

    def test_index_affiliations_carousel(self):
        index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
        main_js = (BASE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")

        # Carousel sits at the top of the page, before the mission text
        self.assertIn('class="hero-carousel"', index_html)
        self.assertIn("data-carousel", index_html)
        self.assertIn('data-interval="5000"', index_html)
        self.assertLess(index_html.index('class="hero-carousel"'), index_html.index('id="mission"'))
        # The mission keeps its original tagline under the heading
        self.assertIn('<p class="home-subtitle">Using statistical physics, quantum mechanics', index_html)

        for title in (
            "Data Driven Materials and Molecular Science Group",
            "MACE-MP: Foundation Model for Materials Chemistry",
            "ML-PEG: Machine Learning Performance and Extrapolation Guide",
            "Project Goldilocks: AI-Driven DFT Automation",
        ):
            self.assertIn(f'<h2 class="slide-title">{title}</h2>', index_html)
        # No small uppercase labels above headings; the department slide has no buttons
        # and its title sits above the chain
        for label_cls in ("slide-eyebrow", "home-eyebrow"):
            self.assertNotIn(label_cls, index_html)
        self.assertEqual(index_html.count('class="slide-links"'), 3)
        self.assertLess(index_html.index("Molecular Science Group</h2>"), index_html.index('class="org-chain"'))
        for url in (
            "https://www.ukri.org/",
            "https://www.ukri.org/councils/stfc/",
            "https://www.sc.stfc.ac.uk/",
            "https://www.sc.stfc.ac.uk/research-and-expertise/computational-materials-and-molecular-science/",
            "https://doi.org/10.1063/5.0297006",
            "https://ml-peg.stfc.ac.uk",
            "https://goldilocks.ac.uk",
        ):
            self.assertIn(f'href="{url}"', index_html)

        # Prev/next buttons and one dot per slide, wired up in main.js
        self.assertIn('class="carousel-btn carousel-prev"', index_html)
        self.assertIn('class="carousel-btn carousel-next"', index_html)
        self.assertEqual(index_html.count('class="carousel-dot"'), 4)
        self.assertIn("function initCarousels()", main_js)
        self.assertIn("startAutoplay", main_js)

        # Organisational chain ends with the DDMMS group highlighted
        for short in ("UKRI", "STFC", "SCD", "CMMS", "DDMMS"):
            self.assertIn(f'<span class="org-chain-short">{short}</span>', index_html)
        self.assertEqual(index_html.count("org-chain-step is-current"), 1)

        # Institutional branding colors and logos on hero rectangles
        self.assertIn('data-org="stfc"', index_html)
        self.assertIn('--step-color: #0072ce', index_html, "STFC rectangle must use STFC branding blue")
        self.assertIn('data-org="ukri"', index_html)
        self.assertIn('data-org="scd"', index_html)
        self.assertIn('data-org="cmms"', index_html)
        self.assertIn('data-org="ddmms"', index_html)

        # Institutional logos rendered for organisations that have one
        for logo_file in ("ukri.svg", "stfc.png", "scd.svg", "ddmms.svg"):
            self.assertIn(f'src="assets/logos/{logo_file}"', index_html)
            self.assertTrue((BASE_DIR / "assets" / "logos" / logo_file).is_file(), f"Missing logo {logo_file}")
        # CMMS has no logo wrap
        self.assertNotIn('src="assets/logos/cmms', index_html)

        # Highlight images are referenced and exist on disk
        for img_rel in (
            "highlights/184110_1_5.0297006.figures.online.f3.jpg",
            "research/ml_peg.jpg",
            "research/goldilocks.jpg",
        ):
            self.assertIn(f'src="assets/images/{img_rel}"', index_html)
            self.assertTrue((BASE_DIR / "assets" / "images" / img_rel).is_file(), f"Missing image {img_rel}")

    def test_render_affiliations_carousel_html(self):
        from components.index import render_affiliations_carousel_html

        self.assertEqual(render_affiliations_carousel_html(None), "")
        self.assertEqual(render_affiliations_carousel_html({"title": "No slides"}), "")

        rendered = render_affiliations_carousel_html({
            "title": "Where We Work",
            "slides": [
                {
                    "title": "Org Slide",
                    "hierarchy": [
                        {"short": "A", "name": "Alpha", "url": "https://example.com/alpha", "logo": "assets/logos/a.svg"},
                        {"short": "B", "name": "Beta", "badge": "Us"},
                    ],
                    "links": [{"text": "Org site", "url": "https://example.com/org"}],
                },
                {
                    "title": "Photo Slide",
                    "image": "assets/images/site.jpg",
                    "image_alt": 'Site "main" building',
                    "image_position": "20% 50%",
                    "text_side": "right",
                },
            ],
        })
        self.assertIn('aria-label="Where We Work"', rendered)
        self.assertIn('aria-label="1 of 2: Org Slide"', rendered)
        self.assertIn('<ol class="org-chain" aria-label="Organisational hierarchy: A &gt; B">', rendered)
        self.assertIn('<img src="assets/logos/a.svg" alt="A logo" class="org-chain-logo"', rendered)
        self.assertIn('<a href="https://example.com/alpha" class="org-chain-name org-chain-link"', rendered)
        self.assertIn('<span class="org-chain-name">Beta</span>', rendered)
        self.assertIn('<span class="org-chain-badge">Us</span>', rendered)
        self.assertEqual(rendered.count("is-current"), 1)
        self.assertIn('href="https://example.com/org"', rendered)
        self.assertIn('alt="Site &quot;main&quot; building"', rendered)
        self.assertIn('style="object-position: 20% 50%;"', rendered)
        self.assertIn('class="carousel-slide carousel-slide-photo slide-text-right"', rendered)
        self.assertEqual(rendered.count('class="carousel-dot"'), 2)

        # A single slide needs no prev/next controls
        single = render_affiliations_carousel_html({"slides": [{"title": "Only"}]})
        self.assertNotIn("carousel-controls", single)

    def test_collaborate_page(self):
        import tempfile
        from components.collaborate import load_collaborate, generate_collaborate_html

        collab_html = (BASE_DIR / "collaborate.html").read_text(encoding="utf-8")
        self.assertIn("<title>Collaborate | Data Driven Materials and Molecular Science</title>", collab_html)
        self.assertIn('<h1 class="page-hero-title">Collaborate With Us</h1>', collab_html)
        self.assertNotIn('class="feature-list"', collab_html, "no filler lists without real content")
        self.assertIn('href="mailto:', collab_html)
        # About research collaboration
        self.assertNotIn("prospective PhD", collab_html)
        self.assertNotIn('opportunities.html', collab_html)
        # Collaborators and research networks, moved here from the People page
        self.assertIn('<section class="home-section" id="collaborators">', collab_html)
        self.assertIn('<h3 class="network-title">Collaborative Research Networks</h3>', collab_html)
        for url in ("https://www.psdi.ac.uk", "https://www.ccp5.ac.uk", "https://mace-docs.readthedocs.io", "https://www.scd.stfc.ac.uk"):
            self.assertIn(f'href="{url}"', collab_html)
        self.assertLess(collab_html.index('id="collaborators"'), collab_html.index('id="contact"'))

        data = load_collaborate()
        self.assertEqual(data["title"], "Collaborate With Us")

        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tf:
            tf.write("""title: "Join Us"
intro: "Custom intro."
sections:
  - title: "Roles"
    items: ["Role A", "Role B"]
contact:
  title: "Say hello"
  description: "Write to us."
  email: "someone@example.com"
""")
            tf_path = Path(tf.name)
        try:
            rendered = generate_collaborate_html(load_collaborate(tf_path))
            self.assertIn('<h1 class="page-hero-title">Join Us</h1>', rendered)
            self.assertIn('<span class="feature-index">02</span>', rendered)
            self.assertIn('<span class="feature-label">Role B</span>', rendered)
            self.assertIn('href="mailto:someone@example.com"', rendered)
            self.assertIn("Say hello", rendered)
            self.assertNotIn('id="collaborators"', rendered, "no collaborators block without data")

            rendered = generate_collaborate_html({
                "title": "Join Us",
                "collaborators": {
                    "title": "Partners",
                    "intro": "Who we work with.",
                    "networks_title": "Networks",
                    "networks": [{"text": "Net A", "url": "https://example.com/a"}, {"text": "No URL"}],
                },
            })
            self.assertIn('<h2 class="home-heading">Partners</h2>', rendered)
            self.assertIn('<p class="home-lead">Who we work with.</p>', rendered)
            self.assertIn('<h3 class="network-title">Networks</h3>', rendered)
            self.assertIn('<div class="link-buttons">', rendered)
            self.assertIn('href="https://example.com/a"', rendered)
            self.assertNotIn("No URL", rendered, "links without a url are skipped")
        finally:
            tf_path.unlink()

        with self.assertRaises(FileNotFoundError):
            load_collaborate(Path("/nonexistent/collaborate.yaml"))

    def test_teaching_page(self):
        import tempfile
        from components.teaching import load_teaching, generate_teaching_html

        teaching_html = (BASE_DIR / "teaching.html").read_text(encoding="utf-8")
        self.assertIn("<title>Training | Data Driven Materials and Molecular Science</title>", teaching_html)

        # Sections
        categories = [
            ("upcoming", "Upcoming"),
            ("schools", "Schools"),
        ]
        for cat_id, cat_title in categories:
            self.assertIn(f'<section class="category-section" id="{cat_id}">', teaching_html)
            self.assertIn(f'<h2 class="home-heading">{cat_title}</h2>', teaching_html)
            self.assertIn(f'<a href="#{cat_id}" class="subnav-pill">{cat_title}</a>', teaching_html)
        self.assertIn("CaMML Spring School 2027", teaching_html)
        # Check sections exist / don't exist
        self.assertNotIn('id="placements"', teaching_html)
        self.assertNotIn('id="graduate-scheme"', teaching_html)
        self.assertNotIn('id="workshops"', teaching_html)
        self.assertNotIn('id="phd"', teaching_html)
        self.assertNotIn("PhD Programme", teaching_html)
        self.assertNotIn("STFC Graduate Scheme", teaching_html)
        self.assertNotIn("stfccareers.co.uk", teaching_html)
        self.assertNotIn('href="collaborate.html#contact"', teaching_html)
        self.assertNotIn('opportunities.html', teaching_html)
        self.assertNotIn("Atharva Anturkar", teaching_html)

        self.assertIn("CCP5 Summer School", teaching_html)
        self.assertIn("Newcastle University", teaching_html)
        self.assertIn("Daresbury Laboratory", teaching_html)
        self.assertIn('href="https://summer2026.ccp5.ac.uk"', teaching_html)
        self.assertIn("assets/images/ccp5_summer_2026.png", teaching_html)
        self.assertIn("assets/images/ccp5_2025.png", teaching_html)
        self.assertIn("assets/images/ccp5_2024.webp", teaching_html)
        self.assertIn('href="https://spring2026.camml.ac.uk"', teaching_html)
        self.assertIn("assets/images/camml_spring_2026.jpeg", teaching_html)
        self.assertIn('href="https://spring2025.camml.ac.uk/about/"', teaching_html)
        self.assertIn('href="https://ase-lib.org/events/2025-06-Lausanne-workshop/"', teaching_html)
        self.assertIn("assets/images/ase_lausanne_2025.jpg", teaching_html)
        self.assertIn('href="https://summer2024.ccp5.ac.uk"', teaching_html)
        self.assertIn('href="https://www.psdi.ac.uk/event/machine-learning-autumn-school-2023/"', teaching_html)
        self.assertIn("Machine Learning for Atomistic Modelling Autumn School", teaching_html)
        self.assertIn('href="https://ase-lib.org/events/2023-04-Daresbury-workshop/"', teaching_html)
        self.assertIn("assets/images/ase_daresbury_2023.jpg", teaching_html)
        self.assertIn("Open Science with the Atomic Simulation Environment", teaching_html)
        self.assertIn('href="https://www.ccpnth.ac.uk/events/ai4nth2026/"', teaching_html)
        self.assertIn("Lecturer: Junwen Yin", teaching_html)
        self.assertIn('href="https://www.mcc.hec.ac.uk/events/ml-training-july-2025/"', teaching_html)
        self.assertIn("Organiser: Elliott Kasoar", teaching_html)
        self.assertIn("Machine Learning Interatomic Potentials (MLIPs) Training Workshop", teaching_html)
        self.assertIn('href="https://indico.ictp.it/event/10842/other-view?view=ictptimetable"', teaching_html)
        self.assertIn("Magurele Summer School for Computing in a Rapidly Evolving Society", teaching_html)
        self.assertIn("Lecturer: Alin Elena · Keynote Speaker: Alin Elena", teaching_html)
        # Every event photo referenced in training.yaml exists on disk
        for cat in load_teaching().get("categories") or []:
            for event in cat.get("events") or []:
                if event.get("image"):
                    self.assertTrue((BASE_DIR / event["image"]).is_file(), f"Missing image {event['image']}")

        # PhD programme moved to People page
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn("Atharva Anturkar", people_html)
        self.assertIn("Mueen Taj", people_html)
        self.assertIn("ALC PhD Programme", people_html)

        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tf:
            tf.write("""title: "Courses"
categories:
  - id: "schools"
    title: "Schools"
    events:
      - year: "2030"
        title: "Linked School"
        role: "Lecturers"
        description: "A week of lectures."
        url: "https://example.com/school"
      - year: "2029"
        title: "Unlinked Workshop"
        image: "assets/images/workshop.jpg"
        image_alt: "Group photo"
      - year: "2028"
  - id: "empty"
    title: "Empty"
  - id: "untitled"
""")
            tf_path = Path(tf.name)
        try:
            rendered = generate_teaching_html(load_teaching(tf_path))
            self.assertIn('<h1 class="page-hero-title">Courses</h1>', rendered)
            self.assertIn('href="https://example.com/school"', rendered)
            self.assertIn('<span class="teaching-role">Lecturers</span>', rendered)
            self.assertIn("A week of lectures.", rendered)
            self.assertIn('<h3 class="teaching-title">Unlinked Workshop</h3>', rendered)
            self.assertEqual(rendered.count('class="teaching-item'), 2, "events without a title are skipped")
            self.assertIn('<li class="teaching-item has-image">', rendered)
            self.assertIn('<img class="teaching-image" src="assets/images/workshop.jpg" alt="Group photo" loading="lazy">', rendered)
            self.assertEqual(rendered.count("Details coming soon."), 1, "only the empty category gets the placeholder")
            self.assertEqual(rendered.count('class="category-section"'), 2, "categories without a title are skipped")
        finally:
            tf_path.unlink()

        with self.assertRaises(FileNotFoundError):
            load_teaching(Path("/nonexistent/training.yaml"))

    def test_category_sections_renderer(self):
        from components.sections import render_category_sections

        subnav, sections = render_category_sections([
            {"id": "one", "title": "One", "description": "About one.",
             "cards": [
                 {"title": "Linked Card", "url": "https://example.com/card", "status": "Open",
                  "details": [
                      {"label": "Who", "value": "Someone"},
                      {"label": "Where", "value": "Somewhere", "url": "https://example.com/where"},
                      {"label": "Skipped"},
                  ],
                  "description": "What it is.",
                  "links": [{"text": "Apply", "url": "https://example.com/apply"}]},
                 {"title": "Bare Card"},
                 {"status": "No title"},
             ],
             "members_title": "Team",
             "members": [{"name": "Ada Lovelace"}, {"name": "Plato"}, {"role": "No name"}],
             "links": [
                 {"text": "External", "url": "https://example.com/ext"},
                 {"text": "Internal", "url": "collaborate.html#contact"},
                 {"text": "No URL"},
             ]},
            {"id": "two", "title": "Two", "members": [{"name": "Solo Person"}]},
        ], "Test navigation")
        self.assertIn('<nav class="subnav-pills" aria-label="Test navigation">', subnav)
        self.assertIn('<a href="#two" class="subnav-pill">Two</a>', subnav)
        self.assertIn('<p class="category-desc">About one.</p>', sections)
        # Cards: badge, details with optional links, buttons inside the card
        self.assertEqual(sections.count('<li class="info-card">'), 2, "cards without a title are skipped")
        self.assertIn('<span class="card-status">Open</span>', sections)
        self.assertIn("<dt>Who</dt>", sections)
        self.assertIn("<dd>Someone</dd>", sections)
        self.assertIn('<dd><a href="https://example.com/where"', sections)
        self.assertNotIn("<dt>Skipped</dt>", sections)
        self.assertIn('<p class="card-desc">What it is.</p>', sections)
        self.assertIn('href="https://example.com/apply"', sections)
        self.assertIn('<h3 class="card-title">Bare Card</h3>', sections)
        # Members: initials, optional heading
        self.assertIn('<h3 class="category-subheading">Team</h3>', sections)
        self.assertIn('<span class="member-initials" aria-hidden="true">AL</span>Ada Lovelace</li>', sections)
        self.assertIn('<span class="member-initials" aria-hidden="true">P</span>Plato</li>', sections)
        self.assertEqual(sections.count('class="member-chip"'), 3)
        self.assertEqual(sections.count("category-subheading"), 1, "no heading without members_title")
        # Links: external in a new tab, internal in the same tab, after everything else
        self.assertIn('href="https://example.com/ext" target="_blank"', sections)
        self.assertIn('<a href="collaborate.html#contact" class="person-link-btn">', sections)
        self.assertNotIn("No URL", sections)
        one = sections[:sections.index('id="two"')]
        self.assertLess(one.index("member-list"), one.index("https://example.com/ext"))
        # A single category needs no jump links
        subnav, _ = render_category_sections([{"id": "solo", "title": "Solo"}], "x")
        self.assertEqual(subnav, "")

    def test_opportunities_removed(self):
        self.assertFalse((BASE_DIR / "data" / "opportunities.yaml").exists())
        self.assertFalse((BASE_DIR / "opportunities.html").exists())
        # Verify training.yaml exists and is loaded
        from components.teaching import load_training, TRAINING_FILE
        self.assertTrue(TRAINING_FILE.is_file())
        training_data = load_training()
        self.assertIn("categories", training_data)

    def test_talks_page(self):
        import tempfile
        from components.talks import load_talks, generate_talks_html

        talks_html = (BASE_DIR / "talks.html").read_text(encoding="utf-8")
        self.assertIn("<title>Talks | Data Driven Materials and Molecular Science</title>", talks_html)
        self.assertIn("ML-PEG: Machine Learning Performance and Extrapolation Guide", talks_html)
        self.assertIn("NVIDIA Atomistic Simulation Summit 2026", talks_html)
        self.assertIn("Machine Learned Potentials for Phonon Calculations of Metal–Organic Frameworks", talks_html)
        self.assertIn("UKPorMat", talks_html)
        self.assertIn("uk-porous-materials-(ukpormat)-annual-conference-2026", talks_html)
        self.assertIn("Bridging the Gap Between Theory and Experiment", talks_html)
        self.assertIn("XAFS 2026", talks_html)
        self.assertIn("https://xafs2026.org/XAFS2026/", talks_html)
        self.assertIn("Machine Learning Performance and Extrapolation Guide (ML-PEG)", talks_html)
        self.assertIn("a-roadmap-for-an-atomistic-machine-learning-software-ecosystem-1376", talks_html)
        self.assertIn("Dr. Alin Marin Elena", talks_html)
        self.assertIn("Elliott Kasoar", talks_html)
        self.assertIn("https://agm46.ccp5.ac.uk/", talks_html)
        self.assertIn("MCC Conference 2026", talks_html)
        self.assertIn("https://www.mcc.hec.ac.uk/events/mcc-conference-2026/", talks_html)
        self.assertIn("Ada Lovelace Centre Scientific Computing Showcase Event", talks_html)
        self.assertIn("https://indico.stfc.ac.uk/event/1554/timetable/?view=standard_numbered", talks_html)
        self.assertIn("Keynote: HPC Best Practices", talks_html)
        self.assertIn("https://indico.ictp.it/event/10842/other-view?view=ictptimetable", talks_html)
        self.assertIn("10th International Workshop of Materials Physics", talks_html)
        self.assertIn("https://infim.ro/event/10th-international-workshop-of-materials-physics/", talks_html)
        self.assertIn("COSY Semester Opening Event", talks_html)
        self.assertIn("https://porelab.no/2025/08/12/cosy-semester-opening-event/", talks_html)
        self.assertIn("MMM Hub Software Spotlight: Janus ML", talks_html)
        self.assertIn("https://thomasyoungcentre.org/event/mmm-hub-software-spotlight-janus-ml/", talks_html)

        # Empty state when there are no talks
        rendered = generate_talks_html({"title": "Talks", "talks": []})
        self.assertIn('<p class="list-empty">', rendered)
        self.assertNotIn('class="talks-list"', rendered)

        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False, suffix=".yaml") as tf:
            tf.write("""title: "Seminars"
talks:
  - year: "2030"
    title: "Linked Talk"
    type: "Invited talk"
    speaker: "Ada Lovelace"
    event: "Big Conference, Manchester"
    description: "About machine-learned potentials."
    url: "https://example.com/slides"
  - year: "2029"
    title: "Unlinked Talk"
  - year: "2028"
""")
            tf_path = Path(tf.name)
        try:
            rendered = generate_talks_html(load_talks(tf_path))
            self.assertIn('<h1 class="page-hero-title">Seminars</h1>', rendered)
            self.assertIn('href="https://example.com/slides"', rendered)
            self.assertIn('<span class="talk-type">Invited talk</span>', rendered)
            self.assertIn('<p class="talk-meta">Ada Lovelace &middot; Big Conference, Manchester</p>', rendered)
            self.assertIn("About machine-learned potentials.", rendered)
            self.assertIn('<h2 class="talk-title">Unlinked Talk</h2>', rendered)
            self.assertEqual(rendered.count('class="talk-item"'), 2, "talks without a title are skipped")
            self.assertNotIn('<p class="list-empty">', rendered)
        finally:
            tf_path.unlink()

        with self.assertRaises(FileNotFoundError):
            load_talks(Path("/nonexistent/talks.yaml"))

    def test_inner_pages_share_flat_page_hero(self):
        for fname in ("people.html", "publications.html", "research.html", "code.html",
                      "news.html", "teaching.html", "collaborate.html", "talks.html",
                      "events.html", "junwen-yin.html"):
            content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('<section class="page-hero">', content, f"{fname} is missing the shared page hero")
            self.assertEqual(content.count('<h1 '), 1, f"{fname} should have exactly one h1")

    def test_news_display_latest_four_and_historical_toggle(self):
        index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
        main_js = (BASE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
        style_css = (BASE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")

        # News container and header toggle
        self.assertIn('id="news-section"', index_html)
        self.assertIn('id="news-header-toggle"', index_html)
        self.assertIn('class="news-box-title news-header-clickable"', index_html)
        self.assertIn('role="button"', index_html)
        self.assertIn('tabindex="0"', index_html)
        self.assertIn('aria-expanded="false"', index_html)
        self.assertIn('aria-controls="news-historical-wrap"', index_html)
        self.assertIn('data-total-count=', index_html)

        # Prominent toggle expand button and history page link to news.html
        self.assertIn('id="news-expand-btn"', index_html)
        self.assertIn('class="news-toggle-bar"', index_html)
        self.assertIn('href="news.html"', index_html)
        self.assertIn('id="news-history-link"', index_html)
        self.assertIn('id="news-expand-btn-text"', index_html)

        # Dedicated news.html historical page exists and renders all milestones
        news_html_path = BASE_DIR / "news.html"
        self.assertTrue(news_html_path.exists(), "news.html page must exist")
        news_html_content = news_html_path.read_text(encoding="utf-8")
        self.assertIn("News &amp; Historical Milestones", news_html_content)
        self.assertIn("Roadmap for an atomistic machine-learning ecosystem", news_html_content)
        self.assertIn("Establishment of the Data Driven Materials and Molecular Science group", news_html_content)

        # Primary list has exactly 4 items
        news_list_match = re.search(r'<ul class="news-list" id="news-list">(.*?)</ul>', index_html, re.DOTALL)
        self.assertIsNotNone(news_list_match, "Primary #news-list not found in index.html")
        latest_items = re.findall(r'<li class="news-item">', news_list_match.group(1))
        self.assertEqual(len(latest_items), 4, "Primary #news-list must display exactly the latest 4 items")

        # News items with links render anchor tags, while unlinked items render plain text
        self.assertIn('class="news-headline-link"', index_html)
        self.assertIn('target="_blank"', index_html)
        self.assertIn('rel="noopener noreferrer"', index_html)
        self.assertIn('https://arxiv.org/abs/2609.39090', index_html)
        self.assertIn('uMOF universal benchmark database', index_html)

        # Historical items hidden under #news-historical-wrap
        self.assertIn('id="news-historical-wrap"', index_html)
        self.assertIn('style="display: none;"', index_html)
        self.assertIn('id="news-historical-list"', index_html)
        hist_list_match = re.search(r'<ul class="news-list news-historical-list" id="news-historical-list"[^>]*>(.*?)</ul>', index_html, re.DOTALL)
        self.assertIsNotNone(hist_list_match, "#news-historical-list not found")
        hist_items = re.findall(r'<li class="news-item">', hist_list_match.group(1))
        self.assertGreaterEqual(len(hist_items), 1, "Historical list should contain remaining items")

        # JavaScript toggle logic handles both header and button
        self.assertIn("initNewsToggle", main_js)
        self.assertIn("news-header-toggle", main_js)
        self.assertIn("news-historical-wrap", main_js)

        # CSS styling: category uses distinct teal color, different from primary blue hyperlink
        self.assertIn(".news-date", style_css)
        self.assertIn("var(--accent-teal)", style_css)
        self.assertIn(".news-headline-link", style_css)
        self.assertIn("var(--primary)", style_css)
        self.assertIn(".news-header-clickable", style_css)
        self.assertIn(".news-toggle-indicator", style_css)
        self.assertIn(".news-toggle-bar", style_css)
        self.assertIn(".news-expand-btn", style_css)
        self.assertIn(".news-historical-divider", style_css)

    def test_core_team_individual_yamls_and_loader(self):
        from build_site import load_person, load_people

        people_dir = BASE_DIR / "data" / "people"
        expected_yamls = [
            "alin-marin-elena.yaml",
            "elliott-kasoar.yaml",
            "junwen-yin.yaml",
        ]
        for yfile in expected_yamls:
            p = people_dir / yfile
            self.assertTrue(p.exists(), f"Individual YAML file {yfile} missing in {people_dir}")
            data = load_person(p)
            self.assertIn("name", data)
            self.assertIn("slug", data)
            self.assertIn("page", data)
            self.assertIn("avatar", data)
            self.assertIn("role", data)
            self.assertIn("affiliation", data)
            self.assertIn("bio", data)
            self.assertIn("tags", data)
            self.assertIn("links", data)

        # Test load_people properly resolves core-team members from individual YAMLs
        people_data = load_people()
        core_sec = next(s for s in people_data["sections"] if s["id"] in ("core-team", "members"))
        self.assertGreaterEqual(len(core_sec["members"]), 3)
        yaml_members = [m for m in core_sec["members"] if m.get("yaml")]
        self.assertGreaterEqual(len(yaml_members), 3)
        for m in yaml_members:
            self.assertTrue(m["page"].endswith(".html"))
            if m.get("bio"):
                self.assertTrue(len(m["bio"]) > 20)

    def test_core_team_individual_pages_and_navigation(self):
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")

        # Clicking on the name of a core member links to their individual page
        self.assertIn('<a href="alin-marin-elena.html" class="person-name-link">Dr. Alin Marin Elena</a>', people_html)
        self.assertIn('<a href="elliott-kasoar.html" class="person-name-link">Elliott Kasoar</a>', people_html)
        self.assertIn('<a href="junwen-yin.html" class="person-name-link">Dr. Junwen Yin</a>', people_html)

        # Avatar is also clickable to their individual page
        self.assertIn('href="alin-marin-elena.html" class="person-avatar-link"', people_html)
        self.assertIn('href="elliott-kasoar.html" class="person-avatar-link"', people_html)
        self.assertIn('href="junwen-yin.html" class="person-avatar-link"', people_html)

        # Verify individual pages are generated and contain key sections
        core_pages = [
            ("alin-marin-elena.html", "Dr. Alin Marin Elena", "Alin Marin Elena"),
            ("elliott-kasoar.html", "Elliott Kasoar", "Elliott Kasoar"),
            ("junwen-yin.html", "Dr. Junwen Yin", "Junwen Yin"),
        ]
        for page_name, full_name, search_name in core_pages:
            page_path = BASE_DIR / page_name
            self.assertTrue(page_path.exists(), f"Profile page {page_name} was not generated")
            content = page_path.read_text(encoding="utf-8")

            # Title and header details
            self.assertIn(full_name, content)
            self.assertIn("profile-header-card", content)
            self.assertIn("profile-header-avatar", content)

            # Back link to team/people page
            self.assertIn('href="people.html"', content)
            self.assertIn("Back to People", content)

            # Biography and Research Interests
            self.assertIn("Biography", content)
            self.assertIn("Research Interests", content)

            # Publications section and link
            self.assertIn("Publications", content)
            self.assertIn("publications.html?author=", content)

            # Also verify file in people/ subdirectory exists
            sub_path = BASE_DIR / "people" / page_name
            self.assertTrue(sub_path.exists(), f"Subdirectory profile page people/{page_name} was not generated")

        # Career entries with a url link the institution name
        junwen_html = (BASE_DIR / "junwen-yin.html").read_text(encoding="utf-8")
        self.assertIn(
            '<a href="https://sites.unimi.it/etsf/" target="_blank" rel="noopener noreferrer">European Theoretical Spectroscopy Facility (ETSF)</a>',
            junwen_html,
        )

    def test_publication_authors_highlighting_only_authors_file(self):
        pubs_js = (BASE_DIR / "assets" / "js" / "publications.js").read_text(encoding="utf-8")
        self.assertIn("matchAuthorFromFile", pubs_js)
        # Ensure publications.json has full author list for multi-author papers
        with open(BASE_DIR / "publications.json", "r", encoding="utf-8") as f:
            pubs = json.load(f)
        multi_author_pubs = [p for p in pubs if len(p.get("authors", [])) > 2]
        self.assertGreater(len(multi_author_pubs), 30, "Most publications should have their full list of authors (>2 authors)")
        
        # Verify that co-authors like Elena Patyukova or Jian Yin are listed in publications.json authors
        all_authors = set()
        for p in pubs:
            for a in p.get("authors", []):
                all_authors.add(a)
        self.assertIn("Elena Patyukova", all_authors)
        self.assertIn("Jian Yin", all_authors)
        self.assertIn("Gábor Csányi", all_authors)

        # Verify that authors without valid ORCID from authors.yaml are loaded and tracked
        from build_site import load_data
        loaded_pubs, loaded_authors = load_data()
        self.assertIn("Federica Zanca", loaded_authors.values())
        self.assertIn("Elena Patyukova", loaded_authors.values())

        # Verify they are enriched into group_authors for their publications
        zanca_pubs = [p for p in loaded_pubs if "Federica Zanca" in p.get("group_authors", [])]
        self.assertGreaterEqual(len(zanca_pubs), 2)
        patyukova_pubs = [p for p in loaded_pubs if "Elena Patyukova" in p.get("group_authors", [])]
        self.assertGreaterEqual(len(patyukova_pubs), 1)

        # Verify publications.html authors-data JSON script contains them
        pubs_html = (BASE_DIR / "publications.html").read_text(encoding="utf-8")
        self.assertIn("Federica Zanca", pubs_html)
        self.assertIn("Elena Patyukova", pubs_html)

    def test_publications_default_2024_onwards(self):
        """Verify that the group publications list defaults to 2024 onwards."""
        pubs_html = (BASE_DIR / "publications.html").read_text(encoding="utf-8")
        self.assertIn('<option value="2024-onwards" selected>2024 onwards</option>', pubs_html)

        pubs_js = (BASE_DIR / "assets" / "js" / "publications.js").read_text(encoding="utf-8")
        self.assertIn("2024-onwards", pubs_js)
        self.assertIn("2024", pubs_js)
        self.assertIn("yearFilter.value = '2024-onwards'", pubs_js)

        from src.components.publications import generate_publications_html, build_html_page
        with open(BASE_DIR / "publications.json", "r", encoding="utf-8") as f:
            pubs = json.load(f)
        authors_dict = {"0000-0002-7013-6670": "Alin Marin Elena"}
        gen_html = generate_publications_html(pubs, authors_dict)
        self.assertIn('<option value="2024-onwards" selected>2024 onwards</option>', gen_html)

        page_html = build_html_page(pubs, authors_dict)
        self.assertIn('<option value="2024-onwards" selected>2024 onwards</option>', page_html)
        self.assertIn("2024-onwards", page_html)

    def test_highlighted_work_on_individual_pages(self):
        """Verify that individual person pages support Highlighted Work with software and bibtex keys."""
        alin_html = (BASE_DIR / "alin-marin-elena.html").read_text(encoding="utf-8")
        self.assertIn('id="highlighted-work"', alin_html)
        self.assertIn("Highlighted Work", alin_html)
        self.assertIn("highlighted-software-card", alin_html)
        self.assertIn("highlighted-paper-card", alin_html)
        self.assertIn("janus-core", alin_html)
        self.assertIn("pack-mm", alin_html)
        self.assertIn("@batatia20257006", alin_html)
        self.assertIn("Ilyes Batatia et al.", alin_html)
        # Highlighted section should truncate authors, not list all 88 authors
        highlighted_block = alin_html.split('id="highlighted-work"')[1].split('</section>')[0]
        self.assertNotIn("Gábor Csányi", highlighted_block)

        elliott_html = (BASE_DIR / "elliott-kasoar.html").read_text(encoding="utf-8")
        self.assertIn('id="highlighted-work"', elliott_html)
        self.assertIn("janus-core", elliott_html)
        self.assertIn("@batatia20269411", elliott_html)

        junwen_html = (BASE_DIR / "junwen-yin.html").read_text(encoding="utf-8")
        self.assertIn('id="highlighted-work"', junwen_html)
        self.assertIn("goldilocks", junwen_html)
        self.assertIn("@patyukova2026565e", junwen_html)

        # Verify that without highlighted_work, the section is cleanly omitted
        from src.components.people import (
            generate_person_html,
            render_highlighted_paper_card,
            render_highlighted_software_card,
            resolve_highlighted_items,
        )
        minimal_member = {"name": "Test Member", "slug": "test-member", "bio": "Test bio"}
        html_without_highlights = generate_person_html(minimal_member, [])
        self.assertNotIn("highlighted-work", html_without_highlights)

    def test_highlighted_work_pictures_and_author_formatting(self):
        """Verify picture rendering and 'First Author et al.' formatting for highlighted work."""
        from src.components.people import (
            generate_person_html,
            render_highlighted_paper_card,
            render_highlighted_software_card,
            resolve_highlighted_items,
        )

        # Test single author: no 'et al.'
        single_author_pub = {
            "title": "Single Author Study",
            "authors": ["Alice Smith"],
            "year": "2024",
            "doi": "10.1000/182",
        }
        card_single = render_highlighted_paper_card(single_author_pub)
        self.assertIn("Alice Smith", card_single)
        self.assertNotIn("et al.", card_single)

        # Test multiple authors: 'First Author et al.'
        multi_author_pub = {
            "title": "Multi Author Study",
            "authors": ["Alice Smith", "Bob Jones", "Charlie Brown"],
            "year": "2025",
            "doi": "10.1000/183",
        }
        card_multi = render_highlighted_paper_card(multi_author_pub)
        self.assertIn("Alice Smith et al.", card_multi)
        self.assertNotIn("Bob Jones", card_multi)
        self.assertNotIn("Charlie Brown", card_multi)

        # Test picture rendering on paper card
        card_with_pic = render_highlighted_paper_card(
            multi_author_pub,
            image="assets/images/highlights/sample_paper.png",
            rel_prefix="../",
        )
        self.assertIn('class="highlighted-card-media"', card_with_pic)
        self.assertIn('src="../assets/images/highlights/sample_paper.png"', card_with_pic)
        self.assertIn('class="highlighted-card-image"', card_with_pic)

        # Test picture rendering on software card
        sample_sw = {
            "id": "my-tool",
            "name": "My Tool",
            "description": "A great modeling package",
        }
        sw_card_with_pic = render_highlighted_software_card(
            sample_sw,
            rel_prefix="../",
            image="assets/images/highlights/my_tool.png",
        )
        self.assertIn('class="highlighted-card-media"', sw_card_with_pic)
        self.assertIn('src="../assets/images/highlights/my_tool.png"', sw_card_with_pic)
        self.assertIn('class="highlighted-card-image"', sw_card_with_pic)

        # Test resolve_highlighted_items with image/picture dictionaries
        sample_pubs = [
            {
                "title": "Paper One",
                "bibtex_key": "smith2024",
                "authors": ["Smith, A.", "Doe, J."],
                "year": "2024",
            }
        ]
        sample_software = [
            {"id": "tool-x", "name": "Tool X", "description": "Package X"}
        ]

        resolved = resolve_highlighted_items(
            [
                {"paper": "smith2024", "picture": "assets/images/paper_pic.jpg"},
                {"software": "tool-x", "image": "assets/images/tool_pic.png"},
                {"smith2024": {"picture": "assets/images/paper_pic2.jpg"}},
            ],
            publications=sample_pubs,
            software_packages=sample_software,
        )
        self.assertEqual(len(resolved), 3)
        self.assertEqual(resolved[0]["image"], "assets/images/paper_pic.jpg")
        self.assertEqual(resolved[1]["image"], "assets/images/tool_pic.png")
        self.assertEqual(resolved[2]["image"], "assets/images/paper_pic2.jpg")

        # Test full page generation with highlighted pictures
        member = {
            "name": "Sample Member",
            "slug": "sample-member",
            "highlighted_work": [
                {"id": "smith2024", "picture": "assets/images/paper_pic.jpg"},
                {"software": "tool-x", "image": "assets/images/tool_pic.png"},
            ],
        }
        member_html = generate_person_html(member, sample_pubs, software=sample_software)
        self.assertIn("highlighted-card-image", member_html)
        self.assertIn('src="assets/images/paper_pic.jpg"', member_html)
        self.assertIn('src="assets/images/tool_pic.png"', member_html)
        self.assertIn("Smith, A. et al.", member_html)

    def test_member_dates_and_publication_filtering(self):
        """Verify join_date and left_date are present in YAML and can filter publications."""
        with open(BASE_DIR / "data" / "people.yaml", "r", encoding="utf-8") as f:
            people_data = yaml.safe_load(f)

        # Check members have join_date
        members_sec = next(s for s in people_data["sections"] if s["id"] == "members")
        for m in members_sec["members"]:
            self.assertIn("join_date", m, f"Member {m['name']} missing join_date in people.yaml")

        # Check former members have join_date and left_date
        former_sec = next(s for s in people_data["sections"] if s["id"] == "former-members")
        for fm in former_sec["members"]:
            self.assertIn("join_date", fm, f"Former member {fm['name']} missing join_date")
            self.assertIn("left_date", fm, f"Former member {fm['name']} missing left_date")

        # Verify filter_publications_by_dates logic
        from src.components.people import filter_publications_by_dates
        test_pubs = [
            {"title": "Paper 2021", "year": "2021"},
            {"title": "Paper 2023", "year": "2023"},
            {"title": "Paper 2024", "year": "2024"},
            {"title": "Paper 2026", "year": "2026"},
        ]
        # Filter for former member (2022 to 2024)
        filtered = filter_publications_by_dates(test_pubs, join_date="2022-09-01", left_date="2024-08-31")
        self.assertEqual([p["year"] for p in filtered], ["2023", "2024"])

        # Filter for current member (from 2024 onwards)
        filtered_current = filter_publications_by_dates(test_pubs, join_date="2024-01-01")
        self.assertEqual([p["year"] for p in filtered_current], ["2024", "2026"])

        # Verify tenure is shown on people.html for former members
        people_html = (BASE_DIR / "people.html").read_text(encoding="utf-8")
        self.assertIn("2024&ndash;2026", people_html)
        self.assertIn("2023&ndash;2024", people_html)

    def test_header_hero_pictures_and_blending(self):
        """Verify generic header pictures are present for each page and blended in CSS."""
        hero_dir = BASE_DIR / "assets" / "images" / "heroes"
        self.assertTrue(hero_dir.is_dir(), "assets/images/heroes directory missing")

        expected_banners = [
            "code_banner.jpg",
            "collaborate_banner.jpg",
            "news_banner.jpg",
            "people_banner.jpg",
            "publications_banner.jpg",
            "research_banner.jpg",
            "teaching_talks_banner.jpg",
        ]
        for b in expected_banners:
            self.assertTrue((hero_dir / b).is_file(), f"Missing hero banner {b}")

        # Verify pages render the blended hero background
        pages_to_check = [
            ("people.html", "people_banner.jpg"),
            ("research.html", "research_banner.jpg"),
            ("code.html", "code_banner.jpg"),
            ("publications.html", "publications_banner.jpg"),
            ("news.html", "news_banner.jpg"),
            ("talks.html", "teaching_talks_banner.jpg"),
            ("teaching.html", "teaching_talks_banner.jpg"),
            ("events.html", "teaching_talks_banner.jpg"),
            ("collaborate.html", "collaborate_banner.jpg"),
            ("alin-marin-elena.html", "people_banner.jpg"),
        ]
        for fname, expected_img in pages_to_check:
            html_content = (BASE_DIR / fname).read_text(encoding="utf-8")
            self.assertIn('class="page-hero-bg"', html_content, f"{fname} missing page-hero-bg")
            self.assertIn('class="page-hero-bg-img"', html_content, f"{fname} missing page-hero-bg-img")
            self.assertIn(expected_img, html_content, f"{fname} does not contain {expected_img}")

        # Check people/ subpage handles relative prefix
        sub_html = (BASE_DIR / "people" / "alin-marin-elena.html").read_text(encoding="utf-8")
        self.assertIn('src="../assets/images/heroes/people_banner.jpg"', sub_html)

        # Check CSS contains horizontal gradient blend
        style_css = (BASE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
        self.assertIn(".page-hero-bg", style_css)
        self.assertIn(".page-hero-bg::after", style_css)
        self.assertIn("90deg", style_css)

    def test_header_nav_pills_different_colours(self):
        """Verify navigation pills are present at the top of the header on two lines with different colors."""
        header_html = (BASE_DIR / "header.html").read_text(encoding="utf-8")
        self.assertIn('header-nav-pills', header_html)
        self.assertIn('header-nav-level1', header_html)
        self.assertIn('header-subline-wrap', header_html)
        self.assertIn('header-nav-subline', header_html)
        self.assertIn('class="nav-pill', header_html)
        self.assertIn('class="nav-pill-dot"', header_html)

        # Check pills exist for core pages (top line and second line sub-pills like research)
        for expected in ("Home", "People", "Research", "Publications", "Software", "Areas", "Talks", "Training", "Events"):
            self.assertIn(f"<span>{expected}</span>", header_html)

        # Footer menu is removed since the header menu is always sticky on
        footer_html = (BASE_DIR / "footer.html").read_text(encoding="utf-8")
        self.assertNotIn('footer-nav-pills', footer_html)

        # People and Software should not have submenus
        self.assertNotIn('data-nav-group="people"', header_html)
        self.assertNotIn('data-nav-group="software"', header_html)

        # Check pills have different colours via --pill-color style attributes
        import re
        colors = re.findall(r'--pill-color:\s*(#[0-9a-fA-F]{3,6})', header_html)
        self.assertGreaterEqual(len(colors), 5, "Expected at least 5 colored pills")
        # Ensure all pill colors are unique
        self.assertEqual(len(colors), len(set(colors)), "Each menu pill should have a distinct color")

        # Check CSS styles exist
        style_css = (BASE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
        self.assertIn(".header-nav-pills", style_css)
        self.assertIn(".header-subline-wrap", style_css)
        self.assertIn(".header-subline-group", style_css)
        self.assertIn(".nav-pill", style_css)
        self.assertIn(".nav-pill.active", style_css)

    def test_events_page(self):
        from components.events import load_events, generate_events_html
        events_html = (BASE_DIR / "events.html").read_text(encoding="utf-8")
        self.assertIn("Events", events_html)
        self.assertNotIn("CaMML Spring School 2027", events_html)
        self.assertNotIn('id="upcoming"', events_html)
        self.assertIn('id="workshops"', events_html)
        self.assertIn("The Atomic Simulation Environment: Integration into Wider Community Projects", events_html)
        self.assertIn("cecam_ase_mainz_2026.jpeg", events_html)
        self.assertIn("46th CCP5 Annual General Meeting and Conference", events_html)
        self.assertIn("https://agm46.ccp5.ac.uk/", events_html)
        self.assertIn("45th CCP5 Annual General Meeting and Conference", events_html)
        self.assertIn("https://agm45.ccp5.ac.uk/", events_html)
        self.assertIn("44th CCP5 Annual General Meeting and Conference", events_html)
        self.assertIn("https://agm44.ccp5.ac.uk/", events_html)
        self.assertIn("Quantum Computing in Materials and Molecular Sciences", events_html)
        self.assertIn("https://royalsociety.org/science-events-and-lectures/2025/10/quantum-computing/", events_html)
        self.assertIn("The Atomic Simulation Environment Ecosystem: Present and Perspectives", events_html)
        self.assertIn("https://ase-lib.org/events/2025-06-Lausanne-workshop/", events_html)
        self.assertIn("ase_lausanne_2025.jpg", events_html)
        self.assertIn("Electronic Structure Software Development: Advancing the Modular Paradigm", events_html)
        self.assertIn("https://www.cecam.org/workshop-details/electronic-structure-software-development-advancing-the-modular-paradigm-1194", events_html)
        self.assertIn("ESL Workshop 11: Connecting Library Developers and Technologies", events_html)
        self.assertIn("https://esl.cecam.org/en/events/esl11/", events_html)
        data = load_events()
        self.assertIn("categories", data)
        rendered = generate_events_html({"title": "Group Events", "categories": []})
        self.assertIn("Group Events", rendered)
        with self.assertRaises(FileNotFoundError):
            load_events(Path("/nonexistent/events.yaml"))


if __name__ == "__main__":
    unittest.main()

