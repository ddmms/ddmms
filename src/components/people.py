"""People page component and data loader for the DDMMS website."""

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
PEOPLE_FILE = BASE_DIR / "data" / "people.yaml"

ORCID_SVG = (
    '<svg viewBox="0 0 256 256" style="fill:#a6ce39;">'
    '<path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/>'
    '<path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/>'
    '</svg>'
)


def load_people(people_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load people sections, members, partner consortia, and opportunities from a YAML file.

    Requires a valid YAML file provided by the user. Raises FileNotFoundError
    if the file cannot be located.
    """
    target_path: Optional[Path] = None
    if people_file is not None:
        cand = Path(people_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / people_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"People YAML file not found: '{people_file}'")
    else:
        for cand in (PEOPLE_FILE, BASE_DIR / "data" / "people.yml"):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(f"People YAML file not found at default location '{PEOPLE_FILE}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    if not parsed or not isinstance(parsed, dict):
        return {"subtitle": "", "sections": []}

    return parsed


def generate_people_html(people_data: Optional[Dict[str, Any]] = None) -> str:
    """Generate the people page HTML dynamically from people data."""
    header_html = get_header("people")
    footer_html = get_footer()

    if people_data is None:
        people_data = load_people()

    subtitle = str(people_data.get("subtitle") or "").strip()
    raw_sections = people_data.get("sections") or []

    # Format subnav pills
    subnav_links = []
    for sec in raw_sections:
        sec_id = sec.get("id", "")
        nav_title = sec.get("nav_title") or sec.get("title") or sec_id
        if sec_id:
            subnav_links.append(f'        <a href="#{sec_id}" class="subnav-pill">{nav_title}</a>')
    subnav_links.append('        <a href="#contact" class="subnav-pill">Collaborate with Us</a>')
    subnav_pills_html = "\n".join(subnav_links)

    # Format sections
    sections_rendered = []
    for sec in raw_sections:
        sec_id = str(sec.get("id") or "").strip()
        sec_title = str(sec.get("title") or "").strip()
        sec_subtitle = str(sec.get("subtitle") or "").strip()
        members = sec.get("members") or []

        cards_rendered = []
        for member in members:
            name = str(member.get("name") or "").strip()
            avatar = str(member.get("avatar") or "").strip()
            role = str(member.get("role") or "").strip()
            affiliation = str(member.get("affiliation") or "").strip()
            bio = str(member.get("bio") or "").strip()
            tenure = str(member.get("tenure") or "").strip()
            destination = str(member.get("destination") or member.get("now") or "").strip()
            tags = member.get("tags") or []
            links = member.get("links") or []

            # Avatar rendering
            if (avatar.startswith("assets/") or avatar.startswith("http") or avatar.startswith("/") or
                any(avatar.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".svg", ".webp"))):
                avatar_html = f"""              <div class="person-avatar">
                <img src="{avatar}" alt="{name}">
              </div>"""
            elif avatar:
                avatar_html = f"""              <div class="person-avatar">{avatar}</div>"""
            else:
                initials = "".join([part[0] for part in name.split() if part])[:2].upper()
                avatar_html = f"""              <div class="person-avatar">{initials}</div>"""

            # Title wrap extra items
            tenure_html = f'\n                <span class="person-tenure">{tenure}</span>' if tenure else ''
            if destination:
                if not destination.startswith("<span>🎓</span>") and not destination.startswith("🎓"):
                    destination_text = f"<span>🎓</span> Now: {destination}"
                else:
                    destination_text = destination
                dest_html = f'\n                <div class="person-badge-dest">{destination_text}</div>'
            else:
                dest_html = ''

            # Tags
            if tags:
                tag_spans = "\n              ".join(f'<span class="person-tag">{t}</span>' for t in tags if str(t).strip())
                tags_html = f"""            <div class="person-tags">
              {tag_spans}
            </div>"""
            else:
                tags_html = ''

            # Links
            link_elements = []
            for lnk in links:
                if not isinstance(lnk, dict):
                    continue
                lnk_text = str(lnk.get("text") or lnk.get("title") or "").strip()
                lnk_url = str(lnk.get("url") or lnk.get("link") or "#").strip()
                is_orcid = (
                    str(lnk.get("icon") or "").lower() == "orcid"
                    or (lnk_text.lower() == "orcid" and "orcid.org" in lnk_url.lower())
                )
                if is_orcid and lnk_url != "#":
                    link_elements.append(
                        f"""              <a href="{lnk_url}" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                {ORCID_SVG}
                <span>{lnk_text}</span>
              </a>"""
                    )
                elif lnk_url.startswith("http://") or lnk_url.startswith("https://"):
                    link_elements.append(
                        f"""              <a href="{lnk_url}" target="_blank" rel="noopener noreferrer" class="person-link-btn">
                <span>{lnk_text}</span>
              </a>"""
                    )
                elif lnk_url.startswith("publications.html"):
                    link_elements.append(
                        f"""              <a href="{lnk_url}" class="person-link-btn">
                <span>{lnk_text}</span>
              </a>"""
                    )
                else:
                    link_elements.append(
                        f"""              <a href="{lnk_url}" class="person-link-btn">{lnk_text}</a>"""
                    )

            if link_elements:
                links_str = "\n".join(link_elements)
                links_html = f"""            <div class="person-links">
{links_str}
            </div>"""
            else:
                links_html = ''

            parts = [
                """          <article class="person-card">""",
                """            <div class="person-header">""",
                avatar_html,
                """              <div class="person-title-wrap">""",
                f"""                <h3>{name}</h3>""",
                f"""                <div class="person-role">{role}</div>""",
                f"""                <div class="person-affiliation">{affiliation}</div>{dest_html}{tenure_html}""",
                """              </div>""",
                """            </div>""",
                f"""            <p class="person-bio">\n              {bio}\n            </p>""",
            ]
            if tags_html:
                parts.append(tags_html)
            if links_html:
                parts.append(links_html)
            parts.append("""          </article>""")

            cards_rendered.append("\n".join(parts))

        cards_html = "\n\n".join(cards_rendered)

        # Extra section extras (e.g. partner consortia box in collaborators)
        extra_box_html = ""
        if sec_id == "collaborators":
            partner_data = people_data.get("partner_consortia")
            if partner_data and isinstance(partner_data, dict):
                p_title = partner_data.get("title", "Partner Consortia & National Initiatives")
                p_desc = partner_data.get("description", "")
                p_links = partner_data.get("links") or []
                p_links_rendered = "\n".join(
                    f'            <a href="{pl.get("url")}" target="_blank" rel="noopener noreferrer" class="person-link-btn">{pl.get("text")}</a>'
                    for pl in p_links if isinstance(pl, dict) and pl.get("url")
                )
                extra_box_html = f"""\n        <!-- Institutional Partners Box -->
        <div style="margin-top: 2rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.75rem;">
          <h4 style="font-size: 1.15rem; font-weight: 700; color: var(--text-muted); margin-bottom: 0.5rem;">{p_title}</h4>
          <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">
            {p_desc}
          </p>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
{p_links_rendered}
          </div>
        </div>"""

        sections_rendered.append(f"""      <!-- {sec_title} Section -->
      <section id="{sec_id}" style="margin-bottom: 4rem;">
        <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
          <h2 class="section-title" style="font-size: 1.85rem;">{sec_title}</h2>
          <p class="section-subtitle">
            {sec_subtitle}
          </p>
        </div>

        <div class="people-grid">
{cards_html}
        </div>{extra_box_html}
      </section>""")

    all_sections_html = "\n\n".join(sections_rendered)

    # Opportunities / Contact
    opp_data = people_data.get("opportunities") or {}
    opp_title = opp_data.get("title", "Join the Research Group")
    opp_desc = opp_data.get("description", "We are always enthusiastic to collaborate with motivated graduate students, postdoctoral researchers, and academic visitors who wish to explore machine-learned interatomic potentials, extreme-scale molecular dynamics, or materials for sustainable energy technologies.")
    opp_email = opp_data.get("email", "alin-marin.elena@stfc.ac.uk")

    opportunities_html = f"""      <!-- Opportunities Section -->
      <section style="margin-top: 4rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2.5rem;" id="contact">
        <div class="section-header" style="text-align: left; margin-bottom: 1.5rem; padding: 0;">
          <h2 class="section-title" style="font-size: 1.85rem;">{opp_title}</h2>
        </div>
        <p style="color: var(--text-muted); font-size: 1.05rem; line-height: 1.7; max-width: 800px; margin-bottom: 1.5rem;">
          {opp_desc}
        </p>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
          <a href="mailto:{opp_email}" class="btn btn-primary"><span>✉</span> Get in Touch via Email</a>
        </div>
      </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>People | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Meet the researchers, developers, former members, collaborators, and visitors in the Data Driven Materials and Molecular Science group.">
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
      <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
        <p class="section-subtitle">
          {subtitle}
        </p>
      </div>

      <!-- Quick Section Navigation -->
      <nav class="subnav-pills" aria-label="People page quick navigation">
{subnav_pills_html}
      </nav>

{all_sections_html}

{opportunities_html}
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
