#!/usr/bin/env python3
"""QA de rotas e URLs (teste de regressão da auditoria de 26/10/2026).

Verifica, a partir do sitemap publicado:
  • robots.txt e sitemap.xml (só URLs 200, canônicas, com <lastmod> válido);
  • em cada página: status 200 sem redirecionamento, canonical = og:url = URL do sitemap,
    1 <h1>, title e description presentes e únicos;
  • todos os links internos (a, link, img, srcset, script, source, og:image, ícones do manifest):
    respondem 200 direto (sem passar por redirecionamento) e âncoras #id existem na página alvo;
  • URLs dentro do JSON-LD, do llms.txt e do llms-full.txt;
  • páginas HTML encontradas no rastreamento x sitemap (órfãs e sobrando);
  • 404 de verdade (status 404 + noindex), arquivos sensíveis inacessíveis;
  • links tel:, mailto:, wa.me e target=_blank com rel=noopener;
  • no modo --live (padrão quando a base é https): variantes sem barra / MAIÚSCULAS /
    index.html → 301 em um único salto para a URL canônica; redirecionamentos do _redirects
    em 301 de um salto até uma página 200; cabeçalhos de segurança.

Uso:  python3 tools/qa_rotas.py [URL_BASE] [--externos]
      (padrão: site ao vivo; para o servidor local use http://localhost:8766)
--externos também testa os links externos (só avisa, não reprova: alguns sites bloqueiam robôs).
Sai com código 1 se algo falhar. Só usa a biblioteca padrão do Python.
"""
import sys, re, json, ssl, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
BASE = (ARGS[0] if ARGS else 'https://brilliant-cat-c5b6e9.netlify.app').rstrip('/')
LIVE = BASE.startswith('https://')
EXTERNOS = '--externos' in sys.argv
ROOT = Path(__file__).resolve().parent.parent
# URL de produção gravada nos arquivos (canonical, sitemap etc.)
PROD = re.search(r"^BASE\s*=\s*['\"](.+?)['\"]", (ROOT / 'scripts/build/config.py').read_text(encoding='utf-8'), re.M).group(1).rstrip('/')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) LDA-QA/1.0'}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
OPENER = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
CACHE = {}

def get(url, method='GET'):
    """(status, headers, corpo) sem seguir redirecionamentos."""
    key = (url, method)
    if key in CACHE: return CACHE[key]
    try:
        r = OPENER.open(urllib.request.Request(url, headers=UA, method=method), timeout=20)
        res = (r.status, {k.lower(): v for k, v in r.headers.items()}, r.read() if method == 'GET' else b'')
    except urllib.error.HTTPError as e:
        res = (e.code, {k.lower(): v for k, v in e.headers.items()}, e.read() if method == 'GET' else b'')
    except Exception as e:
        res = (0, {}, str(e).encode())
    CACHE[key] = res
    return res

def local(u):
    """Converte URL de produção para a BASE testada."""
    return BASE + u[len(PROD):] if u.startswith(PROD) else u

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.refs, s.ids, s.blank, s.h1, s.meta, s.links, s.ld = [], set(), [], 0, {}, {}, []
        s._ld = None; s._t = None; s.title = ''
    def handle_starttag(s, tag, at):
        a = dict(at)
        if 'id' in a: s.ids.add(a['id'])
        if tag == 'a' and 'name' in a: s.ids.add(a['name'])
        if tag == 'h1': s.h1 += 1
        if tag == 'title': s._t = ''
        if tag == 'meta':
            k = a.get('name') or a.get('property')
            if k: s.meta[k] = a.get('content', '')
        if tag == 'link' and a.get('rel'): s.links.setdefault(a['rel'], []).append(a.get('href', ''))
        if tag == 'script' and a.get('type') == 'application/ld+json': s._ld = ''
        for k in ('href', 'src'):
            if a.get(k) is not None and not (tag == 'link' and a.get('rel') in ('preconnect', 'dns-prefetch')):
                s.refs.append((tag, a[k]))
        for k in ('srcset', 'imagesrcset'):
            if a.get(k):
                for part in a[k].split(','):
                    if part.strip(): s.refs.append((tag, part.strip().split()[0]))
        if tag == 'a' and a.get('target') == '_blank': s.blank.append((a.get('href'), a.get('rel') or ''))
    def handle_data(s, d):
        if s._ld is not None: s._ld += d
        if s._t is not None: s._t += d
    def handle_endtag(s, tag):
        if tag == 'script' and s._ld is not None: s.ld.append(s._ld); s._ld = None
        if tag == 'title' and s._t is not None: s.title = s._t.strip(); s._t = None

falhas, avisos = [], []
def falha(msg): falhas.append(msg); print('  ✗', msg)
def aviso(msg): avisos.append(msg); print('  !', msg)

def urls_json(o):
    if isinstance(o, dict):
        for v in o.values(): yield from urls_json(v)
    elif isinstance(o, list):
        for v in o: yield from urls_json(v)
    elif isinstance(o, str) and o.startswith('http'): yield o

print(f'QA de rotas — base {BASE} ({"ao vivo" if LIVE else "local"}), produção {PROD}')

# 1. robots e sitemap ---------------------------------------------------------
st, h, robots = get(BASE + '/robots.txt')
if st != 200: falha(f'robots.txt → {st}')
elif f'Sitemap: {PROD}/sitemap.xml' not in robots.decode(): falha('robots.txt sem a linha Sitemap correta')
if re.search(r'^Disallow:\s*/\s*$', robots.decode(), re.M): falha('robots.txt bloqueia o site inteiro')
st, h, sm = get(BASE + '/sitemap.xml')
if st != 200: falha(f'sitemap.xml → {st}'); sys.exit(1)
sm = sm.decode()
locs = re.findall(r'<loc>(.*?)</loc>', sm)
for lm in re.findall(r'<lastmod>(.*?)</lastmod>', sm):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm): falha(f'lastmod inválido: {lm}')
if len(set(locs)) != len(locs): falha('URLs repetidas no sitemap')
print(f'sitemap: {len(locs)} URLs')

# 2. páginas --------------------------------------------------------------------
pages, titles, descs, refs = {}, {}, {}, {}
for loc in locs:
    if not loc.startswith(PROD + '/') or not loc.endswith('/'): falha(f'sitemap com URL fora do padrão: {loc}')
    st, h, body = get(local(loc))
    if st != 200: falha(f'{loc} → {st} (sitemap deve ter só URLs 200)'); continue
    p = P(); p.feed(body.decode('utf-8', 'replace')); pages[loc] = p
    can = (p.links.get('canonical') or [''])[0]
    if can != loc: falha(f'{loc}: canonical = {can!r}')
    if p.meta.get('og:url') != loc: falha(f'{loc}: og:url = {p.meta.get("og:url")!r}')
    if 'noindex' in p.meta.get('robots', ''): falha(f'{loc}: noindex numa URL do sitemap')
    if p.h1 != 1: falha(f'{loc}: {p.h1} <h1>')
    if not p.title: falha(f'{loc}: sem <title>')
    if not p.meta.get('description'): falha(f'{loc}: sem meta description')
    titles.setdefault(p.title, []).append(loc); descs.setdefault(p.meta.get('description'), []).append(loc)
    for href, rel in p.blank:
        if 'noopener' not in rel.split(): falha(f'{loc}: target=_blank sem rel=noopener → {href}')
    for blk in p.ld:
        try: data = json.loads(blk)
        except Exception as e: falha(f'{loc}: JSON-LD inválido ({e})'); continue
        for u in urls_json(data):   # #fragmentos do JSON-LD são @id de nós, não âncoras HTML
            refs.setdefault(u.split('#')[0], set()).add(loc + ' [JSON-LD]')
    for k in ('og:image', 'twitter:image'):
        if p.meta.get(k): refs.setdefault(p.meta[k], set()).add(loc + f' [{k}]')
    for tag, r in p.refs:
        refs.setdefault(urllib.parse.urljoin(loc, r), set()).add(loc)
for d, n in [(titles, 'title'), (descs, 'description')]:
    for k, v in d.items():
        if len(v) > 1: falha(f'{n} repetido em {len(v)} páginas: {k!r}')

# 3. llms.txt e manifest --------------------------------------------------------
for f in ('/llms.txt', '/llms-full.txt'):
    st, h, b = get(BASE + f)
    if st != 200: falha(f'{f} → {st}'); continue
    for u in re.findall(r'https?://[^\s)>\]"]+', b.decode()):
        refs.setdefault(u.rstrip('.,;'), set()).add(f)
st, h, b = get(BASE + '/site.webmanifest')
if st != 200: falha(f'site.webmanifest → {st}')
else:
    for ic in json.loads(b).get('icons', []): refs.setdefault(PROD + ic['src'], set()).add('site.webmanifest')

# 4. checar cada referência -----------------------------------------------------
externos, html_achados = {}, set()
for u, origem in sorted(refs.items()):
    o = sorted(origem)[0]
    if u.startswith(('tel:', 'mailto:')):
        if u.startswith('tel:') and not re.fullmatch(r'tel:\+55\d{10,11}', u): falha(f'{o}: tel mal formatado {u}')
        if u.startswith('mailto:') and not re.fullmatch(r'mailto:[^@\s]+@[^@\s]+\.[a-z]{2,}(\?.*)?', u): falha(f'{o}: mailto mal formatado {u}')
        continue
    if u.startswith('data:'): continue
    if u.startswith('http://'): falha(f'{o}: link http:// (conteúdo misto/sem TLS) {u}'); continue
    if not u.startswith(PROD):
        if u.startswith('https://wa.me/') and not re.fullmatch(r'https://wa\.me/55\d{10,11}(\?text=[^\s]*)?', u):
            falha(f'{o}: link de WhatsApp mal formatado {u}')
        externos.setdefault(u.split('#')[0], set()).update(origem); continue
    path, _, frag = u.partition('#')
    st, h, body = get(local(path))
    if st in (301, 302, 307, 308):
        falha(f'{o}: link interno passa por redirecionamento {st} → {path} → {h.get("location")}'); continue
    if st != 200: falha(f'{o}: link interno quebrado {st} → {u}'); continue
    if 'text/html' in h.get('content-type', '') and '?' not in path:
        html_achados.add(path)
    if frag:
        alvo = pages.get(path)
        if alvo is None:
            alvo = P(); alvo.feed(body.decode('utf-8', 'replace'))
        if frag not in alvo.ids: falha(f'{o}: âncora inexistente #{frag} em {path}')
print(f'referências verificadas: {len(refs)} ({len(externos)} externas)')

orf = html_achados - set(locs)
for u in sorted(orf): falha(f'página HTML linkada mas fora do sitemap: {u}')
nao_linkadas = set(locs) - html_achados
for u in sorted(nao_linkadas): aviso(f'URL do sitemap sem nenhum link interno: {u}')

# 5. 404 e arquivos sensíveis --------------------------------------------------
st, h, b = get(BASE + '/esta-pagina-nao-existe-qa/')
if st != 404: falha(f'página inexistente → {st} (esperado 404)')
elif b'noindex' not in b: falha('página 404 sem noindex')
for f in ['/scripts/build/config.py', '/package.json', '/README.md', '/docs/', '/tools/qa_rotas.py', '/.git/config',
          '/.env', '/_headers', '/_redirects', '/netlify.toml', '/assets/docs/tabela-precos-2026.pdf',
          '/private/arquivo/', '/src/content/', '/node_modules/', '/assets/js/main.js.map', '/assets/css/style.css.map']:
    if not LIVE and f.startswith('/_'): continue   # o servidor local não esconde _headers/_redirects (o Netlify sim)
    st, h, b = get(BASE + f)
    if st == 200: falha(f'arquivo que não deveria ser público responde 200: {f}')

# 6. modo ao vivo: variantes, redirecionamentos, cabeçalhos ---------------------
if LIVE:
    def um_salto(origem, destino, rotulo):
        st, h, _ = get(origem)
        loc = urllib.parse.urljoin(origem, h.get('location', ''))
        if st != 301: falha(f'{rotulo}: {origem} → {st} (esperado 301)'); return
        if loc != destino: falha(f'{rotulo}: {origem} → {loc} (esperado {destino})'); return
        st2, _, _ = get(destino)
        if st2 != 200: falha(f'{rotulo}: destino {destino} → {st2} (cadeia de redirecionamentos)')
    for loc in locs:
        u = local(loc); path = u[len(BASE):]
        if path == '/':
            um_salto(BASE + '/index.html', BASE + '/', 'index.html'); continue
        um_salto(u.rstrip('/'), u, 'sem barra final')
        um_salto(u + 'index.html', u, 'index.html')
        if path.upper() != path:
            um_salto(BASE + path.upper(), u, 'maiúsculas')
    for line in (ROOT / 'dist/_redirects').read_text().splitlines():
        if line.strip() and not line.startswith('#'):
            src, dst, code = line.split()[:3]
            if code.startswith('404'):
                st, _, _ = get(BASE + src)
                if st != 404: falha(f'_redirects: {src} → {st} (esperado 404)')
            else:
                um_salto(BASE + src, BASE + dst, '_redirects')
    st, h, _ = get(BASE + '/')
    hl = h
    for k in ['content-security-policy', 'strict-transport-security', 'x-content-type-options',
              'x-frame-options', 'referrer-policy', 'permissions-policy']:
        if k not in hl: falha(f'cabeçalho ausente: {k}')
    if "frame-ancestors 'none'" not in hl.get('content-security-policy', ''): falha('CSP sem frame-ancestors')

# 7. externos (opcional) --------------------------------------------------------
if EXTERNOS:
    for u in sorted(externos):
        req = urllib.request.Request(u, headers=UA)
        try:
            code = urllib.request.urlopen(req, timeout=20).status
        except urllib.error.HTTPError as e: code = e.code
        except Exception as e: code = f'erro ({e.__class__.__name__})'
        (print if code == 200 else aviso)(f'  externo {code}: {u}')

print(f'\n{len(falhas)} falha(s), {len(avisos)} aviso(s)')
sys.exit(1 if falhas else 0)
