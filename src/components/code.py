"""Code & Software page component and data loader for the DDMMS website."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

try:
    from .header import get_header
    from .footer import get_footer
except (ImportError, ValueError):
    try:
        from components.header import get_header
        from components.footer import get_footer
    except ImportError:
        from src.components.header import get_header
        from src.components.footer import get_footer

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOFTWARE_FILE = BASE_DIR / "data" / "software.yaml"


def load_software(software_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load software packages and showcase tools from a YAML file (default: data/software.yaml).

    Requires a valid YAML file provided by the user. Raises FileNotFoundError
    if the file cannot be located.
    """
    target_path: Optional[Path] = None
    if software_file is not None:
        cand = Path(software_file)
        if cand.is_file():
            target_path = cand
        else:
            alt = BASE_DIR / software_file
            if alt.is_file():
                target_path = alt
            else:
                raise FileNotFoundError(f"Software YAML file not found: '{software_file}'")
    else:
        for cand in (SOFTWARE_FILE, BASE_DIR / "data" / "software.yml"):
            if cand.is_file():
                target_path = cand
                break
        if target_path is None:
            raise FileNotFoundError(f"Software YAML file not found at default location '{SOFTWARE_FILE}'")

    content = target_path.read_text(encoding="utf-8-sig")
    parsed = yaml.safe_load(content)

    if not parsed:
        return {"subtitle": "", "packages": []}

    if isinstance(parsed, list):
        return {"subtitle": "", "packages": parsed}

    if isinstance(parsed, dict):
        subtitle = str(parsed.get("subtitle") or "").strip()
        packages = parsed.get("packages") or parsed.get("software") or parsed.get("tools") or []
        return {
            "subtitle": subtitle,
            "packages": packages,
        }

    return {"subtitle": "", "packages": []}


def generate_code_html(
    software_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
) -> str:
    """Generate the code & software page HTML dynamically from software data."""
    header_html = get_header("code")
    footer_html = get_footer()

    if software_data is None:
        software_data = load_software()

    subtitle = ""
    packages: List[Dict[str, Any]] = []

    if isinstance(software_data, dict):
        subtitle = str(software_data.get("subtitle") or "").strip()
        raw_packages = software_data.get("packages") or software_data.get("software") or software_data.get("tools") or []
        if isinstance(raw_packages, list):
            packages = raw_packages
    elif isinstance(software_data, list):
        packages = software_data

    cards = []
    for pkg in packages:
        if not isinstance(pkg, dict):
            continue
        pkg_id = str(pkg.get("id") or "").strip()
        name = str(pkg.get("name") or pkg.get("title") or pkg_id).strip()
        logo = str(pkg.get("logo") or "").strip()
        icon = str(pkg.get("icon") or "").strip()
        description = str(pkg.get("description") or pkg.get("desc") or "").strip()
        install_cmd = str(pkg.get("install") or pkg.get("command") or "").strip()
        features = pkg.get("features") or []
        links = pkg.get("links") or []

        # Logo / Icon
        if logo:
            icon_html = f'<img src="{logo}" alt="{name} logo" class="code-card-logo" width="19" height="19"> '
        elif icon:
            icon_html = f'<span class="code-card-icon">{icon}</span> '
        else:
            icon_html = ''

        # Badge
        badge_data = pkg.get("badge")
        badge_html = ""
        if badge_data:
            if isinstance(badge_data, dict):
                badge_text = str(badge_data.get("text") or "").strip()
                badge_style = str(badge_data.get("style") or "").strip()
                style_attr = f' style="{badge_style}"' if badge_style else ''
                badge_html = f'<span class="badge"{style_attr}>{badge_text}</span>'
            elif isinstance(badge_data, str):
                badge_html = f'<span class="badge">{badge_data.strip()}</span>'

        # Install command snippet
        install_box_html = ""
        if install_cmd:
            install_box_html = f"""          <div class="code-install-box">
            <code>{install_cmd}</code>
            <button class="copy-snippet-btn" data-code="{install_cmd}" title="Copy command">📋</button>
          </div>"""

        # Features
        features_list_html = ""
        if isinstance(features, list) and features:
            items_str = "\n".join(f'            <li>{f}</li>' for f in features if str(f).strip())
            features_list_html = f"""          <ul class="code-features-list">
{items_str}
          </ul>"""

        # Links
        links_html = ""
        link_elements = []
        if isinstance(links, list):
            for lnk in links:
                if not isinstance(lnk, dict):
                    continue
                lnk_text = str(lnk.get("text") or lnk.get("title") or "").strip()
                lnk_url = str(lnk.get("url") or lnk.get("link") or "#").strip()
                if not lnk_text or not lnk_url:
                    continue
                is_external = lnk_url.startswith("http://") or lnk_url.startswith("https://")
                target_attr = ' target="_blank" rel="noopener noreferrer"' if is_external else ''
                link_elements.append(
                    f'<a href="{lnk_url}"{target_attr} class="person-link-btn">{lnk_text}</a>'
                )

        if link_elements:
            links_str = "\n            ".join(link_elements)
            links_html = f"""          <div class="person-links">
            {links_str}
          </div>"""

        parts = [
            f"""        <!-- {name} -->""",
            """        <article class="code-card">""",
            """          <div class="code-card-header">""",
            """            <div class="code-title-group">""",
            f"""              <h3>{icon_html}{name}</h3>""",
            """            </div>""",
        ]
        if badge_html:
            parts.append(f"""            {badge_html}""")
        parts.append("""          </div>""")
        if description:
            parts.append(f"""          <p class="code-desc">\n            {description}\n          </p>""")
        if install_box_html:
            parts.append(install_box_html)
        if features_list_html:
            parts.append(features_list_html)
        if links_html:
            parts.append(links_html)
        parts.append("""        </article>""")

        cards.append("\n".join(parts))

    cards_html = "\n\n".join(cards)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
        <p class="section-subtitle">
          {subtitle}
        </p>
      </div>"""
    else:
        subtitle_html = """      <div class="section-header" style="text-align: left; margin-bottom: 2.5rem;">
      </div>"""

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
{subtitle_html}

      <div class="code-grid" style="grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));">
{cards_html}
      </div>
    </div>
  </main>

{footer_html}
  <script src="assets/js/main.js"></script>
</body>
</html>"""


generate_software_html = generate_code_html
