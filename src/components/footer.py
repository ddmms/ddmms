"""Footer component for the DDMMS website."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Union

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
FOOTER_TEMPLATE_FILE = TEMPLATE_DIR / "footer.html"

DEFAULT_FOOTER_HTML = """  <footer class="site-footer">
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
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <span>&copy; {year} Data Driven Materials and Molecular Science (DDMMS). Licensed under BSD-3-Clause.</span>
        <span>United Kingdom</span>
      </div>
    </div>
  </footer>
  <div class="toast" id="toast" role="alert" aria-live="polite"></div>
"""


def generate_footer_html(
    template_file: Optional[Union[str, Path]] = None,
    year: Optional[Union[str, int]] = None,
) -> str:
    """Generate the reusable, modular footer component by reading from a template file."""
    if year is None:
        year = datetime.now().year

    target_path = None
    if template_file is not None:
        target_path = Path(template_file)
        if not target_path.exists():
            alt_path = BASE_DIR / template_file
            if alt_path.exists():
                target_path = alt_path
    else:
        for cand in (
            FOOTER_TEMPLATE_FILE,
            BASE_DIR / "templates" / "footer.html",
        ):
            if cand.is_file():
                target_path = cand
                break

    if target_path and target_path.is_file():
        content = target_path.read_text(encoding="utf-8")
    else:
        content = DEFAULT_FOOTER_HTML

    # Render template variables
    rendered = (
        content.replace("{{ year }}", str(year))
        .replace("{{year}}", str(year))
        .replace("{year}", str(year))
    )
    if not rendered.endswith("\n"):
        rendered += "\n"
    return rendered


def get_footer(full_markup=False):
    """Return the reusable site footer container or full markup.

    Individual HTML pages reuse the separate footer.html file directly,
    eliminating duplicate footer markup across pages.
    """
    if full_markup:
        return generate_footer_html()
    return '  <div id="site-footer" data-include-footer></div>'
