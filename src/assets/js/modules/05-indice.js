/* No desktop, a miniatura do índice segue o ponteiro. */
  const idx = $('.idx');
  if (idx && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce) {
    idx.addEventListener('pointermove', e => {
      const row = e.target.closest('.idx__row'); if (!row) return;
      const r = row.getBoundingClientRect();
      row.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  }

  
