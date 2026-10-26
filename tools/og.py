#!/usr/bin/env python3
"""Gera as imagens de compartilhamento (Open Graph, 1200×630) na direção de arte do site:
papel claro, tinta azul-marinho, Newsreader + IBM Plex, régua milimetrada e uma FOTO REAL do laboratório
(sem filtro de cor, a partir das variantes de tools/foto_real.py).

  og-image.jpg        → padrão (home e páginas sem foto própria)
  og-trabalhos.jpg    → galeria /trabalhos/
  og-<serviço>.jpg    → cada página de serviço com foto real
  og-<artigo>.jpg     → cada artigo do blog com foto real

Uso:  python3 tools/foto_real.py && python3 tools/og.py      (depois rode o build)
Requer: playwright (python) com Chromium e Pillow.
"""
import asyncio, base64, html, io, json, sys
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / 'src' / 'assets'
sys.path.insert(0, str(ROOT / 'src' / 'content'))
from servicos import SERVICOS  # noqa: E402
from blog import POSTS  # noqa: E402
REAL = json.loads((ROOT / 'src' / 'fotos_reais.json').read_text(encoding='utf-8'))
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
LOGO = b64(ROOT / 'src' / 'private' / 'marca' / 'logo-lda.png')
FONTS = {k: b64(S / 'fonts' / f'{v}.woff2') for k, v in
         (('N', 'newsreader-500'), ('NI', 'newsreader-400-italic'), ('P', 'plex-sans'), ('M', 'plex-mono-500'))}


def foto(slug):
    """Maior JPEG da variante 4:5 (ou livre/3:2) da foto real → data URI."""
    for v in 'hgw':
        n = f'{slug}-{v}'
        if n in REAL:
            return b64(S / 'img' / 'real' / f"{n}-{REAL[n]['w']}.jpg")
    raise KeyError(slug)


def tpl(kicker, h1, sub, slug, size=60):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:N;src:url(data:font/woff2;base64,{FONTS['N']})}}
@font-face{{font-family:NI;src:url(data:font/woff2;base64,{FONTS['NI']})}}
@font-face{{font-family:P;src:url(data:font/woff2;base64,{FONTS['P']});font-weight:400 600}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{FONTS['M']})}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#F6F3EE;color:#0E1B2C;font-family:P;position:relative;overflow:hidden}}
.ph{{position:absolute;right:0;top:0;width:470px;height:630px;object-fit:cover;object-position:center}}
.l{{position:absolute;left:72px;top:64px;width:600px}}
.logo{{width:250px;display:block}}
.k{{margin-top:58px;font:500 17px/1 M;letter-spacing:.14em;text-transform:uppercase;color:#0B4F9E;border-top:1px solid #0E1B2C;padding-top:16px;display:flex;justify-content:space-between}}
h1{{margin-top:26px;font:500 {size}px/1.06 N;letter-spacing:-.015em;color:#0B2545}}
h1 em{{font-family:NI;font-weight:400}}
p{{margin-top:24px;font-size:23px;line-height:1.45;color:#545E6B}}
.ruler{{position:absolute;left:72px;bottom:44px;width:600px;height:14px;
background:repeating-linear-gradient(90deg,#0E1B2C 0 1px,transparent 1px 12px) bottom/100% 7px no-repeat,
repeating-linear-gradient(90deg,#0E1B2C 0 1px,transparent 1px 60px) bottom/100% 14px no-repeat;opacity:.55}}
.tag{{white-space:nowrap;position:absolute;right:20px;bottom:18px;font:500 12px/1 M;letter-spacing:.12em;color:#F6F3EE;text-transform:uppercase;background:rgba(14,27,44,.72);padding:7px 10px}}
</style></head><body>
<img class="ph" src="data:image/jpeg;base64,{foto(slug)}" alt="">
<div class="l">
<img class="logo" src="data:image/png;base64,{LOGO}" alt="">
<div class="k"><span>{kicker}</span><span>Belo Horizonte · MG</span></div>
<h1>{h1}</h1>
<p>{sub}</p>
</div><div class="ruler"></div><div class="tag">Foto: LDA</div>
</body></html>'''


def jobs():
    j = [('og-image', tpl('Desde 1975', 'Laboratório de<br>prótese dentária<br><em>em Belo Horizonte</em>',
                          'Zircônia, E-Max, protocolo, PPR e prótese total.<br>Coleta em MG · envios para todo o Brasil.',
                          'proteses-totais-cartao-lda')),
         ('og-trabalhos', tpl('Trabalhos', 'Fotos de trabalhos<br><em>do laboratório</em>',
                              'Prótese total, protocolo, E-Max, metalocerâmica,<br>PPR e Flexite, por categoria.', 'coroas-e-max-modelo-caixa-lda'))]
    for s in SERVICOS:
        if s['img'].startswith('real/'):
            nome = html.escape(s['nav'])
            j.append((f"og-{s['slug']}", tpl('Serviço', nome, 'Laboratório Dental Araújo<br>Sob orçamento · envio para todo o Brasil.',
                                              s['img'][5:], 60 if len(s['nav']) < 24 else 50)))
    for q in POSTS:
        if q['img'].startswith('real/'):
            t = html.escape(q['h1'])
            j.append((f"og-{q['slug']}", tpl('Blog · Artigo', t, 'Laboratório Dental Araújo · para dentistas', q['img'][5:],
                                              52 if len(q['h1']) < 40 else 44 if len(q['h1']) < 60 else 38)))
    return j


async def main():
    out = S / 'img' / 'og'
    for f in out.glob('og-*.jpg'): f.unlink()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        for name, h in jobs():
            await pg.set_content(h); await pg.wait_for_timeout(300)
            png = await pg.screenshot()
            Image.open(io.BytesIO(png)).convert('RGB').save(out / f'{name}.jpg', quality=84, optimize=True, progressive=True)
            print('ok', name)
        await b.close()

asyncio.run(main())
