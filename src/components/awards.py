"""Awards page component and data loader for the DDMMS website."""

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
AWARDS_FILE = BASE_DIR / "data" / "awards.yaml"


def load_awards(awards_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Awards page content from a YAML file (default: data/awards.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if awards_file is None:
        target_path = AWARDS_FILE
    else:
        target_path = Path(awards_file)
        if not target_path.is_file():
            target_path = BASE_DIR / awards_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Awards YAML file not found: '{awards_file or AWARDS_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_awards_html(awards: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Awards page HTML."""
    header_html = get_header("awards")
    footer_html = get_footer()

    if awards is None:
        awards = load_awards()

    hero_html = render_page_hero(
        str(awards.get("title") or "Awards"),
        str(awards.get("intro") or "").strip(),
    )

    rows = []
    for award in awards.get("awards") or []:
        if not isinstance(award, dict) or not award.get("title"):
            continue
        title = str(award.get("title")).strip()
        url = str(award.get("url") or "").strip()
        if url:
            title_html = f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{title}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
        else:
            title_html = title
        meta = " &middot; ".join(str(award.get(k)).strip() for k in ("recipient", "awarded_by") if award.get(k))
        meta_html = f'\n            <p class="award-meta">{meta}</p>' if meta else ""
        desc = str(award.get("description") or "").strip()
        desc_html = f'\n            <p class="award-desc">{desc}</p>' if desc else ""
        rows.append(f"""        <li class="award-item">
          <span class="award-year">{award.get("year", "")}</span>
          <div class="award-body">
            <h2 class="award-title">{title_html}</h2>{meta_html}{desc_html}
          </div>
        </li>""")

    if rows:
        rows_html = "\n".join(rows)
        list_html = f"""        <ul class="awards-list">
{rows_html}
        </ul>"""
    else:
        list_html = '        <p class="list-empty">Awards will be listed here soon.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awards | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Awards, prizes and fellowships received by members of the Data Driven Materials and Molecular Science group at STFC.">
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
