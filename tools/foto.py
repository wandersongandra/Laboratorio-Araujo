#!/usr/bin/env python3
"""Tratamento de cor único das fotos do site + recorte + exportação WebP (640 e 1200 px).

Todas as imagens do site passam por aqui para ficarem com a mesma "cara": saturação contida,
leve split-tone (sombras azul-marinho, luzes porcelana), preto levantado e luvas
verde-água/ciano dessaturadas (não brigam com o azul da marca).

Uso (troca por foto real do laboratório — mesmo nome = nenhuma mudança no build):
    python3 tools/foto.py CAMINHO/foto-original.jpg bancada-tecnico 4/5
    python3 tools/foto.py CAMINHO/foto.jpg fachada-recepcao 3/2 0.5 0.4   # foco x y (0–1)
Gera _build/static/assets/img/foto/<nome>-640.webp e <nome>-1200.webp. Proporções usadas no
site: 4/5 (retrato) e 3/2 (paisagem). Requer Pillow e numpy.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parent.parent / '_build' / 'static' / 'assets' / 'img' / 'foto'
NAVY = np.array([16, 38, 70], float)
WARM = np.array([246, 238, 226], float)

def grade(im, sat=.42, amt=.22):
    a = np.asarray(im.convert('RGB'), float)
    L = (a @ [.2126, .7152, .0722])[..., None]
    cy = np.clip(((a[..., 1:2] + a[..., 2:3]) / 2 - a[..., 0:1] - 10) / 70, 0, 1)  # tons ciano
    a = L + (a - L) * sat * (1 - .7 * cy)          # saturação contida (menor no ciano)
    tint = NAVY * (1 - L / 255) + WARM * (L / 255)
    a = a * (1 - amt) + tint * amt                 # split-tone
    a = a * 0.93 + 12                              # preto levantado (acabamento fosco)
    a = (a - 128) * 1.04 + 128                     # contraste leve
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))

def out(src, name, ratio=None, focus=(.5, .5), sizes=(640, 1200), q=78):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if ratio:
        W, H = im.size
        if W / H > ratio:
            nw = int(H * ratio); x = int((W - nw) * focus[0]); im = im.crop((x, 0, x + nw, H))
        else:
            nh = int(W / ratio); y = int((H - nh) * focus[1]); im = im.crop((0, y, W, y + nh))
    g = grade(im)
    OUT.mkdir(parents=True, exist_ok=True)
    for s in sizes:
        x = g.copy(); x.thumbnail((s, s * 3)); x.save(OUT / f'{name}-{s}.webp', 'WEBP', quality=q, method=6)
    return g.size

def ratio(t):
    a, _, b = t.partition('/'); return float(a) / float(b or 1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    r = ratio(sys.argv[3]) if len(sys.argv) > 3 else None
    f = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (.5, .5)
    print(sys.argv[2], out(sys.argv[1], sys.argv[2], r, f))
