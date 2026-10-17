"""Collaborate page component and data loader for the DDMMS website."""

import html
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml

try:
    from .header import get_header
    from .footer import get_footer
    from .layout import render_page_hero
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
        from components.layout import render_page_hero
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer
        from src.components.layout import render_page_hero

BASE_DIR = Path(__file__).resolve().parent.parent.parent
COLLABORATE_FILE = BASE_DIR / "data" / "collaborate.yaml"


def load_collaborate(collaborate_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Collaborate page content from a YAML file (default: data/collaborate.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if collaborate_file is None:
        target_path = COLLABORATE_FILE
    else:
        target_path = Path(collaborate_file)
        if not target_path.is_file():
            target_path = BASE_DIR / collaborate_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Collaborate YAML file not found: '{collaborate_file or COLLABORATE_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_collaborate_html(collaborate: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Collaborate page HTML."""
    header_html = get_header("collaborate")
    footer_html = get_footer()

    if collaborate is None:
        collaborate = load_collaborate()

    title = str(collaborate.get("title") or "Collaborate With Us").strip()
    intro = str(collaborate.get("intro") or "").strip()

    contact = collaborate.get("contact") or {}
    email = str(contact.get("email") or "").strip()
    button_text = str(contact.get("button_text") or "Email the group").strip()
    mailto = f"mailto:{html.escape(email, quote=True)}" if email else ""

    hero_html = render_page_hero(title, intro)

    sections_html = []
    for sec in collaborate.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        items = [str(i).strip() for i in (sec.get("items") or []) if str(i).strip()]
        items_html = "\n".join(
            f"""          <li class="feature-item">
            <span class="feature-index">{n:02d}</span>
            <span class="feature-label">{item}</span>
          </li>"""
            for n, item in enumerate(items, start=1)
        )
        sections_html.append(f"""    <section class="home-section">
      <div class="container">
        <h2 class="home-heading">{sec.get("title", "")}</h2>
        <ul class="feature-list">
{items_html}
        </ul>
      </div>
    </section>""")

    collaborators = collaborate.get("collaborators")
    if isinstance(collaborators, dict):
        intro_html = f'\n        <p class="home-lead">{collaborators["intro"]}</p>' if collaborators.get("intro") else ""
        network_links = "\n".join(
            f'          <a href="{html.escape(str(link.get("url")), quote=True)}" target="_blank" rel="noopener noreferrer" class="person-link-btn">{link.get("text", "")}</a>'
            for link in (collaborators.get("networks") or [])
            if isinstance(link, dict) and link.get("url")
        )
        networks_html = ""
        if network_links:
            networks_intro = collaborators.get("networks_intro")
            networks_intro_html = f'\n        <p class="network-desc">{networks_intro}</p>' if networks_intro else ""
            networks_html = f"""
        <h3 class="network-title">{collaborators.get("networks_title", "Research Networks")}</h3>{networks_intro_html}
        <div class="link-buttons">
{network_links}
        </div>"""
        sections_html.append(f"""    <section class="home-section" id="collaborators">
      <div class="container">
        <h2 class="home-heading">{collaborators.get("title", "Collaborators")}</h2>{intro_html}{networks_html}
      </div>
    </section>""")

    contact_html = ""
    if contact:
        contact_btn = f"""
        <a href="{mailto}" class="btn btn-primary contact-btn">&#9993; {button_text}</a>
        <p class="contact-email">{html.escape(email)}</p>""" if mailto else ""
        contact_html = f"""
    <section class="home-section home-section-alt" id="contact">
      <div class="container home-narrow">
        <h2 class="home-heading">{contact.get("title", "Get in touch")}</h2>
        <p class="home-lead">{contact.get("description", "")}</p>{contact_btn}
      </div>
    </section>"""

    all_sections_html = "\n\n".join(sections_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Collaborate | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Research collaborations, partner networks and how to get in touch with the Data Driven Materials and Molecular Science group at STFC.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content">
{hero_html}

{all_sections_html}
{contact_html}
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
