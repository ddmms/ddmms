"""Shared layout pieces for the DDMMS website pages."""

from typing import Dict, Optional

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
    "news": "assets/images/heroes/news_banner.jpg",
    "milestone": "assets/images/heroes/news_banner.jpg",
    "teach": "assets/images/heroes/teaching_talks_banner.jpg",
    "course": "assets/images/heroes/teaching_talks_banner.jpg",
    "talk": "assets/images/heroes/teaching_talks_banner.jpg",
    "seminar": "assets/images/heroes/teaching_talks_banner.jpg",
    "presentation": "assets/images/heroes/teaching_talks_banner.jpg",
    "collaborat": "assets/images/heroes/collaborate_banner.jpg",
    "partner": "assets/images/heroes/collaborate_banner.jpg",
    "opportunit": "assets/images/heroes/collaborate_banner.jpg",
    "career": "assets/images/heroes/collaborate_banner.jpg",
    "join": "assets/images/heroes/collaborate_banner.jpg",
}


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
    rel_prefix: str = "",
) -> str:
    """Render the dark full-width title band shown at the top of every inner page,
    with a generic scientific picture nicely blended from left to right.
    """
    intro_html = f'\n        <p class="page-hero-intro">{intro}</p>' if intro else ""
    extra = f"\n{extra_html}" if extra_html else ""

    chosen_bg = bg_image if bg_image is not None else get_hero_bg_for_title(title)
    if chosen_bg:
        img_src = f"{rel_prefix}{chosen_bg}" if (rel_prefix and chosen_bg.startswith("assets/")) else chosen_bg
        bg_html = f"""      <div class="page-hero-bg" aria-hidden="true">
        <img src="{img_src}" alt="" class="page-hero-bg-img" loading="eager">
      </div>\n"""
    else:
        bg_html = ""

    return f"""    <section class="page-hero">
{bg_html}      <div class="container page-hero-container">
        <h1 class="page-hero-title">{title}</h1>{intro_html}{extra}
      </div>
    </section>"""
