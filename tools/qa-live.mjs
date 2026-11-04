/** Smoke test do site publicado; não altera o ambiente remoto. */
const base = (process.argv[2] || process.env.SITE_BASE || '').replace(/\/$/, '');
if (!base) throw new Error('Informe SITE_BASE ou passe a URL como argumento.');
const origin = new URL(base);
if (origin.pathname !== '/' || origin.search || origin.hash ||
    (origin.protocol !== 'https:' && origin.hostname !== '127.0.0.1' && origin.hostname !== 'localhost')) {
  throw new Error('Passe apenas a origem HTTPS do site (HTTP é permitido somente em localhost).');
}

const failures = [];
const fail = (message) => { failures.push(message); console.error(`  ✗ ${message}`); };
const get = async (path, options = {}) => {
  try {
    return await fetch(`${base}${path}`, {
      redirect: 'manual', signal: AbortSignal.timeout(12_000), ...options,
    });
  } catch (error) {
    fail(`${path}: falha de rede (${error.message})`);
    return { status: 0, text: async () => '', headers: { get: () => null } };
  }
};

const sitemapResponse = await get('/sitemap.xml');
if (sitemapResponse.status !== 200) fail(`/sitemap.xml → ${sitemapResponse.status}`);
const sitemap = await sitemapResponse.text();
const locations = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1]);
if (!locations.length) fail('/sitemap.xml sem URLs');
if (locations.length !== new Set(locations).size) fail('/sitemap.xml contém URLs duplicadas');

await Promise.all(locations.map(async (location) => {
  let target;
  try { target = new URL(location); }
  catch { fail(`sitemap: URL inválida: ${location}`); return; }
  if (target.origin !== origin.origin) { fail(`sitemap: host inesperado: ${location}`); return; }
  const path = target.pathname;
  const response = await get(path);
  if (response.status !== 200) { fail(`${path} → ${response.status}`); return; }
  const html = await response.text();
  if (!html.includes(`<link rel="canonical" href="${location}"`)) fail(`${path}: canonical divergente`);
}));

const notFound = await get('/qa-pagina-inexistente/');
if (notFound.status !== 404) fail(`404 → ${notFound.status}`);
const expectedHeaders = {
  'content-security-policy': /frame-ancestors 'none'/,
  'strict-transport-security': /^max-age=\d+$/,
  'x-content-type-options': /^nosniff$/,
  'x-frame-options': /^DENY$/,
  'referrer-policy': /^strict-origin-when-cross-origin$/,
  'permissions-policy': /camera=\(\)/,
  'cross-origin-opener-policy': /^same-origin$/,
  'cross-origin-resource-policy': /^same-origin$/,
  'x-permitted-cross-domain-policies': /^none$/,
};
for (const path of ['/', '/contato/', '/assets/fonts/plex-sans.woff2', '/qa-pagina-inexistente/']) {
  const response = await get(path);
  for (const [header, pattern] of Object.entries(expectedHeaders)) {
    const value = response.headers.get(header);
    // Header repetido chega aqui unido por ", " — sinal de regra duplicada.
    if (!value) fail(`${path}: header ausente: ${header}`);
    else if (!pattern.test(value)) fail(`${path}: ${header} inesperado: ${value}`);
  }
  if (/unsafe-eval|unsafe-inline/.test(response.headers.get('content-security-policy') || '')) fail(`${path}: CSP fraca`);
}

for (const path of ['/_headers', '/_redirects', '/.assetsignore', '/.env', '/.dev.vars', '/package.json', '/wrangler.jsonc', '/.git/config', '/README.md', '/assets/js/main.js.map']) {
  const response = await get(path);
  if (response.status !== 404) fail(`${path} deveria ser 404 e respondeu ${response.status}`);
}

const legacy = await get('/tabela-de-precos/');
if (legacy.status !== 301 || !legacy.headers.get('location')?.endsWith('/contato/')) {
  fail(`/tabela-de-precos/ → ${legacy.status} ${legacy.headers.get('location') || ''}`);
}
const oldPdf = await get('/assets/docs/tabela-precos-2026.pdf');
if (oldPdf.status === 200) fail('PDF antigo ainda responde 200');

console.log(`\n${failures.length} falha(s); ${locations.length} URLs verificadas`);
process.exit(failures.length ? 1 : 0);
