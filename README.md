# Building the DDMMS Website

Instructions to build and serve the static website locally using [uv](https://docs.astral.sh/uv/).

## Build Instructions

### 1. Fetch Publications

Fetch the latest publication records from ORCID and write them to `publications.json` and `PUBLICATIONS.md`. This step does **not** generate HTML pages. Run it on first setup and whenever you want to refresh the publication list:

```bash
uv run --with requests --with pyyaml python src/pubs.py
```

### 2. Generate HTML Pages

Build all HTML pages from local data (including `publications.json`). Always run this step, including after step 1:

```bash
uv run --with pyyaml python src/build_site.py
```

## Preview Locally

Serve the repository root using Python's built-in HTTP server:

```bash
uv run python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.
