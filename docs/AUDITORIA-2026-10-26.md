# Auditoria completa do site — 26/10/2026

- **Site:** Laboratório Dental Araújo · https://brilliant-cat-c5b6e9.netlify.app
- **Projeto:** `/workspace/site-clone` (gerador `_build/build.py` → `dist/`)
- **Backup anterior à auditoria:** `/workspace/site-clone-v3-backup/`
- **Deploy final:** `6adf7216510ccc34dabc2f82` (produção, 26/10/2026)

---

## 1. Resumo

O site já estava em bom estado: nenhum link quebrado, nenhum erro de JavaScript, nenhuma
violação de acessibilidade, cabeçalhos de segurança nota A+ e nenhum preço publicado.
A auditoria encontrou **18 pontos**: **nenhum crítico ou alto**, 6 médios, 8 baixos e
4 informativos. **11 foram corrigidos e verificados no ar**. Os outros 7 dependem do laboratório
ou do dono do site, ou foram aceitos como estão (com justificativa).

| Severidade | Encontrados | Corrigidos | Pendentes / aceitos |
|---|---:|---:|---:|
| Crítica | 0 | 0 | 0 |
| Alta | 0 | 0 | 0 |
| Média | 6 | 4 | 2 (dependem do laboratório) |
| Baixa | 8 | 6 | 2 (dependem do laboratório) |
| Informativa | 4 | 1 | 3 (aceitos ou opcionais) |
| **Total** | **18** | **11** | **7** |

**Os mais importantes, em linguagem simples:**

1. **Endereços duplicados.** Cada página também abria em `/…/index.html` (ex.:
   `/sobre/index.html`), com o mesmo conteúdo e status 200. Para o Google isso é conteúdo duplicado.
   Agora esses endereços levam (301) para a URL oficial, num único salto, nas 20 páginas.
2. **Aviso de "espaço reservado" visível ao público.** Na página Sobre aparecia um quadro
   "Foto real: recepção ou fachada do Ed. Mesbla — Espaço reservado para foto do laboratório".
   Ele saiu do site público. No código, a marcação ficou como comentário, pronta para a foto real.
3. **Testes que não reprovavam.** O verificador de SEO (`qa_seo.py`) só imprimia problemas, sem
   nunca falhar. Agora ele falha. Também foram criados dois testes novos e permanentes:
   `qa_rotas.py` (rotas, redirecionamentos, canonical, sitemap, links, âncoras e 404, no ar ou
   local) e `qa_interacao.py` (âncoras dentro de acordeões, site sem JavaScript, movimento
   reduzido e menu por teclado).
4. **Pequeno "pulo" de layout nas páginas de serviço** (CLS 0,022), causado pela fonte itálica do
   título, que carregava depois. A fonte agora é pré-carregada e o CLS caiu para **0**.
5. **Página de erro com status errado.** Acessada direto, `/404.html` e `/404` respondiam 200.
   Agora respondem 404.

**Pedido incluído nesta rodada:** o crédito **"Desenvolvido por gandra.tech"** está no rodapé de
todas as páginas, com link para https://www.gandra.tech/ (abre em nova aba, `rel="noopener"`).
Fica discreto, na linha de base do rodapé. O contraste é 11,9:1 no link e 6,8:1 no texto, acima do
AA. O link responde 200 (curl, linkinator e `qa_rotas --externos`).

---

## 2. Metodologia

Tudo foi feito em ordem, com backup antes (`/workspace/site-clone-v3-backup/`). Antes de ir para a
produção, as mudanças de rota foram testadas em **deploys de rascunho** (draft) do Netlify, que
não alteram o site publicado.

| Área | Como foi verificado | Ferramenta |
|---|---|---|
| Rotas e URLs | Rastreamento a partir do `sitemap.xml` publicado. Foram verificadas 159 referências internas (links, imagens, `srcset`, ícones, URLs do JSON-LD e dos `llms*.txt`), 34 âncoras e 23 links externos. Variantes testadas: sem barra, MAIÚSCULAS, `/index.html`, http, www. Também: cadeias de redirecionamento, 404 real e arquivos internos expostos | `tools/qa_rotas.py` (novo), curl, linkinator |
| SEO técnico | Títulos e descrições (tamanho e unicidade), um H1, hierarquia de títulos, `alt`, canonical/og:url, breadcrumbs × URL, imagem OG (tamanho real × declarado), datas | `tools/qa_seo.py`, script de apoio |
| Dados estruturados | As 20 páginas passaram pelo validador oficial do schema.org | validator.schema.org |
| Segurança | Cabeçalhos no ar, Mozilla Observatory, `rel` dos links `_blank`, conteúdo de `dist/` (tokens, `.md`, `.py`, mapas, PDF antigo), `npm audit` | curl, Observatory API, `qa_rotas.py` |
| Front-end | Console em 21 URLs × 3 larguras. Sem JS, movimento reduzido, âncoras em acordeões, menu móvel por teclado. axe em 21 páginas × 2 larguras. Lighthouse móvel e desktop no ar. Tamanho e dimensões das imagens. Cache | `qa_paginas.py`, `qa_interacao.py` (novo), `a11y.mjs`, Lighthouse 12 |
| Conteúdo | Ausência de "R$" e de valores. Telefones, endereço e horário em todas as páginas e no JSON-LD. Ortografia (corretor pt) e expressões genéricas | `qa_sem_precos.py`, scripts de apoio, pyspellchecker |
| Build e código | pyflakes, ESLint, stylelint, html-validate. Build reprodutível (dois builds, comparação de hash de todos os arquivos). Código e CSS sem uso | npm scripts, md5sum, script de apoio |

**Limites:** o teste de "pesquisa aprimorada" do Google (Rich Results Test) exige navegador
interativo e não foi rodado; o validador do schema.org cobre a sintaxe e o vocabulário. A
variante `http://` não pôde ser testada do servidor de trabalho, porque a porta 80 é bloqueada.
Ela foi conferida por um leitor externo, que chegou à versão https. A variante `www.` não se
aplica ao endereço `.netlify.app`, que não tem certificado para www; volta a valer com domínio
próprio.

---

## 3. Achados

Severidade: **Média** afeta SEO, a imagem do site ou a confiabilidade dos testes. **Baixa** é
um ajuste fino. **Informativa** não é defeito; é registro ou decisão.

| ID | Área | Severidade | Achado | Status |
|---|---|---|---|---|
| R1 | Rotas | Média | `/…/index.html` respondia 200 nas 20 páginas (conteúdo duplicado) | ✅ Corrigido |
| R2 | Rotas | Baixa | `/404.html` e `/404` respondiam 200 | ✅ Corrigido |
| F1 | Front-end | Média | Quadro "Espaço reservado para foto do laboratório" visível em /sobre/ | ✅ Corrigido |
| Q1 | Testes | Média | `qa_seo.py` nunca reprovava (sempre saía com código 0) | ✅ Corrigido |
| Q2 | Testes | Média | Não havia teste automático de rotas e redirecionamentos no ar, âncoras, modo sem JS ou menu por teclado. O pyflakes não fazia parte do `lint` | ✅ Corrigido |
| F2 | Desempenho | Baixa | CLS 0,022 nas páginas de serviço (fonte itálica do H1 não pré-carregada) | ✅ Corrigido |
| S1 | SEO | Baixa | 3 meta descriptions acima de 160 caracteres (home 165, implante 167, artigo do protocolo 161) | ✅ Corrigido |
| S2 | SEO | Baixa | `lastmod` e `dateModified` = data do build em todas as páginas. Na política e nos termos, divergiam do "Atualizado em 24/10/2026" visível | ✅ Corrigido |
| F3 | Arquivos | Baixa | 2 arquivos publicados sem uso: `logo-lda.png` e `logo-lda-branco.png` (43 KB) | ✅ Corrigido |
| C1 | Conteúdo | Baixa | Rótulo "Em resumo" repetido em 14 páginas e frase genérica ("em formato direto") | ✅ Corrigido |
| F4 | Código | Informativa | Regra CSS sem uso (`.sec--tight`) | ✅ Corrigido |
| P1 | Domínio | Média | Site no endereço provisório `.netlify.app` | ⏳ Depende do laboratório |
| P2 | Presença | Média | Perfil de Empresa no Google, Search Console e Bing (envio do sitemap) | ⏳ Depende do laboratório |
| P3 | Conteúdo | Baixa | Fotos ilustrativas ainda no lugar de fotos reais (fachada/recepção, trabalhos, antes e depois) | ⏳ Depende do laboratório |
| P4 | Conteúdo | Baixa | Afirmações sem documento de apoio no projeto: "um dos primeiros laboratórios de prótese da cidade", "mais de 35 técnicos", "cerca de 400 m²" | ⏳ Confirmar com o laboratório |
| P5 | SEO | Informativa | Rich Results Test do Google não rodado (exige navegador interativo). Desde 2023, o Google só mostra FAQ em destaque para sites de governo e saúde | ⏳ Opcional |
| P6 | Conteúdo | Informativa | O endereço aparece em formatos diferentes ("sala"/"Sala", "Ed."/"Edifício"), sempre com os mesmos dados | ➖ Aceito |
| P7 | Build | Informativa | `netlify.toml` declara Python 3.12; o build local roda em 3.13. Só vale no deploy via Git | ➖ Aceito |

### Detalhes: evidência, correção e verificação

**R1 — `/…/index.html` com status 200 (Média)**
- *Evidência:* `curl -I https://…/sobre/index.html` → `200`, e o mesmo nas 20 páginas. `qa_rotas.py`
  no ar registrou 20 falhas antes da correção.
- *Correção:* `build.py` ganhou `redirects_index()`, que grava em `_redirects` uma regra forçada
  por página (`/sobre/index.html  /sobre/  301!`). Toda página nova entra sozinha. As regras são
  explícitas (sem curinga) para não arriscar laço na raiz.
- *Verificação:* testado primeiro em rascunho e depois no ar. `/index.html` → 301 `/` e
  `/sobre/index.html` → 301 `/sobre/`, num único salto até um 200. A raiz `/` continua 200, sem
  laço (`curl -L`: 0 redirecionamentos).

**R2 — página de erro com 200 (Baixa)**
- *Evidência:* `/404.html` → 200 e `/404` → 200. A página tinha `noindex`, então o impacto era pequeno.
- *Correção:* `REDIRECTS` recebeu `/404.html /404.html 404!` e `/404 /404.html 404!`.
- *Verificação:* no ar, as duas respondem 404 com a página personalizada (`noindex`).
  `/nao-existe/` também → 404.

**F1 — quadro "espaço reservado" visível (Média)**
- *Evidência:* em /sobre/, dentro do acordeão, o visitante lia "Foto real: recepção ou fachada do
  Ed. Mesbla — Espaço reservado para foto do laboratório". Também aparecia para leitores
  externos e IAs.
- *Correção:* nova chave `MOSTRAR_ESPACOS_FOTO = False`. `photo_slot()` grava só
  `<!-- FOTO REAL: … -->` no HTML. Para revisar o layout, basta mudar a chave localmente.
- *Verificação:* `grep "Espaço reservado" dist/` → 0 ocorrências. O comentário `FOTO REAL` continua
  presente (docs/FOTOS.md atualizado).

**Q1 — `qa_seo.py` não reprovava (Média)**
- *Evidência:* o script terminava com `print('BAD', bad)` e saía com código 0 mesmo com problemas,
  então o `npm run qa` passaria com um H1 duplicado.
- *Correção:* o script sai com código 1 se houver problema ou título/descrição duplicados.
  Também passou a exigir `alt` em todas as imagens, título com 20–60 caracteres e descrição com
  70–160 (a 404 é exceção).
- *Verificação:* foi assim que S1 apareceu. Depois da correção, `BAD []` e código 0.

**Q2 — testes de regressão (Média)**
- *Correção:* dois testes novos e permanentes:
  - `tools/qa_rotas.py [URL] [--externos]`, só com a biblioteca padrão do Python. Verifica:
    - robots e sitemap;
    - em cada página: 200 direto, canonical = og:url = URL do sitemap, 1 H1, títulos e
      descrições únicos, `noopener`, JSON-LD válido;
    - todos os links, imagens, `srcset`, ícones, URLs do JSON-LD e dos `llms*.txt`: 200 sem
      redirecionamento;
    - âncoras `#id`, formato de `tel:`, `mailto:` e `wa.me`;
    - páginas fora do sitemap, 404 com `noindex`, 15 caminhos internos que não podem estar
      públicos;
    - **no ar**: as variantes sem barra, em MAIÚSCULAS e com `/index.html` levam (301) para a
      URL canônica num salto; regras do `_redirects`; cabeçalhos de segurança.
  - `tools/qa_interacao.py [URL]` (Playwright):
    - 34 âncoras (linkadas ou dentro de acordeões): o `<details>` abre e o alvo aparece na tela;
    - 20 páginas sem JS e 20 com movimento reduzido: nenhum conteúdo invisível e nenhuma
      animação infinita;
    - menu móvel por teclado: Tab, Enter, Esc e o foco volta ao botão.
  - Scripts npm:
    - `qa` agora roda build + lint (com **pyflakes**) + SEO + sem-preços + **rotas** + páginas
      + **interação**;
    - `qa:live` (novo) roda rotas com externos, sem-preços e console **no site publicado**;
    - também: `qa:rotas`, `qa:interacao`, `pyflakes` e `links:externos`.
- *Verificação:* os testes novos acharam R1 e R2. Depois das correções: 0 falhas, local e no ar.

**F2 — CLS 0,022 nas páginas de serviço (Baixa)**
- *Evidência:* Lighthouse móvel em `/servicos/zirconia-e-max/`: CLS 0,022. O elemento deslocado era
  `.phero__text > .intro-2`. Causa: o trecho em itálico do H1 ("em Belo Horizonte", Newsreader
  itálica) carregava depois da primeira pintura e mudava a quebra de linha.
- *Correção:* `newsreader-400-italic` entrou na lista `FONTS` de pré-carregamento (+22 KB, que já
  eram baixados de qualquer forma).
- *Verificação:* local, CLS 0,022 → 0 (duas medições). No ar: CLS 0 em home, serviço e sobre, no
  celular e no desktop. Nenhum aviso de "preload sem uso" no console.

**S1 — descrições longas (Baixa)**
- *Correção:* as três foram reescritas sem perder informação ("envio para todo o Brasil" virou
  "envio ao Brasil"; "Entenda as etapas" virou "As etapas").
- *Verificação:* agora têm 156, 158 e 153 caracteres; `qa_seo` exige 70–160.

**S2 — datas de modificação (Baixa)**
- *Correção:* nova tabela `MODIFICADO` no `build.py`. Política e termos ficam com `2026-10-24`
  no sitemap e no JSON-LD, igual ao "Atualizado em" visível. As demais páginas usam `TODAY`.
- *Verificação:* `sitemap.xml` tem 18 URLs com 2026-10-26 e 2 com 2026-10-24, e o `dateModified`
  bate com elas.

**F3 — arquivos sem uso publicados (Baixa)**
- *Evidência:* comparação de cada arquivo de `dist/` com todas as referências (HTML, CSS, JS,
  manifest, txt, xml). Só os dois PNG do logotipo não eram usados no site; eram apenas a matriz
  do `tools/og.py`.
- *Correção:* os dois foram movidos para `_build/fontes/marca/` (fora do site) e o `og.py` foi
  ajustado.
- *Verificação:* a imagem OG regerada ficou idêntica pixel a pixel. Nenhum arquivo de `dist/` ficou
  sem referência.

**C1 — rótulo repetitivo (Baixa)**
- *Correção:* no quadro lateral, "Em resumo" virou "O laboratório". Na ficha técnica, o rótulo
  virou "Dados" e o subtítulo, "Endereço, equipe, prazos e garantia do laboratório."

**F4 — CSS sem uso (Informativa).** Removida `.sec--tight`. `.sr-only` (utilitário padrão de
acessibilidade) e os estilos do antes/depois e do espaço de foto foram mantidos de propósito: são
de componentes prontos e desligados.

**P1 a P7 — pendentes ou aceitos:** ver seção 5.

---

## 4. Verificado sem problemas

| Item | Resultado |
|---|---|
| Barra final | `/sobre` → 301 `/sobre/` (um salto) em todas as páginas |
| MAIÚSCULAS | `/SOBRE/` e `/Sobre/` → 301 `/sobre/` (Netlify) |
| Tabela de preços antiga | `/tabela-de-precos` e `/tabela-de-precos/` → 301 `/contato/` (200, um salto); PDF antigo → 404 |
| http → https | Redireciona para https; HSTS com `max-age` de 1 ano, `includeSubDomains` e `preload` |
| Canonical, og:url e hreflang | canonical = og:url = URL final 200 nas 20 páginas. Sem hreflang (site só em pt-BR, `lang="pt-BR"`), o que é correto |
| Sitemap e robots | 20 URLs, todas 200, canônicas, com barra e `lastmod` AAAA-MM-DD; robots libera buscadores e IAs e aponta o sitemap |
| Links internos | 159 referências, 0 quebradas, 0 passando por redirecionamento; 34 âncoras existem e abrem o acordeão |
| Links externos | 23, todos 200: WhatsApp (2 números), Google Maps, Instagram, Facebook, gov.br/ANPD, Planalto (LGPD), políticas de privacidade, gandra.tech |
| `tel:`, `mailto:`, `wa.me` | Formato E.164 (`tel:+5531…`), e-mail válido, mensagens do WhatsApp codificadas (UTF-8 com %) |
| JSON-LD | schema.org: **0 erros e 0 avisos nas 20 páginas**. Breadcrumbs batem com a URL. URLs internas do JSON-LD respondem 200 |
| `llms.txt` e `llms-full.txt` | Todas as URLs respondem 200 |
| Imagem OG | 1200×630 reais = declarados, 89 KB, em todas as páginas |
| Títulos e H1 | 20 títulos únicos (40–53 caracteres), 1 H1 por página, sem saltos de hierarquia, todas as imagens com `alt` |
| Cabeçalhos | CSP sem `unsafe-inline`, HSTS, nosniff, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP |
| Mozilla Observatory | **A+ (130/100), 12 de 12 testes** (26/10/2026, depois do deploy) |
| `target="_blank"` | Todos com `rel="noopener"` (os do laboratório também com `noreferrer`) |
| `dist/` | Sem tokens, `.md`, `.py`, `.map`, PDF ou dados de preço. `_headers` e `_redirects` → 404 no ar |
| Dependências | `npm audit`: 0 vulnerabilidades |
| Conteúdo misto | Nenhuma referência `http://` |
| Telefones, endereço e horário | Iguais em todas as páginas, no rodapé, no `llms*.txt` e no JSON-LD. Pedidos: (31) 3271-9766, (31) 3271-9688 e WhatsApp (31) 98652-1387. Financeiro: (31) 3212-1384 e WhatsApp (31) 98652-1201. Seg. a sex., 8h–11h30 e 12h45–18h. Av. Afonso Pena, 262, sala 1602, CEP 30130-923 |
| Preços | Nenhum "R$" nem valor (`qa_sem_precos`, local e no ar) |
| Ortografia | Corretor pt: só termos técnicos corretos (zircônia, troquel, overdenture…) e slugs de URL |
| Imagens | 136 `<img>`, todas com `width`/`height`; só o logotipo do topo é carregado sem `lazy` (correto); nenhuma imagem acima de 150 KB; WebP em 640 e 1200 px |
| Cache | CSS/JS/fontes com 1 ano `immutable` (CSS e JS têm `?v=hash`); imagens e ícones 7 dias; HTML com revalidação |
| Build | Reprodutível (dois builds seguidos, hashes idênticos); pyflakes, ESLint, stylelint e html-validate sem erros |

---

## 5. Pendências (dependem do laboratório ou do dono do site)

1. **Domínio próprio (P1).** Ligar, por exemplo, `www.dentalaraujo.com.br` no Netlify e trocar
   `BASE` no `build.py` (passo a passo no README). Depois, rodar
   `python3 tools/qa_rotas.py https://www.dentalaraujo.com.br` e conferir também `www` × sem `www`.
2. **Google e Bing (P2).** Criar ou verificar o Perfil de Empresa no Google com o mesmo nome,
   endereço, telefone e horário do site. Cadastrar o site no Search Console e no Bing Webmaster
   e enviar o `sitemap.xml`.
3. **Fotos reais (P3).** Fachada ou recepção (para /sobre/), equipe na bancada, trabalhos do
   laboratório e, se houver autorização, pares de antes e depois. Os pontos de troca estão em
   `docs/FOTOS.md`.
4. **Confirmar dados (P4).** "Um dos primeiros laboratórios de prótese da cidade", "mais de 35
   técnicos" e "cerca de 400 m²". Se algum não for exato, ajustar em `_build/content/` e no
   `build.py`.
5. **Opcional (P5).** Rodar o [Teste de pesquisa aprimorada](https://search.google.com/test/rich-results)
   numa página de serviço e num artigo depois do domínio próprio.

Aceitos sem mudança: P6 (formatos do endereço; os dados são os mesmos) e P7 (versão do Python no
`netlify.toml`, usada só no deploy via Git).

---

## 6. Resultados finais dos testes (26/10/2026, deploy `6adf7216510ccc34dabc2f82`)

| Teste | Resultado |
|---|---|
| `npm run qa` (build, html-validate, stylelint, ESLint, pyflakes, qa_seo, qa_sem_precos, qa_rotas, qa_paginas, qa_interacao) | **0 falhas** |
| `npm run qa:live` (qa_rotas no ar + 23 externos, qa_sem_precos --live, qa_paginas no ar) | **0 falhas, 0 avisos** |
| `qa_interacao.py` no ar | **0 falhas** (34 âncoras, 20 páginas sem JS, 20 com movimento reduzido, menu) |
| axe-core (21 páginas × 2 larguras + menu aberto) | **0 violações** |
| linkinator (local + gandra.tech) | **74 links, todos 200** |
| schema.org (20 páginas) | **0 erros, 0 avisos** |
| Mozilla Observatory | **A+, 130/100, 12/12** |
| `npm audit` | 0 vulnerabilidades |
| Console (21 URLs × 1440/1366/390 px, no ar) | 0 erros, 0 avisos |

**Lighthouse 12 no ar** (desempenho / acessibilidade / boas práticas / SEO):

| Página | Celular | Desktop |
|---|---|---|
| Home | 99 / 100 / 100 / 100 · LCP 1,8 s · CLS 0 | 100 / 100 / 100 / 100 · LCP 0,5 s · CLS 0 |
| Zircônia e E-Max | 100 / 100 / 100 / 100 · LCP 1,6 s · **CLS 0** (era 0,022) | 100 / 100 / 100 / 100 · LCP 0,5 s · CLS 0 |
| Sobre | 100 / 100 / 100 / 100 · LCP 1,6 s · CLS 0 | 100 / 100 / 100 / 100 · LCP 0,4 s · CLS 0 |

---

## 7. Arquivos alterados nesta auditoria

- `_build/build.py`:
  - `redirects_index()`;
  - regras 404 em `REDIRECTS`;
  - `MODIFICADO`/`modificado()`;
  - `MOSTRAR_ESPACOS_FOTO`;
  - `FONTS` com a itálica;
  - crédito no `footer()`;
  - descrição da home;
  - rótulos "Dados" e "O laboratório".
- `_build/content/servicos.py` e `_build/content/blog.py`: duas descrições.
- `_build/static/assets/css/style.css`: `.footer__sign` e `.footer__credit`; removida `.sec--tight`.
- `_build/static/assets/img/marca/*.png` → `_build/fontes/marca/`; `tools/og.py` com o novo caminho.
- `tools/qa_seo.py`: agora reprova e tem novas regras. Novos: `tools/qa_rotas.py` e
  `tools/qa_interacao.py`.
- `package.json` (2.1.0): `qa` ampliado; novos `qa:live`, `qa:rotas`, `qa:interacao`, `pyflakes` e
  `links:externos`.
- Documentação: README, docs/QUALIDADE.md, docs/ARQUITETURA.md, docs/FOTOS.md, docs/SEGURANCA.md e
  este relatório.
- `tools/relatorio_pdf.py` (novo): gera o PDF deste relatório (`python3 tools/relatorio_pdf.py docs/AUDITORIA-2026-10-26.md /workspace/AUDITORIA-2026-10-26.pdf`).
- Capturas: `screenshots/auditoria-rodape-credito-{d,t,m}.png` (rodapé com o crédito).
