/* ---------- 2. Âncoras ---------- */
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const t = document.getElementById(id.slice(1)); if (!t) return;
    e.preventDefault(); t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); history.replaceState(null, '', id);
  }));

  
