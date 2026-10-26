/**
 * Laboratório Dental Araújo — interações do site (JavaScript puro, sem dependências).
 *
 * Carregado com `defer` em todas as páginas. A classe `js` no <html> é colocada por um
 * script inline mínimo no <head> (permitido na CSP por hash SHA-256, ver _build/build.py),
 * e é ela que ativa as animações de revelação no CSS; sem JavaScript, tudo aparece normal.
 *
 * Módulos (cada um só age se encontrar seus elementos na página):
 *   1. Rastreamento   – cliques em [data-track] vão para window.dataLayer (GA4/GTM, se instalado).
 *   2. Âncoras        – rolagem suave para links internos "#id".
 *   3. Cabeçalho      – estado "is-stuck"/"is-hidden" ao rolar, submenu "Serviços",
 *                       menu mobile (#burger/#nav, tecla Esc) e link ativo (aria-current).
 *   4. Revelações     – IntersectionObserver adiciona `.in` em .rv / .rv-img.
 *   5. Índice         – miniatura do índice de serviços acompanha o cursor (desktop).
 *   6. Mapa           – o iframe do Google Maps só é criado quando o usuário pede (#loadMap).
 *  12. Galeria        – ampliação das fotos de /trabalhos/ num <dialog> (teclado, foco, setas).
 *
 * Segurança: o script não insere HTML vindo do usuário nem da URL; o único elemento
 * criado dinamicamente é o iframe do mapa, com endereço fixo e sandbox. A galeria só troca o
 * src/alt de uma <img> existente por URLs do próprio site (atributos data-lb gerados no build).
 * Movimento: com `prefers-reduced-motion: reduce` não há animações nem rolagem suave.
 */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const yr = $('#year'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- 1. Rastreamento de conversões (GA4 / GTM) ---------- */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', e => {
    const el = e.target.closest('[data-track]'); if (!el) return;
    window.dataLayer.push({ event: 'lead_click', lead_type: el.dataset.track });
    if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { method: el.dataset.track });
  });

  /* ---------- 2. Âncoras ---------- */
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const t = document.getElementById(id.slice(1)); if (!t) return;
    e.preventDefault(); t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); history.replaceState(null, '', id);
  }));

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

  /* ---------- 4. Revelações discretas ao rolar ---------- */
  const rv = $$('.rv, .rv-img');
  if (!reduce && 'IntersectionObserver' in window) {
    // .rv-img começa recortado (clip-path) e não "intersecta": observa-se o elemento pai
    const map = new Map();
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { (map.get(e.target) || []).forEach(x => x.classList.add('in')); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(el => { const o = el.classList.contains('rv-img') ? el.parentElement : el; if (!map.has(o)) { map.set(o, []); io.observe(o); } map.get(o).push(el); });
  } else rv.forEach(el => el.classList.add('in'));

  /* ---------- 5. Índice de serviços: miniatura acompanha o cursor (desktop) ---------- */
  const idx = $('.idx');
  if (idx && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce) {
    idx.addEventListener('pointermove', e => {
      const row = e.target.closest('.idx__row'); if (!row) return;
      const r = row.getBoundingClientRect();
      row.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  }

  /* ---------- 6. Mapa sob demanda (nada é carregado do Google antes do clique) ---------- */
  $('#loadMap')?.addEventListener('click', () => {
    const m = $('#map'), f = document.createElement('iframe');
    f.title = 'Mapa: Laboratório Dental Araújo, Av. Afonso Pena 262, Belo Horizonte';
    f.loading = 'lazy'; f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox');
    f.src = 'https://www.google.com/maps?q=Laborat%C3%B3rio+Dental+Ara%C3%BAjo,+Av.+Afonso+Pena,+262+-+sala+1602,+Belo+Horizonte+-+MG&ll=-19.9162258,-43.9407838&z=17&output=embed';
    m.replaceChildren(f);
    const note = document.getElementById('mapNote'); if (note) note.textContent = 'Mapa: Google Maps';
  });

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

  /* ---------- 8. Faixa de fotos: botão pausar/continuar (também pausa com mouse ou foco, via CSS) ---------- */
  $$('[data-strip-toggle]').forEach(b => b.addEventListener('click', () => {
    const s = b.closest('.strip'), p = s.classList.toggle('is-paused');
    b.setAttribute('aria-pressed', p); b.textContent = p ? 'Continuar' : 'Pausar';
  }));

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

  /* ---------- 10. Acordeões: abrem quando o link aponta para dentro deles; tudo aberto na impressão ---------- */
  const openHash = () => { const id = location.hash.slice(1); const t = id ? document.getElementById(decodeURIComponent(id)) : null; const d = t ? t.closest('details') : null; if (d) d.open = true; };
  addEventListener('hashchange', openHash); openHash();
  addEventListener('beforeprint', () => $$('details').forEach(d => { d.open = true; }));

  /* ---------- 11. Antes e depois (desligado até haver pares reais: ver docs/FOTOS.md) ---------- */
  $$('[data-ba]').forEach(f => {
    const r = $('.ba__range', f); if (!r) return;
    const set = () => f.style.setProperty('--x', r.value + '%');
    r.addEventListener('input', set); set(); f.classList.add('ba--on');
  });

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
})();
