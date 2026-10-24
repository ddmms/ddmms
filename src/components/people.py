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
    from .layout import render_page_hero
    from .code import load_software
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
        from components.layout import render_page_hero
        from components.code import load_software
    except ImportError:
        try:
            from src.components.header import get_header
            from src.components.footer import get_footer
            from src.components.layout import render_page_hero
            from src.components.code import load_software
        except ImportError:
            load_software = None

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
                    # Team member without explicit yaml key: check data/people/<slug>.yaml
                    if sec_id in ("core-team", "members") and member.get("name"):
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
    hero_html = render_page_hero(
        str(people_data.get("title") or "Meet the Team"),
        subtitle,
    )

    # Sections without members are hidden unless empty_text or show_empty is set
    raw_sections = [
        sec for sec in raw_sections
        if sec.get("members") or sec.get("empty_text") or sec.get("show_empty")
    ]

    # Format subnav pills (only worth showing when there is more than one section)
    subnav_links = []
    for sec in raw_sections:
        sec_id = sec.get("id", "")
        nav_title = sec.get("nav_title") or sec.get("title") or sec_id
        if sec_id:
            subnav_links.append(f'        <a href="#{sec_id}" class="subnav-pill">{nav_title}</a>')
    subnav_html = ""
    if len(subnav_links) > 1:
        subnav_pills_html = "\n".join(subnav_links)
        subnav_html = f"""      <!-- Quick Section Navigation -->
      <nav class="subnav-pills" aria-label="People page quick navigation">
{subnav_pills_html}
      </nav>

"""

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
            if not tenure:
                j_d = member.get("join_date") or member.get("joined")
                l_d = member.get("left_date") or member.get("left")
                if j_d and l_d:
                    m_j = re.search(r"\b(19\d\d|20\d\d)\b", str(j_d))
                    m_l = re.search(r"\b(19\d\d|20\d\d)\b", str(l_d))
                    if m_j and m_l:
                        tenure = f"{m_j.group(1)}&ndash;{m_l.group(1)}"
                elif j_d and sec_id in ("former-members", "alumni"):
                    m_j = re.search(r"\b(19\d\d|20\d\d)\b", str(j_d))
                    if m_j:
                        tenure = m_j.group(1)
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
        if cards_rendered:
            grid_html = f"""
        <div class="people-grid">
{cards_html}
        </div>"""
        elif sec.get("empty_text"):
            empty_msg = html.escape(str(sec.get("empty_text")).strip())
            grid_html = f"""
        <p class="list-empty">{empty_msg}</p>"""
        else:
            grid_html = ""

        anchor_alias = f'      <span id="core-team" aria-hidden="true"></span>\n' if sec_id == "members" else ""

        sections_rendered.append(f"""{anchor_alias}      <!-- {sec_title} Section -->
      <section id="{sec_id}" class="people-section">
        <div class="section-header">
          <h2 class="section-title">{sec_title}</h2>
          <p class="section-subtitle">
            {sec_subtitle}
          </p>
        </div>

{grid_html}
      </section>""")

    all_sections_html = "\n\n".join(sections_rendered)

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

  <main id="main-content">
{hero_html}

    <section class="home-section">
      <div class="container">
{subnav_html}{all_sections_html}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def compute_bibtex_key(pub: Dict[str, Any]) -> str:
    """Generate or retrieve bibtex citation key for a publication."""
    if pub.get("bibtex_key"):
        return str(pub["bibtex_key"]).strip()
    if pub.get("key"):
        return str(pub["key"]).strip()
    authors = pub.get("authors") or pub.get("group_authors") or []
    if authors:
        first = str(authors[0]).strip().split()[-1].lower()
        first = re.sub(r"[^a-z0-9]", "", first)
    else:
        first = "pub"
    year = str(pub.get("year") or "date")
    doi = str(pub.get("preprint_doi") or pub.get("doi") or "")
    doi_clean = re.sub(r"[^a-zA-Z0-9]", "", doi)
    key_doi = doi_clean[-4:] if len(doi_clean) >= 4 else doi_clean
    return f"{first}{year}{key_doi}"


def get_software_packages(software_data=None) -> List[Dict[str, Any]]:
    """Get list of software package dictionaries."""
    if software_data is None:
        if load_software is not None:
            try:
                software_data = load_software()
            except Exception:
                software_data = None
        if software_data is None:
            sw_path = BASE_DIR / "data" / "software.yaml"
            if sw_path.is_file():
                try:
                    software_data = yaml.safe_load(sw_path.read_text(encoding="utf-8-sig"))
                except Exception:
                    software_data = None

    if isinstance(software_data, dict):
        return software_data.get("packages") or software_data.get("software") or []
    elif isinstance(software_data, list):
        return software_data
    return []


def resolve_highlighted_items(
    highlighted_list: List[Any],
    publications: Optional[List[Dict[str, Any]]] = None,
    software_packages: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Resolve highlighted items (by software identifier or bibtex key/DOI) to enriched objects."""
    resolved: List[Dict[str, Any]] = []
    pubs = publications or []
    sw_packages = software_packages or []

    for item in highlighted_list:
        identifier = ""
        item_type = None
        comment = ""
        image = ""
        custom_data = {}

        if isinstance(item, str):
            identifier = item.strip()
        elif isinstance(item, dict):
            # Check single-key mapping like { "batatia20257006": { "image": "...", "comment": "..." } }
            if len(item) == 1 and not any(
                k in item
                for k in (
                    "id", "key", "bibtex", "identifier", "software",
                    "paper", "publication", "type", "image", "picture",
                    "img", "photo", "figure", "comment", "note", "description",
                )
            ):
                key, val = next(iter(item.items()))
                identifier = str(key).strip()
                if isinstance(val, dict):
                    comment = str(val.get("comment") or val.get("note") or val.get("description") or "").strip()
                    image = str(val.get("image") or val.get("picture") or val.get("img") or val.get("photo") or val.get("figure") or "").strip()
                    custom_data = dict(val)
                elif isinstance(val, str):
                    comment = val.strip()
            else:
                if "software" in item:
                    identifier = str(item["software"]).strip()
                    item_type = "software"
                elif "paper" in item or "publication" in item:
                    identifier = str(item.get("paper") or item.get("publication")).strip()
                    item_type = "paper"
                else:
                    identifier = str(
                        item.get("id") or item.get("key") or item.get("bibtex") or item.get("identifier") or ""
                    ).strip()
                    item_type = item.get("type")
                comment = str(item.get("comment") or item.get("note") or item.get("description") or "").strip()
                image = str(
                    item.get("image")
                    or item.get("picture")
                    or item.get("img")
                    or item.get("photo")
                    or item.get("figure")
                    or ""
                ).strip()
                custom_data = dict(item)

        if not identifier and not custom_data:
            continue

        clean_id = re.sub(r"[^a-zA-Z0-9_-]", "", identifier).lower()

        # Check software first if not forced to paper
        found_software = None
        if item_type != "paper":
            for pkg in sw_packages:
                pkg_id = str(pkg.get("id") or "").lower().strip()
                pkg_name = str(pkg.get("name") or "").lower().strip()
                if clean_id in (pkg_id, pkg_name) or identifier.lower() in (pkg_id, pkg_name):
                    found_software = dict(pkg)
                    break
            if found_software:
                if comment:
                    found_software["comment"] = comment
                if image:
                    found_software["image"] = image
                resolved.append({
                    "type": "software",
                    "data": found_software,
                    "comment": comment,
                    "image": image or found_software.get("image", ""),
                })
                continue
            elif item_type == "software" and custom_data:
                if image:
                    custom_data["image"] = image
                resolved.append({
                    "type": "software",
                    "data": custom_data,
                    "comment": comment,
                    "image": image,
                })
                continue

        # Check publications by bibtex key, DOI, or arXiv ID
        matched_pub = None
        matched_key = ""
        for p in pubs:
            b_key = compute_bibtex_key(p).lower()
            p_bib = str(p.get("bibtex_key") or p.get("key") or "").strip().lower()
            p_doi = str(p.get("doi") or "").strip()
            p_pre_doi = str(p.get("preprint_doi") or "").strip()
            p_arxiv = str(p.get("arxiv_id") or "").strip().lower()

            clean_p_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", p_doi, flags=re.I).lower().replace("doi:", "").strip()
            clean_pre_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", p_pre_doi, flags=re.I).lower().replace("doi:", "").strip()

            id_lower = identifier.lower()

            # Exact or clean bibtex key match
            if b_key == clean_id or p_bib == clean_id or b_key == id_lower or p_bib == id_lower:
                matched_pub = p
                matched_key = b_key
                break

            # Prefix bibtex match (e.g. 'patyukova2026' -> 'patyukova2026565e')
            if len(clean_id) >= 6 and (b_key.startswith(clean_id) or (p_bib and p_bib.startswith(clean_id))):
                matched_pub = p
                matched_key = b_key
                break

            # DOI match
            if clean_p_doi and (id_lower == clean_p_doi or clean_id == re.sub(r"[^a-zA-Z0-9]", "", clean_p_doi)):
                matched_pub = p
                matched_key = b_key
                break

            if clean_pre_doi and (id_lower == clean_pre_doi or clean_id == re.sub(r"[^a-zA-Z0-9]", "", clean_pre_doi)):
                matched_pub = p
                matched_key = b_key
                break

            # arXiv ID match
            if p_arxiv and (id_lower == p_arxiv or id_lower == f"arxiv.{p_arxiv}"):
                matched_pub = p
                matched_key = b_key
                break

        if matched_pub:
            pub_data = dict(matched_pub)
            if image:
                pub_data["image"] = image
            resolved.append({
                "type": "paper",
                "data": pub_data,
                "key": matched_key,
                "comment": comment,
                "image": image or pub_data.get("image", ""),
            })
        elif custom_data and custom_data.get("title"):
            pub_data = dict(custom_data)
            if image:
                pub_data["image"] = image
            resolved.append({
                "type": custom_data.get("type", "paper"),
                "data": pub_data,
                "key": identifier,
                "comment": comment,
                "image": image or pub_data.get("image", ""),
            })

    return resolved


def render_highlighted_software_card(
    pkg: Dict[str, Any],
    rel_prefix: str = "",
    image: str = "",
) -> str:
    """Render a card for a highlighted software tool."""
    name = pkg.get("name") or pkg.get("id") or "Software"
    logo = pkg.get("logo") or ""
    icon = pkg.get("icon") or ""
    desc = pkg.get("description") or ""
    badge = pkg.get("badge") or {}
    install = pkg.get("install") or ""
    links = pkg.get("links") or []
    comment = pkg.get("comment") or ""
    img = image or pkg.get("image") or pkg.get("picture") or pkg.get("img") or pkg.get("figure") or ""

    image_html = ""
    if img:
        img_str = str(img).strip()
        img_src = f"{rel_prefix}{img_str}" if (rel_prefix and img_str.startswith("assets/")) else img_str
        image_html = f"""\n          <div class="highlighted-card-media">
            <img src="{img_src}" alt="{html.escape(name, quote=True)}" class="highlighted-card-image" loading="lazy">
          </div>"""

    if logo:
        logo_src = f"{rel_prefix}{logo}" if (rel_prefix and str(logo).startswith("assets/")) else logo
        logo_html = f'<img src="{logo_src}" alt="{name}" class="highlighted-work-logo">'
    elif icon:
        logo_html = f'<span class="highlighted-work-icon">{icon}</span>'
    else:
        logo_html = '<span class="highlighted-work-icon">💻</span>'

    badge_text = badge.get("text") if isinstance(badge, dict) else str(badge or "")
    badge_html = f'<span class="badge badge-meta">{badge_text}</span>' if badge_text else ''

    # Primary link
    primary_url = "#"
    links_html = []
    if links and isinstance(links, list):
        for lnk in links:
            t = lnk.get("text") or "Link"
            u = lnk.get("url") or lnk.get("link") or "#"
            if primary_url == "#" and u != "#":
                primary_url = u
            clean_t = t.replace("&rarr;", "").replace("→", "").strip()
            links_html.append(
                f'<a href="{u}" target="_blank" rel="noopener noreferrer" class="btn-action"><span>🔗</span> {clean_t}</a>'
            )
    links_bar = f'<div class="highlighted-card-actions">{" ".join(links_html)}</div>' if links_html else ""

    install_html = f'<div class="highlighted-card-install"><code>{install}</code></div>' if install else ""
    comment_html = f'<div class="highlighted-card-comment">{comment}</div>' if comment else ""

    return f"""        <div class="highlighted-card highlighted-software-card">
          <div class="highlighted-card-top">
            <span class="badge badge-software"><span>💻</span> Software</span>
            {badge_html}
          </div>{image_html}
          <div class="highlighted-card-header">
            {logo_html}
            <h3 class="highlighted-card-title"><a href="{primary_url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
          </div>
          <p class="highlighted-card-desc">{desc}</p>
          {comment_html}
          {install_html}
          {links_bar}
        </div>"""


def render_highlighted_paper_card(
    pub: Dict[str, Any],
    bibtex_key: str = "",
    comment: str = "",
    rel_prefix: str = "",
    image: str = "",
) -> str:
    """Render a card for a highlighted publication."""
    title = pub.get("title") or "Publication"
    authors = pub.get("authors") or pub.get("group_authors") or []
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]

    if authors:
        first_author = re.sub(r"[,;]+$", "", str(authors[0])).strip()
        if len(authors) > 1:
            if not re.search(r"\bet al\.?$", first_author, flags=re.I):
                authors_str = f"{first_author} et al."
            else:
                authors_str = first_author
        else:
            authors_str = first_author
    else:
        authors_str = "DDMMS"

    journal = pub.get("journal") or ""
    year = str(pub.get("year") or "")
    doi = pub.get("preprint_doi") or pub.get("doi") or ""
    clean_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I).replace("doi:", "").strip()
    pub_url = f"https://doi.org/{clean_doi}" if clean_doi else (pub.get("url") or "#")

    meta_parts = []
    if journal:
        meta_parts.append(f"<em>{journal}</em>")
    if year:
        meta_parts.append(f'<span class="badge badge-year">{year}</span>')
    meta_str = " ".join(meta_parts)

    doi_badge = f'<a href="https://doi.org/{clean_doi}" target="_blank" rel="noopener noreferrer" class="badge badge-doi">DOI: {clean_doi}</a>' if clean_doi else ""
    key_badge = f'<span class="badge badge-bibtex" title="BibTeX Key">@{bibtex_key}</span>' if bibtex_key else ""
    comment_html = f'<div class="highlighted-card-comment">{comment}</div>' if comment else ""

    img = image or pub.get("image") or pub.get("picture") or pub.get("img") or pub.get("figure") or ""
    image_html = ""
    if img:
        img_str = str(img).strip()
        img_src = f"{rel_prefix}{img_str}" if (rel_prefix and img_str.startswith("assets/")) else img_str
        image_html = f"""\n          <div class="highlighted-card-media">
            <img src="{img_src}" alt="{html.escape(title, quote=True)}" class="highlighted-card-image" loading="lazy">
          </div>"""

    return f"""        <div class="highlighted-card highlighted-paper-card">
          <div class="highlighted-card-top">
            <span class="badge badge-paper"><span>📄</span> Publication</span>
            {key_badge}
          </div>{image_html}
          <h3 class="highlighted-card-title"><a href="{pub_url}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
          <div class="highlighted-card-authors">{authors_str}</div>
          <div class="highlighted-card-meta">{meta_str} {doi_badge}</div>
          {comment_html}
          <div class="highlighted-card-actions">
            <a href="{pub_url}" target="_blank" rel="noopener noreferrer" class="btn-action"><span>🔗</span> View Publication</a>
            <a href="publications.html?search={clean_doi or quote(title[:30])}" class="btn-action"><span>📚</span> Group Catalogue</a>
          </div>
        </div>"""


def filter_publications_by_dates(
    publications: List[Dict[str, Any]],
    join_date: Optional[Union[str, int]] = None,
    left_date: Optional[Union[str, int]] = None,
) -> List[Dict[str, Any]]:
    """Filter publications to those published during tenure (join_date <= pub_year <= left_date)."""
    join_year = None
    left_year = None
    if join_date:
        m = re.search(r"\b(19\d\d|20\d\d)\b", str(join_date))
        if m:
            join_year = int(m.group(1))
    if left_date:
        m = re.search(r"\b(19\d\d|20\d\d)\b", str(left_date))
        if m:
            left_year = int(m.group(1))

    if join_year is None and left_year is None:
        return publications

    filtered = []
    for p in publications:
        try:
            yr = int(p.get("year", 0))
        except (ValueError, TypeError):
            yr = 0
        if yr == 0:
            filtered.append(p)
            continue
        if join_year is not None and yr < join_year:
            continue
        if left_year is not None and yr > left_year:
            continue
        filtered.append(p)
    return filtered


def generate_person_html(
    person_data: Dict[str, Any],
    publications: Optional[List[Dict[str, Any]]] = None,
    base_href: Optional[str] = None,
    software: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
) -> str:
    """Generate a dedicated individual profile page for a team member."""
    header_html = get_header("people")
    footer_html = get_footer()

    name = str(person_data.get("name") or "").strip()
    role = str(person_data.get("role") or "").strip()
    affiliation = str(person_data.get("affiliation") or "").strip()
    avatar = str(
        person_data.get("page_avatar")
        or person_data.get("personal_avatar")
        or person_data.get("hero_image")
        or person_data.get("avatar")
        or ""
    ).strip()
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
        avatar_html = f'<img src="{avatar_src}" alt="{name}" class="profile-header-avatar">'
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
                c_url = str(c.get("url") or "").strip()
                if c_url:
                    c_inst = f'<a href="{html.escape(c_url, quote=True)}" target="_blank" rel="noopener noreferrer">{c_inst}</a>'
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

    # Highlighted Work Section
    highlighted_raw = (
        person_data.get("highlighted_work")
        or person_data.get("highlighted")
        or person_data.get("highlights")
        or []
    )
    if isinstance(highlighted_raw, str):
        highlighted_raw = [highlighted_raw]
    elif isinstance(highlighted_raw, dict):
        flattened = []
        for k, v in highlighted_raw.items():
            if isinstance(v, list):
                for sub in v:
                    if isinstance(sub, str):
                        flattened.append({k.rstrip("s"): sub})
                    elif isinstance(sub, dict):
                        flattened.append(sub)
            elif isinstance(v, (str, dict)):
                flattened.append({k.rstrip("s"): v} if isinstance(v, str) else v)
        highlighted_raw = flattened

    software_packages = get_software_packages(software)
    resolved_highlights = resolve_highlighted_items(highlighted_raw, publications, software_packages)

    highlighted_section = ""
    if resolved_highlights:
        cards_rendered = []
        for h in resolved_highlights:
            h_type = h.get("type")
            h_data = h.get("data") or {}
            h_img = h.get("image") or h_data.get("image") or ""
            if h_type == "software":
                cards_rendered.append(
                    render_highlighted_software_card(
                        h_data, rel_prefix=rel_prefix, image=h_img
                    )
                )
            else:
                cards_rendered.append(
                    render_highlighted_paper_card(
                        h_data,
                        bibtex_key=h.get("key", ""),
                        comment=h.get("comment", ""),
                        rel_prefix=rel_prefix,
                        image=h_img,
                    )
                )

        cards_html = "\n".join(cards_rendered)
        highlighted_section = f"""      <!-- Highlighted Work Section -->
      <section class="profile-section" id="highlighted-work">
        <h2 class="profile-section-title">Highlighted Work</h2>
        <div class="highlighted-work-grid">
{cards_html}
        </div>
      </section>"""

    # Publications matching
    matched_pubs: List[Dict[str, Any]] = []
    if publications:
        clean_name_lower = clean_name.lower().replace("-", " ")
        clean_tokens = [tok for tok in clean_name_lower.split() if len(tok) > 1]
        for pub in publications:
            matched = False
            for g in pub.get("group_authors", []):
                gl = str(g).lower().replace("-", " ")
                if clean_name_lower in gl or gl in clean_name_lower:
                    matched = True
                    break
            if not matched:
                for a in pub.get("authors", []):
                    al = str(a).lower().replace("-", " ")
                    if clean_name_lower in al or al in clean_name_lower:
                        matched = True
                        break
                    if len(clean_tokens) >= 2 and clean_tokens[-1] in al and (clean_tokens[0] in al or clean_tokens[0][0] in al):
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
        p_doi = p.get("preprint_doi") or p.get("doi", "")
        p_authors = ", ".join(p.get("authors") or p.get("group_authors") or [])

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

  <main id="main-content">
    <section class="page-hero">
      <div class="container">
        <div class="profile-header-card">
          <div class="profile-header-details">
            <a href="people.html" class="person-back-link">&larr; Back to People</a>
            <h1 class="page-hero-title profile-header-name">{name}</h1>
            <div class="profile-header-role">{role}</div>
            <div class="profile-header-affiliation">{affiliation}</div>
{links_block}
          </div>
          <div class="profile-header-avatar-wrap">
            {avatar_html}
          </div>
        </div>
      </div>
    </section>

    <section class="home-section">
      <div class="container">
      <!-- Biography Section -->
      <section class="profile-section">
        <h2 class="profile-section-title">Biography</h2>
        <div class="profile-bio-text">
{bio_paragraphs}
        </div>
      </section>

{highlighted_section}

{research_section}

{career_section}

{publications_section}
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
