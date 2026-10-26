/* ---------- 14. Barra de leitura no topo ---------- */
  if (!reduce) {
    const line = document.createElement('div');
    line.className = 'scroll-line';
    line.setAttribute('aria-hidden', 'true');
    document.body.prepend(line);
    let raf = 0;
    const paint = () => {
      raf = 0;
      const max = document.documentElement.scrollHeight - innerHeight;
      const p = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
      line.style.setProperty('--p', p.toFixed(4));
    };
    addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(paint); }, { passive: true });
    paint();
  }
