/* ---------- 4. Revelações discretas ao rolar ---------- */
  const rv = $$('.rv, .rv-img');
  if (!reduce && 'IntersectionObserver' in window) {
    // .rv-img começa recortado (clip-path) e não "intersecta": observa-se o elemento pai
    const map = new Map();
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { (map.get(e.target) || []).forEach(x => x.classList.add('in')); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(el => { const o = el.classList.contains('rv-img') ? el.parentElement : el; if (!map.has(o)) { map.set(o, []); io.observe(o); } map.get(o).push(el); });
  } else rv.forEach(el => el.classList.add('in'));

  const wa = $('.wa'), footer = $('.footer');
  if (wa && footer && 'IntersectionObserver' in window) {
    const waObserver = new IntersectionObserver(([entry]) => {
      wa.classList.toggle('wa--hidden', entry.isIntersecting);
    }, { threshold: .08 });
    waObserver.observe(footer);
  }

  
