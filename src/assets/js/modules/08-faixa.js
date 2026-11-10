/* O botão pausa a faixa. O CSS também pausa no mouse e no foco. */
  $$('[data-strip-toggle]').forEach(b => b.addEventListener('click', () => {
    const s = b.closest('.strip'), p = s.classList.toggle('is-paused');
    b.setAttribute('aria-pressed', p); b.textContent = p ? 'Continuar' : 'Pausar';
  }));

  
