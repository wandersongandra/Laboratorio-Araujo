/* ---------- 10. Acordeões: abrem quando o link aponta para dentro deles; tudo aberto na impressão ---------- */
  const decodeHash = raw => { try { return decodeURIComponent(raw); } catch { return ''; } };
  const openHash = () => { const id = decodeHash(location.hash.slice(1)); const t = id ? document.getElementById(id) : null; const d = t ? t.closest('details') : null; if (d) d.open = true; };
  addEventListener('hashchange', openHash); openHash();
  addEventListener('beforeprint', () => $$('details').forEach(d => { d.open = true; }));

  
