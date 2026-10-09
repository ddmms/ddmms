"""Pubs - Aggregate research publications from ORCID API.

Copyright (c) 2026, Alin M. Elena and contributors
Distributed under the terms of the BSD 3-Clause License.
"""
import argparse
import csv
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Union
import requests
import yaml

# HTML generation is delegated to components.publications; re-export for backward compatibility
try:
    from .components.publications import build_html_page, generate_html
except (ImportError, ValueError):
    try:
        from components.publications import build_html_page, generate_html
    except ImportError:
        from src.components.publications import build_html_page, generate_html

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_AUTHORS_PATH = str(BASE_DIR / "data" / "authors.yaml")
DEFAULT_CSV_PATH = str(BASE_DIR / "data" / "authors.csv")

# Fallback dictionary if authors file is not found
DEFAULT_ORCID_IDS: Dict[str, str] = {
    "0000-0002-7013-6670": "Alin Marin Elena",
}


def load_orcids_from_yaml(yaml_path: str = DEFAULT_AUTHORS_PATH) -> Dict[str, str]:
    """Load ORCID to author name mapping from a YAML file.

    Format expected:
      - orcid: '0000-0002-7013-6670'
        name: 'Alin Marin Elena'
      or dictionary mapping of '0000-...': 'Name'
    """
    p = Path(yaml_path)
    if not p.is_file():
        alt = BASE_DIR / yaml_path
        if alt.is_file():
            p = alt
        else:
            raise FileNotFoundError(f"Authors YAML file not found at '{yaml_path}'")

    content = p.read_text(encoding="utf-8-sig")
    data = yaml.safe_load(content)
    mapping: Dict[str, str] = {}
    orcid_pattern = re.compile(r"^(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$", re.IGNORECASE)

    def add_author(raw_orcid, raw_name):
        if not raw_orcid or not raw_name:
            return
        clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", str(raw_orcid), flags=re.IGNORECASE).strip()
        if orcid_pattern.match(clean_orcid):
            mapping[clean_orcid] = str(raw_name).strip()

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add_author(item.get("orcid") or item.get("id"), item.get("name"))
    elif isinstance(data, dict):
        raw_list = data.get("authors")
        if isinstance(raw_list, list):
            for item in raw_list:
                if isinstance(item, dict):
                    add_author(item.get("orcid") or item.get("id"), item.get("name"))
        else:
            for k, v in data.items():
                if k.lower() not in ("authors", "title", "description"):
                    add_author(k, v)

    return mapping


def load_orcids_from_csv(csv_path: str = DEFAULT_AUTHORS_PATH) -> Dict[str, str]:
    """Load ORCID to author name mapping from a CSV or YAML file.

    Maintained for backward compatibility. Supports both CSV and YAML paths.
    """
    if not os.path.exists(csv_path):
        alt_path = os.path.join(str(BASE_DIR), csv_path)
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            raise FileNotFoundError(f"Authors file not found at '{csv_path}'")

    # If it's a YAML file, route to YAML loader
    if csv_path.lower().endswith((".yaml", ".yml")):
        return load_orcids_from_yaml(csv_path)

    mapping: Dict[str, str] = {}
    orcid_pattern = re.compile(r"^(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$", re.IGNORECASE)

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for line_num, row in enumerate(reader, start=1):
            if not row or not any(field.strip() for field in row):
                continue

            first_cell = row[0].strip()
            if first_cell.startswith("#"):
                continue

            # Header row detection
            if first_cell.lower() in ("orcid", "orcid_id", "orcid id", "id"):
                continue

            if len(row) < 2:
                print(f"Warning: Skipping invalid row {line_num} in {csv_path}: expected 'orcid,name'")
                continue

            raw_orcid = row[0].strip()
            name = row[1].strip()

            clean_orcid = re.sub(r"^https?://(www\.)?orcid\.org/", "", raw_orcid, flags=re.IGNORECASE).strip()

            if not orcid_pattern.match(clean_orcid):
                print(f"Warning: Skipping row {line_num} in {csv_path}: invalid ORCID '{raw_orcid}'")
                continue

            if not name:
                print(f"Warning: Skipping row {line_num} in {csv_path}: missing author name for '{clean_orcid}'")
                continue

            mapping[clean_orcid] = name

    return mapping


load_orcids = load_orcids_from_yaml


def get_configured_orcid_ids(path: Optional[str] = None) -> Dict[str, str]:
    """Retrieve ORCID mapping from YAML (or CSV fallback) if available, otherwise return default mapping."""
    if path is None:
        for cand in (DEFAULT_AUTHORS_PATH, str(BASE_DIR / "data" / "authors.yml"), DEFAULT_CSV_PATH):
            if os.path.isfile(cand):
                path = cand
                break
    if path and os.path.isfile(path):
        try:
            if path.lower().endswith((".yaml", ".yml")):
                loaded = load_orcids_from_yaml(path)
            else:
                loaded = load_orcids_from_csv(path)
            if loaded:
                return loaded
        except Exception as e:
            print(f"Warning: Could not read {path}: {e}")
    return dict(DEFAULT_ORCID_IDS)


# Initialized from YAML/CSV if present
ORCID_IDS: Dict[str, str] = get_configured_orcid_ids()
ORCIDS_IDS = ORCID_IDS

ORCID_API_BASE = "https://pub.orcid.org/v3.0"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "pubs-fetcher/1.0 (https://orcid.org; mailto:admin@example.org)",
}


def extract_doi(external_ids: Dict[str, Any] | None) -> str | None:
    """Find and normalize DOI from external-ids field."""
    if not external_ids or not isinstance(external_ids, dict):
        return None
    for ext_id in external_ids.get("external-id") or []:
        if not ext_id or not isinstance(ext_id, dict):
            continue
        id_type = ext_id.get("external-id-type")
        if id_type and str(id_type).lower() == "doi":
            doi_val = ext_id.get("external-id-value")
            if doi_val and isinstance(doi_val, str):
                doi_clean = doi_val.strip()
                doi_clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi_clean, flags=re.IGNORECASE)
                doi_clean = re.sub(r"^doi:\s*", "", doi_clean, flags=re.IGNORECASE)
                return doi_clean.strip().lower()
    return None


def extract_fallback_url(summary: Dict[str, Any], group: Dict[str, Any] | None = None) -> str | None:
    """Extract alternative URL from summary url field or external-ids."""
    url_obj = summary.get("url")
    if isinstance(url_obj, dict):
        val = url_obj.get("value")
        if val and isinstance(val, str) and val.strip():
            return val.strip()

    # Check external-id URLs in summary and group
    containers = [summary.get("external-ids")]
    if group and isinstance(group, dict):
        containers.append(group.get("external-ids"))

    for container in containers:
        if not container or not isinstance(container, dict):
            continue
        for ext_id in container.get("external-id") or []:
            if not ext_id or not isinstance(ext_id, dict):
                continue
            ext_url_obj = ext_id.get("external-id-url")
            if isinstance(ext_url_obj, dict):
                ext_url = ext_url_obj.get("value")
                if ext_url and isinstance(ext_url, str) and ext_url.strip():
                    return ext_url.strip()
            # If the external-id itself is a URL
            id_type = ext_id.get("external-id-type")
            if id_type and str(id_type).lower() in ("uri", "url"):
                id_val = ext_id.get("external-id-value")
                if id_val and isinstance(id_val, str) and id_val.strip().startswith("http"):
                    return id_val.strip()
    return None


def assemble_doi_url(doi: Optional[str]) -> Optional[str]:
    """Assemble a standard HTTPS DOI URL from a DOI string."""
    if not doi or not isinstance(doi, str):
        return None
    clean = doi.strip()
    clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"^doi:\s*", "", clean, flags=re.IGNORECASE).strip()
    return f"https://doi.org/{clean}" if clean else None


def get_publication_url(pub: Dict[str, Any]) -> Optional[str]:
    """Assemble publication URL using DOI if present, falling back to url field."""
    doi = pub.get("doi")
    if doi:
        assembled = assemble_doi_url(doi)
        if assembled:
            return assembled
    return pub.get("url")


def select_best_summary(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Select the preferred work summary in a group (display-index 0), or the first."""
    if not summaries:
        return {}
    for s in summaries:
        if str(s.get("display-index", "")).strip() == "0":
            return s
    return summaries[0]


def fetch_member_works(orcid_id: str, cache_dir: str = "data/cache") -> List[Dict[str, Any]]:
    """Retrieve all work summaries for an individual ORCID record, with offline cache support."""
    url = f"{ORCID_API_BASE}/{orcid_id}/works"
    data = None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if cache_dir:
                try:
                    os.makedirs(cache_dir, exist_ok=True)
                    cache_file = os.path.join(cache_dir, f"{orcid_id}.json")
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                except OSError:
                    pass
        else:
            print(f"Warning: Failed to fetch {orcid_id} (HTTP {resp.status_code})")
    except requests.RequestException as e:
        print(f"Warning: Network error fetching {orcid_id}: {e}")

    # Fallback to local cache if network response not available
    if not data and cache_dir:
        cache_file = os.path.join(cache_dir, f"{orcid_id}.json")
        if os.path.isfile(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"Loaded cached records for {orcid_id}")
            except Exception as e:
                print(f"Warning: Could not read cache for {orcid_id}: {e}")

    if not data:
        return []

    group_items = data.get("group") or []
    records = []

    for group in group_items:
        # Each group contains one or more work summaries (usually versions of the same work)
        summaries = group.get("work-summary") or []
        if not summaries:
            continue

        summary = select_best_summary(summaries)

        # Extract title (fallback across summaries if preferred lacks one)
        title = None
        for s in [summary] + summaries:
            title_obj = s.get("title")
            if isinstance(title_obj, dict):
                inner_title = title_obj.get("title")
                if isinstance(inner_title, dict):
                    val = inner_title.get("value")
                    if val and isinstance(val, str) and val.strip():
                        title = val.strip()
                        break
        if not title:
            continue

        # Extract publication year (fallback across summaries)
        year = None
        for s in [summary] + summaries:
            pub_date = s.get("publication-date")
            if isinstance(pub_date, dict):
                year_obj = pub_date.get("year")
                if isinstance(year_obj, dict):
                    y_val = year_obj.get("value")
                    if y_val and str(y_val).strip():
                        year = str(y_val).strip()
                        break
        if not year:
            year = "Unknown"

        # Extract journal / publication venue (fallback across summaries)
        venue = None
        for s in [summary] + summaries:
            journal_obj = s.get("journal-title")
            if isinstance(journal_obj, dict):
                j_val = journal_obj.get("value")
                if j_val and isinstance(j_val, str) and j_val.strip():
                    venue = j_val.strip()
                    break

        # Extract DOI (check summary, all summaries, and group)
        doi = extract_doi(summary.get("external-ids"))
        if not doi:
            for s in summaries:
                doi = extract_doi(s.get("external-ids"))
                if doi:
                    break
        if not doi:
            doi = extract_doi(group.get("external-ids"))

        # URL: assemble using DOI if available, or fall back to alternative URL
        work_url = assemble_doi_url(doi) or extract_fallback_url(summary, group)

        records.append({
            "title": title,
            "year": year,
            "journal": venue,
            "doi": doi,
            "url": work_url,
            "type": summary.get("type") or "other",
        })

    return records


def normalize_title(title: str) -> str:
    """Normalize title for fuzzy comparison during deduplication."""
    return re.sub(r"\W+", "", title.lower())


def aggregate_publications(
    orcids: Sequence[str] | Dict[str, str] | None = None,
    cache_dir: str = "data/cache",
) -> List[Dict[str, Any]]:
    """Fetch and deduplicate publications across all researchers with author tracking."""
    if orcids is None:
        mapping = ORCID_IDS
    elif isinstance(orcids, dict):
        mapping = orcids
    else:
        mapping = {o: ORCID_IDS.get(o, o) for o in orcids}

    deduped: List[Dict[str, Any]] = []
    doi_map: Dict[str, Dict[str, Any]] = {}
    title_map: Dict[str, Dict[str, Any]] = {}

    for orcid, author_name in mapping.items():
        works = fetch_member_works(orcid, cache_dir=cache_dir)
        for work in works:
            doi = work.get("doi")
            norm_title = normalize_title(work["title"])

            existing = None
            if doi and doi in doi_map:
                existing = doi_map[doi]
            elif norm_title in title_map:
                existing = title_map[norm_title]

            if existing:
                # Merge author tracking across group members
                if author_name and author_name not in existing.setdefault("authors", []):
                    existing["authors"].append(author_name)
                if orcid and orcid not in existing.setdefault("orcids", []):
                    existing["orcids"].append(orcid)

                # Merge richer metadata if available
                if not existing.get("doi") and doi:
                    existing["doi"] = doi
                    doi_map[doi] = existing
                if existing.get("doi"):
                    existing["url"] = assemble_doi_url(existing["doi"])
                elif not existing.get("url") and work.get("url"):
                    existing["url"] = work["url"]
                if not existing.get("journal") and work.get("journal"):
                    existing["journal"] = work["journal"]
                if existing.get("year") == "Unknown" and work.get("year") != "Unknown":
                    existing["year"] = work["year"]
            else:
                work_copy = dict(work)
                if work_copy.get("doi"):
                    work_copy["url"] = assemble_doi_url(work_copy["doi"])
                work_copy["authors"] = [author_name] if author_name else []
                work_copy["orcids"] = [orcid] if orcid else []
                deduped.append(work_copy)
                if doi:
                    doi_map[doi] = work_copy
                if norm_title:
                    title_map[norm_title] = work_copy

    # Sort descending by year (Unknowns at the end), then alphabetically by title
    def sort_key(item):
        yr = item["year"]
        year_num = int(yr) if str(yr).isdigit() else 0
        return (-year_num, item.get("title", "").lower())

    return sorted(deduped, key=sort_key)


def generate_markdown(
    publications: List[Dict[str, Any]],
    output_path: str = "PUBLICATIONS.md",
    last_updated: Optional[str] = None,
):
    """Write grouped publications by year to Markdown."""
    if last_updated is None:
        last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        "# Group Publications",
        "",
        "*Auto-generated via ORCID Public API*",
        f"*Last updated: {last_updated}*",
    ]

    current_year = None
    for pub in publications:
        year = pub["year"]
        if year != current_year:
            current_year = year
            lines.extend(["", f"## {current_year}", ""])

        target_url = get_publication_url(pub)
        title_str = f"**[{pub['title']}]({target_url})**" if target_url else f"**{pub['title']}**"
        venue_str = f" *{pub['journal']}*." if pub.get("journal") else ""
        doi_str = f" [DOI: {pub['doi']}](https://doi.org/{pub['doi']})" if pub.get("doi") else ""

        lines.append(f"- {title_str}{venue_str}{doi_str}")

    lines.extend([
        "",
        "---",
        "",
        "Copyright (c) 2026, Alin M. Elena and contributors. Released under the [BSD 3-Clause License](LICENSE).",
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")
    print(f"Generated {output_path} with {len(publications)} publications.")


def export_json(publications: List[Dict[str, Any]], output_path: str = "publications.json"):
    """Export publications list to JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(publications)} publications to {output_path}")


def main():
    """Fetch publications data from ORCID API and export to JSON/Markdown."""
    parser = argparse.ArgumentParser(
        description="Fetch and aggregate publications for DDMMS research group members using ORCID API."
    )
    parser.add_argument(
        "orcids",
        nargs="*",
        default=None,
        help="ORCID IDs to fetch (optional positional args). Overrides or filters CSV/YAML members.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="PUBLICATIONS.md",
        help="Output Markdown file path (default: PUBLICATIONS.md)",
    )
    parser.add_argument(
        "--authors",
        "--authors-yaml",
        "--authors-csv",
        "--csv",
        dest="authors_path",
        default=DEFAULT_AUTHORS_PATH,
        help="Path to YAML or CSV containing author ORCID mappings (default: data/authors.yaml)",
    )
    parser.add_argument(
        "--orcids",
        nargs="+",
        dest="flag_orcids",
        help="List of ORCID IDs to fetch (overrides file configuration)",
    )
    parser.add_argument(
        "--json",
        default="publications.json",
        help="Output JSON file path (default: publications.json)",
    )
    parser.add_argument(
        "--cache-dir",
        default="data/cache",
        help="Directory to cache ORCID API responses (default: data/cache)",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Skip exporting JSON",
    )
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Skip exporting Markdown bibliography",
    )
    args = parser.parse_args()

    # Determine orcid mapping
    if args.authors_path and os.path.isfile(args.authors_path):
        if args.authors_path.lower().endswith((".yaml", ".yml")):
            orcid_dict = load_orcids_from_yaml(args.authors_path)
        else:
            orcid_dict = load_orcids_from_csv(args.authors_path)
    else:
        orcid_dict = ORCID_IDS

    selected_orcids = args.flag_orcids or (args.orcids if args.orcids else None)
    if selected_orcids:
        orcids_input = selected_orcids
        orcid_dict = {o: orcid_dict.get(o, o) for o in selected_orcids}
    else:
        orcids_input = orcid_dict

    print(f"Fetching / reading publications for {len(orcid_dict)} author(s)...")
    pubs = aggregate_publications(orcids_input, cache_dir=args.cache_dir)

    if not pubs:
        print("Warning: No publications found or fetched.")
    else:
        print(f"Aggregated {len(pubs)} unique publication records.")

    # Write Markdown
    if not args.no_markdown and args.output:
        generate_markdown(pubs, output_path=args.output)

    # Write JSON
    if not args.no_json and args.json:
        export_json(pubs, output_path=args.json)

    print("Publications data synchronization complete!")
    print("To generate or rebuild the website pages, run: python src/build_site.py")


if __name__ == "__main__":
    main()
