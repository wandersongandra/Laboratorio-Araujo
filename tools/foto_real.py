#!/usr/bin/env python3
"""Exporta as FOTOS REAIS do laboratório para o site, SEM filtro de cor.

Diferente de tools/foto.py (que aplica a "grade" das imagens ilustrativas), aqui a cor é preservada:
só recorte, redimensionamento (Lanczos) e compressão. Para dentistas, cor fiel importa.

  - lê src/content/fotos_reais.py (retângulo do trabalho e variantes por foto);
  - variante 'h' 4:5, 'w' 3:2, 'g' livre: amplia o recorte com pixels reais da própria foto e,
    só quando falta foto, completa com o fundo escuro da borda (emenda suavizada), sem cortar o trabalho;
  - larguras 480/800/1200 (nunca maiores que o recorte original: não amplia);
  - AVIF + WebP + JPEG (fallback), sem EXIF/GPS/ICC/XMP (imagem nova, nenhum metadado copiado);
  - grava src/fotos_reais.json (larguras e dimensões), lido pelo build.

  - fotos do Drive: aplica a orientação EXIF (celular) ANTES do recorte e grava imagem nova (sem GPS).

Uso:  python3 tools/foto_real.py      (originais em /workspace/fotos-drive e /workspace/fotos-reais-originais;
      mude com FOTOS_DRIVE=… FOTOS_CHAT=…). Depois rode o build de novo.
Os originais NUNCA vão para src/assets, dist/ ou o zip: só as variantes otimizadas.
"""
import json, os, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src' / 'content'))
from fotos_reais import FOTOS  # noqa: E402

SRC = Path(os.environ.get('FOTOS_CHAT', '/workspace/fotos-reais-originais'))
DRIVE = Path(os.environ.get('FOTOS_DRIVE', '/workspace/fotos-drive'))
OUT = ROOT / 'src' / 'assets' / 'img' / 'real'
MAN = ROOT / 'src' / 'fotos_reais.json'
WIDTHS = (480, 800, 1200)
RATIO = {'h': 4 / 5, 'w': 3 / 2, 'g': None}
MARGEM = 0.04          # folga em volta do trabalho


def bg_color(im):
    """Cor de fundo = mediana da borda externa (as fotos têm fundo preto, às vezes com vinheta)."""
    w, h = im.size; b = max(4, round(min(w, h) * 0.02))
    strip = Image.new('RGB', (160, 40))
    for i, box in enumerate(((0, 0, w, b), (0, h - b, w, h), (0, 0, b, h), (w - b, 0, w, h))):
        strip.paste(im.crop(box).resize((40, 40)), (40 * i, 0))
    return tuple(ImageStat.Stat(strip).median)


def frame(im, reg, ratio, fill='pad'):
    """Caixa de recorte contendo o trabalho + margem. fill='pad': pode sair da foto (o que falta vira
    fundo escuro). fill='crop' (foto cujo modelo encosta na borda): a caixa encolhe até caber na foto."""
    W, H = im.size
    x0, y0, x1, y1 = reg[0] * W, reg[1] * H, reg[2] * W, reg[3] * H
    mx, my = (x1 - x0) * MARGEM, (y1 - y0) * MARGEM
    x0, x1 = max(0, x0 - mx), min(W, x1 + mx); y0, y1 = max(0, y0 - my), min(H, y1 + my)
    if ratio:
        w, h = x1 - x0, y1 - y0
        if w / h < ratio: nw, nh = h * ratio, h
        else: nw, nh = w, w / ratio
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if fill == 'crop':
            k = min(W / nw, H / nh, 1); nw, nh = nw * k, nh * k

        def fit(c, n, lim):           # centraliza; se couber na foto, desliza para dentro dela
            a = c - n / 2
            if n <= lim: a = min(max(a, 0), lim - n)
            return a
        x0, y0 = fit(cx, nw, W), fit(cy, nh, H); x1, y1 = x0 + nw, y0 + nh
    return tuple(round(v) for v in (x0, y0, x1, y1))


def compose(im, box, bg):
    x0, y0, x1, y1 = box; W, H = im.size
    cw, ch = x1 - x0, y1 - y0
    if x0 >= 0 and y0 >= 0 and x1 <= W and y1 <= H:
        return im.crop(box), False
    canvas = Image.new('RGB', (cw, ch), bg)
    sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    part = im.crop((sx0, sy0, sx1, sy1))
    # emenda suave só nos lados em que houve preenchimento
    f = max(6, round(min(part.size) * 0.035))
    mask = Image.new('L', part.size, 255); pw, ph = part.size
    grad = [round(255 * (i + 1) / (f + 1)) for i in range(f)]
    mp = mask.load()
    for yy in range(ph):
        for i, v in enumerate(grad):
            if x0 < 0: mp[i, yy] = min(mp[i, yy], v)
            if x1 > W: mp[pw - 1 - i, yy] = min(mp[pw - 1 - i, yy], v)
    for xx in range(pw):
        for i, v in enumerate(grad):
            if y0 < 0: mp[xx, i] = min(mp[xx, i], v)
            if y1 > H: mp[xx, ph - 1 - i] = min(mp[xx, ph - 1 - i], v)
    canvas.paste(part, (sx0 - x0, sy0 - y0), mask)
    return canvas, True


def save_all(img, name, maxw):
    cw = img.size[0]
    top = min(cw, maxw or WIDTHS[-1], WIDTHS[-1])
    ws = sorted({w for w in WIDTHS if w < top} | {top})
    if len(ws) > 1 and ws[-1] - ws[-2] < 160: ws.pop(-2)        # evita larguras quase iguais
    for w in ws:
        h = round(img.size[1] * w / cw)
        x = img.resize((w, h), Image.LANCZOS) if w != cw else img.copy()
        clean = Image.new('RGB', x.size); clean.paste(x)          # imagem nova: nenhum metadado herdado
        clean.save(OUT / f'{name}-{w}.avif', 'AVIF', quality=62, speed=4)
        clean.save(OUT / f'{name}-{w}.webp', 'WEBP', quality=82, method=6)
        if w in (ws[0], ws[-1]):    # JPEG: só fallback (navegador sem AVIF/WebP) e a maior (JSON-LD, ampliação)
            clean.save(OUT / f'{name}-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    return ws, img.size


def abrir(ft):
    """Original → RGB já na orientação certa, sem nenhum metadado (EXIF/GPS/ICC/XMP)."""
    if ft.get('src'): path = DRIVE / ft['src']
    else: path = next(SRC.glob(ft['id'] + '*.jpg'))
    src = Image.open(path); src = ImageOps.exif_transpose(src); src.load()
    im = Image.new('RGB', src.size); im.paste(src.convert('RGB'))
    if ft.get('pre'):
        W, H = im.size; a = ft['pre']
        im = im.crop((round(a[0] * W), round(a[1] * H), round(a[2] * W), round(a[3] * H)))
    return im


def exportar(ft):
    im = abrir(ft); bg = bg_color(im); res = {}; log = []
    for v, reg in ft['var'].items():
        box = frame(im, reg or ft['reg'], RATIO[v], ft.get('fill', 'pad'))
        out, pad = compose(im, box, bg)
        name = f"{ft['slug']}-{v}"
        ws, (cw, ch) = save_all(out, name, ft.get('maxw'))
        top = ws[-1]
        res[name] = dict(ws=ws, w=top, h=round(ch * top / cw), pad=pad, src=ft['id'])
        log.append(f"{ft['id']} {v} box={box} crop={cw}x{ch} pad={pad} -> {ws}")
    return res, log


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob('*'): f.unlink()
    man = {}
    with ProcessPoolExecutor(max(1, (os.cpu_count() or 2) - 1)) as ex:
        for res, log in ex.map(exportar, FOTOS):
            man.update(res); print('\n'.join(log), flush=True)
    MAN.write_text(json.dumps(man, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    tot = sum(p.stat().st_size for p in OUT.glob('*'))
    print(f'ok: {len(FOTOS)} fotos, {len(man)} variantes, {len(list(OUT.glob("*")))} arquivos, {tot/1e6:.1f} MB em {OUT}')

if __name__ == '__main__':
    main()
