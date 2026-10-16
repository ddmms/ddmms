"""Shared layout pieces for the DDMMS website pages."""


def render_page_hero(title: str, intro: str = "", extra_html: str = "") -> str:
    """Render the dark full-width title band shown at the top of every inner page."""
    intro_html = f'\n        <p class="page-hero-intro">{intro}</p>' if intro else ""
    extra = f"\n{extra_html}" if extra_html else ""
    return f"""    <section class="page-hero">
      <div class="container">
        <h1 class="page-hero-title">{title}</h1>{intro_html}{extra}
      </div>
    </section>"""
