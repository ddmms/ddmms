"""Index / About page component for the DDMMS website."""

from pathlib import Path

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


def generate_index_html(pubs=None, authors=None, news=None):
    """Generate the index / about homepage HTML."""
    header_html = get_header("index")
    footer_html = get_footer()

    if news is None:
        news = load_news()

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
        news_section_html = f"""          <div class="news-box" style="margin-bottom: 1.5rem;" id="news-section">
            <h3 class="news-box-title news-header-clickable" id="news-header-toggle" role="button" tabindex="0" aria-expanded="false" aria-controls="news-historical-wrap" title="Click to view all {total_count} news updates or open history page" data-total-count="{total_count}">
              <span><span>📢</span> Recent Highlights &amp; News</span>
              <a href="news.html" class="news-toggle-indicator" id="news-history-link" title="Open complete historical news page">
                <span id="news-toggle-badge" class="news-toggle-badge">All News &amp; History ({total_count})</span>
                <span id="news-toggle-arrow" class="news-toggle-arrow">&rarr;</span>
              </a>
            </h3>
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
        news_section_html = f"""          <div class="news-box" style="margin-bottom: 1.5rem;" id="news-section">
            <h3 class="news-box-title" id="news-header-toggle">
              <span><span>📢</span> Recent Highlights &amp; News</span>
            </h3>
            <ul class="news-list" id="news-list">
{latest_news_html}
            </ul>
          </div>"""

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

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          Uniting statistical physics, quantum mechanics, and artificial intelligence to explore matter at the atomic level.
        </p>
      </div>

      <div class="about-grid">
        <div class="about-text">
          <h3>The Group Mission</h3>
          <p>
            The <strong>Data Driven Materials and Molecular Science (DDMMS)</strong> group is hosted within the Scientific Computing Department (SCD) of the Science and Technology Facilities Council (STFC), part of UK Research and Innovation (UKRI), based at Sci-Tech Daresbury.
          </p>
          <p>
            Computational materials science has long faced a fundamental trade-off: high-accuracy quantum mechanical calculations (such as density functional theory and post-Hartree-Fock) are computationally expensive and limited to small systems, whereas classical empirical force fields scale to millions of atoms but suffer from fixed functional forms and limited chemical transferability.
          </p>
          <p>
            Our core mission is to eliminate this trade-off by constructing robust, physics-informed machine-learned interatomic potentials (MLIPs), creating automated calculation workflows, and running extreme-scale simulations on high-performance computing facilities.
          </p>


        </div>

        <div class="about-sidebar">
{news_section_html}

          <div class="news-box">
            <h3 class="news-box-title"><span>🤝</span> Work With Us</h3>
            <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">
              We welcome prospective PhD researchers, postdocs, and international scientific visitors interested in machine-learning interatomic potentials, molecular dynamics algorithms, and porous materials.
            </p>
            <a href="people.html#contact" class="btn btn-primary" style="width: 100%;">Contact the Group</a>
          </div>
        </div>
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


def generate_about_html():
    """Alias for generate_index_html."""
    return generate_index_html()
