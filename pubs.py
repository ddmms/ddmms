#!/usr/bin/env python3
"""Pubs - Aggregate research publications from ORCID API and generate website.

Copyright (c) 2026, Alin M. Elena and contributors
Distributed under the terms of the BSD 3-Clause License.
"""
import argparse
import os
import sys
from pathlib import Path

# Add src to sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pubs import (
    DEFAULT_CSV_PATH,
    ORCID_IDS,
    aggregate_publications,
    export_json,
    generate_markdown,
    load_orcids_from_csv,
)

import build_site


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate publications for DDMMS research group members using ORCID API."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="PUBLICATIONS.md",
        help="Output Markdown file path (default: PUBLICATIONS.md)",
    )
    parser.add_argument(
        "--csv",
        "--authors-csv",
        dest="authors_csv",
        default=DEFAULT_CSV_PATH,
        help="Path to CSV containing 'orcid,name' mappings (default: data/authors.csv)",
    )
    parser.add_argument(
        "--orcids",
        nargs="+",
        help="List of ORCID IDs to fetch (overrides CSV configuration)",
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
        "--no-site",
        action="store_true",
        help="Skip rebuilding website HTML pages",
    )
    args = parser.parse_args()

    # Determine orcid mapping
    if args.authors_csv and os.path.isfile(args.authors_csv):
        orcid_dict = load_orcids_from_csv(args.authors_csv)
    else:
        orcid_dict = ORCID_IDS

    if args.orcids:
        orcids_input = args.orcids
        orcid_dict = {o: orcid_dict.get(o, o) for o in args.orcids}
    else:
        orcids_input = orcid_dict

    print(f"Fetching / reading publications for {len(orcid_dict)} author(s)...")
    pubs = aggregate_publications(orcids_input, cache_dir=args.cache_dir)

    if not pubs:
        print("Warning: No publications found or fetched.")
    else:
        print(f"Aggregated {len(pubs)} unique publication records.")

    # Write Markdown
    if args.output:
        generate_markdown(pubs, output_path=args.output)

    # Write JSON
    if args.json:
        export_json(pubs, output_path=args.json)

    # Rebuild website
    if not args.no_site:
        print("Rebuilding website pages...")
        build_site.main()

    print("All tasks completed successfully!")


if __name__ == "__main__":
    main()

