/* ---------- 10. Acordeões: abrem quando o link aponta para dentro deles; tudo aberto na impressão ---------- */
  const openHash = () => { const id = location.hash.slice(1); const t = id ? document.getElementById(decodeURIComponent(id)) : null; const d = t ? t.closest('details') : null; if (d) d.open = true; };
  addEventListener('hashchange', openHash); openHash();
  addEventListener('beforeprint', () => $$('details').forEach(d => { d.open = true; }));

  
