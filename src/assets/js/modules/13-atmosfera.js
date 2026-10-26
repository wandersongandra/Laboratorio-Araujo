/* ---------- 13. Atmosfera: luz e inclinação nas fotos de destaque ---------- */
  const stages = $$('.hero, .phero--photo');
  if (!reduce && stages.length && matchMedia('(pointer: fine)').matches) {
    stages.forEach(stage => {
      const media = $('.hero__media, .phero__media', stage);
      if (!media) return;
      let raf = 0;
      let px = 62;
      let py = 28;
      let tx = 0;
      let ty = 0;
      const paint = () => {
        raf = 0;
        media.style.setProperty('--px', px + '%');
        media.style.setProperty('--py', py + '%');
        media.style.setProperty('--tx', tx.toFixed(2) + 'deg');
        media.style.setProperty('--ty', ty.toFixed(2) + 'deg');
      };
      stage.addEventListener('pointermove', ev => {
        const box = media.getBoundingClientRect();
        if (!box.width || !box.height) return;
        const x = (ev.clientX - box.left) / box.width;
        const y = (ev.clientY - box.top) / box.height;
        px = Math.min(100, Math.max(0, x * 100));
        py = Math.min(100, Math.max(0, y * 100));
        tx = (x - 0.5) * 7;
        ty = (0.5 - y) * 5;
        if (!raf) raf = requestAnimationFrame(paint);
      }, { passive: true });
      stage.addEventListener('pointerleave', () => {
        px = 62;
        py = 28;
        tx = 0;
        ty = 0;
        if (!raf) raf = requestAnimationFrame(paint);
      });
    });
  }
