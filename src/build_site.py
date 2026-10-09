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

# Import modular components with flexible path resolution
try:
    from .components.header import generate_header_html, get_header
    from .components.footer import generate_footer_html, get_footer
    from .components.news import load_news, generate_news_html
    from .components.index import generate_index_html, generate_about_html
    from .components.code import generate_code_html
    from .components.publications import generate_publications_html
    from .components.people import generate_people_html
    from .components.research import generate_research_html
except (ImportError, ValueError):
    try:
        from components.header import generate_header_html, get_header
        from components.footer import generate_footer_html, get_footer
        from components.news import load_news, generate_news_html
        from components.index import generate_index_html, generate_about_html
        from components.code import generate_code_html
        from components.publications import generate_publications_html
        from components.people import generate_people_html
        from components.research import generate_research_html
    except ImportError:
        from src.components.header import generate_header_html, get_header
        from src.components.footer import generate_footer_html, get_footer
        from src.components.news import load_news, generate_news_html
        from src.components.index import generate_index_html, generate_about_html
        from src.components.code import generate_code_html
        from src.components.publications import generate_publications_html
        from src.components.people import generate_people_html
        from src.components.research import generate_research_html

__all__ = [
    "BASE_DIR",
    "PUBLICATIONS_FILE",
    "AUTHORS_FILE",
    "NEWS_FILE",
    "load_data",
    "load_news",
    "generate_header_html",
    "get_header",
    "generate_footer_html",
    "get_footer",
    "generate_index_html",
    "generate_about_html",
    "generate_code_html",
    "generate_publications_html",
    "generate_people_html",
    "generate_research_html",
    "generate_news_html",
    "build_site",
    "main",
]


def load_data():
    """Load publications from publications.json and authors from data/authors.yaml (or CSV fallback)."""
    pubs = []
    if PUBLICATIONS_FILE.exists():
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            pubs = json.load(f)

    authors = {
        "0000-0002-7013-6670": "Alin Marin Elena",
        "0009-0005-2015-9478": "Elliott Kasoar",
        "0000-0001-7374-9352": "Junwen Yin",
    }

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
                        orcid = str(item.get("orcid") or item.get("id") or "").strip()
                        name = str(item.get("name") or "").strip()
                        if orcid and name:
                            clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", orcid, flags=re.IGNORECASE).strip()
                            authors[clean_orcid] = name
            elif isinstance(loaded_yaml, dict):
                raw_authors = loaded_yaml.get("authors", loaded_yaml)
                if isinstance(raw_authors, list):
                    for item in raw_authors:
                        if isinstance(item, dict):
                            orcid = str(item.get("orcid") or item.get("id") or "").strip()
                            name = str(item.get("name") or "").strip()
                            if orcid and name:
                                clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", orcid, flags=re.IGNORECASE).strip()
                                authors[clean_orcid] = name
                elif isinstance(raw_authors, dict):
                    for k, v in raw_authors.items():
                        clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", str(k), flags=re.IGNORECASE).strip()
                        authors[clean_orcid] = str(v).strip()
        else:
            reader = csv.reader(content.splitlines())
            for row in reader:
                if not row or row[0].startswith("#") or row[0].lower() in ("orcid", "id"):
                    continue
                if len(row) >= 2:
                    clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", row[0].strip(), flags=re.IGNORECASE).strip()
                    authors[clean_orcid] = row[1].strip()

    return pubs, authors


def main():
    """Generate all site pages using modular components."""
    print("Loading publications, authors, and news...")
    pubs, authors = load_data()
    news = load_news()
    print(f"Loaded {len(pubs)} publications, {len(authors)} authors, and {len(news)} news items.")

    header_content = generate_header_html()
    footer_content = generate_footer_html()

    pages = {
        "header.html": header_content,
        "footer.html": footer_content,
        "index.html": generate_index_html(pubs, authors, news),
        "publications.html": generate_publications_html(pubs, authors),
        "people.html": generate_people_html(),
        "research.html": generate_research_html(),
        "code.html": generate_code_html(),
        "news.html": generate_news_html(news),
    }

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
