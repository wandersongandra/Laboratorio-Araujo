/** Prepara variantes de imagem sem Python; depende apenas do ImageMagick local. */
import { access, mkdir } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const args = process.argv.slice(2);

function option(name, fallback) {
  const prefix = `--${name}=`;
  const value = args.find((arg) => arg.startsWith(prefix));
  return value ? value.slice(prefix.length) : fallback;
}

function usage(message) {
  if (message) console.error(`Erro: ${message}\n`);
  console.error('Uso: node tools/prepare-images.mjs FOTO SLUG [--kind=real|foto] [--ratio=3/2] [--focus=0.5,0.5] [--output-dir=PASTA]');
  process.exit(1);
}

const source = args.find((arg) => !arg.startsWith('--'));
const slug = args.filter((arg) => !arg.startsWith('--'))[1];
const kind = option('kind', 'real');
const ratioText = option('ratio', '');
const focusText = option('focus', '0.5,0.5');
const outputDir = resolve(root, option('output-dir', kind === 'real' ? 'src/assets/img/real' : 'src/assets/img/foto'));

if (!source || !slug) usage('informe o arquivo de origem e o slug.');
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) usage('o slug deve usar kebab-case.');
if (!['real', 'foto'].includes(kind)) usage('--kind deve ser real ou foto.');
if (ratioText && !/^\d+(?:\.\d+)?\/\d+(?:\.\d+)?$/.test(ratioText)) usage('--ratio deve ser, por exemplo, 3/2 ou 4/5.');
const [focusX, focusY] = focusText.split(',').map(Number);
if (![focusX, focusY].every((value) => Number.isFinite(value) && value >= 0 && value <= 1)) usage('--focus deve conter dois valores entre 0 e 1.');

const input = resolve(source);
try { await access(input); } catch { usage(`arquivo não encontrado: ${input}`); }
await mkdir(outputDir, { recursive: true });

function runMagick(argumentsList) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn('magick', argumentsList, { stdio: ['ignore', 'pipe', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('error', (error) => reject(new Error(`ImageMagick não encontrado: ${error.message}`)));
    child.on('close', (code) => code === 0
      ? resolvePromise()
      : reject(new Error(`ImageMagick falhou (${code}): ${stderr.trim()}`)));
  });
}

const ratio = ratioText ? (() => {
  const [width, height] = ratioText.split('/').map(Number);
  return width / height;
})() : null;
const widths = kind === 'real' ? [480, 800, 1200] : [640, 1200];
const formats = kind === 'real'
  ? [{ extension: 'avif', quality: 62 }, { extension: 'webp', quality: 82 }]
  : [{ extension: 'webp', quality: 78 }];
const gravity = `${focusY < 0.33 ? 'north' : focusY > 0.67 ? 'south' : ''}${focusX < 0.33 ? 'west' : focusX > 0.67 ? 'east' : ''}` || 'center';

for (const width of widths) {
  const height = ratio ? Math.round(width / ratio) : null;
  const geometry = height ? `${width}x${height}` : `${width}x`;
  for (const format of formats) {
    const destination = resolve(outputDir, `${slug}-${width}.${format.extension}`);
    const imageArgs = [input, '-auto-orient', '-strip', '-resize', height ? `${geometry}^` : `${geometry}>`];
    if (height) imageArgs.push('-gravity', gravity, '-extent', geometry);
    imageArgs.push('-quality', String(format.quality), destination);
    await runMagick(imageArgs);
    console.log(`ok ${destination}`);
  }
  if (kind === 'real') {
    const destination = resolve(outputDir, `${slug}-${width}.jpg`);
    const imageArgs = [input, '-auto-orient', '-strip', '-resize', height ? `${geometry}^` : `${geometry}>`];
    if (height) imageArgs.push('-gravity', 'center', '-extent', geometry);
    imageArgs.push('-quality', '84', destination);
    await runMagick(imageArgs);
    console.log(`ok ${destination}`);
  }
}

console.log(`Variantes criadas em ${outputDir}. Atualize os metadados da rota e rode npm run qa.`);
