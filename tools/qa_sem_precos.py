#!/usr/bin/env python3
"""QA "sem preços": garante que o site publicado não mostra valores nem a antiga tabela.

Desde 24/10/2026 os serviços são sob orçamento. Este script:
  1. varre dist/ (HTML, TXT, XML, JSON-LD) atrás de "R$", "preço", "tabela-de-precos",
     ".pdf" e de Offer/price/priceRange nos dados estruturados; só o PDF em PDFS_OK é aceito, e o texto dele é varrido;
  2. com --live URL, confere no ar que /tabela-de-precos/ responde 301 → /contato/
     e que o PDF antigo não responde 200.

Uso:  python3 tools/qa_sem_precos.py                    (só dist/)
      python3 tools/qa_sem_precos.py --live https://brilliant-cat-c5b6e9.netlify.app
"""
import re, sys, json, subprocess, urllib.request, urllib.error
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / 'dist'
PADROES = [r'R\$', r'preço', r'tabela-de-precos', r'\.pdf\b', r'tabela de preços']
# Ocorrências legítimas: a regra de redirecionamento e a frase dos termos que diz que o site não publica preços.
PERMITIDAS = {('_redirects', None), ('termos-de-uso/index.html', 'O site não publica preços.'),
              ('blog/requisicao-para-laboratorio-de-protese/index.html', '/assets/docs/requisicao-laboratorio-de-protese.pdf')}
# Único PDF permitido (26/10/2026): o modelo de requisição em branco. O texto dele também é varrido (pdftotext).
PDFS_OK = {'assets/docs/requisicao-laboratorio-de-protese.pdf'}

def permitida(rel, linha):
    return any(rel == f and (t is None or t in linha) for f, t in PERMITIDAS)

def varrer():
    erros = 0
    for f in sorted(DIST.rglob('*')):
        if not f.is_file() or f.suffix not in ('.html', '.txt', '.xml', '.webmanifest', '') : continue
        rel = f.relative_to(DIST).as_posix()
        for n, linha in enumerate(f.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            for p in PADROES:
                if re.search(p, linha, re.I) and not permitida(rel, linha):
                    erros += 1; print(f'  {rel}:{n}  [{p}]  {linha.strip()[:110]}')
        if f.suffix == '.html':
            for bloco in re.findall(r'<script type="application/ld\+json">(.*?)</script>', f.read_text(encoding='utf-8'), re.S):
                s = json.dumps(json.loads(bloco))
                for chave in ('"Offer', '"price"', '"priceRange"', '"priceCurrency"', 'OfferCatalog'):
                    if chave in s: erros += 1; print(f'  {rel}: JSON-LD contém {chave}')
    for f in DIST.rglob('*.pdf'):
        rel = f.relative_to(DIST).as_posix()
        if rel not in PDFS_OK: erros += 1; print(f'  PDF não permitido em dist/: {rel}'); continue
        try: txt = subprocess.run(['pdftotext', str(f), '-'], capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError): erros += 1; print(f'  não foi possível ler {rel} (instale poppler-utils)'); continue
        for p in (r'R\$', r'preço', r'tabela de preços'):
            if re.search(p, txt, re.I): erros += 1; print(f'  {rel}: contém [{p}]')
    return erros

class _SemRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None

def ao_vivo(base):
    op = urllib.request.build_opener(_SemRedirect)
    def req(path):
        try: r = op.open(urllib.request.Request(base + path, method='GET'), timeout=20); return r.status, r.headers
        except urllib.error.HTTPError as e: return e.code, e.headers
    erros = 0
    for path in ('/tabela-de-precos/', '/tabela-de-precos'):
        st, h = req(path); loc = h.get('Location', '')
        ok = st == 301 and loc.rstrip('/').endswith('/contato')
        print(f'  {path} → {st} {loc}  {"ok" if ok else "ERRO"}'); erros += not ok
    st, _ = req('/assets/docs/tabela-precos-2026.pdf')
    print(f'  /assets/docs/tabela-precos-2026.pdf → {st}  {"ok" if st != 200 else "ERRO"}'); erros += st == 200
    return erros

if __name__ == '__main__':
    print('dist/:'); e = varrer()
    if '--live' in sys.argv: print('no ar:'); e += ao_vivo(sys.argv[sys.argv.index('--live') + 1].rstrip('/'))
    print('OK: nenhum preço publicado' if e == 0 else f'FALHOU: {e} problema(s)')
    sys.exit(1 if e else 0)
