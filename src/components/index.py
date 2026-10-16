"""Index / About page component and data loader for the DDMMS website."""

import html
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

try:
    from .header import get_header
    from .footer import get_footer
    from .news import load_news
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
        from components.news import load_news
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer
        from src.components.news import load_news

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MISSION_FILE = BASE_DIR / "data" / "mission.yaml"


def load_mission(mission_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load group mission and index metadata from a YAML file (default: data/mission.yaml).

    Requires a valid YAML file provided by the user. Raises FileNotFoundError
    if the file cannot be located.
    """
    target_path: Optional[Path] = None
    if mission_file is not None:
        cand = Path(mission_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / mission_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"Mission YAML file not found: '{mission_file}'")
    else:
        for cand in (
            MISSION_FILE,
            BASE_DIR / "data" / "mission.yml",
            BASE_DIR / "data" / "index.yaml",
            BASE_DIR / "data" / "index.yml",
        ):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(f"Mission YAML file not found at default location '{MISSION_FILE}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    if not parsed:
        return {"title": "The Group Mission", "subtitle": "", "paragraphs": []}

    if isinstance(parsed, list):
        return {"title": "The Group Mission", "subtitle": "", "paragraphs": parsed}

    if isinstance(parsed, dict):
        title = str(parsed.get("title") or "The Group Mission").strip()
        subtitle = str(parsed.get("subtitle") or "").strip()
        raw_paragraphs = (
            parsed.get("paragraphs")
            or parsed.get("mission")
            or parsed.get("content")
            or parsed.get("description")
            or []
        )
        if isinstance(raw_paragraphs, str):
            paragraphs = [p.strip() for p in raw_paragraphs.split("\n\n") if p.strip()]
        elif isinstance(raw_paragraphs, list):
            paragraphs = [str(p).strip() for p in raw_paragraphs if str(p).strip()]
        else:
            paragraphs = []

        affiliations = parsed.get("affiliations") or {}
        return {
            "title": title,
            "subtitle": subtitle,
            "paragraphs": paragraphs,
            "affiliations": affiliations,
        }

    return {"title": "The Group Mission", "subtitle": "", "paragraphs": []}


load_index = load_mission


def render_affiliations_carousel_html(affiliations: Optional[Dict[str, Any]]) -> str:
    """Render the full-width, swipeable homepage carousel (department + work sites)."""
    if not isinstance(affiliations, dict):
        return ""
    slides = [c for c in (affiliations.get("slides") or []) if isinstance(c, dict)]
    if not slides:
        return ""

    title = html.escape(str(affiliations.get("title") or "Our Home at STFC").strip(), quote=True)
    total = len(slides)

    rendered_slides = []
    dots = []
    for idx, slide in enumerate(slides, start=1):
        slide_id = f"affiliation-slide-{idx}"
        slide_title = str(slide.get("title", ""))
        label = html.escape(f"{idx} of {total}: {slide_title}", quote=True)
        hierarchy = [h for h in (slide.get("hierarchy") or []) if isinstance(h, dict)]
        image = str(slide.get("image") or "").strip()

        links_html = "\n".join(
            f'                  <a href="{html.escape(str(link.get("url", "")), quote=True)}" class="slide-link" target="_blank" rel="noopener noreferrer">{link.get("text", "")}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
            for link in (slide.get("links") or [])
            if isinstance(link, dict) and link.get("url")
        )
        content_html = f"""              <div class="slide-content">
                <span class="slide-eyebrow">{slide.get("eyebrow", "")}</span>
                <h2 class="slide-title">{slide_title}</h2>
                <p class="slide-desc">{slide.get("description", "")}</p>
                <div class="slide-links">
{links_html}
                </div>
              </div>"""

        if hierarchy:
            steps = []
            for i, level in enumerate(hierarchy):
                current_cls = " is-current" if i == len(hierarchy) - 1 else ""
                name = level.get("name", "")
                url = str(level.get("url") or "").strip()
                if url:
                    # The link stretches over the whole row (see .org-chain-link::after)
                    name_html = (
                        f'<a href="{html.escape(url, quote=True)}" class="org-chain-name org-chain-link" target="_blank" rel="noopener noreferrer">{name}</a>\n'
                        f'                    <span class="org-chain-ext" aria-hidden="true">&#8599;</span>'
                    )
                else:
                    name_html = f'<span class="org-chain-name">{name}</span>'
                badge = str(level.get("badge") or "").strip()
                badge_html = f'\n                    <span class="org-chain-badge">{badge}</span>' if badge else ""
                steps.append(f"""                  <li class="org-chain-step{current_cls}">
                    <span class="org-chain-short">{level.get("short", "")}</span>
                    {name_html}{badge_html}
                  </li>""")
            steps_html = "\n".join(steps)
            chain_label = html.escape(" > ".join(str(h.get("short", "")) for h in hierarchy), quote=True)
            slide_cls = "carousel-slide carousel-slide-org"
            body_html = f"""            <div class="container slide-inner">
{content_html}
              <div class="slide-visual slide-visual-org">
                <ol class="org-chain" aria-label="Organisational hierarchy: {chain_label}">
{steps_html}
                </ol>
              </div>
            </div>"""
        else:
            visual_html = ""
            slide_cls = "carousel-slide"
            if image:
                alt = html.escape(str(slide.get("image_alt") or slide_title), quote=True)
                position = str(slide.get("image_position") or "").strip()
                style_attr = f' style="object-position: {html.escape(position, quote=True)};"' if position else ""
                slide_cls = "carousel-slide carousel-slide-photo"
                visual_html = f"""            <div class="slide-visual slide-visual-photo">
              <img src="{html.escape(image, quote=True)}" alt="{alt}"{style_attr}>
            </div>
"""
            body_html = f"""{visual_html}            <div class="container slide-inner">
{content_html}
            </div>"""

        if str(slide.get("text_side") or "").strip().lower() == "right":
            slide_cls += " slide-text-right"

        rendered_slides.append(f"""          <article class="{slide_cls}" id="{slide_id}" aria-roledescription="slide" aria-label="{label}">
{body_html}
          </article>""")

        current_attr = ' aria-current="true"' if idx == 1 else ""
        dots.append(f'            <button type="button" class="carousel-dot" aria-label="Go to slide {idx}: {html.escape(slide_title, quote=True)}" aria-controls="{slide_id}"{current_attr}></button>')

    slides_html = "\n".join(rendered_slides)
    controls_html = ""
    if total > 1:
        dots_html = "\n".join(dots)
        controls_html = f"""
        <div class="carousel-controls">
          <button type="button" class="carousel-btn carousel-prev" aria-label="Previous slide">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <div class="carousel-dots">
{dots_html}
          </div>
          <button type="button" class="carousel-btn carousel-next" aria-label="Next slide">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
          </button>
        </div>"""

    return f"""    <section class="hero-carousel" id="affiliations" data-carousel aria-roledescription="carousel" aria-label="{title}">
        <div class="carousel-track" tabindex="0">
{slides_html}
        </div>{controls_html}
    </section>"""


def generate_index_html(
    pubs=None,
    authors=None,
    news=None,
    mission: Optional[Union[Dict[str, Any], List[str], str]] = None,
):
    """Generate the index / about homepage HTML dynamically."""
    header_html = get_header("index")
    footer_html = get_footer()

    if news is None:
        news = load_news()

    if mission is None:
        mission = load_mission()

    # Extract mission data
    if isinstance(mission, dict):
        mission_title = str(mission.get("title") or "The Group Mission").strip()
        mission_subtitle = str(mission.get("subtitle") or "").strip()
        raw_paragraphs = mission.get("paragraphs") or mission.get("mission") or []
        if isinstance(raw_paragraphs, str):
            raw_paragraphs = [p.strip() for p in raw_paragraphs.split("\n\n") if p.strip()]
        affiliations_data = mission.get("affiliations") or {}
    elif isinstance(mission, list):
        mission_title = "The Group Mission"
        mission_subtitle = ""
        raw_paragraphs = mission
        affiliations_data = {}
    elif isinstance(mission, str):
        mission_title = "The Group Mission"
        mission_subtitle = ""
        raw_paragraphs = [p.strip() for p in mission.split("\n\n") if p.strip()]
        affiliations_data = {}
    else:
        mission_title = "The Group Mission"
        mission_subtitle = ""
        raw_paragraphs = []
        affiliations_data = {}

    paragraphs = [str(p).strip() for p in raw_paragraphs if str(p).strip()]
    # The first paragraph is shown as a larger lead-in
    mission_paragraphs_html = "\n".join(
        f"""          <p{' class="home-lead"' if i == 0 else ''}>
            {p}
          </p>"""
        for i, p in enumerate(paragraphs)
    )
    subtitle_html = f'\n        <p class="home-subtitle">{mission_subtitle}</p>' if mission_subtitle else ""

    total_count = len(news)
    latest_news = news[:4]
    historical_news = news[4:]

    def render_news_items(items):
        rendered = []
        for item in items:
            date_val = item.get("date", "")
            headline_val = item.get("headline", "")
            link_val = (item.get("link") or "").strip()
            if link_val:
                is_external = link_val.startswith("http://") or link_val.startswith("https://")
                target_attr = ' target="_blank" rel="noopener noreferrer"' if is_external else ''
                headline_html = f'<a href="{link_val}" class="news-headline-link"{target_attr}>{headline_val} <span class="news-link-arrow" aria-hidden="true">&rarr;</span></a>'
            else:
                headline_html = headline_val

            rendered.append(f"""              <li class="news-item">
                <div class="news-date">{date_val}</div>
                <div class="news-headline">{headline_html}</div>
              </li>""")
        return "\n".join(rendered)

    latest_news_html = render_news_items(latest_news)

    if historical_news:
        historical_news_html = render_news_items(historical_news)
        news_section_html = f"""        <div class="news-box news-box-flat" id="news-section">
            <h2 class="news-box-title news-header-clickable" id="news-header-toggle" role="button" tabindex="0" aria-expanded="false" aria-controls="news-historical-wrap" title="Click to view all {total_count} news updates or open history page" data-total-count="{total_count}">
              <span>Recent Highlights &amp; News</span>
              <a href="news.html" class="news-toggle-indicator" id="news-history-link" title="Open complete historical news page">
                <span id="news-toggle-badge" class="news-toggle-badge">All News &amp; History ({total_count})</span>
                <span id="news-toggle-arrow" class="news-toggle-arrow">&rarr;</span>
              </a>
            </h2>
            <ul class="news-list" id="news-list">
{latest_news_html}
            </ul>
            <div class="news-toggle-bar">
              <a href="news.html" class="news-expand-btn" id="news-expand-btn" title="Open complete historical news archive">
                <span id="news-expand-btn-text">View all {total_count} news updates &amp; history archive</span>
                <span id="news-expand-btn-icon" class="news-expand-btn-icon">&rarr;</span>
              </a>
            </div>
            <div id="news-historical-wrap" class="news-historical-wrap" style="display: none;">
              <div class="news-historical-divider">Historical Archive ({len(historical_news)} earlier milestones)</div>
              <ul class="news-list news-historical-list" id="news-historical-list" style="margin-top: 0.85rem;">
{historical_news_html}
              </ul>
            </div>
        </div>"""
    else:
        news_section_html = f"""        <div class="news-box news-box-flat" id="news-section">
            <h2 class="news-box-title" id="news-header-toggle">
              <span>Recent Highlights &amp; News</span>
            </h2>
            <ul class="news-list" id="news-list">
{latest_news_html}
            </ul>
        </div>"""

    affiliations_html = render_affiliations_carousel_html(affiliations_data)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Mission, background, and methodology of the Data Driven Materials and Molecular Science group at STFC Daresbury Laboratory, UKRI.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content">
{affiliations_html}

    <section class="home-section" id="mission">
      <div class="container home-narrow">
        <span class="home-eyebrow">About DDMMS</span>
        <h2 class="home-heading">{mission_title}</h2>{subtitle_html}
        <div class="home-prose">
{mission_paragraphs_html}
        </div>
      </div>
    </section>

    <section class="home-section home-section-alt" id="news">
      <div class="container home-narrow">
        <span class="home-eyebrow">What's new</span>
{news_section_html}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


def generate_about_html(*args, **kwargs):
    """Alias for generate_index_html."""
    return generate_index_html(*args, **kwargs)
