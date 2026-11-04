"""Header component for the DDMMS website."""

from functools import lru_cache
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


@lru_cache(maxsize=1)
def _default_header_html() -> str:
    """Read and cache the default header template, which is identical for every page."""
    return generate_header_html()


def get_header(active_page="home"):
    """Return the full site header markup, for inlining into a generated page.

    The header is baked into each page at build time rather than fetched by the
    browser, so navigation works without JavaScript and needs no extra request.
    ``active_page`` is accepted for call-site readability; the active section is
    highlighted at runtime by ``initHeader`` in assets/js/main.js, which derives
    it from the current URL.
    """
    return _default_header_html()
