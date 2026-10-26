#!/usr/bin/env python3
"""Gera o modelo de requisição para laboratório de prótese (PDF A4, 1 página), publicado em
/assets/docs/requisicao-laboratorio-de-protese.pdf e citado no artigo do blog de mesmo tema.
Uso:  python3 tools/requisicao_pdf.py      (depois rode python3 _build/build.py)
Requer:  pip install playwright  (Chromium do Playwright). Sem preços: o modelo só organiza o pedido."""
import asyncio, base64, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST = ROOT / '_build/static/assets/docs/requisicao-laboratorio-de-protese.pdf'
FONT = ROOT / '_build/static/assets/fonts'
def f64(n): return base64.b64encode((FONT / n).read_bytes()).decode()

def boxes(items): return ''.join(f'<span class="ck"><i></i>{t}</span>' for t in items)
def teeth(a): return ''.join(f'<span class="t">{n}</span>' for n in a)
SUP = teeth([18,17,16,15,14,13,12,11]) + '<b></b>' + teeth([21,22,23,24,25,26,27,28])
INF = teeth([48,47,46,45,44,43,42,41]) + '<b></b>' + teeth([31,32,33,34,35,36,37,38])

CSS = f'''@font-face{{font-family:Plex;src:url(data:font/woff2;base64,{f64("plex-sans.woff2")}) format("woff2");font-weight:100 900}}
@font-face{{font-family:News;src:url(data:font/woff2;base64,{f64("newsreader-500.woff2")}) format("woff2")}}
@page{{size:A4;margin:11mm 12mm}}
*{{box-sizing:border-box}}
body{{font:9.4pt/1.4 Plex,Arial,sans-serif;color:#1B2433;margin:0}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #1B2433;padding-bottom:5px;margin-bottom:7px}}
h1{{font:500 17pt/1.1 News,Georgia,serif;margin:0}}
header p{{margin:0;text-align:right;font-size:7.6pt;color:#3F4A5A}}
section{{border:1px solid #9AA3AF;border-radius:3px;padding:7px 9px 8px;margin-bottom:9px}}
h2{{font-size:7.8pt;letter-spacing:.08em;text-transform:uppercase;margin:0 0 4px;color:#3F4A5A}}
.row{{display:flex;gap:10px;margin:8px 0}}
.f{{flex:1;display:flex;gap:4px;align-items:flex-end;white-space:nowrap}}
.f u{{flex:1;border-bottom:1px solid #6B7480;height:14px;text-decoration:none}}
.ck{{display:inline-flex;align-items:center;gap:3px;margin:4px 11px 4px 0;white-space:nowrap}}
.ck i{{width:9px;height:9px;border:1px solid #1B2433;display:inline-block}}
.odo{{display:flex;flex-direction:column;gap:3px;align-items:center;margin:3px 0}}
.odo div{{display:flex;gap:2px}}
.t{{width:28px;height:21px;border:1px solid #6B7480;font-size:7pt;display:flex;align-items:center;justify-content:center}}
.odo b{{width:8px;border-left:1px dashed #6B7480;margin:0 3px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.lines{{height:100px;background:repeating-linear-gradient(transparent 0 19px,#B8BEC6 19px 20px)}}
.draw{{height:100px;border:1px dashed #9AA3AF}}
footer{{display:flex;justify-content:space-between;gap:12px;margin-top:6px;font-size:7.4pt;color:#3F4A5A}}
footer .sig{{flex:1;border-top:1px solid #1B2433;padding-top:2px;text-align:center;margin-top:34px}}
.hint{{font-size:7.2pt;color:#5A6472}}'''

HTML = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Requisição para laboratório de prótese</title><style>{CSS}</style></head><body>
<header><div><h1>Requisição para laboratório de prótese</h1><span class="hint">Modelo para impressão · preencha à mão e envie junto com o caso</span></div>
<p><b>Laboratório Dental Araújo</b><br>Av. Afonso Pena, 262, 16º andar, sala 1602 · Ed. Mesbla<br>Centro · Belo Horizonte/MG · CEP 30130-923<br>(31) 3271-9766 · WhatsApp (31) 98652-1387</p></header>

<section><h2>1. Dentista e paciente</h2>
<div class="row"><span class="f">Dentista <u></u></span><span class="f" style="flex:.45">CRO <u></u></span></div>
<div class="row"><span class="f">Telefone/WhatsApp <u></u></span><span class="f">E-mail <u></u></span></div>
<div class="row"><span class="f">Endereço de entrega <u></u></span></div>
<div class="row"><span class="f">Paciente (nome ou código) <u></u></span><span class="f" style="flex:.5">Data de envio <u></u></span></div>
<div class="row"><span class="f" style="flex:.6">Próxima consulta <u></u></span><span class="ck"><i></i>Urgência (acréscimo de 30% por etapa)</span></div>
</section>

<section><h2>2. Trabalho e material</h2>
<div>{boxes(["Coroa","Ponte","Faceta","Restaurado","Núcleo","Barra de protocolo","Barra clips / overdenture","Guia cirúrgico","PPR Roach","Parcial Flexite","Parcial em acrílico","Prótese total","Placa","Ortodontia","Provisório"])}<span class="f" style="display:inline-flex;width:150px">Outro <u></u></span></div>
<div style="margin-top:3px"><b>Material:</b> {boxes(["Zircônia","E-Max","Metalocerâmica","Metálica","Resina Ceramage","Resina popular","Acrílico","Flexite"])}<span class="f" style="display:inline-flex;width:150px">Liga / outro <u></u></span></div>
</section>

<section><h2>3. Elementos e cor</h2>
<div class="odo"><div>{SUP}</div><div>{INF}</div></div>
<p class="hint" style="margin:0 0 3px;text-align:center">Marque os elementos. Em pontes, indique pilares (P) e pônticos (X).</p>
<div class="row"><span class="f">Cor <u></u></span><span class="f">Escala usada <u></u></span><span class="f">Cor do remanescente <u></u></span><span class="ck"><i></i>Fotos com escala enviadas</span></div>
</section>

<section><h2>4. Etapa e implantes</h2>
<div><b>Etapa:</b> {boxes(["Modelo / moldeira individual","Base de prova / plano de cera","Prova da armação","Montagem dos dentes","Prova da barra","Finalização","Conserto"])}</div>
<div class="row"><span class="f">Sistema de implante <u></u></span><span class="f">Plataforma <u></u></span></div>
<div>Componentes enviados: {boxes(["Análogos","Transferentes","Minipilares","Cilindros"])}<span class="f" style="display:inline-flex;width:150px">Outros <u></u></span></div>
</section>

<section><h2>5. O que vai na caixa</h2>
<div>{boxes(["Moldagem","Modelo","Antagonista","Registro de mordida","Componentes de implante","Peça para prova","Fotos"])}</div>
</section>

<div class="two">
<section><h2>6. Observações (tudo por escrito)</h2><div class="lines"></div></section>
<section><h2>7. Desenho / planejamento</h2><div class="draw"></div></section>
</div>

<footer><span>Recados e informações extras devem vir por escrito nesta folha.<br>Prazo médio de 7 dias úteis por etapa, podendo variar conforme a demanda.</span>
<span class="sig">Assinatura e carimbo do cirurgião-dentista (CRO)</span></footer>
</body></html>'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(HTML, wait_until='load')
        await pg.pdf(path=str(DST), format='A4', print_background=True, prefer_css_page_size=True)
        await b.close()
    print('ok', DST.relative_to(ROOT))
asyncio.run(main())
