"""News component and data loader for the DDMMS website."""

from pathlib import Path
import yaml

try:
    from .header import get_header
    from .footer import get_footer
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer

BASE_DIR = Path(__file__).resolve().parent.parent.parent
NEWS_FILE = BASE_DIR / "data" / "news.yaml"
NEWS_CSV_FILE = BASE_DIR / "data" / "news.csv"

DEFAULT_NEWS = [
    {
        "date": "2026 Milestone",
        "headline": "Roadmap for an atomistic machine-learning ecosystem published on arXiv (2609.39090).",
        "link": "https://arxiv.org/abs/2609.39090",
    },
    {
        "date": "2026 Release",
        "headline": "Goldilocks automated k-point sampling framework for Quantum ESPRESSO published in <em>Digital Discovery</em>.",
        "link": "https://doi.org/10.1039/D4DD00045A",
    },
    {
        "date": "2026 Discovery",
        "headline": "uMOF universal benchmark database and ML interatomic potentials released for metal-organic frameworks.",
        "link": "",
    },
    {
        "date": "Software Ecosystem",
        "headline": "aiida-mlip released, integrating janus-core workflows with full data provenance in AiiDA.",
        "link": "https://github.com/stfc/aiida-mlip",
    },
]


def load_news(news_file=None):
    """Load news items from YAML file (data/news.yaml) or fallback CSV file.

    Supported YAML format:
      - date: "2026 Milestone"
        headline: "Roadmap..."
        link: "https://..."

    Supported CSV row format:
      Date or Category | Headline [ | Optional Link URL ]
    """
    if news_file is None:
        news_file = NEWS_FILE
        if not news_file.exists():
            for alt_name in ("news.yml", "news.csv"):
                cand = BASE_DIR / "data" / alt_name
                if cand.exists():
                    news_file = cand
                    break

    target_path = Path(news_file)
    if not target_path.exists():
        alt_path = BASE_DIR / news_file
        if alt_path.exists():
            target_path = alt_path

    news_items = []
    if target_path.exists():
        content = target_path.read_text(encoding="utf-8-sig")
        is_yaml = target_path.suffix.lower() in (".yaml", ".yml") or ("\n- " in content or content.startswith("- "))
        parsed = None
        if is_yaml:
            try:
                parsed = yaml.safe_load(content)
            except Exception:
                parsed = None

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

        # Fallback to pipe-separated CSV parsing if not YAML or no items loaded
        if not news_items:
            for line in content.splitlines():
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue
                parts = clean_line.split("|")
                if len(parts) >= 3:
                    date_tag = parts[0].strip()
                    last_part = parts[-1].strip()
                    if len(parts) > 3 and (last_part.startswith("http://") or last_part.startswith("https://") or last_part.startswith("/") or not last_part):
                        headline = "|".join(parts[1:-1]).strip()
                        link = last_part
                    else:
                        headline = parts[1].strip()
                        link = parts[2].strip()
                elif len(parts) == 2:
                    date_tag = parts[0].strip()
                    headline = parts[1].strip()
                    link = ""
                else:
                    date_tag = "News"
                    headline = parts[0].strip()
                    link = ""

                if headline:
                    news_items.append({
                        "date": date_tag,
                        "headline": headline,
                        "link": link,
                    })

    return news_items if news_items else [dict(item) for item in DEFAULT_NEWS]


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
            action_btn = f'<a href="{link_val}" class="btn btn-sm btn-outline"{target_attr} style="margin-top: 0.65rem; display: inline-flex; align-items: center; gap: 0.35rem;">Visit Resource &rarr;</a>'
        else:
            headline_html = headline_val
            action_btn = ''

        news_cards.append(f"""        <article class="news-card-archive" style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; box-shadow: var(--shadow-sm); position: relative; border-left: 4px solid var(--accent-teal);">
          <div class="news-date">{date_val}</div>
          <div class="news-headline" style="font-size: 1.05rem; line-height: 1.5; margin-top: 0.35rem;">{headline_html}</div>
          {f'<div style="margin-top: 0.5rem;">{action_btn}</div>' if action_btn else ''}
        </article>""")

    news_cards_html = "\n".join(news_cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>News &amp; Milestones | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="All historical news, publications, software releases, and milestones from the Data Driven
  Materials and Molecular Science group at SCD-STFC-UKRI.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
          <div>
            <h1 class="section-title">News &amp; Historical Milestones</h1>
            <p class="section-subtitle">
              Chronological archive of research milestones, software releases, funded grants, and community workshops.
            </p>
          </div>
          <a href="index.html" class="btn btn-outline" style="align-self: center;">&larr; Back to About</a>
        </div>
      </div>

      <div class="news-archive-grid" style="display: flex; flex-direction: column; gap: 1.25rem; max-width: 860px;">
{news_cards_html}
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
