#!/usr/bin/env python3
"""Site generator for Data Driven Materials and Molecular Science (DDMMS) website.

Generates responsive, accessible HTML pages with shared navigation,
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
        "0000-0001-7374-9352": "Junwen Yin"
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
        ("about", "About", "about.html", "#about"),
        ("people", "People", "people.html", "#people"),
        ("research", "Research", "research.html", "#research"),
        ("publications", "Publications", "publications.html", "#publications"),
        ("code", "Code", "code.html", "#code")
    ]

    # For index.html, internal navigation jumps to section anchors
    # For subpages, navigation links point to the respective page or home anchors
    is_home = (active_page == "home")

    nav_items_desktop = []
    nav_items_mobile = []

    for key, label, page_url, anchor in pages:
        is_active = (active_page == key)
        active_cls = ' class="active"' if is_active else ''
        target_href = anchor if is_home else page_url

        nav_items_desktop.append(f'<li class="nav-item"><a href="{target_href}"{active_cls}>{label}</a></li>')
        nav_items_mobile.append(f'<li class="mobile-nav-item"><a href="{target_href}"{active_cls}><span>{label}</span><span>→</span></a></li>')

    desktop_nav_html = "\n        ".join(nav_items_desktop)
    mobile_nav_html = "\n        ".join(nav_items_mobile)

    home_href = "index.html" if not is_home else "#top"

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

    <!-- Mobile Drawer -->
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
            <li><a href="code.html">Code & Software</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Affiliations</h5>
          <ul class="footer-links">
            <li><a href="https://www.scd.stfc.ac.uk" target="_blank" rel="noopener noreferrer">STFC SCD</a></li>
            <li><a href="https://www.ukri.org" target="_blank" rel="noopener noreferrer">UKRI</a></li>
            <li><a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer">CCP5</a></li>
            <li><a href="https://sci-techdaresbury.com" target="_blank" rel="noopener noreferrer">Sci-Tech Daresbury</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Open Science</h5>
          <ul class="footer-links">
            <li><a href="https://github.com/ddmms" target="_blank" rel="noopener noreferrer">GitHub @ddmms</a></li>
            <li><a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer">janus-core</a></li>
            <li><a href="https://github.com/stfc/FTorch" target="_blank" rel="noopener noreferrer">FTorch</a></li>
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
    pubs_json_str = json.dumps(pubs)
    authors_json_str = json.dumps(authors)

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Data Driven Materials and Molecular Science | DDMMS</title>
  <meta name="description" content="Data Driven Materials and Molecular Science research group - Machine learning interatomic potentials, multiscale molecular dynamics, and materials discovery.">
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
            <span>STFC &bull; UKRI &bull; Sci-Tech Daresbury</span>
          </div>
          <h1 class="hero-title">
            <span class="gradient-text">Data Driven</span> Materials &amp; Molecular Science
          </h1>
          <p class="hero-subtitle">
            Pioneering the convergence of physics-informed machine learning, high-performance molecular dynamics, and automated workflows to decipher materials from quantum to continuum scales.
          </p>
          <div class="hero-cta-group">
            <a href="#research" class="btn btn-primary">Explore Research</a>
            <a href="#code" class="btn btn-outline">Our Software &amp; Code</a>
            <a href="#publications" class="btn btn-outline">Publications ({len(pubs)})</a>
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
                <div class="hero-stat-num">5+</div>
                <div class="hero-stat-label">Open Packages</div>
              </div>
              <div class="hero-stat-item">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-label">Open Science</div>
              </div>
              <div class="hero-stat-item">
                <div class="hero-stat-num">HPC</div>
                <div class="hero-stat-label">Scale Computing</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="section-wrapper bg-alt" id="about">
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
              Our research focuses on solving the accuracy-versus-scale dilemma in atomistic simulation. By integrating <strong>equivariant graph neural networks (MACE, SevenNet)</strong>, advanced electronic structure theories (CP2K, Quantum ESPRESSO), and massive-parallel molecular dynamics (DL_POLY 5), we investigate materials for energy storage, heterogeneous catalysis, carbon capture, and clean technologies.
            </p>

            <div class="about-pillars">
              <div class="pillar-card">
                <div class="pillar-icon">⚛</div>
                <h4 class="pillar-title">Machine Learning Potentials</h4>
                <p class="pillar-desc">Equivariant foundation models (MACE, SevenNet, CHGNet) delivering DFT-level fidelity across millions of atoms.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">⚡</div>
                <h4 class="pillar-title">Extreme-Scale MD</h4>
                <p class="pillar-desc">High-performance algorithms in DL_POLY 5, GPU acceleration, and symplectic integrators on supercomputers.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">💎</div>
                <h4 class="pillar-title">Nanoporous Materials</h4>
                <p class="pillar-desc">Metal-organic frameworks (uMOF), negative thermal expansion, vibrational phonons, and gas adsorption.</p>
              </div>
              <div class="pillar-card">
                <div class="pillar-icon">🛠</div>
                <h4 class="pillar-title">Open-Source Ecosystem</h4>
                <p class="pillar-desc">FAIR scientific codes including janus-core, FTorch, and automated ORCID publication portals.</p>
              </div>
            </div>

            <div style="margin-top: 1rem;">
              <a href="about.html" class="btn btn-outline">Read More About Our Mission &rarr;</a>
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
                  <div class="news-headline">Automated k-point sampling framework for Quantum ESPRESSO published in <em>Digital Discovery</em>.</div>
                </li>
                <li class="news-item">
                  <div class="news-date">2026 Discovery</div>
                  <div class="news-headline">uMOF universal benchmark database and ML interatomic potentials released for metal-organic frameworks.</div>
                </li>
                <li class="news-item">
                  <div class="news-date">Software Impact</div>
                  <div class="news-headline">FTorch featured in <em>Journal of Open Source Software (JOSS)</em> for coupling PyTorch with native Fortran.</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- People Section -->
    <section class="section-wrapper" id="people">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Our Team</span>
          <h2 class="section-title">Researchers &amp; Software Architects</h2>
          <p class="section-subtitle">
            Multidisciplinary researchers bridging physics, chemistry, machine learning, and high-performance computing.
          </p>
        </div>

        <div class="people-grid">
          <!-- Alin Marin Elena -->
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
              Senior computational scientist with extensive leadership in molecular dynamics, machine-learned interatomic potentials, DL_POLY 5 architecture, and scientific software engineering for large-scale materials discovery.
            </p>
            <div class="person-tags">
              <span class="person-tag">MLIPs</span>
              <span class="person-tag">Molecular Dynamics</span>
              <span class="person-tag">DL_POLY</span>
              <span class="person-tag">Molten Salts</span>
              <span class="person-tag">HPC</span>
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
                <span>View Publications</span>
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
              Specialist in equivariant graph neural network potentials (MACE, SevenNet), active learning dataset selection, and workflow automation. Core lead and architect of the janus-core materials simulation platform.
            </p>
            <div class="person-tags">
              <span class="person-tag">MACE Foundation Models</span>
              <span class="person-tag">janus-core</span>
              <span class="person-tag">Active Learning</span>
              <span class="person-tag">Python &amp; ASE</span>
            </div>
            <div class="person-links">
              <a href="https://orcid.org/0009-0005-2015-9478" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                <svg viewBox="0 0 256 256" style="fill:#a6ce39;"><path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/><path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/></svg>
                <span>ORCID</span>
              </a>
              <a href="publications.html?author=Elliott%20Kasoar" class="person-link-btn">
                <span>View Publications</span>
              </a>
            </div>
          </article>

          <!-- Junwen Yin -->
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
              Expert in ab initio electronic structure methods, nonadiabatic molecular dynamics, CP2K code extensions, and materials modeling for photoactive and electrochemically driven systems.
            </p>
            <div class="person-tags">
              <span class="person-tag">Nonadiabatic Dynamics</span>
              <span class="person-tag">CP2K Framework</span>
              <span class="person-tag">DFT</span>
              <span class="person-tag">Photochemistry</span>
            </div>
            <div class="person-links">
              <a href="https://orcid.org/0000-0001-7374-9352" target="_blank" rel="noopener noreferrer" class="person-link-btn" title="ORCID Profile">
                <svg viewBox="0 0 256 256" style="fill:#a6ce39;"><path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/><path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/></svg>
                <span>ORCID</span>
              </a>
              <a href="publications.html?author=Junwen%20Yin" class="person-link-btn">
                <span>View Publications</span>
              </a>
            </div>
          </article>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="people.html" class="btn btn-outline">Meet All Members, Collaborators &amp; Open Positions &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Research Section -->
    <section class="section-wrapper bg-alt" id="research">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Research Themes</span>
          <h2 class="section-title">Core Scientific Frontiers</h2>
          <p class="section-subtitle">
            Exploring materials complexity across spatial and temporal dimensions with data-driven and quantum-mechanics tools.
          </p>
        </div>

        <div class="research-grid">
          <!-- Pillar 1 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Machine Learning</span>
              <h3 class="research-card-title">Foundation Machine-Learned Interatomic Potentials</h3>
              <p class="research-card-desc">
                Developing, fine-tuning, and benchmarking equivariant graph neural networks (MACE, SevenNet, CHGNet). Enhancing transferability, active learning dataset selection, and long-range polarizable electrostatics for molecular and condensed-phase systems.
              </p>
            </div>
            <ul class="research-highlights">
              <li>MACE-POLAR polarisable foundation models</li>
              <li>Active-learning training set optimization</li>
              <li>Cross-learning between electronic structure levels</li>
            </ul>
          </div>

          <!-- Pillar 2 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Porous Frameworks</span>
              <h3 class="research-card-title">Metal-Organic Frameworks &amp; Nanoporous Solids</h3>
              <p class="research-card-desc">
                High-throughput screening of flexible MOF structures, negative thermal expansion (NTE) mechanics, vibrational phonon dynamics, and selective catalytic centers for hydrocarbon separations and environmental cleanup.
              </p>
            </div>
            <ul class="research-highlights">
              <li>uMOF database and benchmark interatomic potentials</li>
              <li>Phonon dispersion &amp; thermodynamic stability</li>
              <li>Subnanometric Pd speciation for selective catalysis</li>
            </ul>
          </div>

          <!-- Pillar 3 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Liquid State Physics</span>
              <h3 class="research-card-title">Molten Salts, Complex Liquids &amp; Transport</h3>
              <p class="research-card-desc">
                Investigating microscopic transport properties, ionic correlations, viscosity, and fundamental bounds of thermal conductivity in molten chloride/fluoride salts and high-entropy liquid mixtures for advanced clean energy reactors.
              </p>
            </div>
            <ul class="research-highlights">
              <li>Thermal conductivity bounds in molten salts</li>
              <li>Green-Kubo and Einstein transport coefficient derivations</li>
              <li>Equilibrium isotope fractionation in mineral phases</li>
            </ul>
          </div>

          <!-- Pillar 4 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">HPC &amp; Algorithms</span>
              <h3 class="research-card-title">Massively Parallel Molecular Dynamics</h3>
              <p class="research-card-desc">
                Architecting DL_POLY 5 for ultra-scale parallelism on distributed memory supercomputers, offloading compute kernels to GPU accelerators, and on-the-fly trajectory analysis for systems comprising tens of millions of atoms.
              </p>
            </div>
            <ul class="research-highlights">
              <li>DL_POLY 5 massive parallelism &amp; domain decomposition</li>
              <li>Symplectic integrators and rigid-body constraints</li>
              <li>On-the-fly property evaluations and statistical sampling</li>
            </ul>
          </div>

          <!-- Pillar 5 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Workflows</span>
              <h3 class="research-card-title">Autonomous Multiscale Simulation Workflows</h3>
              <p class="research-card-desc">
                End-to-end automated simulation pipelines connecting structure parsing, cell relaxation via FrechetCellFilter, full 6x6 elasticity stiffness tensors ($C_{{ij}}$), equation of state (EOS), and CI-NEB transition state searches.
              </p>
            </div>
            <ul class="research-highlights">
              <li>Automated single points, geometry optimizations &amp; MD</li>
              <li>Equation of state &amp; elastic tensor calculation pipelines</li>
              <li>Automated Quantum ESPRESSO k-point mesh optimization</li>
            </ul>
          </div>

          <!-- Pillar 6 -->
          <div class="research-card">
            <div class="research-card-top">
              <span class="research-tag">Spectroscopy</span>
              <h3 class="research-card-title">Inelastic Neutron Scattering &amp; Spectroscopy Validation</h3>
              <p class="research-card-desc">
                Directly validating machine-learned interatomic potential energy landscapes against high-pressure inelastic neutron scattering experiments at ISIS Neutron and Muon Source and international beamline facilities.
              </p>
            </div>
            <ul class="research-highlights">
              <li>Experimental validation of potential energy landscapes</li>
              <li>Dynamical structure factor $S(Q, \\omega)$ calculations</li>
              <li>Phonon anharmonicity and thermal expansion in perovskites</li>
            </ul>
          </div>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="research.html" class="btn btn-primary">Discover More Research Details &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Publications Section (Integrated from ../pubs) -->
    <section class="section-wrapper" id="publications">
      <div class="container" id="pubs-app-root">
        <div class="section-header">
          <span class="section-pill">Research Output</span>
          <h2 class="section-title">Publications &amp; Preprints</h2>
          <p class="section-subtitle">
            Curated and auto-aggregated from group member ORCID records. Filter dynamically by author, year, or search topic.
          </p>
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

        <!-- Results Counter & Status Bar -->
        <div class="pubs-results-bar">
          <div class="pubs-counter">
            Showing <strong class="pub-visible-count">0</strong> of <strong class="pub-total-count">{len(pubs)}</strong> publications
          </div>

          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <a href="publications.html" class="btn-action" title="Open full publication catalog">
              <span>📚</span> Full Publication Catalog
            </a>
            <a href="publications.json" download="publications.json" class="btn-action" title="Download raw JSON feed">
              <span>{{ }}</span> JSON Feed
            </a>
            <a href="PUBLICATIONS.md" class="btn-action" title="View Markdown bibliography">
              <span>📄</span> Markdown
            </a>
          </div>
        </div>

        <!-- Publication Cards List -->
        <div class="pubs-container"></div>
      </div>
    </section>

    <!-- Code & Software Section -->
    <section class="section-wrapper bg-alt" id="code">
      <div class="container">
        <div class="section-header">
          <span class="section-pill">Software &amp; Tools</span>
          <h2 class="section-title">Open-Source Scientific Codes</h2>
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
              Tools for materials modeling with machine-learned interatomic potentials (MACE, SevenNet, CHGNet, M3GNet). Provides both a high-level Python API and a rich CLI for automated atomistic workflows.
            </p>
            <div class="code-install-box">
              <code>pip install janus-core</code>
              <button class="copy-snippet-btn" data-code="pip install janus-core" title="Copy install command">📋</button>
            </div>
            <ul class="code-features-list">
              <li>Single points, forces, stresses, Hessians</li>
              <li>Geometry optimization (BFGS, FIRE, FrechetCellFilter)</li>
              <li>Molecular dynamics (NVE, NVT, NPT, Langevin, Nosé-Hoover)</li>
              <li>Automated phonons, equation of state, elasticity tensors &amp; NEB</li>
            </ul>
            <div class="person-links">
              <a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
              <a href="https://stfc.github.io/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">Documentation</a>
            </div>
          </article>

          <!-- FTorch -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>🔥</span> FTorch</h3>
              </div>
              <span class="badge" style="background:#fee2e2; color:#991b1b;">Fortran / C++</span>
            </div>
            <p class="code-desc">
              A lightweight library for coupling PyTorch machine learning models directly into native Fortran applications, enabling fast ML inferencing inside legacy HPC simulation codes.
            </p>
            <div class="code-install-box">
              <code>git clone https://github.com/stfc/FTorch.git</code>
              <button class="copy-snippet-btn" data-code="git clone https://github.com/stfc/FTorch.git" title="Copy git clone command">📋</button>
            </div>
            <ul class="code-features-list">
              <li>Zero-copy tensor passing between Fortran and TorchScript</li>
              <li>Seamless deployment of deep neural networks in HPC models</li>
              <li>Peer-reviewed and published in JOSS (Journal of Open Source Software)</li>
            </ul>
            <div class="person-links">
              <a href="https://github.com/stfc/FTorch" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
              <a href="https://doi.org/10.21105/joss.07602" target="_blank" rel="noopener noreferrer" class="person-link-btn">JOSS Paper</a>
            </div>
          </article>

          <!-- DL_POLY 5 -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>🌐</span> DL_POLY 5</h3>
              </div>
              <span class="badge" style="background:#e0e7ff; color:#3730a3;">Fortran / MPI / OMP</span>
            </div>
            <p class="code-desc">
              Flagship STFC general-purpose atomistic molecular dynamics package engineered for massive parallelism on distributed-memory supercomputers and heterogeneous accelerators.
            </p>
            <div class="code-install-box">
              <code>cmake -B build -DENABLE_MPI=ON</code>
              <button class="copy-snippet-btn" data-code="cmake -B build -DENABLE_MPI=ON" title="Copy build command">📋</button>
            </div>
            <ul class="code-features-list">
              <li>Scalable domain decomposition for 10M+ atoms</li>
              <li>Symplectic integrators and rigid-body quaternions</li>
              <li>Calculates system properties on the fly via massive parallelism</li>
            </ul>
            <div class="person-links">
              <a href="https://www.scd.stfc.ac.uk/Pages/DL_POLY.aspx" target="_blank" rel="noopener noreferrer" class="person-link-btn">STFC DL_POLY Portal &rarr;</a>
              <a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">CCP5</a>
            </div>
          </article>

          <!-- uMOF -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>🏛</span> uMOF Benchmark</h3>
              </div>
              <span class="badge" style="background:#ecfdf5; color:#065f46;">Dataset / MLIP</span>
            </div>
            <p class="code-desc">
              A universal database, benchmark suite, and machine learning interatomic potentials tailored specifically for metal-organic frameworks and hybrid crystalline structures.
            </p>
            <div class="code-install-box">
              <code>pip install mof-analysis</code>
              <button class="copy-snippet-btn" data-code="pip install mof-analysis" title="Copy command">📋</button>
            </div>
            <ul class="code-features-list">
              <li>Comprehensive database of relaxed MOF structures &amp; phonons</li>
              <li>Machine learned potentials for high-throughput vibrational screening</li>
              <li>Negative thermal expansion analysis suite</li>
            </ul>
            <div class="person-links">
              <a href="https://arxiv.org/abs/2608.28100" target="_blank" rel="noopener noreferrer" class="person-link-btn">arXiv Preprint &rarr;</a>
            </div>
          </article>

          <!-- pubs -->
          <article class="code-card">
            <div class="code-card-header">
              <div class="code-title-group">
                <h3><span>📚</span> pubs</h3>
              </div>
              <span class="badge" style="background:#fef3c7; color:#92400e;">Python / Automation</span>
            </div>
            <p class="code-desc">
              Automated research publication aggregator and web portal generator using the ORCID Public API for academic research groups.
            </p>
            <div class="code-install-box">
              <code>python pubs.py</code>
              <button class="copy-snippet-btn" data-code="python pubs.py" title="Copy command">📋</button>
            </div>
            <ul class="code-features-list">
              <li>ORCID API synchronization with local caching</li>
              <li>Generates interactive HTML portals, Markdown bibliographies &amp; JSON feeds</li>
              <li>Automated GitHub Actions weekly workflow deployment</li>
            </ul>
            <div class="person-links">
              <a href="https://github.com/ddmms/pubs" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub Repository &rarr;</a>
            </div>
          </article>
        </div>

        <div style="text-align: center; margin-top: 2.5rem;">
          <a href="code.html" class="btn btn-outline">Explore Full Software Directory &amp; Documentation &rarr;</a>
        </div>
      </div>
    </section>
  </main>

{footer_html}

  <!-- Embedded Data for 100% Offline and Local Functionality -->
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
      // Initialize publications with interactive filtering
      window.initPublications('pubs-app-root');
    }});
  </script>
</body>
</html>"""
    return content

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
            Our research combines rigorous physics with modern data science across three interconnected layers:
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

          <h3 style="margin-top: 2rem;">Collaborative Ecosystem</h3>
          <p>
            We work closely with the Collaborative Computational Project for computer simulation of condensed and materials phases (CCP5), the ISIS Neutron and Muon Source, the Diamond Light Source, and academic institutions worldwide.
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
  <meta name="description" content="Research areas of the Data Driven Materials and Molecular Science group: MLIPs, MOFs, molten salts, DL_POLY 5, and automated workflows.">
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
              Accurate modeling of chemical reactivity, phases transitions, and defect dynamics requires potential energy surfaces that respect rotational, translational, and permutational invariances. We develop and extend equivariant graph neural network potentials such as MACE, SevenNet, and CHGNet.
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
            <span class="research-tag">Theme 4 &bull; Supercomputing</span>
            <h2 class="research-card-title">Massively Parallel Atomistic MD: DL_POLY 5</h2>
            <p class="research-card-desc">
              STFC DL_POLY 5 is engineered for massive parallelism on distributed-memory supercomputers and heterogeneous accelerators. We lead core enhancements in spatial domain decomposition, rigid-body quaternion dynamics, on-the-fly physical observable calculation, and GPU offloading to model complex condensed systems comprising tens of millions of atoms.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="code.html" class="btn btn-outline">View DL_POLY 5 Software Details &rarr;</a>
          </div>
        </article>

        <!-- Theme 5 -->
        <article class="research-card">
          <div class="research-card-top">
            <span class="research-tag">Theme 5 &bull; Autonomous Workflows</span>
            <h2 class="research-card-title">High-Throughput Simulation Workflows with janus-core</h2>
            <p class="research-card-desc">
              Bridging the gap between interatomic potentials and scientific discovery requires seamless automation. With janus-core, we provide unified pipelines for geometry relaxation (BFGS, FIRE, FrechetCellFilter), equation of state fitting (Birch-Murnaghan, Murnaghan), full 6x6 elasticity stiffness tensors ($C_{{ij}}$), and climbing image nudged elastic band (CI-NEB) minimum energy pathways.
            </p>
          </div>
          <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
            <a href="https://stfc.github.io/janus-core" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Read janus-core Documentation &rarr;</a>
          </div>
        </article>
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
  <meta name="description" content="Open-source scientific software, tools, and repositories developed by the DDMMS research group.">
  <link rel="icon" type="image/svg+xml" href="assets/logos/ddmms.svg">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header_html}

  <main id="main-content" style="padding-top: 3rem;">
    <div class="container">
      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <span class="section-pill">Open Source Ecosystem</span>
        <h1 class="section-title">Software, Codes &amp; Tools</h1>
        <p class="section-subtitle">
          Freely accessible, well-documented, and tested scientific tools supporting the atomistic modeling community.
        </p>
      </div>

      <div class="code-grid" style="grid-template-columns: 1fr 1fr;">
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
            <li>Single-point energies, forces, stress tensors, Hessians</li>
            <li>Geometry optimization with FrechetCellFilter &amp; BFGS/FIRE</li>
            <li>Molecular dynamics (NVE, NVT, NPT) with thermostat/barostat logging</li>
            <li>Automated equation of state (EOS) and full 6x6 elasticity stiffness tensors ($C_{{ij}}$)</li>
            <li>Phonon band structures &amp; DOS via Phonopy</li>
            <li>Minimum Energy Pathways with Climbing-Image NEB</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/stfc/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub &rarr;</a>
            <a href="https://stfc.github.io/janus-core" target="_blank" rel="noopener noreferrer" class="person-link-btn">Docs</a>
            <a href="https://pypi.org/project/janus-core/" target="_blank" rel="noopener noreferrer" class="person-link-btn">PyPI</a>
          </div>
        </article>

        <!-- FTorch -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🔥</span> FTorch</h3>
            </div>
            <span class="badge" style="background:#fee2e2; color:#991b1b;">Fortran / C++ / PyTorch</span>
          </div>
          <p class="code-desc">
            A library for direct coupling of PyTorch machine learning models into native Fortran applications. Developed to lower the technical barrier for incorporating modern AI/ML into large legacy numerical engines.
          </p>
          <div class="code-install-box">
            <code>git clone https://github.com/stfc/FTorch.git</code>
            <button class="copy-snippet-btn" data-code="git clone https://github.com/stfc/FTorch.git" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Direct integration with LibTorch without Python runtime overhead</li>
            <li>Preserves high computational throughput on HPC clusters</li>
            <li>Published in the Journal of Open Source Software (JOSS)</li>
            <li>Extensive tutorial suite and CMake build templates</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/stfc/FTorch" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub &rarr;</a>
            <a href="https://doi.org/10.21105/joss.07602" target="_blank" rel="noopener noreferrer" class="person-link-btn">JOSS Paper</a>
          </div>
        </article>

        <!-- DL_POLY 5 -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>🌐</span> DL_POLY 5</h3>
            </div>
            <span class="badge" style="background:#e0e7ff; color:#3730a3;">Fortran / MPI / OpenMP</span>
          </div>
          <p class="code-desc">
            STFC's flagship molecular dynamics simulation package designed for distributed memory supercomputers. Scales smoothly across thousands of cores for materials, biomolecules, and complex solutions.
          </p>
          <div class="code-install-box">
            <code>cmake -B build -DENABLE_MPI=ON</code>
            <button class="copy-snippet-btn" data-code="cmake -B build -DENABLE_MPI=ON" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Massively parallel domain decomposition</li>
            <li>On-the-fly transport coefficient and correlation calculation</li>
            <li>Rigid body quaternions, bond constraints, and Ewald sums</li>
          </ul>
          <div class="person-links">
            <a href="https://www.scd.stfc.ac.uk/Pages/DL_POLY.aspx" target="_blank" rel="noopener noreferrer" class="person-link-btn">STFC Portal &rarr;</a>
            <a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer" class="person-link-btn">CCP5</a>
          </div>
        </article>

        <!-- pubs -->
        <article class="code-card">
          <div class="code-card-header">
            <div class="code-title-group">
              <h3><span>📚</span> pubs</h3>
            </div>
            <span class="badge" style="background:#fef3c7; color:#92400e;">Python / ORCID / CI</span>
          </div>
          <p class="code-desc">
            Automated publication aggregation engine using the ORCID Public API. Synchronizes research group bibliographies, deduplicates multi-author papers, and generates static searchable portals and feeds.
          </p>
          <div class="code-install-box">
            <code>python pubs.py</code>
            <button class="copy-snippet-btn" data-code="python pubs.py" title="Copy command">📋</button>
          </div>
          <ul class="code-features-list">
            <li>Continuous weekly synchronization via GitHub Actions</li>
            <li>Outputs interactive HTML, Markdown bibliography &amp; JSON feeds</li>
            <li>Instantaneous offline execution with embedded local caching</li>
          </ul>
          <div class="person-links">
            <a href="https://github.com/ddmms/pubs" target="_blank" rel="noopener noreferrer" class="person-link-btn">GitHub &rarr;</a>
            <a href="publications.html" class="person-link-btn">View Live Portal</a>
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
        "code.html": generate_code_html()
    }

    for filename, content in pages.items():
        out_path = BASE_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filename} ({len(content)} bytes)")

    print("Site generation complete!")

if __name__ == "__main__":
    main()
