"""Publications page component for the DDMMS website."""

import json

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


def generate_publications_html(pubs, authors):
    """Generate the publications catalogue page HTML."""
    header_html = get_header("publications")
    footer_html = get_footer()
    pubs_json_str = json.dumps(pubs)
    authors_json_str = json.dumps(authors)

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Publications | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Full publication catalogue for the Data Driven Materials and Molecular Science group, auto-aggregated from ORCID.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 2.5rem;">
    <div class="container" id="pubs-app-root">
      <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
        <p class="section-subtitle">
          Comprehensive, real-time bibliography aggregated via the ORCID Public API for members of Data Driven Materials and Molecular Science.
        </p>
      </div>

      <!-- Quick Metrics Summary -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Total Articles</div>
          <div id="stat-total-pubs" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">{len(pubs)}</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Group Authors</div>
          <div id="stat-authors" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">{len(authors)}</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Years Span</div>
          <div id="stat-years" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">-</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Journals &amp; Venues</div>
          <div id="stat-venues" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">-</div>
        </div>
      </div>

      <!-- Controls Card -->
      <div class="pubs-controls-card">
        <div class="pubs-controls-grid">
          <div class="form-group">
            <label for="pub-filter-author"><span>👤</span> Filter by Author</label>
            <select id="pub-filter-author" class="form-control pub-filter-author">
              <option value="all">All Group Members</option>
            </select>
          </div>

          <div class="form-group">
            <label for="pub-filter-year"><span>📅</span> Filter by Year</label>
            <select id="pub-filter-year" class="form-control pub-filter-year">
              <option value="all">All Years</option>
            </select>
          </div>

          <div class="form-group">
            <label for="pub-filter-search"><span>🔍</span> Search Keywords</label>
            <input type="text" id="pub-filter-search" class="form-control pub-filter-search" placeholder="Title, journal, DOI, author...">
          </div>

          <div class="form-group">
            <label for="pub-filter-sort"><span>⚡</span> Sort Order</label>
            <select id="pub-filter-sort" class="form-control pub-filter-sort">
              <option value="year-desc">Year (Newest First)</option>
              <option value="year-asc">Year (Oldest First)</option>
              <option value="title-asc">Title (A - Z)</option>
            </select>
          </div>
        </div>

        <div class="pubs-controls-extra">
          <label class="checkbox-label">
            <input type="checkbox" class="pub-toggle-group-year" checked>
            <span>Group publications by year</span>
          </label>

          <button type="button" class="btn-action pub-reset-btn">
            <span>↺</span> Reset Filters
          </button>
        </div>
      </div>

      <!-- Status Bar -->
      <div class="pubs-results-bar">
        <div class="pubs-counter">
          Showing <strong class="pub-visible-count">0</strong> of <strong class="pub-total-count">{len(pubs)}</strong> publications
        </div>

        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          <a href="publications.json" download="publications.json" class="btn-action" title="Download raw JSON feed">
            <span>{{ }}</span> Download JSON
          </a>
          <a href="PUBLICATIONS.md" class="btn-action" title="View Markdown bibliography">
            <span>📄</span> View Markdown
          </a>
        </div>
      </div>

      <!-- Publication Cards List -->
      <div class="pubs-container"></div>
    </div>
  </main>

{footer_html}

  <script id="publications-data" type="application/json">
{pubs_json_str}
  </script>
  <script id="authors-data" type="application/json">
{authors_json_str}
  </script>

  <script src="assets/js/main.js"></script>
  <script src="assets/js/publications.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      window.initPublications('pubs-app-root');
    }});
  </script>
</body>
</html>"""
    return content
