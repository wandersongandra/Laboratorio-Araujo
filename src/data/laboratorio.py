"""Fonte única dos dados do Laboratório Dental Araújo.

Telefones, endereço, horários, e-mail, CNPJ e redes sociais vivem só aqui.
Templates, JSON-LD, llms.txt e conteúdo legal/FAQ devem ler deste módulo.
"""
from __future__ import annotations

from typing import TypedDict


class Telefone(TypedDict):
    label: str
    display: str
    e164: str  # só dígitos com país, ex.: 553132719766
    tel: str  # tel:+55...
    track: str


class WhatsApp(TypedDict):
    label: str
    display: str
    e164: str
    track: str


class Horario(TypedDict):
    dias: str
    abre: str
    fecha: str
    texto_curto: str
    texto_longo: str
    texto_frase: str
    schema: list[dict[str, object]]


LAB: dict[str, object] = {
    "name": "Laboratório Dental Araújo",
    "short_name": "LDA",
    "legal_name": "Laboratório Dental Araújo Ltda",
    "cnpj": "19.223.635/0001-86",
    "founding_year": "1975",
    "founding_date": "1975-09-08",
    "founders": ("Edison Araújo", "Pedro Paulo Araújo"),
    "team_size": "mais de 40",
    "structure": "sede própria no Ed. Mesbla, com 10 salas",
    "email": "dentalaraujo@yahoo.com.br",
    "slogan": "Há 50 anos no mercado. Pioneira na prótese dentária.",
    # Endereço (formatos usados no site; os dados são os mesmos).
    "address": {
        "street": "Av. Afonso Pena, 262",
        "floor": "16º andar",
        "room": "sala 1602",
        "room_title": "Sala 1602",
        "building": "Ed. Mesbla",
        "building_full": "Edifício Mesbla",
        "district": "Centro",
        "city": "Belo Horizonte",
        "region": "MG",
        "postal": "30130-923",
        "country": "BR",
        # Linha única (llms, JSON-LD, constante ADDR legada)
        "full": (
            "Av. Afonso Pena, 262 – 16º andar, Sala 1602, Ed. Mesbla – "
            "Centro – Belo Horizonte/MG – 30130-923"
        ),
        "street_schema": "Av. Afonso Pena, 262, 16º andar, Sala 1602 – Edifício Mesbla",
        "geo": {"latitude": -19.9162258, "longitude": -43.9407838},
    },
    "phones": {
        "pedidos": [
            {
                "label": "Atendimento e orçamentos",
                "display": "(31) 3271-9766",
                "e164": "553132719766",
                "tel": "tel:+553132719766",
                "track": "phone",
            },
            {
                "label": "Atendimento e orçamentos",
                "display": "(31) 3271-9688",
                "e164": "553132719688",
                "tel": "tel:+553132719688",
                "track": "phone",
            },
        ],
        "financeiro": [
            {
                "label": "Financeiro",
                "display": "(31) 3212-1384",
                "e164": "553132121384",
                "tel": "tel:+553132121384",
                "track": "phone_fin",
            },
        ],
    },
    "whatsapp": {
        "pedidos": {
            "label": "WhatsApp – atendimento e orçamentos",
            "display": "(31) 98652-1387",
            "e164": "5531986521387",
            "track": "whatsapp",
        },
        "financeiro": {
            "label": "Financeiro (WhatsApp)",
            "display": "(31) 98652-1201",
            "e164": "5531986521201",
            "track": "whatsapp_fin",
        },
    },
    "hours": {
        "dias": "Seg. a sex.",
        "abre": "08:00",
        "fecha": "18:00",
        "texto_curto": "Seg. a sex. · 08:00–18:00",
        "texto_longo": "Seg. a sex., 08:00 às 18:00",
        "texto_frase": "de segunda a sexta, das 08:00 às 18:00",
        "schema": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ],
                "opens": "08:00",
                "closes": "18:00",
            },
        ],
    },
    "social": {
        "instagram": "https://www.instagram.com/labdentalaraujo/",
        "facebook": "https://www.facebook.com/laboratoriodentalaraujo",
        "maps": "https://maps.app.goo.gl/D3UgE8PvNiXERDP37",
    },
    "credit": {
        "label": "Desenvolvido por",
        "name": "gandra.tech",
        "url": "https://www.gandra.tech/",
    },
}


def wa_url(e164: str | None = None, text: str | None = None) -> str:
    """Link wa.me; se text for passado, deve ser codificado pelo chamador (quote)."""
    num = e164 or LAB["whatsapp"]["pedidos"]["e164"]  # type: ignore[index]
    if text is None:
        return f"https://wa.me/{num}"
    return f"https://wa.me/{num}?text={text}"


def phone_display_pedidos() -> str:
    pedidos = LAB["phones"]["pedidos"]  # type: ignore[index]
    return " · ".join(p["display"] for p in pedidos)  # type: ignore[index]
