/* ---------- 13. Imagens de destaque: revelar somente após o carregamento ---------- */
  $$('.curtain').forEach(frame => {
    const img = $('img', frame);
    const reveal = () => frame.classList.add('curtain--ready');
    if (!img || img.complete) reveal();
    else {
      img.addEventListener('load', reveal, { once: true });
      img.addEventListener('error', reveal, { once: true });
    }
  });
