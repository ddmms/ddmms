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
    pages = [
        ("about", "About", "about.html"),
        ("people", "People", "people.html"),
        ("research", "Research", "research.html"),
        ("publications", "Publications", "publications.html"),
        ("code", "Code", "code.html"),
    ]

    nav_items_desktop = []
    nav_items_mobile = []

    for key, label, page_url in pages:
        is_active = (active_page == key)
        active_cls = ' class="active"' if is_active else ''

        nav_items_desktop.append(f'<li class="nav-item"><a href="{page_url}"{active_cls}>{label}</a></li>')
        nav_items_mobile.append(f'<li class="mobile-nav-item"><a href="{page_url}"{active_cls}><span>{label}</span><span>→</span></a></li>')

    desktop_nav_html = "\n        ".join(nav_items_desktop)
    mobile_nav_html = "\n        ".join(nav_items_mobile)

    home_href = "index.html"

    return f"""  <header class="site-header" id="top">
    <div class="container header-container">
      <a href="{home_href}" class="brand-link" aria-label="DDMMS Home">
        <img id="site-logo" class="brand-logo-img" src="assets/logos/ddmms_for_light_modes.svg" alt="Data Driven Materials and Molecular Science">
        <div class="brand-text-block">
          <span class="brand-title-main">DDMMS</span>
          <span class="brand-title-sub">Data Driven Materials &amp; Molecular Science</span>
        </div>
      </a>

      <nav class="nav-desktop" aria-label="Primary Navigation">
        <ul class="nav-links">
        {desktop_nav_html}
        </ul>
      </nav>

      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" aria-label="Toggle Dark/Light Mode" title="Toggle theme">
          <svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0012.3 2zm-.3 18a8 8 0 110-16 8.3 8.3 0 011.7.2 8 8 0 00-1.9 7.8 8 8 0 007.8 8c-.5 0-1.1 0-1.6-.0z"/></svg>
        </button>

        <button type="button" class="mobile-toggle-btn" aria-label="Open Navigation Menu" aria-expanded="false" aria-controls="mobile-drawer">
          <span class="hamburger-icon">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </span>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <div class="mobile-drawer" id="mobile-drawer">
      <ul class="mobile-nav-links">
        {mobile_nav_html}
      </ul>
      <div class="mobile-actions">
        <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">Theme Appearance</span>
        <button type="button" class="theme-toggle-btn" aria-label="Toggle theme">
          <svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0012.3 2zm-.3 18a8 8 0 110-16 8.3 8.3 0 011.7.2 8 8 0 00-1.9 7.8 8 8 0 007.8 8c-.5 0-1.1 0-1.6-.0z"/></svg>
        </button>
      </div>
    </div>
  </header>"""


def get_footer():
    return """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <h4>Data Driven Materials and Molecular Science</h4>
          <p>Accelerating atomistic discovery through physics-informed machine learning, multiscale molecular simulation, and open-source scientific workflows.</p>
        </div>

        <div class="footer-col">
          <h5>Navigation</h5>
          <ul class="footer-links">
            <li><a href="about.html">About Us</a></li>
            <li><a href="people.html">People</a></li>
            <li><a href="research.html">Research Themes</a></li>
            <li><a href="publications.html">Publications</a></li>
            <li><a href="code.html">Code &amp; Software</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Affiliations</h5>
          <ul class="footer-links">
            <li><a href="https://www.scd.stfc.ac.uk" target="_blank" rel="noopener noreferrer">STFC SCD</a></li>
            <li><a href="https://www.ukri.org" target="_blank" rel="noopener noreferrer">UKRI</a></li>
            <li><a href="https://www.psdi.ac.uk" target="_blank" rel="noopener noreferrer">PSDI Data to Knowledge</a></li>
            <li><a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer">CCP5</a></li>
            <li><a href="https://sci-techdaresbury.com" target="_blank" rel="noopener noreferrer">Sci-Tech Daresbury</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Software &amp; Feeds</h5>
          <ul class="footer-links">
            <li><a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer">janus-core</a></li>
            <li><a href="https://github.com/stfc/aiida-mlip" target="_blank" rel="noopener noreferrer">aiida-mlip</a></li>
            <li><a href="https://ml-peg.stfc.ac.uk" target="_blank" rel="noopener noreferrer">ml-peg</a></li>
            <li><a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer">goldilocks.ac.uk</a></li>
            <li><a href="publications.json" download="publications.json">publications.json</a></li>
            <li><a href="PUBLICATIONS.md" target="_blank">PUBLICATIONS.md</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <span>&copy; 2026 Data Driven Materials and Molecular Science (DDMMS). Licensed under BSD-3-Clause.</span>
        <span>Sci-Tech Daresbury &bull; Warrington &bull; United Kingdom</span>
      </div>
    </div>
  </footer>
  <div class="toast" id="toast" role="alert" aria-live="polite"></div>"""


def generate_index_html(pubs, authors):
    header_html = get_header("home")
    footer_html = get_footer()

    # Get sample latest publications
    recent_pubs = pubs[:4]
    recent_pubs_html = []
    for p in recent_pubs:
        url = p.get("url") or (f"https://doi.org/{p['doi']}" if p.get("doi") else None)
        title_content = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{p["title"]}</a>' if url else p["title"]
        authors_str = ", ".join(p.get("authors", []))
        venue_str = f" <em>{p['journal']}</em>" if p.get("journal") else ""
        doi_badge = f'<a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener noreferrer" class="badge badge-doi">DOI: {p["doi"]}</a>' if p.get("doi") else ""

        recent_pubs_html.append(f"""          <article class="pub-card" style="padding: 1.15rem;">
            <h4 class="pub-title" style="font-size: 1rem;">{title_content}</h4>
            <div class="pub-meta">
              <span style="font-weight: 600; color: var(--text);">{authors_str}</span>
              <span class="badge badge-year">{p.get("year", "2026")}</span>
              <span class="pub-venue">{venue_str}</span>
              {doi_badge}
            </div>
          </article>""")
    recent_pubs_rendered = "\n".join(recent_pubs_html)

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Data Driven Materials and Molecular Science | DDMMS</title>
  <meta name="description" content="Data Driven Materials and Molecular Science (DDMMS) research group at STFC Daresbury Laboratory, UKRI. Machine learning interatomic potentials, multiscale molecular dynamics, and materials discovery.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header_html}

  <main id="main-content">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container hero-grid">
        <div class="hero-content">
          <div class="hero-badge">
            <span class="pulse-dot"></span>
            <span>STFC &bull; UKRI &bull; PSDI Data to Knowledge &bull; Sci-Tech Daresbury</span>
          </div>
          <h1 class="hero-title">
            <span class="gradient-text">Data Driven</span> Materials &amp; Molecular Science
          </h1>
          <p class="hero-subtitle">
            Pioneering the convergence of physics-informed machine learning, high-performance molecular dynamics, and automated workflows to decipher materials from quantum to continuum scales.
          </p>
          <div class="hero-cta-group">
            <a href="research.html" class="btn btn-primary">Explore Research Themes</a>
            <a href="code.html" class="btn btn-outline">Our Software &amp; Codes</a>
            <a href="publications.html" class="btn btn-outline">Publications ({len(pubs)})</a>
          </div>
        </div>

        <div class="hero-visual">
          <div class="hero-card-display">
            <img class="hero-card-logo" src="assets/logos/ddmms_for_light_modes-with-text.svg" alt="DDMMS Logo">
            <div class="hero-card-stats">
              <div class="hero-stat-item">
                <div class="hero-stat-num">{len(pubs)}+</div>
                <div class="hero-stat-label">Publications</div>
              </div>
              <div class="hero-stat-item">
                <div class="hero-stat-num">4</div>
                <div class="hero-stat-label">Core Packages</div>
              </div>
              <div class="hero-stat-item">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-label">Open Science</div>
              </div>
              <div class="hero-stat-item">
                <div class="hero-stat-num">HPC</div>
                <div class="hero-stat-label">Scale Science</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission & Overview Section -->
    <section class="section-wrapper bg-alt">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">About The Group</span>
          <h2 class="section-title">Bridging Physics, Data &amp; Molecular Engineering</h2>
          <p class="section-subtitle">
            We develop theory, computational algorithms, and scalable software to simulate complex chemical and physical phenomena with first-principles precision.
          </p>
        </div>

        <div class="about-grid">
          <div class="about-text">
            <p>
              The <strong>Data Driven Materials and Molecular Science (DDMMS)</strong> group is based at the Science and Technology Facilities Council (STFC) Scientific Computing Department at Sci-Tech Daresbury, UKRI.
            </p>
            <p>
              Our research overcomes the traditional trade-off between quantum mechanical accuracy and large-scale simulation capabilities. By creating <strong>equivariant graph neural network potentials</strong>, automated calculation workflows, and high-performance computing pipelines, we enable predictive simulation of complex materials for energy storage, catalysis, carbon capture, and quantum technologies.
            </p>

            <div class="about-pillars">
              <div class="pillar-card">
                <div class="pillar-icon">⚛</div>
                <h4 class="pillar-title">Machine Learning Potentials</h4>
                <p class="pillar-desc">Equivariant foundation models (MACE, SevenNet, CHGNet) delivering DFT fidelity across millions of atoms.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">⚡</div>
                <h4 class="pillar-title">Extreme-Scale MD</h4>
                <p class="pillar-desc">Massively parallel algorithms, GPU offloading, and symplectic statistical mechanics.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">💎</div>
                <h4 class="pillar-title">Nanoporous Materials</h4>
                <p class="pillar-desc">Metal-organic frameworks (uMOF), negative thermal expansion, phonons, and gas adsorption.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">🛠</div>
                <h4 class="pillar-title">Automated Workflows</h4>
                <p class="pillar-desc">Reproducible pipelines with janus-core, aiida-mlip, ml-peg, and goldilocks.</p>
              </div>
            </div>

            <div style="margin-top: 1.5rem;">
              <a href="about.html" class="btn btn-primary">Read More About Our Group &rarr;</a>
            </div>
          </div>

          <div class="about-sidebar">
            <div class="news-box">
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
          </div>
        </div>
      </div>
    </section>

    <!-- Research Highlights Section -->
    <section class="section-wrapper">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Research Themes</span>
          <h2 class="section-title">Core Scientific Frontiers</h2>
          <p class="section-subtitle">
            Advancing computational materials discovery across length and timescales.
          </p>
        </div>

        <div class="research-grid">
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Theme 1</span>
              <h3 class="research-card-title">Foundation ML Interatomic Potentials</h3>
              <p class="research-card-desc">
                Developing equivariant graph neural networks (MACE, SevenNet, CHGNet), polarizable electrostatics (MACE-POLAR), and active-learning training set optimization.
              </p>
            </div>
          </div>

          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Theme 2</span>
              <h3 class="research-card-title">Metal-Organic Frameworks &amp; Porous Solids</h3>
              <p class="research-card-desc">
                High-throughput screening of flexible MOF structures, negative thermal expansion (NTE) mechanics, vibrational phonon dynamics, and selective catalytic centers.
              </p>
            </div>
          </div>

          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Theme 3</span>
              <h3 class="research-card-title">Complex Fluids &amp; Molten Salts</h3>
              <p class="research-card-desc">
                Microscopic transport properties, ionic correlations, viscosity, and fundamental bounds of thermal conductivity in molten salts for green energy systems.
              </p>
            </div>
          </div>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="research.html" class="btn btn-outline">Explore All Research Programs &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Software & Codes Showcase -->
    <section class="section-wrapper bg-alt">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Software &amp; Codes</span>
          <h2 class="section-title">Open-Source Scientific Tools</h2>
          <p class="section-subtitle">
            Community-driven, FAIR-compliant software designed for reproducibility, modularity, and high-performance computing.
          </p>
        </div>

        <div class="code-grid">
          <!-- janus-core -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>🪐</span> janus-core</h3>
              </div>
              <span class="badge" style="background:#dbeafe; color:#1e40af;">Python / ASE</span>
            </div>
            <p class="code-desc">
              High-level Python API and rich CLI for materials modeling with machine-learned interatomic potentials (MACE, SevenNet, CHGNet, M3GNet).
            </p>
            <div class="code-install-box">
              <code>pip install janus-core</code>
              <button class="copy-snippet-btn" data-code="pip install janus-core" title="Copy install command">📋</button>
            </div>
            <div class="person-links" style="margin-top: 1rem;">
              <a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repo &rarr;</a>
              <a href="https://stfc.github.io/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
            </div>
          </article>

          <!-- aiida-mlip -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>🔄</span> aiida-mlip</h3>
              </div>
              <span class="badge" style="background:#fef3c7; color:#92400e;">AiiDA / Provenance</span>
            </div>
            <p class="code-desc">
              AiiDA plugin integrating janus-core for reproducible calculations with machine-learned interatomic potentials and full data provenance.
            </p>
            <div class="code-install-box">
              <code>pip install aiida-mlip</code>
              <button class="copy-snippet-btn" data-code="pip install aiida-mlip" title="Copy install command">📋</button>
            </div>
            <div class="person-links" style="margin-top: 1rem;">
              <a href="https://github.com/stfc/aiida-mlip" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repo &rarr;</a>
              <a href="https://stfc.github.io/aiida-mlip" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
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
              Machine Learning Performance and Extrapolation Guide. A benchmarking framework evaluating MLIPs across diverse systems and physical properties.
            </p>
            <div class="code-install-box">
              <code>git clone https://github.com/ddmms/ml-peg.git</code>
              <button class="copy-snippet-btn" data-code="git clone https://github.com/ddmms/ml-peg.git" title="Copy command">📋</button>
            </div>
            <div class="person-links" style="margin-top: 1rem;">
              <a href="https://github.com/ddmms/ml-peg" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repo &rarr;</a>
              <a href="https://ml-peg.stfc.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">Live Portal</a>
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
              Web application and library for generating input files with optimised k-point meshes for Quantum ESPRESSO SCF calculations. Part of the PSDI Data to Knowledge initiative.
            </p>
            <div class="code-install-box">
              <code>pip install goldilocks</code>
              <button class="copy-snippet-btn" data-code="pip install goldilocks" title="Copy command">📋</button>
            </div>
            <div class="person-links" style="margin-top: 1rem;">
              <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">goldilocks.ac.uk &rarr;</a>
              <a href="https://github.com/stfc/goldilocks" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repo</a>
              <a href="https://goldilocks.streamlit.app" target="_blank" rel="noopener noreferrer" class="person-link-btn">Streamlit App</a>
            </div>
          </article>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="code.html" class="btn btn-primary">View Full Code &amp; Software Directory &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Recent Publications Preview -->
    <section class="section-wrapper">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Recent Research</span>
          <h2 class="section-title">Latest Publications</h2>
          <p class="section-subtitle">
            Synchronized directly via ORCID. Browse our latest journal articles and preprints.
          </p>
        </div>

        <div class="pubs-list" style="margin-bottom: 2rem;">
{recent_pubs_rendered}
        </div>

        <div style="text-align: center;">
          <a href="publications.html" class="btn btn-primary">Search &amp; Filter All {len(pubs)} Publications &rarr;</a>
        </div>
      </div>
    </section>

    <!-- People Preview -->
    <section class="section-wrapper bg-alt">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Our Team</span>
          <h2 class="section-title">Researchers &amp; Software Architects</h2>
          <p class="section-subtitle">
            Multidisciplinary scientists bridging physics, chemistry, machine learning, and high-performance computing.
          </p>
        </div>

        <div class="people-grid">
          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">AE</div>
              <div class="person-title-wrap">
                <h3>Dr. Alin Marin Elena</h3>
                <div class="person-role">Group Leader &bull; Senior Computational Scientist</div>
                <div class="person-affiliation">STFC SCD, UKRI | CCP5 Executive Committee</div>
              </div>
            </div>
            <p class="person-bio">
              Specializing in atomistic molecular dynamics, machine-learned interatomic potentials, DL_POLY development, and scientific computing infrastructures.
            </p>
            <div class="person-links">
              <a href="people.html" class="person-link-btn">Full Profile &rarr;</a>
              <a href="publications.html?author=Alin%20Marin%20Elena" class="person-link-btn">Publications</a>
            </div>
          </article>

          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">EK</div>
              <div class="person-title-wrap">
                <h3>Elliott Kasoar</h3>
                <div class="person-role">Computational Scientist &bull; Research Associate</div>
                <div class="person-affiliation">STFC SCD, UKRI</div>
              </div>
            </div>
            <p class="person-bio">
              Specialist in equivariant graph neural networks, foundation interatomic potentials (MACE), active learning, and lead developer of janus-core.
            </p>
            <div class="person-links">
              <a href="people.html" class="person-link-btn">Full Profile &rarr;</a>
              <a href="publications.html?author=Elliott%20Kasoar" class="person-link-btn">Publications</a>
            </div>
          </article>

          <article class="person-card">
            <div class="person-header">
              <div class="person-avatar">JY</div>
              <div class="person-title-wrap">
                <h3>Dr. Junwen Yin</h3>
                <div class="person-role">Computational Scientist &bull; Research Associate</div>
                <div class="person-affiliation">STFC SCD, UKRI</div>
              </div>
            </div>
            <p class="person-bio">
              Expert in ab initio electronic structure methods, nonadiabatic dynamics, extended CP2K simulations, and materials modeling.
            </p>
            <div class="person-links">
              <a href="people.html" class="person-link-btn">Full Profile &rarr;</a>
              <a href="publications.html?author=Junwen%20Yin" class="person-link-btn">Publications</a>
            </div>
          </article>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="people.html" class="btn btn-outline">Meet All Members &amp; Open Opportunities &rarr;</a>
        </div>
      </div>
    </section>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""
    return content


def generate_code_html():
    header_html = get_header("code")
    footer_html = get_footer()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Code &amp; Software | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Open-source scientific software packages developed by DDMMS: janus-core, aiida-mlip, ml-peg, and goldilocks.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-pill">Software Suite</span>
        <h1 class="section-title">Open-Source Scientific Codes &amp; Tools</h1>
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
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 2.5rem;">
    <div class="container" id="pubs-app-root">
      <div class="section-header" style="text-align: left; margin-bottom: 2rem;">
        <span class="section-pill">Research Bibliography</span>
        <h1 class="section-title">Publications &amp; Preprints</h1>
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
    header_html = get_header("about")
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
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-pill">About DDMMS</span>
        <h1 class="section-title">Our Vision, Science &amp; Heritage</h1>
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

          <h3 style="margin-top: 1.5rem;">Methodological Pillars</h3>
          <p>
            Our research combines rigorous physics with modern data science across four interconnected layers:
          </p>
          <div class="about-pillars" style="margin-top: 0.5rem;">
            <div class="pillar-card">
              <div class="pillar-icon">🧬</div>
              <h4 class="pillar-title">1. Machine Learning &amp; AI</h4>
              <p class="pillar-desc">Equivariant graph neural networks (MACE, SevenNet, CHGNet), polarizable foundation models, and active learning strategies.</p>
            </div>
            <div class="pillar-card">
              <div class="pillar-icon">⚡</div>
              <h4 class="pillar-title">2. Atomistic Simulation</h4>
              <p class="pillar-desc">First-principles DFT, nonadiabatic dynamics with CP2K, and massive-parallel molecular dynamics with DL_POLY 5.</p>
            </div>
            <div class="pillar-card">
              <div class="pillar-icon">🔬</div>
              <h4 class="pillar-title">3. Materials Discovery</h4>
              <p class="pillar-desc">Metal-organic frameworks (MOFs), molten salts for green energy, negative thermal expansion, and heterogeneous catalysts.</p>
            </div>
            <div class="pillar-card">
              <div class="pillar-icon">🌐</div>
              <h4 class="pillar-title">4. Open Science &amp; FAIR</h4>
              <p class="pillar-desc">Modular, reproducible software pipelines published under permissive open-source licenses for the international community.</p>
            </div>
          </div>

          <h3 style="margin-top: 2rem;">Collaborative Ecosystem &amp; PSDI Data to Knowledge</h3>
          <p>
            We are an active development partner in the UKRI <strong>Physical Sciences Data Infrastructure (PSDI)</strong> under the <strong>Data to Knowledge</strong> program. Through projects such as <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer"><strong>Goldilocks</strong> (goldilocks.ac.uk)</a>, we develop tools, machine learning representations, and optimal parameter datasets to enhance the efficiency, reproducibility, and sustainability of electronic structure calculations across the UK research community.
          </p>
          <p>
            We also work closely with the Collaborative Computational Project for computer simulation of condensed and materials phases (CCP5), the ISIS Neutron and Muon Source, the Diamond Light Source, and academic institutions worldwide.
          </p>
        </div>

        <div class="about-sidebar">
          <div class="news-box">
            <h3 class="news-box-title"><span>🏛</span> Key Facts &amp; Infrastructure</h3>
            <ul class="news-list">
              <li class="news-item">
                <div class="news-date">Institution</div>
                <div class="news-headline">STFC Scientific Computing Department, UKRI.</div>
              </li>
              <li class="news-item">
                <div class="news-date">Location</div>
                <div class="news-headline">Sci-Tech Daresbury, Cheshire / Warrington, UK.</div>
              </li>
              <li class="news-item">
                <div class="news-date">National Infrastructure</div>
                <div class="news-headline">PSDI (Physical Sciences Data Infrastructure) – Data to Knowledge program partner.</div>
              </li>
              <li class="news-item">
                <div class="news-date">HPC Supercomputing</div>
                <div class="news-headline">SCARF, ARCHER2 UK National Supercomputing Service, and Tier-2 centers.</div>
              </li>
              <li class="news-item">
                <div class="news-date">Community Leadership</div>
                <div class="news-headline">Active governance in CCP5, DL_POLY consortia, and atomistic machine learning standards.</div>
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


def generate_people_html():
    header_html = get_header("people")
    footer_html = get_footer()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>People | Data Driven Materials and Molecular Science</title>
  <meta name="description" content="Meet the researchers, developers, and collaborators in the Data Driven Materials and Molecular Science group.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-pill">The Group</span>
        <h1 class="section-title">Members &amp; Researchers</h1>
        <p class="section-subtitle">
          Our team comprises specialists in theoretical condensed matter physics, computational chemistry, software architecture, and AI for science.
        </p>
      </div>

      <div class="people-grid">
        <!-- Dr. Alin Marin Elena -->
        <article class="person-card">
          <div class="person-header">
            <div class="person-avatar">AE</div>
            <div class="person-title-wrap">
              <h3>Dr. Alin Marin Elena</h3>
              <div class="person-role">Group Leader &bull; Senior Computational Scientist</div>
              <div class="person-affiliation">STFC SCD, UKRI | CCP5 Executive Committee</div>
            </div>
          </div>
          <p class="person-bio">
            Alin leads the Data Driven Materials and Molecular Science research group. His work centres on multiscale molecular dynamics algorithms, the architecture and scalable parallelisation of DL_POLY 5, physics-informed machine learning, and transport properties in complex liquids and molten salts.
          </p>
          <div class="person-tags">
            <span class="person-tag">ML Interatomic Potentials</span>
            <span class="person-tag">Molecular Dynamics</span>
            <span class="person-tag">DL_POLY Consortia</span>
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
            <div class="person-avatar">EK</div>
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
            <div class="person-avatar">JY</div>
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

      <!-- Opportunities Section -->
      <section style="margin-top: 4rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2.5rem;" id="contact">
        <h2 style="font-size: 1.75rem; font-weight: 800; color: var(--text); margin-bottom: 1rem;">Join the Research Group</h2>
        <p style="color: var(--text-muted); font-size: 1.05rem; line-height: 1.7; max-width: 800px; margin-bottom: 1.5rem;">
          We are always enthusiastic to collaborate with motivated graduate students, postdoctoral researchers, and academic visitors who wish to explore machine-learned interatomic potentials, extreme-scale molecular dynamics, or materials for sustainable energy technologies.
        </p>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
          <a href="mailto:alin-marin.elena@stfc.ac.uk" class="btn btn-primary"><span>✉</span> Get in Touch via Email</a>
          <a href="https://www.scd.stfc.ac.uk" target="_blank" rel="noopener noreferrer" class="btn btn-outline">STFC Careers &amp; Fellowships &rarr;</a>
        </div>
      </section>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


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
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-pill">Scientific Portfolio</span>
        <h1 class="section-title">Research Themes &amp; Programs</h1>
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
            <span class="research-tag">Theme 5 &bull; PSDI Data to Knowledge &amp; Benchmarks</span>
            <h2 class="research-card-title">Sustainable DFT &amp; Community Benchmarks (Goldilocks &amp; ML-PEG)</h2>
            <p class="research-card-desc">
              Computational electronic structure calculations represent a major fraction of workloads on national supercomputing services like ARCHER2. In collaboration with the <strong>PSDI (Physical Sciences Data Infrastructure) Data to Knowledge</strong> initiative, we develop <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer"><strong>Goldilocks</strong> (goldilocks.ac.uk)</a> to predict optimal, sustainable k-point convergence parameters for Quantum ESPRESSO, eliminating compute and electricity waste while preserving target accuracy.
            </p>
            <p class="research-card-desc" style="margin-top: 0.5rem;">
              Alongside Goldilocks, our ML-PEG benchmarking platform provides rigorous, multi-property evaluation protocols for community machine-learned interatomic potentials.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="https://goldilocks.ac.uk" target="_blank" rel="noopener noreferrer" class="btn btn-primary">goldilocks.ac.uk &rarr;</a>
            <a href="code.html" class="btn btn-outline">Explore Code &amp; Software &rarr;</a>
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
        "about.html": generate_about_html(),
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
