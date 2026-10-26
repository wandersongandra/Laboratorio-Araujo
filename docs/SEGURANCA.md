# Segurança do site

Revisão de 24/10/2026. Site estático: não há backend, banco, login, formulário, cookie ou
dado pessoal coletado; a superfície de ataque se resume ao que o navegador carrega. O objetivo foi
deixar o navegador recusar qualquer coisa que não seja do próprio site.

O site oficial usa Cloudflare Workers Assets. As verificações de produção devem ser executadas
contra o domínio configurado em `SITE_BASE` após cada publicação.

## Resultado

| Verificação | Resultado |
|---|---|
| Mozilla HTTP Observatory | Pendente: executar contra o domínio oficial Cloudflare |
| Arquivos internos no ar (`docs/`, `package.json`, `.git/`, `.env`, `_headers`, `_redirects`, mapas de código e arquivos antigos) | Pendente: confirmar após a publicação Cloudflare (`tools/qa-live.mjs`) |
| Critérios do securityheaders.com (os 6 cabeçalhos, CSP sem `unsafe-inline`) | **A+** (todos presentes; o site deles exige chave de API, por isso a nota foi calculada pelos mesmos critérios) |
| Erros de CSP no console (21 URLs × 3 larguras, no ar) | 0 |
| `npm audit` (ferramentas de desenvolvimento) | 0 vulnerabilidades |
| Segredos no repositório | nenhum |

## Cabeçalhos esperados no domínio oficial

```
content-security-policy: default-src 'self'; script-src 'self' 'sha256-Du+OJKJSbdUgz5nrHeWWINvez6XKDDU/tyj/5c2uvwo='; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=(), browsing-topics=()
cross-origin-opener-policy: same-origin
```

O arquivo `dist/_headers` é copiado de `src/site/files/_headers` pelo build Node; não edite a
saída à mão. O comportamento final dos headers deve ser confirmado depois do primeiro deploy
Cloudflare.

## O que foi encontrado e o que foi feito

| # | Ponto revisado | Situação e medida |
|---|---|---|
| 1 | Sem CSP; site usava GSAP e Lenis (bibliotecas de terceiros) | Bibliotecas removidas; todo o movimento agora é CSS + `IntersectionObserver` em `main.js`. Tudo é servido do próprio domínio (fontes WOFF2 inclusive), e a CSP só permite `'self'` |
| 2 | Scripts inline | Resta um, de uma linha (`document.documentElement.classList.add('js')`), liberado por **hash SHA-256** na CSP. O build calcula o hash; mudou o script, a CSP acompanha |
| 3 | Estilos inline (`style=""`, `<style>`) | O HTML não tem nenhum; `style-src 'self'` sem `unsafe-inline`. O html-validate (`no-inline-style`) impede que voltem |
| 4 | Sem cabeçalhos de segurança | HSTS, nosniff, `X-Frame-Options: DENY` + `frame-ancestors 'none'` (contra clickjacking), Referrer-Policy, Permissions-Policy (bloqueia câmera, microfone, geolocalização, pagamento, FLoC/Topics) e COOP |
| 5 | `innerHTML` no destaque da busca de preços e no mapa | Reescritos com nós DOM (`createElement`, `textContent`, `replaceChildren`). O ESLint proíbe `innerHTML`, `outerHTML`, `document.write` e `eval`. A busca de preços foi removida em 24/10/2026, junto com a tabela |
| 6 | Hash da URL (`#preco-…`) usado direto como seletor | Era validado com `/^[a-z0-9-]+$/`; o código saiu junto com a tabela de preços (24/10/2026) |
| 7 | Mapa do Google (único conteúdo de terceiro) | Carrega só depois do clique em "Carregar mapa"; iframe com `sandbox` (scripts, mesma origem e pop-ups para "Abrir no Maps"), `referrerpolicy` e `loading="lazy"`. A CSP só permite frames de `www.google.com` e `maps.google.com` |
| 8 | Links externos com `target="_blank"` só com `noopener` | Todos com `rel="noopener noreferrer"` (21 ocorrências) |
| 9 | Mensagem pré-preenchida do WhatsApp | A URL é codificada no código do site antes do redirecionamento para o WhatsApp |
| 10 | Dependências de desenvolvimento com 2 vulnerabilidades moderadas (`uuid` via linkinator) | `npm audit fix` → 0 |
| 11 | `JSON-LD` dentro de `<script>` | Mantido em bloco dedicado e verificado pelo QA estrutural; não há interpolação de HTML executável |

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
- Depois de publicar: `curl -sI https://SEU-DOMINIO/` e o Observatory (link acima).
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
4. Com analytics vem a LGPD: publique uma política de privacidade e, se usar cookies de anúncio,
   um banner de consentimento.
5. Os cliques em WhatsApp, telefone e mapa já têm `data-track="…"`, e `main.js` os envia ao
   `dataLayer` quando ele existe; com o GA4 ativo, viram eventos sem mudar o HTML.
