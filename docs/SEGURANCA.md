# Segurança do site

Revisão de 24/10/2026, atualizada em 27/10/2026. Site estático: não há backend, banco, login, formulário, cookie ou
dado pessoal coletado; a superfície de ataque se resume ao que o navegador carrega. O objetivo foi
deixar o navegador recusar qualquer coisa que não seja do próprio site.

O site oficial usa Cloudflare Workers Assets. As verificações de produção devem ser executadas
contra o domínio configurado em `SITE_BASE` após cada publicação.

## Resultado

| Verificação | Resultado |
|---|---|
| Arquivos internos no ar (`_headers`, `_redirects`, `.assetsignore`, `.env`, `.dev.vars`, `package.json`, `wrangler.jsonc`, `.git/`, `README.md`, mapas de código) | 404 (verificado por `tools/qa-live.mjs`) |
| Erros de CSP / Trusted Types no console (25 páginas + 404, Chromium) | 0 |
| `npm audit` (ferramentas de desenvolvimento) | 0 vulnerabilidades |
| Segredos no repositório (gitleaks 8.30.1, todo o histórico) | nenhum |
| Metadados EXIF/GPS nas imagens publicadas | nenhum |

## Arquitetura (o que existe e o que não existe)

- **Existe:** páginas HTML estáticas, CSS/JS próprios, fontes WOFF2 próprias, imagens, um PDF
  (ficha de requisição), `sitemap.xml`, `robots.txt`, `llms.txt`. Publicado pelo Worker
  `laboratorio-araujo`, que **só serve assets** (não há `main` no `wrangler.jsonc`).
- **Não existe:** backend, API, login, cookies, formulário (`<form>`/POST), upload, banco ou
  armazenamento de dados. Por isso não há rate limit, Turnstile ou proteção de API a configurar:
  não há endpoint para proteger. O Worker responde 405 a `POST`, `PUT`, `DELETE`, `OPTIONS` e `TRACE`.
- **Terceiros:** só links de saída (WhatsApp `wa.me`, Instagram, Facebook, Google Maps, gandra.tech,
  referências científicas) e o mapa do Google, que só carrega depois do clique. Nenhum script,
  fonte ou imagem de terceiros é carregado.

## Cabeçalhos

Fonte única: `src/site/files/_headers` (copiado para `dist/_headers` pelo build e aplicado pelo
Workers Assets). O Worker não tem código e o site em `workers.dev` não tem Cloudflare Rules,
então não há outra camada que repita cabeçalhos. A regra `/*` tem os cabeçalhos de segurança; as
demais regras só têm `Cache-Control`/`Content-Type`, e o QA (`tools/qa-static.mjs`) falha se um
mesmo cabeçalho aparecer em duas regras (o Workers Assets juntaria os valores).

### Antes (produção em 27/10/2026, commit `8a30fb6`)

```
content-security-policy: default-src 'self'; script-src 'self' 'sha256-Du+OJKJSbdUgz5nrHeWWINvez6XKDDU/tyj/5c2uvwo='; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests
strict-transport-security: max-age=31536000; includeSubDomains
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=(), browsing-topics=()
cross-origin-opener-policy: same-origin
```

### Depois (esta revisão)

```
content-security-policy: default-src 'self'; script-src 'self' 'sha256-Du+OJKJSbdUgz5nrHeWWINvez6XKDDU/tyj/5c2uvwo='; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests; require-trusted-types-for 'script'; trusted-types 'none'
strict-transport-security: max-age=31536000
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), magnetometer=(), microphone=(), midi=(), payment=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), xr-spatial-tracking=(), browsing-topics=()
cross-origin-opener-policy: same-origin
cross-origin-resource-policy: same-origin
x-permitted-cross-domain-policies: none
```

### Por que cada escolha

- **CSP sem `unsafe-inline`/`unsafe-eval`, sem `*`.** Tudo é `'self'`. Exceções, e o motivo:
  - `script-src 'sha256-…'`: o único script inline (`document.documentElement.classList.add('js')`)
    precisa rodar antes do CSS para evitar "piscada" das animações. Liberado só por hash; o QA
    confere que o hash da CSP bate com o script e que não sobra hash antigo.
  - `img-src data:`: a imagem vazia `src="data:,"` do visualizador de fotos de `/trabalhos/`
    (é trocada pela foto ao abrir). Nenhuma imagem externa é permitida.
  - `frame-src https://www.google.com https://maps.google.com`: o mapa em `/contato/` e na home,
    carregado só no clique, dentro de `iframe sandbox`.
  - `connect-src 'self'`: mantido como estava (o JS não faz requisições; não amplia nada).
- **Trusted Types (`require-trusted-types-for 'script'; trusted-types 'none'`)**: novo. O código
  não usa `innerHTML`/`eval`; com isso o navegador (Chromium) recusa qualquer injeção de HTML ou
  script por JS, mesmo que um bug futuro tente. Testado nas 25 páginas + 404, galeria, menu e
  mapa: 0 violações.
- **HSTS `max-age=31536000`, sem `includeSubDomains` e sem `preload`.** Antes havia
  `includeSubDomains`, o que contraria a regra do projeto enquanto não existir domínio próprio
  validado. O domínio `.dev` inteiro já está na lista HSTS preload dos navegadores, então HTTPS
  continua obrigatório em `workers.dev` de qualquer forma. **Quando houver domínio próprio:** só
  ativar `includeSubDomains`/`preload` depois de confirmar que todos os subdomínios têm HTTPS.
- **`X-Frame-Options: DENY` + `frame-ancestors 'none'`**: ninguém pode embutir o site (clickjacking).
- **Permissions-Policy**: desliga câmera, microfone, geolocalização, pagamento, USB, serial, HID,
  MIDI, WebAuthn, XR etc. Só entram recursos que o Chromium reconhece (`bluetooth` foi testado e
  gerava aviso no console, por isso ficou fora).
- **COOP `same-origin`**: links para WhatsApp/Instagram abrem com `noopener`; nada depende de
  `window.opener`.
- **CORP `same-origin`**: impede que outros sites usem imagens/fontes/PDF do laboratório como
  subrecurso. Não afeta pré-visualizações de link (WhatsApp, Facebook e Google buscam a
  `og:image` no servidor, sem CORP), nem quem abre o PDF ou a imagem diretamente.
- **`X-Permitted-Cross-Domain-Policies: none`**: bloqueia políticas Flash/PDF entre domínios.
- **Cache**: inalterado (`immutable` só em CSS/JS/fontes versionados).

## Outras proteções no código

- `src/site/files/.assetsignore`: o Wrangler não publica `.env`, `.dev.vars`, `.git`,
  `*.map`, `*.md`, `*.log` mesmo que apareçam em `dist/` por engano (testado: com o arquivo, 404;
  sem ele, 200).
- `.gitignore` também cobre `.env`, `.env.*`, `.dev.vars.*`, `*.pem` e `*.key` (repositório público).
- `tools/qa-static.mjs` falha o build de QA se houver: `target="_blank"` sem
  `rel="noopener noreferrer"`, URL `http://`, referência a Netlify, `sourceMappingURL`, caminho local
  de máquina, token `{{…}}` não substituído, `<form>`, `onclick=""`, arquivo proibido em `dist/`,
  canonical não absoluto, CSP fraca, hash de script divergente ou cabeçalho duplicado.
- `tools/qa-live.mjs` confere, no site publicado, os 9 cabeçalhos e que os arquivos internos dão 404.

## O que dá e o que não dá em `workers.dev`

| Recurso | Situação |
|---|---|
| Proteção DDoS padrão da Cloudflare | Ativa automaticamente, sem custo |
| WAF gerenciado, regras de firewall, Browser Integrity Check, Bot Fight Mode, rate limiting | **Não disponível**: são configurações de zona (domínio próprio). `workers.dev` não tem zona |
| Cloudflare Rules (Transform/Redirect) | Não disponível em `workers.dev`; cabeçalhos ficam no `_headers` |
| HSTS `includeSubDomains`/`preload` | Não aplicável sem domínio próprio |
| Turnstile / rate limit de API | Desnecessário: não há formulário nem endpoint |

Quando houver domínio próprio na Cloudflare: ativar Managed Rules gratuitas, Bot Fight Mode e
Browser Integrity Check com escopo do site, sem bloquear Googlebot nem assets, e revisar HSTS.

## Riscos restantes

- **URLs de preview de branch são públicas.** Builds de branches que não são `main` geram versões
  de preview em `*.workers.dev` (não afetam produção). Não suba conteúdo sensível em branch.
- `/404/` responde 200 com a página de erro (efeito do `html_handling`); ela tem `noindex`.
- Trusted Types só é aplicado em navegadores Chromium; nos demais vale a CSP restante.

## Rollback

1. **Pelo GitHub:** reverter o merge do PR na `main` (botão *Revert* do PR ou
   `git revert -m 1 <commit-do-merge>` e push). O deploy automático publica a versão anterior.
2. **Pela Cloudflare (imediato):** Workers & Pages → `laboratorio-araujo` → Deployments → escolher a
   versão anterior (ex.: `8a607bed`, do commit `8a30fb6`) → *Rollback*.

## O que foi encontrado e o que foi feito

| # | Ponto revisado | Situação e medida |
|---|---|---|
| 1 | Sem CSP; site usava GSAP e Lenis (bibliotecas de terceiros) | Bibliotecas removidas; todo o movimento agora é CSS + `IntersectionObserver` em `main.js`. Tudo é servido do próprio domínio (fontes WOFF2 inclusive), e a CSP só permite `'self'` |
| 2 | Scripts inline | Resta um, de uma linha (`document.documentElement.classList.add('js')`), liberado por **hash SHA-256** na CSP. O build calcula o hash; mudou o script, a CSP acompanha |
| 3 | Estilos inline (`style=""`, `<style>`) | O HTML não tem nenhum; `style-src 'self'` sem `unsafe-inline`. O html-validate (`no-inline-style`) impede que voltem |
| 4 | Sem cabeçalhos de segurança | HSTS (sem `includeSubDomains` desde 27/10/2026), nosniff, `X-Frame-Options: DENY` + `frame-ancestors 'none'` (contra clickjacking), Referrer-Policy, Permissions-Policy (bloqueia câmera, microfone, geolocalização, pagamento, FLoC/Topics) e COOP |
| 5 | `innerHTML` no destaque da busca de preços e no mapa | Reescritos com nós DOM (`createElement`, `textContent`, `replaceChildren`). O ESLint proíbe `innerHTML`, `outerHTML`, `document.write` e `eval`. A busca de preços foi removida em 24/10/2026, junto com a tabela |
| 6 | Hash da URL (`#preco-…`) usado direto como seletor | Era validado com `/^[a-z0-9-]+$/`; o código saiu junto com a tabela de preços (24/10/2026) |
| 7 | Mapa do Google (único conteúdo de terceiro) | Carrega só depois do clique em "Carregar mapa"; iframe com `sandbox` (scripts, mesma origem e pop-ups para "Abrir no Maps"), `referrerpolicy` e `loading="lazy"`. A CSP só permite frames de `www.google.com` e `maps.google.com` |
| 8 | Links externos com `target="_blank"` só com `noopener` | Todos com `rel="noopener noreferrer"`. Em 27/10/2026 o crédito gandra.tech do rodapé ainda estava só com `noopener` e foi corrigido; o QA agora impede regressão |
| 9 | Mensagem pré-preenchida do WhatsApp | A URL é codificada no código do site antes do redirecionamento para o WhatsApp |
| 10 | Dependências de desenvolvimento com 2 vulnerabilidades moderadas (`uuid` via linkinator) | `npm audit fix` → 0 |
| 11 | `JSON-LD` dentro de `<script>` | Mantido em bloco dedicado e verificado pelo QA estrutural; não há interpolação de HTML executável |
| 12 | Link com `#` malformado (ex.: `#%E0%A4%A`) | `decodeURIComponent` lançava erro e interrompia o JS da página (galeria, barra de leitura etc.). Corrigido em 27/10/2026 com `try/catch` em `10-acordeao.js` |
| 13 | `HSTS` com `includeSubDomains` sem domínio próprio | Removido em 27/10/2026 (ver Cabeçalhos) |

**Segredos:** nenhum token de deploy deve ser versionado. A publicação Cloudflare deve usar a
autenticação do Wrangler no ambiente do operador. Foi feita uma varredura no projeto (padrões de token/chave e o valor literal da
variável): nada encontrado. `.gitignore` exclui `node_modules`, `dist` e logs.

**Privacidade (LGPD):** o site não grava cookies, não usa analytics e não chama terceiros, a não ser
o mapa, que só carrega quando o visitante pede. Por isso não precisa de banner de cookies hoje.
A [política de privacidade](/politica-de-privacidade/)
descreve isso; se entrar analytics, atualize a política (seção Cookies) e a CSP antes.

**Redirecionamentos:** `src/site/files/_redirects` é copiado pelo build e leva `/tabela-de-precos/` para
`/contato/` com 301. O cache de `/assets/docs/*` saiu do `_headers`, porque a pasta não existe mais.

## Como manter

- **Não** use `innerHTML`, `style=""`, `<style>`, `onclick=""` ou scripts de CDN: a CSP bloqueia,
  e o lint acusa.
- Mudou o script inline? Nada a fazer: o build recalcula o hash.
- Depois de publicar: `node tools/qa-live.mjs https://laboratorio-araujo.gandratecnologia.workers.dev`.
- De tempos em tempos: `npm audit`.

### Adicionar Google Analytics 4 (se o dono quiser)

1. Crie `src/assets/js/ga.js` com o código de inicialização (`window.dataLayer = …;
   gtag('config', 'G-XXXX')`), **sem** script inline.
2. No shell compartilhado (`src/site/layout/before-main.html`), antes de `main.js`, inclua
   `<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>` e
   `<script src="/assets/js/ga.js" defer></script>`.
3. Em `src/site/files/_headers`, acrescente:
   - `script-src … https://www.googletagmanager.com`
   - `connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com`
   - `img-src 'self' data: https://*.google-analytics.com https://www.googletagmanager.com`
   - Trusted Types: o gtag.js cria `<script src>` por JS, o que `require-trusted-types-for 'script'`
     bloqueia. Teste antes; se houver violação, remova `require-trusted-types-for 'script'; trusted-types 'none'`
     da CSP e registre o motivo aqui.
4. Com analytics vem a LGPD: publique uma política de privacidade e, se usar cookies de anúncio,
   um banner de consentimento.
5. Os cliques em WhatsApp, telefone e mapa já têm `data-track="…"`, e `main.js` os envia ao
   `dataLayer` quando ele existe; com o GA4 ativo, viram eventos sem mudar o HTML.
