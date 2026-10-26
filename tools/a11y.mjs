// Acessibilidade: roda o axe-core (regras WCAG 2.0/2.1/2.2 A e AA + boas práticas) em todas as
// URLs do sitemap, em 1366 px e 390 px, com o menu mobile aberto numa passada extra.
// Uso: npm run a11y [-- URL_BASE]      (padrão http://localhost:8766; suba antes: npm run serve)
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const BASE = (process.argv[2] || 'http://localhost:8766').replace(/\/$/, '');
const paths = [...readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8')
  .matchAll(/<loc>https?:\/\/[^/]+(\/[^<]*)<\/loc>/g)].map(m => m[1]).concat('/404.html');

// Usa o Chromium já instalado pelo Playwright, se houver.
function chromePath() {
  const dir = join(homedir(), '.cache', 'ms-playwright');
  if (!existsSync(dir)) return undefined;
  const c = readdirSync(dir).filter(d => /^chromium-\d+$/.test(d)).sort().pop();
  const p = c && join(dir, c, 'chrome-linux64', 'chrome');
  return p && existsSync(p) ? p : undefined;
}

const browser = await chromium.launch({ executablePath: chromePath() });
let total = 0;
for (const [w, h] of [[1366, 850], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  for (const p of paths) {
    const page = await ctx.newPage();
    await page.goto(BASE + p, { waitUntil: 'networkidle' });
    if (w === 390 && p === '/') await page.click('#burger');
    const r = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
    total += r.violations.length;
    const v = r.violations.map(x => `${x.id}(${x.impact}) ×${x.nodes.length}: ${x.nodes[0].target.join(' ')}`);
    console.log(`${w} ${p} ${v.length ? 'VIOLAÇÕES ' + v.join(' | ') : 'ok'} (${r.passes.length} regras aprovadas)`);
    await page.close();
  }
  await ctx.close();
}
await browser.close();
console.log('violações:', total);
process.exit(total ? 1 : 0);
