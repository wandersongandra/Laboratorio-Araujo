/** Cria a fonte HTML estática inicial a partir do dist validado. */
import { mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const dist = join(root, 'dist');
const pages = join(root, 'src', 'site', 'pages');
const files = join(root, 'src', 'site', 'files');
const layout = join(root, 'src', 'site', 'layout');
const data = JSON.parse(await readFile(join(root, 'src', 'site', 'data', 'site.json'), 'utf8'));
const publishedFiles = new Set([
  '_headers', '_redirects', 'llms-full.txt', 'llms.txt', 'robots.txt', 'sitemap.xml',
]);

const tokenPairs = [
  [data.phone1Tel, '{{PHONE_1_TEL}}'], [data.phone2Tel, '{{PHONE_2_TEL}}'],
  [data.financialPhoneTel, '{{FINANCIAL_PHONE_TEL}}'],
  [data.whatsappUrl, '{{WHATSAPP_URL}}'], [data.financialWhatsappUrl, '{{FINANCIAL_WHATSAPP_URL}}'],
  [data.phone1Display, '{{PHONE_1_DISPLAY}}'], [data.phone2Display, '{{PHONE_2_DISPLAY}}'],
  [data.whatsappDisplay, '{{WHATSAPP_DISPLAY}}'],
  [data.financialPhoneDisplay, '{{FINANCIAL_PHONE_DISPLAY}}'],
  [data.financialWhatsappDisplay, '{{FINANCIAL_WHATSAPP_DISPLAY}}'],
  [data.email, '{{EMAIL}}'], [data.cnpj, '{{CNPJ}}'], [data.legalName, '{{LEGAL_NAME}}'],
];

function tokenize(text) {
  return tokenPairs.reduce((value, [literal, token]) => value.split(literal).join(token), text);
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

await rm(pages, { recursive: true, force: true });
await rm(files, { recursive: true, force: true });
await rm(layout, { recursive: true, force: true });
await mkdir(pages, { recursive: true });
await mkdir(files, { recursive: true });
await mkdir(layout, { recursive: true });

let shellBefore;
let shellAfter;
for (const source of await walk(dist)) {
  const rel = relative(dist, source);
  if (rel.endsWith('.html')) {
    const html = tokenize(await readFile(source, 'utf8'));
    const body = html.indexOf('<body>');
    const main = html.indexOf('<main id="conteudo">');
    const mainEnd = html.indexOf('</main>', main);
    if (body < 0 || main < 0 || mainEnd < 0) throw new Error(`HTML sem shell esperado: ${rel}`);
    const before = html.slice(body + '<body>'.length, main);
    const after = html.slice(mainEnd + '</main>'.length);
    if (shellBefore === undefined) {
      shellBefore = before;
      shellAfter = after;
      await writeFile(join(layout, 'before-main.html'), before, 'utf8');
      await writeFile(join(layout, 'after-main.html'), after, 'utf8');
    } else if (before !== shellBefore || after !== shellAfter) {
      throw new Error(`Shell divergente: ${rel}`);
    }
    const pageDir = join(pages, rel.replace(/\.html$/, ''));
    await mkdir(pageDir, { recursive: true });
    await writeFile(join(pageDir, 'head.html'), html.slice(0, body + '<body>'.length), 'utf8');
    await writeFile(join(pageDir, 'main.html'), html.slice(main + '<main id="conteudo">'.length, mainEnd), 'utf8');
  } else if (publishedFiles.has(rel)) {
    await writeFile(join(files, rel), tokenize(await readFile(source, 'utf8')), 'utf8');
  }
}

console.log(`Fonte estática criada em ${pages}`);
