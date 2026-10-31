# Fotos do site: origem, tratamento e onde entra cada uma

Atualizado em 29/10/2026. Desde esta data, o site usa **fotos reais de trabalhos do Laboratório
Dental Araújo** em todos os espaços em que havia uma foto real adequada. Elas aparecem com a
etiqueta **"Foto: LDA"**. Onde não há foto real adequada, continua uma foto de banco (Pexels)
com a etiqueta **"Imagem ilustrativa"**.

## Fontes das fotos reais

1. **Google Drive do laboratório** (fonte principal): pastas por tipo de trabalho. **O nome da
   pasta é a classificação usada.** São 306 fotos e 6 vídeos (cerca de 1,1 GB). Os vídeos não
   foram usados. **Os originais não vão para o `dist/` nem para o zip**; só as versões tratadas.
2. **30 fotos enviadas no chat** (complemento). Delas, 18 foram usadas, depois de tirar
   duplicatas.

| Pasta do Drive | Arquivos | Fotos usadas |
|---|---|---|
| DENTADURAS | 95 fotos + 5 vídeos | 2 |
| BARRA CLIP | 5 | 1 |
| COROA - FACETAS - AFINS | 80 fotos + 1 vídeo | 2 |
| METAL ROACH | 47 | 3 |
| DENTAL D | 23 | 1 |
| FLEXITE | 2 | 2 |
| ODONTOAPNEIA | 1 | 1 |
| 3D | 46 | 1 |
| 3D/Maquinário | 7 | 1 |
| **Drive, total** | **306 fotos** | **14** |
| Fotos do chat | 30 | 18 |
| **Total no site** | | **32** |

No acervo não há fotos de fachada, recepção ou equipe. Por isso o espaço `fachada-recepcao`
de /sobre/ continua reservado, apenas como comentário no HTML.

## Critérios

- **Sem rosto de paciente e sem nome legível.** Fotos com nome escrito no modelo ou com escrita
  cursiva que pode ser um nome ficaram de fora (Drive: COROA - FACETAS - AFINS `IMG_20231006_1749*`/`1750*`, com "Pedro"; DENTAL D `02.9.jpg`).
  Números de caso no gesso são aceitos, mas a preferência foi por fotos sem eles.
- **O material só é afirmado quando há certeza.** "E-Max" aparece só onde o próprio nome do
  arquivo do laboratório diz isso ("Coroa E-Max 001", "Facetas E-max 001"). Nas outras fotos, a
  legenda descreve o que se vê.
- **Duplicatas:** comparação por hash perceptual (pHash + dHash). Entre duas versões da mesma
  foto, ficou a que tem a marca d'água do laboratório.
- **Nenhum filtro de cor.** Fotos reais só passam por rotação conforme o EXIF, recorte e
  redimensionamento. A marca da câmera ("Shot on MI 9T") foi removida pelo recorte na foto da
  barra clip.
- **EXIF/GPS removidos:** cada arquivo é gerado a partir de uma imagem nova, sem metadados.
- **Sem ampliação:** a maior largura é a do recorte original (por isso existem arquivos como
  `-728` e `-1119`).

## Mapa: foto → espaço no site

Todas as 32 fotos também estão na galeria [/trabalhos/](/trabalhos/). Os cartões de serviço e
as capas dos artigos se repetem nas listagens, como "Outros serviços" e "Artigos".

| ID | Origem (pasta) | Categoria | Arquivo (`assets/img/real/`) | Legenda | Onde aparece |
|---|---|---|---|---|---|
| d282 | DENTADURAS | Prótese total | `proteses-totais-cartao-lda` | Próteses totais com gengiva caracterizada | Topo de /servicos/protese-total/ e cartão "Prótese total" na home e em /servicos/; faixa; OG padrão (og-image.jpg) e og-protese-total |
| d270 | DENTADURAS | Prótese total | `proteses-totais-em-oclusao` | Próteses totais em oclusão | Figura de /servicos/protese-total/ |
| d002 | BARRA CLIP | Sobre implantes e barra clip | `barra-clip-sobre-modelo` | Barra clip sobre o modelo | Figura de /servicos/protese-sobre-implante/; faixa |
| d005 | COROA - FACETAS - AFINS | Metalocerâmica | `coroas-e-max-modelo-caixa-lda` | Aplicação de porcelana (metalocerâmica) | Topo de /servicos/metaloceramica/; faixa da home; galeria /trabalhos/ (metalocerâmica). Obs.: pasta do Drive dizia E-Max, dono corrigiu. |
| d006 | COROA - FACETAS - AFINS | Coroas e facetas | `facetas-e-max-sobre-modelo` | Facetas em E-Max | Figura de /servicos/zirconia-e-max/; faixa |
| d123 | METAL ROACH | PPR: Metal Roach e Dental D | `armacoes-metal-roach-modelos` | Armações metálicas de PPR (Metal Roach) | Faixa da home; galeria |
| d130 | METAL ROACH | PPR: Metal Roach e Dental D | `ppr-pronta-armacao-metalica` | PPR pronta, com armação metálica | Figura de /servicos/protese-parcial-removivel-ppr/; faixa |
| d131 | METAL ROACH | PPR: Metal Roach e Dental D | `ppr-pronta-vista-de-cima` | PPR pronta, vista de cima | Capa do artigo "PPR ou prótese flexível" |
| d143 | DENTAL D | PPR: Metal Roach e Dental D | `grampo-estetico-dental-d` | Grampo estético Dental D | Só galeria |
| d156 | FLEXITE | Prótese flexível (Flexite) | `protese-flexivel-flexite` | Prótese flexível (Flexite) | Topo de /servicos/protese-flexivel-flexite/ e cartão; faixa |
| d157 | FLEXITE | Prótese flexível (Flexite) | `protese-flexivel-flexite-lateral` | Prótese flexível (Flexite), vista lateral | Figura de /servicos/protese-flexivel-flexite/ |
| d085 | ODONTOAPNEIA | Placas, aparelhos e anti-ronco | `aparelho-odontoapneia` | Aparelho anti-ronco (Odonto Apneia) | Topo de /servicos/placas-de-bruxismo-e-ortodontia/ e cartão; faixa |
| d166 | 3D | Bancada e impressão 3D | `modelos-impressos-3d` | Modelos impressos em 3D | Faixa; galeria |
| d207 | 3D/Maquinário | Bancada e impressão 3D | `impressoras-3d-laboratorio` | Impressoras 3D do laboratório | Figura de /sobre/ (imagem do laboratório no JSON-LD) |
| 70c0 | chat (curadas) | Prótese total | `proteses-totais-gengiva-caracterizada` | Próteses totais com gengiva caracterizada | Topo da home (LCP) e imagem principal da home no JSON-LD |
| 0153 | chat (curadas) | Prótese total | `proteses-totais-sobre-modelos` | Próteses totais montadas sobre os modelos | Só galeria |
| 0f03 | chat (curadas) | Sobre implantes e barra clip | `protese-sobre-implantes-e-modelo` | Prótese sobre implantes e modelo com componentes | Topo de /servicos/protese-sobre-implante/ e cartão; faixa |
| 445f | chat (curadas) | Sobre implantes e barra clip | `protese-superior-sobre-implantes` | Prótese superior sobre implantes e modelo com análogos | Capa do artigo "Barra de protocolo" |
| 72c6 | chat (curadas) | Coroas e facetas | `coroas-anteriores-modelos-articulados` | Coroas anteriores sobre modelos articulados | Só galeria |
| 1ea3 | chat (curadas) | Coroas e facetas | `coroas-anteriores-gengiva-artificial` | E-max (lentes de contato) | Galeria /trabalhos/ (coroas e facetas) |
| 280c | chat (curadas) | Coroas e facetas | `coroas-anteriores-superficie-espelhada` | Coroas anteriores prontas | Capa do artigo "Zircônia ou E-Max" |
| 18fb | chat (curadas) | Coroas e facetas | `coroas-anteriores-sobre-modelo` | Coroas anteriores sobre modelo de gesso | Só galeria |
| d8c0 | chat (curadas) | Metalocerâmica | `pontes-fixas` | Metalocerâmica | Galeria /trabalhos/ (metalocerâmica) |
| 369d | chat (curadas) | Metalocerâmica | `pontes-metaloceramicas` | Pontes metalocerâmicas | Figura de /servicos/metaloceramica/; capa do artigo "Metalocerâmica ou zircônia"; faixa |
| ee07 | chat (curadas) | Sobre implantes e barra clip | `estruturas-metalicas-sobre-modelos` | Barra de protocolo | Galeria /trabalhos/ (implantes); /servicos/protese-sobre-implante/; faixa da home. Obs.: não é metalocerâmica. |
| ed14 | chat (curadas) | PPR: Metal Roach e Dental D | `armacoes-metalicas-ppr` | Armações metálicas de PPR | Topo de /servicos/protese-parcial-removivel-ppr/ e cartão "PPR" |
| 694c | chat (curadas) | PPR: Metal Roach e Dental D | `enceramento-armacoes-ppr` | Enceramento das armações de PPR | Só galeria |
| d9f0 | chat (curadas) | PPR: Metal Roach e Dental D | `protese-parcial-sem-grampos-aparentes` | Prótese parcial sem grampos metálicos aparentes | Só galeria |
| 0541 | chat (curadas) | Placas, aparelhos e anti-ronco | `dispositivo-acrilico-conector-metalico` | Dispositivo em acrílico com conector metálico | Só galeria |
| 4316 | chat (curadas) | Placas, aparelhos e anti-ronco | `aparelhos-removiveis-sobre-modelos` | Aparelhos removíveis sobre modelos | Figura de /servicos/placas-de-bruxismo-e-ortodontia/ |
| 4ff7 | chat (curadas) | Bancada e impressão 3D | `modelo-com-coroas-nas-maos` | Conferência das coroas no modelo | Capa do artigo "Requisição para laboratório" |
| 0043 | chat (curadas) | Bancada e impressão 3D | `modelos-troquelizados-trabalhos-posteriores` | Trabalhos posteriores sobre modelos troquelizados | Figura da seção "O laboratório" na home |

**Faixa "Na bancada" da home** (manifesto publicado em `src/fotos_reais.json`): d282, d005,
d002, d123, d006, 0f03, d130, d085, 369d, d156, d166 e ee07.

**Imagens de compartilhamento (`assets/img/og/`, já exportadas):**
- `og-image.jpg`: padrão, com a foto d282;
- `og-trabalhos.jpg`: foto d005;
- `og-<serviço>.jpg`: para os 7 serviços que têm foto real;
- `og-<artigo>.jpg`: para os 5 artigos que têm foto real.

## Espaços que continuam com "Imagem ilustrativa" (Pexels)

| Espaço | Arquivo | Motivo |
|---|---|---|
| Topo de /servicos/resinas-e-provisorios/ e o cartão | `foto/escultura-resina` | Não há foto real de resina ou provisório com classificação certa |
| Figura de /servicos/resinas-e-provisorios/ | `foto/modelo-gesso-maos` | Mesmo motivo |
| Figura de /envio-para-todo-brasil/ | `foto/moldagem-alginato` | O acervo não tem foto de moldagem ou envio |
| Capa do artigo "Como enviar um caso" | `foto/moldeiras` | Mesmo motivo |

Fotos Pexels sob a [Licença Pexels](https://www.pexels.com/license/): escultura-resina 7788511,
modelo-gesso-maos 16309612, moldagem-alginato 7788356 e moldeiras 7788360. As outras fotos de
banco (e a antiga `aparelho-ortodontico`) saíram do site e foram removidas do repositório
(limpeza de 26/10/2026); ainda existem no histórico do Git se precisar recuperá-las.

## Dúvidas de classificação (a confirmar com o laboratório)

| Foto | Dúvida | O que o site diz hoje |
|---|---|---|
| 0043 | O material rosa é cera? | "Trabalhos posteriores sobre modelos troquelizados" |
| 0f03 | É overdenture ou protocolo? | "Prótese sobre implantes" |
| 445f | É protocolo? | "Prótese superior sobre implantes" |
| 18fb | Que tipo de pino ou núcleo aparece? | "Coroas anteriores sobre modelo de gesso" |
| 1ea3, 280c, 72c6, d8c0 | Qual é o material (zircônia, E-Max ou outro)? | Sem material na legenda |
| 369d, ee07 | Foram classificadas como metalocerâmica só pelo aspecto | "Pontes metalocerâmicas" / "Estruturas metálicas" |
| 694c | O modelo é refratário? | "Enceramento das armações de PPR" |
| d9f0 | É Flexite? | "Prótese parcial sem grampos metálicos aparentes" |
| 0541 | Provavelmente é anti-ronco (odontoapneia) | "Dispositivo em acrílico com conector metálico" |
| 4316 | Parece um aparelho tipo Hawley | "Aparelhos removíveis sobre modelos" |
| d270 | A base é transparente? | "Próteses totais em oclusão" |
| Drive DENTADURAS/`Protocolo 001.jpeg` | Tem fios parecidos com grampos e número de caso | **Não usada** |
| 0153 | Pode ser a mesma prótese das fotos 223/224 do Drive, em versão editada | Usada, já que as fotos não são idênticas |

## Duplicatas descartadas

- **Fotos do chat:** foram 10 pares; ficou a versão com marca d'água.

  | Ficou | Descartada |
  |---|---|
  | 0043 | d927 |
  | 0153 | a6af |
  | 0f03 | 9b0e |
  | 4316 | f726 |
  | d9f0 | ae30 |
  | 1ea3 | e2bf |
  | 694c | afc6 |
  | ee07 | d6ee |
  | 280c | 8f05 |
  | f686 | af5b |

- **Chat × Drive:** nenhuma foto idêntica. A menor distância de hash foi 39/128.
- **Drive:** sequências da mesma cena; ficou a melhor de cada uma.
  - BARRA CLIP 0, 1, 3 e 4: mesma barra da foto 2;
  - DENTADURAS 288/289 e 271;
  - séries 38/39, 47–49, 182–185 e 208/209;
  - outras sequências semelhantes.

## Fotos não usadas, com o motivo

- **Chat e153:** detalhe do mesmo caso da 1ea3.
- **Chat f686:** não dá para saber se é enceramento ou provisório.
- **Drive COROA - FACETAS - AFINS `IMG_20231006_174917/174928/175017/175025`:** nome de pessoa ("Pedro") no modelo.
- **Drive DENTAL D `02.9.jpg`:** escrita cursiva que pode ser um nome.
- **Drive DENTADURAS `Protocolo 001.jpeg`:** classificação incerta e número de caso.
- **Drive COROA `IMG_20240510_085416`, `IMG_20241031_170639200_HDR` e `170702735_HDR`:** pontes sobre suportes de impressão, talvez provisórias; assunto incerto.
- **Drive COROA `IMG-20240703-WA0094`:** foto em preto e branco.
- **Restante do acervo (cerca de 270 fotos):** quase duplicatas, foco ou luz piores, ou
  enquadramento com fundo poluído. O limite pedido era de cerca de 40 a 60 fotos no site.

## Como o site usa as fotos (técnico)

- Catálogo publicado: `src/fotos_reais.json`. Cada foto tem:
  - `id`, `src`, `pasta`, `cat` e `slug`;
  - `alt` e `cap`;
  - o recorte prévio `pre`, a região do trabalho `reg`, as variantes `var`, `fill` e `maxw`.
- As variantes já exportadas ficam em `src/assets/img/real/`:
  - `h`: 4:5, para o topo das páginas;
  - `w`: 3:2, para figuras e capas;
  - `g`: arquivo-fonte da galeria/faixa (proporção nativa); a grade exibe em 4:3 com cover.
  - Larguras de 480, 800 e 1200 px, em AVIF, WebP e JPEG.
- HTML: `<picture>` com AVIF e WebP, e `<img>` JPEG como fallback, com `srcset`/`sizes`,
  `width`/`height` (CLS 0), texto alternativo descritivo e `loading="lazy"`.
  - A exceção é a imagem LCP: ela usa `fetchpriority="high"` e tem preload AVIF.
  - Na home, o preload só vale para telas ≥ 1025 px, porque no celular a foto fica abaixo do texto.
  - Nas páginas internas, o topo usa 4:5 no desktop e 3:2 no celular, por *art direction*.
- JSON-LD: `ImageObject` (`creditText`, `creator` e `copyrightHolder` = o laboratório) em
  `primaryImageOfPage`, Service e Article. A galeria `/trabalhos/` tem `ImageGallery`. O
  `sitemap.xml` lista as fotos reais com `<image:image>`.
- Galeria `/trabalhos/`:
  - grade uniforme CSS Grid (3 colunas no desktop, 2 no mobile); cada card tem a mesma
    largura e a mesma altura de imagem (`aspect-ratio: 4/3` + `object-fit: cover`);
  - ponto focal por foto via classes `gal__a--fp-*` (`object-position`); o lightbox/`href`
    continua mostrando a foto completa sem crop;
  - legendas alinhadas na mesma linha de base; última fila incompleta fica à esquerda,
    com cards do mesmo tamanho;
  - cada miniatura é um link para o JPEG grande, então funciona sem JS;
  - com JS, a foto amplia num `<dialog>` com setas, ←/→, Esc, clique fora para fechar e foco
    devolvido (`main.js`, módulo 12).

### Trocar ou acrescentar uma foto real

```bash
# 1. prepare as variantes com Node + ImageMagick (o comando não altera o HTML)
npm run images:prepare -- caminho/foto.jpg nome-da-foto --kind=real --ratio=3/2 --focus=0.5,0.5
# 2. atualize os caminhos e metadados no head.html/main.html da rota
npm run build
npm run qa
```

O utilitário grava fotos reais em `src/assets/img/real/` nas larguras 480/800/1200, em AVIF, WebP
e JPEG. Para imagens ilustrativas, use `--kind=foto`; ele grava WebP em 640/1200. O ImageMagick
deve estar disponível no PATH. Para usar uma foto publicada, atualize os caminhos e metadados no
`head.html`/`main.html` da rota correspondente. Preserve `alt`, `width`, `height`, `srcset` e
`sizes`.

### Antes e depois

O componente existe, mas está desligado no HTML publicado. Ele só deve ser
ligado com pares reais do mesmo caso e com autorização.

## Fotos novas (outubro/2026) — chat do laboratório

Em 28–29/10/2026 o laboratório enviou 17 fotos originais (nomes oficiais do dono) para
complementar a galeria `/trabalhos/`. Ficaram só na galeria (sem trocar capas de serviço).
Total no site: **49** fotos reais.

Privacidade: em `encerramento-protese-total` o nome manuscrito **"Dr. Rafaela"** no gesso
(topo e base do modelo) foi desfocado antes da exportação. Nas demais 16 fotos o OCR não
encontrou nome de pessoa; a marca do cartão do laboratório em `porcelana-sobre-implante`
foi mantida.

| ID | Arquivo (`assets/img/real/`) | Categoria | Legenda | Motivo da categoria |
|---|---|---|---|---|
| n01 | `porcelana-sobre-implante` | Sobre implantes e barra clip | Porcelana sobre implante | Trabalho sobre implante |
| n02 | `escultura-em-cera` | Bancada e impressão 3D | Escultura em cera | Etapa de bancada (enceramento) |
| n03 | `placa-bruxismo-acrilico` | Placas, aparelhos e anti-ronco | Placa de bruxismo em acrílico | Placa |
| n04 | `placa-de-esportes` | Placas, aparelhos e anti-ronco | Placa de esportes | Protetor bucal |
| n05 | `coroa-metalo-plastica` | Coroas e facetas | Coroa metalo-plástica | Coroa (não é metalocerâmica) |
| n06 | `zirconia` | Coroas e facetas | Zircônia | Coroa/ponte em zircônia |
| n07 | `rmf` | Metalocerâmica | RMF | Núcleo metálico fundido (metal) |
| n08 | `rmf-vista-oclusal` | Metalocerâmica | RMF, vista oclusal | Mesmo RMF, outra vista |
| n09 | `encerramento-protese-total` | Prótese total | Encerramento de prótese total | Enceramento de PT |
| n10 | `ptr` | Prótese total | PTR | Prótese total removível |
| n11 | `dental-d` | PPR: Metal Roach e Dental D | Dental D | Grampo/estética Dental D |
| n12 | `flexite` | Prótese flexível (Flexite) | Flexite | Flexite |
| n13 | `escultura-ppt-roach-bilateral` | PPR: Metal Roach e Dental D | Escultura de PPT com estrutura metálica (Roach bilateral) | PPR / Roach |
| n14 | `roach-bilateral` | PPR: Metal Roach e Dental D | Roach bilateral | Armação Roach |
| n15 | `aparelho-de-contencao` | Placas, aparelhos e anti-ronco | Aparelho de contenção | Aparelho ortodôntico |
| n16 | `solidex-a` | Coroas e facetas | Solidex | Resina Solidex (sem categoria própria de resinas na galeria) |
| n17 | `solidex-b` | Coroas e facetas | Solidex | Segunda vista do Solidex |

Nenhuma categoria nova foi criada. Solidex e coroa metalo-plástica entraram em **Coroas e
facetas** por serem coroas/facetas em resina; RMF entrou em **Metalocerâmica** por ser
estrutura metálica fundida ligada a esse fluxo.
