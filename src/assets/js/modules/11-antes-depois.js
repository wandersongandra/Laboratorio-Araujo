/* ---------- 11. Antes e depois (desligado até haver pares reais: ver docs/FOTOS.md) ---------- */
  $$('[data-ba]').forEach(f => {
    const r = $('.ba__range', f); if (!r) return;
    const set = () => f.style.setProperty('--x', r.value + '%');
    r.addEventListener('input', set); set(); f.classList.add('ba--on');
  });

  
