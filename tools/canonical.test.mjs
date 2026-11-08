import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import {
  CANONICAL_HOST,
  CANONICAL_ORIGIN,
  LEGACY_HOST,
  classifyRequest,
  handleRequest,
  isPreviewBuild,
  redirectHeaders,
  resolveBuildPolicy,
  toCanonicalUrl,
} from '../src/worker/canonical.mjs';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');

function request(url, method = 'GET') {
  return new Request(url, { method });
}

function assetEnv(body = 'ok', status = 200, headers = { 'Content-Security-Policy': "default-src 'self'", 'X-Content-Type-Options': 'nosniff' }) {
  const calls = [];
  return {
    calls,
    env: {
      ASSETS: {
        async fetch(input) {
          calls.push(input.url);
          return new Response(body, { status, headers });
        },
      },
    },
  };
}

test('o apex passa intacto e não redireciona HTTP nem www no código', async () => {
  const { env, calls } = assetEnv();
  const asset = await env.ASSETS.fetch(request(`${CANONICAL_ORIGIN}/contato/`));
  const same = await handleRequest(request(`${CANONICAL_ORIGIN}/contato/?a=1`), env);
  assert.equal(same.status, 200);
  assert.equal(same.headers.get('X-Robots-Tag'), null);
  assert.equal(same.headers.get('Content-Security-Policy'), "default-src 'self'");
  assert.equal(calls.at(-1), `${CANONICAL_ORIGIN}/contato/?a=1`);
  const httpApex = await handleRequest(request(`http://${CANONICAL_HOST}/contato/?a=1`), env);
  assert.equal(httpApex.status, 200);
  assert.equal(httpApex.headers.get('Location'), null);
  const www = await handleRequest(request(`https://www.${CANONICAL_HOST}/contato/?a=1`), env);
  assert.equal(www.status, 200);
  assert.equal(www.headers.get('Location'), null);
  assert.equal(www.headers.get('X-Robots-Tag'), 'noindex, nofollow');
  assert.equal(www.headers.get('Content-Security-Policy'), "default-src 'self'");
  assert.notEqual(asset.status, 301);
});

test('workers.dev estável redireciona com path e query, sem loop e sem open redirect', async () => {
  const { env, calls } = assetEnv();
  const source = `https://${LEGACY_HOST}/trabalhos/?tag=zirc%C3%B4nia&x=1`;
  const response = await handleRequest(request(source), env);
  assert.equal(calls.length, 0);
  assert.equal(response.status, 301);
  assert.equal(response.headers.get('Location'), `${CANONICAL_ORIGIN}/trabalhos/?tag=zirc%C3%B4nia&x=1`);
  assert.equal(response.headers.get('Strict-Transport-Security'), 'max-age=31536000');
  assert.equal(/includeSubDomains|preload/i.test(response.headers.get('Strict-Transport-Security')), false);
  assert.equal(response.headers.get('X-Content-Type-Options'), 'nosniff');
  assert.equal(response.headers.get('X-Frame-Options'), 'DENY');
  const again = classifyRequest(new URL(response.headers.get('Location')), 'GET');
  assert.equal(again.action, 'pass');
  const head = await handleRequest(request(`https://${LEGACY_HOST}/contato/?a=1&b=dois`, 'HEAD'), env);
  assert.equal(head.status, 301);
  assert.equal(head.headers.get('Location'), `${CANONICAL_ORIGIN}/contato/?a=1&b=dois`);
  const post = await handleRequest(request(`https://${LEGACY_HOST}/contato/?a=1`, 'POST'), env);
  assert.notEqual(post.status, 301);
  assert.equal(post.headers.get('X-Robots-Tag'), 'noindex, nofollow');
  assert.equal(toCanonicalUrl({ pathname: '/contato/../admin', search: '' }), null);
  assert.equal(toCanonicalUrl({ pathname: '//evil.com', search: '' }), null);
  const slashed = await handleRequest(request(`https://${LEGACY_HOST}//evil.com`), env);
  assert.notEqual(slashed.status, 301);
  assert.equal((slashed.headers.get('Location') || '').includes('evil.com'), false);
  const normalized = await handleRequest(request(`https://${LEGACY_HOST}/contato/../admin?x=1`), env);
  assert.equal(normalized.headers.get('Location'), `${CANONICAL_ORIGIN}/admin?x=1`);
  const cased = await handleRequest(request(`https://${LEGACY_HOST.toUpperCase()}/mapa-do-site/?x=1`), env);
  assert.equal(cased.headers.get('Location'), `${CANONICAL_ORIGIN}/mapa-do-site/?x=1`);
});

test('preview e deployment não vão para o apex e recebem noindex', async () => {
  const hosts = [
    `f38ce885-${LEGACY_HOST}`,
    `preview-${LEGACY_HOST}`,
    `version-123-${LEGACY_HOST}`,
    'laboratorio-araujo.example.workers.dev',
    'deploy.laboratoriodentalaraujo.workers.dev',
  ];
  for (const host of hosts) {
    const { env, calls } = assetEnv('<html></html>', 200);
    const response = await handleRequest(request(`https://${host}/contato/?a=1`), env);
    assert.equal(response.status, 200, host);
    assert.equal(response.headers.get('Location'), null, host);
    assert.equal(response.headers.get('X-Robots-Tag'), 'noindex, nofollow', host);
    assert.equal(calls[0], `https://${host}/contato/?a=1`);
    assert.equal(classifyRequest(new URL(`https://${host}/`), 'GET').action, 'noindex');
  }
});

test('cabeçalhos do 301 não enfraquecem o _headers e não incluem HSTS amplo', async () => {
  const file = await readFile(join(root, 'src/site/files/_headers'), 'utf8');
  const headers = redirectHeaders(`${CANONICAL_ORIGIN}/`);
  for (const name of [
    'Strict-Transport-Security',
    'X-Content-Type-Options',
    'X-Frame-Options',
    'Referrer-Policy',
    'Permissions-Policy',
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Resource-Policy',
    'X-Permitted-Cross-Domain-Policies',
  ]) {
    const value = file.match(new RegExp(`${name}:\\s*(.+)`))[1].trim();
    assert.equal(headers[name], value);
  }
  assert.equal(/includeSubDomains|preload/i.test(headers['Strict-Transport-Security']), false);
  assert.equal(headers['Content-Security-Policy'].includes("frame-ancestors 'none'"), true);
  assert.equal(toCanonicalUrl(new URL(`${CANONICAL_ORIGIN}/contato/?a=1`)), `${CANONICAL_ORIGIN}/contato/?a=1`);
});

test('política de build aceita só o apex e distingue preview', () => {
  assert.equal(resolveBuildPolicy({}).origin, CANONICAL_ORIGIN);
  assert.equal(resolveBuildPolicy({}).indexable, true);
  assert.equal(resolveBuildPolicy({ SITE_BASE: CANONICAL_ORIGIN, WORKERS_CI_BRANCH: 'main' }).indexable, true);
  assert.equal(resolveBuildPolicy({ SITE_BASE: `${CANONICAL_ORIGIN}/`, WORKERS_CI_BRANCH: 'main' }).preview, false);
  assert.equal(isPreviewBuild({ WORKERS_CI_BRANCH: 'fix/auditoria-lda-nov-2026' }), true);
  assert.equal(resolveBuildPolicy({ SITE_BASE: CANONICAL_ORIGIN, WORKERS_CI_BRANCH: 'cursor/canonical-apex-workers-dev-55d8' }).indexable, false);
  assert.equal(resolveBuildPolicy({ SITE_PREVIEW: '1', WORKERS_CI_BRANCH: 'main' }).preview, true);
  for (const value of [
    `https://${LEGACY_HOST}`,
    `https://www.${CANONICAL_HOST}`,
    'http://laboratoriodentalaraujo.com.br',
    `${CANONICAL_ORIGIN}/contato`,
    'https://outro.example',
  ]) {
    assert.throws(() => resolveBuildPolicy({ SITE_BASE: value }), /SITE_BASE deve ser/);
  }
});

function runBuild(extra = {}) {
  const env = { ...process.env };
  for (const key of ['SITE_BASE', 'CF_PAGES_URL', 'SITE_PREVIEW', 'WORKERS_CI_BRANCH', 'CF_PAGES_BRANCH', 'CF_PAGES', 'WORKERS_CI']) {
    delete env[key];
  }
  Object.assign(env, extra);
  return spawnSync(process.execPath, ['scripts/build.mjs'], { cwd: root, env, encoding: 'utf8' });
}

async function htmlFiles(dir) {
  const found = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) found.push(...await htmlFiles(path));
    else if (entry.name.endsWith('.html')) found.push(path);
  }
  return found;
}

test('build de produção e de preview', async () => {
  const legacy = runBuild({ SITE_BASE: `https://${LEGACY_HOST}` });
  assert.notEqual(legacy.status, 0);
  assert.match(`${legacy.stderr}`, /SITE_BASE deve ser/);

  const preview = runBuild({ SITE_BASE: CANONICAL_ORIGIN, WORKERS_CI_BRANCH: 'preview-seo' });
  assert.equal(preview.status, 0, preview.stderr);
  const previewRobots = await readFile(join(dist, 'robots.txt'), 'utf8');
  const previewSitemap = await readFile(join(dist, 'sitemap.xml'), 'utf8');
  assert.equal(/Sitemap:/i.test(previewRobots), false);
  assert.equal(previewSitemap.includes('<loc>'), false);
  assert.match(previewRobots, /User-agent: Googlebot/);
  assert.equal(/Disallow\s*:/i.test(previewRobots), false);
  for (const file of await htmlFiles(dist)) {
    const html = await readFile(file, 'utf8');
    assert.match(html, /content="noindex, nofollow"/);
    assert.equal(html.includes('workers.dev'), false);
    assert.match(html, new RegExp(CANONICAL_ORIGIN.replaceAll('.', '\\.')));
  }

  const production = runBuild({ SITE_BASE: CANONICAL_ORIGIN, WORKERS_CI_BRANCH: 'main' });
  assert.equal(production.status, 0, production.stderr);
  const home = await readFile(join(dist, 'index.html'), 'utf8');
  const robots = await readFile(join(dist, 'robots.txt'), 'utf8');
  const sitemap = await readFile(join(dist, 'sitemap.xml'), 'utf8');
  const llms = await readFile(join(dist, 'llms.txt'), 'utf8');
  assert.match(home, /content="index, follow, max-image-preview:large, max-snippet:-1"/);
  assert.match(home, new RegExp(`<link rel="canonical" href="${CANONICAL_ORIGIN}/">`));
  assert.match(home, new RegExp(`"@id":"${CANONICAL_ORIGIN}/#laboratorio"`));
  assert.match(robots, new RegExp(`Sitemap: ${CANONICAL_ORIGIN}/sitemap.xml`));
  assert.match(sitemap, new RegExp(`<loc>${CANONICAL_ORIGIN}/</loc>`));
  assert.equal(sitemap.includes('/404'), false);
  assert.match(llms, new RegExp(`${CANONICAL_ORIGIN}/contato/`));
  assert.equal(home.includes('workers.dev'), false);
  const notFound = await readFile(join(dist, '404.html'), 'utf8');
  assert.match(notFound, /content="noindex, follow"/);
});
