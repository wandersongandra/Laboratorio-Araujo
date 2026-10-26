#!/usr/bin/env python3
"""QA de interação (auditoria 26/10/2026), com Playwright/Chromium:
  1. âncoras: para cada página do sitemap, abre cada #id linkado no site e cada #id que fica dentro
     de um acordeão (<details class="acc">); o alvo precisa ficar visível, com o <details> aberto,
     e dentro da tela;
  2. sem JavaScript: o conteúdo principal precisa estar visível (nada preso em opacity:0) e
     os acordeões continuam abríveis (são <details> nativos);
  3. prefers-reduced-motion: nenhuma animação CSS infinita rodando e conteúdo visível;
  4. menu móvel (390 px) por teclado: Tab até o botão, Enter abre (aria-expanded=true),
     Esc fecha e o foco volta ao botão.
Uso:  python3 tools/qa_interacao.py [URL_BASE]   (padrão http://localhost:8766)
Sai com código 1 se algo falhar."""
import sys, re, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8766').rstrip('/')
DIST = Path(__file__).resolve().parent.parent / 'dist'
PATHS = ['/' + re.sub(r'^https?://[^/]+/?', '', u) for u in re.findall(r'<loc>(.*?)</loc>', (DIST / 'sitemap.xml').read_text())]
falhas = []
def falha(m): falhas.append(m); print('  ✗', m)

def arquivo(path): return DIST / path.lstrip('/') / 'index.html'

def alvos():
    """(página, id) linkados no site + ids dentro de acordeões."""
    out = set()
    for path in PATHS:
        s = arquivo(path).read_text()
        for href in re.findall(r'href="([^"]*#[^"]+)"', s):
            p, frag = href.split('#', 1)
            if frag == 'conteudo': continue
            out.add((p or path, frag))
        for acc in re.findall(r'<details class="acc.*?</details>', s, re.S):
            for i in re.findall(r'\sid="([^"]+)"', acc): out.add((path, i))
    return sorted(out)

VISIVEL = """id => { const e = document.getElementById(id); if (!e) return 'inexistente';
  const d = e.closest('details'); if (d && !d.open) return 'details fechado';
  const r = e.getBoundingClientRect(); if (!r.width && !r.height) return 'sem caixa';
  if (r.bottom < 0 || r.top > innerHeight) return 'fora da tela (top=' + Math.round(r.top) + ')';
  return 'ok'; }"""

OCULTOS = """() => [...document.querySelectorAll('main h1, main h2, main p, main li, main img')]
  .filter(e => { const s = getComputedStyle(e); const r = e.getBoundingClientRect();
    return r.width && r.height && !e.closest('details:not([open])') && !e.closest('[aria-hidden=true]') &&
      (parseFloat(s.opacity) === 0 || s.visibility === 'hidden'); }).length"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # 1. âncoras
        ctx = await b.new_context(viewport={'width': 1366, 'height': 850})
        lista = alvos(); print(f'âncoras: {len(lista)}')
        for path, frag in lista:
            pg = await ctx.new_page()
            await pg.goto(f'{BASE}{path}#{frag}', wait_until='load'); await pg.wait_for_timeout(700)
            r = await pg.evaluate(VISIVEL, frag)
            if r != 'ok': falha(f'{path}#{frag}: {r}')
            await pg.close()
        await ctx.close()
        # 2 e 3. sem JS e movimento reduzido
        for rot, kw in [('sem JS', dict(java_script_enabled=False)), ('movimento reduzido', dict(reduced_motion='reduce'))]:
            ctx = await b.new_context(viewport={'width': 1366, 'height': 850}, **kw)
            for path in PATHS:
                pg = await ctx.new_page(); await pg.goto(BASE + path, wait_until='load'); await pg.wait_for_timeout(300)
                await pg.evaluate('window.scrollTo(0, document.body.scrollHeight)'); await pg.wait_for_timeout(300)
                n = await pg.evaluate(OCULTOS)
                if n: falha(f'{rot} {path}: {n} elemento(s) do conteúdo invisíveis')
                if 'reduz' in rot:
                    inf = await pg.evaluate("document.getAnimations().filter(a => a.effect && a.effect.getTiming().iterations === Infinity && a.playState === 'running').length")
                    if inf: falha(f'{rot} {path}: {inf} animação(ões) infinita(s) rodando')
                else:
                    acc = await pg.query_selector('details.acc:not([open]) > summary')
                    if acc:
                        await acc.click(); aberto = await pg.evaluate("document.querySelector('details.acc[open]') !== null")
                        if not aberto: falha(f'{rot} {path}: acordeão não abre')
                await pg.close()
            await ctx.close()
            print(f'{rot}: {len(PATHS)} páginas verificadas')
        # 4. menu móvel por teclado
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}); pg = await ctx.new_page()
        await pg.goto(BASE + '/', wait_until='load')
        for _ in range(12):
            await pg.keyboard.press('Tab')
            if await pg.evaluate("document.activeElement.id === 'burger'"): break
        else: falha('menu: botão do menu não recebe foco pelo Tab')
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400)
        if await pg.get_attribute('#burger', 'aria-expanded') != 'true': falha('menu: Enter não abre')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(400)
        if await pg.get_attribute('#burger', 'aria-expanded') != 'false': falha('menu: Esc não fecha')
        elif not await pg.evaluate("document.activeElement.id === 'burger'"): falha('menu: foco não volta ao botão após Esc')
        print('menu móvel: verificado')
        await b.close()
    print(f'\n{len(falhas)} falha(s)')
    sys.exit(1 if falhas else 0)

asyncio.run(main())
