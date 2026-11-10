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

    const currentPath = window.location.pathname;
    const currentFilename = currentPath.split('/').pop() || 'index.html';
    const currentHash = window.location.hash;

    // Detect active section
    let activeSection = '';
    if (['research.html', 'talks.html', 'teaching.html', 'events.html'].includes(currentFilename)) {
      activeSection = 'research';
    } else if (
      currentFilename === 'people.html' ||
      currentFilename.endsWith('-elena.html') ||
      currentFilename.endsWith('-kasoar.html') ||
      currentFilename.endsWith('-yin.html') ||
      currentPath.includes('/people/')
    ) {
      activeSection = 'people';
    } else if (currentFilename === 'code.html') {
      activeSection = 'software';
    } else if (currentFilename === 'publications.html') {
      activeSection = 'publications';
    } else if (currentFilename === 'index.html' || currentFilename === '') {
      activeSection = 'home';
    }

    // Two-line header Level-2 subline controller
    const sublineWrap = headerScope.querySelector('.header-subline-wrap');
    const subGroups = headerScope.querySelectorAll('.header-subline-group');

    function showSubGroup(groupName) {
      let hasMatch = false;
      subGroups.forEach(g => {
        if (g.getAttribute('data-nav-group') === groupName) {
          g.classList.add('active');
          hasMatch = true;
        } else {
          g.classList.remove('active');
        }
      });
      if (sublineWrap) {
        if (hasMatch) {
          sublineWrap.classList.add('is-visible');
        } else {
          sublineWrap.classList.remove('is-visible');
        }
      }
    }

    // Set initial Level-2 subline according to active section
    if (activeSection) {
      showSubGroup(activeSection);
    }

    // Hover & focus on Level-1 top line pills dynamically populates Level-2 second line
    const level1Pills = headerScope.querySelectorAll('.header-nav-level1 .nav-pill');
    level1Pills.forEach(pill => {
      const targetGroup = pill.getAttribute('data-nav-target');
      pill.addEventListener('mouseenter', () => {
        if (targetGroup) showSubGroup(targetGroup);
      });
      pill.addEventListener('focus', () => {
        if (targetGroup) showSubGroup(targetGroup);
      });
    });

    const headerNavArea = headerScope.closest('.site-header') || headerScope;
    headerNavArea.addEventListener('mouseleave', () => {
      showSubGroup(activeSection);
    });

    // Apply active classes on all nav links, pills, and chips
    headerScope.querySelectorAll('.nav-desktop .nav-item a, .nav-pill, .subnav-pill, .corner-nav-link, .corner-subnav-chip, .mobile-nav-item a').forEach(link => {
      const href = link.getAttribute('href') || '';
      const hrefClean = href.split('#')[0];

      // Level 1 top line pill
      if (link.closest('.header-nav-level1')) {
        const target = link.getAttribute('data-nav-target');
        if (target === activeSection) {
          link.classList.add('active');
        }
      } else if (link.closest('.header-subline-group')) {
        // Level 2 second line sub-pill
        if (href === currentFilename || (currentFilename === '' && href === 'index.html')) {
          link.classList.add('active');
        } else if (hrefClean === currentFilename && currentHash && href.includes(currentHash)) {
          link.classList.add('active');
        } else if (currentFilename === 'research.html' && href === 'research.html') {
          link.classList.add('active');
        } else if (currentFilename === 'code.html' && href === 'code.html') {
          link.classList.add('active');
        } else if (currentFilename === 'people.html' && !currentHash && href === 'people.html#members') {
          link.classList.add('active');
        }
      } else {
        // Drawer / fallback links
        if (hrefClean === currentFilename || (currentFilename === '' && hrefClean === 'index.html')) {
          link.classList.add('active');
          const parentGroup = link.closest('.corner-nav-group');
          if (parentGroup) {
            const subpanel = parentGroup.querySelector('.corner-subnav-panel');
            const toggleBtn = parentGroup.querySelector('.corner-nav-group-toggle-btn');
            if (subpanel) subpanel.classList.add('show');
            if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
          }
        } else if (activeSection === 'people' && hrefClean === 'people.html') {
          link.classList.add('active');
        } else if (activeSection === 'research' && hrefClean === 'research.html') {
          link.classList.add('active');
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

  // Scope to the <header> itself: its parent is <body>, where
  // closest('.site-header') finds nothing and mouseleave never fires.
  const existingHeader = document.querySelector('.site-header');
  if (existingHeader) {
    initHeader(existingHeader);
  }

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
      let activeIndex = 0;

      function goTo(index) {
        activeIndex = (index + slides.length) % slides.length;
        const targetSlide = slides[activeIndex];
        const leftPos = targetSlide ? targetSlide.offsetLeft : activeIndex * track.clientWidth;
        track.scrollTo({ left: leftPos, behavior: reduceMotion ? 'auto' : 'smooth' });
        updateDots();
      }

      function updateDots() {
        const active = activeIndex;
        dots.forEach((dot, i) => dot.setAttribute('aria-current', i === active ? 'true' : 'false'));
      }

      const prevBtn = carousel.querySelector('.carousel-prev');
      const nextBtn = carousel.querySelector('.carousel-next');
      if (prevBtn) prevBtn.addEventListener('click', () => { goTo(activeIndex - 1); restartAutoplay(); });
      if (nextBtn) nextBtn.addEventListener('click', () => { goTo(activeIndex + 1); restartAutoplay(); });
      dots.forEach((dot, i) => dot.addEventListener('click', () => { goTo(i); restartAutoplay(); }));

      track.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
          e.preventDefault();
          goTo(activeIndex + (e.key === 'ArrowRight' ? 1 : -1));
          restartAutoplay();
        }
      });

      // Auto-revolve every 5s (default 5000ms), pausing only if tab is hidden
      const autoplayDelay = parseInt(carousel.dataset.interval || '5000', 10);
      let timer = null;

      function startAutoplay() {
        if (slides.length <= 1) return;
        stopAutoplay();
        timer = setInterval(() => {
          if (document.visibilityState !== 'hidden') {
            goTo(activeIndex + 1);
          }
        }, autoplayDelay);
      }

      function stopAutoplay() {
        if (timer !== null) {
          clearInterval(timer);
          timer = null;
        }
      }

      function restartAutoplay() {
        stopAutoplay();
        startAutoplay();
      }

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          stopAutoplay();
        } else {
          startAutoplay();
        }
      });

      startAutoplay();

      let frame = null;
      track.addEventListener('scroll', () => {
        if (frame) cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          activeIndex = currentIndex();
          updateDots();
        });
      }, { passive: true });

      // the browser may restore or jump the scroll position after init (e.g. #slide links)
      window.addEventListener('load', updateDots);
      updateDots();
    });
  }

  // Header and footer are inlined at build time; nothing to fetch.
  function initPage() {
    initNewsToggle();
    initCarousels();
    window.renderAllMath();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initPage();
      setTimeout(window.renderAllMath, 200);
    });
  } else {
    initPage();
    setTimeout(window.renderAllMath, 200);
  }

  window.addEventListener('load', () => {
    if (typeof window.renderAllMath === 'function') {
      window.renderAllMath();
    }
    initNewsToggle();
  });

})();
