# Site do Laboratório Dental Araújo

Site institucional e comercial do **Laboratório Dental Araújo (LDA)**, laboratório de prótese
dentária em Belo Horizonte desde 1975 (Av. Afonso Pena, 262, sala 1602, Centro). O público é
**cirurgião-dentista e clínica**: o site mostra os serviços (todos **sob orçamento**, sem
preços publicados), explica como enviar casos de todo o Brasil e leva o contato para o WhatsApp de pedidos.

- **Hospedagem primária:** Cloudflare Workers Assets via Wrangler; o domínio final ainda deve ser
  definido em `SITE_BASE` no ambiente de build.
- **Endereço provisório atual:** https://brilliant-cat-c5b6e9.netlify.app (legado/validação)
- **Páginas:** 25 (home, hub de serviços + 8 serviços, sobre, envio, perguntas, contato,
  blog + 6 artigos, política de privacidade e termos de uso), mais a 404.
- **Tecnologia:** HTML e CSS estáticos gerados por Node.js/ESM, com JavaScript puro (sem
  frameworks, sem bibliotecas de terceiros, sem cookies e sem rastreadores). Não existe backend.
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
├── src/                       FONTE do site
│   ├── site/                   fonte estática publicada pelo build Node
│   │   ├── data/site.json      identidade e contatos tokenizados
│   │   ├── layout/             shell compartilhado antes/depois do conteúdo
│   │   ├── pages/              head + main de cada rota publicada
│   │   └── files/              headers, redirects, sitemap, robots e llms
│   ├── assets/
│   │   ├── css/               tokens, base, layout, components, pages, motion (+ bundle.txt)
│   │   ├── js/modules/        00-helpers … 12-galeria (+ bundle.txt)
│   │   ├── fonts/  icons/  img/{marca,og,foto,real}/  docs/
│   │   ├── favicon.ico  site.webmanifest
│   ├── private/marca/         PNG matriz do logo (não publicado)
│   └── fotos_reais.json        manifesto histórico não usado pelo build
├── scripts/build.mjs          gerador estático Node.js/ESM
├── dist/                      SAÍDA gerada (não edite à mão; sobe na Cloudflare)
├── tools/                     servidor Node, lint, migração, QA e acessibilidade
├── private/arquivo/           tabela de preços original (só local; NUNCA no Git)
├── package.json               scripts npm: build, serve, qa, qa:live, lint:*
├── wrangler.jsonc             configuração primária de assets estáticos na Cloudflare
└── netlify.toml               compatibilidade legada com build Node
```

Detalhes, diagrama mermaid e papel de cada módulo: [docs/ARQUITETURA.md](docs/ARQUITETURA.md).

## Como gerar o site

Requisitos: **Node.js** e as dependências do projeto (`npm install`). O build de produção não
depende de runtime de backend, banco de dados, API ou servidor de aplicação.

```bash
npm run build                    # recria dist/ (25 páginas + 404)
npm run serve                    # http://127.0.0.1:8766 com os cabeçalhos locais
```

Para gerar canonical, sitemap e JSON-LD para o domínio Cloudflare, configure a base antes do build:

```powershell
$env:SITE_BASE = 'https://www.seudominio.com.br'
npm run build
```

O build monta CSS/JS a partir dos módulos, copia assets, combina o layout compartilhado com as
rotas em `src/site/pages`, gera as 25 páginas + 404, o
`sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, o `_headers` (com a CSP) e o `_redirects`.

`npm run migrate:static` é uma ferramenta pontual de migração/recaptura do `dist` validado para
`src/site`. Não faz parte do build normal e não deve ser executada para editar conteúdo existente.

Checagem completa antes de publicar (precisa de `npm install` e do Playwright com Chromium):

```bash
npm install
npm run qa                       # build + lint HTML/CSS/JS + QA estrutural Node
npm run serve                    # em outro terminal, para os checks de navegador
npm run a11y                     # acessibilidade (com npm run serve rodando)
npm run links                    # links quebrados (com npm run serve rodando)
```

## Tarefas comuns

### Orçamento e preços (o site não publica valores)
Desde 24/10/2026 todos os serviços são **sob orçamento**, pelo WhatsApp ou pelo telefone. O site
não mostra valores, não tem tabela de preços nem PDF de preços, e o JSON-LD não tem `Offer`/`price`.
- A antiga página `/tabela-de-precos/` redireciona (301) para `/contato/` (arquivo-fonte
  `src/site/files/_redirects` → `dist/_redirects`). O PDF antigo responde 404.
- A fonte original (PDF e dados) está em `private/arquivo/`, fora do build e fora do repositório Git.
- O conteúdo publicado das páginas fica em `src/site/pages`; não há catálogo dinâmico nem backend.
- Depois de qualquer mudança de texto, rode `npm run qa`.

### Dados do laboratório (telefone, endereço, horário)
Contatos usados no HTML publicado ficam centralizados em `src/site/data/site.json`. Os tokens são
resolvidos pelo build em todas as rotas, reduzindo divergências entre header, footer e páginas.

### Documentos legais
`/politica-de-privacidade/` e `/termos-de-uso/` ficam em `src/site/pages`. Ao mudar algo,
atualize `VIGENCIA`. O texto é um modelo: revise com o laboratório e um advogado
(pontos em aberto em docs/ARQUITETURA.md).

### Textos curtos e acordeões
- "Pontos principais", rótulos e texto completo ficam no `main.html` da rota correspondente em
  `src/site/pages`.
- Antes e depois: componente pronto e **desligado** (`ANTES_DEPOIS = []`). Só ligue com pares
  reais e autorização; ver [docs/FOTOS.md](docs/FOTOS.md).

### Rotas e redirecionamentos
- `dist/_redirects` é copiado pelo build a partir de `src/site/files/_redirects`.
- Datas e metadados publicados ficam no `head.html` da rota correspondente.

### Crédito do desenvolvedor no rodapé
"Desenvolvido por [gandra.tech](https://www.gandra.tech/)" no shell compartilhado
(`src/site/layout/after-main.html`, `.footer__credit`).

### Adicionar um artigo no blog
1. Crie uma nova pasta de rota em `src/site/pages/blog/<slug>/index/`.
2. Copie `head.html` e `main.html` de um artigo semelhante e altere o conteúdo e os metadados.
3. Use `<h2>` nas seções, preserve canonical/JSON-LD e ligue o artigo ao serviço correspondente.
4. Atualize `src/site/files/sitemap.xml` e os arquivos `llms*.txt` quando a nova rota for publicada.
5. Rode `npm run build`.

### Adicionar uma página de serviço
1. Crie uma nova pasta de rota em `src/site/pages/servicos/<slug>/index/`.
2. Copie `head.html` e `main.html` de um serviço semelhante, sem publicar preços.
3. Atualize os links da hub, sitemap e arquivos `llms*.txt` quando aplicável.
4. Rode `npm run build`.

### Fotos reais
As fotos já publicadas ficam em `src/assets/img/real/` e são copiadas pelo build. Para preparar
novas variantes sem Python, use o utilitário Node `npm run images:prepare -- ...`, que chama o
ImageMagick local, remove metadados e gera WebP/AVIF/JPEG conforme o tipo. Detalhes em
[docs/FOTOS.md](docs/FOTOS.md).

## Publicar na Cloudflare

O caminho oficial é o Wrangler, usando `wrangler.jsonc` e `dist/` como assets estáticos:

```bash
SITE_BASE=https://www.seudominio.com.br npm run build
npm run deploy
```

No PowerShell, use `$env:SITE_BASE = 'https://www.seudominio.com.br'` antes dos comandos.
`npm run deploy` executa o build e `wrangler deploy`; esta etapa requer autenticação Cloudflare.
O `netlify.toml` permanece apenas para compatibilidade histórica e não é o caminho primário.

Depois de publicar, defina `SITE_BASE` para o domínio Cloudflare e rode `npm run qa:live`.

## Definir ou trocar o domínio canônico

1. Configure o domínio personalizado no projeto Cloudflare e aponte o DNS conforme o painel.
2. Defina **`SITE_BASE`** (sem barra no final) no ambiente de build/deploy.
3. Rode o build e publique. Cadastre o domínio no Search Console / Bing e envie o sitemap.

## O que não está neste repositório (de propósito)

- Nenhuma senha, token ou chave.
- Nenhum script de analytics: eventos de clique vão para `window.dataLayer`. Para medir, instale
  GA4/GTM e **libere os domínios na CSP** (`src/site/files/_headers`), senão o navegador bloqueia.
  Passo a passo em [docs/SEGURANCA.md](docs/SEGURANCA.md).
- Tabela de preços original, capturas de tela e `.env`.
