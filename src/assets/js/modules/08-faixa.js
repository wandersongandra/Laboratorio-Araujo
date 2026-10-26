/* ---------- 8. Faixa de fotos: botão pausar/continuar (também pausa com mouse ou foco, via CSS) ---------- */
  $$('[data-strip-toggle]').forEach(b => b.addEventListener('click', () => {
    const s = b.closest('.strip'), p = s.classList.toggle('is-paused');
    b.setAttribute('aria-pressed', p); b.textContent = p ? 'Continuar' : 'Pausar';
  }));

  
