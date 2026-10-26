/** QA estrutural local do site estático, sem servidor de aplicação. */
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
    if (!reference || reference.startsWith(('#', 'data:', 'mailto:', 'tel:', 'javascript:'))) continue;
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

console.log(`\n${failures.length} falha(s); ${htmlFiles.length - 1} páginas + 404 verificadas`);
process.exit(failures.length ? 1 : 0);
