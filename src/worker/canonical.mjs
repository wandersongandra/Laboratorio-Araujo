/**
 * Política do domínio oficial do Laboratório Dental Araújo.
 *
 * O apex https://laboratoriodentalaraujo.com.br é o único canônico.
 * HTTP→HTTPS e www→apex são regras da zona Cloudflare, não deste módulo.
 * Aqui só o workers.dev estável de produção redireciona; qualquer outro host
 * (preview, version URL, deployment) permanece no lugar e sai com noindex.
 */

export const CANONICAL_ORIGIN = 'https://laboratoriodentalaraujo.com.br';
export const CANONICAL_HOST = 'laboratoriodentalaraujo.com.br';
export const LEGACY_HOST = 'laboratorio-araujo.gandratecnologia.workers.dev';
export const PRODUCTION_BRANCH = 'main';
export const REDIRECT_HSTS = 'max-age=31536000';

const REDIRECT_PERMISSIONS_POLICY = 'accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), magnetometer=(), microphone=(), midi=(), payment=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), xr-spatial-tracking=(), browsing-topics=()';

export function normalizeHost(hostname) {
  return String(hostname || '').trim().toLowerCase().replace(/\.+$/, '');
}

export function isPreviewBuild(env = {}) {
  if (String(env.SITE_PREVIEW || '') === '1') return true;
  const branch = String(env.WORKERS_CI_BRANCH || env.CF_PAGES_BRANCH || '').trim();
  return branch !== '' && branch !== PRODUCTION_BRANCH;
}

function parseConfiguredOrigin(value) {
  let url;
  try {
    url = new URL(value);
  } catch {
    return { ok: false, error: `SITE_BASE não é uma URL: ${value}` };
  }
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash || (url.pathname !== '/' && url.pathname !== '')) {
    return { ok: false, error: 'SITE_BASE deve ser uma origem HTTPS, sem caminho, credenciais, query ou fragmento.' };
  }
  return { ok: true, origin: url.origin };
}

export function resolveBuildPolicy(env = {}) {
  const configured = [env.SITE_BASE, env.CF_PAGES_URL]
    .map((value) => String(value || '').trim())
    .filter(Boolean);
  for (const value of configured) {
    const parsed = parseConfiguredOrigin(value);
    if (!parsed.ok) throw new Error(parsed.error);
    if (parsed.origin !== CANONICAL_ORIGIN) {
      throw new Error(`SITE_BASE deve ser ${CANONICAL_ORIGIN}. Recebido: ${parsed.origin}.`);
    }
  }
  const preview = isPreviewBuild(env);
  return { origin: CANONICAL_ORIGIN, indexable: !preview, preview };
}

export function toCanonicalUrl(url) {
  const path = `${url.pathname || '/'}${url.search || ''}`;
  if (!path.startsWith('/') || path.startsWith('//') || path.includes('\\') || path.includes('\0')) return null;
  if (/(^|\/)\.\.(\/|$)/.test(path)) return null;
  const location = `${CANONICAL_ORIGIN}${path}`;
  const check = new URL(location);
  if (check.origin !== CANONICAL_ORIGIN) return null;
  if (`${check.pathname}${check.search}` !== path) return null;
  return location;
}

export function classifyRequest(url, method) {
  const host = normalizeHost(url.hostname);
  if (host === CANONICAL_HOST) return { action: 'pass' };
  if (host === LEGACY_HOST && (method === 'GET' || method === 'HEAD')) {
    const location = toCanonicalUrl(url);
    if (location) return { action: 'redirect', location };
  }
  return { action: 'noindex' };
}

export function redirectHeaders(location) {
  return {
    Location: location,
    'Content-Security-Policy': "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
    'Strict-Transport-Security': REDIRECT_HSTS,
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': REDIRECT_PERMISSIONS_POLICY,
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Resource-Policy': 'same-origin',
    'X-Permitted-Cross-Domain-Policies': 'none',
    'Cache-Control': 'public, max-age=300',
  };
}

export async function handleRequest(request, env) {
  const url = new URL(request.url);
  const decision = classifyRequest(url, request.method);
  if (decision.action === 'redirect') {
    return new Response(null, { status: 301, headers: redirectHeaders(decision.location) });
  }
  const asset = await env.ASSETS.fetch(request);
  if (decision.action !== 'noindex') return asset;
  const headers = new Headers(asset.headers);
  const robots = headers.get('X-Robots-Tag') || '';
  if (!/noindex/i.test(robots)) headers.set('X-Robots-Tag', 'noindex, nofollow');
  return new Response(asset.body, { status: asset.status, statusText: asset.statusText, headers });
}
