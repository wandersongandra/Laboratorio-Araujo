/* ---------- 3. Cabeçalho, submenu e menu mobile ---------- */
  const header = $('.header'), nav = $('#nav'), burger = $('#burger');
  let lastY = 0, ticking = false;
  const onScroll = () => {
    const y = scrollY;
    header.classList.toggle('is-stuck', y > 8);
    const hide = y > 600 && y > lastY + 6 && !nav.classList.contains('open');
    if (hide) header.classList.add('is-hidden'); else if (y < lastY - 6 || y < 600) header.classList.remove('is-hidden');
    lastY = y; ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  $$('.nav__more').forEach(b => b.addEventListener('click', () => {
    const g = b.closest('.nav__group'); const o = g.classList.toggle('open'); b.setAttribute('aria-expanded', o);
  }));
  document.addEventListener('click', e => { $$('.nav__group.open').forEach(g => { if (!g.contains(e.target)) { g.classList.remove('open'); $('.nav__more', g).setAttribute('aria-expanded', false); } }); });

  const setMenu = open => {
    nav.classList.toggle('open', open); burger.classList.toggle('open', open);
    document.documentElement.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open); burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  $$('a', nav).forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') { setMenu(false); $$('.nav__group.open').forEach(g => g.classList.remove('open')); } });

  const path = location.pathname.replace(/index\.html$/, '');
  $$('a[data-nav]', nav).forEach(a => { const h = a.getAttribute('href'); if (h !== '/' ? path.startsWith(h) : path === '/') { a.classList.add('active'); a.setAttribute('aria-current', 'page'); } });

  
