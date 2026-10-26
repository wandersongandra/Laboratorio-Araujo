# Site do Laboratório Dental Araújo

Site institucional e comercial do **Laboratório Dental Araújo (LDA)**, laboratório de prótese
dentária em Belo Horizonte desde 1976 (Av. Afonso Pena, 262, sala 1602, Centro). O público é
**cirurgião-dentista e clínica**: o site mostra os serviços (todos **sob orçamento**, sem
preços publicados), explica como enviar casos de todo o Brasil e leva o contato para o WhatsApp de pedidos.

- **Endereço atual:** https://brilliant-cat-c5b6e9.netlify.app (Netlify)
- **Páginas:** 20 (home, hub de serviços + 8 serviços, sobre, envio, perguntas, contato,
  blog + 6 artigos, política de privacidade e termos de uso), mais a 404.
- **Tecnologia:** HTML e CSS estáticos gerados por um gerador Python modular, com JavaScript puro
  (sem frameworks, sem bibliotecas de terceiros, sem cookies e sem rastreadores).
  Fontes e imagens ficam no próprio site.

> Documentação técnica: [docs/ARQUITETURA.md](docs/ARQUITETURA.md) (pastas, fluxo de build, SEO/GEO) ·
> [docs/SEGURANCA.md](docs/SEGURANCA.md) (cabeçalhos, CSP) ·
> [docs/QUALIDADE.md](docs/QUALIDADE.md) (validações e resultados) ·
> [docs/FOTOS.md](docs/FOTOS.md) (origem das imagens e fotos reais) ·
> [docs/PALAVRAS-CHAVE.md](docs/PALAVRAS-CHAVE.md) (mapa de palavras-chave) e
> [docs/AUDITORIA-2026-10-26.md](docs/AUDITORIA-2026-10-26.md) (auditoria completa).

---

## Estrutura de pastas

```
Laboratorio-Araujo/
├── README.md                  este guia
├── docs/                      ARQUITETURA, SEGURANCA, QUALIDADE, FOTOS, PALAVRAS-CHAVE, AUDITORIA
├── src/                       FONTE do site (é aqui que se edita)
│   ├── data/laboratorio.py    fonte única: nome, CNPJ, endereço, telefones, WhatsApp, horários, redes
│   ├── content/               conteúdo editorial em Python
│   │   ├── catalogo.py        itens de cada linha e condições gerais (sem preços)
│   │   ├── servicos.py        as 8 páginas de serviço
│   │   ├── blog.py            artigos do blog
│   │   ├── fotos_reais.py     catálogo das fotos reais
│   │   ├── paginas.py         ficha técnica e FAQ
│   │   ├── legal.py           privacidade (LGPD) e termos
│   │   └── resumos.py         "Pontos principais" e rótulos curtos
│   ├── templates/             layouts / partials / pages (layouts reexportam o build hoje)
│   ├── assets/
│   │   ├── css/               tokens, base, layout, components, pages, motion (+ bundle.txt)
│   │   ├── js/modules/        00-helpers … 12-galeria (+ bundle.txt)
│   │   ├── fonts/  icons/  img/{marca,og,foto,real}/  docs/
│   │   ├── favicon.ico  site.webmanifest
│   ├── private/marca/         PNG matriz do logo (não publicado)
│   └── fotos_reais.json       manifesto das fotos reais
├── scripts/build/             gerador modular (config, content_loader, util, minify, security, site)
├── dist/                      SAÍDA gerada (não edite à mão; sobe no Netlify)
├── tools/                     serve, QA, fotos, OG, PDF de requisição
├── private/arquivo/           tabela de preços original (só local; NUNCA no Git)
├── package.json               scripts npm: build, serve, qa, qa:live, lint:*
├── requirements.txt           Pillow (necessário para o build)
├── requirements-dev.txt       numpy, playwright, pypdf (ferramentas opcionais)
└── netlify.toml               command = python -m scripts.build; publish = dist
```

Detalhes, diagrama mermaid e papel de cada módulo: [docs/ARQUITETURA.md](docs/ARQUITETURA.md).

## Como gerar o site

Requisitos: **Python 3.12+** e **Pillow** (`pip install -r requirements.txt`).

```bash
npm run build                    # ou: python -m scripts.build  → recria dist/ (≈ 1 s)
npm run serve                    # http://127.0.0.1:8766 com os mesmos cabeçalhos do Netlify
```

O build: monta CSS/JS a partir dos módulos, copia assets, gera as 24 páginas + 404, o
`sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, o `_headers` (com a CSP) e o `_redirects`.

Checagem completa antes de publicar (precisa de `npm install` e do Playwright com Chromium):

```bash
npm install
pip install -r requirements-dev.txt
npm run qa                       # build + lint HTML/CSS/JS + SEO + "sem preços" + navegador
npm run a11y                     # acessibilidade (com npm run serve rodando)
npm run links                    # links quebrados (com npm run serve rodando)
```

No Windows, o `tools/qa_sem_precos.py` usa `pdftotext` (Poppler) ou, se faltar, `pypdf`.

## Tarefas comuns

### Orçamento e preços (o site não publica valores)
Desde 24/10/2026 todos os serviços são **sob orçamento**, pelo WhatsApp ou pelo telefone. O site
não mostra valores, não tem tabela de preços nem PDF de preços, e o JSON-LD não tem `Offer`/`price`.
- A antiga página `/tabela-de-precos/` redireciona (301) para `/contato/` (constante `REDIRECTS`
  em `scripts/build/site.py` → `dist/_redirects`). O PDF antigo responde 404.
- A fonte original (PDF e dados) está em `private/arquivo/`, fora do build e fora do repositório Git.
- Itens e observações de cada linha (sem valores) ficam em `src/content/catalogo.py`; as
  condições gerais (prazo, urgência de 30%, garantia, pagamento) em `CONDICOES`, no mesmo arquivo.
- Depois de qualquer mudança de texto, rode `python tools/qa_sem_precos.py`.

### Dados do laboratório (telefone, endereço, horário)
Edite **somente** `src/data/laboratorio.py` e rode o build. Header, footer, contato, JSON-LD e
`llms.txt` leem dessa fonte única.

### Documentos legais
`/politica-de-privacidade/` e `/termos-de-uso/` saem de `src/content/legal.py`. Ao mudar algo,
atualize `VIGENCIA`. O texto é um modelo: revise com o laboratório e um advogado
(pontos em aberto em docs/ARQUITETURA.md).

### Textos curtos e acordeões
- "Pontos principais" e rótulos da home: `src/content/resumos.py`.
- Texto completo: `servicos.py` (campo `body`) e builders em `scripts/build/site.py`.
- Antes e depois: componente pronto e **desligado** (`ANTES_DEPOIS = []`). Só ligue com pares
  reais e autorização; ver [docs/FOTOS.md](docs/FOTOS.md).

### Rotas e redirecionamentos
- `dist/_redirects` é gerado pelo build (`REDIRECTS` + `redirects_index()`).
- Datas: `TODAY` e `MODIFICADO` em `scripts/build/config.py`.

### Crédito do desenvolvedor no rodapé
"Desenvolvido por [gandra.tech](https://www.gandra.tech/)" em `footer()` (`.footer__credit`).

### Adicionar um artigo no blog
1. Em `src/content/blog.py`, copie um item de `POSTS` e altere slug, date, title (≤ 60), desc,
   h1, lead, img/img_alt, primary/secondary, related_service, related_posts, refs e body.
2. Use `<h2>` nas seções e linke para o serviço comercial do mesmo assunto.
3. Rode `npm run build`.

### Adicionar uma página de serviço
1. Em `src/content/servicos.py`, copie um item de `SERVICOS`.
2. Se tiver itens próprios, crie a linha em `catalogo.py` e o ícone em `site.py` (`ICON`).
3. Rode o build.

### Fotos reais
O catálogo fica em `src/content/fotos_reais.py`. Para exportar de novo:
```bash
FOTOS_DRIVE=/caminho/fotos-drive FOTOS_CHAT=/caminho/fotos-chat python tools/foto_real.py
python tools/og.py
npm run build
```
Use `'real/<slug>'` no `img`/`fig`. Detalhes: [docs/FOTOS.md](docs/FOTOS.md).

## Publicar no Netlify

**Opção A: manual.** Gere o site e envie o conteúdo de `dist/` (arrastar no Netlify ou API com zip).
O token fica numa variável de ambiente; nunca o grave em arquivos do projeto.

**Opção B: deploy contínuo via Git.** O `netlify.toml` já informa
`command = "python -m scripts.build"` e `publish = "dist"`.

Depois de publicar, rode `npm run qa:live`.

## Trocar para um domínio próprio

1. No Netlify: *Domain management → Add a domain* e aponte o DNS.
2. Em `scripts/build/config.py`, troque **`BASE`** (sem barra no final).
3. Rode o build e publique. Cadastre o domínio no Search Console / Bing e envie o sitemap.

## O que não está neste repositório (de propósito)

- Nenhuma senha, token ou chave.
- Nenhum script de analytics: eventos de clique vão para `window.dataLayer`. Para medir, instale
  GA4/GTM e **libere os domínios na CSP** (`scripts/build/security.py`), senão o navegador bloqueia.
  Passo a passo em [docs/SEGURANCA.md](docs/SEGURANCA.md).
- Tabela de preços original, capturas de tela e `.env`.
)
