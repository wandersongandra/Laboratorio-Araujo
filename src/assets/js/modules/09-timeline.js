/* ---------- 9. Linha do tempo: barra de progresso preenchida conforme a rolagem ---------- */
  const tlw = $('[data-tl]');
  if (tlw) {
    const steps = $$('.tl li', tlw);
    const upd = () => {
      const r = tlw.getBoundingClientRect(), vh = innerHeight;
      const p = reduce ? 1 : Math.max(0, Math.min(1, (vh * .85 - r.top) / (r.height + vh * .35)));
      tlw.style.setProperty('--p', p.toFixed(3));
      steps.forEach((li, i) => li.classList.toggle('on', p >= i / steps.length + .02 || p === 1));
    };
    let tq = false;
    addEventListener('scroll', () => { if (!tq) { tq = true; requestAnimationFrame(() => { upd(); tq = false; }); } }, { passive: true });
    addEventListener('resize', upd, { passive: true });
    upd();
  }

  
