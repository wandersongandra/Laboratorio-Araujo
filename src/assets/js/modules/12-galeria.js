/* ---------- 12. Galeria /trabalhos/: ampliação acessível em <dialog> ---------- */
  // Sem JS (ou sem <dialog>), cada foto é um link comum para o JPEG grande.
  const lb = $('[data-lb-dialog]'), shots = $$('[data-lb]');
  if (lb && shots.length && typeof lb.showModal === 'function') {
    const im = $('.lb__img', lb), txt = $('[data-lb-text]', lb), num = $('[data-lb-n]', lb);
    let cur = 0, opener = null;
    const show = i => {
      cur = (i + shots.length) % shots.length;
      const a = shots[cur], src = $('img', a);
      im.src = a.dataset.lb; im.alt = src ? src.alt : '';
      txt.textContent = a.dataset.cap || ''; num.textContent = `${cur + 1} / ${shots.length}`;
    };
    shots.forEach((a, i) => a.addEventListener('click', e => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.button > 0) return;
      e.preventDefault(); opener = a; show(i); lb.showModal(); $('[data-lb-close]', lb).focus();
    }));
    $('[data-lb-prev]', lb).addEventListener('click', () => show(cur - 1));
    $('[data-lb-next]', lb).addEventListener('click', () => show(cur + 1));
    $('[data-lb-close]', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
    });
    lb.addEventListener('close', () => { im.removeAttribute('src'); if (opener) opener.focus(); });
  }
