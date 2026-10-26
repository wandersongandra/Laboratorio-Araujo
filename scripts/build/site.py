#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderização do site: imagens, layouts, blocos, páginas, SEO e meta.

Parte modular do gerador (`python -m scripts.build`). A lógica HTML/JSON-LD
permanece aqui para preservar a saída; config/minify/security/util ficam à parte.
"""
from __future__ import annotations

import json
import re
from PIL import Image as _PIL

from .config import (
    ADDR,
    ADDR_FOOTER_L1,
    ADDR_FOOTER_L2,
    ADDR_UTIL,
    ASSETS,
    BASE,
    CNPJ,
    DIST,
    EMAIL,
    FB,
    FIN_PHONE_SCHEMA,
    FIN_WA_SCHEMA,
    FOTOS_JSON,
    HOURS_CURTO,
    HOURS_FOOTER,
    HOURS_FRASE,
    HOURS_LONGO,
    IG,
    LAB,
    LEGAL_NAME,
    MAPS,
    NAME,
    PHONE_1_DISPLAY,
    PHONE_1_SCHEMA,
    PHONE_1_TEL,
    PHONE_2_DISPLAY,
    PHONE_2_SCHEMA,
    PHONE_2_TEL,
    STREET_SCHEMA,
    TODAY,
    WA,
    WA_DISPLAY,
    WA_SCHEMA,
    modificado,
)
from .util import e, lc, nobreak, strip, telclass, ver, wa
from .minify import copy_and_minify_assets
from .security import INLINE_JS, headers_file

from .content_loader import (
    CATS,
    CONDICOES,
    FAIXA_REAL,
    FACTS,
    FAQ_GROUPS,
    FOTOS_REAIS,
    FR_CATS,
    FR_ID,
    FR_SLUG,
    GARANTIA,
    POSTS,
    PRAZO,
    PRIVACIDADE,
    RESUMO,
    RESUMO_ENVIO,
    RESUMO_SOBRE,
    SERVICOS,
    TAG,
    TERMOS,
    VIGENCIA,
    porque,
)

CAT = {c["id"]: c for c in CATS}
SVC = {s["slug"]: s for s in SERVICOS}


def fill(t: str) -> str:
    return t.replace("{PRAZO}", PRAZO).replace("{GARANTIA}", GARANTIA)


# ------------------------------------------------------------------ 4. imagens e ícones
# Dois tipos de foto:
#  - 'foto/<nome>': imagens ILUSTRATIVAS (banco de imagens), webp 640/1200 (tools/foto.py);
#  - 'real/<slug>': fotos REAIS do laboratório (tools/foto_real.py, sem filtro de cor), em <picture>
#    AVIF + WebP + JPEG de reserva, larguras 480/800/1200, variantes 'h' 4:5, 'w' 3:2 e 'g' livre.
# img() escreve srcset + width/height reais (evita CLS); fotos abaixo da dobra usam loading=lazy.
_DIM = {}
REAL = json.loads(FOTOS_JSON.read_text(encoding='utf-8'))
PAGE_IMGS = {}     # fotos reais usadas na página em construção (sitemap de imagens), zerado em out()

def is_real(base): return base.startswith('real/')

def rvar(base, pref='wgh'):
    """Nome da variante exportada de uma foto real, na ordem de preferência dada."""
    slug = base[5:]
    for v in pref:
        if f'{slug}-{v}' in REAL: return f'{slug}-{v}'
    raise KeyError(base)

def real_meta(base):
    return FR_SLUG[base[5:]]

def img_url(base, pref='wgh'):
    """URL absoluta da maior versão (JPEG para foto real) — JSON-LD, sitemap de imagens, ampliação."""
    if is_real(base):
        n = rvar(base, pref); return BASE + f"/assets/img/real/{n}-{REAL[n]['w']}.jpg"
    return BASE + f"/assets/img/{base}-1200.webp"

def img_obj(base, pref='wgh'):
    """ImageObject (foto real, com crédito do laboratório) ou só a URL (imagem ilustrativa)."""
    if not is_real(base): return img_url(base)
    n = rvar(base, pref); m = real_meta(base)
    return {"@type": "ImageObject", "url": img_url(base, pref), "contentUrl": img_url(base, pref),
            "width": REAL[n]['w'], "height": REAL[n]['h'], "caption": m['alt'], "creditText": NAME,
            "creator": {"@id": BIZ_ID}, "copyrightHolder": {"@id": BIZ_ID}}

def dims(base, size=640):
    if is_real(base):
        n = rvar(base); return REAL[n]['w'], REAL[n]['h']
    k = (base, size)
    if k not in _DIM:
        with _PIL.open(ASSETS / 'img' / f'{base}-{size}.webp') as im: _DIM[k] = im.size
    return _DIM[k]

def _srcset(n, ext):
    return ', '.join(f'/assets/img/real/{n}-{w}.{ext} {w}w' for w in REAL[n]['ws'])

def _jpgs(n):
    ws = REAL[n]['ws']; return [w for w in (ws[0], ws[-1])] if len(ws) > 1 else ws

def real_img(base, alt, cls='', lazy=True, sizes='(max-width:1024px) 92vw, 640px', prio=False, pref='wgh', alt_mobile=None):
    """<picture> com AVIF e WebP (srcset responsivo) e <img> JPEG de reserva, sem metadados (EXIF/GPS).
    alt_mobile: variante para telas ≤1024px (direção de arte do topo: 4:5 no desktop, 3:2 no celular)."""
    n = rvar(base, pref); r = REAL[n]
    PAGE_IMGS.setdefault(img_url(base, pref), alt or real_meta(base)['alt'])
    src = ''
    if alt_mobile:
        m = rvar(base, alt_mobile)
        if m != n:
            for t, ext in (('avif', 'avif'), ('webp', 'webp')):
                src += (f'<source media="(max-width:1024px)" type="image/{t}" srcset="{_srcset(m, ext)}" sizes="{sizes}"'
                        f' width="{REAL[m]["w"]}" height="{REAL[m]["h"]}">')
    src += f'<source type="image/avif" srcset="{_srcset(n, "avif")}" sizes="{sizes}"><source type="image/webp" srcset="{_srcset(n, "webp")}" sizes="{sizes}">'
    j = _jpgs(n)
    a = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if prio else '')
    c = f' class="{cls}"' if cls else ''
    jset = ', '.join(f'/assets/img/real/{n}-{w}.jpg {w}w' for w in j)
    return (f'<picture>{src}<img{c} src="/assets/img/real/{n}-{j[0]}.jpg" srcset="{jset}" sizes="{sizes}"'
            f' alt="{e(alt)}" width="{r["w"]}" height="{r["h"]}"{a}></picture>')

def img(base, alt, cls='', lazy=True, sizes='(max-width:1024px) 92vw, 640px', prio=False, only640=False, pref='wgh', alt_mobile=None):
    """base: 'foto/zirconia-estrutura' (ilustrativa, webp 640/1200) ou 'real/<slug>' (foto do LDA)."""
    if is_real(base):
        return real_img(base, alt, cls, lazy, '200px' if only640 else sizes, prio, pref, alt_mobile)
    b = f'/assets/img/{base}'
    w, h = dims(base)
    a = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if prio else '')
    c = f' class="{cls}"' if cls else ''
    ss = '' if only640 else f' srcset="{b}-640.webp 640w, {b}-1200.webp 1200w" sizes="{sizes}"'
    return f'<img{c} src="{b}-640.webp"{ss} alt="{e(alt)}" width="{w}" height="{h}"{a}>'

def ratio(base, pref='wgh'):
    if is_real(base):
        n = rvar(base, pref); return 'r32' if REAL[n]['w'] > REAL[n]['h'] else ''
    w, h = dims(base); return 'r32' if w > h else ''

def tag_for(base):
    """Rótulo da legenda: foto real do laboratório × imagem ilustrativa (banco de imagens)."""
    return 'Foto: LDA' if is_real(base) else 'Imagem ilustrativa'

def preload_tags(base, pref, mobile=None, sizes=None, media=None):
    """<link rel=preload> da foto LCP: AVIF da variante certa para cada faixa de tela."""
    sz = sizes or HERO_SIZES
    if not is_real(base):
        b = f"/assets/img/{base}"
        return f'<link rel="preload" as="image" type="image/webp" href="{b}-640.webp" imagesrcset="{b}-640.webp 640w, {b}-1200.webp 1200w" imagesizes="{sz}" fetchpriority="high">\n'
    n = rvar(base, pref); m = rvar(base, mobile) if mobile else n
    def one(v, media):
        md = f' media="{media}"' if media else ''
        return (f'<link rel="preload" as="image" type="image/avif" href="/assets/img/real/{v}-{REAL[v]["ws"][0]}.avif"'
                f' imagesrcset="{_srcset(v, "avif")}" imagesizes="{sz}"{md} fetchpriority="high">\n')
    if m == n: return one(n, media or '')
    return one(m, '(max-width:1024px)') + one(n, '(min-width:1025px)')

# ícones de linha próprios: grade 24, traço 1.5, pontas arredondadas
IC = {
 'chat': '<path d="M4 5.5h16v10.5H10l-4.5 3.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/>',
 'truck': '<path d="M2.5 6.5h11v9.5h-11zM13.5 9.5h4l3 3v3.5h-7"/><circle cx="6.5" cy="17.5" r="1.7"/><circle cx="17" cy="17.5" r="1.7"/>',
 'bench': '<path d="M3 20.5h18M6 20.5v-5h12v5"/><path d="M9.5 15.5l5.5-9 2.2 1.3-4.6 7.7"/><circle cx="16.3" cy="5.3" r="1.3"/>',
 'box': '<path d="M3.5 8L12 4l8.5 4v8.5L12 20.5l-8.5-4z"/><path d="M3.5 8L12 12l8.5-4M12 12v8.5"/>',
 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'shield': '<path d="M12 3.5l7.5 3v5.5c0 4.2-3.2 7.4-7.5 8.5-4.3-1.1-7.5-4.3-7.5-8.5V6.5z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
 'pin': '<path d="M12 21s6.5-6.6 6.5-11.5a6.5 6.5 0 0 0-13 0C5.5 14.4 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.3"/>',
 'down': '<path d="M12 4v11M7.5 10.5L12 15l4.5-4.5M5 19.5h14"/>',
 'phone': '<path d="M6.5 3.5h3l1.5 4-2 1.3a10 10 0 0 0 6.2 6.2l1.3-2 4 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5.5a2 2 0 0 1 2-2z"/>',
 'camera': '<path d="M3.5 7.5h4l1.5-2h6l1.5 2h4v11h-17z"/><circle cx="12" cy="13" r="3.5"/>',
 'ruler': '<path d="M3 15.5L15.5 3l5.5 5.5L8.5 21z"/><path d="M7 11.5l2 2M10 8.5l1.5 1.5M13 5.5l2 2M5.5 14.5l1 1"/>',
}
def icon(n, cls='ico'): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{IC[n]}</svg>'

# ------------------------------------------------------------------ 5. estrutura comum: cabeçalho, rodapé, <head>
NAV = [('/servicos/', 'Serviços'), ('/envio-para-todo-brasil/', 'Envio'), ('/sobre/', 'Sobre'),
       ('/perguntas-frequentes/', 'FAQ'), ('/blog/', 'Blog'), ('/contato/', 'Contato')]
MSG = 'Olá! Sou dentista e gostaria de enviar um caso para o laboratório.'
MSG_ORC = 'Olá! Sou dentista e gostaria de solicitar um orçamento.'

def header():
    drop = ''.join(f'<a href="/servicos/{s["slug"]}/">{s["nav"]}<i>{i+1:02d}</i></a>' for i, s in enumerate(SERVICOS))
    items = []
    for u, t in NAV:
        if u == '/servicos/':
            items.append(f'<div class="nav__group"><a href="{u}" data-nav>{t}</a>'
                         f'<button class="nav__more" type="button" aria-expanded="false" aria-label="Mostrar serviços"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>'
                         f'<div class="nav__drop">{drop}<a class="all" href="/servicos/">Todos os serviços <i>→</i></a></div></div>')
        else:
            items.append(f'<a href="{u}" data-nav>{t}</a>')
    return f'''<section class="util" aria-label="Contato rápido"><div class="container">
  <span>{HOURS_CURTO}</span><span>{ADDR_UTIL}</span>
  <span class="sp"><a href="{PHONE_1_TEL}" data-track="phone_util">{PHONE_1_DISPLAY}</a></span><span><a href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_util">WhatsApp {WA_DISPLAY}</a></span>
</div></section>
<header class="header" id="topo">
  <div class="container header__inner">
    <a href="/" class="brand" aria-label="{NAME}, página inicial"><img src="/assets/img/marca/logo-lda.webp" alt="LDA {NAME}" width="453" height="96"></a>
    <nav class="nav" id="nav" aria-label="Menu principal">
      {"".join(items)}
      <a class="btn btn--sm nav__cta" href="{wa(MSG)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_header">Enviar caso</a>
    </nav>
    <button type="button" class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>'''

def footer():
    svc = ''.join(f'<a href="/servicos/{s["slug"]}/">{s["nav"]}</a>' for s in SERVICOS)
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <img src="/assets/img/marca/logo-lda-branco.webp" alt="LDA {NAME}" class="footer__logo" width="453" height="96" loading="lazy">
        <p class="footer__nap"><b>{NAME}</b><br>{ADDR_FOOTER_L1}<br>{ADDR_FOOTER_L2}<br>
        <a href="{PHONE_1_TEL}">{PHONE_1_DISPLAY}</a> · <a href="{PHONE_2_TEL}">{PHONE_2_DISPLAY}</a><br>
        <a href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_footer">WhatsApp {WA_DISPLAY}</a><br>{HOURS_FOOTER}</p>
        <div class="footer__social"><a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram</a><a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook</a><a href="{MAPS}" target="_blank" rel="noopener noreferrer">Google Maps</a></div>
      </div>
      <div><h2>Serviços</h2><nav aria-label="Serviços">{svc}</nav></div>
      <div><h2>Laboratório</h2><nav aria-label="Institucional"><a href="/envio-para-todo-brasil/">Envio para todo o Brasil</a><a href="/sobre/">Sobre o laboratório</a><a href="/trabalhos/">Trabalhos (fotos)</a><a href="/perguntas-frequentes/">Perguntas frequentes</a><a href="/blog/">Blog</a><a href="/contato/#orcamento">Solicitar orçamento</a><a href="/contato/">Contato</a></nav></div>
      <div><h2>Leitura</h2><nav aria-label="Blog">{"".join(f'<a href="/blog/{p["slug"]}/">{p["h1"]}</a>' for p in POSTS_RECENTES)}</nav></div>
    </div>
    <div class="footer__base"><span>© <span id="year">2026</span> {LEGAL_NAME} · CNPJ {CNPJ}</span><nav class="footer__legal" aria-label="Documentos legais"><a href="/politica-de-privacidade/">Política de privacidade</a><a href="/termos-de-uso/">Termos de uso</a></nav><span class="footer__sign"><span>Laboratório de prótese dentária em Belo Horizonte, MG, desde 1975</span><span class="footer__credit">Desenvolvido por <a href="https://www.gandra.tech/" target="_blank" rel="noopener">gandra.tech</a></span></span></div>
  </div>
</footer>'''

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3z" class="o"/><path d="M11.5 9.5c.4-.1.9 0 1.1.5l1 2.4c.1.4 0 .8-.3 1l-.8.8a8.6 8.6 0 0 0 4.3 4.3l.8-.8c.3-.3.7-.4 1-.3l2.4 1c.5.2.6.7.5 1.1-.3 1.4-1.6 2.3-3 2.1A10.5 10.5 0 0 1 9.4 12.5c-.2-1.4.7-2.7 2.1-3z" class="f"/></svg>'
WIDGETS = f'<section aria-label="Atendimento por WhatsApp"><a class="wa" href="{wa("Olá! Sou dentista e gostaria de mais informações.")}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_float" aria-label="Conversar no WhatsApp">{WA_SVG}<span>WhatsApp</span></a></section>'

FONTS = ['newsreader-500', 'newsreader-400-italic', 'plex-sans']   # itálico: evita CLS do .hl no H1 (auditoria 26/10)

def page(p, main, graph):
    """Monta o HTML completo de uma página.
    p: dict(path, title ≤60, desc, preload? (foto do topo), og_type?, og_title?, date?, noindex?)
    main: HTML do <main>; graph: nós JSON-LD da página (Organization e WebSite entram sempre)."""
    url = BASE + p['path']
    assert len(p['title']) <= 60, (p['path'], len(p['title']), p['title'])
    ld = json.dumps({"@context": "https://schema.org", "@graph": [business(), website()] + graph}, ensure_ascii=False, separators=(',', ':'))
    ld = ld.replace('<', '\\u003c')   # nenhum texto do JSON-LD consegue fechar o <script> (defesa em profundidade)
    pre = ''.join(f'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/{f}.woff2" crossorigin>\n' for f in FONTS)
    if p.get('preload'):
        pre += preload_tags(p['preload'], p.get('preload_pref', 'hwg'), p.get('preload_mobile'), p.get('preload_sizes'), p.get('preload_media'))
    robots = 'noindex, follow' if p.get('noindex') else 'index, follow, max-image-preview:large, max-snippet:-1'
    og_img = BASE + '/assets/img/og/' + p.get('og', 'og-image') + '.jpg'
    extra = ''
    if p.get('og_type') == 'article':
        extra = f'<meta property="article:published_time" content="{p["date"]}">\n<meta property="article:modified_time" content="{TODAY}">\n'
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#F6F3EE">
<meta name="geo.region" content="BR-MG">
<meta name="geo.placename" content="Belo Horizonte">
<meta name="geo.position" content="-19.9162258;-43.9407838">
<meta name="ICBM" content="-19.9162258, -43.9407838">
<meta property="og:type" content="{p.get("og_type","website")}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(p.get("og_title", p["title"]))}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(p.get("og_alt", NAME + ", laboratório de prótese dentária em Belo Horizonte"))}">
{extra}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(p.get("og_title", p["title"]))}">
<meta name="twitter:description" content="{e(p["desc"])}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt">
{pre}<link rel="stylesheet" href="/assets/css/style.css?v={ver('assets/css/style.css')}">
<script>{INLINE_JS}</script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
{header()}
<main id="conteudo">
{main}
</main>
{footer()}
{WIDGETS}
<script src="/assets/js/main.js?v={ver('assets/js/main.js')}" defer></script>
</body>
</html>
'''

# ------------------------------------------------------------------ 6. blocos reutilizáveis
HERO_SIZES = '(max-width:1024px) 92vw, 440px'

def crumbs_html(trail):
    lis = []
    for i, (n, u) in enumerate(trail):
        lis.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{u}">{e(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Você está aqui"><ol>{"".join(lis)}</ol></nav>'

def cta_btns(msg=None, contato=True):
    m = msg if isinstance(msg, str) else MSG_ORC
    c = '<a class="arrow" href="/contato/">Outros canais de contato</a>' if contato else ''
    return f'<div class="btns"><a class="btn" href="{wa(m)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_hero">{icon("chat")}Solicitar orçamento</a>{c}</div>'

def phero(trail, kicker, h1, lead, media=None, media_alt='', cta=True, meta='', cap='Imagem ilustrativa'):
    btns = cta_btns(cta, trail[-1][1] != '/contato/') if cta else ''
    if media:
        if is_real(media):
            cap = tag_for(media); capt = real_meta(media)['cap']
            im = img(media, media_alt, lazy=False, prio=True, sizes=HERO_SIZES, pref='hwg', alt_mobile='wgh')
            r = ratio(media, 'hwg')
        else:
            capt = media_alt; im = img(media, media_alt, lazy=False, prio=True, sizes=HERO_SIZES); r = ratio(media)
        fig = (f'<figure class="phero__media intro-3"><div class="frame curtain {r}">{im}</div>'
               f'<figcaption class="cap"><span>{e(capt)}</span><span>{cap}</span></figcaption></figure>')
    else:
        fig = ''
    return f'''<section class="phero{" phero--photo" if media else ""}" aria-labelledby="h1">
  <div class="container">
    {crumbs_html(trail)}
    <div class="phero__grid">
      <div class="phero__text">
        <span class="label intro">{kicker}</span>
        <h1 id="h1" class="intro">{h1}</h1>
        <p class="phero__lead intro-2">{lead}</p>
        <div class="intro-2">{btns}{meta}</div>
      </div>
      {fig}
    </div>
  </div>
</section>'''

def shead(n, label, title, p='', hid=None, link=None):
    lk = f'<br><a class="arrow" href="{link[0]}">{link[1]}</a>' if link else ''
    pp = f'<p class="shead__p">{p}{lk}</p>' if (p or link) else ''
    return f'''<div class="shead rv"><span class="shead__n">{n} / {label}</span>
  <div class="shead__t"><h2{f' id="{hid}"' if hid else ''}>{title}</h2></div>{pp}</div>'''

ICON = {
 'porcelana': '<path d="M7 3.5c-2 0-3 1.5-3 4 0 3 1 5 1.5 8S6 20.5 7.5 20.5c1.4 0 1.5-4 3-5h3c1.5 1 1.6 5 3 5 1.5 0 2-3 2.5-6S20 10.5 20 7.5c0-2.5-1-4-3-4-1.7 0-3 1-5 1S8.7 3.5 7 3.5z"/>',
 'metaloceramica': '<path d="M7 3.5c-2 0-3 1.5-3 4 0 2 .4 3.6.9 5.2h14.2c.5-1.6.9-3.2.9-5.2 0-2.5-1-4-3-4-1.7 0-3 1-5 1S8.7 3.5 7 3.5z"/><path d="M4.9 12.7c.3 1 .5 1.9.6 2.8.5 3 .5 5 2 5 1.4 0 1.5-4 3-5h3c1.5 1 1.6 5 3 5 1.5 0 1.5-2 2-5 .1-.9.3-1.8.6-2.8"/>',
 'rmf': '<path d="M8 3.5h8l1.5 6H6.5z"/><path d="M9 9.5v4.5M15 9.5v4.5M7.5 14h9l-1.5 6.5h-6z"/>',
 'resinas': '<path d="M9 3.5h6v3.5l3 3v11H6v-11l3-3z"/><path d="M6 14h12"/>',
 'implantes': '<path d="M8 3.5h8l-1 3.5H9zM9.5 7v13.5h5V7M9.5 10.5h5M9.5 14h5M9.5 17.5h5"/>',
 'ppr-roach': '<path d="M3.5 14c3-6 14-6 17 0M6.5 14v4M17.5 14v4M9.5 12v6h5v-6"/>',
 'ppr-parcial': '<path d="M3.5 12c4-5 13-5 17 0-4 5-13 5-17 0z"/><path d="M9 10v4M12 9.5v5M15 10v4"/>',
 'ptr': '<path d="M3.5 9.5c3-4 14-4 17 0v3c-3 4-14 4-17 0z"/><path d="M7.5 8.3v5.4M12 7.5v7M16.5 8.3v5.4"/>',
 'placas': '<path d="M4 10.5c0-3 4-5 8-5s8 2 8 5-3 6-8 6-8-3-8-6z"/><path d="M8 10.5c1 1.5 7 1.5 8 0"/>',
}
def pcard(c, ci):
    """Cartão com os itens de uma linha de serviço (sem preços: tudo é sob orçamento)."""
    lis = ''.join(f'<li class="pitem">{e(n)}</li>' for n in c['items'])
    obs = ''.join(f'<span>{e(o)}</span>' for o in c['obs'])
    n = len(c['items'])
    return f'''<article class="pcat" id="itens-{c["id"]}">
  <header class="pcat__head"><span class="pcat__ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICON[c["id"]]}</svg></span><div><h3>{c["title"]}</h3><span class="pcat__count">{ci+1:02d} · {n} {"itens" if n > 1 else "item"}</span></div></header>
  <ul class="plist">{lis}</ul>
  <p class="pcat__obs">{obs}</p>
</article>'''


def card(href, im, alt, label, title, text, foot_l, foot_r):
    return (f'<a class="card rv" href="{href}"><div class="card__img">{img(im, alt, sizes="(max-width:760px) 92vw, 400px")}</div>'
            f'<span class="label label--plain label--card">{label}</span><h3>{title}</h3><p>{text}</p>'
            f'<div class="card__foot"><span>{foot_l}</span><span>{foot_r}</span></div></a>')

def svc_card(s):
    return card(f'/servicos/{s["slug"]}/', s['img'], s['img_alt'], s['kicker'], s['nav'], s['blurb'], 'Ver serviço', '→')

def post_card(q):
    d = q['date'].split('-')
    return card(f'/blog/{q["slug"]}/', q['img'], q['img_alt'], f'Artigo · {d[2]}/{d[1]}/{d[0]}', q['h1'], q['desc'], 'Ler artigo', '→')

def related(slugs, title='Serviços relacionados', n='§'):
    return f'''<section class="sec sec--stone" aria-labelledby="rel-title">
  <div class="container">
    {shead(n, 'Veja também', title, hid='rel-title')}
    <div class="cards">{"".join(svc_card(SVC[s]) for s in slugs)}</div>
  </div>
</section>'''

def cta_band(h='Tem um caso <em>para enviar?</em>', p='Chame no WhatsApp para combinar material, prazo e a coleta em Minas Gerais ou o envio de outro estado.', msg=MSG):
    return f'''<section class="cta" aria-labelledby="cta-title">
  <div class="container cta__grid">
    <h2 id="cta-title" class="rv">{h}</h2>
    <div class="cta__side rv"><p>{p}</p>
      <div class="btns"><a class="btn btn--light" href="{wa(msg)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_cta">{icon("chat")}WhatsApp (31) 98652-1387</a><a class="btn btn--line-light" href="tel:+553132719766" data-track="phone_cta">{icon("phone")}(31) 3271-9766</a></div>
    </div>
  </div>
</section>'''

def faq_block(pairs, title='Perguntas frequentes', hid='faq-title', n='§', label='Dúvidas', p='', link=None):
    d = '\n'.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    lk = f'<a class="arrow" href="{link[0]}">{link[1]}</a>' if link else ''
    return f'''<div class="faq">
  <div class="faq__head rv"><span class="shead__n">{n} / {label}</span><h2 id="{hid}">{title}</h2>{f"<p>{p}</p>" if p else ""}{lk}</div>
  <div class="faq__list rv">{d}</div>
</div>'''

def faq_section(pairs, title='Perguntas frequentes', hid='faq-title', n='§', p='', link=None, cls=''):
    return f'<section class="sec {cls}" aria-labelledby="{hid}"><div class="container">{faq_block(pairs, title, hid, n, p=p, link=link)}</div></section>'

def facts_block(title='Ficha técnica do laboratório', hid='facts-title', n='§', cls='', extra=''):
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in FACTS)
    return f'''<section class="sec {cls}" aria-labelledby="{hid}">
  <div class="container">
    {shead(n, 'Dados', title, 'Endereço, equipe, prazos e garantia do laboratório.', hid=hid)}
    <dl class="facts rv">{dl}</dl>{extra}
  </div>
</section>'''

def aside_card(s=None):
    if s:
        msg = f'Olá! Sou dentista e gostaria de um orçamento de {s["nav"]}.'
        t = s['nav']; h = 'Orçamento'
    else:
        msg, t, h = MSG_ORC, 'Fale com o laboratório', 'Atendimento'
    return f'''<aside class="aside">
  <div class="abox"><p class="abox__h">{h}</p><h2 class="abox__t">{t}</h2><p class="abox__note">Valores informados sob orçamento, pelo WhatsApp ou pelo telefone.</p>
    <a class="btn" href="{wa(msg)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_aside">{icon("chat")}Solicitar orçamento</a>
    <a class="btn btn--ghost" href="tel:+553132719766" data-track="phone_aside">{icon("phone")}(31) 3271-9766</a></div>
  <div class="abox"><p class="abox__h">O laboratório</p><ul>
    <li>{icon("ruler")}Desde 1975 no Centro de BH</li><li>{icon("bench")}40+ profissionais · 10 salas no Mesbla</li><li>{icon("clock")}7 dias úteis por etapa, em média</li>
    <li>{icon("shield")}Garantia de até 6 meses</li><li>{icon("truck")}Coleta em MG · envio para todo o Brasil</li></ul></div>
</aside>'''

def resumo(items, title='Pontos principais'):
    """Tópicos curtos e visíveis no topo de páginas longas (textos em content/resumos.py)."""
    li = ''.join(f'<li>{t}</li>' for t in items)
    return f'<div class="sum rv"><p class="sum__h">{title}</p><ul>{li}</ul></div>'

def accordion(body, open_titles=(), label='Detalhes'):
    """Recolhe cada seção <h2> em <details class="acc">. O texto inteiro continua no HTML (SEO/IAs);
    só fica fechado. Conteúdo antes do primeiro <h2> continua visível."""
    parts = re.split(r'(?=<h2[ >])', body.strip())
    head = '' if parts[0].startswith('<h2') else parts[0]
    acc = ''
    for x in parts:
        if not x.startswith('<h2'): continue
        attrs, t, rest = re.match(r'<h2([^>]*)>(.*?)</h2>(.*)', x, re.S).groups()
        op = ' open' if strip(t) in open_titles else ''
        acc += f'<details class="acc"{op}><summary><h2{attrs}>{t}</h2></summary><div class="acc__body">{rest.strip()}</div></details>'
    return f'{head}<p class="accs__h">{label}</p><div class="accs">{acc}</div>'

def fig(base, alt, cap, slot=None, tag=None, pref='wgh'):
    """Foto com legenda. O rótulo sai sozinho: "Foto: LDA" (foto real) ou "Imagem ilustrativa"."""
    tag = tag_for(base) if tag is None else tag
    tag_html = f'<span>{tag}</span>' if tag else ''
    r = ratio(base, pref)
    return (f'<figure class="fig{"" if r else " fig--tall"}"><div class="frame rv-img {r}">{img(base, alt, sizes="(max-width:1024px) 92vw, 720px" if r else "(max-width:760px) 92vw, 440px", pref=pref)}</div>'
            f'<figcaption><span>{cap}</span>{tag_html}</figcaption></figure>')

MOSTRAR_ESPACOS_FOTO = False   # auditoria 26/10/2026: o quadro "espaço reservado" aparecia no site público

def photo_slot(key, text, cls=''):
    """Espaço marcado para uma foto real do laboratório (procure por "FOTO REAL" no HTML gerado).
    Com MOSTRAR_ESPACOS_FOTO = False, só o comentário vai para o HTML (nada aparece ao visitante)."""
    if not MOSTRAR_ESPACOS_FOTO:
        return f'<!-- FOTO REAL: {text} (data-foto-real="{key}") -->'
    return (f'<!-- FOTO REAL: {text} -->\n<div class="photo-slot{(" " + cls) if cls else ""}" data-foto-real="{key}"><div>{icon("camera")}{text}<br>'
            f'<span class="photo-slot__hint">Espaço reservado para foto do laboratório</span></div></div>')

STREETS = '''<svg class="streets" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<g fill="none" stroke="#D3CBBE" stroke-width="10"><path d="M-20 210L420 60"/><path d="M60-20l120 340"/><path d="M250-20L330 320"/><path d="M-20 120h440"/></g>
<g fill="none" stroke="#E2DCD2" stroke-width="5"><path d="M-20 40l200 70 240-20"/><path d="M140 320l60-200 220-60"/><path d="M-20 270h440"/><path d="M20-20l40 340"/></g>
<g font-family="IBM Plex Mono, monospace" font-size="8" fill="#7A828D" letter-spacing=".8"><text x="268" y="98" transform="rotate(-18 268 98)">AV. AFONSO PENA</text><text x="24" y="114">R. DA BAHIA</text><text x="196" y="250" transform="rotate(70 196 250)">AV. AMAZONAS</text></g>
</svg>'''

def contact_section(n='§', title='Endereço e contatos', hid='contato-title', cls=''):
    return f'''<section class="sec {cls}" id="contato" aria-labelledby="{hid}">
  <div class="container">
    {shead(n, 'Contato', title, f'Atendemos {HOURS_FRASE}.', hid=hid)}
    <div class="contact">
      <div class="contact__info rv">
        <ul class="clist">
          <li><span>Endereço</span><span>Av. Afonso Pena, 262, 16º andar, sala 1602<br>Ed. Mesbla, Centro, Belo Horizonte/MG<br>CEP 30130-923</span></li>
          <li><span>Atendimento e orçamentos</span><span><a href="tel:+553132719766" data-track="phone">(31) 3271-9766</a> · <a href="tel:+553132719688" data-track="phone">(31) 3271-9688</a></span></li>
          <li><span>WhatsApp</span><span><a href="{wa('Olá! Sou dentista e gostaria de mais informações.')}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_contact">(31) 98652-1387</a></span></li>
          <li><span>Financeiro</span><span><a href="tel:+553132121384" data-track="phone_fin">(31) 3212-1384</a> · <a href="https://wa.me/5531986521201" target="_blank" rel="noopener noreferrer" data-track="whatsapp_fin">WhatsApp (31) 98652-1201</a></span></li>
          <li><span>E-mail</span><span><a href="mailto:dentalaraujo@yahoo.com.br" data-track="email">dentalaraujo@yahoo.com.br</a></span></li>
          <li><span>Instagram</span><span><a href="{IG}" target="_blank" rel="noopener noreferrer">@labdentalaraujo</a></span></li>
          <li><span>Horário</span><span>{HOURS_LONGO}</span></li>
        </ul>
      </div>
      <div class="contact__map rv">
        <div class="map" id="map">{STREETS}
          <div class="map__pin" aria-hidden="true"><b>LDA · Sala 1602</b><i></i></div>
          <div class="map__btns"><button type="button" class="btn btn--sm" id="loadMap">{icon("pin")}Carregar mapa</button><a class="btn btn--sm" href="{MAPS}" target="_blank" rel="noopener noreferrer" data-track="maps">Abrir no Google Maps</a></div>
        </div>
        <p class="cap"><span>Centro de Belo Horizonte</span><span id="mapNote">Esquema sem escala</span></p>
      </div>
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ 7. dados estruturados (JSON-LD)
BIZ_ID = BASE + '/#laboratorio'
# Área atendida (palavras-chave 26/10/2026): BH e Grande BH (coleta), MG (coleta e entrega) e Brasil (envio).
# Contagem e Betim são citadas no texto de /envio-para-todo-brasil/; não criar páginas por cidade (doorway).
AREA = [{"@type": "City", "name": "Belo Horizonte"},
        {"@type": "AdministrativeArea", "name": "Região Metropolitana de Belo Horizonte"},
        {"@type": "City", "name": "Contagem"}, {"@type": "City", "name": "Betim"},
        {"@type": "State", "name": "Minas Gerais"}, {"@type": "Country", "name": "Brasil"}]
def business():
    return {
     "@type": ["LocalBusiness", "MedicalBusiness"], "@id": BIZ_ID, "name": NAME,
     "alternateName": ["LDA", "LDA Laboratório Dental Araújo"], "legalName": LEGAL_NAME,
     "taxID": CNPJ, "foundingDate": LAB["founding_year"],
     "slogan": LAB["slogan"],
     "description": "Laboratório de prótese dentária em Belo Horizonte desde 1975, com mais de 40 profissionais e 10 salas no Edifício Mesbla. Zircônia, E-Max, metalocerâmica, barra de protocolo, PPR, prótese total, prótese flexível, resinas, placas e ortodontia, com coleta e entrega em Minas Gerais e atendimento para todo o Brasil.",
     "url": BASE + '/', "logo": BASE + "/assets/icons/icon-512.png",
     "image": [BASE + "/assets/img/og/og-image.jpg", img_url(HOME_FOTO, 'hwg'), img_url('real/impressoras-3d-laboratorio', 'hg')],
     "telephone": PHONE_1_SCHEMA, "email": EMAIL,
     "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 40},
     "address": {"@type": "PostalAddress", "streetAddress": STREET_SCHEMA,
                 "addressLocality": LAB["address"]["city"], "addressRegion": LAB["address"]["region"],
                 "postalCode": LAB["address"]["postal"], "addressCountry": LAB["address"]["country"]},
     "geo": {"@type": "GeoCoordinates", "latitude": LAB["address"]["geo"]["latitude"],
             "longitude": LAB["address"]["geo"]["longitude"]},
     "hasMap": MAPS,
     "openingHoursSpecification": LAB["hours"]["schema"],
     "areaServed": AREA,
     "contactPoint": [
      {"@type": "ContactPoint", "contactType": "customer service", "name": "Atendimento e orçamentos", "telephone": PHONE_1_SCHEMA, "areaServed": "BR", "availableLanguage": "Portuguese"},
      {"@type": "ContactPoint", "contactType": "customer service", "name": "Atendimento e orçamentos", "telephone": PHONE_2_SCHEMA, "areaServed": "BR", "availableLanguage": "Portuguese"},
      {"@type": "ContactPoint", "contactType": "sales", "name": "WhatsApp – atendimento e orçamentos", "telephone": WA_SCHEMA, "areaServed": "BR", "availableLanguage": "Portuguese"},
      {"@type": "ContactPoint", "contactType": "billing support", "name": "Financeiro", "telephone": FIN_PHONE_SCHEMA, "availableLanguage": "Portuguese"},
      {"@type": "ContactPoint", "contactType": "billing support", "name": "Financeiro (WhatsApp)", "telephone": FIN_WA_SCHEMA, "availableLanguage": "Portuguese"}],
     "sameAs": [IG, FB, MAPS],
     "knowsAbout": ["prótese dentária", "coroa de zircônia", "ponte fixa de zircônia", "E-Max (dissilicato de lítio)", "faceta em cerâmica",
                    "coroa metalocerâmica", "núcleo metálico fundido", "prótese protocolo sobre implante", "barra de protocolo",
                    "overdenture com barra clips", "guia cirúrgico para implante", "prótese parcial removível (PPR) com armação Roach",
                    "prótese total removível", "prótese flexível", "coroa de resina Ceramage", "coroa provisória",
                    "placa de bruxismo", "placa de clareamento", "protetor bucal", "aparelho anti-ronco", "ortodontia e ortopedia funcional"],
    }

def website():
    return {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + '/', "name": NAME, "inLanguage": "pt-BR",
            "publisher": {"@id": BIZ_ID}}

def faq_ld(pairs, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in pairs]}

def crumbs_ld(trail, url):
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(trail)]}

def webpage(p, url, kind='WebPage'):
    d = {"@type": kind, "@id": url + "#webpage", "url": url, "name": p['title'], "description": p['desc'],
         "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BIZ_ID}, "dateModified": modificado(url[len(BASE):])}
    if len(p.get('trail', [])) > 1: d["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if p.get('img'): d["primaryImageOfPage"] = img_obj(p['img'])
    return d


# ------------------------------------------------------------------ 8. páginas
HOME_FOTO = 'real/proteses-totais-gengiva-caracterizada'   # foto do topo da home (LCP)
PAGES = []   # (path, prio)
PAGE_IMG_MAP = {}   # path → {url da foto real: legenda} (sitemap de imagens)
POSTS_RECENTES = sorted(POSTS, key=lambda q: q['date'], reverse=True)   # estável: empate mantém a ordem do arquivo
SLUG_POST = {q['slug']: q for q in POSTS}

def refs_html(q):
    """Seção "Referências" do artigo (fontes dos fatos citados no texto)."""
    if not q.get('refs'): return ''
    li = ''.join(f'<li>{t} <a href="{u}" target="_blank" rel="noopener noreferrer">Acessar a fonte</a>.</li>' for t, u in q['refs'])
    return f'<h2>Referências</h2><ol class="refs">{li}</ol>'

def posts_rel(q, n=2):
    """Artigos em "Leia também": os indicados em related_posts; completa com os mais recentes."""
    rel = [SLUG_POST[x] for x in q.get('related_posts', []) if x in SLUG_POST and x != q['slug']]
    for x in POSTS_RECENTES:
        if len(rel) >= n: break
        if x is not q and x not in rel: rel.append(x)
    return rel[:n]

def out(path, htmltext, prio='0.7'):
    f = DIST / path.lstrip('/') / 'index.html' if path.endswith('/') else DIST / path.lstrip('/')
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(telclass(nobreak(htmltext)), encoding='utf-8')
    if path != '/404.html':
        PAGES.append((path, prio)); PAGE_IMG_MAP[path] = dict(PAGE_IMGS)
    PAGE_IMGS.clear()

def idx_list():
    rows = ''.join(
        f'<li class="idx__row"><a href="/servicos/{s["slug"]}/"><span class="idx__n">{i+1:02d}</span><span class="idx__t">{s["nav"]}</span>'
        f'<span class="idx__d">{s["blurb"]}</span><span class="idx__p"><small>Tipos de peça</small>{sum(len(CAT[c]["items"]) for c in s["cats"]):02d}</span><span class="idx__a" aria-hidden="true">→</span></a>'
        f'<span class="idx__img" aria-hidden="true">{img(s["img"], "", only640=True)}</span></li>'
        for i, s in enumerate(SERVICOS))
    return f'<ol class="idx rv">{rows}</ol>'

# ---------- componentes da home enxuta (v2, 26/10/2026) ----------
def svc_tiles():
    """Cartões curtos de serviço: foto com revelação por máscara, nome e rótulo curto (resumos.TAG)."""
    li = ''.join(
        f'<li><a class="tile" href="/servicos/{s["slug"]}/"><span class="tile__img rv-img">{img(s["img"], "", sizes="(max-width:760px) 46vw, 300px")}</span>'
        f'<span class="tile__n">{i+1:02d}</span><span class="tile__t">{s["nav"]}</span><span class="tile__d">{TAG[s["slug"]]}</span>'
        f'<span class="tile__a" aria-hidden="true">→</span></a></li>'
        for i, s in enumerate(SERVICOS))
    return f'<ul class="tiles">{li}</ul>'

# faixa horizontal de fotos REAIS do laboratório (content/fotos_reais.py: FAIXA_REAL), em loop
FAIXA_H = 230   # altura máxima da foto na faixa (CSS: clamp(150px,18vw,230px))

def faixa():
    def items(dup):
        li = ''
        for k in FAIXA_REAL:
            f = FR_ID[k]; base = 'real/' + f['slug']; n = rvar(base, 'g')
            wpx = round(FAIXA_H * REAL[n]['w'] / REAL[n]['h'])
            li += (f'<li><figure>{img(base, "" if dup else f["alt"], sizes=f"{wpx}px", pref="g")}'
                   f'<figcaption>{e(f["cap"]).replace("E-Max", "<span class=\"nw\">E-Max</span>")}</figcaption></figure></li>')
        return li
    return f'''<section class="strip" aria-labelledby="strip-title">
  <div class="container strip__head">
    <h2 id="strip-title" class="label">Na bancada</h2>
    <span class="strip__note">Fotos de trabalhos do laboratório</span>
    <a class="strip__link" href="/trabalhos/">Ver todos os trabalhos</a>
    <button class="strip__btn" type="button" aria-pressed="false" data-strip-toggle>Pausar</button>
  </div>
  <section class="strip__view" tabindex="0" aria-label="Fotos de trabalhos de prótese do laboratório; role para o lado">
    <div class="strip__rail"><ul class="strip__set">{items(False)}</ul><ul class="strip__set strip__dup" aria-hidden="true">{items(True)}</ul></div>
  </section>
</section>'''

# ---------- antes e depois (componente pronto, DESLIGADO) ----------
# Só entra no site com pares REAIS de fotos do mesmo caso, com autorização (ver docs/FOTOS.md).
# Cada item: (antes, depois, alt_antes, alt_depois, legenda) — bases em assets/img/, como em img().
ANTES_DEPOIS = []

def antes_depois(pares):
    if not pares: return ''
    figs = ''.join(f'''<figure class="ba rv" data-ba>
  <div class="ba__frame">
    <div class="ba__after">{img(d, ad, sizes="(max-width:1024px) 92vw, 720px")}</div>
    <div class="ba__before">{img(a, aa, sizes="(max-width:1024px) 92vw, 720px")}</div>
    <span class="ba__tag ba__tag--a" aria-hidden="true">Antes</span><span class="ba__tag ba__tag--d" aria-hidden="true">Depois</span>
    <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Comparar antes e depois: arraste para os lados">
  </div>
  <figcaption class="cap"><span>{cap}</span><span>Caso real · com autorização</span></figcaption>
</figure>''' for a, d, aa, ad, cap in pares)
    return f'''<section class="sec sec--white" aria-labelledby="ba-title">
  <div class="container">
    {shead('§', 'Casos', 'Antes e depois', hid='ba-title')}
    <div class="bas">{figs}</div>
  </div>
</section>'''

def build_home():
    steps = [('01', 'chat', 'Contato', 'WhatsApp ou telefone: conte o caso e receba o orçamento.'),
             ('02', 'truck', 'Coleta ou envio', 'Coleta em MG. De outros estados, Correios ou transportadora.'),
             ('03', 'bench', 'Bancada', '7 dias úteis por etapa. Urgência: +30% por etapa.'),
             ('04', 'box', 'Retorno', 'Prova ou instalação, com garantia de até 6 meses.')]
    tl = ''.join(f'<li class="rv"><span class="tl__d">Etapa {d}</span>{icon(ic)}<h3>{t}</h3><p>{p}</p></li>' for d, ic, t, p in steps)
    short = [FAQ_GROUPS[0][1][0], FAQ_GROUPS[0][1][1], FAQ_GROUPS[2][1][0], FAQ_GROUPS[2][1][1], FAQ_GROUPS[3][1][0]]
    posts = ''
    for q in POSTS_RECENTES[:3]:   # home: só os 3 mais recentes (o blog lista todos)
        d = q['date'].split('-'); words = len(strip(q['body']).split())
        posts += (f'<a class="post rv" href="/blog/{q["slug"]}/"><div class="post__img">{img(q["img"], q["img_alt"], sizes="(max-width:760px) 92vw, 400px")}</div>'
                  f'<span class="label label--plain">{d[2]}/{d[1]}/{d[0]} · {max(1, round(words / 200))} min</span><h3>{q["h1"]}</h3></a>')
    hero_alt = FR_SLUG[HOME_FOTO[5:]]['alt']
    main = f'''<section class="hero" aria-labelledby="h1">
  <div class="container hero__grid">
    <div class="hero__text">
      <span class="label intro">Laboratório de prótese dentária · Centro de BH</span>
      <h1 id="h1" class="intro">Laboratório de prótese dentária em BH, <em>desde 1975</em></h1>
      <p class="hero__lead intro-2">Zircônia, E-Max, protocolo, PPR e prótese total para dentistas de Belo Horizonte, da Grande BH e de todo o Brasil.</p>
      <div class="btns intro-2"><a class="btn btn--go" href="{wa(MSG_ORC)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_hero">{icon("chat")}Solicitar orçamento</a><a class="arrow" href="#processo">Como enviar um caso</a></div>
      <div class="specs intro-3">
        <div><b><span class="cnt n2" data-count="50">50</span> anos</b><span>Desde 1975</span></div>
        <div><b><span class="cnt n2" data-count="40">40</span>+</b><span>Profissionais</span></div>
        <div><b><span class="cnt n2" data-count="10">10</span> salas</b><span>Ed. Mesbla · BH</span></div>
        <div><b>Brasil</b><span>Coleta em MG, envio de todo o país</span></div>
      </div>
    </div>
    <figure class="hero__media intro-3">
      <span class="ruler" aria-hidden="true"></span>
      <div class="frame curtain">{img(HOME_FOTO, hero_alt, lazy=False, prio=True, sizes=HERO_SIZES, pref="hwg")}</div>
      <figcaption class="cap"><span>Fig. 01 · {e(FR_SLUG[HOME_FOTO[5:]]["cap"])}</span><span>Foto: LDA</span></figcaption>
    </figure>
  </div>
</section>
{faixa()}

<section class="sec" id="servicos" aria-labelledby="servicos-title">
  <div class="container">
    {shead('01', 'Serviços', 'O que sai da nossa bancada', 'Oito linhas de trabalho, todas sob orçamento.', 'servicos-title', ('/servicos/', 'Todos os serviços'))}
    {svc_tiles()}
  </div>
</section>

<section class="sec sec--navy" id="processo" aria-labelledby="processo-title">
  <div class="container">
    {shead('02', 'Processo', 'Como enviar um caso', 'Sem cadastro nem portal. Quatro etapas, do consultório à bancada e de volta.', 'processo-title', ('/envio-para-todo-brasil/', 'Envio de outro estado'))}
    <div class="tlw" data-tl><span class="tl__bar" aria-hidden="true"><i></i></span><ol class="tl">{tl}</ol></div>
    <p class="tl__cta rv"><a class="btn btn--light btn--go" href="{wa(MSG_ORC)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_processo">{icon("chat")}Solicitar orçamento</a></p>
  </div>
</section>

<section class="sec" aria-labelledby="lab-title">
  <div class="container">
    {shead('03', 'O laboratório', 'Cinquenta anos no mesmo endereço do Centro', hid='lab-title')}
    <div class="story">
      <p class="story__q rv">Atendemos dentistas, não pacientes. Requisição por escrito e <em>conversa direta com a bancada</em>.</p>
      <div class="story__body rv"><p class="btns"><a class="arrow" href="/sobre/">Nossa história</a><a class="arrow" href="/perguntas-frequentes/">Perguntas frequentes</a></p></div>
      <div class="plaque rv"><div class="plaque__a"><b>50</b><span>anos de laboratório em 2026</span></div>
        <div class="plaque__b"><span>Edifício Mesbla</span><span>Av. Afonso Pena, 262</span><span>16º andar · Sala 1602</span><i>CNPJ 19.223.635/0001-86</i></div></div>
      <figure class="story__fig"><div class="frame rv-img r32">{img("real/modelos-troquelizados-trabalhos-posteriores", FR_ID["0043"]["alt"], sizes="(max-width:1024px) 92vw, 400px", pref="w")}</div>
        <figcaption class="cap"><span>{e(FR_ID["0043"]["cap"])}</span><span>Foto: LDA</span></figcaption></figure>
      <!-- FOTO REAL: espaço para foto da equipe na bancada (paisagem 3:2) -->
    </div>
  </div>
</section>
{antes_depois(ANTES_DEPOIS)}
{faq_section(short, n='04', link=('/perguntas-frequentes/', 'Todas as perguntas'))}

<section class="sec sec--stone" aria-labelledby="blog-title">
  <div class="container">
    {shead('05', 'Leitura', 'Artigos para dentistas', hid='blog-title', link=('/blog/', 'Ver o blog'))}
    <div class="posts">{posts}</div>
  </div>
</section>

{contact_section('06')}
{cta_band()}'''
    p = dict(path='/', title='Laboratório de Prótese Dentária em BH | Dental Araújo',
             og_title='Laboratório Dental Araújo | Prótese dentária em BH desde 1975',
             desc='Laboratório de prótese dentária em Belo Horizonte desde 1975: zircônia, E-Max, protocolo, PPR e prótese total para dentistas de BH, MG e todo o Brasil.',
             preload=HOME_FOTO, preload_pref='hwg', preload_media='(min-width:1025px)', trail=[('Início', '/')], img=HOME_FOTO)
    out('/', page(p, main, [webpage(p, BASE + '/')]), '1.0')

def build_hub():
    path = '/servicos/'; url = BASE + path
    trail = [('Início', '/'), ('Serviços', path)]
    p = dict(path=path, title='Serviços de Laboratório de Prótese Dentária | LDA',
             desc='Tipos de prótese dentária feitos pelo Laboratório Dental Araújo em BH: protocolo sobre implante, zircônia, E-Max, metalocerâmica, PPR, prótese total e placas.',
             trail=trail)
    body = f'''{phero(trail, "Serviços", 'Serviços de laboratório de prótese dentária <span class="hl">em BH</span>',
      'Da coroa unitária à reabilitação completa sobre implantes. Abaixo estão as oito linhas de trabalho do laboratório, todas sob orçamento.')}
<section class="sec" aria-labelledby="lista-title">
  <div class="container">
    {shead('01', 'Índice', 'Escolha o tipo de prótese', 'Cada página traz indicações, o que enviar, prazos e garantia.', 'lista-title')}
    {idx_list()}
  </div>
</section>
<section class="sec sec--white" aria-labelledby="como-title">
  <div class="container page page--full">
    <div class="prose prose--s2 rv">
      <h2 id="como-title">Que tipos de prótese o laboratório faz?</h2>
      <p>O <strong>Laboratório Dental Araújo</strong> atende cirurgiões-dentistas e clínicas desde 1975 e confecciona <strong>todos os tipos de prótese dentária</strong>: fixas em cerâmica pura (zircônia e E-Max) e metalocerâmica, restaurações metálicas, resinas e provisórios, próteses sobre implante (barra de protocolo, barra clips, guia cirúrgico), removíveis (PPR Roach, parciais em acrílico e Flexite, prótese total), placas oclusais e aparelhos ortodônticos e ortopédicos.</p>
      <h2>Como escolher o serviço certo para o caso</h2>
      <p>Cada página de serviço traz indicações gerais, o que enviar ao laboratório, prazos e garantia. Para comparar materiais, o blog tem guias sobre <a href="/blog/zirconia-ou-e-max-qual-indicar/">zircônia ou E-Max</a>, <a href="/blog/metaloceramica-ou-zirconia/">metalocerâmica ou zircônia</a> e <a href="/blog/ppr-ou-protese-flexivel/">PPR ou prótese flexível</a>. Se o caso não se encaixa em nenhuma das opções, descreva o trabalho pelo WhatsApp: o atendimento confirma se ele é feito e passa o orçamento.</p>
      <h2>Prazo, garantia e logística</h2>
      <p>{PRAZO} {GARANTIA} Fazemos coleta e entrega em Minas Gerais e recebemos trabalhos de todo o Brasil (<a href="/envio-para-todo-brasil/">veja como enviar</a>).</p>
    </div>
  </div>
</section>
{cta_band()}'''
    il = {"@type": "ItemList", "@id": url + "#lista", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": BASE + f'/servicos/{s["slug"]}/', "name": s['nav']} for i, s in enumerate(SERVICOS)]}
    out(path, page(p, body, [webpage(p, url, 'CollectionPage'), crumbs_ld(trail, url), il]), '0.9')

def build_service(s):
    path = f'/servicos/{s["slug"]}/'; url = BASE + path
    trail = [('Início', '/'), ('Serviços', '/servicos/'), (s['nav'], path)]
    p = dict(path=path, title=s['title'], desc=s['desc'], trail=trail, img=s['img'], preload=s['img'], preload_mobile='wgh')
    if is_real(s['img']): p.update(og=f'og-{s["slug"]}', og_alt=s['img_alt'])
    body_html = (resumo(RESUMO[s['slug']]) + fig(s['fig'], s['fig_alt'], s['fig_cap'])
                 + accordion(fill(s['body']) + porque(s), label=f'Tudo sobre {lc(s["nav"])}'))
    cats = s['cats']
    grid = ''.join(pcard(CAT[c], i) for i, c in enumerate(cats))
    msg = f'Olá! Sou dentista e gostaria de um orçamento de {s["nav"]}.'
    itens = f'''<section class="sec sec--stone" id="itens" aria-labelledby="itens-title">
  <div class="container">
    {shead('02', 'Itens', f'O que fazemos em {lc(s["nav"])}', 'Trabalhos desta linha. O valor de cada caso é informado sob orçamento, pelo WhatsApp ou pelo telefone.', 'itens-title')}
    <div class="pgrid{" is-single" if len(cats) == 1 else ""}">{grid}</div>
    <div class="pfoot rv"><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_orcamento">{icon("chat")}Solicitar orçamento no WhatsApp</a><a class="btn btn--ghost" href="/contato/">Outros canais de contato</a></div>
  </div>
</section>'''
    meta = (f'<div class="meta"><span>{icon("clock")}7 dias úteis por etapa</span><span>{icon("shield")}Garantia de até 6 meses</span>'
            f'<span>{icon("truck")}Envio para todo o Brasil</span></div>')
    main = f'''{phero(trail, s["kicker"], s["h1"], s["lead"], s["img"], s["img_alt"], cta=msg, meta=meta)}
<section class="sec" aria-label="Sobre o serviço">
  <div class="container page">
    <article class="prose">{body_html}</article>
    {aside_card(s)}
  </div>
</section>
{itens}
{faq_section(s["faq"], f"Dúvidas sobre {lc(s['nav'])}", n='03')}
{related(s["related"], n='04')}
{cta_band()}'''
    svc = {"@type": "Service", "@id": url + "#servico", "name": s['nav'], "serviceType": s['service_type'], "url": url,
           "description": s['desc'], "provider": {"@id": BIZ_ID}, "image": img_obj(s['img']),
           "areaServed": AREA,
           "audience": {"@type": "Audience", "audienceType": "Cirurgiões-dentistas e clínicas odontológicas"}}
    out(path, page(p, main, [webpage(p, url), crumbs_ld(trail, url), svc, faq_ld(s['faq'], url)]), '0.9')

def build_simple(path, title, desc, kicker, h1, lead, body, kind='WebPage', extra_ld=(), facts=False, aside=True, after='', prio='0.7', name=None, img_schema=None,
                 summary=None, top='', open_titles=()):
    """summary: tópicos visíveis + seções <h2> recolhidas em acordeões (top = figura visível acima deles)."""
    if summary: body = resumo(summary) + top + accordion(body, open_titles)
    url = BASE + path
    trail = [('Início', '/'), (name or kicker, path)]
    p = dict(path=path, title=title, desc=desc, trail=trail, img=img_schema)
    inner = f'<div class="container page"><article class="prose">{body}</article>{aside_card() if aside else ""}</div>'
    main = f'''{phero(trail, kicker, h1, lead)}
<section class="sec">{inner}</section>
{facts_block(n='02', cls='sec--white') if facts else ''}{after}
{cta_band()}'''
    graph = [webpage(p, url, kind), crumbs_ld(trail, url)] + list(extra_ld)
    out(path, page(p, main, graph), prio)


def build_sobre():
    body = '''
<h2>Quem somos</h2>
<p>Pedro Paulo e Edison, filhos de profissional de Odontologia e guiados pelo pai, deram início ao aprendizado da nobre arte de cuidar dos dentes de “gregos” e “troianos”.</p>
<p>Nascidos em Barbacena, os dois irmãos logo demonstraram aptidão pelo trabalho.</p>
<p>Com dezenove anos de idade, Edison começou o curso de aperfeiçoamento em prótese no Rio de Janeiro, trabalhou em um grande laboratório em Belo Horizonte e, depois de algum tempo, já seguro de seus conhecimentos, começou a colocar em prática o sonho de montar o próprio laboratório.</p>
<p>Pedro Paulo trabalhava no setor bancário à época, mas aproveitava o tempo de que dispunha à noite para se dedicar ao laboratório.</p>
<p>Desde <strong>8 de setembro de 1975</strong>, o laboratório já se encontrava com suas máquinas funcionando.</p>
<p>Juntos, os dois irmãos — com a boa qualidade apresentada e os compromissos de entrega cumpridos — fizeram com que o crescimento a cada dia desse ao <strong>Laboratório Dental Araújo</strong> o prestígio desejado.</p>
<p>Cinco anos após a inauguração, a empresa já empregava vinte profissionais.</p>
<p>Hoje, 50 anos depois, o respeito aos clientes, a excepcional qualidade do trabalho, o profissionalismo e a dedicação — sede própria no Edifício Mesbla com 10 salas, modernas instalações, maquinário de última geração, mais de 40 empregados qualificados e atendimento em todo o Brasil — continuam nos credenciando a assinar nosso compromisso com os dentistas.</p>
<p><strong>Edison Araújo</strong> e <strong>Pedro Paulo Araújo</strong>.</p>
{FIG}
<h2>O que fazemos</h2>
<p>Trabalhamos em todas as áreas da prótese dentária: <a href="/servicos/zirconia-e-max/">zircônia e E-Max</a>, <a href="/servicos/metaloceramica/">metalocerâmica e RMF</a>, <a href="/servicos/resinas-e-provisorios/">resinas e provisórios</a>, <a href="/servicos/protese-sobre-implante/">prótese sobre implante e protocolo</a>, <a href="/servicos/protese-parcial-removivel-ppr/">PPR</a>, <a href="/servicos/protese-flexivel-flexite/">prótese flexível</a>, <a href="/servicos/protese-total/">prótese total</a> e <a href="/servicos/placas-de-bruxismo-e-ortodontia/">placas e ortodontia</a>.</p>
<h2>Como trabalhamos com o dentista</h2>
<p>Nosso cliente é o cirurgião-dentista. O atendimento é direto, por telefone e WhatsApp, para alinhar material, cor, prazo e detalhes técnicos antes de começar. Fazemos <strong>coleta e entrega em Minas Gerais</strong> e mantemos uma rede de parceiros para ampliar o atendimento. Informações extras sobre o caso devem ir por escrito junto com a requisição, para que nada se perca entre o consultório e a bancada.</p>
{SLOT}
<h2>Orçamento</h2>
<p>Todos os serviços são feitos sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelos telefones (31) 3271-9766 e (31) 3271-9688. Dentes, metais e componentes, quando o trabalho leva, são orçados à parte. Veja <a href="/contato/#orcamento">como pedir um orçamento</a>.</p>
<h2>Condições de trabalho</h2>
<ul>
<li>Prazo médio de 7 dias úteis por etapa. Com urgência, há acréscimo de 30% em cada etapa.</li>
<li>Garantia de até 6 meses para defeito comprovado na confecção (serviços 100% realizados no laboratório).</li>
<li>Pagamento até o dia 10 de cada mês.</li>
<li>Atendimento de segunda a sexta, das 08:00 às 18:00.</li>
</ul>
<p>Dados da empresa: Laboratório Dental Araújo Ltda, CNPJ 19.223.635/0001-86.</p>'''
    body = body.replace('{FIG}', '')
    top = fig('real/impressoras-3d-laboratorio', FR_ID['d207']['alt'], FR_ID['d207']['cap'] + ' · <a href="/trabalhos/">ver trabalhos</a>', pref='hg')
    body = body.replace('{SLOT}', photo_slot('fachada-recepcao', 'Foto real: recepção ou fachada do Ed. Mesbla', 'photo-slot--wide'))
    build_simple('/sobre/', 'Sobre o Laboratório Dental Araújo | Desde 1975 em BH',
      'Laboratório Dental Araújo: fundado em 1975 por Edison e Pedro Paulo Araújo, sede no Ed. Mesbla, mais de 40 profissionais e atendimento em todo o Brasil.',
      'Sobre · Desde 1975', 'Laboratório de prótese em BH <span class="hl">desde 1975</span>',
      'História dos fundadores, 50 anos de prótese dentária em Belo Horizonte e compromisso com o cirurgião-dentista.',
      body, kind='AboutPage', facts=True, name='Sobre', img_schema='real/impressoras-3d-laboratorio',
      summary=RESUMO_SOBRE, top=top, open_titles=('Quem somos',))

def build_envio():
    body = '''
<h2>Laboratório de prótese que atende todo o Brasil</h2>
<p>O <strong>Laboratório Dental Araújo</strong> fica em Belo Horizonte, mas atende cirurgiões-dentistas e clínicas de <strong>todo o Brasil</strong>. Em <strong>Minas Gerais</strong>, incluindo a capital e a Grande BH (Contagem, Betim e demais cidades da região metropolitana), fazemos coleta e entrega dos trabalhos. Para outros estados, o caso pode ser enviado pelos Correios ou por transportadora, e devolvemos o trabalho pronto no endereço do consultório.</p>
<h2>Como funciona, passo a passo</h2>
<ol class="steps">
<li><span><strong>Contato:</strong> fale com o atendimento pelo WhatsApp (31) 98652-1387 ou pelos telefones (31) 3271-9766 e (31) 3271-9688. Informe o tipo de trabalho e a cidade.</span></li>
<li><span><strong>Coleta ou envio:</strong> em MG, combinamos a coleta. Nos demais estados, você envia a caixa para o endereço do laboratório.</span></li>
<li><span><strong>Confecção:</strong> a equipe confere o material recebido e inicia o trabalho. O prazo médio é de 7 dias úteis por etapa.</span></li>
<li><span><strong>Retorno:</strong> o trabalho volta ao consultório para prova ou instalação, no prazo combinado.</span></li>
</ol>
{FIG}
<h2>O que enviar junto com o caso</h2>
<ul>
<li>Requisição completa: material, elementos, cor, etapa e observações por escrito.</li>
<li>Moldagem ou modelo sem defeitos, antagonista e registro de mordida.</li>
<li>Componentes de implante, quando houver, com a indicação do sistema.</li>
<li>Fotos com escala de cor, em trabalhos estéticos.</li>
</ul>
<p>Veja o checklist completo no artigo <a href="/blog/como-enviar-um-caso-para-o-laboratorio-de-protese/">como enviar um caso para o laboratório de prótese</a> e use o <a href="/blog/requisicao-para-laboratorio-de-protese/">modelo de requisição em PDF</a>.</p>
<h2>Como embalar</h2>
<p>Use uma caixa rígida, com cada moldagem em um saco fechado e identificado e com espaços preenchidos para que nada se mova. A requisição deve ir em um envelope dentro da caixa. Desinfete as moldagens conforme o protocolo do material antes de embalar.</p>
<h2>Endereço para envio</h2>
<p><strong>Laboratório Dental Araújo</strong><br>Av. Afonso Pena, 262, 16º andar, Sala 1602, Edifício Mesbla<br>Centro, Belo Horizonte – MG, CEP 30130-923</p>
<p class="note">Antes de enviar, confirme pelo WhatsApp para alinhar prazo, forma de retorno e eventuais custos de frete.</p>
<h2>Prazos, urgência e garantia</h2>
<p>{PRAZO} {GARANTIA} O tempo de transporte entre a sua cidade e Belo Horizonte deve ser somado ao prazo de laboratório.</p>
<h2>Orçamento para outros estados</h2>
<p>O orçamento é feito pelo WhatsApp ou pelo telefone, como para os consultórios de Belo Horizonte. Na mesma conversa, combine a forma de envio, o retorno do trabalho e os eventuais custos de frete.</p>'''
    body = body.replace('{FIG}', '')
    top = fig('foto/moldagem-alginato', 'Moldagem em alginato sobre moldeira, pronta para envio', 'Moldagem conferida antes de embalar')
    faq = FAQ_GROUPS[2][1][:2]
    build_simple('/envio-para-todo-brasil/', 'Laboratório de Prótese para Todo o Brasil | LDA',
      'Envie seu caso ao Laboratório Dental Araújo de qualquer estado: coleta e entrega em MG, envio pelos Correios ou transportadora e retorno ao consultório.',
      'Envio para todo o Brasil', 'Laboratório de prótese que atende <span class="hl">todo o Brasil</span>',
      'Coleta e entrega em Minas Gerais e envio de casos de qualquer estado para o laboratório no Centro de Belo Horizonte.',
      fill(body), extra_ld=[faq_ld(faq, BASE + '/envio-para-todo-brasil/')],
      after=faq_section(faq, 'Dúvidas sobre envio', n='02', cls='sec--stone'), prio='0.8', name='Envio para todo o Brasil', img_schema='foto/moldagem-alginato',
      summary=RESUMO_ENVIO, top=top, open_titles=('Como funciona, passo a passo', 'Endereço para envio'))

def build_faq():
    path = '/perguntas-frequentes/'; url = BASE + path
    trail = [('Início', '/'), ('Perguntas frequentes', path)]
    p = dict(path=path, title='Perguntas Frequentes | Laboratório Dental Araújo',
             desc='Prazos, urgência, garantia, envio, orçamento e pagamento: respostas diretas às dúvidas mais comuns de dentistas sobre o Laboratório Dental Araújo em BH.',
             trail=trail)
    allq = []; groups = ''
    for gi, (g, pairs) in enumerate(FAQ_GROUPS):
        allq += pairs
        groups += f'<div class="faq-group">{faq_block(pairs, g, f"g{gi}", f"{gi+1:02d}", label="Tema")}</div>'
    main = phero(trail, f'FAQ · {sum(len(x) for _, x in FAQ_GROUPS)} respostas', 'Perguntas frequentes sobre o <span class="hl">laboratório</span>',
                 'Respostas diretas sobre prazos, urgência, garantia, envio, orçamento e pagamento, com base nas condições oficiais do laboratório.') + \
           f'<section class="sec" aria-label="Perguntas por tema"><div class="container">{groups}</div></section>' + cta_band('Ficou <em>alguma dúvida?</em>')
    page_ld = webpage(p, url); page_ld['@type'] = 'FAQPage'
    page_ld['mainEntity'] = faq_ld(allq, url)['mainEntity']
    out(path, page(p, main, [page_ld, crumbs_ld(trail, url)]), '0.7')

ORCAMENTO = f'''<section class="sec" id="orcamento" aria-labelledby="orcamento-title"><div class="container">
{shead('03', 'Orçamento', 'Como pedir um orçamento', 'Os valores são informados sob orçamento, pelo WhatsApp ou pelo telefone. Quanto mais completa a descrição, mais rápida a resposta.', 'orcamento-title')}
<div class="ledger-wrap">
  <div class="ledger rv"><div class="ledger__head"><span>O que informar</span><span>WhatsApp ou telefone</span></div><ol class="cond">
    <li><span>Tipo de trabalho e material (por exemplo, coroa em zircônia ou PPR Roach).</span></li>
    <li><span>Elementos envolvidos e a etapa em que o caso está.</span></li>
    <li><span>Cidade do consultório, para combinar coleta em MG ou envio de outro estado.</span></li>
    <li><span>Se precisa de urgência (acréscimo de 30% em cada etapa).</span></li>
  </ol></div>
  <aside class="rv"><div class="btns btns--stack"><a class="btn" href="{wa(MSG_ORC)}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_orcamento">{icon("chat")}Solicitar orçamento</a><a class="btn btn--ghost" href="tel:+553132719766" data-track="phone_orcamento">{icon("phone")}(31) 3271-9766</a></div>
    <p class="ledger-note">Dentes, soldas, componentes protéticos, ligas metálicas, vazamento, troquéis e gengivas artificiais são orçados à parte.</p></aside>
</div></div></section>'''

def build_contato():
    path = '/contato/'; url = BASE + path
    trail = [('Início', '/'), ('Contato', path)]
    p = dict(path=path, title='Contato | Laboratório Dental Araújo – BH',
             desc='Telefones, WhatsApp, e-mail, endereço, horário e como pedir um orçamento ao Laboratório Dental Araújo, Av. Afonso Pena, 262, Centro de BH.',
             trail=trail)
    cards = f'''<section class="sec sec--stone" aria-labelledby="canais-title"><div class="container">
{shead('02', 'Canais', 'Com quem falar', hid='canais-title')}
<div class="ccards rv">
<div><h3>Atendimento e orçamentos</h3><p>Telefones fixos.</p><p><a href="tel:+553132719766" data-track="phone">(31) 3271-9766</a><br><a href="tel:+553132719688" data-track="phone">(31) 3271-9688</a></p></div>
<div><h3>WhatsApp</h3><p>Orçamentos, pedidos e envio de casos.</p><p><a href="{wa('Olá! Sou dentista e gostaria de mais informações.')}" target="_blank" rel="noopener noreferrer" data-track="whatsapp_contact">(31) 98652-1387</a></p></div>
<div><h3>Financeiro</h3><p>Pagamentos até o dia 10 de cada mês.</p><p><a href="tel:+553132121384" data-track="phone_fin">(31) 3212-1384</a><br><a href="https://wa.me/5531986521201" target="_blank" rel="noopener noreferrer" data-track="whatsapp_fin">WhatsApp (31) 98652-1201</a></p></div>
<div><h3>E-mail e redes</h3><p><a href="mailto:dentalaraujo@yahoo.com.br" data-track="email">dentalaraujo@yahoo.com.br</a><br><a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram @labdentalaraujo</a><br><a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook</a></p></div>
</div></div></section>'''
    main = phero(trail, 'Contato', 'Contato do Laboratório Dental Araújo <span class="hl">em BH</span>',
                 f'Av. Afonso Pena, 262, 16º andar, sala 1602, Edifício Mesbla, Centro, Belo Horizonte/MG. Atendimento {HOURS_FRASE}.') + \
           contact_section('01', 'Endereço, telefones e mapa') + cards + ORCAMENTO
    out(path, page(p, main, [webpage(p, url, 'ContactPage'), crumbs_ld(trail, url)]), '0.8')

def build_blog():
    path = '/blog/'; url = BASE + path
    trail = [('Início', '/'), ('Blog', path)]
    p = dict(path=path, title='Blog para Dentistas: Prótese Dentária | Dental Araújo',
             desc='Artigos para cirurgiões-dentistas sobre prótese dentária: escolha de material, PPR ou flexível, etapas do protocolo e modelo de requisição em PDF.',
             trail=trail)
    main = phero(trail, 'Blog', 'Blog de prótese dentária para <span class="hl">dentistas</span>',
                 'Textos práticos da equipe do Laboratório Dental Araújo sobre escolha de material, envio de casos e etapas de trabalho, com as fontes citadas.', cta=False) + \
           f'<section class="sec" aria-labelledby="art-title"><div class="container">{shead("01", "Artigos", "Artigos recentes", hid="art-title")}<div class="cards">{"".join(post_card(q) for q in POSTS_RECENTES)}</div></div></section>' + cta_band()
    blog_ld = {"@type": "Blog", "@id": url + "#blog", "name": "Blog do Laboratório Dental Araújo", "url": url, "publisher": {"@id": BIZ_ID},
               "blogPost": [{"@id": BASE + f"/blog/{q['slug']}/#artigo"} for q in POSTS_RECENTES]}
    out(path, page(p, main, [webpage(p, url, 'CollectionPage'), crumbs_ld(trail, url), blog_ld]), '0.6')
    for q in POSTS:
        pth = f"/blog/{q['slug']}/"; u = BASE + pth
        tr = [('Início', '/'), ('Blog', '/blog/'), (q['h1'], pth)]
        pp = dict(path=pth, title=q['title'], desc=q['desc'], trail=tr, img=q['img'], preload=q['img'], og_type='article', date=q['date'])
        if is_real(q['img']): pp.update(og=f"og-{q['slug']}", og_alt=q['img_alt'])
        d = q['date'].split('-'); dbr = f'{d[2]}/{d[1]}/{d[0]}'
        words = len(strip(q['body']).split())
        meta = (f'<div class="meta"><span>Equipe {NAME}</span><span><time datetime="{q["date"]}">{dbr}</time></span>'
                f'<span>{max(1, round(words / 200))} min de leitura</span></div>')
        rel = posts_rel(q)
        rs = SVC[q['related_service']] if q['related_service'] else SVC['protese-sobre-implante']
        after = f'''<section class="sec sec--stone" aria-labelledby="mais-title"><div class="container">
{shead('02', 'Continue lendo', 'Leia também', hid='mais-title')}
<div class="cards">{"".join(post_card(x) for x in rel)}{svc_card(rs)}</div></div></section>'''
        main = f'''{phero(tr, "Blog · Artigo", q["h1"], q["lead"], q["img"], q["img_alt"], cta=False, meta=meta)}
<section class="sec"><div class="container page"><article class="prose">{q["body"]}{refs_html(q)}</article>{aside_card(SVC[q["related_service"]] if q["related_service"] else None)}</div></section>
{after}
{cta_band()}'''
        art = {"@type": "Article", "@id": u + "#artigo", "headline": q['h1'], "description": q['desc'], "inLanguage": "pt-BR",
               "image": img_obj(q['img']), "datePublished": q['date'], "dateModified": TODAY,
               "author": {"@type": "Organization", "name": NAME, "url": BASE + '/'}, "publisher": {"@id": BIZ_ID},
               "mainEntityOfPage": {"@id": u + "#webpage"}, "wordCount": words, "keywords": ', '.join([q['primary']] + q['secondary']),
               "audience": {"@type": "Audience", "audienceType": "Cirurgiões-dentistas"}}
        if q.get('refs'):
            art["citation"] = [{"@type": "CreativeWork", "name": strip(t), "url": u2} for t, u2 in q['refs']]
        out(pth, page(pp, main, [webpage(pp, u), crumbs_ld(tr, u), art]), '0.6')


def build_trabalhos():
    """Galeria de fotos REAIS por categoria (pastas do Drive do LDA), com ampliação acessível (<dialog>, main.js)."""
    path = '/trabalhos/'; url = BASE + path
    trail = [('Início', '/'), ('Trabalhos', path)]
    p = dict(path=path, title='Trabalhos do Laboratório: Fotos de Próteses | LDA',
             desc='Fotos reais de próteses feitas no Laboratório Dental Araújo, em BH: prótese total, protocolo, barra clip, E-Max, metalocerâmica, PPR e Flexite.',
             trail=trail, og='og-trabalhos', og_alt='Fotos de trabalhos do Laboratório Dental Araújo')
    por_cat = {c: [f for f in FOTOS_REAIS if f['cat'] == c] for c, _ in FR_CATS}
    chips = ''.join(f'<li><a href="#{c}">{n} <span>{len(por_cat[c])}</span></a></li>' for c, n in FR_CATS if por_cat[c])
    secs = ''
    for c, nome in FR_CATS:
        fs = por_cat[c]
        if not fs: continue
        li = ''
        for f in fs:
            base = 'real/' + f['slug']; n = rvar(base, 'g')
            big = f"/assets/img/real/{n}-{REAL[n]['w']}"
            li += (f'<li><a class="gal__a" href="{big}.jpg" data-lb="{big}.webp" data-cap="{e(f["cap"])}">'
                   f'{img(base, f["alt"], sizes="(max-width:760px) 46vw, (max-width:1180px) 31vw, 370px", pref="g")}'
                   f'<span class="sr-only"> (ampliar foto)</span></a><p class="gal__cap">{e(f["cap"])}</p></li>')
        secs += (f'<section class="gal__sec" id="{c}" aria-labelledby="{c}-t"><h2 id="{c}-t" class="gal__h">{nome} '
                 f'<span>{len(fs):02d} {"foto" if len(fs) == 1 else "fotos"}</span></h2><ul class="gal">{li}</ul></section>')
    lead = f'{len(FOTOS_REAIS)} fotos de peças feitas no Laboratório Dental Araújo, organizadas por tipo de trabalho. Toque numa foto para ampliar.'
    hero = phero(trail, 'Trabalhos', 'Trabalhos do laboratório de prótese <span class="hl">em BH</span>', lead)
    main = f'''{hero}
<section class="sec" aria-label="Galeria de trabalhos">
  <div class="container">
    <nav class="galnav" aria-label="Categorias da galeria"><ul>{chips}</ul></nav>
    {secs}
    <p class="gal__note">Fotos do próprio laboratório, sem retoque de cor. Os casos aparecem sem dados de pacientes; números escritos nos modelos são códigos internos de trabalho.</p>
  </div>
</section>
<dialog class="lb" aria-label="Foto ampliada" data-lb-dialog>
  <figure class="lb__fig"><img class="lb__img" src="data:," alt=""><figcaption class="lb__cap"><span data-lb-text></span><span data-lb-n></span></figcaption></figure>
  <button class="lb__btn lb__prev" type="button" data-lb-prev aria-label="Foto anterior">←</button>
  <button class="lb__btn lb__next" type="button" data-lb-next aria-label="Próxima foto">→</button>
  <button class="lb__btn lb__close" type="button" data-lb-close aria-label="Fechar">×</button>
</dialog>
{cta_band()}'''
    wp = webpage(p, url, 'CollectionPage')
    gal_ld = {"@type": "ImageGallery", "@id": url + "#galeria", "name": "Trabalhos do Laboratório Dental Araújo", "url": url,
              "isPartOf": {"@id": url + "#webpage"}, "about": {"@id": BIZ_ID},
              "associatedMedia": [img_obj('real/' + f['slug'], 'g') for f in FOTOS_REAIS]}
    out(path, page(p, main, [wp, crumbs_ld(trail, url), gal_ld]), '0.6')

def build_404():
    p = dict(path='/404.html', title='Página não encontrada | Laboratório Dental Araújo', desc='A página que você procura não existe ou mudou de endereço.', noindex=True)
    links = ''.join(f'<a class="btn btn--ghost btn--sm" href="{u}">{t}</a>' for u, t in [('/servicos/', 'Serviços'), ('/perguntas-frequentes/', 'Perguntas frequentes'), ('/contato/', 'Contato')])
    main = f'''<section class="e404"><div class="container"><b aria-hidden="true">404</b>
<h1>Página não encontrada</h1>
<p>O endereço pode ter mudado. Volte para a página inicial ou abra uma das seções abaixo.</p>
<div class="btns"><a class="btn" href="/">Ir para o início</a>{links}</div></div></section>'''
    out('/404.html', page(p, main, []))


# ------------------------------------------------------------------ 9. arquivos técnicos e main()
def build_meta():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, prio in PAGES:
        ims = ''.join(f'<image:image><image:loc>{e(u)}</image:loc></image:image>' for u in PAGE_IMG_MAP.get(path, {}))   # só fotos reais do LDA
        sm.append(f'  <url><loc>{BASE}{path}</loc><lastmod>{modificado(path)}</lastmod><priority>{prio}</priority>{ims}</url>')
    sm.append('</urlset>')
    (DIST / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
    bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'Google-Extended', 'ClaudeBot', 'Bingbot', 'Googlebot']
    rb = '# Laboratório Dental Araújo – robots.txt\n# Buscadores e assistentes de IA são bem-vindos.\n\n'
    rb += ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)
    rb += f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n'
    (DIST / 'robots.txt').write_text(rb, encoding='utf-8')
    # llms.txt
    L = [f'# {NAME}', '',
         '> Laboratório de prótese dentária em Belo Horizonte (MG), fundado em 1975, com mais de 40 profissionais e 10 salas no Edifício Mesbla. Atende cirurgiões-dentistas e clínicas de BH, da Grande BH e de Minas Gerais (coleta e entrega) e de todo o Brasil (envio pelos Correios ou transportadora). Serviços sob orçamento, pelo WhatsApp ou telefone.', '',
         'Público: somente cirurgiões-dentistas e clínicas. O laboratório não atende pacientes diretamente (Lei nº 6.710/1979, art. 4º).', '',
         'Valores: sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelos telefones (31) 3271-9766 e (31) 3271-9688.', '',
         '## Fatos rápidos', ''] + [f'- {k}: {v}' for k, v in FACTS] + ['',
         '## Páginas principais', '',
         f'- [Início]({BASE}/): visão geral do laboratório',
         f'- [Serviços]({BASE}/servicos/): todos os tipos de prótese',
         f'- [Sobre]({BASE}/sobre/): história e estrutura',
         f'- [Trabalhos]({BASE}/trabalhos/): fotos reais de próteses feitas no laboratório, por categoria',
         f'- [Envio para todo o Brasil]({BASE}/envio-para-todo-brasil/): como enviar casos',
         f'- [Perguntas frequentes]({BASE}/perguntas-frequentes/): prazos, urgência, garantia, pagamento',
         f'- [Contato]({BASE}/contato/): telefones, WhatsApp, endereço e como pedir orçamento', '', '## Serviços', ''] + \
        [f'- [{s["nav"]}]({BASE}/servicos/{s["slug"]}/): {s["blurb"]} Sob orçamento.' for s in SERVICOS] + \
        ['', '## Blog', ''] + [f'- [{q["h1"]}]({BASE}/blog/{q["slug"]}/): {q["desc"]}' for q in POSTS_RECENTES] + \
        ['', '## Documentos', '', f'- [Política de privacidade]({BASE}/politica-de-privacidade/): dados tratados pelo site e pelo atendimento (LGPD)',
         f'- [Termos de uso]({BASE}/termos-de-uso/): uso do site, orçamento, prazos, garantia e pagamento'] + \
        ['', '## Opcional', '', f'- [Versão completa para LLMs]({BASE}/llms-full.txt): itens de cada serviço, condições e FAQ em texto', '']
    (DIST / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')
    F = [f'# {NAME} – informações completas', '', f'Atualizado em {TODAY}. Fonte: informações oficiais do laboratório. Os serviços são feitos sob orçamento; o site não publica valores.', '',
         '## Identificação', '', f'- Nome: {NAME} (LDA) – razão social Laboratório Dental Araújo Ltda, CNPJ 19.223.635/0001-86',
         f'- Endereço: {ADDR}', '- Telefones: (31) 3271-9766, (31) 3271-9688 · WhatsApp (31) 98652-1387',
         '- Financeiro: (31) 3212-1384 · WhatsApp (31) 98652-1201', '- E-mail: dentalaraujo@yahoo.com.br',
         f'- Instagram: {IG} · Facebook: {FB} · Google Maps: {MAPS}', f'- Site: {BASE}/', '',
         '## Fatos rápidos', ''] + [f'- {k}: {v}' for k, v in FACTS] + ['', '## Itens por linha de serviço (sob orçamento)', '']
    for c in CATS:
        F.append(f'### {c["title"]}')
        F += [f'- {n}' for n in c['items']]
        F += [f'- Obs.: {o}' for o in c['obs']] + ['']
    F += ['## Condições de trabalho', ''] + [f'- {strip(t)}' for t in CONDICOES] + ['', '## Serviços (resumo)', '']
    for s in SERVICOS:
        F += [f'### {s["nav"]} – {BASE}/servicos/{s["slug"]}/', strip(s['lead']), ''] + [f'- P: {q} R: {strip(a)}' for q, a in s['faq']] + ['']
    F += ['## Perguntas frequentes', '']
    for g, pairs in FAQ_GROUPS:
        F += [f'### {g}'] + [f'- P: {q} R: {strip(a)}' for q, a in pairs] + ['']
    F += ['## Artigos do blog (resumo e fontes)', '']
    for q in POSTS_RECENTES:
        F += [f'### {q["h1"]} – {BASE}/blog/{q["slug"]}/', f'Publicado em {q["date"]}. {strip(q["lead"])}', '']
        F += [f'- Fonte: {strip(t)} {u}' for t, u in q.get('refs', [])]
        if q.get('refs'): F.append('')
    (DIST / 'llms-full.txt').write_text('\n'.join(F), encoding='utf-8')

def build_legal(doc, other):
    """Documento legal: sumário gerado dos ids das seções (aside à esquerda no DOM, para vir antes no celular)."""
    path = doc['path']; url = BASE + path
    trail = [('Início', '/'), (doc['name'], path)]
    p = dict(path=path, title=doc['title'], desc=doc['desc'], trail=trail)
    body = ''.join(f'<h2 id="{i}">{t}</h2>{h}' for i, t, h in doc['sections'])
    toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in doc['sections'])
    aside = f'''<aside class="aside">
  <nav class="abox toc" aria-label="Neste documento"><p class="abox__h">Neste documento</p><ol>{toc}</ol></nav>
  <div class="abox"><p class="abox__h">Vigência</p><p class="abox__note">Vigente desde <strong>{VIGENCIA}</strong>. Dúvidas: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <a class="btn btn--ghost" href="{other['path']}">{other['name']}</a></div>
</aside>'''
    main = f'''{phero(trail, doc['kicker'], doc['h1'], doc['lead'], cta=False, meta=f'<p class="phero__meta">Atualizado em {VIGENCIA}</p>')}
<section class="sec"><div class="container page page--legal">{aside}<article class="prose prose--legal">{body}</article></div></section>'''
    out(path, page(p, main, [webpage(p, url), crumbs_ld(trail, url)]), '0.3')

# Cloudflare Workers/Pages: só aceita 200, 301, 302, 303, 307, 308 (sem "!" do Netlify e sem 404).
# O status 404 da página de erro vem de wrangler.jsonc → assets.not_found_handling = "404-page".
REDIRECTS = """# Tabela de preços removida em 24/10/2026: os serviços passaram a ser sob orçamento.
/tabela-de-precos/  /contato/  301
/tabela-de-precos   /contato/  301
"""

def redirects_index():
    """Auditoria 26/10/2026: /pasta/index.html → URL canônica com barra.

    No Cloudflare, redirects do ``_redirects`` aplicam mesmo se o arquivo existir
    (não precisa do ``!`` do Netlify). Regras explícitas por página, sem curingas.
    """
    linhas = ['# /…/index.html → URL canônica com barra (gerado por redirects_index())']
    for path, _ in PAGES:
        linhas.append(f'{path}index.html  {path}  301')
    return '\n'.join(linhas) + '\n'

def main():
    """Ordem importa: static → minificação → páginas (ver() lê o hash do CSS/JS já minificado) → meta."""
    copy_and_minify_assets()
    build_home(); build_hub()
    for s in SERVICOS: build_service(s)
    build_sobre(); build_trabalhos(); build_envio(); build_faq(); build_contato(); build_blog()
    build_legal(PRIVACIDADE, TERMOS); build_legal(TERMOS, PRIVACIDADE); build_404()
    build_meta()
    (DIST / '_headers').write_text(headers_file(), encoding='utf-8')
    (DIST / '_redirects').write_text(REDIRECTS + redirects_index(), encoding='utf-8')
    print(f'ok: {len(PAGES)} páginas + 404 → {DIST}')

if __name__ == '__main__':
    main()
