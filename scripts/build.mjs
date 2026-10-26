/**
 * Build estático do Laboratório Dental Araújo.
 *
 * O site não tem backend: este processo monta assets e publica páginas HTML
 * estáticas na estrutura esperada pelo Cloudflare Workers Assets.
 */
import { createHash } from 'node:crypto';
import { cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const assets = join(root, 'src', 'assets');
const sourcePages = join(root, 'src', 'site', 'pages');
const sourceFiles = join(root, 'src', 'site', 'files');
const sourceLayout = join(root, 'src', 'site', 'layout');
const siteData = JSON.parse(await readFile(join(root, 'src', 'site', 'data', 'site.json'), 'utf8'));
const dist = join(root, 'dist');
const configuredBase = process.env.SITE_BASE?.trim();
if (!configuredBase) {
  throw new Error('SITE_BASE é obrigatório. Informe o domínio oficial da Cloudflare antes do build.');
}

const parsedBase = new URL(configuredBase);
if (parsedBase.protocol !== 'https:' || parsedBase.username || parsedBase.password || parsedBase.search || parsedBase.hash) {
  throw new Error('SITE_BASE deve ser uma URL HTTPS sem credenciais, query string ou fragmento.');
}

const base = configuredBase.replace(/\/$/, '');
const tokens = {
  '{{SITE_BASE}}': base,
  '{{PHONE_1_TEL}}': siteData.phone1Tel, '{{PHONE_2_TEL}}': siteData.phone2Tel,
  '{{FINANCIAL_PHONE_TEL}}': siteData.financialPhoneTel, '{{WHATSAPP_URL}}': siteData.whatsappUrl,
  '{{FINANCIAL_WHATSAPP_URL}}': siteData.financialWhatsappUrl,
  '{{PHONE_1_DISPLAY}}': siteData.phone1Display, '{{PHONE_2_DISPLAY}}': siteData.phone2Display,
  '{{WHATSAPP_DISPLAY}}': siteData.whatsappDisplay, '{{FINANCIAL_PHONE_DISPLAY}}': siteData.financialPhoneDisplay,
  '{{FINANCIAL_WHATSAPP_DISPLAY}}': siteData.financialWhatsappDisplay,
  '{{EMAIL}}': siteData.email, '{{CNPJ}}': siteData.cnpj, '{{LEGAL_NAME}}': siteData.legalName,
};

const cssBundle = [
  'tokens.css', 'base.css', 'buttons.css', 'layout-chrome.css', 'layout-sections.css',
  'pages-home.css', 'components.css', 'pages-internal.css', 'motion.css', 'layout-responsive.css',
];
const jsBundle = [
  '00-helpers.js', '01-rastreamento.js', '02-ancoras.js', '03-cabecalho.js', '04-revelacoes.js',
  '05-indice.js', '06-mapa.js', '07-contadores.js', '08-faixa.js', '09-timeline.js',
  '10-acordeao.js', '11-antes-depois.js', '12-galeria.js', '13-atmosfera.js', '14-leitura.js',
];

const cssHeader = '/* Laboratório Dental Araújo — CSS gerado (bundle). Fontes em src/assets/css/; ver docs/ARQUITETURA.md. */\n';
const jsHeader = '/**\n * Laboratório Dental Araújo — interações (JS gerado a partir de src/assets/js/modules).\n */\n';

function minifyCss(source) {
  let css = '';
  for (let i = 0; i < source.length;) {
    const quote = source[i];
    if (quote === '"' || quote === "'") {
      let end = i + 1;
      while (end < source.length && source[end] !== quote) end += source[end] === '\\' ? 2 : 1;
      css += source.slice(i, end + 1);
      i = end + 1;
    } else if (source.startsWith('/*', i)) {
      const end = source.indexOf('*/', i + 2);
      i = end < 0 ? source.length : end + 2;
    } else {
      css += source[i++];
    }
  }
  const parts = css.split(/("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/);
  for (let i = 0; i < parts.length; i += 2) {
    parts[i] = parts[i]
      .replace(/\s+/g, ' ')
      .replace(/\s*([{};,>])\s*/g, '$1')
      .replace(/;}\s*/g, '}');
  }
  return parts.join('').trim() + '\n';
}

function minifyJs(source) {
  const withoutBlocks = source.replace(/^\s*\/\*.*?\*\/\s*$/gms, '');
  const lines = withoutBlocks.split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('//'));
  return `${lines.join('\n')}\n`;
}

async function assembleCss() {
  const parts = await Promise.all(cssBundle.map((name) => readFile(join(assets, 'css', name), 'utf8')));
  return cssHeader + parts.join('');
}

async function assembleJs() {
  const parts = await Promise.all(jsBundle.map((name) => readFile(join(assets, 'js', 'modules', name), 'utf8')));
  return `${jsHeader}(() => {\n  'use strict';\n${parts.join('')}})();\n`;
}

async function copyAssetTree(source, target, ignored = new Set()) {
  await mkdir(target, { recursive: true });
  for (const entry of await readdir(source, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    const from = join(source, entry.name);
    const to = join(target, entry.name);
    if (entry.isDirectory()) await copyAssetTree(from, to);
    else await cp(from, to);
  }
}

async function copyTree(source, target) {
  await mkdir(target, { recursive: true });
  for (const entry of await readdir(source, { withFileTypes: true })) {
    const from = join(source, entry.name);
    const to = join(target, entry.name);
    if (entry.isDirectory()) await copyTree(from, to);
    else await cp(from, to);
  }
}

async function renderPages() {
  const before = await readFile(join(sourceLayout, 'before-main.html'), 'utf8');
  const after = await readFile(join(sourceLayout, 'after-main.html'), 'utf8');
  for (const pageDir of await walkDirectories(sourcePages)) {
    const rel = relative(sourcePages, pageDir);
    const head = await readFile(join(pageDir, 'head.html'), 'utf8');
    const main = await readFile(join(pageDir, 'main.html'), 'utf8');
    const output = join(dist, `${rel}.html`);
    await mkdir(join(output, '..'), { recursive: true });
    await writeFile(output, `${head}${before}<main id="conteudo">${main}</main>${after}`, 'utf8');
  }
}

async function walkDirectories(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (await hasPageParts(path)) result.push(path);
      else result.push(...await walkDirectories(path));
    }
  }
  return result;
}

async function hasPageParts(dir) {
  const names = new Set((await readdir(dir)).map((name) => name.toLowerCase()));
  return names.has('head.html') && names.has('main.html');
}

function hash(buffer) {
  return createHash('md5').update(buffer).digest('hex').slice(0, 8);
}

function toCrlf(text) {
  return text.replace(/\r?\n/g, '\r\n');
}

async function replaceTextFiles(dir, cssVersion, jsVersion) {
  const textExtensions = new Set(['.html', '.txt', '.xml', '.json', '.webmanifest', '']);
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      await replaceTextFiles(path, cssVersion, jsVersion);
      continue;
    }
    const ext = entry.name.includes('.') ? entry.name.slice(entry.name.lastIndexOf('.')) : '';
    if (!textExtensions.has(ext)) continue;
    let text = await readFile(path, 'utf8');
    for (const [token, value] of Object.entries(tokens)) text = text.replaceAll(token, value);
    text = text
      .replace(/assets\/css\/style\.css\?v=[a-f0-9]+/g, `assets/css/style.css?v=${cssVersion}`)
      .replace(/assets\/js\/main\.js\?v=[a-f0-9]+/g, `assets/js/main.js?v=${jsVersion}`);
    await writeFile(path, text, 'utf8');
  }
}

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
await cp(join(assets, 'favicon.ico'), join(dist, 'favicon.ico'));
await cp(join(assets, 'site.webmanifest'), join(dist, 'site.webmanifest'));
await copyAssetTree(assets, join(dist, 'assets'), new Set(['css', 'js', 'favicon.ico', 'site.webmanifest']));
await mkdir(join(dist, 'assets', 'css'), { recursive: true });
await mkdir(join(dist, 'assets', 'js'), { recursive: true });

const css = minifyCss(await assembleCss());
const js = minifyJs(await assembleJs());
const cssFile = toCrlf(css);
const jsFile = toCrlf(js);
await writeFile(join(dist, 'assets', 'css', 'style.css'), cssFile, 'utf8');
await writeFile(join(dist, 'assets', 'js', 'main.js'), jsFile, 'utf8');
await renderPages();
await copyTree(sourceFiles, dist);

const cssVersion = hash(Buffer.from(cssFile));
const jsVersion = hash(Buffer.from(jsFile));
await replaceTextFiles(dist, cssVersion, jsVersion);

const pages = (await walkHtml(dist)).length;
console.log(`ok: ${pages - 1} paginas + 404 -> ${dist}`);

async function walkHtml(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) result.push(...await walkHtml(path));
    else if (entry.name.endsWith('.html')) result.push(path);
  }
  return result;
}
