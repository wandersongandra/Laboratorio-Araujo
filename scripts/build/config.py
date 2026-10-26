"""Configuração do gerador estático e caminhos do projeto."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
DIST = ROOT / "dist"
ASSETS = SRC / "assets"
CONTENT = SRC / "content"
DATA = SRC / "data"
PRIVATE = SRC / "private"
FOTOS_JSON = SRC / "fotos_reais.json"

for p in (str(CONTENT), str(DATA), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

from laboratorio import LAB  # noqa: E402

# Endereço público do site. Usado em canonical, og:url, sitemap, JSON-LD e llms.txt.
# Ao trocar para o domínio próprio (ex.: https://www.dentalaraujo.com.br), mude aqui e rode o build.
BASE = "https://brilliant-cat-c5b6e9.netlify.app"
TODAY = "2026-10-26"
# Auditoria 26/10/2026: páginas cujo conteúdo não mudou desde outra data.
MODIFICADO = {
    "/politica-de-privacidade/": "2026-10-24",
    "/termos-de-uso/": "2026-10-24",
}

NAME: str = LAB["name"]  # type: ignore[assignment,index]
WA: str = LAB["whatsapp"]["pedidos"]["e164"]  # type: ignore[index]
MAPS: str = LAB["social"]["maps"]  # type: ignore[index]
IG: str = LAB["social"]["instagram"]  # type: ignore[index]
FB: str = LAB["social"]["facebook"]  # type: ignore[index]
ADDR: str = LAB["address"]["full"]  # type: ignore[index]
EMAIL: str = LAB["email"]  # type: ignore[assignment,index]
CNPJ: str = LAB["cnpj"]  # type: ignore[assignment,index]
LEGAL_NAME: str = LAB["legal_name"]  # type: ignore[assignment,index]

# Atalhos de formatação (mesmos textos do site legado).
_ADDR = LAB["address"]  # type: ignore[index]
_PHONES = LAB["phones"]["pedidos"]  # type: ignore[index]
_WA = LAB["whatsapp"]["pedidos"]  # type: ignore[index]
_HOURS = LAB["hours"]  # type: ignore[index]

ADDR_UTIL = f"{_ADDR['street']} · {_ADDR['floor']} · {_ADDR['district']}, BH"
ADDR_FOOTER_L1 = f"{_ADDR['street']}, {_ADDR['floor']}, {_ADDR['room']}"
ADDR_FOOTER_L2 = (
    f"{_ADDR['building']}, {_ADDR['district']}, {_ADDR['city']}/{_ADDR['region']}, {_ADDR['postal']}"
)
PHONE_1_DISPLAY = _PHONES[0]["display"]  # type: ignore[index]
PHONE_1_TEL = _PHONES[0]["tel"]  # type: ignore[index]
PHONE_2_DISPLAY = _PHONES[1]["display"]  # type: ignore[index]
PHONE_2_TEL = _PHONES[1]["tel"]  # type: ignore[index]
WA_DISPLAY = _WA["display"]  # type: ignore[index]
HOURS_CURTO = _HOURS["texto_curto"]  # type: ignore[index]
HOURS_FOOTER = _HOURS["texto_longo"]  # type: ignore[index]
HOURS_LONGO = _HOURS["texto_longo"]  # type: ignore[index]
HOURS_FRASE = _HOURS["texto_frase"]  # type: ignore[index]


def tel_schema(e164: str) -> str:
    """Formato do JSON-LD legado: fixo +55-31-3271-9766; móvel +55-31-98652-1387."""
    rest = e164[2:]
    ddd, num = rest[:2], rest[2:]
    if len(num) == 9:
        return f"+55-{ddd}-{num[:5]}-{num[5:]}"
    return f"+55-{ddd}-{num[:4]}-{num[4:]}"


PHONE_1_SCHEMA = tel_schema(_PHONES[0]["e164"])  # type: ignore[index]
PHONE_2_SCHEMA = tel_schema(_PHONES[1]["e164"])  # type: ignore[index]
WA_SCHEMA = tel_schema(_WA["e164"])  # type: ignore[index]
FIN_PHONE_SCHEMA = tel_schema(LAB["phones"]["financeiro"][0]["e164"])  # type: ignore[index]
FIN_WA_SCHEMA = tel_schema(LAB["whatsapp"]["financeiro"]["e164"])  # type: ignore[index]
STREET_SCHEMA = _ADDR["street_schema"]  # type: ignore[index]

# Ordem de concatenação do CSS (= cascata do style.css legado).
CSS_BUNDLE = [
    "tokens.css",
    "base.css",
    "buttons.css",
    "layout-chrome.css",
    "layout-sections.css",
    "pages-home.css",
    "components.css",
    "pages-internal.css",
    "motion.css",
    "layout-responsive.css",
]

JS_BUNDLE = (ASSETS / "js" / "modules" / "bundle.txt").read_text(encoding="utf-8").split()


def modificado(path: str) -> str:
    return MODIFICADO.get(path, TODAY)
