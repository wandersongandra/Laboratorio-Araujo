/** Smoke real do site gerado em seis larguras; executar com tools/serve.mjs ativo. */
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';

const base = (process.argv[2] || 'http://127.0.0.1:8766').replace(/\/$/, '');
const sitemap = readFileSync(new URL('../dist/sitemap.xml', import.meta.url), 'utf8');
const routes = [...sitemap.matchAll(/<loc>https?:\/\/[^/]+(\/[^<]*)<\/loc>/g)].map((match) => match[1]);
routes.push('/404.html');
const sizes = [320, 390, 768, 1024, 1366, 1920];
const issues = [];
let inspected = 0;

function fail(route, width, message) {
  issues.push(`${width}px ${route}: ${message}`);
  console.error(`  ✗ ${issues.at(-1)}`);
}

const browser = await chromium.launch();
try {
  for (const width of sizes) {
    const context = await browser.newContext({
      viewport: { width, height: width < 600 ? 844 : 900 },
      reducedMotion: 'reduce',
      deviceScaleFactor: 1,
    });
    try {
      for (const route of routes) {
        const page = await context.newPage();
        page.on('pageerror', (error) => fail(route, width, `JavaScript: ${error.message}`));
        try {
          const response = await page.goto(`${base}${route}`, { waitUntil: 'load', timeout: 15_000 });
          const expected = route === '/404.html' ? 404 : 200;
          if (response?.status() !== expected) fail(route, width, `HTTP ${response?.status()} (esperado ${expected})`);
          const state = await page.evaluate(() => ({
            pageWidth: document.documentElement.scrollWidth,
            viewportWidth: innerWidth,
            main: Boolean(document.querySelector('main')),
            h1: document.querySelectorAll('h1').length,
            brokenEagerImages: [...document.images].filter((image) =>
              image.loading !== 'lazy' && image.complete && image.naturalWidth === 0,
            ).map((image) => image.currentSrc || image.src),
          }));
          if (state.pageWidth > state.viewportWidth + 1) {
            fail(route, width, `rolagem horizontal ${state.pageWidth}px > ${state.viewportWidth}px`);
          }
          if (!state.main || state.h1 !== 1) fail(route, width, `main/h1 ausente ou duplicado (${state.h1})`);
          for (const url of state.brokenEagerImages) fail(route, width, `imagem não carregada: ${url}`);

          if (route === '/' && width < 600) {
            const burger = page.locator('#burger');
            await burger.click();
            if (await burger.getAttribute('aria-expanded') !== 'true') fail(route, width, 'menu mobile não abriu');
            const submenu = page.locator('.nav__more').first();
            await submenu.click();
            if (await submenu.getAttribute('aria-expanded') !== 'true') fail(route, width, 'submenu não abriu');
            await page.keyboard.press('Escape');
            if (await burger.getAttribute('aria-expanded') !== 'false' ||
                await submenu.getAttribute('aria-expanded') !== 'false') {
              fail(route, width, 'Escape não fechou menu e submenu corretamente');
            }
          }
          inspected++;
        } catch (error) {
          fail(route, width, `não foi possível concluir o teste: ${error.message}`);
        } finally {
          await page.close();
        }
      }
    } finally {
      await context.close();
    }
  }
} finally {
  await browser.close();
}

console.log(`\n${inspected}/${routes.length * sizes.length} combinações rota × viewport; ${issues.length} falha(s)`);
process.exit(issues.length ? 1 : 0);
