"""Footer component for the DDMMS website."""


def generate_footer_html() -> str:
    """Generate the reusable, modular footer component."""
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
            <li><a href="index.html">About Us</a></li>
            <li><a href="people.html">People</a></li>
            <li><a href="research.html">Research Themes</a></li>
            <li><a href="publications.html">Publications</a></li>
            <li><a href="code.html">Software</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>Affiliations</h5>
          <ul class="footer-links">
            <li><a href="https://www.scd.stfc.ac.uk" target="_blank" rel="noopener noreferrer">STFC SCD</a></li>
            <li><a href="https://www.ukri.org" target="_blank" rel="noopener noreferrer">UKRI</a></li>
            <li><a href="https://www.psdi.ac.uk" target="_blank" rel="noopener noreferrer">PSDI Data to Knowledge</a></li>
            <li><a href="https://www.ccp5.ac.uk" target="_blank" rel="noopener noreferrer">CCP5</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <span>&copy; 2026 Data Driven Materials and Molecular Science (DDMMS). Licensed under BSD-3-Clause.</span>
        <span>United Kingdom</span>
      </div>
    </div>
  </footer>
  <div class="toast" id="toast" role="alert" aria-live="polite"></div>
"""


def get_footer(full_markup=False):
    """Return the reusable site footer container or full markup.

    Individual HTML pages reuse the separate footer.html file directly,
    eliminating duplicate footer markup across pages.
    """
    if full_markup:
        return generate_footer_html()
    return '  <div id="site-footer" data-include-footer></div>'

