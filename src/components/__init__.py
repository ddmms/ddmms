"""Modular components for the DDMMS site."""

from .header import generate_header_html, get_header
from .footer import generate_footer_html, get_footer
from .news import DEFAULT_NEWS, load_news, generate_news_html
from .index import generate_index_html, generate_about_html
from .code import generate_code_html
from .publications import generate_publications_html
from .people import generate_people_html
from .research import generate_research_html

__all__ = [
    "generate_header_html",
    "get_header",
    "generate_footer_html",
    "get_footer",
    "DEFAULT_NEWS",
    "load_news",
    "generate_news_html",
    "generate_index_html",
    "generate_about_html",
    "generate_code_html",
    "generate_publications_html",
    "generate_people_html",
    "generate_research_html",
]
