"""Events page component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml

from .layout import render_page, render_page_hero
from .sections import render_category_sections

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVENTS_FILE = BASE_DIR / "data" / "events.yaml"


def load_events(events_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Events page content from a YAML file (default: data/events.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if events_file is None:
        target_path = EVENTS_FILE
    else:
        target_path = Path(events_file)
        if not target_path.is_file():
            target_path = BASE_DIR / events_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Events YAML file not found: '{events_file or EVENTS_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_events_html(events: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Events page HTML."""

    if events is None:
        events = load_events()

    hero_html = render_page_hero(
        str(events.get("title") or "Events"),
        str(events.get("intro") or "").strip(),
    )

    subnav_html, categories_html = render_category_sections(
        events.get("categories") or [], "Events page quick navigation"
    )

    return render_page(
        title="Events",
        description="Conferences, workshops, summer schools and seminars organised or hosted by the Data Driven Materials and Molecular Science group.",
        active_page="events",
        main_html=f"""{hero_html}

    <section class="home-section">
      <div class="container">
{subnav_html}{categories_html}
      </div>
    </section>""",
    )

