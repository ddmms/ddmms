#!/usr/bin/env python3
"""Site generator for Data Driven Materials and Molecular Science (DDMMS) website.

Orchestrates page generation by invoking individual page components,
loading data feeds (publications, authors, news), and writing static HTML assets.
"""

import csv
import json
import re
import sys
from pathlib import Path
import yaml

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PUBLICATIONS_FILE = BASE_DIR / "publications.json"
AUTHORS_FILE = BASE_DIR / "data" / "authors.yaml"
AUTHORS_CSV_FILE = BASE_DIR / "data" / "authors.csv"
HEADER_FILE = BASE_DIR / "header.html"
FOOTER_FILE = BASE_DIR / "footer.html"
NEWS_FILE = BASE_DIR / "data" / "news.yaml"
RESEARCH_FILE = BASE_DIR / "data" / "research.yaml"
PEOPLE_FILE = BASE_DIR / "data" / "people.yaml"
SOFTWARE_FILE = BASE_DIR / "data" / "software.yaml"
MISSION_FILE = BASE_DIR / "data" / "mission.yaml"
COLLABORATE_FILE = BASE_DIR / "data" / "collaborate.yaml"
TRAINING_FILE = BASE_DIR / "data" / "training.yaml"
TEACHING_FILE = TRAINING_FILE
TALKS_FILE = BASE_DIR / "data" / "talks.yaml"
EVENTS_FILE = BASE_DIR / "data" / "events.yaml"

# Import modular components with flexible path resolution
try:
    from .components.header import generate_header_html, get_header
    from .components.footer import generate_footer_html, get_footer
    from .components.news import load_news, generate_news_html
    from .components.index import generate_index_html, generate_about_html, load_mission
    from .components.code import generate_code_html, generate_software_html, load_software
    from .components.publications import generate_publications_html
    from .components.people import generate_people_html, load_people, generate_person_html, load_person
    from .components.research import generate_research_html, load_research
    from .components.collaborate import generate_collaborate_html, load_collaborate
    from .components.teaching import generate_teaching_html, load_teaching, load_training
    from .components.talks import generate_talks_html, load_talks
    from .components.events import generate_events_html, load_events
except (ImportError, ValueError):
    try:
        from components.header import generate_header_html, get_header
        from components.footer import generate_footer_html, get_footer
        from components.news import load_news, generate_news_html
        from components.index import generate_index_html, generate_about_html, load_mission
        from components.code import generate_code_html, generate_software_html, load_software
        from components.publications import generate_publications_html
        from components.people import generate_people_html, load_people, generate_person_html, load_person
        from components.research import generate_research_html, load_research
        from components.collaborate import generate_collaborate_html, load_collaborate
        from components.teaching import generate_teaching_html, load_teaching, load_training
        from components.talks import generate_talks_html, load_talks
        from components.events import generate_events_html, load_events
    except ImportError:
        from src.components.header import generate_header_html, get_header
        from src.components.footer import generate_footer_html, get_footer
        from src.components.news import load_news, generate_news_html
        from src.components.index import generate_index_html, generate_about_html, load_mission
        from src.components.code import generate_code_html, generate_software_html, load_software
        from src.components.publications import generate_publications_html
        from src.components.people import generate_people_html, load_people, generate_person_html, load_person
        from src.components.research import generate_research_html, load_research
        from src.components.collaborate import generate_collaborate_html, load_collaborate
        from src.components.teaching import generate_teaching_html, load_teaching, load_training
        from src.components.talks import generate_talks_html, load_talks
        from src.components.events import generate_events_html, load_events

__all__ = [
    "BASE_DIR",
    "PUBLICATIONS_FILE",
    "AUTHORS_FILE",
    "NEWS_FILE",
    "RESEARCH_FILE",
    "PEOPLE_FILE",
    "SOFTWARE_FILE",
    "MISSION_FILE",
    "COLLABORATE_FILE",
    "TRAINING_FILE",
    "TEACHING_FILE",
    "TALKS_FILE",
    "EVENTS_FILE",
    "load_data",
    "load_news",
    "load_research",
    "load_people",
    "load_software",
    "load_mission",
    "load_collaborate",
    "load_training",
    "load_teaching",
    "load_talks",
    "load_events",
    "generate_header_html",
    "get_header",
    "generate_footer_html",
    "get_footer",
    "generate_index_html",
    "generate_about_html",
    "generate_code_html",
    "generate_software_html",
    "generate_publications_html",
    "generate_people_html",
    "generate_research_html",
    "generate_news_html",
    "generate_collaborate_html",
    "generate_teaching_html",
    "generate_talks_html",
    "generate_events_html",
    "build_site",
    "main",
]


ORCID_PATTERN = re.compile(r"^(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$", re.IGNORECASE)


def add_author_entry(target_dict: Dict[str, str], raw_orcid: Any, raw_name: Any):
    """Add author to target_dict, using cleaned ORCID if valid, or a unique no-orcid key."""
    name = str(raw_name or "").strip()
    if not name:
        return
    clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", str(raw_orcid or ""), flags=re.IGNORECASE).strip()
    if ORCID_PATTERN.match(clean_orcid):
        target_dict[clean_orcid] = name
    else:
        target_dict[f"no-orcid-{name}"] = name


def load_data():
    """Load publications from publications.json and authors from data/authors.yaml (or CSV fallback)."""
    pubs = []
    if PUBLICATIONS_FILE.exists():
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            pubs = json.load(f)

    authors = {}

    authors_path = AUTHORS_FILE
    if not authors_path.exists():
        for cand in (BASE_DIR / "data" / "authors.yml", AUTHORS_CSV_FILE):
            if cand.exists():
                authors_path = cand
                break

    if authors_path.exists():
        content = authors_path.read_text(encoding="utf-8-sig")
        is_yaml = authors_path.suffix.lower() in (".yaml", ".yml") or ("\n- " in content or content.startswith("- "))
        loaded_yaml = None
        if is_yaml:
            try:
                loaded_yaml = yaml.safe_load(content)
            except Exception:
                loaded_yaml = None

        if loaded_yaml:
            if isinstance(loaded_yaml, list):
                for item in loaded_yaml:
                    if isinstance(item, dict):
                        add_author_entry(authors, item.get("orcid") or item.get("id"), item.get("name"))
            elif isinstance(loaded_yaml, dict):
                raw_authors = loaded_yaml.get("authors", loaded_yaml)
                if isinstance(raw_authors, list):
                    for item in raw_authors:
                        if isinstance(item, dict):
                            add_author_entry(authors, item.get("orcid") or item.get("id"), item.get("name"))
                elif isinstance(raw_authors, dict):
                    for k, v in raw_authors.items():
                        add_author_entry(authors, k, v)
        else:
            reader = csv.reader(content.splitlines())
            for row in reader:
                if not row or row[0].startswith("#") or row[0].lower() in ("orcid", "id"):
                    continue
                if len(row) >= 2:
                    add_author_entry(authors, row[0], row[1])

    if not authors:
        authors = {
            "0000-0002-7013-6670": "Alin Marin Elena",
            "0009-0005-2015-9478": "Elliott Kasoar",
            "0000-0001-7374-9352": "Junwen Yin",
        }

    # Ensure any group member from authors (with or without a valid ORCID) present in
    # pub["authors"] is tracked in pub["group_authors"]
    group_author_names = list(authors.values())
    for pub in pubs:
        existing_group = pub.setdefault("group_authors", [])
        pub_authors = pub.get("authors", [])
        for g_name in group_author_names:
            if g_name in existing_group:
                continue
            g_clean = g_name.lower().replace("-", " ")
            g_tokens = [tok for tok in g_clean.split() if len(tok) > 1]
            if not g_tokens:
                continue
            g_family = g_tokens[-1]
            g_first = g_tokens[0]
            for a in pub_authors:
                a_clean = a.lower().replace("-", " ")
                a_tokens = a_clean.split()
                if g_family in a_tokens:
                    other = [t for t in a_tokens if t != g_family]
                    if any(g_first in o or (len(o) == 1 and o == g_first[0]) for o in other):
                        existing_group.append(g_name)
                        break

    return pubs, authors


def main():
    """Generate all site pages using modular components."""
    print("Loading publications, authors, news, research, people, software, and mission...")
    pubs, authors = load_data()
    news = load_news()
    research_data = load_research()
    people_data = load_people()
    software_data = load_software()
    mission_data = load_mission()
    collaborate_data = load_collaborate()
    teaching_data = load_training()
    talks_data = load_talks()
    events_data = load_events()
    total_people = sum(len(s.get("members", [])) for s in people_data.get("sections", []))
    print(
        f"Loaded {len(pubs)} publications, {len(authors)} authors, "
        f"{len(news)} news items, {len(research_data.get('areas') or research_data.get('themes', []))} research areas, "
        f"{total_people} people records, {len(software_data.get('packages', []))} software packages, "
        f"and group mission."
    )

    header_content = generate_header_html()
    footer_content = generate_footer_html()

    pages = {
        "header.html": header_content,
        "footer.html": footer_content,
        "index.html": generate_index_html(
            pubs,
            authors,
            news,
            mission=mission_data,
            collaborate=collaborate_data,
        ),
        "publications.html": generate_publications_html(pubs, authors),
        "people.html": generate_people_html(people_data),
        "research.html": generate_research_html(research_data),
        "code.html": generate_code_html(software_data),
        "news.html": generate_news_html(news),
        "talks.html": generate_talks_html(talks_data),
        "teaching.html": generate_teaching_html(teaching_data),
        "events.html": generate_events_html(events_data),
        "collaborate.html": generate_collaborate_html(collaborate_data),
    }

    # Generate individual profile pages for members with dedicated pages
    for sec in people_data.get("sections", []):
        if sec.get("id") in ("core-team", "members", "alc-phd"):
            for member in sec.get("members", []):
                page_filename = member.get("page")
                slug = member.get("slug")
                if page_filename:
                    pages[page_filename] = generate_person_html(member, pubs, software=software_data)
                    if "/" not in page_filename:
                        pages[f"people/{page_filename}"] = generate_person_html(member, pubs, base_href="../", software=software_data)
                elif slug:
                    pages[f"{slug}.html"] = generate_person_html(member, pubs, software=software_data)
                    pages[f"people/{slug}.html"] = generate_person_html(member, pubs, base_href="../", software=software_data)

    for filename, content in pages.items():
        out_path = BASE_DIR / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filename} ({len(content)} bytes)")

    print("Site generation complete!")


build_site = main


if __name__ == "__main__":
    main()
