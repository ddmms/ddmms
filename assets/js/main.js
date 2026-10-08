/**
 * Data Driven Materials and Molecular Science (DDMMS)
 * Main JavaScript: Theme, Mobile Navigation, Interactions & Utilities
 */

(function () {
  'use strict';

  // --- Theme Management ---
  const THEME_KEY = 'ddmms-theme';
  const themeToggleBtns = document.querySelectorAll('.theme-toggle-btn');
  const brandLogos = document.querySelectorAll('.brand-logo-img');
  const heroLogos = document.querySelectorAll('.hero-card-logo');

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

    brandLogos.forEach(img => {
      img.src = brandLogoSrc;
    });

    heroLogos.forEach(img => {
      img.src = heroLogoSrc;
    });

    // Update button icons
    themeToggleBtns.forEach(btn => {
      btn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
      btn.innerHTML = theme === 'dark'
        ? `<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 00-1.41 0 .996.996 0 000 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 000-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 000-1.41.996.996 0 00-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 000-1.41.996.996 0 00-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>`
        : `<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0012.3 2zm-.3 18a8 8 0 110-16 8.3 8.3 0 011.7.2 8 8 0 00-1.9 7.8 8 8 0 007.8 8c-.5 0-1.1 0-1.6-.0z"/></svg>`;
    });
  }

  const initialTheme = localStorage.getItem(THEME_KEY) || getSystemTheme();
  applyTheme(initialTheme);

  themeToggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  });

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem(THEME_KEY)) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // --- Mobile Drawer Navigation ---
  const mobileToggleBtn = document.querySelector('.mobile-toggle-btn');
  const mobileDrawer = document.querySelector('.mobile-drawer');

  if (mobileToggleBtn && mobileDrawer) {
    function toggleDrawer(open) {
      const isOpen = open !== undefined ? open : !mobileDrawer.classList.contains('open');
      mobileDrawer.classList.toggle('open', isOpen);
      mobileToggleBtn.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }

    mobileToggleBtn.addEventListener('click', () => toggleDrawer());

    // Close when clicking nav link
    const mobileLinks = mobileDrawer.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => toggleDrawer(false));
    });

    // Close when clicking outside
    document.addEventListener('click', e => {
      if (
        mobileDrawer.classList.contains('open') &&
        !mobileDrawer.contains(e.target) &&
        !mobileToggleBtn.contains(e.target)
      ) {
        toggleDrawer(false);
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && mobileDrawer.classList.contains('open')) {
        toggleDrawer(false);
      }
    });
  }

  // --- Active Nav Link Highlight on Scroll ---
  const sections = document.querySelectorAll('section[id]');
  const desktopNavLinks = document.querySelectorAll('.nav-desktop .nav-item a');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-item a');

  if (sections.length > 0 && ('IntersectionObserver' in window)) {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            const updateLinks = links => {
              links.forEach(link => {
                const href = link.getAttribute('href');
                if (href === `#${id}` || href.endsWith(`#${id}`)) {
                  link.classList.add('active');
                } else if (href.startsWith('#')) {
                  link.classList.remove('active');
                }
              });
            };
            updateLinks(desktopNavLinks);
            updateLinks(mobileNavLinks);
          }
        });
      },
      {
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0
      }
    );

    sections.forEach(sec => observer.observe(sec));
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

})();
