"""Utilitários de texto e versionamento de assets."""

from __future__ import annotations

import hashlib
import html
import re
from urllib.parse import quote

from .config import DIST, WA

e = html.escape


def wa(t: str) -> str:
    """Mensagem do WhatsApp sempre codificada (quote)."""
    return f"https://wa.me/{WA}?text=" + quote(t)


def strip(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def ver(p: str) -> str:
    """Hash curto do arquivo JÁ publicado em dist/ → ?v= para quebrar cache."""
    return hashlib.md5((DIST / p.lstrip("/")).read_bytes()).hexdigest()[:8]


_NW = re.compile(r"(<h[1-3]\b[^>]*>)(.*?)(</h[1-3]>)", re.S)


def nobreak(htmltext: str) -> str:
    """Evita quebra de linha no hífen de E-Max em títulos."""
    return _NW.sub(
        lambda m: m.group(1)
        + re.sub(r"(?<![\w-])E-Max\b", '<span class="nw">E-Max</span>', m.group(2))
        + m.group(3),
        htmltext,
    )


def telclass(t: str) -> str:
    """Links tel: ganham a classe tel (white-space:nowrap)."""
    t = re.sub(r'<a class="([^"]*)"( href="tel:)', r'<a class="\1 tel"\2', t)
    return re.sub(r'<a href="tel:', '<a class="tel" href="tel:', t)


def lc(t: str) -> str:
    """Minúscula só na primeira letra, preservando siglas."""
    return t[0].lower() + t[1:] if len(t) > 1 and t[1].islower() else t
