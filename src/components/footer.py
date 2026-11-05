"""Footer component for the DDMMS website."""

from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
FOOTER_TEMPLATE_FILE = TEMPLATE_DIR / "footer.html"


def generate_footer_html(
    template_file: Optional[Union[str, Path]] = None,
    year: Optional[Union[str, int]] = None,
) -> str:
    """Generate the reusable, modular footer component by reading from a template file.

    Requires a template file either at the default location (src/templates/footer.html)
    or provided via the template_file argument.
    """
    if year is None:
        year = datetime.now().year

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
                raise FileNotFoundError(f"Footer template file not found: '{template_file}'")
    else:
        for cand in (
            FOOTER_TEMPLATE_FILE,
            BASE_DIR / "templates" / "footer.html",
        ):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(
                f"Footer template file not found at default location '{FOOTER_TEMPLATE_FILE}'"
            )

    content = target_path.read_text(encoding="utf-8")

    # Render template variables
    rendered = (
        content.replace("{{ year }}", str(year))
        .replace("{{year}}", str(year))
        .replace("{year}", str(year))
    )
    if not rendered.endswith("\n"):
        rendered += "\n"
    return rendered


@lru_cache(maxsize=1)
def _default_footer_html() -> str:
    """Read and cache the default footer template, which is identical for every page."""
    return generate_footer_html()


def get_footer():
    """Return the full site footer markup, for inlining into a generated page.

    The footer is baked into each page at build time rather than fetched by the
    browser, so it renders without JavaScript and needs no extra request.
    """
    return _default_footer_html()
