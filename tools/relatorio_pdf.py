#!/usr/bin/env python3
"""Gera o PDF de um relatório em Markdown (ex.: docs/AUDITORIA-2026-10-26.md) com o Chromium do Playwright.
Uso:  python3 tools/relatorio_pdf.py docs/AUDITORIA-2026-10-26.md saida.pdf
Requer:  pip install markdown playwright"""
import sys, asyncio, pathlib, markdown
from playwright.async_api import async_playwright

src, dst = pathlib.Path(sys.argv[1]), sys.argv[2]
body = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables', 'fenced_code', 'sane_lists'])
CSS = '''body{font:10.2pt/1.5 "DejaVu Sans",Arial,sans-serif;color:#13233A}
h1{font-size:20pt;color:#0B3B74;border-bottom:3px solid #0B3B74;padding-bottom:6px;margin-top:0}
h2{font-size:14pt;color:#0B3B74;margin-top:22px;border-bottom:1px solid #C9D5E4;padding-bottom:3px;page-break-after:avoid}
h3{font-size:11.5pt;color:#0B3B74;page-break-after:avoid}
table{border-collapse:collapse;width:100%;margin:8px 0 12px;font-size:8.6pt}
tr{page-break-inside:avoid}
th{background:#0B3B74;color:#fff;text-align:left;padding:5px 6px}
td{border-bottom:1px solid #D8E0EA;padding:4px 6px;vertical-align:top}
tr:nth-child(even) td{background:#F3F6FA}
code{font:8.6pt "DejaVu Sans Mono",monospace;background:#EEF2F7;padding:0 3px;border-radius:3px;word-break:break-word}
hr{border:0;border-top:1px solid #C9D5E4;margin:16px 0}
a{color:#0B5CB8}'''
title = src.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
html = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
FOOT = f'<div style="font-size:7pt;width:100%;text-align:center;color:#6B7A90">{title} · Laboratório Dental Araújo · página <span class="pageNumber"></span> de <span class="totalPages"></span></div>'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(html, wait_until='load')
        await pg.pdf(path=dst, format='A4', print_background=True, display_header_footer=True,
                     header_template='<span></span>', footer_template=FOOT,
                     margin={'top': '16mm', 'bottom': '18mm', 'left': '14mm', 'right': '14mm'})
        await b.close()
    print('ok', dst)
asyncio.run(main())
