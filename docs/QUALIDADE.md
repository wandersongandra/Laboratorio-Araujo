# Qualidade — ferramentas, comandos e resultados

Última verificação completa: 26/10/2026 (auditoria; ver [AUDITORIA-2026-10-26.md](AUDITORIA-2026-10-26.md)), antes e depois do deploy
(`https://brilliant-cat-c5b6e9.netlify.app`).

## Como rodar

```bash
npm install                      # uma vez (PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 se já tiver Chromium)
pip install -r requirements-dev.txt && python3 -m playwright install chromium
npm run build                    # gera dist/ (CSS/JS minificados, _headers, sitemap…)
npm run serve &                  # servidor local em :8766 com os mesmos cabeçalhos/CSP do Netlify
npm run qa                       # build + lint (+pyflakes) + SEO + "sem preços" + rotas + páginas + interação
npm run qa:live                  # depois do deploy: rotas/301/404/cabeçalhos/externos, preços e console NO AR
npm run a11y                     # axe-core em todas as páginas (1366 e 390 px)
npm run links                    # linkinator (links internos)
```

| Comando | Ferramenta | O que verifica |
|---|---|---|
| `npm run lint:html` | html-validate 9 (`html-validate:recommended` + regras em `.htmlvalidate.json`) | HTML válido e acessível no `dist/`; proíbe `style=""`; título ≤ 60 |
| `npm run lint:css` | stylelint 16 + `stylelint-config-standard` | Sintaxe, duplicatas, propriedades inválidas |
| `npm run lint:js` | ESLint 9 (`eslint.config.mjs`) | Erros de JS; proíbe `innerHTML`, `outerHTML`, `document.write`, `eval` |
| `python3 -m pyflakes _build tools` | pyflakes | Erros no gerador e nos scripts |
| `python3 tools/qa_seo.py` | próprio | Título/descrição por página e duplicados, um `<h1>`, hierarquia de títulos, JSON-LD válido, links e imagens internos inexistentes, `alt` ausente |
| `python3 tools/qa_sem_precos.py [--live URL]` | próprio | `dist/` sem "R$", "preço", "tabela-de-precos", ".pdf" nem `Offer`/`price` no JSON-LD (fora das exceções do script); com `--live`, `/tabela-de-precos/` → 301 `/contato/` e PDF antigo ≠ 200 |
| `python3 tools/qa_paginas.py [URL]` | próprio + Playwright | Todas as URLs do sitemap + uma 404 em 1440, 1366 e 390 px: status HTTP, erros de JS, erros/avisos de console (inclusive CSP), rolagem horizontal |
| `python3 tools/qa_rotas.py [URL] [--externos]` | próprio (só biblioteca padrão) | robots e sitemap (só URLs 200, `lastmod` válido); em cada página: 200 direto, canonical = og:url = URL, 1 `<h1>`, títulos/descrições únicos, `target=_blank` com `noopener`, JSON-LD válido; todos os links internos, imagens, `srcset`, ícones do manifest, URLs do JSON-LD e dos `llms*.txt` respondem 200 sem redirecionamento; âncoras `#id` existem; `tel:`/`mailto:`/`wa.me` bem formados; páginas fora do sitemap; 404 real com `noindex`; arquivos internos inacessíveis. **No ar** (URL https): sem barra, MAIÚSCULAS e `/index.html` → 301 de um salto; regras do `_redirects`; cabeçalhos de segurança. `--externos` testa os links externos |
| `python3 tools/qa_interacao.py [URL]` | próprio + Playwright | Cada `#id` linkado ou dentro de acordeão abre o `<details>` e fica na tela; sem JavaScript e com movimento reduzido nada do conteúdo fica invisível; sem animação infinita no modo reduzido; menu móvel por teclado (Tab, Enter, Esc, foco de volta) |
| `npm run a11y` | axe-core (WCAG 2.0/2.1/2.2 A e AA + boas práticas) | 21 páginas (20 + 404) × 2 larguras, mais o menu mobile aberto |
| `npm run links` | linkinator 6 | Links quebrados |
| `npx lighthouse@12` | Lighthouse | Desempenho, acessibilidade, boas práticas, SEO |
| `npm audit` | npm | Vulnerabilidades nas dependências de desenvolvimento |

## Resultados da auditoria (26/10/2026)

Relatório completo, com metodologia, achados e pendências: [AUDITORIA-2026-10-26.md](AUDITORIA-2026-10-26.md).
Resumo: `npm run qa` e `npm run qa:live` com 0 falhas, axe 0 violações, linkinator 74 links OK
(inclui o crédito gandra.tech), schema.org 0 erros/0 avisos nas 20 páginas, Observatory A+ (130),
CLS da página de serviço 0,022 → 0.

## Resultados da versão enxuta (26/10/2026)

| Verificação | Resultado |
|---|---|
| `npm run qa` (build, html-validate, stylelint, ESLint, qa_seo, qa_sem_precos, qa_paginas) | **0 erros / 0 falhas** |
| pyflakes | 0 avisos |
| axe-core | **0 violações** em 21 páginas × 2 larguras |
| linkinator | 73 links OK |
| qa_paginas e qa_sem_precos **no ar** | 0 falhas; nenhum preço; `/tabela-de-precos/` → 301 `/contato/`; PDF antigo → 404 |
| Sem JS / movimento reduzido | números com o valor final, faixa de fotos com rolagem lateral, barra da linha do tempo cheia, nada animado |
| Antes e depois | testado localmente com par fictício (arrastar e teclado: `--x` 50% → 25%); **não publicado** |

Palavras visíveis (`main.innerText`, 1440 px; texto de acordeão fechado não conta):

| Página | Antes | Depois |
|---|---|---|
| Home | 1.298 | 536 |
| Zircônia e E-Max | 928 | 449 |
| Sobre | 570 | 410 |
| Envio para todo o Brasil | 544 | 353 |

Altura da home: 10.365 → 7.108 px (desktop) e 16.772 → 10.926 px (celular).

Lighthouse 12 **no ar** (26/10/2026):

| Página | Perfil | Desempenho | Acessib. | Boas práticas | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|---|
| Home | mobile | 100 | 100 | 100 | 100 | 1,9 s | 0,001 | 0 ms |
| Home | desktop | 100 | 100 | 100 | 100 | 0,5 s | 0,001 | 0 ms |
| Zircônia e E-Max | mobile | 100 | 100 | 100 | 100 | 1,4 s | 0,022 | 0 ms |
| Zircônia e E-Max | desktop | 100 | 100 | 100 | 100 | 0,5 s | 0,001 | 0 ms |

No servidor local (sem CDN/compressão) a home mobile marca 93 e o serviço mobile 97, como a versão
anterior (94). O CLS de 0,022 no serviço vem do cabeçalho da página interna (troca de fonte) e já
existia.

Capturas: `screenshots/antes-v2-*.png` e `screenshots/depois-v2-*.png` (home e zircônia, 1440 e
390 px); animações em `screenshots/animacoes-v2.mp4` e `.gif`; teste local do antes/depois em
`screenshots/componente-antes-depois-TESTE-local.png` (par fictício, não publicado).

## Resultados (24/10/2026)

| Verificação | Resultado |
|---|---|
| html-validate (21 arquivos) | **0 erros** (eram 215: `aria-label` em `div`, botão sem `type`, telefone quebrando linha, `label` com dois controles, `role=region`) |
| stylelint | **0 erros** |
| ESLint | **0 erros** |
| pyflakes | **0 avisos** |
| axe-core | **0 violações** em 21 páginas × 2 larguras (corrigido: regiões sem rótulo na barra de contato e no botão do WhatsApp, cabeçalho de tabela vazio, contraste do "404") |
| qa_paginas, local e **no ar** | **0 falhas** em 63 combinações (21 URLs × 3 larguras): sem erro de JS, sem erro de CSP, sem rolagem horizontal; as 20 URLs do sitemap com 200 e `/nao-existe/` com 404 |
| qa_seo | 0 problemas, nenhum título ou descrição duplicado; títulos de 40 a 53 caracteres; documentos legais com `WebPage` + `BreadcrumbList` |
| qa_sem_precos, local e **no ar** | 0 ocorrências indevidas em `dist/`; `/tabela-de-precos/` e `/tabela-de-precos` → **301** `/contato/`; `/assets/docs/tabela-precos-2026.pdf` → **404** |
| linkinator | 73 links internos OK; externos OK. O Facebook responde 400 a robôs, mas com navegador real abre normalmente |
| npm audit | 0 vulnerabilidades |
| Contraste (tokens) | texto 15,7:1; secundário 6,0:1; links 7,2:1; branco no azul-marinho 15,4:1 (mínimo AA: 4,5:1) |
| Mapa sob a CSP | carrega no ar (iframe do Google Maps) sem erro de console |
| Segurança | ver [SEGURANCA.md](SEGURANCA.md): Observatory A+ |

### Lighthouse — antes × depois

"Antes" = site no ar antes da revisão de design/segurança; "depois" = no ar após o deploy de 24/10/2026.
Lighthouse 12, Chromium headless, perfil padrão (mobile: Moto G com 4G lento simulado).

| Página | Perfil | Desempenho | Acessib. | Boas práticas | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|---|
| Política de privacidade | mobile | 99 | 100 | 100 | 100 | 2,1 s | 0 | 0 ms |
| Política de privacidade | desktop | 100 | 100 | 100 | 100 | 0,5 s | 0 | 0 ms |
| Termos de uso | mobile | 99 | 100 | 100 | 100 | 2,1 s | 0 | 0 ms |
| Termos de uso | desktop | 100 | 100 | 100 | 100 | 0,5 s | 0 | 0 ms |
| Home | mobile — antes | 82 | 100 | 100 | 100 | 3,3 s | — | — |
| Home | mobile — **depois** | **100** | 100 | 100 | 100 | 1,9 s | 0,001 | 0 ms |
| Home | desktop — antes | 98 | 100 | 100 | 100 | — | — | — |
| Home | desktop — **depois** | **100** | 100 | 100 | 100 | 0,5 s | 0,001 | 0 ms |
| Zircônia e E-Max | mobile — antes | 86 | 100 | 100 | 100 | — | — | — |
| Zircônia e E-Max | mobile — **depois** | **100** | 100 | 100 | 100 | 1,8 s | 0,02 | 0 ms |
| Zircônia e E-Max | desktop — antes | 98 | 100 | 100 | 100 | — | — | — |
| Zircônia e E-Max | desktop — **depois** | **100** | 100 | 100 | 100 | 0,5 s | 0,001 | 0 ms |

Os documentos legais foram medidos no servidor local (24/10/2026). As notas variam alguns pontos entre execuções (rede e CPU). No servidor local, sem CDN, o
desempenho mobile ficou em 94–95.

### O que mais pesou no desempenho

- Saída do GSAP e do Lenis: menos JavaScript e nenhuma rolagem "sequestrada".
- CSS e JS minificados no build (40 KB e 9,6 KB, contra 43 KB e 12,7 KB dos fontes legíveis),
  com cache imutável de 1 ano e `?v=hash`.
- Foto do topo com `preload` + `fetchpriority="high"` e WebP de 640/1200 px; demais fotos com
  `loading="lazy"` e dimensões declaradas (CLS ≈ 0).
- Quatro arquivos de fonte auto-hospedados (WOFF2), os dois usados acima da dobra com `preload`,
  todos com `font-display: swap`, e fontes de fallback
  ajustadas (`size-adjust`) para o texto não pular quando a fonte carrega.
- CSS morto removido (`.mono`, `.ruler--h`, `.pcat--teaser` e outras).

## Revisão visual

Capturas de página inteira (1440 e 390 px) de todas as páginas, menu mobile aberto com submenu,
submenu no desktop, 404, blog e mapa no contato, revisadas uma a uma. Problema achado e corrigido
nesta revisão: no celular, o menu aberto ficava cortado em 53 px de altura, porque o
`backdrop-filter` do cabeçalho virava o bloco de contenção do menu `position: fixed`. O cabeçalho
mobile agora usa fundo sólido.
Capturas finais: `screenshots/` (desktop, mobile, serviço, antes/depois da home) e, após a retirada
dos preços, `politica-de-privacidade-{d,m}.png`, `termos-de-uso-{d,m}.png`,
`servico-zirconia-{d,m}.png`, `home-{d,m}.png` e `contato-{d,m}.png`.

## Fotos reais (26/10/2026, deploy 6adf9553ff966f268eb1ca5d)

| Teste | Resultado |
|---|---|
| `npm run qa` (build, html-validate, stylelint, eslint, pyflakes, SEO, sem preços, rotas, páginas, interação) | 0 falhas, 0 avisos |
| `npm run a11y` (axe, 25 páginas × desktop/celular) | 0 violações; lightbox aberto também 0 |
| linkinator local (recursivo) | 477 links, 0 quebrados |
| `npm run qa:live` | 0 falhas; 2 avisos conhecidos (PubMed 203, DOI Wiley 403) |
| Lighthouse no ar: home, /servicos/protese-total/, /trabalhos/ (celular e desktop) | 100/100/100/100 nas 6 medições; CLS 0 |
| Imagens em `dist/` com EXIF/XMP | 0 |
