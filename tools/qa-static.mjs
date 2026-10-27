/** QA estrutural local do site estático, sem servidor de aplicação. */
import { createHash } from 'node:crypto';
import { readdir, readFile, stat } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');
const failures = [];

function fail(message) {
  failures.push(message);
  console.error(`  ✗ ${message}`);
}

async function walk(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) result.push(...await walk(path));
    else result.push(path);
  }
  return result;
}

function rel(path) {
  return relative(dist, path).replaceAll('\\', '/');
}

function targetFile(reference) {
  const url = new URL(reference, 'https://local.invalid');
  let pathname = decodeURIComponent(url.pathname);
  if (!pathname.startsWith('/')) return null;
  pathname = pathname.replace(/^\/+/, '');
  if (!pathname || pathname.endsWith('/')) pathname += 'index.html';
  return join(dist, pathname);
}

async function checkReferences(name, html) {
  const refs = [];
  for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) refs.push(match[1]);
  for (const match of html.matchAll(/(?:srcset|imagesrcset)="([^"]+)"/g)) {
    for (const item of match[1].split(',')) refs.push(item.trim().split(/\s+/)[0]);
  }
  for (const reference of refs) {
    if (!reference || ['#', 'data:', 'mailto:', 'tel:', 'javascript:'].some((prefix) => reference.startsWith(prefix))) continue;
    const parsed = new URL(reference, 'https://local.invalid');
    if (parsed.origin !== 'https://local.invalid') continue;
    const file = targetFile(reference);
    if (file && !(await exists(file))) fail(`${name}: referência interna ausente ${reference}`);
  }
}

function exists(path) {
  return stat(path).then(() => true).catch(() => false);
}

function allowedPriceText(name, line) {
  return name === '_redirects'
    || (name === 'termos-de-uso/index.html' && line.includes('O site não publica preços.'))
    || (name === 'blog/requisicao-para-laboratorio-de-protese/index.html'
      && line.includes('/assets/docs/requisicao-laboratorio-de-protese.pdf'));
}

const files = await walk(dist);
const htmlFiles = files.filter((path) => path.endsWith('.html')).sort();
const titles = new Map();
const descriptions = new Map();
const pricePatterns = [/R\$/i, /preço/i, /tabela-de-precos/i, /\.pdf\b/i, /tabela de preços/i];

for (const path of htmlFiles) {
  const name = rel(path);
  const html = await readFile(path, 'utf8');
  const title = html.match(/<title>(.*?)<\/title>/s)?.[1] || '';
  const description = html.match(/name="description" content="(.*?)"/s)?.[1] || '';
  const h1 = [...html.matchAll(/<h1[\s>]/g)].length;
  const headings = [...html.matchAll(/<h([1-6])[\s>]/g)].map((match) => Number(match[1]));
  const jumps = headings.filter((level, index) => index > 0 && level > headings[index - 1] + 1);
  const images = [...html.matchAll(/<img\b[^>]*>/g)].map((match) => match[0]);
  const missingAlt = images.filter((image) => !/\balt="/.test(image));
  const main = html.match(/<main id="conteudo">([\s\S]*?)<\/main>/)?.[1] || '';
  const words = main.replace(/<[^>]+>/g, ' ').trim().split(/\s+/).filter(Boolean).length;

  if (h1 !== 1) fail(`${name}: esperado 1 h1, encontrado ${h1}`);
  if (jumps.length) fail(`${name}: salto de hierarquia de headings`);
  if (missingAlt.length) fail(`${name}: ${missingAlt.length} imagem(ns) sem alt`);
  if (title.length < 20 || title.length > 60) fail(`${name}: title com ${title.length} caracteres`);
  if (name !== '404.html' && (description.length < 70 || description.length > 160)) {
    fail(`${name}: description com ${description.length} caracteres`);
  }
  for (const block of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(block[1]); } catch (error) { fail(`${name}: JSON-LD inválido (${error.message})`); }
  }
  for (const line of html.split(/\r?\n/)) {
    if (pricePatterns.some((pattern) => pattern.test(line)) && !allowedPriceText(name, line)) {
      fail(`${name}: conteúdo de preço/PDF não permitido`);
    }
  }
  await checkReferences(name, html);
  if (!titles.has(title)) titles.set(title, []);
  titles.get(title).push(name);
  if (!descriptions.has(description)) descriptions.set(description, []);
  descriptions.get(description).push(name);
  console.log(`${name.padEnd(64)} h1=${h1} words=${words}`);
}

const textFiles = files.filter((path) => /\.(html|txt|xml|json|webmanifest)$/.test(path) || !path.includes('.'));
for (const path of textFiles) {
  if (path.endsWith('.html')) continue;
  const name = rel(path);
  const text = await readFile(path, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    if (pricePatterns.some((pattern) => pattern.test(line)) && !allowedPriceText(name, line)) {
      fail(`${name}: conteúdo de preço/PDF não permitido`);
    }
  }
}

for (const pages of titles.values()) if (pages.length > 1) fail(`title duplicado: ${pages.join(', ')}`);
for (const pages of descriptions.values()) if (pages.length > 1) fail(`description duplicada: ${pages.join(', ')}`);

const sitemap = await readFile(join(dist, 'sitemap.xml'), 'utf8');
const locations = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1]);
if (locations.length !== htmlFiles.length - 1) fail(`sitemap com ${locations.length} URLs; esperado ${htmlFiles.length - 1}`);
const production = locations[0]?.match(/^(https?:\/\/[^/]+)/)?.[1];
const robots = await readFile(join(dist, 'robots.txt'), 'utf8');
if (production && !robots.includes(`Sitemap: ${production}/sitemap.xml`)) fail('robots.txt sem Sitemap correspondente');

const pdfs = files.filter((path) => path.endsWith('.pdf')).map(rel);
for (const pdf of pdfs) if (pdf !== 'assets/docs/requisicao-laboratorio-de-protese.pdf') fail(`PDF não permitido: ${pdf}`);

// ---------- segurança da saída publicada (ver docs/SEGURANCA.md) ----------
const forbiddenFiles = /(^|\/)(\.env(\..*)?|\.dev\.vars.*|\.git|\.DS_Store|Thumbs\.db)$|\.(map|md|log|pem|key)$/;
for (const path of files) if (forbiddenFiles.test(rel(path))) fail(`arquivo que não deve ser publicado: ${rel(path)}`);

const leakPatterns = [
  [/netlify/i, 'referência a Netlify'],
  [/sourceMappingURL/, 'source map referenciado'],
  [/\/workspace\/|\/opt\/buildhome|\/home\/[a-z]|\/Users\/[A-Za-z]|[A-Z]:\\Users\\/, 'caminho local de máquina'],
  [/\{\{[A-Z0-9_]+\}\}/, 'token de template não substituído'],
];
const xmlNamespaces = /http:\/\/www\.(sitemaps\.org|google\.com\/schemas|w3\.org)\//g;
for (const path of files.filter((file) => /\.(html|txt|xml|json|webmanifest|css|js)$/.test(file))) {
  const name = rel(path);
  const text = await readFile(path, 'utf8');
  for (const [pattern, label] of leakPatterns) if (pattern.test(text)) fail(`${name}: ${label}`);
  if (/http:\/\//.test(text.replace(xmlNamespaces, ''))) fail(`${name}: URL http:// (conteúdo misto)`);
}

const inlineHashes = new Set();
for (const path of htmlFiles) {
  const name = rel(path);
  const html = await readFile(path, 'utf8');
  for (const tag of html.matchAll(/<a\b[^>]*\btarget="_blank"[^>]*>/g)) {
    const relAttr = tag[0].match(/\brel="([^"]*)"/)?.[1].split(/\s+/) || [];
    if (!relAttr.includes('noopener') || !relAttr.includes('noreferrer')) fail(`${name}: target="_blank" sem rel="noopener noreferrer": ${tag[0]}`);
  }
  if (/<form\b/i.test(html)) fail(`${name}: formulário encontrado (a CSP usa form-action 'none')`);
  if (/\son[a-z]+="/i.test(html)) fail(`${name}: handler de evento inline`);
  for (const block of html.matchAll(/<script>([\s\S]*?)<\/script>/g)) {
    inlineHashes.add(`'sha256-${createHash('sha256').update(block[1]).digest('base64')}'`);
  }
  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
  if (production && !canonical?.startsWith(`${production}/`)) fail(`${name}: canonical não é absoluto em ${production}`);
}

const headersFile = await readFile(join(dist, '_headers'), 'utf8');
const globalRule = headersFile.split(/\r?\n(?=\S)/).find((block) => block.startsWith('/*\n') || block.startsWith('/*\r\n')) || '';
const globalHeaders = new Map();
for (const line of globalRule.split(/\r?\n/).slice(1)) {
  const match = line.match(/^\s+([A-Za-z-]+):\s*(.+)$/);
  if (!match) continue;
  const key = match[1].toLowerCase();
  if (globalHeaders.has(key)) fail(`_headers: ${match[1]} duplicado na regra /*`);
  globalHeaders.set(key, match[2]);
}
const requiredHeaders = {
  'content-security-policy': null,
  'strict-transport-security': /^max-age=\d{7,}$/,
  'x-content-type-options': /^nosniff$/,
  'x-frame-options': /^DENY$/,
  'referrer-policy': /^strict-origin-when-cross-origin$/,
  'permissions-policy': /camera=\(\).*geolocation=\(\).*microphone=\(\).*payment=\(\).*usb=\(\)/,
  'cross-origin-opener-policy': /^same-origin$/,
};
for (const [header, expected] of Object.entries(requiredHeaders)) {
  const value = globalHeaders.get(header);
  if (!value) fail(`_headers: ${header} ausente na regra /*`);
  else if (expected && !expected.test(value)) fail(`_headers: ${header} com valor inesperado: ${value}`);
}
const csp = globalHeaders.get('content-security-policy') || '';
for (const weak of ["'unsafe-eval'", "'unsafe-inline'", "'unsafe-hashes'", 'http:', ' * ', ' *;']) {
  if (` ${csp} `.includes(weak)) fail(`CSP contém ${weak.trim()}`);
}
for (const directive of ["object-src 'none'", "base-uri 'self'", "frame-ancestors 'none'", "form-action 'none'"]) {
  if (!csp.includes(directive)) fail(`CSP sem ${directive}`);
}
const scriptSrc = csp.match(/script-src ([^;]+)/)?.[1].split(/\s+/) || [];
for (const hashValue of inlineHashes) if (!scriptSrc.includes(hashValue)) fail(`CSP sem o hash do script inline ${hashValue}`);
for (const source of scriptSrc.filter((item) => item.startsWith("'sha256-"))) {
  if (!inlineHashes.has(source)) fail(`CSP com hash de script que não existe mais: ${source}`);
}
const otherRules = headersFile.split(/\r?\n(?=\S)/).filter((block) => !block.startsWith('#') && block !== globalRule);
for (const block of otherRules) {
  for (const line of block.split(/\r?\n/).slice(1)) {
    const key = line.match(/^\s+([A-Za-z-]+):/)?.[1].toLowerCase();
    if (key && globalHeaders.has(key)) fail(`_headers: ${key} repetido em ${block.split(/\r?\n/)[0]} (seria enviado duas vezes)`);
  }
}

console.log(`\n${failures.length} falha(s); ${htmlFiles.length - 1} páginas + 404 verificadas`);
process.exit(failures.length ? 1 : 0);
