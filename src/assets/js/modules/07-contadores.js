/* ---------- 7. Contadores (números da home): contam até o valor real ao entrar na tela ---------- */
  // O HTML já traz o número final (visível sem JS e para buscadores); aqui só se anima a contagem.
  const cnt = $$('[data-count]');
  if (cnt.length && !reduce && 'IntersectionObserver' in window) {
    const run = el => {
      const to = +el.dataset.count, t0 = performance.now(), dur = 1400;
      const tick = t => { const k = Math.min(1, (t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    };
    cnt.forEach(el => { el.textContent = '0'; });
    const ioc = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { run(e.target); ioc.unobserve(e.target); } }), { threshold: .6 });
    cnt.forEach(el => ioc.observe(el));
  }

  
