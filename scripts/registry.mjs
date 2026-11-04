/** Cadastro profissional: só publica dados completos e confirmados pelo laboratório. */
function field(data, key) {
  const value = data[key] ?? '';
  if (typeof value !== 'string') throw new Error(`${key} deve ser texto em site.json`);
  return value.trim();
}

export function registryFromSite(data) {
  const technicalLeadName = field(data, 'technicalLeadName');
  const technicalLeadCro = field(data, 'technicalLeadCro');
  const laboratoryCro = field(data, 'laboratoryCro');
  if (Boolean(technicalLeadName) !== Boolean(technicalLeadCro)) {
    throw new Error('Responsável técnico: informe technicalLeadName e technicalLeadCro juntos.');
  }
  return { technicalLeadName, technicalLeadCro, laboratoryCro };
}

function escapeHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}

export function registryMarkup(registry) {
  const { technicalLeadName, technicalLeadCro, laboratoryCro } = registry;
  const entries = [];
  if (laboratoryCro) entries.push(['Inscrição do laboratório', laboratoryCro]);
  if (technicalLeadName) entries.push(['Responsável técnico', `${technicalLeadName} · ${technicalLeadCro}`]);
  return {
    footer: entries.length
      ? `<p class="footer__registry">${entries.map(([label, value]) => `<span><strong>${label}:</strong> ${escapeHtml(value)}</span>`).join('<br>')}</p>`
      : '',
    facts: entries.map(([label, value]) => `<div><dt>${label}</dt><dd>${escapeHtml(value)}</dd></div>`).join(''),
  };
}

/** Acrescenta os registros ao LocalBusiness de cada página, preservando outros nós do grafo. */
export function injectRegistryJsonLd(html, registry) {
  if (!registry.technicalLeadName && !registry.laboratoryCro) return html;
  return html.replace(/(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g, (all, open, json, close) => {
    const data = JSON.parse(json);
    const business = data['@graph']?.find((node) => node['@id']?.endsWith('/#laboratorio'));
    if (!business) return all;
    if (registry.laboratoryCro) {
      business.identifier = { '@type': 'PropertyValue', propertyID: 'CRO-MG', value: registry.laboratoryCro };
    }
    if (registry.technicalLeadName) {
      business.employee = {
        '@type': 'Person', name: registry.technicalLeadName, jobTitle: 'Responsável técnico',
        identifier: { '@type': 'PropertyValue', propertyID: 'CRO-MG', value: registry.technicalLeadCro },
      };
    }
    // Impede que dados cadastrados possam encerrar a tag script no HTML.
    return `${open}${JSON.stringify(data).replaceAll('<', '\\u003c')}${close}`;
  });
}
