/**
 * Data Driven Materials and Molecular Science (DDMMS)
 * Main JavaScript: Theme, Mobile Navigation, Interactions & Utilities
 */

(function () {
  'use strict';

  // --- Theme Management ---
  const THEME_KEY = 'ddmms-theme';

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);

    // Update logos to match light/dark contrast
    const brandLogoSrc = theme === 'dark'
      ? 'assets/logos/ddmms_for_dark_modes.svg'
      : 'assets/logos/ddmms_for_light_modes.svg';

    const heroLogoSrc = theme === 'dark'
      ? 'assets/logos/ddmms_for_dark_modes-with-text.svg'
      : 'assets/logos/ddmms_for_light_modes-with-text.svg';

    document.querySelectorAll('.brand-logo-img').forEach(img => {
      img.src = brandLogoSrc;
    });

    document.querySelectorAll('.hero-card-logo').forEach(img => {
      img.src = heroLogoSrc;
    });

    // Update button icons
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
      btn.innerHTML = theme === 'dark'
        ? `<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 000-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 000-1.41.996.996 0 00-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 000-1.41.996.996 0 00-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>`
        : `<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0012.3 2zm-.3 18a8 8 0 110-16 8.3 8.3 0 011.7.2 8 8 0 00-1.9 7.8 8 8 0 007.8 8c-.5 0-1.1 0-1.6-.0z"/></svg>`;
    });
  }

  const initialTheme = localStorage.getItem(THEME_KEY) || getSystemTheme();
  applyTheme(initialTheme);

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem(THEME_KEY)) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // --- Header Initialization & Interactions ---
  function initHeader(headerScope) {
    if (!headerScope) return;

    // Apply active link
    const currentFilename = window.location.pathname.split('/').pop() || 'about.html';
    headerScope.querySelectorAll('.nav-desktop .nav-item a, .mobile-nav-item a').forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentFilename || (currentFilename === '' && href === 'about.html') || (currentFilename === 'index.html' && href === 'about.html')) {
        link.classList.add('active');
      }
    });

    // Theme toggle buttons in header
    headerScope.querySelectorAll('.theme-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    });

    // Mobile Drawer Navigation
    const mobileToggleBtn = headerScope.querySelector('.mobile-toggle-btn');
    const mobileDrawer = headerScope.querySelector('.mobile-drawer');

    if (mobileToggleBtn && mobileDrawer) {
      function toggleDrawer(open) {
        const isOpen = open !== undefined ? open : !mobileDrawer.classList.contains('open');
        mobileDrawer.classList.toggle('open', isOpen);
        mobileToggleBtn.setAttribute('aria-expanded', String(isOpen));
        document.body.style.overflow = isOpen ? 'hidden' : '';
      }

      mobileToggleBtn.addEventListener('click', () => toggleDrawer());

      mobileDrawer.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => toggleDrawer(false));
      });

      document.addEventListener('click', e => {
        if (
          mobileDrawer.classList.contains('open') &&
          !mobileDrawer.contains(e.target) &&
          !mobileToggleBtn.contains(e.target)
        ) {
          toggleDrawer(false);
        }
      });

      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && mobileDrawer.classList.contains('open')) {
          toggleDrawer(false);
        }
      });
    }

    // Refresh logos and toggle states for current theme
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    applyTheme(currentTheme);
  }

  // Check if header is already present in DOM
  const existingHeader = document.querySelector('.site-header');
  if (existingHeader) {
    initHeader(existingHeader.parentElement || existingHeader);
  }

  // Bind any existing theme toggle buttons outside dynamic header
  document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
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
      <a href="about.html" class="brand-link" aria-label="DDMMS Home">
        <img id="site-logo" class="brand-logo-img" src="assets/logos/ddmms_for_light_modes.svg" alt="Data Driven Materials and Molecular Science">
        <div class="brand-text-block">
          <span class="brand-title-main">DDMMS</span>
          <span class="brand-title-sub">Data Driven Materials &amp; Molecular Science</span>
        </div>
      </a>

      <nav class="nav-desktop" aria-label="Primary Navigation">
        <ul class="nav-links">
          <li class="nav-item"><a href="about.html">About</a></li>
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
        <li class="mobile-nav-item"><a href="about.html"><span>About</span><span>&rarr;</span></a></li>
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
  </header>`;
          initHeader(el);
        });
    });
  }

  // --- Reusable Footer Dynamic Loader ---
  function loadReusableFooter() {
    const footerPlaceholders = document.querySelectorAll('#site-footer, [data-include-footer], #reusable-footer');
    footerPlaceholders.forEach(el => {
      if (el.children.length > 0) return;

      fetch('footer.html')
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.text();
        })
        .then(html => {
          el.innerHTML = html;
        })
        .catch(err => {
          console.debug('Dynamic fetch of footer.html failed, using fallback:', err);
          el.innerHTML = `  <footer class="site-footer">
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

  function initDynamicIncludes() {
    loadReusableHeader();
    loadReusableFooter();
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
  });

})();
