# Data Driven Materials and Molecular Science (DDMMS)

Welcome to the official website repository for the **Data Driven Materials and Molecular Science (DDMMS)** research group at the **Science and Technology Facilities Council (STFC)** Scientific Computing Department, **UK Research and Innovation (UKRI)**, Sci-Tech Daresbury.

---

## 🌟 Overview & Key Features

- **Comprehensive Navigation Menu**:
  - **About**: Group mission, scientific philosophy, methodological pillars, and news milestones.
  - **People**: Detailed researcher profiles (Dr. Alin Marin Elena, Elliott Kasoar, Dr. Junwen Yin), research tags, ORCID IDs, and open positions.
  - **Research**: In-depth coverage of core themes (Foundation MLIPs, Metal-Organic Frameworks, Complex Fluids & Molten Salts, DL_POLY 5 Massively Parallel MD, and Automated Atomistic Workflows).
  - **Publications**: Full interactive catalog integrated from the group's ORCID automated aggregation pipeline (`../pubs`), featuring live text search, author filtering, year filtering, sorting, BibTeX generation, citation copying, and DOI links.
  - **Code**: Showcase of open-source packages (`janus-core`, `FTorch`, `DL_POLY 5`, `uMOF`, `pubs`) with quick copy installation commands and links to repositories.
- **Adaptive Dark / Light Themes**:
  - Dynamically toggles logos between `ddmms_for_light_modes` and `ddmms_for_dark_modes` for pixel-perfect contrast.
  - Persists preference via `localStorage` and respects system `prefers-color-scheme`.
- **100% Mobile Friendly & Responsive**:
  - Fluid typography and responsive CSS grid/flexbox layouts.
  - Mobile hamburger drawer navigation with touch-friendly 44px+ hit targets.
  - Full support for mobile phones, tablets, laptops, and ultra-wide displays.
- **Offline & Standalone Ready**:
  - Publication dataset is directly embedded into the HTML pages alongside JSON export files.
  - Functions completely offline or when opened via local `file://` protocol, as well as on any static web host (GitHub Pages, Netlify, Nginx, Apache).

---

## 📂 Project Structure

```text
.
├── index.html              # Responsive homepage with all sections, hero & live widgets
├── about.html              # Dedicated About page
├── people.html             # Dedicated People & team page
├── research.html           # Dedicated Research themes page
├── publications.html       # Dedicated Publications portal
├── code.html               # Dedicated Software & tools page
├── build_site.py           # Site generator synchronizing shared navigation & data
├── publications.json       # Canonical publications dataset (ORCID aggregated)
├── PUBLICATIONS.md          # Generated Markdown bibliography
├── data/
│   └── authors.csv         # Group member ORCID IDs and names mapping
├── assets/
│   ├── css/
│   │   └── style.css       # Responsive, dark/light themed CSS design system
│   ├── js/
│   │   ├── main.js         # Theme toggle, mobile drawer navigation, utilities
│   │   └── publications.js # Interactive publication filtering, search, & BibTeX
│   └── logos/              # Official DDMMS vector SVGs and PNG logos
└── tests/
    └── test_site.py        # Automated test suite
```

---

## 🚀 Running Locally

You can open `index.html` directly in any web browser, or serve it locally with Python:

```bash
# Serve current directory at http://localhost:8000
python3 -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 🔄 Updating Publications & Automatic Deployment

### Syncing Publications via ORCID

To sync publications directly from the ORCID API, regenerate data, and rebuild all pages:

```bash
python pubs.py
```

Options:
- `--csv data/authors.csv`: Custom path to author mapping CSV
- `--cache-dir data/cache`: Directory caching ORCID API responses
- `-o PUBLICATIONS.md`: Output Markdown bibliography
- `--json publications.json`: Output JSON feed
- `--no-site`: Skip updating HTML site files

### Automated GitHub Actions Deployment

The repository includes a GitHub Actions workflow in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) that:
1. Runs automatically on every `push` to `main` / `master`.
2. Runs on a scheduled weekly cron (`0 5 * * 1`, every Monday morning) to sync publications from ORCID.
3. Can be triggered manually via `workflow_dispatch`.
4. Runs `python pubs.py` to aggregate records and rebuild the site.
5. Runs the unit test suite (`python -m unittest discover tests`).
6. Commits any updated publications data back to the repository.
7. Deploys the static site to GitHub Pages.

---

## 🧪 Testing

Run all unit tests:

```bash
python -m unittest discover tests
```

---

## 📜 License

Distributed under the terms of the BSD 3-Clause License.
Copyright (c) 2026 Data Driven Materials and Molecular Science (DDMMS) & contributors.

