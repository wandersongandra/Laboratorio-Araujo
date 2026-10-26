#!/usr/bin/env python3
"""QA de navegador: abre todas as URLs do sitemap (+ uma 404) em 1440, 1366 e 390 px e verifica
status HTTP, erros de JavaScript, avisos/erros de console (inclusive violações de CSP) e
rolagem horizontal.

Uso:  python3 tools/qa_paginas.py [URL_BASE]     (padrão http://localhost:8766, ver tools/serve.py)
Sai com código 1 se algo falhar. Requer playwright (python) com Chromium.
"""
import sys, asyncio, re
from pathlib import Path
from playwright.async_api import async_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8766').rstrip('/')
SITEMAP = Path(__file__).resolve().parent.parent / 'dist' / 'sitemap.xml'
PATHS = ['/' + re.sub(r'^https?://[^/]+/?', '', u) for u in re.findall(r'<loc>(.*?)</loc>', SITEMAP.read_text())]

async def main():
    falhas = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(1440, 900), (1366, 850), (390, 844)]:
            ctx = await b.new_context(viewport={'width': w, 'height': h})
            for path in PATHS + ['/nao-existe/']:
                pg = await ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
                r = await pg.goto(BASE + path, wait_until='load'); await pg.wait_for_timeout(600)
                await pg.mouse.wheel(0, 3000); await pg.wait_for_timeout(400)
                ov = await pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                esperado = 404 if path == '/nao-existe/' else 200
                if esperado == 404:   # o próprio documento 404 gera um aviso de console esperado
                    errs = [x for x in errs if 'status of 404' not in x]
                ok = r.status == esperado and not errs and not ov
                falhas += not ok
                print(w, r.status, path, 'ok' if ok else 'FALHA', errs[:3], 'ROLAGEM-HORIZONTAL' if ov else '')
                await pg.close()
            await ctx.close()
        await b.close()
    print('falhas:', falhas); sys.exit(1 if falhas else 0)

asyncio.run(main())
