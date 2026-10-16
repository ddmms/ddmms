"""Teaching page component and data loader for the DDMMS website."""

import html
from pathlib import Path
from typing import Any, Dict, Optional, Union
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
TEACHING_FILE = BASE_DIR / "data" / "teaching.yaml"


def load_teaching(teaching_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load Teaching page content from a YAML file (default: data/teaching.yaml).

    Raises FileNotFoundError if the file cannot be located.
    """
    if teaching_file is None:
        target_path = TEACHING_FILE
    else:
        target_path = Path(teaching_file)
        if not target_path.is_file():
            target_path = BASE_DIR / teaching_file
    if not target_path.is_file():
        raise FileNotFoundError(f"Teaching YAML file not found: '{teaching_file or TEACHING_FILE}'")

    parsed = yaml.safe_load(target_path.read_text(encoding="utf-8-sig"))
    return parsed if isinstance(parsed, dict) else {}


def generate_teaching_html(teaching: Optional[Dict[str, Any]] = None) -> str:
    """Generate the Teaching page HTML."""
    header_html = get_header("teaching")
    footer_html = get_footer()

    if teaching is None:
        teaching = load_teaching()

    hero_html = render_page_hero(
        str(teaching.get("title") or "Teaching &amp; Training"),
        str(teaching.get("intro") or "").strip(),
    )

    def render_event(event: Dict[str, Any]) -> str:
        title = str(event.get("title")).strip()
        url = str(event.get("url") or "").strip()
        if url:
            title_html = f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{title}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
        else:
            title_html = title
        role = str(event.get("role") or "").strip()
        role_html = f'\n              <span class="teaching-role">{role}</span>' if role else ""
        desc = str(event.get("description") or "").strip()
        desc_html = f'\n              <p class="teaching-desc">{desc}</p>' if desc else ""
        # Optional photo, shown to the right of the entry
        image = str(event.get("image") or "").strip()
        item_cls = "teaching-item"
        image_html = ""
        if image:
            item_cls += " has-image"
            alt = html.escape(str(event.get("image_alt") or title), quote=True)
            image_html = f'\n            <img class="teaching-image" src="{html.escape(image, quote=True)}" alt="{alt}" loading="lazy">'
        return f"""          <li class="{item_cls}">
            <span class="teaching-year">{event.get("year", "")}</span>
            <div class="teaching-body">
              <h3 class="teaching-title">{title_html}</h3>{role_html}{desc_html}
            </div>{image_html}
          </li>"""

    def external_link(url: str, text: str) -> str:
        return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{text}&nbsp;<span aria-hidden="true">&#8599;</span></a>'

    def render_project(project: Dict[str, Any]) -> str:
        """An ongoing PhD project: status badge, title, who/where, then a short description."""
        title = str(project.get("title")).strip()
        url = str(project.get("url") or "").strip()
        title_html = external_link(url, title) if url else title
        status = str(project.get("status") or "").strip()
        status_html = f'\n            <span class="project-status">{status}</span>' if status else ""

        programme = str(project.get("programme") or "").strip()
        programme_url = str(project.get("programme_url") or "").strip()
        if programme and programme_url:
            programme = external_link(programme_url, programme)
        meta = [
            ("PhD student", str(project.get("student") or "").strip()),
            ("Supervisors", str(project.get("supervisors") or "").strip()),
            ("University", str(project.get("university") or "").strip()),
            ("Programme", programme),
            ("Started", str(project.get("started") or "").strip()),
            ("Duration", str(project.get("duration") or "").strip()),
        ]
        meta_rows = "\n".join(
            f"""              <dt>{label}</dt>
              <dd>{value}</dd>"""
            for label, value in meta if value
        )
        meta_html = f"""
            <dl class="project-meta">
{meta_rows}
            </dl>""" if meta_rows else ""
        desc = str(project.get("description") or "").strip()
        desc_html = f'\n            <p class="project-desc">{desc}</p>' if desc else ""
        return f"""          <li class="project-card">{status_html}
            <h3 class="project-title">{title_html}</h3>{meta_html}{desc_html}
          </li>"""

    def initials(name: str) -> str:
        parts = name.split()
        return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    def render_link(link: Dict[str, Any]) -> str:
        url = str(link.get("url")).strip()
        text = link.get("text", "")
        # Internal links stay in the same tab; external ones open a new tab
        if url.startswith(("http://", "https://")):
            return f'          <a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer" class="person-link-btn">{text}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
        return f'          <a href="{html.escape(url, quote=True)}" class="person-link-btn">{text}&nbsp;<span aria-hidden="true">&rarr;</span></a>'

    categories = [c for c in (teaching.get("categories") or []) if isinstance(c, dict) and c.get("title")]
    subnav_links = []
    category_blocks = []
    for cat in categories:
        cat_id = str(cat.get("id") or "").strip()
        cat_title = str(cat.get("title")).strip()
        if cat_id:
            subnav_links.append(f'        <a href="#{html.escape(cat_id, quote=True)}" class="subnav-pill">{cat_title}</a>')
        id_attr = f' id="{html.escape(cat_id, quote=True)}"' if cat_id else ""

        desc = str(cat.get("description") or "").strip()
        desc_html = f'\n        <p class="teaching-category-desc">{desc}</p>' if desc else ""
        links = [render_link(l) for l in (cat.get("links") or []) if isinstance(l, dict) and l.get("url")]
        links_html = "\n".join(links)
        links_block = f"""
        <div class="link-buttons">
{links_html}
        </div>""" if links else ""
        events = [render_event(e) for e in (cat.get("events") or []) if isinstance(e, dict) and e.get("title")]
        events_html = "\n".join(events)
        events_block = f"""
        <ul class="teaching-list">
{events_html}
        </ul>""" if events else ""
        projects = [render_project(p) for p in (cat.get("projects") or []) if isinstance(p, dict) and p.get("title")]
        projects_html = "\n".join(projects)
        projects_block = f"""
        <ul class="project-list">
{projects_html}
        </ul>""" if projects else ""
        # People on this route (e.g. graduates who trained in the group)
        members = [str(m.get("name")).strip() for m in (cat.get("members") or []) if isinstance(m, dict) and m.get("name")]
        members_block = ""
        if members:
            chips = "\n".join(
                f'          <li class="member-chip"><span class="member-initials" aria-hidden="true">{initials(name)}</span>{name}</li>'
                for name in members
            )
            members_title = str(cat.get("members_title") or "Members").strip()
            members_block = f"""
        <h3 class="teaching-subheading">{members_title}</h3>
        <ul class="member-list">
{chips}
        </ul>"""
        empty_html = "" if (desc or links or events or projects or members) else '\n        <p class="list-empty">Details coming soon.</p>'

        category_blocks.append(f"""      <section class="teaching-category"{id_attr}>
        <h2 class="home-heading">{cat_title}</h2>{desc_html}{events_block}{projects_block}{members_block}{links_block}{empty_html}
      </section>""")

    subnav_html = ""
    if len(subnav_links) > 1:
        subnav_pills_html = "\n".join(subnav_links)
        subnav_html = f"""      <nav class="subnav-pills" aria-label="Teaching page quick navigation">
{subnav_pills_html}
      </nav>

"""
    categories_html = "\n\n".join(category_blocks)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Teaching | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Schools, workshops, PhD projects, the STFC Graduate Scheme and STFC placements with the Data Driven Materials and Molecular Science group.">
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
{subnav_html}{categories_html}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
