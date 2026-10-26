"""Minificação e montagem de CSS/JS para dist/."""

from __future__ import annotations

import re
import shutil

from .config import ASSETS, CSS_BUNDLE, DIST, JS_BUNDLE


def minify_css(src: str) -> str:
    """Remove comentários /* */ e espaços redundantes."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            out.append(src[i : j + 1])
            i = j + 1
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    css = "".join(out)
    parts = re.split(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', css)
    for k in range(0, len(parts), 2):
        t = re.sub(r"\s+", " ", parts[k])
        t = re.sub(r"\s*([{};,>])\s*", r"\1", t)
        parts[k] = t.replace(";}", "}")
    return "".join(parts).strip() + "\n"


def minify_js(src: str) -> str:
    """Remove comentários de linha/bloco e indentação; mantém quebras."""
    src = re.sub(r"^\s*/\*.*?\*/\s*$", "", src, flags=re.S | re.M)
    lines = []
    for line in src.splitlines():
        t = line.strip()
        if t and not t.startswith("//"):
            lines.append(t)
    return "\n".join(lines) + "\n"


def assemble_css() -> str:
    css_dir = ASSETS / "css"
    parts = [(css_dir / name).read_text(encoding="utf-8") for name in CSS_BUNDLE]
    header = (
        "/* Laboratório Dental Araújo — CSS gerado (bundle). "
        "Fontes em src/assets/css/; ver docs/ARQUITETURA.md. */\n"
    )
    return header + "".join(parts)


def assemble_js() -> str:
    mod_dir = ASSETS / "js" / "modules"
    header = (
        "/**\n"
        " * Laboratório Dental Araújo — interações "
        "(JS gerado a partir de src/assets/js/modules).\n"
        " */\n"
    )
    body = "".join((mod_dir / name).read_text(encoding="utf-8") for name in JS_BUNDLE)
    return header + "(() => {\n  'use strict';\n" + body + "})();\n"


def copy_and_minify_assets() -> None:
    """Copia src/assets → dist/ e grava CSS/JS minificados concatenados."""
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for name in ("favicon.ico", "site.webmanifest"):
        shutil.copy2(ASSETS / name, DIST / name)
    dest_assets = DIST / "assets"
    # favicon/manifest ficam na raiz de dist/ (como no Netlify legado), não em assets/.
    shutil.copytree(
        ASSETS,
        dest_assets,
        ignore=shutil.ignore_patterns("css", "js", "favicon.ico", "site.webmanifest"),
    )
    (dest_assets / "css").mkdir(parents=True)
    (dest_assets / "js").mkdir(parents=True)
    (dest_assets / "css" / "style.css").write_text(minify_css(assemble_css()), encoding="utf-8")
    (dest_assets / "js" / "main.js").write_text(minify_js(assemble_js()), encoding="utf-8")
