# Site do Laboratório Dental Araújo

Site institucional e comercial do **Laboratório Dental Araújo (LDA)**, laboratório de prótese
dentária em Belo Horizonte desde 1976 (Av. Afonso Pena, 262, sala 1602, Centro). O público é
**cirurgião-dentista e clínica**: o site mostra os serviços (todos **sob orçamento**, sem
preços publicados), explica como enviar casos de todo o Brasil e leva o contato para o WhatsApp de pedidos.

- **Endereço atual:** https://brilliant-cat-c5b6e9.netlify.app (Netlify)
- **Páginas:** 20 (home, hub de serviços + 8 serviços, sobre, envio, perguntas, contato,
  blog + 3 artigos, política de privacidade e termos de uso), mais a 404.
- **Tecnologia:** HTML e CSS estáticos gerados por um script Python, com um único arquivo de
  JavaScript puro (sem frameworks, sem bibliotecas de terceiros, sem cookies e sem rastreadores).
  Fontes e imagens ficam no próprio site.

> Documentação técnica: [docs/ARQUITETURA.md](docs/ARQUITETURA.md) (páginas, URLs, modelos,
> SEO/GEO, dados estruturados) · [docs/SEGURANCA.md](docs/SEGURANCA.md) (cabeçalhos, CSP) ·
> [docs/QUALIDADE.md](docs/QUALIDADE.md) (validações e resultados) ·
> [docs/FOTOS.md](docs/FOTOS.md) (origem das imagens e onde entram as fotos reais) ·
> [docs/PALAVRAS-CHAVE.md](docs/PALAVRAS-CHAVE.md) (mapa de palavras-chave e SEO on-page, 26/10/2026) e
> [docs/AUDITORIA-2026-10-26.md](docs/AUDITORIA-2026-10-26.md) (auditoria completa de rotas, SEO,
> segurança, front-end e conteúdo, com o que foi corrigido e o que depende do laboratório).

---

## Estrutura de pastas

```
site-clone/
├── README.md                  este guia
├── docs/
│   ├── ARQUITETURA.md         mapa de páginas, URLs, modelos, SEO/GEO e JSON-LD
│   ├── SEGURANCA.md           revisão de segurança, CSP e cabeçalhos HTTP
│   ├── QUALIDADE.md           ferramentas de qualidade e últimos resultados
│   ├── FOTOS.md               fotos reais: origem (pastas do Drive), mapa foto → espaço, dúvidas
│   ├── AUDITORIA-2026-10-26.md  auditoria completa (achados, correções, pendências)
│   └── PALAVRAS-CHAVE.md      mapa de palavras-chave, fontes, plano de conteúdo e pendências do dono
├── _build/                    FONTE do site (é aqui que se edita)
│   ├── build.py               gerador: modelos HTML, JSON-LD, sitemap, llms.txt, _headers, _redirects
│   ├── content/               conteúdo em Python (texto puro, fácil de editar)
│   │   ├── catalogo.py        itens de cada linha de serviço e condições gerais (sem preços)
│   │   ├── servicos.py        as 8 páginas de serviço (texto, FAQ, prazos)
│   │   ├── blog.py            artigos do blog
│   │   ├── fotos_reais.py     catálogo das fotos reais do LDA (pasta, categoria, alt, legenda, recorte)
│   │   ├── paginas.py         ficha técnica do laboratório e perguntas da página de FAQ
│   │   └── legal.py           política de privacidade (LGPD) e termos de uso
│   ├── arquivo/               tabela de preços 2026 original (PDF + dados). NÃO é publicada e não vai para o repositório Git
│   ├── fontes/marca/          logotipo em PNG (matriz usada pelo tools/og.py). NÃO é publicada
│   └── static/                copiado para dist/ como está (CSS/JS são minificados no caminho)
│       ├── favicon.ico  site.webmanifest
│       └── assets/
│           ├── css/style.css  folha de estilos única (comentada, com tokens de design)
│           ├── js/main.js     interações (menu, revelações, contadores, faixa de fotos, linha do tempo,
│           │                  acordeões, antes/depois desligado, mapa sob demanda)
│           ├── fonts/         Newsreader, IBM Plex Sans e IBM Plex Mono (woff2, licença OFL)
│           ├── img/real/      fotos REAIS do LDA (AVIF/WebP/JPEG, 480–1200 px, sem EXIF), geradas por tools/foto_real.py
│           ├── img/foto/      as 4 imagens ilustrativas (Pexels) que ainda restam, 640 e 1200 px (WebP)
│           ├── img/marca/     logotipo em WebP (azul e branco)
│           ├── img/og/        imagens de compartilhamento (1200×630): padrão, /trabalhos/, serviços e artigos
│           └── icons/         ícones do site/app (favicon, apple-touch, 192, 512)
├── dist/                      SAÍDA gerada (não edite à mão). É o que vai para o Netlify
├── tools/                     utilitários de manutenção e QA
│   ├── serve.py               servidor local que aplica os cabeçalhos/CSP do _headers
│   ├── foto_real.py           exporta as fotos reais (sem filtro de cor, sem EXIF, sem ampliar) + manifesto
│   ├── foto.py                (legado) tratamento de cor das imagens ilustrativas; NÃO use em fotos reais
│   ├── og.py                  gera as imagens de compartilhamento a partir das fotos reais
│   ├── qa_paginas.py          abre todas as páginas: status, erros de JS/CSP, rolagem lateral
│   ├── qa_sem_precos.py       garante que dist/ não publica preços nem a antiga tabela/PDF
│   ├── qa_seo.py              títulos, descrições, H1, JSON-LD, links internos
│   ├── qa_rotas.py            rotas e URLs: sitemap, canonical, links/âncoras, 301, 404 (local ou no ar)
│   ├── qa_interacao.py        âncoras em acordeões, sem JS, movimento reduzido, menu por teclado
│   ├── relatorio_pdf.py       gera o PDF de um relatório em Markdown (ex.: a auditoria)
│   ├── requisicao_pdf.py      gera o modelo de requisição em PDF (_build/static/assets/docs/)
│   ├── capturas.py            capturas de tela de página inteira (desktop e celular)
│   └── a11y.mjs               acessibilidade com axe-core em todas as páginas
├── _arquivo/                  imagens ilustrativas que saíram do site (fora do dist/)
├── screenshots/               capturas de referência (antes/depois, desktop, celular)
├── package.json               só ferramentas de qualidade (eslint, stylelint, html-validate…)
├── eslint.config.mjs  .stylelintrc.json  .htmlvalidate.json  .editorconfig  .gitignore
├── requirements.txt           Pillow (necessário para o build)
├── requirements-dev.txt       numpy + playwright (ferramentas opcionais)
└── netlify.toml               só para deploy contínuo via Git (opcional)
```

## Como gerar o site

Requisitos: **Python 3.12+** e **Pillow** (`pip install -r requirements.txt`).

```bash
python3 _build/build.py          # recria dist/ do zero (≈ 1 s)
python3 tools/serve.py           # http://localhost:8766 com os mesmos cabeçalhos do Netlify
```

O build: copia `_build/static/` para `dist/`, minifica CSS e JS, gera as 20 páginas + 404, o
`sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, o `_headers` (com a CSP) e o `_redirects`.

Checagem completa antes de publicar (precisa de `npm install` e do Playwright com Chromium):

```bash
npm install
npm run qa                       # build + lint HTML/CSS/JS + SEO + "sem preços" + navegador
npm run a11y                     # acessibilidade (com tools/serve.py rodando)
npm run links                    # links quebrados (com tools/serve.py rodando)
```

## Tarefas comuns

### Orçamento e preços (o site não publica valores)
Desde 24/10/2026 todos os serviços são **sob orçamento**, pelo WhatsApp ou pelo telefone. O site
não mostra valores, não tem tabela de preços nem PDF, e o JSON-LD não tem `Offer`/`price`.
- A antiga página `/tabela-de-precos/` redireciona (301) para `/contato/` (regra em `REDIRECTS`,
  no `build.py`, gravada em `dist/_redirects`). O PDF antigo responde 404.
- A fonte original (PDF e `prices_data.py`) está em `_build/arquivo/`, fora do build e fora do repositório Git (fica só na cópia local do laboratório). Veja o
  `LEIA-ME.md` dessa pasta antes de pensar em voltar a publicar preços.
- Itens e observações de cada linha (sem valores) ficam em `_build/content/catalogo.py`; as
  condições gerais (prazo, urgência de 30%, garantia, pagamento) em `CONDICOES`, no mesmo arquivo.
- Depois de qualquer mudança de texto, rode `python3 tools/qa_sem_precos.py`: ele procura "R$",
  "preço", "tabela-de-precos" e ".pdf" em `dist/` e falha se achar algo fora do permitido.
  Com `--live https://SEU-SITE` também confere o redirect e o 404 do PDF no ar.

### Documentos legais
`/politica-de-privacidade/` e `/termos-de-uso/` saem de `_build/content/legal.py` (uma lista de
seções por documento; o sumário lateral é gerado dos ids). Ao mudar algo, atualize `VIGENCIA` no
mesmo arquivo. O texto é um modelo: deve ser revisado pelo laboratório e por um advogado
(pontos em aberto em docs/ARQUITETURA.md, seção "Documentos legais").

### Textos curtos e acordeões (versão enxuta, 26/10/2026)

- Os tópicos "Pontos principais" das páginas de serviço, de /sobre/ e de /envio-para-todo-brasil/ e
  os rótulos curtos dos cartões da home ficam em `_build/content/resumos.py`. Só use fatos que já
  estejam no texto completo da página.
- O texto completo de cada página continua em `servicos.py` (campo `body`) e no `build.py`. O build
  recolhe cada seção `<h2>` num acordeão `<details>` (`accordion()`): o texto inteiro fica no HTML
  (buscadores e IAs leem tudo), só aparece fechado. Para deixar uma seção aberta, passe o título
  em `open_titles`.
- Componentes novos da home: contadores (`data-count`), faixa de fotos com botão Pausar (`FAIXA`),
  cartões de serviço (`svc_tiles()`), linha do tempo com barra de progresso (`data-tl`).
- Antes e depois: componente pronto e **desligado** (`ANTES_DEPOIS = []` no `build.py`). Só ligue
  com pares reais de fotos do mesmo caso e autorização; ver [docs/FOTOS.md](docs/FOTOS.md).

### Rotas e redirecionamentos (auditoria de 26/10/2026)

- `dist/_redirects` é gerado pelo build: a constante `REDIRECTS` (tabela antiga → `/contato/`,
  `/404.html` e `/404` com status 404) mais `redirects_index()`, que cria um 301 de
  `/<página>/index.html` para `/<página>/` em todas as páginas. Página nova entra sozinha.
- Datas: `TODAY` é o `lastmod`/`dateModified` padrão; páginas cujo texto não mudou ficam em
  `MODIFICADO` (hoje, política e termos: 24/10/2026, igual ao "Atualizado em" visível).

### Crédito do desenvolvedor no rodapé

A linha de base do rodapé de todas as páginas traz "Desenvolvido por
[gandra.tech](https://www.gandra.tech/)" (abre em nova aba, `rel="noopener"`). Fica em `footer()`
no `build.py` (`.footer__credit` no CSS).

### Adicionar um artigo no blog
1. Em `_build/content/blog.py`, copie um item da lista `POSTS` e altere: `slug` (vira a URL
   `/blog/<slug>/`), `date` (AAAA-MM-DD), `title` (até 60 caracteres), `desc` (≈ 140–160), `h1`,
   `lead`, `img` + `img_alt` (ex.: `'foto/escala-cor'`, sem tamanho e extensão), `primary` e
   `secondary` (palavras-chave; veja o mapa em `docs/PALAVRAS-CHAVE.md` para não repetir o termo principal
   de outra página), `related_service` (slug do serviço ligado ou `None`), `related_posts` (2 slugs para
   "Leia também"; opcional), `refs` (lista de `(citação em HTML, url)`, vira a seção "Referências" e o
   `citation` do JSON-LD; opcional) e `body` (HTML). Fatos técnicos só com fonte em `refs`.
2. Use `<h2>` para as seções (a numeração 01.1, 01.2… é automática) e linke para a página de
   serviço correspondente; é isso que dá autoridade à página comercial.
3. Rode o build. O artigo entra no índice do blog, no sitemap, no `llms.txt` e ganha JSON-LD
   `Article` + breadcrumbs.

### Adicionar uma página de serviço
1. Em `_build/content/servicos.py`, copie um item de `SERVICOS`. Campos: `slug`, `nav` (nome do
   menu), `title`, `desc`, `kicker`, `h1`, `lead`, `img`/`img_alt` (foto do topo), `fig`/`fig_alt`
   (foto no meio do texto), `primary`/`secondary` (palavras-chave), `cats` (linhas de `catalogo.py`
   ligadas a ele), `service_type`, `blurb` (resumo dos cartões), `body`, `faq` e `related`.
2. Se ele tiver itens próprios, crie a linha em `catalogo.py` (com um ícone em `ICON`, no `build.py`) e ponha o `id` em `cats`.
3. Rode o build. A página entra no menu "Serviços", no índice da home, no hub `/servicos/`, no
   sitemap e ganha JSON-LD `Service` (sem preço) + `FAQPage`.

### Fotos reais (galeria /trabalhos/, topos, figuras, faixa, capas)
O catálogo fica em `_build/content/fotos_reais.py`. As fotos originais **não** ficam no projeto
(o acervo do Drive tem 1,1 GB). Para exportar de novo:
```bash
FOTOS_DRIVE=/caminho/fotos-drive FOTOS_CHAT=/caminho/fotos-chat python3 tools/foto_real.py
python3 tools/og.py        # imagens de compartilhamento
python3 _build/build.py
```
Para usar uma foto num espaço, ponha `'real/<slug>'` no `img`/`fig` do serviço ou artigo. A etiqueta
"Foto: LDA", a legenda, o `<picture>` AVIF/WebP/JPEG e o JSON-LD `ImageObject` entram sozinhos.
Toda foto do catálogo aparece também em `/trabalhos/`. Critérios (sem rostos nem nomes, material
só com certeza, sem filtro de cor), mapa completo e dúvidas: [docs/FOTOS.md](docs/FOTOS.md).

## Publicar no Netlify

**Opção A: manual (como é feito hoje).** Gere o site e envie o **conteúdo** de `dist/`:
- arraste a pasta `dist/` em *app.netlify.com → Sites → (site) → Deploys*; ou
- pela API, com um zip cujo topo seja o conteúdo de `dist/`:
  ```bash
  curl -X POST -H "Content-Type: application/zip" \
       -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
       --data-binary @dist.zip \
       https://api.netlify.com/api/v1/sites/<SITE_ID>/deploys
  ```
  O token fica numa variável de ambiente; nunca o grave em arquivos do projeto.

**Opção B: deploy contínuo via Git.** Suba este projeto para um repositório e ligue-o ao Netlify.
O `netlify.toml` já informa o comando (`python3 _build/build.py`) e a pasta (`dist`).

Depois de publicar, rode `npm run qa:live`: confere no ar as URLs do sitemap (200, canonical,
links e âncoras), os 301 (sem barra, MAIÚSCULAS, `/index.html`, tabela antiga), a 404, os
cabeçalhos de segurança, os links externos, a ausência de preços e o console de cada página.
Se mudar o endereço (domínio próprio), passe a URL nova: `python3 tools/qa_rotas.py https://…`.

## Trocar para um domínio próprio

1. No Netlify: *Domain management → Add a domain* (ex.: `www.dentalaraujo.com.br`) e aponte o DNS
   como indicado. O HTTPS é emitido automaticamente.
2. Em `_build/build.py`, troque a constante **`BASE`** pelo novo endereço, sem barra no final:
   `BASE = 'https://www.dentalaraujo.com.br'`.
3. Rode o build e publique. Canonical, Open Graph, sitemap, robots, JSON-LD e `llms.txt` passam a
   usar o domínio novo. Mantenha o endereço `.netlify.app` redirecionando (o Netlify faz isso ao
   definir o domínio principal).
4. No Google Search Console e no Bing Webmaster Tools, cadastre o domínio e envie o `sitemap.xml`.

## O que não está neste repositório (de propósito)

- Nenhuma senha, token ou chave. O deploy usa a variável `NETLIFY_AUTH_TOKEN` do ambiente.
- Nenhum script de analytics: o site já envia eventos de clique (WhatsApp, telefone) para
  `window.dataLayer`. Para medir, instale o GA4/GTM e **libere os domínios dele na CSP**
  (`_build/build.py → CSP`), senão o navegador bloqueia. Passo a passo em
  [docs/SEGURANCA.md](docs/SEGURANCA.md#adicionar-google-analytics-4-se-o-dono-quiser).
