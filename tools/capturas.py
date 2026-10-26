#!/usr/bin/env python3
"""Capturas de tela de página inteira (1440 px "-d" e 390 px "-m") para revisão visual.
Rola a página antes para disparar as revelações (.rv) e o carregamento preguiçoso.

Uso:  python3 tools/capturas.py URL_BASE PASTA_SAIDA caminho:nome [caminho:nome ...]
Ex.:  python3 tools/capturas.py http://localhost:8766 /tmp/shots /:home /servicos/zirconia-e-max/:zirconia
"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

async def main(base, out, items):
    Path(out).mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for it in items:
            path, name = it.rsplit(':', 1)
            for w, h, s in [(1440, 900, 'd'), (390, 844, 'm')]:
                pg = await b.new_page(viewport={'width': w, 'height': h})
                await pg.goto(base.rstrip('/') + path, wait_until='networkidle'); await pg.wait_for_timeout(800)
                H = await pg.evaluate('document.body.scrollHeight')
                for y in range(0, H, 350):
                    await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(80)
                await pg.wait_for_timeout(900); await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(600)
                await pg.screenshot(path=f'{out}/{name}-{s}.png', full_page=True)
                print(name, s, H); await pg.close()
        await b.close()

if __name__ == '__main__':
    if len(sys.argv) < 4: sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
