"""DDMMS Website and Publications Package.

Submodules are imported lazily. Importing them here eagerly would mean
`python -m src.pubs` and `python -m src.build_site` found the module already in
sys.modules and ran its body a second time as __main__ (RuntimeWarning from
runpy), and would shadow the submodules with the same-named functions.
"""

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type checkers only
    from .build_site import build_site, load_data
    from .pubs import aggregate_publications, fetch_member_works

# Public name -> submodule it lives in
_EXPORTS = {
    "ORCID_IDS": "pubs",
    "ORCIDS_IDS": "pubs",
    "aggregate_publications": "pubs",
    "assemble_doi_url": "pubs",
    "build_html_page": "pubs",
    "export_json": "pubs",
    "extract_doi": "pubs",
    "extract_fallback_url": "pubs",
    "fetch_member_works": "pubs",
    "generate_html": "pubs",
    "generate_markdown": "pubs",
    "get_configured_orcid_ids": "pubs",
    "get_publication_url": "pubs",
    "load_orcids": "pubs",
    "load_orcids_from_csv": "pubs",
    "load_orcids_from_yaml": "pubs",
    "normalize_title": "pubs",
    "select_best_summary": "pubs",
    "build_site": "build_site",
    "generate_footer_html": "build_site",
    "generate_header_html": "build_site",
    "generate_news_html": "build_site",
    "generate_publications_html": "build_site",
    "get_footer": "build_site",
    "get_header": "build_site",
    "load_data": "build_site",
    "load_news": "build_site",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str):
    """Resolve a re-exported name on first access (PEP 562)."""
    module = _EXPORTS.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(f".{module}", __name__), name)


def __dir__():
    return sorted(set(globals()) | set(_EXPORTS))
