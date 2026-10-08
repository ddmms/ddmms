/**
 * Data Driven Materials and Molecular Science (DDMMS)
 * Interactive Publications Engine
 * Based on the group's automated ORCID publication architecture.
 */

(function () {
  'use strict';

  function initPublications(containerId, options = {}) {
    const root = document.getElementById(containerId);
    if (!root) return;

    // Load data from embedded JSON or window global
    let publications = [];
    let authorsDict = {
      "0000-0002-7013-6670": "Alin Marin Elena",
      "0009-0005-2015-9478": "Elliott Kasoar",
      "0000-0001-7374-9352": "Junwen Yin"
    };

    if (window.DDMMS_PUBLICATIONS && Array.isArray(window.DDMMS_PUBLICATIONS)) {
      publications = window.DDMMS_PUBLICATIONS;
    } else {
      const pubsEl = document.getElementById('publications-data');
      if (pubsEl) {
        try {
          publications = JSON.parse(pubsEl.textContent.trim());
        } catch (e) {
          console.error('Failed to parse publications data element', e);
        }
      }
    }

    const authorsEl = document.getElementById('authors-data');
    if (authorsEl) {
      try {
        authorsDict = JSON.parse(authorsEl.textContent.trim());
      } catch (e) {
        // fallback to default
      }
    }

    const nameToOrcid = {};
    for (const [orcid, name] of Object.entries(authorsDict)) {
      nameToOrcid[name] = orcid;
    }

    // DOM Elements in the container
    const authorFilter = root.querySelector('.pub-filter-author');
    const yearFilter = root.querySelector('.pub-filter-year');
    const searchInput = root.querySelector('.pub-filter-search');
    const sortSelect = root.querySelector('.pub-filter-sort');
    const groupYearToggle = root.querySelector('.pub-toggle-group-year');
    const resetBtn = root.querySelector('.pub-reset-btn');
    const pubsContainer = root.querySelector('.pubs-container');
    const visibleCountEl = root.querySelector('.pub-visible-count');
    const totalCountEl = root.querySelector('.pub-total-count');

    // Stats Elements if present
    const statTotalPubs = document.getElementById('stat-total-pubs');
    const statAuthors = document.getElementById('stat-authors');
    const statYears = document.getElementById('stat-years');
    const statVenues = document.getElementById('stat-venues');

    function updateStats() {
      if (statTotalPubs) statTotalPubs.textContent = publications.length;
      if (statAuthors) statAuthors.textContent = Object.keys(authorsDict).length;

      const validYears = publications
        .map(p => parseInt(p.year, 10))
        .filter(y => !isNaN(y));
      if (statYears) {
        if (validYears.length > 0) {
          statYears.textContent = `${Math.min(...validYears)} - ${Math.max(...validYears)}`;
        } else {
          statYears.textContent = 'N/A';
        }
      }

      if (statVenues) {
        const venues = new Set(publications.map(p => p.journal).filter(Boolean));
        statVenues.textContent = venues.size;
      }

      if (totalCountEl) totalCountEl.textContent = publications.length;
    }

    function populateAuthorDropdown() {
      if (!authorFilter) return;
      const authorCounts = {};
      for (const name of Object.values(authorsDict)) {
        authorCounts[name] = 0;
      }
      for (const pub of publications) {
        for (const a of (pub.authors || [])) {
          if (authorCounts[a] !== undefined) {
            authorCounts[a]++;
          }
        }
      }

      for (const [name, count] of Object.entries(authorCounts)) {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = `${name} (${count})`;
        authorFilter.appendChild(opt);
      }
    }

    function updateYearDropdown(selectedAuthor = null) {
      if (!yearFilter) return;
      if (!selectedAuthor && authorFilter) {
        selectedAuthor = authorFilter.value;
      }

      const relevantPubs = (selectedAuthor && selectedAuthor !== 'all')
        ? publications.filter(p => p.authors && p.authors.includes(selectedAuthor))
        : publications;

      const yearCounts = {};
      for (const pub of relevantPubs) {
        const yr = pub.year || 'Unknown';
        yearCounts[yr] = (yearCounts[yr] || 0) + 1;
      }

      const sortedYears = Object.keys(yearCounts).sort((a, b) => {
        if (a === 'Unknown') return 1;
        if (b === 'Unknown') return -1;
        return parseInt(b, 10) - parseInt(a, 10);
      });

      const previousYear = yearFilter.value;
      yearFilter.innerHTML = '';

      const allOpt = document.createElement('option');
      allOpt.value = 'all';
      allOpt.textContent = selectedAuthor !== 'all' ? `All Years (${relevantPubs.length})` : 'All Years';
      yearFilter.appendChild(allOpt);

      for (const yr of sortedYears) {
        const opt = document.createElement('option');
        opt.value = yr;
        opt.textContent = `${yr} (${yearCounts[yr]})`;
        yearFilter.appendChild(opt);
      }

      if (previousYear && previousYear !== 'all' && yearCounts[previousYear] !== undefined) {
        yearFilter.value = previousYear;
      } else {
        yearFilter.value = 'all';
      }
    }

    function copyToClipboard(text, successMsg) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          if (window.showToast) window.showToast(successMsg);
        }).catch(() => {
          fallbackCopy(text, successMsg);
        });
      } else {
        fallbackCopy(text, successMsg);
      }
    }

    function fallbackCopy(text, successMsg) {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      if (window.showToast) window.showToast(successMsg);
    }

    function generateBibtex(pub) {
      const firstAuthor = (pub.authors && pub.authors[0]) ? pub.authors[0].split(' ').pop().toLowerCase() : 'pub';
      const year = (pub.year && pub.year !== 'Unknown') ? pub.year : 'date';
      const keyDoi = pub.doi ? pub.doi.replace(/[^a-zA-Z0-9]/g, '') : '';
      const key = `${firstAuthor}${year}${keyDoi.slice(-4)}`;
      let bib = `@article{${key},\n`;
      bib += `  title = {${(pub.title || '').replace(/{/g, '\\{').replace(/}/g, '\\}')}},\n`;
      if (pub.authors && pub.authors.length > 0) {
        bib += `  author = {${pub.authors.join(' and ')}},\n`;
      }
      if (pub.journal) {
        bib += `  journal = {${pub.journal}},\n`;
      }
      if (pub.year && pub.year !== 'Unknown') {
        bib += `  year = {${pub.year}},\n`;
      }
      if (pub.doi) {
        bib += `  doi = {${pub.doi}},\n`;
        bib += `  url = {https://doi.org/${pub.doi}},\n`;
      } else if (pub.url) {
        bib += `  url = {${pub.url}},\n`;
      }
      bib += `}`;
      return bib;
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function createPubCard(pub) {
      const card = document.createElement('article');
      card.className = 'pub-card';

      // Title
      const titleEl = document.createElement('h3');
      titleEl.className = 'pub-title';
      const cleanDoi = pub.doi ? pub.doi.replace(/^https?:\/\/(dx\.)?doi\.org\//i, '').replace(/^doi:\s*/i, '').trim() : '';
      const pubUrl = cleanDoi ? `https://doi.org/${cleanDoi}` : (pub.url || null);

      if (pubUrl) {
        const a = document.createElement('a');
        a.href = pubUrl;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = pub.title;
        titleEl.appendChild(a);
      } else {
        titleEl.textContent = pub.title;
      }
      card.appendChild(titleEl);

      // Meta (Authors, Venue, Badges)
      const metaEl = document.createElement('div');
      metaEl.className = 'pub-meta';

      if (pub.authors && pub.authors.length > 0) {
        const authorsWrapper = document.createElement('div');
        authorsWrapper.className = 'pub-authors';
        for (const author of pub.authors) {
          const chip = document.createElement('span');
          chip.className = 'author-chip';
          chip.title = `Filter by ${author}`;
          chip.innerHTML = `
            <svg class="orcid-icon" viewBox="0 0 256 256">
              <path d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/>
              <path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 62.2c-5.5 0-10-4.5-10-10s4.5-10 10-10 10 4.5 10 10-4.5 10-10 10zm108.8 77.8c0 27.8-19.8 46.2-49.9 46.2H108V79.1h31.6c28.2 0 47.8 19.5 47.8 46.5v14.4zm-16.1-.7c0-20.7-13.8-32.9-33.1-32.9h-14.7v72.8h14.7c20 0 33.1-13.1 33.1-34.1v-5.8z"/>
            </svg>
            <span>${escapeHtml(author)}</span>
          `;
          chip.addEventListener('click', (e) => {
            e.preventDefault();
            if (authorFilter) {
              authorFilter.value = author;
              updateYearDropdown(author);
              render();
            }
          });
          authorsWrapper.appendChild(chip);
        }
        metaEl.appendChild(authorsWrapper);
      }

      if (pub.journal) {
        const venueEl = document.createElement('span');
        venueEl.className = 'pub-venue';
        venueEl.textContent = pub.journal;
        metaEl.appendChild(venueEl);
      }

      if (pub.year) {
        const yearBadge = document.createElement('span');
        yearBadge.className = 'badge badge-year';
        yearBadge.textContent = pub.year;
        metaEl.appendChild(yearBadge);
      }

      if (pub.type && pub.type !== 'other') {
        const typeBadge = document.createElement('span');
        typeBadge.className = 'badge';
        typeBadge.textContent = pub.type.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        metaEl.appendChild(typeBadge);
      }

      if (cleanDoi) {
        const doiBadge = document.createElement('a');
        doiBadge.className = 'badge badge-doi';
        doiBadge.href = `https://doi.org/${cleanDoi}`;
        doiBadge.target = '_blank';
        doiBadge.rel = 'noopener noreferrer';
        doiBadge.textContent = `DOI: ${cleanDoi}`;
        metaEl.appendChild(doiBadge);
      }

      card.appendChild(metaEl);

      // Action Buttons
      const actionsEl = document.createElement('div');
      actionsEl.className = 'pub-actions';

      const btnCite = document.createElement('button');
      btnCite.className = 'btn-action';
      btnCite.innerHTML = '<span>📋</span> Copy Citation';
      btnCite.addEventListener('click', () => {
        const authorStr = (pub.authors && pub.authors.length > 0) ? pub.authors.join(', ') : 'DDMMS Group';
        const venueStr = pub.journal ? ` *${pub.journal}*` : '';
        const doiStr = cleanDoi ? ` https://doi.org/${cleanDoi}` : (pub.url ? ` ${pub.url}` : '');
        const citation = `${authorStr} (${pub.year || 'n.d.'}). ${pub.title}.${venueStr}.${doiStr}`;
        copyToClipboard(citation, 'Citation copied to clipboard!');
      });
      actionsEl.appendChild(btnCite);

      if (cleanDoi) {
        const btnDoi = document.createElement('button');
        btnDoi.className = 'btn-action';
        btnDoi.innerHTML = '<span>🔗</span> Copy DOI';
        btnDoi.addEventListener('click', () => {
          copyToClipboard(`https://doi.org/${cleanDoi}`, 'DOI URL copied to clipboard!');
        });
        actionsEl.appendChild(btnDoi);
      }

      const btnBib = document.createElement('button');
      btnBib.className = 'btn-action';
      btnBib.innerHTML = '<span>📑</span> BibTeX';
      btnBib.addEventListener('click', () => {
        const bibtex = generateBibtex(pub);
        copyToClipboard(bibtex, 'BibTeX entry copied to clipboard!');
      });
      actionsEl.appendChild(btnBib);

      card.appendChild(actionsEl);
      return card;
    }

    function render() {
      if (!pubsContainer) return;

      const selectedAuthor = authorFilter ? authorFilter.value : 'all';
      const selectedYear = yearFilter ? yearFilter.value : 'all';
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      const sortVal = sortSelect ? sortSelect.value : 'year-desc';
      const shouldGroup = groupYearToggle ? groupYearToggle.checked : true;

      let filtered = publications.filter(pub => {
        if (selectedAuthor !== 'all' && (!pub.authors || !pub.authors.includes(selectedAuthor))) {
          return false;
        }
        if (selectedYear !== 'all' && String(pub.year) !== String(selectedYear)) {
          return false;
        }
        if (query !== '') {
          const title = (pub.title || '').toLowerCase();
          const journal = (pub.journal || '').toLowerCase();
          const doi = (pub.doi || '').toLowerCase();
          const authors = (pub.authors || []).join(' ').toLowerCase();
          if (!title.includes(query) && !journal.includes(query) && !doi.includes(query) && !authors.includes(query)) {
            return false;
          }
        }
        return true;
      });

      // Sorting
      filtered.sort((a, b) => {
        const yA = parseInt(a.year, 10) || 0;
        const yB = parseInt(b.year, 10) || 0;
        if (sortVal === 'year-desc') {
          if (yB !== yA) return yB - yA;
          return (a.title || '').localeCompare(b.title || '');
        } else if (sortVal === 'year-asc') {
          if (yA !== yB) return yA - yB;
          return (a.title || '').localeCompare(b.title || '');
        } else if (sortVal === 'title-asc') {
          return (a.title || '').localeCompare(b.title || '');
        }
        return 0;
      });

      if (options.limit && options.limit > 0 && selectedAuthor === 'all' && selectedYear === 'all' && query === '') {
        filtered = filtered.slice(0, options.limit);
      }

      if (visibleCountEl) visibleCountEl.textContent = filtered.length;
      pubsContainer.innerHTML = '';

      if (filtered.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.innerHTML = `
          <h3>No publications found</h3>
          <p>Try clearing or broadening your search query and filters.</p>
        `;
        pubsContainer.appendChild(empty);
        return;
      }

      if (shouldGroup && (!options.limit || filtered.length > 10)) {
        // Group by year
        const groups = {};
        for (const pub of filtered) {
          const yr = pub.year || 'Unknown';
          if (!groups[yr]) groups[yr] = [];
          groups[yr].push(pub);
        }

        const sortedGroupYears = Object.keys(groups).sort((a, b) => {
          if (sortVal === 'year-asc') {
            if (a === 'Unknown') return 1;
            if (b === 'Unknown') return -1;
            return parseInt(a, 10) - parseInt(b, 10);
          } else {
            if (a === 'Unknown') return 1;
            if (b === 'Unknown') return -1;
            return parseInt(b, 10) - parseInt(a, 10);
          }
        });

        for (const yr of sortedGroupYears) {
          const sec = document.createElement('section');
          sec.className = 'year-section';

          const hdr = document.createElement('h3');
          hdr.className = 'year-header';
          hdr.innerHTML = `<span>${yr}</span> <span class="year-count-badge">${groups[yr].length}</span>`;
          sec.appendChild(hdr);

          const list = document.createElement('div');
          list.className = 'pubs-list';
          for (const pub of groups[yr]) {
            list.appendChild(createPubCard(pub));
          }
          sec.appendChild(list);
          pubsContainer.appendChild(sec);
        }
      } else {
        const list = document.createElement('div');
        list.className = 'pubs-list';
        for (const pub of filtered) {
          list.appendChild(createPubCard(pub));
        }
        pubsContainer.appendChild(list);
      }
    }

    // Event listeners
    if (authorFilter) {
      authorFilter.addEventListener('change', () => {
        updateYearDropdown(authorFilter.value);
        render();
      });
    }
    if (yearFilter) yearFilter.addEventListener('change', render);
    if (searchInput) searchInput.addEventListener('input', render);
    if (sortSelect) sortSelect.addEventListener('change', render);
    if (groupYearToggle) groupYearToggle.addEventListener('change', render);

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (authorFilter) authorFilter.value = 'all';
        updateYearDropdown('all');
        if (yearFilter) yearFilter.value = 'all';
        if (searchInput) searchInput.value = '';
        if (sortSelect) sortSelect.value = 'year-desc';
        if (groupYearToggle) groupYearToggle.checked = true;
        render();
      });
    }

    // Initialization
    updateStats();
    populateAuthorDropdown();
    updateYearDropdown('all');
    render();
  }

  window.initPublications = initPublications;
})();

