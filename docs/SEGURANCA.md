# Segurança do site

Revisão de 24/10/2026. Site estático: não há servidor, banco, login, formulário, cookie ou
dado pessoal coletado; a superfície de ataque se resume ao que o navegador carrega. O objetivo foi
deixar o navegador recusar qualquer coisa que não seja do próprio site.

## Resultado

| Verificação | Resultado |
|---|---|
| [Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory/analyze?host=brilliant-cat-c5b6e9.netlify.app) (24/10 e 26/10/2026) | **A+**, 130/100, 12 de 12 testes |
| Arquivos internos no ar (auditoria 26/10/2026: fontes do gerador, `docs/`, `package.json`, `.git/`, `.env`, `_headers`, `_redirects`, mapas de código, PDF antigo) | nenhum responde 200 (`tools/qa_rotas.py`) |
| Critérios do securityheaders.com (os 6 cabeçalhos, CSP sem `unsafe-inline`) | **A+** (todos presentes; o site deles exige chave de API, por isso a nota foi calculada pelos mesmos critérios) |
| Erros de CSP no console (21 URLs × 3 larguras, no ar) | 0 |
| `npm audit` (ferramentas de desenvolvimento) | 0 vulnerabilidades |
| Segredos no repositório | nenhum |

## Cabeçalhos no ar (`curl -sI https://brilliant-cat-c5b6e9.netlify.app/`)

```
content-security-policy: default-src 'self'; script-src 'self' 'sha256-Du+OJKJSbdUgz5nrHeWWINvez6XKDDU/tyj/5c2uvwo='; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests
strict-transport-security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=(), browsing-topics=()
cross-origin-opener-policy: same-origin
```

O arquivo `dist/_headers` é **gerado** pelo build (`headers_file()` em `build.py`); não edite à mão.
No `*.netlify.app` o Netlify substitui o HSTS pelo dele (o mesmo valor com `preload`), sem
duplicar o cabeçalho.

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
| 9 | Mensagem pré-preenchida do WhatsApp | Sempre codificada com `urllib.parse.quote` no build (o carrinho da tabela, que usava `encodeURIComponent`, foi removido) |
| 10 | Dependências de desenvolvimento com 2 vulnerabilidades moderadas (`uuid` via linkinator) | `npm audit fix` → 0 |
| 11 | Selo "Powered by Netlify" injetado nas páginas, com script e estilo inline (gerava erros de CSP no console e baixava Boas Práticas do Lighthouse para 93) | Desativado nas configurações do site no Netlify (`built_with_badge_enabled: false`); o Netlify ainda insere só um comentário HTML, inofensivo |
| 12 | `JSON-LD` dentro de `<script>` | Gerado por `json.dumps` e com `<` escapado como `\u003c` (nenhum texto consegue fechar a tag) |

**Segredos:** o token de deploy do Netlify fica só na variável de ambiente `NETLIFY_AUTH_TOKEN`
de quem publica. Foi feita uma varredura no projeto (padrões de token/chave e o valor literal da
variável): nada encontrado. `.gitignore` exclui `node_modules`, `dist` e logs.

**Privacidade (LGPD):** o site não grava cookies, não usa analytics e não chama terceiros, a não ser
o mapa, que só carrega quando o visitante pede. Por isso não precisa de banner de cookies hoje.
A [política de privacidade](https://brilliant-cat-c5b6e9.netlify.app/politica-de-privacidade/)
descreve isso; se entrar analytics, atualize a política (seção Cookies) e a CSP antes.

**Redirecionamentos:** `dist/_redirects` (gerado pelo build) leva `/tabela-de-precos/` para
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
2. Em `page()` (`build.py`), antes de `main.js`, inclua
   `<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX"></script>` e
   `<script src="/assets/js/ga.js" defer></script>`.
3. Em `CSP` (`build.py`), acrescente:
   - `script-src … https://www.googletagmanager.com`
   - `connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com`
   - `img-src 'self' data: https://*.google-analytics.com https://www.googletagmanager.com`
4. Com analytics vem a LGPD: publique uma política de privacidade e, se usar cookies de anúncio,
   um banner de consentimento.
5. Os cliques em WhatsApp, telefone e mapa já têm `data-track="…"`, e `main.js` os envia ao
   `dataLayer` quando ele existe; com o GA4 ativo, viram eventos sem mudar o HTML.
