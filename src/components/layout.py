"""Shared layout pieces for the DDMMS website pages."""

from typing import Dict, Optional

from .header import get_header
from .footer import get_footer

SITE_NAME = "Data Driven Materials and Molecular Science"

# Mapping of page title keywords to generic hero banner pictures
PAGE_HERO_IMAGES: Dict[str, str] = {
    "people": "assets/images/heroes/people_banner.jpg",
    "team": "assets/images/heroes/people_banner.jpg",
    "member": "assets/images/heroes/people_banner.jpg",
    "person": "assets/images/heroes/people_banner.jpg",
    "community": "assets/images/heroes/people_banner.jpg",
    "research": "assets/images/heroes/research_banner.jpg",
    "theme": "assets/images/heroes/research_banner.jpg",
    "publication": "assets/images/heroes/publications_banner.jpg",
    "preprint": "assets/images/heroes/publications_banner.jpg",
    "software": "assets/images/heroes/code_banner.jpg",
    "tool": "assets/images/heroes/code_banner.jpg",
    "code": "assets/images/heroes/code_banner.jpg",
    "skill": "assets/images/heroes/code_banner.jpg",
    "news": "assets/images/heroes/news_banner.jpg",
    "milestone": "assets/images/heroes/news_banner.jpg",
    "teach": "assets/images/heroes/teaching_talks_banner.jpg",
    "train": "assets/images/heroes/teaching_talks_banner.jpg",
    "course": "assets/images/heroes/teaching_talks_banner.jpg",
    "talk": "assets/images/heroes/teaching_talks_banner.jpg",
    "seminar": "assets/images/heroes/teaching_talks_banner.jpg",
    "presentation": "assets/images/heroes/teaching_talks_banner.jpg",
    "event": "assets/images/heroes/teaching_talks_banner.jpg",
    "workshop": "assets/images/heroes/teaching_talks_banner.jpg",
    "collaborat": "assets/images/heroes/collaborate_banner.jpg",
    "partner": "assets/images/heroes/collaborate_banner.jpg",
    "opportunit": "assets/images/heroes/collaborate_banner.jpg",
    "career": "assets/images/heroes/collaborate_banner.jpg",
    "join": "assets/images/heroes/collaborate_banner.jpg",
}


def render_page(
    title: str,
    description: str,
    main_html: str,
    active_page: str = "home",
    head_extra: str = "",
    body_end: str = "",
    extra_scripts: str = "",
) -> str:
    """Render a complete site page around ``main_html``.

    This is the single source of the document shell: ``<head>`` metadata, the
    inlined site header and footer, and the common script tags. Page components
    supply only the inner HTML of ``<main>``.

    Args:
        title: Page-specific part of the ``<title>``; the site name is appended.
        description: Content of the ``<meta name="description">`` tag.
        main_html: Inner HTML of ``<main id="main-content">``.
        active_page: Section name passed through to the header and emitted as
            ``<body data-active-page>`` for the nav highlighting in main.js.
        head_extra: Extra markup appended inside ``<head>``.
        body_end: Markup inserted after the footer, before the common scripts.
        extra_scripts: Script tags appended after ``assets/js/main.js``.
    """
    head_extra = f"{head_extra}\n" if head_extra and not head_extra.endswith("\n") else head_extra
    body_end = f"{body_end}\n" if body_end and not body_end.endswith("\n") else body_end
    extra_scripts = (
        f"\n{extra_scripts}" if extra_scripts and not extra_scripts.startswith("\n") else extra_scripts
    )

    header_html = get_header(active_page).rstrip("\n")
    footer_html = get_footer().rstrip("\n")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
{head_extra}</head>
<body data-active-page="{active_page}">
{header_html}

  <main id="main-content">
{main_html}
  </main>

{footer_html}
{body_end}  <script src="assets/js/main.js"></script>{extra_scripts}
</body>
</html>
"""


def get_hero_bg_for_title(title: str) -> str:
    """Determine the most appropriate generic hero banner picture for a page title."""
    lower = title.lower()
    for kw, img in PAGE_HERO_IMAGES.items():
        if kw in lower:
            return img
    return "assets/images/heroes/research_banner.jpg"


def render_page_hero(
    title: str,
    intro: str = "",
    extra_html: str = "",
    bg_image: Optional[str] = None,
) -> str:
    """Render the dark full-width title band shown at the top of every inner page,
    with a generic scientific picture nicely blended from left to right.
    """
    intro_html = f'\n        <p class="page-hero-intro">{intro}</p>' if intro else ""
    extra = f"\n{extra_html}" if extra_html else ""

    chosen_bg = bg_image if bg_image is not None else get_hero_bg_for_title(title)
    if chosen_bg:
        bg_html = f"""      <div class="page-hero-bg" aria-hidden="true">
        <img src="{chosen_bg}" alt="" class="page-hero-bg-img" loading="eager">
      </div>\n"""
    else:
        bg_html = ""

    return f"""    <section class="page-hero">
{bg_html}      <div class="container page-hero-container">
        <h1 class="page-hero-title">{title}</h1>{intro_html}{extra}
      </div>
    </section>"""
