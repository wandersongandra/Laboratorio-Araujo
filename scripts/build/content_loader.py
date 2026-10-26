"""Carrega o conteúdo editorial de ``src/content/``."""

from __future__ import annotations

from blog import POSTS
from catalogo import CATS, CONDICOES
from fotos_reais import FAIXA_REAL
from fotos_reais import CATS as FR_CATS
from fotos_reais import FOTOS as FOTOS_REAIS
from fotos_reais import POR_ID as FR_ID
from fotos_reais import POR_SLUG as FR_SLUG
from legal import PRIVACIDADE, TERMOS, VIGENCIA
from legal import EMAIL as LEGAL_EMAIL
from paginas import FACTS, FAQ_GROUPS
from resumos import RESUMO, RESUMO_ENVIO, RESUMO_SOBRE, TAG
from servicos import GARANTIA, PRAZO, SERVICOS, porque

__all__ = [
    "CATS",
    "CONDICOES",
    "SERVICOS",
    "PRAZO",
    "GARANTIA",
    "porque",
    "FOTOS_REAIS",
    "FR_SLUG",
    "FR_CATS",
    "FAIXA_REAL",
    "FR_ID",
    "POSTS",
    "FACTS",
    "FAQ_GROUPS",
    "PRIVACIDADE",
    "TERMOS",
    "VIGENCIA",
    "LEGAL_EMAIL",
    "TAG",
    "RESUMO",
    "RESUMO_SOBRE",
    "RESUMO_ENVIO",
]
