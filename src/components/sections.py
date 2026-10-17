"""Shared renderer for pages built from YAML categories (Teaching, Opportunities).

Each category is a section with an optional description followed by any of:
events (dated list), cards (e.g. PhD projects, upcoming events), members
(name chips) and links (buttons, always last).
"""

import html
from typing import Any, Dict, List, Tuple


def _external_link(url: str, text: str) -> str:
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{text}&nbsp;<span aria-hidden="true">&#8599;</span></a>'


def _initials(name: str) -> str:
    parts = name.split()
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


def _render_link_button(link: Dict[str, Any], indent: str = "          ") -> str:
    url = str(link.get("url")).strip()
    text = link.get("text", "")
    # Internal links stay in the same tab; external ones open a new tab
    if url.startswith(("http://", "https://")):
        return f'{indent}<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer" class="person-link-btn">{text}&nbsp;<span aria-hidden="true">&#8599;</span></a>'
    return f'{indent}<a href="{html.escape(url, quote=True)}" class="person-link-btn">{text}&nbsp;<span aria-hidden="true">&rarr;</span></a>'


def _link_buttons(links: List[Any], indent: str) -> List[str]:
    return [_render_link_button(l, indent + "  ") for l in links or [] if isinstance(l, dict) and l.get("url")]


def _render_event(event: Dict[str, Any]) -> str:
    """One row of a dated list: year on the left, entry and optional photo on the right."""
    title = str(event.get("title")).strip()
    url = str(event.get("url") or "").strip()
    title_html = _external_link(url, title) if url else title
    role = str(event.get("role") or "").strip()
    role_html = f'\n              <span class="teaching-role">{role}</span>' if role else ""
    desc = str(event.get("description") or "").strip()
    desc_html = f'\n              <p class="teaching-desc">{desc}</p>' if desc else ""
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


def _render_card(card: Dict[str, Any]) -> str:
    """A boxed entry: status badge, title, label/value details, description, buttons."""
    title = str(card.get("title")).strip()
    url = str(card.get("url") or "").strip()
    title_html = _external_link(url, title) if url else title
    status = str(card.get("status") or "").strip()
    status_html = f'\n            <span class="card-status">{status}</span>' if status else ""

    rows = []
    for d in card.get("details") or []:
        if not isinstance(d, dict) or not d.get("label") or not d.get("value"):
            continue
        value = str(d["value"]).strip()
        d_url = str(d.get("url") or "").strip()
        rows.append(f"""              <dt>{d["label"]}</dt>
              <dd>{_external_link(d_url, value) if d_url else value}</dd>""")
    rows_html = "\n".join(rows)
    details_html = f"""
            <dl class="card-meta">
{rows_html}
            </dl>""" if rows else ""
    desc = str(card.get("description") or "").strip()
    desc_html = f'\n            <p class="card-desc">{desc}</p>' if desc else ""
    buttons = _link_buttons(card.get("links"), "            ")
    buttons_html = "\n".join(buttons)
    buttons_block = f"""
            <div class="link-buttons">
{buttons_html}
            </div>""" if buttons else ""
    return f"""          <li class="info-card">{status_html}
            <h3 class="card-title">{title_html}</h3>{details_html}{desc_html}{buttons_block}
          </li>"""


def render_category_sections(categories: List[Any], nav_label: str) -> Tuple[str, str]:
    """Return (jump-link nav, sections) HTML for a list of category dicts."""
    subnav_links = []
    blocks = []
    for cat in categories or []:
        if not isinstance(cat, dict) or not cat.get("title"):
            continue
        cat_id = str(cat.get("id") or "").strip()
        cat_title = str(cat.get("title")).strip()
        if cat_id:
            subnav_links.append(f'        <a href="#{html.escape(cat_id, quote=True)}" class="subnav-pill">{cat_title}</a>')
        id_attr = f' id="{html.escape(cat_id, quote=True)}"' if cat_id else ""

        desc = str(cat.get("description") or "").strip()
        desc_html = f'\n        <p class="category-desc">{desc}</p>' if desc else ""

        events = [_render_event(e) for e in cat.get("events") or [] if isinstance(e, dict) and e.get("title")]
        events_html = "\n".join(events)
        events_block = f"""
        <ul class="teaching-list">
{events_html}
        </ul>""" if events else ""

        cards = [_render_card(c) for c in cat.get("cards") or [] if isinstance(c, dict) and c.get("title")]
        cards_html = "\n".join(cards)
        cards_block = f"""
        <ul class="card-list">
{cards_html}
        </ul>""" if cards else ""

        members = [str(m.get("name")).strip() for m in cat.get("members") or [] if isinstance(m, dict) and m.get("name")]
        members_block = ""
        if members:
            chips = "\n".join(
                f'          <li class="member-chip"><span class="member-initials" aria-hidden="true">{_initials(name)}</span>{name}</li>'
                for name in members
            )
            members_title = str(cat.get("members_title") or "").strip()
            title_html = f'\n        <h3 class="category-subheading">{members_title}</h3>' if members_title else ""
            members_block = f"""{title_html}
        <ul class="member-list">
{chips}
        </ul>"""

        links = _link_buttons(cat.get("links"), "        ")
        links_html = "\n".join(links)
        links_block = f"""
        <div class="link-buttons">
{links_html}
        </div>""" if links else ""

        empty_html = "" if (desc or events or cards or members or links) else '\n        <p class="list-empty">Details coming soon.</p>'
        blocks.append(f"""      <section class="category-section"{id_attr}>
        <h2 class="home-heading">{cat_title}</h2>{desc_html}{events_block}{cards_block}{members_block}{links_block}{empty_html}
      </section>""")

    subnav_html = ""
    if len(subnav_links) > 1:
        subnav_pills_html = "\n".join(subnav_links)
        subnav_html = f"""      <nav class="subnav-pills" aria-label="{html.escape(nav_label, quote=True)}">
{subnav_pills_html}
      </nav>

"""
    return subnav_html, "\n\n".join(blocks)
