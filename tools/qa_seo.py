#!/usr/bin/env python3
"""Auditoria de SEO do dist/: título (≤60) e descrição por página, um H1, saltos de
hierarquia de títulos, JSON-LD válido, links/imagens internos inexistentes, imagens sem alt,
títulos/descrições duplicados.  Uso: python3 tools/qa_seo.py"""
import re,json,glob,os
from pathlib import Path
D=str(Path(__file__).resolve().parent.parent/'dist')
titles={};descs={};bad=[]
for f in sorted(glob.glob(D+'/**/*.html',recursive=True)):
    s=open(f).read(); rel=f[len(D):].replace('\\','/')
    t=re.search(r'<title>(.*?)</title>',s).group(1); d=re.search(r'name="description" content="(.*?)"',s).group(1)
    titles.setdefault(t,[]).append(rel); descs.setdefault(d,[]).append(rel)
    h1=len(re.findall(r'<h1[\s>]',s))
    hs=[int(x) for x in re.findall(r'<h([1-6])[\s>]',s)]
    jumps=[(a,b) for a,b in zip(hs,hs[1:]) if b>a+1]
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: g=json.loads(m)
        except Exception as ex: bad.append((rel,'jsonld',ex))
    types=[n['@type'] for n in json.loads(re.search(r'ld\+json">(.*?)</script>',s,re.S).group(1))['@graph']]
    for u in re.findall(r'(?:href|src)="(/[^"#?]*)',s)+[x.split()[0] for x in re.findall(r'srcset="([^"]+)"',s) for x in x.split(', ')]:
        p=D+u; p=p+'index.html' if p.endswith('/') else p
        if not os.path.exists(p): bad.append((rel,'missing',u))
    imgs=re.findall(r'<img[^>]*>',s); noalt=[i for i in imgs if 'alt=' not in i]
    words=len(re.sub(r'<[^>]+>',' ',re.search(r'<main id="conteudo">(.*)</main>',s,re.S).group(1)).split())
    print(f'{rel:60} t{len(t):3} d{len(d):3} h1={h1} jumps={len(jumps)} noalt={len(noalt)} words={words} {types[2:]}')
    if h1!=1: bad.append((rel,'h1',h1))
    if jumps: bad.append((rel,'jumps',jumps[:3]))
    if noalt: bad.append((rel,'alt',len(noalt)))
    if not 20<=len(t)<=60: bad.append((rel,'title_len',len(t)))
    if rel!='/404.html' and not 70<=len(d)<=160: bad.append((rel,'desc_len',len(d)))
print('dup titles',[v for v in titles.values() if len(v)>1]); print('dup desc',[v for v in descs.values() if len(v)>1])
print('BAD',bad)
dups=[v for v in titles.values() if len(v)>1]+[v for v in descs.values() if len(v)>1]
raise SystemExit(1 if bad or dups else 0)   # auditoria 26/10/2026: antes só imprimia, nunca reprovava
