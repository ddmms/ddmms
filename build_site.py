#!/usr/bin/env python3
"""Site generator for Data Driven Materials and Molecular Science (DDMMS) website.

Generates responsive, accessible separate HTML pages with shared navigation,
light/dark theme toggle, logo integration, and publications system.
"""

import csv
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLICATIONS_FILE = BASE_DIR / "publications.json"
AUTHORS_FILE = BASE_DIR / "data" / "authors.csv"
FOOTER_FILE = BASE_DIR / "footer.html"
INCLUDES_FOOTER_FILE = BASE_DIR / "_includes" / "footer.html"


def load_data():
    pubs = []
    if PUBLICATIONS_FILE.exists():
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            pubs = json.load(f)

    authors = {
        "0000-0002-7013-6670": "Alin Marin Elena",
        "0009-0005-2015-9478": "Elliott Kasoar",
        "0000-0001-7374-9352": "Junwen Yin",
    }
    if AUTHORS_FILE.exists():
        with open(AUTHORS_FILE, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith("#") or row[0].lower() in ("orcid", "id"):
                    continue
                if len(row) >= 2:
                    authors[row[0].strip()] = row[1].strip()

    return pubs, authors


def get_header(active_page="home"):
    """Return the reusable site header container.

    Individual HTML pages reuse the separate header.html file directly,
    eliminating duplicate header markup across pages.
    """
    return '  <div id="site-header" data-include-header></div>'


def get_footer():
    """Return the reusable site footer container.

    Individual HTML pages reuse the separate footer.html file directly,
    eliminating duplicate footer markup across pages.
    """
    return '  <div id="site-footer" data-include-footer></div>'


def generate_index_html(pubs=None, authors=None):
    header_html = get_header("index")
    footer_html = get_footer()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Mission, background, and methodology of the Data Driven Materials and Molecular Science group at STFC Daresbury Laboratory, UKRI.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          Uniting statistical physics, quantum mechanics, and artificial intelligence to explore matter at the atomic level.
        </p>
      </div>

      <div class="about-grid">
        <div class="about-text">
          <h3>The Group Mission</h3>
          <p>
            The <strong>Data Driven Materials and Molecular Science (DDMMS)</strong> group is hosted within the Scientific Computing Department (SCD) of the Science and Technology Facilities Council (STFC), part of UK Research and Innovation (UKRI), based at Sci-Tech Daresbury.
          </p>
          <p>
            Computational materials science has long faced a fundamental trade-off: high-accuracy quantum mechanical calculations (such as density functional theory and post-Hartree-Fock) are computationally expensive and limited to small systems, whereas classical empirical force fields scale to millions of atoms but suffer from fixed functional forms and limited chemical transferability.
          </p>
          <p>
            Our core mission is to eliminate this trade-off by constructing robust, physics-informed machine-learned interatomic potentials (MLIPs), creating automated calculation workflows, and running extreme-scale simulations on high-performance computing facilities.
          </p>


        </div>

        <div class="about-sidebar">
          <div class="news-box" style="margin-bottom: 1.5rem;">
            <h3 class="news-box-title"><span>📢</span> Recent Highlights &amp; News</h3>
            <ul class="news-list">
              <li class="news-item">
                <div class="news-date">2026 Milestone</div>
                <div class="news-headline">Roadmap for an atomistic machine-learning ecosystem published on arXiv (2609.39090).</div>
              </li>
              <li class="news-item">
                <div class="news-date">2026 Release</div>
                <div class="news-headline">Goldilocks automated k-point sampling framework for Quantum ESPRESSO published in <em>Digital Discovery</em>.</div>
              </li>
              <li class="news-item">
                <div class="news-date">2026 Discovery</div>
                <div class="news-headline">uMOF universal benchmark database and ML interatomic potentials released for metal-organic frameworks.</div>
              </li>
              <li class="news-item">
                <div class="news-date">Software Ecosystem</div>
                <div class="news-headline">aiida-mlip released, integrating janus-core workflows with full data provenance in AiiDA.</div>
              </li>
            </ul>
          </div>

          <div class="news-box">
            <h3 class="news-box-title"><span>🤝</span> Work With Us</h3>
            <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">
              We welcome prospective PhD researchers, postdocs, and international scientific visitors interested in machine-learning interatomic potentials, molecular dynamics algorithms, and porous materials.
            </p>
            <a href="people.html#contact" class="btn btn-primary" style="width: 100%;">Contact the Group</a>
          </div>
        </div>
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


def generate_code_html():
    header_html = get_header("code")
    footer_html = get_footer()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Code &amp; Software | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Open-source scientific software packages developed by DDMMS: janus-core, aiida-mlip, aiidalab-mlip, pack-mm, ml-peg, and goldilocks.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          Community-driven, well-tested, and reproducible scientific tools developed by the Data Driven Materials and Molecular Science group.
        </p>
      </div>

      <div class="code-grid" style="grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));">
        <!-- janus-core -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🪐</span> janus-core</h3>
            </div>
            <span class="badge" style="background:#dbeafe; color:#1e40af;">Python / ASE / CLI</span>
          </div>
          <p class="code-desc">
            Tools for materials modeling with machine-learned interatomic potentials (MACE, SevenNet, CHGNet, M3GNet). Provides a simple, robust CLI and Python API with full ASE calculator support.
          </p>
          <div class="code-install-box">
            <code>pip install janus-core</code>
            <button class="copy-snippet-btn" data-code="pip install janus-core" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Single-point energies, forces, stress tensors, and Hessians</li>
            <li>Geometry optimization with FrechetCellFilter and BFGS/FIRE</li>
            <li>Molecular dynamics in NVE, NVT, and NPT ensembles with thermostat/barostat logging</li>
            <li>Automated equation of state (EOS) and full 6x6 elasticity stiffness tensors ($C_{{ij}}$)</li>
            <li>Phonon band structures &amp; DOS via Phonopy integration</li>
            <li>Minimum Energy Pathways with Climbing-Image NEB</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
            <a href="https://stfc.github.io/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
            <a href="https://pypi.org/project/janus-core/" target="_blank" rel="noopener noreferrer" class="person-link-btn">PyPI</a>
          </div>
        </article>

        <!-- aiida-mlip -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🔄</span> aiida-mlip</h3>
            </div>
            <span class="badge" style="background:#fef3c7; color:#92400e;">AiiDA / Workflows</span>
          </div>
          <p class="code-desc">
            An open-source AiiDA plugin integrating the janus-core library to manage automated workflows for machine learning interatomic potentials (MLIPs) with complete data provenance.
          </p>
          <div class="code-install-box">
            <code>pip install aiida-mlip</code>
            <button class="copy-snippet-btn" data-code="pip install aiida-mlip" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Full provenance graphs recording every calculation input, output, and potential parameter</li>
            <li>Automated single-point, geometry optimization, and molecular dynamics workchains</li>
            <li>Scalable execution across local workstations and remote HPC clusters</li>
            <li>Integrates directly with the wider AiiDA simulation and materials informatics ecosystem</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/stfc/aiida-mlip" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
            <a href="https://stfc.github.io/aiida-mlip" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
            <a href="https://pypi.org/project/aiida-mlip/" target="_blank" rel="noopener noreferrer" class="person-link-btn">PyPI</a>
          </div>
        </article>

        <!-- aiidalab-mlip -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🧪</span> aiidalab-mlip</h3>
            </div>
            <span class="badge" style="background:#e0f2fe; color:#0369a1;">AiiDAlab / Web GUI</span>
          </div>
          <p class="code-desc">
            An interactive browser-based AiiDAlab application for configuring and running machine learning interatomic potential calculations with AiiDA and aiida-mlip.
          </p>
          <div class="code-install-box">
            <code>pip install aiidalab-mlip</code>
            <button class="copy-snippet-btn" data-code="pip install aiidalab-mlip" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Interactive web interface for submitting MLIP simulations without writing boilerplate code</li>
            <li>Structure loading from CIF, XYZ, and standard crystallography formats with 3D visualization</li>
            <li>Direct integration with pre-trained foundation models (MACE-MP and others)</li>
            <li>Interactive single-point energy, force evaluations, and geometry optimizations with full AiiDA provenance</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/stfc/aiidalab-mlip" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
          </div>
        </article>

        <!-- pack-mm -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>📦</span> pack-mm</h3>
            </div>
            <span class="badge" style="background:#fce7f3; color:#9d174d;">Python / Packing / CLI</span>
          </div>
          <p class="code-desc">
            A Python package and CLI for building realistic atomistic and molecular systems for materials modeling, utilizing machine-learned interatomic potentials (via janus-core) with Monte Carlo and Molecular Dynamics routines.
          </p>
          <div class="code-install-box">
            <code>pip install pack-mm</code>
            <button class="copy-snippet-btn" data-code="pip install pack-mm" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Generates realistic packed starting configurations for complex liquids, interfaces, and porous frameworks</li>
            <li>Uses janus-core for MLIP interactions, with MACE-MP foundation models enabled by default</li>
            <li>High-performance packing leveraging Monte Carlo, Molecular Dynamics, and hybrid MC/MD relaxation</li>
            <li>Full Python API and intuitive CLI with support for both CPU and CUDA GPU acceleration</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/ddmms/pack-mm" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
            <a href="https://ddmms.github.io/pack-mm" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
            <a href="https://pypi.org/project/pack-mm/" target="_blank" rel="noopener noreferrer" class="person-link-btn">PyPI</a>
          </div>
        </article>

        <!-- ml-peg -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>📊</span> ml-peg</h3>
            </div>
            <span class="badge" style="background:#e0e7ff; color:#3730a3;">Benchmark / Guide</span>
          </div>
          <p class="code-desc">
            Machine Learning Performance and Extrapolation Guide. A comprehensive benchmarking framework and interactive performance guide to evaluate MLIPs across diverse chemical systems, extrapolations, and physical observables.
          </p>
          <div class="code-install-box">
            <code>git clone https://github.com/ddmms/ml-peg.git</code>
            <button class="copy-snippet-btn" data-code="git clone https://github.com/ddmms/ml-peg.git" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Evaluates model performance beyond basic force/energy errors to actual physical stability</li>
            <li>Tests out-of-distribution generalization, extrapolation limits, and uncertainty quantification</li>
            <li>Interactive web dashboard for comparing foundation models and dataset baselines</li>
            <li>Open-source protocols for standardized community potential verification</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/ddmms/ml-peg" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
            <a href="https://ml-peg.stfc.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">Live Platform &rarr;</a>
          </div>
        </article>

        <!-- goldilocks -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🐻</span> goldilocks</h3>
            </div>
            <span class="badge" style="background:#ecfdf5; color:#065f46;">PSDI &bull; goldilocks.ac.uk</span>
          </div>
          <p class="code-desc">
            A web application and library for automated generation of input files with optimised k-point meshes for Quantum ESPRESSO self-consistent field (SCF) calculations. Developed as part of the <strong>PSDI (Physical Sciences Data Infrastructure) Data to Knowledge</strong> initiative to eliminate computational waste and improve sustainability on national supercomputers like ARCHER2.
          </p>
          <div class="code-install-box">
            <code>pip install goldilocks</code>
            <button class="copy-snippet-btn" data-code="pip install goldilocks" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Part of the UKRI PSDI Data to Knowledge national infrastructure framework</li>
            <li>Predicts "Goldilocks" k-point convergence parameters to reduce compute waste and carbon footprint</li>
            <li>Dedicated project portal hosted at <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer">goldilocks.ac.uk</a></li>
            <li>Interactive web interface deployed on Streamlit Community Cloud</li>
            <li>Peer-reviewed and published in RSC <em>Digital Discovery</em> (2026, DOI: 10.1039/d5dd00565e)</li>
          </ul>
          <div class="person-links">
            <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">goldilocks.ac.uk &rarr;</a>
            <a href="https://github.com/stfc/goldilocks" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repo &rarr;</a>
            <a href="https://goldilocks.streamlit.app" target="_blank" rel="noopener noreferrer" class="person-link-btn">Streamlit App</a>
            <a href="https://doi.org/10.1039/d5dd00565e" target="_blank" rel="noopener noreferrer" class="person-link-btn">Paper (Digital Discovery)</a>
          </div>
        </article>
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


def generate_publications_html(pubs, authors):
    header_html = get_header("publications")
    footer_html = get_footer()
    pubs_json_str = json.dumps(pubs)
    authors_json_str = json.dumps(authors)

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Publications | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Full publication catalogue for the Data Driven Materials and Molecular Science group, auto-aggregated from ORCID.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 2.5rem;">
    <div class="container" id="pubs-app-root">
      <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
        <p class="section-subtitle">
          Comprehensive, real-time bibliography aggregated via the ORCID Public API for members of Data Driven Materials and Molecular Science.
        </p>
      </div>

      <!-- Quick Metrics Summary -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Total Articles</div>
          <div id="stat-total-pubs" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">{len(pubs)}</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Group Authors</div>
          <div id="stat-authors" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">{len(authors)}</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Years Span</div>
          <div id="stat-years" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">-</div>
        </div>
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; box-shadow: var(--shadow-sm);">
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">Journals &amp; Venues</div>
          <div id="stat-venues" style="font-size: 1.85rem; font-weight: 800; color: var(--primary); margin-top: 0.2rem;">-</div>
        </div>
      </div>

      <!-- Controls Card -->
      <div class="pubs-controls-card">
        <div class="pubs-controls-grid">
          <div class="form-group">
            <label for="pub-filter-author"><span>👤</span> Filter by Author</label>
            <select id="pub-filter-author" class="form-control pub-filter-author">
              <option value="all">All Group Members</option>
            </select>
          </div>

          <div class="form-group">
            <label for="pub-filter-year"><span>📅</span> Filter by Year</label>
            <select id="pub-filter-year" class="form-control pub-filter-year">
              <option value="all">All Years</option>
            </select>
          </div>

          <div class="form-group">
            <label for="pub-filter-search"><span>🔍</span> Search Keywords</label>
            <input type="text" id="pub-filter-search" class="form-control pub-filter-search" placeholder="Title, journal, DOI, author...">
          </div>

          <div class="form-group">
            <label for="pub-filter-sort"><span>⚡</span> Sort Order</label>
            <select id="pub-filter-sort" class="form-control pub-filter-sort">
              <option value="year-desc">Year (Newest First)</option>
              <option value="year-asc">Year (Oldest First)</option>
              <option value="title-asc">Title (A - Z)</option>
            </select>
          </div>
        </div>

        <div class="pubs-controls-extra">
          <label class="checkbox-label">
            <input type="checkbox" class="pub-toggle-group-year" checked>
            <span>Group publications by year</span>
          </label>

          <button type="button" class="btn-action pub-reset-btn">
            <span>↺</span> Reset Filters
          </button>
        </div>
      </div>

      <!-- Status Bar -->
      <div class="pubs-results-bar">
        <div class="pubs-counter">
          Showing <strong class="pub-visible-count">0</strong> of <strong class="pub-total-count">{len(pubs)}</strong> publications
        </div>

        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          <a href="publications.json" download="publications.json" class="btn-action" title="Download raw JSON feed">
            <span>{{ }}</span> Download JSON
          </a>
          <a href="PUBLICATIONS.md" class="btn-action" title="View Markdown bibliography">
            <span>📄</span> View Markdown
          </a>
        </div>
      </div>

      <!-- Publication Cards List -->
      <div class="pubs-container"></div>
    </div>
  </main>

{footer_html}

  <script id="publications-data" type="application/json">
{pubs_json_str}
  </script>
  <script id="authors-data" type="application/json">
{authors_json_str}
  </script>

  <script src="assets/js/main.js"></script>
  <script src="assets/js/publications.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      window.initPublications('pubs-app-root');
    }});
  </script>
</body>
</html>"""
    return content


def generate_about_html():
    return generate_index_html()


def generate_people_html():
    header_html = get_header("people")
    footer_html = get_footer()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>People | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Meet the researchers, developers, former members, collaborators, and visitors in the Data Driven Materials and Molecular Science group.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
        <p class="section-subtitle">
          Our team comprises specialists in theoretical condensed matter physics, computational chemistry, software architecture, and AI for science.
        </p>
      </div>

      <!-- Quick Section Navigation -->
      <nav class="subnav-pills" aria-label="People page quick navigation">
        <a href="#core-team" class="subnav-pill">Core Team</a>
        <a href="#former-members" class="subnav-pill">Former Members</a>
        <a href="#collaborators" class="subnav-pill">Collaborators</a>
        <a href="#visitors" class="subnav-pill">Visitors</a>
        <a href="#contact" class="subnav-pill">Join Us</a>
      </nav>

      <!-- Core Team Section -->
      <section id="core-team" style="margin-bottom: 4rem;">
        <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
          <h2 class="section-title" style="font-size: 1.85rem;">Core Members</h2>
          <p class="section-subtitle">
            Researchers and computational scientists leading DDMMS programs at STFC Daresbury Laboratory.
          </p>
        </div>

        <div class="people-grid">
          <!-- Dr. Alin Marin Elena -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">
                <img src="assets/images/alin_elena.jpg" alt="Dr. Alin Marin Elena">
              </div>
              <div class="person-title-wrap">
                <h3>Dr. Alin Marin Elena</h3>
                <div class="person-role">Group Leader &bull; Principal Computational Scientist</div>
                <div class="person-affiliation">STFC SCD, UKRI | CCP5 Scientific Secretary</div>
              </div>
            </div>
            <p class="person-bio">
              Alin leads the Data Driven Materials and Molecular Science research group. His work centres on multiscale molecular dynamics algorithms, the architecture and scalable parallelisation of DL_POLY 5, physics-informed machine learning, and transport properties in complex liquids and molten salts.
            </p>
            <div class="person-tags">
              <span class="person-tag">ML Interatomic Potentials</span>
              <span class="person-tag">Molecular Dynamics</span>
              <span class="person-tag">DL_POLY 5</span>
              <span class="person-tag">Molten Salts</span>
              <span class="person-tag">High Performance Computing</span>
            </div>
            <div class="person-links">
              <a href="https://orcid.org/0000-0002-7013-6670" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                <svg viewBox="0 0 256 256" style="fill:#a6ce39;"><path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/><path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/></svg>
                <span>ORCID</span>
              </a>
              <a href="https://github.com/alin-elena" target="_blank" rel="noopener noreferrer" class="person-link-btn">
                <span>GitHub</span>
              </a>
              <a href="publications.html?author=Alin%20Marin%20Elena" class="person-link-btn">
                <span>Publications</span>
              </a>
            </div>
          </article>

          <!-- Elliott Kasoar -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">
                <img src="assets/images/elliott_kasoar.jpg" alt="Elliott Kasoar">
              </div>
              <div class="person-title-wrap">
                <h3>Elliott Kasoar</h3>
                <div class="person-role">Computational Scientist &bull; Research Associate</div>
                <div class="person-affiliation">STFC SCD, UKRI</div>
              </div>
            </div>
            <p class="person-bio">
              Elliott focuses on machine learning for atomic systems, equivariant foundation architectures (MACE), training set active learning, and automated atomistic simulation workflows. He is the lead designer and developer of janus-core.
            </p>
            <div class="person-tags">
              <span class="person-tag">MACE Foundation Models</span>
              <span class="person-tag">janus-core Lead</span>
              <span class="person-tag">Active Learning</span>
              <span class="person-tag">Workflow Automation</span>
            </div>
            <div class="person-links">
              <a href="https://orcid.org/0009-0005-2015-9478" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                <svg viewBox="0 0 256 256" style="fill:#a6ce39;"><path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/><path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/></svg>
                <span>ORCID</span>
              </a>
              <a href="publications.html?author=Elliott%20Kasoar" class="person-link-btn">
                <span>Publications</span>
              </a>
            </div>
          </article>

          <!-- Dr. Junwen Yin -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">
                <img src="assets/images/junwen_yin.jpeg" alt="Dr. Junwen Yin">
              </div>
              <div class="person-title-wrap">
                <h3>Dr. Junwen Yin</h3>
                <div class="person-role">Computational Scientist &bull; Research Associate</div>
                <div class="person-affiliation">STFC SCD, UKRI</div>
              </div>
            </div>
            <p class="person-bio">
              Junwen specializes in first-principles quantum chemistry, nonadiabatic electronic transitions, extended CP2K simulations, and modeling complex catalytic and photoactive interfaces under operational environments.
            </p>
            <div class="person-tags">
              <span class="person-tag">Nonadiabatic Dynamics</span>
              <span class="person-tag">CP2K Framework</span>
              <span class="person-tag">DFT Total Energy</span>
              <span class="person-tag">Catalytic Interfaces</span>
            </div>
            <div class="person-links">
              <a href="https://orcid.org/0000-0001-7374-9352" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                <svg viewBox="0 0 256 256" style="fill:#a6ce39;"><path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/><path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/></svg>
                <span>ORCID</span>
              </a>
              <a href="publications.html?author=Junwen%20Yin" class="person-link-btn">
                <span>Publications</span>
              </a>
            </div>
          </article>
        </div>
      </section>

      <!-- Former Members (Alumni) Section -->
      <section id="former-members" style="margin-bottom: 4rem;">
        <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
          <h2 class="section-title" style="font-size: 1.85rem;">Former Members</h2>
          <p class="section-subtitle">
            Researchers, engineers, and graduate scholars who contributed to DDMMS scientific software and research initiatives.
          </p>
        </div>

        <div class="people-grid">
          <!-- Former Member Placeholder 1 (Edit or duplicate as needed) -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">FM1</div>
              <div class="person-title-wrap">
                <h3>Former Member Name</h3>
                <div class="person-role">Role / Position</div>
                <div class="person-affiliation">DDMMS &bull; STFC SCD (Years, e.g. 2022&ndash;2024)</div>
                <div class="person-badge-dest"><span>🎓</span> Now: Current Position / Destination</div>
              </div>
            </div>
            <p class="person-bio">
              Description of research topics, scientific contributions, or software packages developed while with the group.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Area</span>
              <span class="person-tag">Key Contribution</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">ORCID</a>
              <a href="#" class="person-link-btn">GitHub</a>
            </div>
          </article>

          <!-- Former Member Placeholder 2 -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">FM2</div>
              <div class="person-title-wrap">
                <h3>Former Member Name</h3>
                <div class="person-role">Role / Position</div>
                <div class="person-affiliation">DDMMS &bull; STFC SCD (Years, e.g. 2023&ndash;2025)</div>
                <div class="person-badge-dest"><span>🎓</span> Now: Current Position / Destination</div>
              </div>
            </div>
            <p class="person-bio">
              Description of research topics, scientific contributions, or software packages developed while with the group.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Area</span>
              <span class="person-tag">Key Contribution</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">ORCID</a>
              <a href="#" class="person-link-btn">GitHub</a>
            </div>
          </article>
        </div>
      </section>

      <!-- Collaborators Section -->
      <section id="collaborators" style="margin-bottom: 4rem;">
        <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
          <h2 class="section-title" style="font-size: 1.85rem;">Collaborators</h2>
          <p class="section-subtitle">
            Academic collaborators, national laboratory partners, and international consortia advancing atomistic simulation and scientific machine learning.
          </p>
        </div>

        <div class="people-grid">
          <!-- Collaborator Placeholder 1 (Edit or duplicate as needed) -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">C1</div>
              <div class="person-title-wrap">
                <h3>Collaborator Name</h3>
                <div class="person-role">Title / Role</div>
                <div class="person-affiliation">Institution / Organization</div>
              </div>
            </div>
            <p class="person-bio">
              Description of collaborative research topics, joint projects, grants, or shared software development.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Area</span>
              <span class="person-tag">Joint Project</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">Website / Profile &rarr;</a>
              <a href="#" class="person-link-btn">ORCID</a>
            </div>
          </article>

          <!-- Collaborator Placeholder 2 -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">C2</div>
              <div class="person-title-wrap">
                <h3>Collaborator Name</h3>
                <div class="person-role">Title / Role</div>
                <div class="person-affiliation">Institution / Organization</div>
              </div>
            </div>
            <p class="person-bio">
              Description of collaborative research topics, joint projects, grants, or shared software development.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Area</span>
              <span class="person-tag">Joint Project</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">Website / Profile &rarr;</a>
              <a href="#" class="person-link-btn">ORCID</a>
            </div>
          </article>

          <!-- Collaborator Placeholder 3 -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">C3</div>
              <div class="person-title-wrap">
                <h3>Collaborator Name</h3>
                <div class="person-role">Title / Role</div>
                <div class="person-affiliation">Institution / Organization</div>
              </div>
            </div>
            <p class="person-bio">
              Description of collaborative research topics, joint projects, grants, or shared software development.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Area</span>
              <span class="person-tag">Joint Project</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">Website / Profile &rarr;</a>
              <a href="#" class="person-link-btn">ORCID</a>
            </div>
          </article>
        </div>

        <!-- Institutional Partners Box -->
        <div style="margin-top: 2rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.75rem;">
          <h4 style="font-size: 1.15rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;">Partner Consortia &amp; National Initiatives</h4>
          <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1rem;">
            We collaborate closely with major national and international research networks to establish shared atomistic data standards and sustainable scientific infrastructure:
          </p>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="https://www.psdi.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">PSDI Data to Knowledge &rarr;</a>
            <a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">CCP5 (Condensed Phase Simulation) &rarr;</a>
            <a href="https://mace-docs.readthedocs.io" target="_blank" rel="noopener noreferrer" class="person-link-btn">MACE Ecosystem &rarr;</a>
            <a href="https://www.scd.stfc.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">STFC Scientific Computing Department &rarr;</a>
          </div>
        </div>
      </section>

      <!-- Visitors Section -->
      <section id="visitors" style="margin-bottom: 4rem;">
        <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
          <h2 class="section-title" style="font-size: 1.85rem;">Visitors</h2>
          <p class="section-subtitle">
            Academic visitors, guest researchers, and sabbatical fellows who have visited the group at Sci-Tech Daresbury to collaborate on atomistic simulations and machine learning.
          </p>
        </div>

        <div class="people-grid">
          <!-- Visitor Placeholder 1 (Edit or duplicate as needed) -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">V1</div>
              <div class="person-title-wrap">
                <h3>Visitor Name</h3>
                <div class="person-role">Visiting Title / Role</div>
                <div class="person-affiliation">Home Institution / Organization</div>
                <span class="person-tenure">Visiting Tenure &bull; Year(s)</span>
              </div>
            </div>
            <p class="person-bio">
              Description of collaborative research topics, joint projects, visit goals, or simulation topics explored during the visit.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Topic</span>
              <span class="person-tag">Visit Scheme / Grant</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">Website / Profile &rarr;</a>
              <a href="#" class="person-link-btn">ORCID</a>
            </div>
          </article>

          <!-- Visitor Placeholder 2 -->
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">V2</div>
              <div class="person-title-wrap">
                <h3>Visitor Name</h3>
                <div class="person-role">Visiting Title / Role</div>
                <div class="person-affiliation">Home Institution / Organization</div>
                <span class="person-tenure">Visiting Tenure &bull; Year(s)</span>
              </div>
            </div>
            <p class="person-bio">
              Description of collaborative research topics, joint projects, visit goals, or simulation topics explored during the visit.
            </p>
            <div class="person-tags">
              <span class="person-tag">Research Topic</span>
              <span class="person-tag">Visit Scheme / Grant</span>
            </div>
            <div class="person-links">
              <a href="#" class="person-link-btn">Website / Profile &rarr;</a>
              <a href="#" class="person-link-btn">ORCID</a>
            </div>
          </article>
        </div>
      </section>

      <!-- Opportunities Section -->
      <section style="margin-top: 4rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2.5rem;" id="contact">
        <div class="section-header" style="text-align: left; margin-bottom: 1.5rem; padding: 0;">
          <h2 class="section-title" style="font-size: 1.85rem;">Join the Research Group</h2>
        </div>
        <p style="color: var(--text-muted); font-size: 1.05rem; line-height: 1.7; max-width: 800px; margin-bottom: 1.5rem;">
          We are always enthusiastic to collaborate with motivated graduate students, postdoctoral researchers, and academic visitors who wish to explore machine-learned interatomic potentials, extreme-scale molecular dynamics, or materials for sustainable energy technologies.
        </p>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
          <a href="mailto:alin-marin.elena@stfc.ac.uk" class="btn btn-primary"><span>✉</span> Get in Touch via Email</a>
        </div>
      </section>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def generate_research_html():
    header_html = get_header("research")
    footer_html = get_footer()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Research areas of the Data Driven Materials and Molecular Science group: MLIPs, MOFs, molten salts, and automated workflows.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          From quantum-level potential energy surfaces to supercomputing molecular dynamics and macroscopic thermal transport.
        </p>
      </div>

      <div class="research-grid" style="grid-template-columns: 1fr; gap: 2.5rem;">
        <!-- Theme 1 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 1 &bull; Physics-Informed AI</span>
            <h2 class="research-card-title">Foundation Machine-Learned Interatomic Potentials (MLIPs)</h2>
            <p class="research-card-desc">
              Accurate modeling of chemical reactivity, phase transitions, and defect dynamics requires potential energy surfaces that respect rotational, translational, and permutational invariances. We develop and extend equivariant graph neural network potentials such as MACE, SevenNet, and CHGNet.
            </p>
            <p class="research-card-desc" style="margin-top: 0.5rem;">
              Key research topics include the incorporation of polarisable long-range electrostatics (MACE-POLAR), optimal active-learning criteria that balance coverage and model uncertainty, and cross-learning strategies connecting molecular, surface, and inorganic solid phases.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="publications.html?search=MLIP" class="btn btn-outline">Explore Related Publications &rarr;</a>
          </div>
        </article>

        <!-- Theme 2 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 2 &bull; Porous Materials</span>
            <h2 class="research-card-title">Metal-Organic Frameworks &amp; Nanoporous Networks</h2>
            <p class="research-card-desc">
              Metal-Organic Frameworks (MOFs) exhibit remarkable chemical modularity, ultra-high surface areas, and tunable mechanical properties such as negative thermal expansion (NTE). We curate the uMOF benchmark database and build dedicated ML potentials that enable high-throughput phonon calculations, thermodynamic stability screening, and gas adsorption modeling.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="publications.html?search=MOF" class="btn btn-outline">Explore Related Publications &rarr;</a>
          </div>
        </article>

        <!-- Theme 3 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 3 &bull; Liquid State &amp; Clean Energy</span>
            <h2 class="research-card-title">Complex Fluids, Molten Salts &amp; Transport Phenomena</h2>
            <p class="research-card-desc">
              Molten salts serve as critical thermal storage media and coolants in next-generation nuclear and concentrated solar energy systems. We perform molecular dynamics simulations to quantify self-diffusion, ionic conductivity, shear viscosity, and thermal conductivity from first principles, testing fundamental theoretical bounds and experimental calibrations.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="publications.html?search=salt" class="btn btn-outline">Explore Related Publications &rarr;</a>
          </div>
        </article>

        <!-- Theme 4 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 4 &bull; Autonomous Workflows</span>
            <h2 class="research-card-title">High-Throughput Simulation Workflows with janus-core &amp; aiida-mlip</h2>
            <p class="research-card-desc">
              Bridging the gap between interatomic potentials and scientific discovery requires seamless automation. With janus-core and the aiida-mlip plugin, we provide unified pipelines with full data provenance for geometry relaxation (BFGS, FIRE, FrechetCellFilter), equation of state fitting, full 6x6 elasticity stiffness tensors ($C_{{ij}}$), and climbing image nudged elastic band (CI-NEB) minimum energy pathways.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="code.html" class="btn btn-primary">Read Software Documentation &rarr;</a>
          </div>
        </article>

        <!-- Theme 5 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 5 &bull; PSDI Data to Knowledge</span>
            <h2 class="research-card-title">Sustainable DFT &amp; k-Point Optimization (Goldilocks)</h2>
            <p class="research-card-desc">
              Computational electronic structure calculations represent a major fraction of workloads on national supercomputing services like ARCHER2. In collaboration with the <strong>PSDI (Physical Sciences Data Infrastructure) Data to Knowledge</strong> initiative, we develop <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer"><strong>Goldilocks</strong> (goldilocks.ac.uk)</a> to predict optimal, sustainable k-point convergence parameters for Quantum ESPRESSO self-consistent field (SCF) calculations.
            </p>
            <p class="research-card-desc" style="margin-top: 0.5rem;">
              By balancing numerical accuracy with computational efficiency—never under-converged, never computationally wasteful—Goldilocks eliminates compute and electricity waste while preserving target accuracy. Peer-reviewed in RSC <em>Digital Discovery</em> (2026, DOI: 10.1039/d5dd00565e).
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer" class="btn btn-primary">goldilocks.ac.uk &rarr;</a>
            <a href="https://github.com/stfc/goldilocks" target="_blank" rel="noopener noreferrer" class="btn btn-outline">GitHub &rarr;</a>
            <a href="code.html" class="btn btn-outline">Explore in Software &rarr;</a>
          </div>
        </article>

        <!-- Theme 6 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 6 &bull; MLIP Benchmarking &amp; Validation</span>
            <h2 class="research-card-title">Machine Learning Performance and Extrapolation Guide (ML-PEG)</h2>
            <p class="research-card-desc">
              Evaluating machine-learned interatomic potentials requires going beyond simple training force and energy RMSE errors to evaluate true physical stability, phase behavior, and uncertainty quantification. The <strong>ML-PEG</strong> benchmarking platform establishes rigorous evaluation protocols to stress-test MLIPs across diverse chemical systems, out-of-distribution scenarios, and extrapolation limits.
            </p>
            <p class="research-card-desc" style="margin-top: 0.5rem;">
              Alongside standardized community benchmarks, ML-PEG provides an interactive web dashboard for transparently comparing foundation models and dataset baselines across materials discovery tasks.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="https://ml-peg.stfc.ac.uk" target="_blank" rel="noopener noreferrer" class="btn btn-primary">ml-peg.stfc.ac.uk &rarr;</a>
            <a href="https://github.com/ddmms/ml-peg" target="_blank" rel="noopener noreferrer" class="btn btn-outline">GitHub &rarr;</a>
            <a href="code.html" class="btn btn-outline">Explore in Software &rarr;</a>
          </div>
        </article>
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


def main():
    print("Loading publications and authors...")
    pubs, authors = load_data()
    print(f"Loaded {len(pubs)} publications and {len(authors)} authors.")

    pages = {
        "index.html": generate_index_html(pubs, authors),
        "publications.html": generate_publications_html(pubs, authors),
        "people.html": generate_people_html(),
        "research.html": generate_research_html(),
        "code.html": generate_code_html(),
    }

    for filename, content in pages.items():
        out_path = BASE_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filename} ({len(content)} bytes)")

    print("Site generation complete!")


if __name__ == "__main__":
    main()
