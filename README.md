# Building the DDMMS Website

Instructions to build and serve the static website locally using [uv](https://docs.astral.sh/uv/).

## Build Instructions

### 1. Full Build (Fetch Publications & Generate Site)

Fetch latest publication records from ORCID and rebuild all HTML pages, Markdown bibliography, and JSON feeds:

```bash
uv run --with requests python src/pubs.py
```

### 2. Fast Build (Regenerate HTML Pages from Local Data)

Rebuild all HTML pages (`index.html`, `publications.html`, `people.html`, `research.html`, `code.html`) using existing local data without querying the ORCID API:

```bash
uv run python src/build_site.py
```

## Preview Locally

Serve the repository root using Python's built-in HTTP server:

```bash
uv run python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.
