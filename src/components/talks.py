"""Talks page component and data loader for the DDMMS website."""

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
TALKS_FILE = BASE_DIR / "data" / "talks.yaml"


def load_talks(talks_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Talks page content from a YAML file (default: data/talks.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if talks_file is None:
        target_path = TALKS_FILE
    else:
        target_path = Path(talks_file)
        if not target_path.is_file():
            target_path = BASE_DIR / talks_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Talks YAML file not found: '{talks_file or TALKS_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_talks_html(talks: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Talks page HTML."""
    header_html = get_header("talks")
    footer_html = get_footer()

    if talks is None:
        talks = load_talks()

    hero_html = render_page_hero(
        str(talks.get("title") or "Talks"),
        str(talks.get("intro") or "").strip(),
        str(talks.get("eyebrow") or "").strip(),
    )

    rows = []
    for talk in talks.get("talks") or []:
        if not isinstance(talk, dict) or not talk.get("title"):
            continue
        title = str(talk.get("title")).strip()
        url = str(talk.get("url") or "").strip()
        if url:
            title_html = f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{title}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
        else:
            title_html = title
        talk_type = str(talk.get("type") or "").strip()
        type_html = f'\n            <span class="talk-type">{talk_type}</span>' if talk_type else ""
        meta = " &middot; ".join(str(talk.get(k)).strip() for k in ("speaker", "event") if talk.get(k))
        meta_html = f'\n            <p class="talk-meta">{meta}</p>' if meta else ""
        desc = str(talk.get("description") or "").strip()
        desc_html = f'\n            <p class="talk-desc">{desc}</p>' if desc else ""
        rows.append(f"""        <li class="talk-item">
          <span class="talk-year">{talk.get("year", "")}</span>
          <div class="talk-body">
            <h2 class="talk-title">{title_html}</h2>{type_html}{meta_html}{desc_html}
          </div>
        </li>""")

    if rows:
        rows_html = "\n".join(rows)
        list_html = f"""        <ul class="talks-list">
{rows_html}
        </ul>"""
    else:
        list_html = '        <p class="list-empty">Talks will be listed here soon.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Talks | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Invited and contributed talks given by members of the Data Driven Materials and Molecular Science group at STFC.">
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

    <section class="home-section">
      <div class="container">
{list_html}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
