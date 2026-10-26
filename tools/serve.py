#!/usr/bin/env python3
"""Servidor local que imita o Netlify: serve dist/ com URLs bonitas e aplica os cabeçalhos do
bloco "/*" de dist/_headers (inclusive a Content-Security-Policy), para testar a CSP antes do deploy.

Uso:  python3 tools/serve.py [porta]      (padrão 8766)  →  http://localhost:8766/
"""
import http.server, sys, functools
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / 'dist'

def global_headers():
    hs, on = [], False
    for line in (DIST / '_headers').read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if not line.startswith(' '):
            on = line.strip() == '/*'; continue
        if on and ':' in line:
            k, v = line.strip().split(':', 1); hs.append((k.strip(), v.strip()))
    return hs

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        for k, v in global_headers():
            if k != 'Strict-Transport-Security':   # HSTS não faz sentido em http://localhost
                self.send_header(k, v)
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (DIST / '404.html').exists():   # como o Netlify: 404.html personalizado
            body = (DIST / '404.html').read_bytes()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        super().send_error(code, message, explain)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
    http.server.ThreadingHTTPServer(('', port), functools.partial(Handler, directory=str(DIST))).serve_forever()
