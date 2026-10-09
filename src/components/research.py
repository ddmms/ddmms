"""Research page component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
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
RESEARCH_FILE = BASE_DIR / "data" / "research.yaml"


def load_research(research_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load research approach and research themes from a YAML file (default: data/research.yaml).

    Requires a valid YAML file provided by the user. Raises FileNotFoundError
    if the file cannot be located.

    Supported YAML format:
      approach:
        subtitle: "From quantum-level..."
      themes:
        - id: "mlips"
          tag: "Interest 1 • Physics-Informed AI"
          title: "Foundation Machine-Learned Interatomic Potentials (MLIPs)"
          description:
            - "Paragraph 1..."
            - "Paragraph 2..."
          links:
            - text: "Explore Related Publications &rarr;"
              url: "publications.html?search=MLIP"
              class: "btn btn-outline"
    """
    target_path: Optional[Path] = None
    if research_file is not None:
        cand = Path(research_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / research_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"Research YAML file not found: '{research_file}'")
    else:
        for cand in (RESEARCH_FILE, BASE_DIR / "data" / "research.yml"):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(f"Research YAML file not found at default location '{RESEARCH_FILE}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    if not parsed:
        return {"approach": "", "themes": []}

    if isinstance(parsed, list):
        return {"approach": "", "themes": parsed}

    if isinstance(parsed, dict):
        approach = parsed.get("approach") or parsed.get("subtitle") or ""
        themes = parsed.get("themes") or parsed.get("research_themes") or []
        return {
            "approach": approach,
            "themes": themes,
        }

    return {"approach": "", "themes": []}


def generate_research_html(
    research_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    approach: Optional[Union[str, Dict[str, Any]]] = None,
) -> str:
    """Generate the research page HTML."""
    header_html = get_header("research")
    footer_html = get_footer()

    if research_data is None:
        research_data = load_research()

    themes: List[Dict[str, Any]] = []
    if isinstance(research_data, dict):
        if approach is None:
            approach = research_data.get("approach", "")
        raw_themes = research_data.get("themes") or research_data.get("research_themes") or []
        if isinstance(raw_themes, list):
            themes = raw_themes
    elif isinstance(research_data, list):
        themes = research_data

    # Extract approach subtitle
    subtitle = ""
    if isinstance(approach, dict):
        subtitle = str(approach.get("subtitle") or approach.get("description") or approach.get("text") or "").strip()
    elif isinstance(approach, str):
        subtitle = approach.strip()

    section_header_html = ""
    if subtitle:
        section_header_html = f"""      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          {subtitle}
        </p>
      </div>"""
    else:
        section_header_html = """      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
      </div>"""

    cards = []
    for theme in themes:
        if not isinstance(theme, dict):
            continue
        tag = str(theme.get("tag") or "").strip()
        title = str(theme.get("title") or "").strip()
        desc = theme.get("description") or theme.get("desc") or ""

        # Format paragraphs
        desc_paragraphs = []
        if isinstance(desc, list):
            for i, p in enumerate(desc):
                p_text = str(p).strip()
                if not p_text:
                    continue
                style_attr = ' style="margin-top: 0.5rem;"' if i > 0 else ''
                desc_paragraphs.append(f'            <p class="research-card-desc"{style_attr}>\n              {p_text}\n            </p>')
        elif isinstance(desc, str) and desc.strip():
            desc_paragraphs.append(f'            <p class="research-card-desc">\n              {desc.strip()}\n            </p>')

        desc_html = "\n".join(desc_paragraphs)

        # Format action buttons/links
        raw_links = theme.get("links") or theme.get("buttons") or []
        if not raw_links and (theme.get("link") or theme.get("url")):
            raw_links = [{
                "text": theme.get("link_text") or theme.get("text") or "Explore &rarr;",
                "url": theme.get("link") or theme.get("url"),
                "class": theme.get("class", "btn btn-outline"),
            }]

        link_elements = []
        if isinstance(raw_links, list):
            for link_item in raw_links:
                if not isinstance(link_item, dict):
                    continue
                link_text = str(link_item.get("text") or link_item.get("title") or "Explore &rarr;").strip()
                link_url = str(link_item.get("url") or link_item.get("link") or "").strip()
                btn_class = str(link_item.get("class") or "btn btn-outline").strip()

                if not link_url:
                    continue

                is_external = link_url.startswith("http://") or link_url.startswith("https://")
                target_attr = ' target="_blank" rel="noopener noreferrer"' if is_external else ''

                link_elements.append(
                    f'<a href="{link_url}" class="{btn_class}"{target_attr}>{link_text}</a>'
                )

        actions_html = ""
        if link_elements:
            links_str = "\n            ".join(link_elements)
            actions_html = f"""          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; gap: 0.75rem; flex-wrap: wrap;">
            {links_str}
          </div>"""

        tag_html = f'<span class="research-tag">{tag}</span>\n            ' if tag else ''

        cards.append(f"""        <article class="research-card">
          <div class="research-card-top">
            {tag_html}<h2 class="research-card-title">{title}</h2>
{desc_html}
          </div>
{actions_html}
        </article>""")

    cards_html = "\n\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Research areas of the Data Driven Materials and Molecular Science group: MLIPs, MOFs, molten salts, and automated workflows.">
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
{section_header_html}

      <div class="research-grid" style="grid-template-columns: 1fr; gap: 2.5rem;">
{cards_html}
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
