"""Opportunities page component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml

try:
    from .header import get_header
    from .footer import get_footer
    from .layout import render_page_hero
    from .sections import render_category_sections
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
        from components.layout import render_page_hero
        from components.sections import render_category_sections
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer
        from src.components.layout import render_page_hero
        from src.components.sections import render_category_sections

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OPPORTUNITIES_FILE = BASE_DIR / "data" / "opportunities.yaml"


def load_opportunities(opportunities_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Opportunities page content from a YAML file (default: data/opportunities.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if opportunities_file is None:
        target_path = OPPORTUNITIES_FILE
    else:
        target_path = Path(opportunities_file)
        if not target_path.is_file():
            target_path = BASE_DIR / opportunities_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Opportunities YAML file not found: '{opportunities_file or OPPORTUNITIES_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_opportunities_html(opportunities: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Opportunities page HTML."""
    header_html = get_header("opportunities")
    footer_html = get_footer()

    if opportunities is None:
        opportunities = load_opportunities()

    hero_html = render_page_hero(
        str(opportunities.get("title") or "Opportunities"),
        str(opportunities.get("intro") or "").strip(),
    )

    subnav_html, categories_html = render_category_sections(
        opportunities.get("categories") or [], "Opportunities page quick navigation"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Opportunities | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Upcoming events, PhD projects, the STFC Graduate Scheme and STFC placements with the Data Driven Materials and Molecular Science group.">
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
{subnav_html}{categories_html}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
