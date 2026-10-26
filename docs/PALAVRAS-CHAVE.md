# Palavras-chave e SEO on-page — Laboratório Dental Araújo

Data: 26/10/2026 · Site: https://brilliant-cat-c5b6e9.netlify.app · Deploy de produção: `6adf7dccf104b32829080f81` (o anterior do mesmo dia, `6adf7c5b5d2b2742bc27ca9f`, foi o primeiro com estas mudanças)
Backup anterior às mudanças: `/workspace/site-clone-v4-backup/`

## 1. Resumo

- **Público:** cirurgiões-dentistas e clínicas (B2B). Foco em Belo Horizonte e Grande BH, Minas Gerais (coleta e entrega) e envio de todo o Brasil.
- **O que foi feito:**
    - mapa de palavras-chave com 1 termo principal por página, sem canibalização;
    - ajuste de títulos, descrições, H2, FAQ, JSON-LD e `llms.txt`;
    - 3 artigos novos com fontes;
    - modelo de requisição em PDF.
- **Regras seguidas:**
    - sem preços;
    - sem páginas "porta" por cidade;
    - sem repetição forçada de termos;
    - fatos técnicos só com fonte citada na própria página.
- **Medido × estimado:** este documento **não tem volume de busca**. Não havia ferramenta com dados reais de volume disponível, e nenhum número foi inventado. O que foi **medido** é se o termo aparece no autocompletar do Google: 135 consultas, com os arquivos em `/workspace/kw/`. Também foi medido quem aparece nos resultados de busca. A **prioridade** de cada termo é uma **estimativa qualitativa**, feita por intenção (comercial local, comercial nacional ou informacional técnica) e pela aderência ao que o laboratório faz.

## 2. Método e fontes

| Fonte | O que deu | Limite |
|---|---|---|
| Google Autocomplete (`suggestqueries.google.com`, `hl=pt-BR`, `gl=br`), 4 lotes, 135 consultas | Termos que existem nas buscas reais e as variações mais comuns | Não informa volume. Algumas consultas voltam vazias, entre elas "coroa de zircônia", "coroa metalocerâmica" e "coroa sobre implante" |
| Pesquisa web (resultados de busca) | Concorrentes que aparecem para "laboratório de prótese dentária BH" e termos de serviço | Visão aproximada, não é a página do Google em tempo real |
| Google SERP direto | — | Pediu captcha em navegador automático. **Não foi contornado** |
| Bing em navegador automático | — | Trouxe resultados irrelevantes; descartado |
| "As pessoas também perguntam" (PAA) | — | Não ficou acessível sem o Google SERP. As perguntas da FAQ vieram do autocompletar nas formas "X ou Y" e "o que é" |
| Concorrentes | **BH:** Dentatech, Glaucia Galvão, Amauri, Labordent, TECLAB, 3D Dental Lab, Exclusive Dent. **Nacionais:** Shiratori, Protética Dente, Ultra, Hirama | Quase todos se posicionam como "fluxo digital/CAD-CAM" |
| Lei nº 6.710/1979 (planalto.gov.br) | Art. 4º: o técnico não pode atender o paciente diretamente nem fazer propaganda ao público em geral. Parágrafo único: a propaganda dirigida a dentistas deve trazer o nome do laboratório, o responsável e o número de inscrição no CRO | — |
| Literatura (resumos conferidos no Europe PMC e nos sites das revistas) | Sailer 2015, Pjetursson 2015 e 2018, Hill 2014, Rev Odontol UNESP 2019, Arch Health Invest 2017 | O PubMed bloqueia leitura automática (403/203); o link continua correto |

**Posicionamento resultante:**

- O LDA não disputa o termo "digital", e o site **não afirma** que o laboratório trabalha com STL ou fluxo digital.
- Os diferenciais usados são:
    - 50 anos de história (desde 1976);
    - linha analógica completa, inclusive removíveis (PPR, PT, flexível);
    - coleta em MG;
    - envio de todo o Brasil.

**Termos excluídos de propósito:**

- termos de preço, como "valor", "preço" e "tabela de preços" (o site não publica valores);
- termos de paciente, como "dentadura", "dente de zircônia", "lente de contato dental" e "perto de mim" com intenção de paciente. A Lei 6.710 proíbe propaganda ao público em geral;
- "prótese dentária fixa gratuita".

## 3. Mapa de palavras-chave (1 principal por URL)

Prioridade (estimada):

- **A:** comercial e local, com alta aderência ao laboratório;
- **B:** comercial, por serviço;
- **C:** informacional, para dentistas.

| URL | Principal (prioridade) | Secundárias | Evidência (autocompletar) |
|---|---|---|---|
| `/` | laboratório de prótese dentária em BH / Belo Horizonte (A) | laboratório de prótese em Belo Horizonte, prótese dentária BH, desde 1976, Grande BH | "laboratorio de protese dentaria bh", "laboratório de prótese dentária em belo horizonte", "protese dentaria bh" |
| `/servicos/` | tipos de prótese dentária / serviços de laboratório (B) | laboratório de prótese completo | "laboratório de prótese dentária" + serviços |
| `/servicos/protese-sobre-implante/` | prótese protocolo sobre implante (B) | barra de protocolo, overdenture com barra clip, guia cirúrgico para implante, coroa sobre implante | "barra de protocolo", "overdenture barra clip", "guia cirúrgico para implante protocolo" |
| `/servicos/zirconia-e-max/` | coroa de zircônia (B) | coroa e faceta em E-Max, ponte fixa de zircônia, dissilicato de lítio, metal free | "ponte fixa de zirconia", "faceta e max", "dissilicato de litio", "metal free protese" |
| `/servicos/metaloceramica/` | coroa metalocerâmica (B) | ponte metalocerâmica, núcleo metálico fundido, metalocerâmica sobre implante, coroa veneer | "metalocerâmica sobre implante", "núcleo metálico fundido" |
| `/servicos/protese-parcial-removivel-ppr/` | PPR prótese parcial removível (B) | armação metálica de PPR, PPR Roach, grampo Roach | "ppr prótese parcial removível", "armação ppr", "ppr roach", "grampo roach ppr" |
| `/servicos/protese-total/` | prótese total removível (B) | PTR, prótese total caracterizada, palato incolor, STG | "prótese total removível", "prótese total caracterizada", "protese total palato incolor", "protese total stg" |
| `/servicos/protese-flexivel-flexite/` | prótese flexível (B) | Flexite unilateral, parcial provisória em acrílico, prótese sem grampo metálico | "flexite unilateral", "prótese flexível" |
| `/servicos/resinas-e-provisorios/` | coroa de resina Ceramage (B) | coroa provisória de laboratório, ponte com fibra, provisório em acrílico | "resina ceramage shofu", "provisório sobre implante" |
| `/servicos/placas-de-bruxismo-e-ortodontia/` | placa de bruxismo (laboratório) (B) | placa miorrelaxante, placa de clareamento, protetor bucal personalizado, contenção ortodôntica, aparelho anti-ronco | "placa de bruxismo laboratorio", "laboratório que faz placa de bruxismo", "placa miorrelaxante acrilica", "protetor bucal personalizado dentista", "contenção ortodôntica estética" |
| `/envio-para-todo-brasil/` | laboratório de prótese que atende todo o Brasil (A) | coleta em BH, Grande BH (Contagem, Betim) e MG; envio pelos Correios | Variações por cidade: "laboratório de prótese dentária em [cidade]" e "laboratorio de protese dentaria contagem/betim/divinópolis/ipatinga/juiz de fora/montes claros/uberlândia" |
| `/sobre/` | Laboratório Dental Araújo (marca) | história, desde 1976 | "laboratório dental araújo" já aparece no autocompletar |
| `/perguntas-frequentes/` | dúvidas sobre laboratório de prótese | prazo, garantia, envio, requisição, atendimento a pacientes | — |
| `/contato/` | contato Laboratório Dental Araújo | telefone, WhatsApp, endereço | — |
| `/blog/zirconia-ou-e-max-qual-indicar/` | zircônia ou E-Max (C) | dissilicato de lítio x zircônia, faceta de E-Max ou zircônia | "e max ou zirconia", "dissilicato de litio x zirconia" |
| `/blog/metaloceramica-ou-zirconia/` **(novo)** | metalocerâmica ou zircônia (C) | metalocerâmica x zircônia, ponte de zircônia ou metalocerâmica, coroa de zircônia sobre implante | "metalocerâmica ou zircônia" |
| `/blog/ppr-ou-protese-flexivel/` **(novo)** | PPR ou prótese flexível (C) | prótese flexível ou PPR, indicação da prótese flexível | "protese flexivel ou ppr" |
| `/blog/requisicao-para-laboratorio-de-protese/` **(novo)** | requisição para laboratório de prótese (C) | modelo de requisição de prótese, requisição em PDF, ordem de serviço | "requisição para laboratório de prótese dentária pdf" |
| `/blog/como-enviar-um-caso-para-o-laboratorio-de-protese/` | como enviar caso para laboratório de prótese (C) | enviar e embalar moldagem, coleta em BH | — |
| `/blog/barra-de-protocolo-etapas-e-prazos/` | prótese protocolo: etapas (C) | barra de protocolo passo a passo, moldagem de transferência, assentamento passivo | "prótese protocolo etapas", "moldagem de transferência protocolo", "assentamento passivo" |

**Regras contra canibalização aplicadas:**

1. **"Requisição"** ficou só no artigo próprio e saiu das secundárias de "como enviar". Os dois se linkam.
2. **"Zircônia × outro material":**
    - **E-Max** fica no artigo E-Max;
    - **metalocerâmica** fica no artigo novo;
    - o serviço de zircônia fica com a intenção comercial ("coroa de zircônia").
3. **"PPR × flexível":**
    - a comparação fica no artigo;
    - cada serviço mantém o próprio termo comercial;
    - "prótese parcial removível flexível" ficou só na página de serviço.
4. **"Prótese protocolo":**
    - a página de serviço fica com o termo comercial;
    - o artigo fica com "etapas".
5. **BH:**
    - só a home disputa "laboratório de prótese dentária em BH";
    - os serviços usam "em BH" apenas no título/H1 como qualificador;
    - **não** foram criadas páginas por cidade.

## 4. O que foi aplicado no site

**Títulos, descrições e textos:**

Páginas principais:

- **Home:**
    - descrição: "Laboratório de prótese dentária em Belo Horizonte desde 1976 … para dentistas de BH, MG e todo o Brasil";
    - texto do topo cita a Grande BH;
    - a seção do blog mostra os 3 artigos mais recentes.
- **Hub `/servicos/`:**
    - descrição: "Tipos de prótese dentária feitos…";
    - ganhou links contextuais para os 3 artigos de comparação.

Serviços (descrição, H2 e FAQ revisados com os termos do mapa):

- **Protocolo:**
    - H2 "Laboratório de prótese protocolo em BH" e "Protocolo ou overdenture com barra clips?";
    - FAQ "etapas" e "o que enviar".
- **Zircônia:**
    - H2 "Coroa de zircônia e E-Max feitas em BH";
    - FAQ "Zircônia ou E-Max", "ponte fixa", "faceta".
- **Metalocerâmica:**
    - FAQ "metalocerâmica ou zircônia" e "sobre implante";
    - núcleo metálico fundido.
- **PPR:**
    - H2 "Laboratório de PPR em Belo Horizonte" e "Armação metálica Roach: o que é".
- **Prótese total:**
    - o título saiu de "Dentadura" para "Prótese Total Removível (PTR)";
    - entrou "prótese total caracterizada" (Coloform);
    - FAQ "simples × palato incolor".
- **Flexível:**
    - FAQ "unilateral";
    - link para o artigo PPR × flexível.
- **Resinas:**
    - FAQ "O que é a resina Ceramage?" (Shofu).
- **Placas:**
    - H2 "Laboratório que faz placa de bruxismo em BH" e "Protetor bucal personalizado";
    - FAQ "rígida ou macia".

Blog e envio:

- **Blog:**
    - artigo de protocolo renomeado para "Prótese protocolo: etapas e prazos";
    - índice ordenado do mais novo para o mais antigo;
    - "Leia também" mostra 2 artigos escolhidos (`related_posts`) + o serviço.
- **Envio:**
    - cita coleta em BH, Contagem, Betim e região metropolitana;
    - link para o modelo de requisição.

**Perguntas frequentes (novas):**

- "Vocês fazem coleta em Contagem, Betim e na Grande BH?"
- "O laboratório atende pacientes diretamente?" A resposta é não, com base na Lei 6.710, art. 4º.
- "Vocês fazem overdenture com barra clips?"
- A resposta sobre requisição passou a ter link para o modelo em PDF.

**Dados estruturados (JSON-LD):**

- `areaServed` (laboratório e cada `Service`): Belo Horizonte, Região Metropolitana de Belo Horizonte, Contagem, Betim, Minas Gerais e Brasil.
- `knowsAbout` passou de 11 para 21 itens. Entre os novos:
    - ponte fixa de zircônia;
    - E-Max (dissilicato de lítio);
    - núcleo metálico fundido;
    - overdenture com barra clips;
    - guia cirúrgico;
    - PPR Roach;
    - Ceramage;
    - protetor bucal;
    - anti-ronco.
- `serviceType` foi revisado nos serviços alterados.
- `Article` ganhou `citation`, com as referências de cada artigo, e `audience` (Cirurgiões-dentistas).

**IA generativa:**

- `llms.txt`:
    - linha de público: só dentistas, sem atendimento a pacientes (Lei 6.710);
    - Grande BH;
    - blog do mais novo para o mais antigo.
- `llms-full.txt`:
    - nova seção "Artigos do blog (resumo e fontes)";
    - respostas da FAQ em texto puro, sem HTML.

**Conteúdo novo (3 itens, todos no sitemap, com links internos e JSON-LD `Article`):**

1. `/blog/metaloceramica-ou-zirconia/` traz dados de sobrevida em 5 anos das revisões sistemáticas:
    - **Sailer 2015**, coroas unitárias: metalocerâmica 94,7%, zircônia 92,1%;
    - **Pjetursson 2015**, pontes: 94,4% × 90,4%;
    - **Pjetursson 2018**, coroas sobre implante: 98,3% × 97,6%.
2. `/blog/ppr-ou-protese-flexivel/` usa como fontes:
    - Rev Odontol UNESP 2019 (poliamida termoinjetada; uso de transição);
    - Arch Health Invest 2017 (alternativa estética e para alergia; incerteza em extremidade livre);
    - Hill 2014 (pouca evidência científica).
3. `/blog/requisicao-para-laboratorio-de-protese/` tem os campos da requisição e o **modelo em PDF para imprimir** (`/assets/docs/requisicao-laboratorio-de-protese.pdf`, A4, 1 página, sem preços). O arquivo publicado é mantido em `src/assets/docs/`.

**Visual:** os textos novos ficaram dentro de acordeões, FAQ ou blog. O topo das páginas continua enxuto.

## 5. Testes (26/10/2026)

| Teste | Resultado |
|---|---|
| `npm run qa`: build, html-validate, stylelint, eslint, pyflakes, qa_seo, qa_sem_precos, qa_rotas, qa_paginas, qa_interacao | **OK, 0 falhas**. Títulos de 40 a 56 caracteres e descrições de 58 a 160; nenhum título ou descrição duplicado |
| axe (WCAG 2.x AA), todas as URLs do sitemap + 404, em 1366 px e 390 px | **0 violações**. Um contraste do botão de download foi corrigido |
| linkinator (links internos) | **0 quebrados** |
| `npm run qa:live` (no ar, inclusive links externos) | **0 falhas**, 2 avisos: o PubMed responde 203 e o DOI da Wiley responde 403 para robôs. Os dois links estão corretos no navegador |
| Lighthouse 12 no ar (desempenho / acessibilidade / boas práticas / SEO) | Home 94/100/100/100 · artigo metalo × zircônia 100/100/100/100 · artigo requisição 100/100/100/100 · serviço protocolo 100/100/100/100 |
| Mozilla Observatory | **A+** (130 pontos, 12/12 testes) |
| Conferência dist × produção | 0 diferenças, desconsiderando o comentário que a Netlify injeta |

## 6. Plano de conteúdo (próximos artigos, 1 a 2 por mês)

| Tema | Termo principal (autocompletar) | Liga para |
|---|---|---|
| Tipos de placa de bruxismo: acrílico, silicone ou acetato | placa de bruxismo acrílico / silicone / acetato | /servicos/placas-de-bruxismo-e-ortodontia/ |
| Protocolo ou overdenture: critérios de indicação | overdenture barra clip | /servicos/protese-sobre-implante/ |
| Núcleo metálico fundido ou pino de fibra de vidro | nucleo metalico fundido ou pino de fibra de vidro | /servicos/metaloceramica/ |
| Moldagem de transferência: moldeira aberta ou fechada | moldagem de transferência protocolo | /blog/barra-de-protocolo-etapas-e-prazos/ |
| Prótese total caracterizada: o que muda | prótese total caracterizada | /servicos/protese-total/ |
| Zircônia monolítica ou estratificada | zirconia monolitica e estratificada | /servicos/zirconia-e-max/ |

Regras para cada artigo novo:

- citar as fontes;
- não usar preços;
- linkar para o serviço comercial;
- não repetir o termo principal de outra página.

## 7. O que depende do dono (fora do código)

1. **Responsável técnico (RT) e CRO no site (obrigatório).** O parágrafo único do art. 4º da Lei 6.710/1979 exige que a propaganda dirigida a dentistas traga o nome do laboratório, o do responsável e o número de inscrição no CRO. Envie nome e número; eles entram no rodapé, no `/sobre/` e no JSON-LD.
2. **Domínio próprio:** veja o README, "Trocar para um domínio próprio". Hoje o site está em `*.netlify.app`, o que limita o ranqueamento.
3. **Google Business Profile:**
    - reivindicar e verificar;
    - categoria principal "Laboratório de prótese dentária";
    - NAP idêntico ao do site;
    - fotos reais;
    - link para o site.
4. **Google Search Console e Bing Webmaster Tools:** verificar o domínio, enviar `sitemap.xml` e acompanhar as consultas reais. É a fonte de volume e cliques que falta neste documento.
5. **Avaliações no Google:** pedir aos dentistas clientes e responder a todas.
6. **Corrigir o NAP em diretórios** que já citam o laboratório. Endereço correto: Av. Afonso Pena, 262, 16º andar, sala 1602, CEP 30130-923, (31) 3271-9766.
    - **Enkontre:** mostra "sl 1908" e está na categoria "Dentistas – Radiologia". Corrigir a sala e a categoria.
    - **Encontra Centro BH:** mostra o telefone (31) 3212-1384, que é o financeiro, e o CEP 30130-000. Corrigir.
    - **InfoIsInfo:** mostra o telefone (31) 3212-138x. Corrigir.
    - **Dentists10 e Assufemg:** conferir.
7. **Confirmar serviços citados no Facebook/diretórios** que não estão no site: In Ceram, Solidex/Artglass, Attachment, Jaqueta, Coroa veneer, Flexidy, Dental D. Só entram no site se ainda forem feitos.
8. **Fotos reais:** veja [FOTOS.md](FOTOS.md).

## 8. Onde mexer no código

- Palavras-chave por página: metadados no `head.html` de cada rota em `src/site/pages/`. Os dos artigos vão para `keywords` do JSON-LD.
- Artigos:
    - `related_posts` define o "Leia também";
    - `refs` define a seção "Referências" e o `citation` do JSON-LD.
- Área atendida e `knowsAbout`: JSON-LD no `head.html` das rotas correspondentes.
- Modelo de requisição: arquivo estático em `src/assets/docs/`; `npm run qa` garante que não há PDF adicional publicado.
