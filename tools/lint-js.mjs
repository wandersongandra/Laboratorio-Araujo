/** Executa ESLint no bundle-fonte sem criar src/assets/js/main.js. */
import { spawnSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const eslint = join(root, 'node_modules', 'eslint', 'bin', 'eslint.js');
const bundle = [
  '00-helpers.js', '01-rastreamento.js', '02-ancoras.js', '03-cabecalho.js', '04-revelacoes.js',
  '05-indice.js', '06-mapa.js', '07-contadores.js', '08-faixa.js', '09-timeline.js',
  '10-acordeao.js', '11-antes-depois.js', '12-galeria.js', '13-atmosfera.js', '14-leitura.js',
];
const header = '/**\n * Laboratório Dental Araújo — interações (JS gerado a partir de src/assets/js/modules).\n */\n';
const modules = await Promise.all(bundle.map((name) => readFile(join(root, 'src', 'assets', 'js', 'modules', name), 'utf8')));
const source = `${header}(() => {\n  'use strict';\n${modules.join('')}})();\n`;
const result = spawnSync(process.execPath, [eslint, '--stdin', '--stdin-filename', 'src/assets/js/main.js'], {
  cwd: root,
  input: source,
  encoding: 'utf8',
  stdio: ['pipe', 'inherit', 'inherit'],
});
process.exit(result.status ?? 2);
