"""Teaching page component and data loader for the DDMMS website."""

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
TRAINING_FILE = BASE_DIR / "data" / "training.yaml"
TEACHING_FILE = TRAINING_FILE


def load_training(training_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Training page content from a YAML file (default: data/training.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if training_file is None:
        target_path = TRAINING_FILE
        if not target_path.is_file():
            fallback_legacy = BASE_DIR / "data" / "teaching.yaml"
            if fallback_legacy.is_file():
                target_path = fallback_legacy
    else:
        target_path = Path(training_file)
        if not target_path.is_file():
            target_path = BASE_DIR / training_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Training YAML file not found: '{training_file or TRAINING_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


load_teaching = load_training


def generate_teaching_html(teaching: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Teaching page HTML."""
    header_html = get_header("teaching")
    footer_html = get_footer()

    if teaching is None:
        teaching = load_teaching()

    hero_html = render_page_hero(
        str(teaching.get("title") or "Teaching &amp; Training"),
        str(teaching.get("intro") or "").strip(),
    )

    subnav_html, categories_html = render_category_sections(
        teaching.get("categories") or [], "Teaching page quick navigation"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Teaching | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Schools and workshops run by the Data Driven Materials and Molecular Science group.">
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
