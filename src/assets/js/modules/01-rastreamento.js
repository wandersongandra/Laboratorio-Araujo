/* ---------- 1. Rastreamento de conversões (GA4 / GTM) ---------- */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', e => {
    const el = e.target.closest('[data-track]'); if (!el) return;
    window.dataLayer.push({ event: 'lead_click', lead_type: el.dataset.track });
    if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { method: el.dataset.track });
  });

  
