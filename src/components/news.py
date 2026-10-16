"""News component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

try:
    from .header import get_header
    from .footer import get_footer
    from .layout import render_page_hero
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
        from components.layout import render_page_hero
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer
        from src.components.layout import render_page_hero

BASE_DIR = Path(__file__).resolve().parent.parent.parent
NEWS_FILE = BASE_DIR / "data" / "news.yaml"


def load_news(news_file: Optional[Union[str, Path]] = None) -> List[Dict[str, str]]:
    """Load news items from a YAML file (default: data/news.yaml).

    Requires a valid YAML file provided by the user. Raises FileNotFoundError
    if the file cannot be located.

    Supported YAML format:
      - date: "2026 Milestone"
        headline: "Roadmap..."
        link: "https://..."
    """
    target_path: Optional[Path] = None
    if news_file is not None:
        cand = Path(news_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / news_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"News YAML file not found: '{news_file}'")
    else:
        for cand in (NEWS_FILE, BASE_DIR / "data" / "news.yml"):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(f"News YAML file not found at default location '{NEWS_FILE}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    news_items: List[Dict[str, str]] = []
    if parsed:
        raw_list = parsed if isinstance(parsed, list) else parsed.get("news", [])
        if isinstance(raw_list, list):
            for item in raw_list:
                if not isinstance(item, dict):
                    continue
                date_tag = str(item.get("date") or item.get("category") or "News").strip()
                headline = str(item.get("headline") or item.get("title") or "").strip()
                link = str(item.get("link") or item.get("url") or "").strip()
                if headline:
                    news_items.append({
                        "date": date_tag,
                        "headline": headline,
                        "link": link,
                    })

    return news_items


def generate_news_html(news=None):
    """Generate the dedicated historical news & milestones archive page."""
    header_html = get_header("about")
    footer_html = get_footer()

    if news is None:
        news = load_news()

    news_cards = []
    for item in news:
        date_val = item.get("date", "")
        headline_val = item.get("headline", "")
        link_val = (item.get("link") or "").strip()
        if link_val:
            is_external = link_val.startswith("http://") or link_val.startswith("https://")
            target_attr = ' target="_blank" rel="noopener noreferrer"' if is_external else ''
            headline_html = f'<a href="{link_val}" class="news-headline-link"{target_attr}>{headline_val} <span class="news-link-arrow" aria-hidden="true">&rarr;</span></a>'
        else:
            headline_html = headline_val

        news_cards.append(f"""          <li class="news-item">
            <div class="news-date">{date_val}</div>
            <div class="news-headline">{headline_html}</div>
          </li>""")

    news_cards_html = "\n".join(news_cards)
    hero_html = render_page_hero(
        "News &amp; Historical Milestones",
        "Chronological archive of research milestones, software releases, funded grants, and community workshops.",
        "Updates",
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>News &amp; Milestones | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="All historical news, publications, software releases, and milestones from the Data Driven Materials and Molecular Science group at STFC Daresbury Laboratory.">
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
        <ul class="news-list news-archive-list">
{news_cards_html}
        </ul>
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
