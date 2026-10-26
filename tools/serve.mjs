/** Servidor local read-only para validar os assets estáticos como no deploy. */
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');
const port = Number(process.argv[2] || 8766);
const mime = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.woff2': 'font/woff2',
  '.ico': 'image/x-icon', '.pdf': 'application/pdf',
};

function headers() {
  return readFile(join(dist, '_headers'), 'utf8').then((text) => {
    const result = {};
    let active = false;
    for (const line of text.split(/\r?\n/)) {
      if (!line.trim() || line.trimStart().startsWith('#')) continue;
      if (!line.startsWith(' ')) { active = line.trim() === '/*'; continue; }
      if (active && line.includes(':')) {
        const [name, ...value] = line.trim().split(':');
        if (name !== 'Strict-Transport-Security') result[name] = value.join(':').trim();
      }
    }
    return result;
  });
}

function safePath(pathname) {
  const decoded = decodeURIComponent(pathname);
  const candidate = normalize(join(dist, decoded.replace(/^[/\\]+/, '')));
  return relative(dist, candidate).startsWith('..') ? null : candidate;
}

const commonHeaders = await headers();
createServer(async (req, res) => {
  try {
    const url = new URL(req.url || '/', 'http://127.0.0.1');
    let file = safePath(url.pathname);
    if (!file) { res.writeHead(400); res.end('Bad Request'); return; }
    let info;
    try { info = await stat(file); } catch { info = null; }
    if (info?.isDirectory()) file = join(file, 'index.html');
    try { await stat(file); } catch { if (url.pathname !== '/404.html') { file = join(dist, '404.html'); res.statusCode = 404; } }
    const body = await readFile(file);
    res.setHeader('Content-Type', mime[extname(file).toLowerCase()] || 'application/octet-stream');
    for (const [name, value] of Object.entries(commonHeaders)) res.setHeader(name, value);
    if (url.pathname === '/404.html') res.statusCode = 404;
    res.end(body);
  } catch {
    res.writeHead(500); res.end('Internal Server Error');
  }
}).listen(port, '127.0.0.1', () => console.log(`http://127.0.0.1:${port}/`));
