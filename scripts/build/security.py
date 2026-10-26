"""CSP, script inline e dist/_headers."""

from __future__ import annotations

import base64
import hashlib

INLINE_JS = "document.documentElement.classList.add('js')"
INLINE_JS_HASH = (
    "'sha256-"
    + base64.b64encode(hashlib.sha256(INLINE_JS.encode()).digest()).decode()
    + "'"
)

CSP = "; ".join(
    [
        "default-src 'self'",
        f"script-src 'self' {INLINE_JS_HASH}",
        "style-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "frame-src https://www.google.com https://maps.google.com",
        "manifest-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'none'",
        "frame-ancestors 'none'",
        "upgrade-insecure-requests",
    ]
)


def headers_file() -> str:
    """Conteúdo do dist/_headers (Cloudflare Workers/Pages e Netlify)."""
    return f"""# Gerado por scripts.build — não edite em dist/. Ver docs/SEGURANCA.md.
/*
  Content-Security-Policy: {CSP}
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=(), browsing-topics=()
  Cross-Origin-Opener-Policy: same-origin
/assets/css/*
  Cache-Control: public, max-age=31536000, immutable
/assets/js/*
  Cache-Control: public, max-age=31536000, immutable
/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/assets/img/*
  Cache-Control: public, max-age=604800
/assets/icons/*
  Cache-Control: public, max-age=604800
/favicon.ico
  Cache-Control: public, max-age=604800
/site.webmanifest
  Content-Type: application/manifest+json; charset=utf-8
/llms.txt
  Content-Type: text/plain; charset=utf-8
/llms-full.txt
  Content-Type: text/plain; charset=utf-8
"""
