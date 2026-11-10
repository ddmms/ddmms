"""Teaching page component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml

from .layout import render_page, render_page_hero
from .sections import render_category_sections

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

    if teaching is None:
        teaching = load_teaching()

    hero_html = render_page_hero(
        str(teaching.get("title") or "Training"),
        str(teaching.get("intro") or "").strip(),
    )

    subnav_html, categories_html = render_category_sections(
        teaching.get("categories") or [], "Training page quick navigation"
    )

    return render_page(
        title="Training",
        description="Schools and training programmes run by the Data Driven Materials and Molecular Science group.",
        active_page="teaching",
        main_html=f"""{hero_html}

    <section class="home-section">
      <div class="container">
{subnav_html}{categories_html}
      </div>
    </section>""",
    )
