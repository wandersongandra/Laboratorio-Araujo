/** Corrige mecanicamente descritores srcset a partir dos arquivos reais. Requer ImageMagick. */
import { execFileSync } from 'node:child_process';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const site = join(root, 'src', 'site');
const assets = join(root, 'src');
const srcsetAttribute = /\b(srcset|imagesrcset)="([^"]+)"/g;
const imageEntry = /^(\/[^\s?#]+)\s+(\d+)w$/;

async function htmlFiles(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) result.push(...await htmlFiles(path));
    else if (path.endsWith('.html')) result.push(path);
  }
  return result;
}

const files = await htmlFiles(site);
const sources = await Promise.all(files.map(async (path) => ({ path, html: await readFile(path, 'utf8') })));
const urls = new Set();
for (const { html } of sources) {
  for (const attr of html.matchAll(srcsetAttribute)) {
    for (const segment of attr[2].split(',')) {
      const matched = segment.trim().match(imageEntry);
      if (matched) urls.add(matched[1]);
    }
  }
}
const imageUrls = [...urls];
const widths = execFileSync('identify', [
  '-ping', '-format', '%w\n',
  ...imageUrls.map((url) => join(assets, url.slice(1))),
], { encoding: 'utf8', timeout: 90_000, maxBuffer: 5 * 1024 * 1024 }).trimEnd().split('\n').map(Number);
if (widths.length !== imageUrls.length || widths.some((width) => !Number.isInteger(width) || width < 1)) {
  throw Error(`Não foi possível ler todas as dimensões (${widths.length}/${imageUrls.length})`);
}
const imageWidths = new Map(imageUrls.map((url, index) => [url, widths[index]]));

let changedFiles = 0;
let correctedEntries = 0;
let duplicatesRemoved = 0;
for (const { path, html } of sources) {
  const updated = html.replace(srcsetAttribute, (attribute, name, value) => {
    const seen = new Set();
    const entries = [];
    for (const original of value.split(',')) {
      const entry = original.trim();
      const match = entry.match(imageEntry);
      if (!match || !imageWidths.has(match[1])) { entries.push(entry); continue; }
      const [, url, declared] = match;
      if (seen.has(url)) { duplicatesRemoved++; continue; }
      seen.add(url);
      const actual = imageWidths.get(url);
      if (Number(declared) !== actual) correctedEntries++;
      entries.push(`${url} ${actual}w`);
    }
    return `${name}="${entries.join(', ')}"`;
  });
  if (updated !== html) {
    await writeFile(path, updated, 'utf8');
    changedFiles++;
  }
}
console.log(`${changedFiles} arquivos alterados; ${correctedEntries} descritores corrigidos; ${duplicatesRemoved} referências duplicadas removidas.`);
