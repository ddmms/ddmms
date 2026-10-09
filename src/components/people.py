"""People page component, individual member page generator, and data loaders for the DDMMS website."""

import html
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote
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


def load_person(person_file: Union[str, Path]) -> Dict[str, Any]:
    """Load an individual person's YAML file.

    Raises FileNotFoundError if the file cannot be located.
    """
    target_path: Optional[Path] = None
    cand = Path(person_file)
    if cand.is_file():
        target_path = cand
    else:
        alt = BASE_DIR / person_file
        if alt.is_file():
            target_path = alt
        else:
            alt2 = BASE_DIR / "data" / "people" / person_file
            if alt2.is_file():
                target_path = alt2
            else:
                raise FileNotFoundError(f"Person YAML file not found: '{person_file}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    if not parsed or not isinstance(parsed, dict):
        return {}

    name = str(parsed.get("name") or "").strip()
    if "slug" not in parsed or not parsed["slug"]:
        clean = re.sub(r"^(dr\.|prof\.|mr\.|ms\.|mrs\.)\s+", "", name, flags=re.I).strip().lower()
        clean = re.sub(r"[^\w\s-]", "", clean)
        parsed["slug"] = re.sub(r"[\s_]+", "-", clean)

    if "page" not in parsed or not parsed["page"]:
        parsed["page"] = f"{parsed['slug']}.html"

    return parsed


def load_people(people_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load people sections, members, partner consortia, and opportunities from a YAML file.

    Resolves individual member YAML files for core team members or any member
    referencing a YAML file via `yaml:` or `file:`. Raises FileNotFoundError if
    the people YAML file cannot be located.
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

    people_dir = target_path.parent
    for sec in parsed.get("sections", []):
        sec_id = str(sec.get("id") or "").strip()
        members = sec.get("members") or []
        resolved_members = []
        for member in members:
            if isinstance(member, str) and (member.endswith(".yaml") or member.endswith(".yml")):
                cand_path = people_dir / member if (people_dir / member).is_file() else member
                person_data = load_person(cand_path)
                resolved_members.append(person_data)
            elif isinstance(member, dict):
                yaml_ref = member.get("yaml") or member.get("file")
                if yaml_ref:
                    cand_path = people_dir / yaml_ref if (people_dir / yaml_ref).is_file() else yaml_ref
                    person_data = load_person(cand_path)
                    # File data provides base, member dict can override
                    merged = {**person_data, **member}
                    merged.setdefault("slug", person_data.get("slug"))
                    merged.setdefault("page", person_data.get("page"))
                    resolved_members.append(merged)
                else:
                    # Core team member without explicit yaml key: check data/people/<slug>.yaml
                    if sec_id == "core-team" and member.get("name"):
                        name = member.get("name")
                        clean = re.sub(r"^(dr\.|prof\.|mr\.|ms\.|mrs\.)\s+", "", name, flags=re.I).strip().lower()
                        clean = re.sub(r"[^\w\s-]", "", clean)
                        slug = re.sub(r"[\s_]+", "-", clean)
                        for check_slug in (slug, slug.replace("dr-", "")):
                            possible_file = people_dir / "people" / f"{check_slug}.yaml"
                            if possible_file.is_file():
                                person_data = load_person(possible_file)
                                member = {**person_data, **member}
                                break
                        if "slug" not in member:
                            member["slug"] = slug
                        if "page" not in member:
                            member["page"] = f"{member['slug']}.html"
                    resolved_members.append(member)
        sec["members"] = resolved_members

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
            page = member.get("page")

            # Clickable name for members with an individual page
            if page:
                name_html = f'<a href="{page}" class="person-name-link">{name}</a>'
            else:
                name_html = name

            # Avatar rendering
            if (avatar.startswith("assets/") or avatar.startswith("http") or avatar.startswith("/") or
                any(avatar.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".svg", ".webp"))):
                avatar_inner = f"""              <div class="person-avatar">
                <img src="{avatar}" alt="{name}">
              </div>"""
            elif avatar:
                avatar_inner = f"""              <div class="person-avatar">{avatar}</div>"""
            else:
                initials = "".join([part[0] for part in name.split() if part])[:2].upper()
                avatar_inner = f"""              <div class="person-avatar">{initials}</div>"""

            if page:
                avatar_html = (
                    f'              <a href="{page}" class="person-avatar-link" aria-label="View profile of {name}">\n'
                    f'{avatar_inner}\n'
                    f'              </a>'
                )
            else:
                avatar_html = avatar_inner

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
                f"""                <h3>{name_html}</h3>""",
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


def generate_person_html(
    person_data: Dict[str, Any],
    publications: Optional[List[Dict[str, Any]]] = None,
    base_href: Optional[str] = None,
) -> str:
    """Generate a dedicated individual profile page for a team member."""
    header_html = get_header("people")
    footer_html = get_footer()

    name = str(person_data.get("name") or "").strip()
    role = str(person_data.get("role") or "").strip()
    affiliation = str(person_data.get("affiliation") or "").strip()
    avatar = str(person_data.get("avatar") or "").strip()
    email = str(person_data.get("email") or "").strip()
    bio = str(person_data.get("bio") or "").strip()
    short_bio = str(person_data.get("short_bio") or "").strip()
    tags = person_data.get("tags") or []
    links = person_data.get("links") or []
    research_interests = person_data.get("research_interests") or []
    career_entries = person_data.get("education_and_career") or []

    # Clean name without academic titles for publication searches
    clean_name = re.sub(r"^(dr\.|prof\.|mr\.|ms\.|mrs\.)\s+", "", name, flags=re.I).strip()

    # Meta description snippet
    meta_desc = short_bio or bio[:160]
    meta_desc_escaped = html.escape(re.sub(r"\s+", " ", meta_desc).strip())

    # Base href tag for subdirectory placement if needed
    base_tag = f'  <base href="{base_href}">\n' if base_href else ""
    rel_prefix = base_href if base_href else ""

    # Avatar element
    if (avatar.startswith("assets/") or avatar.startswith("http") or avatar.startswith("/") or
        any(avatar.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".svg", ".webp"))):
        avatar_src = f"{rel_prefix}{avatar}" if (rel_prefix and avatar.startswith("assets/")) else avatar
        avatar_html = f'<img src="{avatar_src}" alt="{name}" class="profile-header-avatar" style="max-height: 300px; height: auto; width: auto; max-width: 100%; object-fit: cover;">'
    elif avatar:
        avatar_html = f'<div class="profile-header-avatar profile-header-avatar-text">{avatar}</div>'
    else:
        initials = "".join([part[0] for part in clean_name.split() if part])[:2].upper()
        avatar_html = f'<div class="profile-header-avatar profile-header-avatar-text">{initials}</div>'

    # Action / Social / Profile links
    link_buttons = []
    if email:
        link_buttons.append(
            f'<a href="mailto:{email}" class="person-link-btn" title="Send Email">'
            f'<span>✉</span> <span>{email}</span></a>'
        )

    publications_found_in_links = False
    for lnk in links:
        if not isinstance(lnk, dict):
            continue
        lnk_text = str(lnk.get("text") or lnk.get("title") or "").strip()
        lnk_url = str(lnk.get("url") or lnk.get("link") or "#").strip()
        is_orcid = (
            str(lnk.get("icon") or "").lower() == "orcid"
            or (lnk_text.lower() == "orcid" and "orcid.org" in lnk_url.lower())
        )
        if lnk_text.lower() == "publications" or "publications.html" in lnk_url:
            publications_found_in_links = True

        if is_orcid and lnk_url != "#":
            link_buttons.append(
                f'<a href="{lnk_url}" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">'
                f'{ORCID_SVG} <span>{lnk_text}</span></a>'
            )
        elif lnk_url.startswith("http://") or lnk_url.startswith("https://"):
            link_buttons.append(
                f'<a href="{lnk_url}" target="_blank" rel="noopener noreferrer" class="person-link-btn">'
                f'<span>{lnk_text}</span></a>'
            )
        elif lnk_url.startswith("publications.html"):
            link_buttons.append(
                f'<a href="{lnk_url}" class="person-link-btn"><span>{lnk_text}</span></a>'
            )
        else:
            link_buttons.append(
                f'<a href="{lnk_url}" class="person-link-btn">{lnk_text}</a>'
            )

    if not publications_found_in_links:
        link_buttons.append(
            f'<a href="publications.html?author={quote(clean_name)}" class="person-link-btn"><span>Publications</span></a>'
        )

    links_rendered = "\n            ".join(link_buttons)
    links_block = f"""          <div class="profile-meta-links">
            {links_rendered}
          </div>""" if link_buttons else ""

    # Biography text paragraphs
    bio_paragraphs = "\n".join(f"          <p>{p.strip()}</p>" for p in bio.split("\n\n") if p.strip())

    # Research Interests & Tags section
    research_section = ""
    if research_interests or tags:
        interests_html = ""
        if research_interests:
            items_rendered = "\n".join(f"          <li>{item}</li>" for item in research_interests)
            interests_html = f"""        <ul class="profile-interests-list">
{items_rendered}
        </ul>"""

        tags_html = ""
        if tags:
            tag_spans = " ".join(f'<span class="person-tag">{t}</span>' for t in tags)
            tags_html = f"""        <div class="person-tags" style="margin-top: 1.25rem;">
          {tag_spans}
        </div>"""

        research_section = f"""      <!-- Research Focus Section -->
      <section class="profile-section">
        <h2 class="profile-section-title">Research Interests &amp; Focus</h2>
{interests_html}
{tags_html}
      </section>"""

    # Career / Education section
    career_section = ""
    if career_entries:
        career_items = []
        for c in career_entries:
            if isinstance(c, dict):
                c_role = c.get("role", "")
                c_inst = c.get("institution", "")
                career_items.append(
                    f'          <li class="profile-career-item"><strong>{c_role}</strong> &mdash; <span>{c_inst}</span></li>'
                )
            elif isinstance(c, str):
                career_items.append(f'          <li class="profile-career-item">{c}</li>')
        if career_items:
            career_items_rendered = "\n".join(career_items)
            career_section = f"""      <!-- Appointments & Roles Section -->
      <section class="profile-section">
        <h2 class="profile-section-title">Appointments &amp; Roles</h2>
        <ul class="profile-career-list">
{career_items_rendered}
        </ul>
      </section>"""

    # Publications matching
    matched_pubs: List[Dict[str, Any]] = []
    if publications:
        clean_tokens = [tok for tok in clean_name.lower().split() if len(tok) > 1]
        for pub in publications:
            pub_authors = [str(a).lower() for a in pub.get("authors", [])]
            matched = False
            for a in pub_authors:
                if clean_name.lower() in a:
                    matched = True
                    break
                if len(clean_tokens) >= 2 and clean_tokens[0] in a and clean_tokens[-1] in a:
                    matched = True
                    break
            if matched:
                matched_pubs.append(pub)

        def pub_sort_key(p: Dict[str, Any]) -> int:
            try:
                return int(p.get("year", 0))
            except (ValueError, TypeError):
                return 0

        matched_pubs.sort(key=pub_sort_key, reverse=True)

    pub_items_rendered = []
    for p in matched_pubs[:5]:
        p_title = p.get("title", "")
        p_year = p.get("year", "")
        p_journal = p.get("journal", "")
        p_doi = p.get("doi", "")
        p_authors = ", ".join(p.get("authors", [])[:4])
        if len(p.get("authors", [])) > 4:
            p_authors += " et al."

        doi_badge = f'<a href="https://doi.org/{p_doi}" target="_blank" rel="noopener noreferrer" class="badge-doi">DOI: {p_doi}</a>' if p_doi else ""
        journal_text = f"<em>{p_journal}</em>" if p_journal else ""
        meta_parts = [part for part in [journal_text, str(p_year)] if part]
        meta_str = " &bull; ".join(meta_parts)

        pub_items_rendered.append(f"""          <div class="profile-pub-item">
            <div class="profile-pub-title">{p_title}</div>
            <div class="profile-pub-meta">
              <span>{p_authors}</span>
              <span>{meta_str}</span>
              {doi_badge}
            </div>
          </div>""")

    pubs_count_label = f" ({len(matched_pubs)})" if matched_pubs else ""
    author_query = quote(clean_name)
    pubs_list_html = "\n".join(pub_items_rendered) if pub_items_rendered else "          <p style='color: var(--text-muted);'>Publications aggregated via the DDMMS ORCID catalogue.</p>"

    publications_section = f"""      <!-- Publications Section -->
      <section class="profile-section">
        <h2 class="profile-section-title">Recent Publications</h2>
        <div class="profile-pubs-list">
{pubs_list_html}
        </div>
        <div style="margin-top: 1.5rem; text-align: left;">
          <a href="publications.html?author={author_query}" class="btn btn-primary">
            View All Publications by {name}{pubs_count_label} &rarr;
          </a>
        </div>
      </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="{meta_desc_escaped}">
{base_tag}  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 2.5rem; padding-bottom: 4rem;">
    <div class="container" style="max-width: 960px;">

      <!-- Breadcrumb / Back Link -->
      <div style="margin-bottom: 1.5rem;">
        <a href="people.html" class="person-back-link">
          &larr; Back to People
        </a>
      </div>

      <!-- Person Profile Header Card -->
      <article class="profile-header-card">
        <div class="profile-header-avatar-wrap">
          {avatar_html}
        </div>
        <div class="profile-header-details">
          <h1 class="profile-header-name">{name}</h1>
          <div class="profile-header-role">{role}</div>
          <div class="profile-header-affiliation">{affiliation}</div>
{links_block}
        </div>
      </article>

      <!-- Biography Section -->
      <section class="profile-section">
        <h2 class="profile-section-title">Biography</h2>
        <div class="profile-bio-text">
{bio_paragraphs}
        </div>
      </section>

{research_section}

{career_section}

{publications_section}

    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
