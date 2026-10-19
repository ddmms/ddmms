/**
 * Data Driven Materials and Molecular Science (DDMMS)
 * Main JavaScript: Theme, Mobile Navigation, Interactions & Utilities
 */

(function () {
  'use strict';

  // --- Theme Management ---
  const THEME_KEY = 'ddmms-theme';

  const THEME_NAMES = {
    default: 'Cyber Cyan',
    dark: 'Cyber Cyan',
    nord: 'Nord Frost',
    dracula: 'Dracula',
    monokai: 'Monokai Pro',
    gruvbox: 'Gruvbox Retro',
    catppuccin: 'Catppuccin',
    solarized: 'Solarized',
    light: 'Daylight',
  };

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'default'
      : 'light';
  }

  function applyTheme(themeId) {
    if (!THEME_NAMES[themeId]) {
      themeId = 'default';
    }

    document.documentElement.setAttribute('data-theme', themeId);
    try {
      localStorage.setItem(THEME_KEY, themeId);
    } catch (e) {}

    // Update logos to match light/dark contrast
    const isLight = themeId === 'light';
    const brandLogoSrc = isLight
      ? 'assets/logos/ddmms_for_light_modes.svg'
      : 'assets/logos/ddmms_for_dark_modes.svg';

    const heroLogoSrc = isLight
      ? 'assets/logos/ddmms_for_light_modes-with-text.svg'
      : 'assets/logos/ddmms_for_dark_modes-with-text.svg';

    document.querySelectorAll('.brand-logo-img, #site-logo').forEach(img => {
      img.src = brandLogoSrc;
    });

    const cornerBtnLogo = document.getElementById('corner-btn-logo');
    if (cornerBtnLogo) {
      cornerBtnLogo.src = brandLogoSrc;
    }

    document.querySelectorAll('.hero-card-logo').forEach(img => {
      img.src = heroLogoSrc;
    });

    // Update active theme badge
    const badge = document.getElementById('theme-active-name');
    if (badge) {
      badge.textContent = THEME_NAMES[themeId] || 'Cyber Cyan';
    }

    // Update active states on buttons and pills in theme popup and menu
    document.querySelectorAll('.theme-option-btn').forEach(btn => {
      const id = btn.getAttribute('data-theme-id');
      const isActive = id === themeId || (id === 'default' && (themeId === 'default' || themeId === 'dark'));
      btn.classList.toggle('active', isActive);
    });

    document.querySelectorAll('.theme-swatch-pill').forEach(pill => {
      const id = pill.getAttribute('data-theme-id') || pill.getAttribute('data-theme-name');
      const isActive = id === themeId || (id === 'default' && (themeId === 'default' || themeId === 'dark'));
      pill.classList.toggle('active', isActive);
    });

    // Update theme-toggle-btn aria labels
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.setAttribute('aria-label', `Current theme: ${THEME_NAMES[themeId] || themeId}. Click to choose theme.`);
    });
  }

  const initialTheme = localStorage.getItem(THEME_KEY) || getSystemTheme();
  applyTheme(initialTheme);

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem(THEME_KEY)) {
        applyTheme(e.matches ? 'default' : 'light');
      }
    });
  }

  // --- Header Initialization & Interactions ---
  function initHeader(headerScope) {
    if (!headerScope) return;

    // Apply active link on all nav links, pills, and chips
    const currentFilename = window.location.pathname.split('/').pop() || 'index.html';
    headerScope.querySelectorAll('.nav-desktop .nav-item a, .subnav-pill, .corner-nav-link, .corner-subnav-chip, .mobile-nav-item a').forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentFilename || (currentFilename === '' && href === 'index.html')) {
        link.classList.add('active');
        const parentDropdown = link.closest('.nav-item-has-dropdown');
        if (parentDropdown) {
          const mainLink = parentDropdown.querySelector('.nav-link-main');
          if (mainLink) mainLink.classList.add('active');
        }
        // If it's a chip inside a corner nav group, expand that group
        const parentGroup = link.closest('.corner-nav-group');
        if (parentGroup) {
          const subpanel = parentGroup.querySelector('.corner-subnav-panel');
          const toggleBtn = parentGroup.querySelector('.corner-nav-group-toggle-btn');
          if (subpanel) subpanel.classList.add('show');
          if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
        }
      }
    });

    // Corner Theme Controls & Panel
    const cornerThemeToggle = headerScope.querySelector('#corner-theme-toggle, .corner-theme-btn');
    const cornerThemePanel = headerScope.querySelector('#corner-theme-panel, .corner-theme-panel');
    const cornerMenuToggle = headerScope.querySelector('#corner-menu-toggle, .corner-menu-btn, .mobile-toggle-btn');
    const cornerMenuPanel = headerScope.querySelector('#corner-menu-panel, .corner-menu-panel, .mobile-drawer');

    function toggleThemePanel(open) {
      if (!cornerThemePanel || !cornerThemeToggle) return;
      const isOpen = open !== undefined ? open : !cornerThemePanel.classList.contains('show');
      cornerThemePanel.classList.toggle('show', isOpen);
      cornerThemeToggle.setAttribute('aria-expanded', String(isOpen));
      if (isOpen && cornerMenuPanel && cornerMenuToggle) {
        cornerMenuPanel.classList.remove('show', 'open');
        cornerMenuToggle.setAttribute('aria-expanded', 'false');
      }
    }

    function toggleMenuPanel(open) {
      if (!cornerMenuPanel || !cornerMenuToggle) return;
      const isOpen = open !== undefined ? open : !cornerMenuPanel.classList.contains('show');
      cornerMenuPanel.classList.toggle('show', isOpen);
      cornerMenuPanel.classList.toggle('open', isOpen);
      cornerMenuToggle.setAttribute('aria-expanded', String(isOpen));
      if (isOpen && cornerThemePanel && cornerThemeToggle) {
        cornerThemePanel.classList.remove('show');
        cornerThemeToggle.setAttribute('aria-expanded', 'false');
      }
    }

    if (cornerThemeToggle && cornerThemePanel) {
      cornerThemeToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleThemePanel();
      });
    }

    if (cornerMenuToggle && cornerMenuPanel) {
      cornerMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenuPanel();
      });

      cornerMenuPanel.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => toggleMenuPanel(false));
      });

      // Submenu group toggles inside corner menu
      cornerMenuPanel.querySelectorAll('.corner-nav-group-toggle-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          const expanded = btn.getAttribute('aria-expanded') === 'true';
          btn.setAttribute('aria-expanded', String(!expanded));
          const group = btn.closest('.corner-nav-group');
          if (group) {
            const subpanel = group.querySelector('.corner-subnav-panel');
            if (subpanel) {
              subpanel.classList.toggle('show', !expanded);
            }
          }
        });
      });
    }

    // Global click listener to close popups on outside click
    document.addEventListener('click', e => {
      if (
        cornerThemePanel && cornerThemePanel.classList.contains('show') &&
        !cornerThemePanel.contains(e.target) &&
        !(cornerThemeToggle && cornerThemeToggle.contains(e.target))
      ) {
        toggleThemePanel(false);
      }
      if (
        cornerMenuPanel && (cornerMenuPanel.classList.contains('show') || cornerMenuPanel.classList.contains('open')) &&
        !cornerMenuPanel.contains(e.target) &&
        !(cornerMenuToggle && cornerMenuToggle.contains(e.target))
      ) {
        toggleMenuPanel(false);
      }
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        if (cornerThemePanel && cornerThemePanel.classList.contains('show')) {
          toggleThemePanel(false);
        }
        if (cornerMenuPanel && (cornerMenuPanel.classList.contains('show') || cornerMenuPanel.classList.contains('open'))) {
          toggleMenuPanel(false);
        }
      }
    });

    // Theme option buttons in theme dropdown panel
    headerScope.querySelectorAll('.theme-option-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const themeId = btn.getAttribute('data-theme-id');
        if (themeId) {
          applyTheme(themeId);
        }
      });
    });

    // Theme swatch pills in menu
    headerScope.querySelectorAll('.theme-swatch-pill').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const themeId = btn.getAttribute('data-theme-id') || btn.getAttribute('data-theme-name');
        if (themeId) {
          applyTheme(themeId);
        }
      });
    });

    // Refresh logos and toggle states for current theme
    const currentTheme = document.documentElement.getAttribute('data-theme') || initialTheme;
    applyTheme(currentTheme);
  }

  // Check if header is already present in DOM
  const existingHeader = document.querySelector('.site-header');
  if (existingHeader) {
    initHeader(existingHeader.parentElement || existingHeader);
  }

  // Bind any existing theme toggle buttons or option buttons outside dynamic header
  document.querySelectorAll('.theme-option-btn, .theme-swatch-pill').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const themeId = btn.getAttribute('data-theme-id') || btn.getAttribute('data-theme-name');
      if (themeId) {
        applyTheme(themeId);
      }
    });
  });

  // --- Toast Notification Utility ---
  window.showToast = function (message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  };

  // --- Copy Snippet Button Handlers ---
  document.querySelectorAll('.copy-snippet-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const code = btn.getAttribute('data-code');
      if (code) {
        navigator.clipboard.writeText(code).then(() => {
          window.showToast(`Copied: "${code}"`);
        }).catch(() => {
          window.showToast('Failed to copy to clipboard');
        });
      }
    });
  });

  // --- Reusable Header Dynamic Loader ---
  function loadReusableHeader() {
    const headerPlaceholders = document.querySelectorAll('#site-header, [data-include-header], #reusable-header');
    headerPlaceholders.forEach(el => {
      if (el.children.length > 0) return;

      fetch('header.html')
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.text();
        })
        .then(html => {
          el.innerHTML = html;
          initHeader(el);
        })
        .catch(err => {
          console.debug('Dynamic fetch of header.html failed, using fallback:', err);
          el.innerHTML = `  <header class="site-header" id="top">
    <div class="container header-container">
      <a href="index.html" class="brand-link" aria-label="DDMMS Home">
        <img id="site-logo" class="brand-logo-img" src="assets/logos/ddmms_for_light_modes.svg" alt="Data Driven Materials and Molecular Science">
        <div class="brand-text-block">
          <span class="brand-title-main">DDMMS</span>
          <span class="brand-title-sub">Data Driven Materials &amp; Molecular Science</span>
        </div>
      </a>

      <div class="header-actions">
        <button
          type="button"
          id="corner-theme-toggle"
          class="corner-theme-btn theme-toggle-btn"
          aria-expanded="false"
          aria-controls="corner-theme-panel"
          aria-label="Choose color theme"
          title="Choose color theme"
        >
          <svg class="palette-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.49 2 2 6.49 2 12s4.49 10 10 10a2.5 2.5 0 0 0 2.5-2.5c0-.61-.23-1.21-.64-1.67-.4-.46-.61-.99-.61-1.58 0-1.38 1.12-2.5 2.5-2.5h1.75c3.04 0 5.5-2.46 5.5-5.5C22 5.61 17.39 2 12 2zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 8 6.5 8s1.5.67 1.5 1.5S7.33 11 6.5 11zm3-4c-.83 0-1.5-.67-1.5-1.5S8.67 4 9.5 4s1.5.67 1.5 1.5S10.33 7 9.5 7zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 4 14.5 4s1.5.67 1.5 1.5S15.33 7 14.5 7zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 8 17.5 8s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
        </button>

        <button type="button" id="corner-menu-toggle" class="corner-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="corner-menu-panel">
          <img id="corner-btn-logo" src="assets/logos/ddmms_for_light_modes.svg" alt="DDMMS" class="brand-avatar">
          <span id="corner-current-section">Menu</span>
          <span class="menu-icon-bars" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </div>
    </div>

    <!-- Theme Selection Panel matching mlego.elena.re -->
    <div id="corner-theme-panel" class="corner-theme-panel" role="dialog" aria-label="Color theme selector">
      <div class="corner-theme-panel-header">
        <span class="corner-theme-panel-title">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" class="theme-header-icon"><path d="M12 2C6.49 2 2 6.49 2 12s4.49 10 10 10a2.5 2.5 0 0 0 2.5-2.5c0-.61-.23-1.21-.64-1.67-.4-.46-.61-.99-.61-1.58 0-1.38 1.12-2.5 2.5-2.5h1.75c3.04 0 5.5-2.46 5.5-5.5C22 5.61 17.39 2 12 2zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 8 6.5 8s1.5.67 1.5 1.5S7.33 11 6.5 11zm3-4c-.83 0-1.5-.67-1.5-1.5S8.67 4 9.5 4s1.5.67 1.5 1.5S10.33 7 9.5 7zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 4 14.5 4s1.5.67 1.5 1.5S15.33 7 14.5 7zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 8 17.5 8s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
          Color Theme
        </span>
        <span class="theme-active-badge" id="theme-active-name">Cyber Cyan</span>
      </div>
      <div class="theme-options-grid">
        <button type="button" class="theme-option-btn active" data-theme-id="default" title="Cyber Cyan"><span class="theme-swatch" style="--swatch-1: #57cbcc; --swatch-2: #6cb670; --swatch-bg: #0f1318;"></span><span class="theme-name">Cyber Cyan</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="nord" title="Nord Frost"><span class="theme-swatch" style="--swatch-1: #88c0d0; --swatch-2: #a3be8c; --swatch-bg: #242933;"></span><span class="theme-name">Nord Frost</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="dracula" title="Dracula"><span class="theme-swatch" style="--swatch-1: #bd93f9; --swatch-2: #ff79c6; --swatch-bg: #21222c;"></span><span class="theme-name">Dracula</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="monokai" title="Monokai Pro"><span class="theme-swatch" style="--swatch-1: #ffd866; --swatch-2: #ff6188; --swatch-bg: #19181a;"></span><span class="theme-name">Monokai Pro</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="gruvbox" title="Gruvbox Retro"><span class="theme-swatch" style="--swatch-1: #fabd2f; --swatch-2: #8ec07c; --swatch-bg: #1d2021;"></span><span class="theme-name">Gruvbox Retro</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="catppuccin" title="Catppuccin Mocha"><span class="theme-swatch" style="--swatch-1: #cba6f7; --swatch-2: #f5c2e7; --swatch-bg: #11111b;"></span><span class="theme-name">Catppuccin</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="solarized" title="Solarized Dark"><span class="theme-swatch" style="--swatch-1: #2aa198; --swatch-2: #cb4b16; --swatch-bg: #00212b;"></span><span class="theme-name">Solarized</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
        <button type="button" class="theme-option-btn" data-theme-id="light" title="Daylight"><span class="theme-swatch" style="--swatch-1: #0891b2; --swatch-2: #16a34a; --swatch-bg: #f8fafc;"></span><span class="theme-name">Daylight</span><svg class="theme-check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></button>
      </div>
    </div>

    <!-- Floating Corner Menu Panel -->
    <div id="corner-menu-panel" class="corner-menu-panel mobile-drawer" role="menu">
      <div class="corner-panel-header">
        <span class="corner-panel-title">DDMMS Navigation</span>
        <span class="corner-panel-badge">ddmms.stfc.ac.uk</span>
      </div>
      <ul id="corner-nav-list" class="corner-nav-list mobile-nav-links">
        <li class="mobile-nav-item"><a href="index.html" class="corner-nav-link" style="--nav-item-color: #57cbcc;">Home</a></li>
        <li class="mobile-nav-item"><a href="people.html" class="corner-nav-link" style="--nav-item-color: #2dd4bf;">People</a></li>
        <li class="mobile-nav-item"><a href="research.html" class="corner-nav-link" style="--nav-item-color: #6cb670;">Research</a></li>
        <li class="mobile-nav-item"><a href="publications.html" class="corner-nav-link" style="--nav-item-color: #38bdf8;">Publications</a></li>
        <li class="mobile-nav-item"><a href="code.html" class="corner-nav-link" style="--nav-item-color: #fbbf24;">Software</a></li>
      </ul>
    </div>
  </header>`;
          initHeader(el);
        });
    });
  }

  // --- Reusable Footer Dynamic Loader ---
  function initFooter(footerScope) {
    if (!footerScope) return;
    const currentFilename = window.location.pathname.split('/').pop() || 'index.html';
    footerScope.querySelectorAll('.subnav-pill').forEach(pill => {
      const href = pill.getAttribute('href');
      if (href === currentFilename || (currentFilename === '' && href === 'index.html')) {
        pill.classList.add('active');
      }
    });
  }

  function loadReusableFooter() {
    const footerPlaceholders = document.querySelectorAll('#site-footer, [data-include-footer], #reusable-footer');
    footerPlaceholders.forEach(el => {
      if (el.children.length > 0) {
        initFooter(el);
        return;
      }

      fetch('footer.html')
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.text();
        })
        .then(html => {
          el.innerHTML = html;
          initFooter(el);
        })
        .catch(err => {
          console.debug('Dynamic fetch of footer.html failed, using fallback:', err);
          el.innerHTML = `  <footer class="site-footer">
    <div class="container">
      <nav class="subpage-nav-bar footer-nav-pills" aria-label="Footer quick navigation">
        <div class="subpage-nav-scroller footer-pills-list">
          <a href="index.html" class="subnav-pill" style="--pill-color: #57cbcc;"><span class="subnav-pill-title">Home</span></a>
          <a href="people.html" class="subnav-pill" style="--pill-color: #2dd4bf;"><span class="subnav-pill-title">People</span></a>
          <a href="research.html" class="subnav-pill" style="--pill-color: #4ade80;"><span class="subnav-pill-title">Research</span></a>
          <a href="publications.html" class="subnav-pill" style="--pill-color: #38bdf8;"><span class="subnav-pill-title">Publications</span></a>
          <a href="code.html" class="subnav-pill" style="--pill-color: #fbbf24;"><span class="subnav-pill-title">Software</span></a>
          <a href="news.html" class="subnav-pill" style="--pill-color: #f472b6;"><span class="subnav-pill-title">News</span></a>
          <a href="talks.html" class="subnav-pill" style="--pill-color: #a78bfa;"><span class="subnav-pill-title">Talks</span></a>
          <a href="teaching.html" class="subnav-pill" style="--pill-color: #818cf8;"><span class="subnav-pill-title">Teaching</span></a>
          <a href="opportunities.html" class="subnav-pill" style="--pill-color: #fb923c;"><span class="subnav-pill-title">Opportunities</span></a>
          <a href="collaborate.html" class="subnav-pill" style="--pill-color: #34d399;"><span class="subnav-pill-title">Collaborate</span></a>
          <a href="awards.html" class="subnav-pill" style="--pill-color: #eab308;"><span class="subnav-pill-title">Awards</span></a>
        </div>
      </nav>
      <div class="footer-grid">
        <div class="footer-brand">
          <h4>Data Driven Materials and Molecular Science</h4>
          <p>Accelerating atomistic discovery through physics-informed machine learning, multiscale molecular simulation, and open-source scientific workflows.</p>
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
  <div class="toast" id="toast" role="alert" aria-live="polite"></div>`;
          initFooter(el);
        });
    });
  }

  // --- Math Rendering (KaTeX + Offline Fallback) ---
  function renderMathFallback(container) {
    if (!container) return;
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null, false);
    const nodesToReplace = [];
    let currentNode;
    while ((currentNode = walker.nextNode())) {
      if (currentNode.nodeValue && currentNode.nodeValue.includes('$')) {
        const parent = currentNode.parentElement;
        if (parent) {
          const tag = parent.tagName.toLowerCase();
          if (!['script', 'style', 'textarea', 'pre', 'code'].includes(tag) && !parent.closest('.katex') && !parent.closest('.math-rendered')) {
            nodesToReplace.push(currentNode);
          }
        }
      }
    }

    nodesToReplace.forEach(node => {
      const text = node.nodeValue;
      if (!text || !text.includes('$')) return;
      const mathRegex = /\$([^$]+)\$/g;
      if (!mathRegex.test(text)) return;

      const span = document.createElement('span');
      span.innerHTML = text.replace(mathRegex, (_, expr) => {
        expr = expr.trim();
        let formatted = expr
          .replace(/\\delta/g, '&delta;')
          .replace(/\\alpha/g, '&alpha;')
          .replace(/\\beta/g, '&beta;')
          .replace(/\\gamma/g, '&gamma;')
          .replace(/\\epsilon/g, '&epsilon;')
          .replace(/([a-zA-Z0-9])_\{+([a-zA-Z0-9]+)\}+/g, '<em>$1</em><sub>$2</sub>')
          .replace(/([a-zA-Z0-9])_([a-zA-Z0-9]+)/g, '<em>$1</em><sub>$2</sub>')
          .replace(/([a-zA-Z0-9])\^\{+([a-zA-Z0-9]+)\}+/g, '<em>$1</em><sup>$2</sup>')
          .replace(/([a-zA-Z0-9])\^([a-zA-Z0-9]+)/g, '<em>$1</em><sup>$2</sup>');
        if (/^[a-zA-Z]$/.test(formatted)) {
          formatted = `<em>${formatted}</em>`;
        }
        return `<span class="math-rendered">${formatted}</span>`;
      });

      if (node.parentNode) {
        node.parentNode.replaceChild(span, node);
      }
    });
  }

  window.renderAllMath = function (targetEl) {
    const el = targetEl || document.body;
    if (!el) return;
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(el, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false },
            { left: '\\[', right: '\\]', display: true }
          ],
          throwOnError: false
        });
        return;
      } catch (err) {
        console.debug('KaTeX renderMathInElement error:', err);
      }
    }
    renderMathFallback(el);
  };

  // --- News Section Toggle ---
  function initNewsToggle() {
    const headerToggle = document.getElementById('news-header-toggle');
    const expandBtn = document.getElementById('news-expand-btn');
    const historicalWrap = document.getElementById('news-historical-wrap');
    const toggleBadge = document.getElementById('news-toggle-badge');
    const toggleArrow = document.getElementById('news-toggle-arrow');
    const expandBtnText = document.getElementById('news-expand-btn-text');
    const expandBtnIcon = document.getElementById('news-expand-btn-icon');
    if (!historicalWrap || (!headerToggle && !expandBtn)) return;

    const totalCount = (headerToggle && headerToggle.getAttribute('data-total-count')) || 'all';

    function setExpandedState(nextExpanded) {
      if (headerToggle) {
        headerToggle.setAttribute('aria-expanded', String(nextExpanded));
      }
      if (expandBtn) {
        expandBtn.setAttribute('aria-expanded', String(nextExpanded));
      }
      historicalWrap.style.display = nextExpanded ? 'block' : 'none';

      if (toggleArrow) {
        toggleArrow.innerHTML = nextExpanded ? '&uarr;' : '&darr;';
      }
      if (toggleBadge) {
        toggleBadge.textContent = nextExpanded ? 'Show latest 4' : `View all (${totalCount})`;
      }

      if (expandBtnText) {
        expandBtnText.textContent = nextExpanded ? 'Show latest 4 news' : `View all ${totalCount} news updates`;
      }
      if (expandBtnIcon) {
        expandBtnIcon.innerHTML = nextExpanded ? '&uarr;' : '&darr;';
      }
    }

    function toggleNews(e) {
      if (e && e.target && e.target.closest('a')) {
        return; // Allow direct link navigation without triggering accordion toggle
      }
      const currentExpanded = (headerToggle ? headerToggle.getAttribute('aria-expanded') : (expandBtn && expandBtn.getAttribute('aria-expanded'))) === 'true';
      setExpandedState(!currentExpanded);
    }

    if (headerToggle && !headerToggle._newsToggleBound) {
      headerToggle._newsToggleBound = true;
      headerToggle.addEventListener('click', toggleNews);
      headerToggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleNews();
        }
      });
    }

    if (expandBtn && !expandBtn._newsToggleBound) {
      expandBtn._newsToggleBound = true;
      expandBtn.addEventListener('click', toggleNews);
    }
  }

  // --- Homepage Carousel ---
  // Swiping is native (CSS scroll-snap); this wires up the arrows, dots and keyboard.
  function initCarousels() {
    document.querySelectorAll('[data-carousel]').forEach(carousel => {
      const track = carousel.querySelector('.carousel-track');
      if (!track || carousel._carouselBound) return;
      carousel._carouselBound = true;

      const slides = Array.from(track.querySelectorAll('.carousel-slide'));
      const dots = Array.from(carousel.querySelectorAll('.carousel-dot'));
      const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      const currentIndex = () => Math.round(track.scrollLeft / Math.max(track.clientWidth, 1));

      function goTo(index) {
        const target = (index + slides.length) % slides.length;
        track.scrollTo({ left: target * track.clientWidth, behavior: reduceMotion ? 'auto' : 'smooth' });
      }

      function updateDots() {
        const active = currentIndex();
        dots.forEach((dot, i) => dot.setAttribute('aria-current', i === active ? 'true' : 'false'));
      }

      const prevBtn = carousel.querySelector('.carousel-prev');
      const nextBtn = carousel.querySelector('.carousel-next');
      if (prevBtn) prevBtn.addEventListener('click', () => goTo(currentIndex() - 1));
      if (nextBtn) nextBtn.addEventListener('click', () => goTo(currentIndex() + 1));
      dots.forEach((dot, i) => dot.addEventListener('click', () => goTo(i)));

      track.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
          e.preventDefault();
          goTo(currentIndex() + (e.key === 'ArrowRight' ? 1 : -1));
        }
      });

      let frame = null;
      track.addEventListener('scroll', () => {
        if (frame) cancelAnimationFrame(frame);
        frame = requestAnimationFrame(updateDots);
      }, { passive: true });

      // the browser may restore or jump the scroll position after init (e.g. #slide links)
      window.addEventListener('load', updateDots);
      updateDots();
    });
  }

  function initDynamicIncludes() {
    loadReusableHeader();
    loadReusableFooter();
    initNewsToggle();
    initCarousels();
    window.renderAllMath();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initDynamicIncludes();
      setTimeout(window.renderAllMath, 200);
    });
  } else {
    initDynamicIncludes();
    setTimeout(window.renderAllMath, 200);
  }

  window.addEventListener('load', () => {
    if (typeof window.renderAllMath === 'function') {
      window.renderAllMath();
    }
    initNewsToggle();
  });

})();
