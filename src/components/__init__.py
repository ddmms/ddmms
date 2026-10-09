"""Modular components for the DDMMS site."""

from .header import generate_header_html, get_header
from .footer import generate_footer_html, get_footer
from .news import load_news, generate_news_html
from .index import generate_index_html, generate_about_html, load_mission, load_index
from .code import generate_code_html, generate_software_html, load_software
from .publications import generate_publications_html, build_html_page, generate_html
from .people import generate_people_html, load_people, generate_person_html, load_person
from .research import generate_research_html, load_research

__all__ = [
    "generate_header_html",
    "get_header",
    "generate_footer_html",
    "get_footer",
    "load_news",
    "generate_news_html",
    "load_mission",
    "load_index",
    "generate_index_html",
    "generate_about_html",
    "load_software",
    "generate_code_html",
    "generate_software_html",
    "generate_publications_html",
    "build_html_page",
    "generate_html",
    "load_people",
    "generate_people_html",
    "load_person",
    "generate_person_html",
    "load_research",
    "generate_research_html",
]
