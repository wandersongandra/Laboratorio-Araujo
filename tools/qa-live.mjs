/** Smoke test do site publicado; não altera o ambiente remoto. */
const base = (process.argv[2] || process.env.SITE_BASE || '').replace(/\/$/, '');
if (!base) throw new Error('Informe SITE_BASE ou passe a URL como argumento.');

const failures = [];
const fail = (message) => { failures.push(message); console.error(`  ✗ ${message}`); };
const get = (path, options = {}) => fetch(`${base}${path}`, { redirect: 'manual', ...options });

const sitemapResponse = await get('/sitemap.xml');
if (sitemapResponse.status !== 200) fail(`/sitemap.xml → ${sitemapResponse.status}`);
const sitemap = await sitemapResponse.text();
const locations = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1]);

for (const location of locations) {
  const path = new URL(location).pathname;
  const response = await get(path);
  if (response.status !== 200) { fail(`${path} → ${response.status}`); continue; }
  const html = await response.text();
  if (!html.includes(`<link rel="canonical" href="${location}"`)) fail(`${path}: canonical divergente`);
}

const notFound = await get('/qa-pagina-inexistente/');
if (notFound.status !== 404) fail(`404 → ${notFound.status}`);
const headers = await get('/');
for (const header of ['content-security-policy', 'x-content-type-options', 'x-frame-options', 'referrer-policy']) {
  if (!headers.headers.has(header)) fail(`header ausente: ${header}`);
}

const legacy = await get('/tabela-de-precos/');
if (legacy.status !== 301 || !legacy.headers.get('location')?.endsWith('/contato/')) {
  fail(`/tabela-de-precos/ → ${legacy.status} ${legacy.headers.get('location') || ''}`);
}
const oldPdf = await get('/assets/docs/tabela-precos-2026.pdf');
if (oldPdf.status === 200) fail('PDF antigo ainda responde 200');

console.log(`\n${failures.length} falha(s); ${locations.length} URLs verificadas`);
process.exit(failures.length ? 1 : 0);
