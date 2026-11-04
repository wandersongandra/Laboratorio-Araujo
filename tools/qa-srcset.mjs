/** Auditoria opcional de srcset; requer `identify` (ImageMagick). */
import { execFileSync } from 'node:child_process';
import { readFile, readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');
const declared = new Map();
let failures = 0;

async function walk(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) result.push(...await walk(path));
    else if (path.endsWith('.html')) result.push(path);
  }
  return result;
}

for (const path of await walk(dist)) {
  const html = await readFile(path, 'utf8');
  for (const srcset of html.matchAll(/(?:srcset|imagesrcset)="([^"]+)"/g)) {
    const imageUrls = new Set();
    const widths = new Set();
    for (const entry of srcset[1].split(',')) {
      const match = entry.trim().match(/^(\/[^\s?#]+)\s+(\d+)w$/);
      if (!match) continue;
      const [, url, width] = match;
      if (imageUrls.has(url) || widths.has(Number(width))) {
        failures++;
        console.error(`  ✗ srcset duplicado (${url}, ${width}w) em ${relative(dist, path)}`);
      }
      imageUrls.add(url);
      widths.add(Number(width));
      if (!declared.has(url)) declared.set(url, new Map());
      const uses = declared.get(url);
      if (!uses.has(Number(width))) uses.set(Number(width), relative(dist, path));
    }
  }
}

// One invocation instead of hundreds: faster and less expensive on CI hosts.
const urls = [...declared.keys()];
const images = urls.map((url) => join(dist, url.slice(1)));
let metadata;
try {
  metadata = execFileSync('identify', ['-ping', '-format', '%w\n', ...images], {
    encoding: 'utf8', timeout: 90_000, maxBuffer: 5 * 1024 * 1024,
  }).trimEnd().split('\n').map(Number);
} catch (error) {
  console.error('Não foi possível conferir as dimensões com ImageMagick:', error.message);
  process.exit(2);
}
if (metadata.length !== urls.length) {
  console.error(`Metadados incompletos: ${metadata.length}/${urls.length} imagens`);
  process.exit(2);
}

for (const [i, url] of urls.entries()) {
  const uses = declared.get(url);
  const actual = metadata[i];
  for (const [width, page] of uses) {
    if (width !== actual) {
      failures++;
      console.error(`  ✗ ${url}: declarado ${width}w, real ${actual}w (ex.: ${page})`);
    }
  }
}

console.log(`\n${declared.size} imagens srcset distintas; ${failures} divergência(s)`);
process.exit(failures ? 1 : 0);
