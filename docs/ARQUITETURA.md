# Arquitetura do site — Laboratório Dental Araújo

Atualizado em 24/10/2026. Site: https://brilliant-cat-c5b6e9.netlify.app
(gerado por `python3 _build/build.py` → `dist/`). Uso diário: ver o [README](../README.md).

## 1. Visão geral

| Camada | O que é | Onde |
|---|---|---|
| Conteúdo | Textos, FAQ, itens de serviço, condições, artigos, documentos legais (dados Python) | `_build/content/*.py` |
| Modelos | Funções Python com f-strings que devolvem HTML | `_build/build.py` (seções 5–8) |
| Estilo | Uma folha de estilos com tokens de design | `_build/static/assets/css/style.css` |
| Comportamento | Um script sem dependências, carregado com `defer` | `_build/static/assets/js/main.js` |
| Saída | HTML estático + assets + arquivos técnicos | `dist/` |
| Hospedagem | Netlify (CDN, HTTPS, URLs limpas, `_headers`, `_redirects`) | site `brilliant-cat-c5b6e9` |

Não há servidor, banco de dados, formulário, cookie nem script de terceiros. O único conteúdo
externo é o mapa do Google, que só é carregado quando o visitante clica em "Carregar mapa" (contato).

## 2. Mapa de páginas

```
/                                        Home (prioridade 1.0)
├── /servicos/                           Hub de serviços (0.9)
│   ├── /servicos/protese-sobre-implante/
│   ├── /servicos/zirconia-e-max/
│   ├── /servicos/metaloceramica/
│   ├── /servicos/protese-parcial-removivel-ppr/
│   ├── /servicos/protese-total/
│   ├── /servicos/protese-flexivel-flexite/
│   ├── /servicos/resinas-e-provisorios/
│   └── /servicos/placas-de-bruxismo-e-ortodontia/        (8 páginas de serviço, 0.9)
├── /sobre/                              História, estrutura, condições de trabalho (0.7)
├── /trabalhos/                          Galeria de fotos reais por categoria, com ampliação (0.6)
├── /envio-para-todo-brasil/             Coleta em MG, envio de outros estados (0.7)
├── /perguntas-frequentes/               5 grupos de perguntas (0.7)
├── /contato/                            Endereço, telefones, mapa sob demanda, #orcamento (0.8)
├── /blog/                               Índice do blog (0.6)
│   ├── /blog/metaloceramica-ou-zirconia/              (26/10/2026)
│   ├── /blog/ppr-ou-protese-flexivel/                 (26/10/2026)
│   ├── /blog/requisicao-para-laboratorio-de-protese/  (26/10/2026, com o PDF /assets/docs/requisicao-laboratorio-de-protese.pdf)
│   ├── /blog/zirconia-ou-e-max-qual-indicar/
│   ├── /blog/como-enviar-um-caso-para-o-laboratorio-de-protese/
│   └── /blog/barra-de-protocolo-etapas-e-prazos/
├── /politica-de-privacidade/            Política de privacidade, LGPD (0.3)
└── /termos-de-uso/                      Termos de uso (0.3)
/404.html                                Página de erro (noindex, fora do sitemap)

Redirecionamentos (dist/_redirects): /tabela-de-precos/ → /contato/ (301). Página removida em 24/10/2026.
```

Ligações internas: o menu principal leva a Serviços (com submenu das 8 páginas), Envio, Sobre,
FAQ, Blog e Contato; cada serviço aponta para serviços relacionados, para `/contato/` e para o
WhatsApp com um pedido de orçamento já preenchido; cada artigo aponta para o serviço comercial do
mesmo assunto. O rodapé de todas as páginas tem os links "Política de privacidade" e "Termos de uso".

## 3. Convenções de URL

- Minúsculas, sem acento, palavras separadas por hífen, **sempre com barra no final**
  (`/servicos/protese-total/`). O Netlify serve `pasta/index.html` nessa URL.
- Dois níveis no máximo: `/<seção>/<página>/`. Serviços em `/servicos/`, artigos em `/blog/`.
- O slug contém a palavra-chave principal da página (`protese-parcial-removivel-ppr`).
- Âncoras úteis: `/contato/#orcamento` (como pedir orçamento), `#itens` nas páginas de serviço,
  e uma âncora por seção nos documentos legais (ex. `/politica-de-privacidade/#direitos`).
- Arquivos: `assets/img/foto/<nome>-640.webp` e `-1200.webp`; CSS e JS com `?v=<hash>`
  (cache de 1 ano, o hash muda a cada alteração).
- Variantes resolvem num único 301 para a URL canônica: sem barra (`/sobre` → `/sobre/`) e
  MAIÚSCULAS (`/SOBRE/` → `/sobre/`) pelo Netlify; `/sobre/index.html` → `/sobre/` pelas regras
  geradas por `redirects_index()`. `/404.html` e `/404` respondem 404. http → https é automático
  (com HSTS). Teste: `python3 tools/qa_rotas.py` (no ar).
- **Não mude URLs publicadas.** Se for inevitável, acrescente um 301 na constante `REDIRECTS`
  do `build.py` (gravada em `dist/_redirects`), ex.: `/antiga/  /nova/  301`.

## 4. Sistema de modelos

`build.py` é organizado em seções numeradas (ver o sumário no topo do arquivo):

1. **Configuração:** `BASE` (domínio), `TODAY`, telefone de WhatsApp `WA`, endereço, redes.
2. **Minificação:** `minify_css` / `minify_js` (conservadores; só retiram comentários e espaços).
3. **Segurança:** o único script inline (`INLINE_JS`), o hash dele, a `CSP` e `headers_file()`.
4. **Imagens:** `img()` escreve `<img>` com `srcset` 640/1200, `width`/`height` reais e
   `loading="lazy"` (exceto a foto do topo, que recebe `preload` + `fetchpriority="high"`).
5. **Estrutura comum:** `header()`, `footer()`, botão de WhatsApp e `page()`, que monta o `<head>`
   (title, description, canonical, robots, Open Graph, Twitter, geo, ícones, JSON-LD) e o corpo.
6. **Blocos:** `phero()` (cabeçalho de página interna), `shead()` (cabeçalho de seção numerado
   "01 / Rótulo"), `pcard()` (itens de uma linha de serviço, sem preço), `card()`/`svc_card()`/`post_card()`,
   `related()`, `cta_band()`, `faq_block()`/`faq_section()`, `idx_list()` (índice numerado, no hub de serviços), `facts_block()`, `aside_card()`, `fig()` (foto + legenda),
   `resumo()` (tópicos visíveis), `accordion()` (seções `<h2>` recolhidas em `<details>`), `svc_tiles()` (cartões da home), `faixa()` (faixa de fotos),
   `antes_depois()` (desligado enquanto `ANTES_DEPOIS` estiver vazio), `photo_slot()`
   (espaço reservado para foto real), `contact_section()`.
7. **JSON-LD:** `business()`, `website()`, `webpage()`, `crumbs_ld()`, `faq_ld()`. Nenhum
   nó tem `Offer`, `price` ou `priceRange`: o site não publica valores.
8. **Páginas:** `build_home()`, `build_hub()`, `build_service(s)`,
   `build_sobre()`, `build_envio()`, `build_faq()`, `build_contato()`, `build_blog()`,
   `build_legal(doc, outro)`, `build_404()`.
   Todas terminam em `out(caminho, html, prioridade)`, que grava o arquivo, aplica `nobreak()`
   (E-Max não quebra no hífen) e `telclass()` (telefones não quebram) e registra a URL no sitemap.
9. **Arquivos técnicos:** `build_meta()` (sitemap, robots, llms.txt, llms-full.txt), `REDIRECTS`
   (→ `_redirects`) e `main()`.

Regras que o build garante (e que quebram o build se violadas): título com até 60 caracteres
(`assert` em `page()`); o HTML não tem `style=""` nem `<style>` (a CSP proíbe); o JSON-LD é gerado
com `json.dumps` (nunca à mão).

### Front-end

- **CSS** (`style.css`): sumário no topo, tokens em `:root` (cores, fontes, escala tipográfica
  fluida com `clamp()`), seções numeradas 0–12, três pontos de quebra (1180, 1024 e 760 px).
- **JS** (`main.js`, sem bibliotecas): módulos independentes (1 rastreamento de cliques, 2 âncoras,
  3 cabeçalho e menu, 4 revelações ao rolar, 5 miniaturas do índice, 6 mapa sob demanda,
  7 contadores, 8 botão Pausar da faixa de fotos, 9 barra de progresso da linha do tempo,
  10 acordeão aberto por link `#âncora` e tudo aberto na impressão, 11 antes/depois). Cada módulo só
  roda se o elemento existir na página. Sem JS, o site funciona: o conteúdo aparece completo
  (números com o valor final, faixa de fotos com rolagem lateral, linha do tempo preenchida).
- **Movimento** (versão enxuta, 26/10/2026), tudo em CSS/JS próprio, ativado pela classe `js` no
  `<html>` e só com `prefers-reduced-motion: no-preference`:
  - revelações discretas (opacidade/translação curta) e fotos reveladas por máscara (`clip-path`);
  - contadores 0 → valor real (50 anos, 35+, 400 m²) ao entrar na tela; largura fixa por número de
    dígitos (`.cnt.n2/.n3`, algarismos tabulares), então a contagem não desloca nada (CLS ≈ 0);
  - faixa horizontal de fotos em loop lento; pausa com mouse, foco ou botão "Pausar"
    (`aria-pressed`); a cópia que fecha o loop tem `aria-hidden` e `alt=""`;
  - linha do tempo "Como enviar um caso" com barra ocre que acompanha a rolagem
    (`--p` via CSSOM, permitido pela CSP) e ícones que acendem por etapa;
  - microinterações: cartões sobem 3 px com sombra curta, foto amplia 4%, seta avança; botões
    afundam no clique (`scale(.97)`); setas dos links deslizam;
  - acordeões com altura animada onde há suporte (`interpolate-size` + `::details-content`);
    nos demais navegadores abrem sem animação.
  Com `prefers-reduced-motion: reduce`, nada se move: números já finais, faixa vira rolagem lateral,
  barra cheia.
- **Páginas longas:** serviços, /sobre/ e /envio-para-todo-brasil/ abrem com "Pontos principais"
  (3–4 tópicos) e uma figura; o restante fica em acordeões `<details class="acc">` com o `<h2>`
  dentro do `<summary>`, então o texto completo e a hierarquia de títulos continuam no HTML.

## 5. Estratégia de SEO

**On-page (todas as páginas):**
- `<title>` único com até 60 caracteres (hoje 40–53) e `meta description` única (≈ 130–165 caracteres; a 404 tem uma curta).
- Um único `<h1>` com o termo e a cidade; hierarquia de títulos sem saltos (verificado por
  `tools/qa_seo.py`).
- `canonical` absoluto, Open Graph + Twitter Card (imagem 1200×630), `meta geo` (BR-MG).
- Migalhas de pão visíveis + `BreadcrumbList` em todas as páginas internas.
- Páginas de serviço com ≈ 900–1.100 palavras no `<main>`, H2 em forma de pergunta respondida logo no primeiro
  parágrafo, lista dos itens da linha (sem valores) e chamada "Solicitar orçamento".
- Imagens com `alt` descritivo, WebP responsivo, dimensões declaradas (CLS ≈ 0), lazy-load.
- Velocidade: CSS e JS próprios e pequenos (≈ 40 KB e 10 KB), fontes auto-hospedadas com
  `preload` e `font-display: swap`, nenhum script de terceiros (ver Lighthouse em QUALIDADE.md).

**Mapa de palavras-chave** (uma intenção principal por URL, sem canibalização). A versão completa,
com fontes, evidências do autocompletar, plano de conteúdo e pendências, está em
[PALAVRAS-CHAVE.md](PALAVRAS-CHAVE.md) (revisão de 26/10/2026). Resumo:

| URL | Palavra-chave principal | Secundárias |
|---|---|---|
| / | laboratório de prótese dentária BH | laboratório de prótese Belo Horizonte, laboratório dental BH, desde 1976 |
| /servicos/ | serviços de laboratório de prótese | tipos de prótese dentária, laboratório de prótese completo |
| /servicos/protese-sobre-implante/ | prótese protocolo sobre implante | barra de protocolo, overdenture com barra clip, guia cirúrgico para implante, coroa sobre implante |
| /servicos/zirconia-e-max/ | coroa de zircônia | coroa e faceta em E-Max, ponte fixa de zircônia, dissilicato de lítio, metal free |
| /servicos/metaloceramica/ | coroa metalocerâmica | ponte metalocerâmica, núcleo metálico fundido, metalocerâmica sobre implante, coroa veneer |
| /servicos/protese-parcial-removivel-ppr/ | PPR prótese parcial removível | armação metálica de PPR, PPR Roach, grampo Roach |
| /servicos/protese-total/ | prótese total removível | PTR, prótese total caracterizada, palato incolor, STG ("dentadura" excluído: termo de paciente) |
| /servicos/protese-flexivel-flexite/ | prótese flexível | Flexite unilateral, parcial provisória em acrílico, prótese sem grampo metálico |
| /servicos/resinas-e-provisorios/ | coroa de resina Ceramage | coroa provisória laboratório, ponte com fibra, restaurado em resina, provisório em acrílico |
| /servicos/placas-de-bruxismo-e-ortodontia/ | placa de bruxismo (laboratório) | placa miorrelaxante, placa de clareamento, protetor bucal personalizado, contenção ortodôntica, aparelho anti-ronco |
| /sobre/ | Laboratório Dental Araújo | história, 50 anos, pioneiro em BH, equipe |
| /trabalhos/ | fotos de trabalhos de laboratório de prótese | fotos de prótese, trabalhos do laboratório |
| /envio-para-todo-brasil/ | laboratório de prótese que atende todo o Brasil | coleta em BH, Grande BH (Contagem, Betim) e MG, envio pelos Correios |
| /perguntas-frequentes/ | dúvidas laboratório de prótese | prazo, garantia, pagamento, envio |
| /contato/ | contato Laboratório Dental Araújo | telefone, WhatsApp, endereço Av. Afonso Pena, orçamento |
| /blog/zirconia-ou-e-max-qual-indicar/ | zircônia ou E-Max | diferença zircônia e E-Max, quando indicar E-Max, coroa de zircônia indicação |
| /blog/como-enviar-um-caso-para-o-laboratorio-de-protese/ | como enviar caso para laboratório de prótese | enviar e embalar moldagem, coleta em BH |
| /blog/barra-de-protocolo-etapas-e-prazos/ | prótese protocolo: etapas | barra de protocolo passo a passo, moldagem de transferência, assentamento passivo |
| /blog/metaloceramica-ou-zirconia/ | metalocerâmica ou zircônia | ponte de zircônia ou metalocerâmica, coroa de zircônia sobre implante |
| /blog/ppr-ou-protese-flexivel/ | PPR ou prótese flexível | prótese flexível ou PPR, indicação da prótese flexível |
| /blog/requisicao-para-laboratorio-de-protese/ | requisição para laboratório de prótese | modelo de requisição, requisição em PDF, ordem de serviço |

As palavras de serviços e artigos vêm dos campos `primary`/`secondary` em `_build/content/`.
Os artigos são informativos (topo de funil) e linkam para o serviço comercial do mesmo assunto.

## 6. Estratégia de GEO (respostas de IA generativa)

- **`/llms.txt`**: resumo do laboratório, fatos rápidos e links para as páginas principais, cada um
  com uma linha de descrição ("Sob orçamento"), e a seção "Documentos" (privacidade e termos).
- **`/llms-full.txt`**: fatos, todos os serviços com FAQ, os itens de cada linha (sem valores), as condições
  de trabalho e as perguntas
  frequentes, em texto puro (para leitura direta por assistentes).
- **Ficha técnica** visível (home e /sobre/): fundação 1976, ≈ 400 m², mais de 35 especialistas,
  endereço, horário, prazo, garantia e área atendida — fatos curtos e citáveis.
- **Perguntas como títulos** ("Qual laboratório de prótese em BH faz barra de protocolo?") seguidas
  de resposta direta, o formato que os assistentes extraem.
- **`robots.txt`** libera GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended,
  ClaudeBot, Bingbot, Googlebot e `*`, e indica o sitemap.
- **`sitemap.xml`** com as 23 URLs (documentos legais com prioridade 0.3), `lastmod` e prioridade.
- Mesmo nome, endereço e telefone (NAP) no site, no JSON-LD e nos perfis externos.

## 7. Dados estruturados (JSON-LD)

Cada página tem **um** bloco `<script type="application/ld+json">` com um `@graph`. Os nós
`LocalBusiness + MedicalBusiness` (o laboratório, `@id` = `BASE/#laboratorio`) e `WebSite`
aparecem em todas as páginas; os demais dependem do tipo:

| Tipo de página | Nós do @graph (além de LocalBusiness e WebSite) |
|---|---|
| Home | `WebPage` |
| Hub de serviços | `CollectionPage`, `BreadcrumbList`, `ItemList` (os 8 serviços) |
| Serviço (×8) | `WebPage`, `BreadcrumbList`, `Service` (sem preço), `FAQPage` |
| Sobre | `AboutPage`, `BreadcrumbList` |
| Envio | `WebPage`, `BreadcrumbList`, `FAQPage` |
| Perguntas frequentes | `FAQPage` (como a própria página), `BreadcrumbList` |
| Contato | `ContactPage`, `BreadcrumbList` |
| Índice do blog | `CollectionPage`, `BreadcrumbList`, `Blog` |
| Artigo (×6) | `WebPage`, `BreadcrumbList`, `Article` (autor/editor = o laboratório; `citation` com as referências; `audience` = dentistas) |
| Privacidade, Termos | `WebPage`, `BreadcrumbList` (páginas indexáveis) |
| 404 | só os nós comuns (página `noindex`) |

O nó do laboratório inclui: razão social, CNPJ, fundação, endereço, geo, horários,
telefones, e-mail, `hasMap`, `sameAs` (Instagram, Facebook, Google Maps) e
número mínimo de funcionários (sem faixa de preço nem catálogo de ofertas). Para validar:
https://validator.schema.org e https://search.google.com/test/rich-results.

## 8. Orçamento: o site não publica preços

Desde 24/10/2026, a pedido do laboratório, todos os serviços são **sob orçamento** (WhatsApp ou
telefone). O que mudou:
- Removidos: a página `/tabela-de-precos/`, o PDF `/assets/docs/tabela-precos-2026.pdf`, todos os
  valores em R$ (home, serviços, FAQ, blog, sobre, envio, llms.txt, llms-full.txt, metas), o
  carrinho/pedido do JS e os nós `Offer`/`OfferCatalog`/`priceRange` do JSON-LD.
- `/tabela-de-precos/` → 301 para `/contato/`, que ganhou a seção `#orcamento`. O PDF antigo dá 404.
- Mantidos: os nomes dos itens e as observações de cada linha (`catalogo.py`), o prazo de 7 dias
  úteis, a urgência de 30% (percentual), a garantia de 6 meses e o pagamento até o dia 10.
- A fonte original está em `_build/arquivo/` (PDF, `prices_data.py` e o antigo `qa_precos.py`),
  fora do build e de `dist/`.
- Controle: `tools/qa_sem_precos.py` (no `npm run qa`) falha se `dist/` tiver "R$", "preço",
  "tabela-de-precos", ".pdf" ou `Offer`/`price` no JSON-LD, fora das exceções documentadas no
  script (a regra do `_redirects` e a frase dos termos "O site não publica preços").

## 9. Documentos legais

`/politica-de-privacidade/` e `/termos-de-uso/` (conteúdo em `_build/content/legal.py`, vigência
24/10/2026). Layout: sumário lateral gerado dos ids das seções, caixa de vigência e link para o
outro documento. Indexáveis, prioridade 0.3, `WebPage` + `BreadcrumbList`, links no rodapé e no
`llms.txt`.

**São modelos e precisam de revisão do laboratório e, de preferência, de um advogado.** Pontos
em aberto:
1. Encarregado (DPO): nomear um ou confirmar o enquadramento como agente de pequeno porte
   (Resolução CD/ANPD nº 2/2022), mantendo o canal de comunicação (hoje o e-mail).
2. Prazos de retenção (fiscal, garantia, prescrição) e guarda de registros de acesso (Marco Civil,
   art. 15: 6 meses para provedores de aplicação, se aplicável), já que os logs ficam com a Netlify.
3. Papel no tratamento de dados de pacientes (operador do dentista ou controlador próprio) e se
   há contrato ou termo com os dentistas sobre isso.
4. Se a base do art. 11, II, "f" (tutela da saúde) se aplica a um laboratório de prótese.
5. Prática real de identificação de pacientes nas requisições (nome completo, iniciais, código).
6. Transportadoras usadas além dos Correios e responsabilidade por danos no transporte.
7. Medidas de segurança internas do laboratório (acesso, armazenamento, descarte de modelos).
8. Contadores, advogados ou sistemas (ERP, emissor de notas) que recebem dados.
9. Se fotos de trabalhos de pacientes são ou serão publicadas (exigiria autorização).
10. Pagamento até o dia 10: forma, multa e juros por atraso (os termos não criam regras novas).
11. Regras de orçamento (validade, forma de aprovação), hoje não descritas por falta de definição.
12. Validade da cláusula de foro (Belo Horizonte/MG) nas relações com dentistas de outros estados.
13. Se o laboratório passar a usar analytics (GA4/GTM), atualizar a seção de cookies antes.

## 10. Pendências do dono (fora do site)

0. **Responsável técnico e CRO (Lei 6.710/1979, art. 4º, parágrafo único):** informar nome e número para entrarem no site. Ver [PALAVRAS-CHAVE.md](PALAVRAS-CHAVE.md), seção 7 (inclui as correções de NAP em diretórios).
1. **Google Business Profile:** reivindicar e verificar; categoria "Laboratório de prótese
   dentária"; mesmo NAP do site; fotos reais; link para o site.
2. **Domínio próprio:** ver README, "Trocar para um domínio próprio".
3. **Google Search Console** e **Bing Webmaster Tools:** verificar o domínio e enviar o sitemap.
4. **Avaliações no Google:** pedir aos dentistas clientes e responder a todas.
5. **Citações locais:** o mesmo NAP em diretórios (Apontador, TeleListas, Guia Mais, associações).
6. **Fotos reais:** ver [FOTOS.md](FOTOS.md).
7. **Conteúdo contínuo:** 1 a 2 artigos por mês, sempre linkando para o serviço correspondente.
