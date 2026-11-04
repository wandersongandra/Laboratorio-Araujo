/** URLs de produção usam somente uma origem HTTPS, nunca um subdiretório ou um host relativo. */
export const DEFAULT_SITE_BASE = 'https://laboratorio-araujo.gandratecnologia.workers.dev';

export function normalizeSiteBase(value) {
  if (!value || typeof value !== 'string') {
    throw new Error('SITE_BASE é obrigatório para gerar canonical, sitemap e dados estruturados absolutos.');
  }
  let url;
  try { url = new URL(value.trim()); }
  catch { throw new Error('SITE_BASE deve ser uma origem HTTPS válida (ex.: https://exemplo.com.br).'); }
  if (url.protocol !== 'https:' || !url.hostname || url.username || url.password ||
      url.pathname !== '/' || url.search || url.hash || url.port) {
    throw new Error('SITE_BASE deve ser apenas a origem HTTPS, sem porta, caminho, credenciais, query ou fragmento.');
  }
  return url.origin;
}

export function resolveSiteBase(env = process.env) {
  return normalizeSiteBase(env.SITE_BASE?.trim() || env.CF_PAGES_URL?.trim() || DEFAULT_SITE_BASE);
}
