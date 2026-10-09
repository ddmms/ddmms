"""Header component for the DDMMS website."""


def generate_header_html() -> str:
    """Generate the reusable, modular header component."""
    return """  <header class="site-header" id="top">
    <div class="container header-container">
      <a href="index.html" class="brand-link" aria-label="DDMMS Home">
        <img id="site-logo" class="brand-logo-img" src="assets/logos/ddmms_for_light_modes.svg" alt="Data Driven Materials and Molecular Science">
        <div class="brand-text-block">
          <span class="brand-title-main">DDMMS</span>
          <span class="brand-title-sub">Data Driven Materials &amp; Molecular Science</span>
        </div>
      </a>

      <nav class="nav-desktop" aria-label="Primary Navigation">
        <ul class="nav-links">
          <li class="nav-item"><a href="index.html">About</a></li>
          <li class="nav-item"><a href="people.html">People</a></li>
          <li class="nav-item"><a href="research.html">Research</a></li>
          <li class="nav-item"><a href="publications.html">Publications</a></li>
          <li class="nav-item"><a href="code.html">Software</a></li>
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
        <li class="mobile-nav-item"><a href="index.html"><span>About</span><span>&rarr;</span></a></li>
        <li class="mobile-nav-item"><a href="people.html"><span>People</span><span>&rarr;</span></a></li>
        <li class="mobile-nav-item"><a href="research.html"><span>Research</span><span>&rarr;</span></a></li>
        <li class="mobile-nav-item"><a href="publications.html"><span>Publications</span><span>&rarr;</span></a></li>
        <li class="mobile-nav-item"><a href="code.html"><span>Software</span><span>&rarr;</span></a></li>
      </ul>
      <div class="mobile-actions">
        <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">Theme Appearance</span>
        <button type="button" class="theme-toggle-btn" aria-label="Toggle theme">
          <svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0012.3 2zm-.3 18a8 8 0 110-16 8.3 8.3 0 011.7.2 8 8 0 00-1.9 7.8 8 8 0 007.8 8c-.5 0-1.1 0-1.6-.0z"/></svg>
        </button>
      </div>
    </div>
  </header>
"""


def get_header(active_page="home", full_markup=False):
    """Return the reusable site header container or full markup.

    Individual HTML pages reuse the separate header.html file directly,
    eliminating duplicate header markup across pages.
    """
    if full_markup:
        return generate_header_html()
    return '  <div id="site-header" data-include-header></div>'
