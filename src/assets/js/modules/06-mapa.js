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

  
