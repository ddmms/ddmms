"""Header component for the DDMMS website."""

from pathlib import Path
from typing import Optional, Union

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
HEADER_TEMPLATE_FILE = TEMPLATE_DIR / "header.html"


def generate_header_html(
    template_file: Optional[Union[str, Path]] = None,
) -> str:
    """Generate the reusable, modular header component by reading from a template file.

    Requires a template file either at the default location (src/templates/header.html)
    or provided via the template_file argument.
    """
    target_path: Optional[Path] = None
    if template_file is not None:
        cand = Path(template_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / template_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"Header template file not found: '{template_file}'")
    else:
        for cand in (
            HEADER_TEMPLATE_FILE,
            BASE_DIR / "templates" / "header.html",
        ):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(
                f"Header template file not found at default location '{HEADER_TEMPLATE_FILE}'"
            )

    content = target_path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
    return content


def get_header(active_page="home", full_markup=False):
    """Return the reusable site header container or full markup.

    Individual HTML pages reuse the separate header.html file directly,
    eliminating duplicate header markup across pages.
    """
    if full_markup:
        return generate_header_html()
    return '  <div id="site-header" data-include-header></div>'
