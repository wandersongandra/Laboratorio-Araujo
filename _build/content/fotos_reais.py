"""Fotos REAIS do Laboratório Dental Araújo usadas no site (seleção de 26/10/2026).

Duas fontes, ambas do próprio LDA (originais FORA do site e do zip):
  - Google Drive do laboratório, baixado em /workspace/fotos-drive/ (fonte PRINCIPAL; a pasta do Drive
    é a classificação confiável: 'pasta' abaixo);
  - 30 fotos enviadas no chat, em /workspace/fotos-reais-originais/ (tratadas, fundo preto, com marca d'água),
    usadas como complemento; 'id' = 4 primeiros caracteres do arquivo.

Fonte única para tools/foto_real.py (gera AVIF/WebP/JPEG, SEM filtro de cor, sem EXIF/GPS) e para o
build.py (alt, legendas, faixa da home, galeria /trabalhos/, JSON-LD ImageObject, sitemap de imagens).

Campos:
  id    → chave curta ('dNNN' = foto do Drive; 4 caracteres = foto do chat)
  src   → (só Drive) caminho relativo a /workspace/fotos-drive/
  pasta → pasta do Drive (None = foto do chat, classificada pelo que se vê)
  cat   → categoria da galeria /trabalhos/ (ver CATS)
  slug  → nome público: assets/img/real/<slug>-<variante>-<largura>.<avif|webp|jpg>
  pre   → (opcional) recorte prévio da foto, ex.: para tirar a marca "Shot on …" do celular
  reg   → retângulo do trabalho (x0, y0, x1, y1, em fração da foto já girada pela orientação EXIF)
  var   → 'h' 4:5 (topo no desktop) · 'w' 3:2 (cartões, figuras, topo no celular) · 'g' livre
          (galeria e faixa). Valor = retângulo próprio ou None (usa reg).
  fill  → 'pad' (completa com o fundo escuro da borda) ou 'crop' (só recorta; padrão nas fotos do Drive)
  maxw  → largura máxima exportada (não amplia fotos pequenas)
Legendas e alt descrevem só o que se vê ou o que a pasta/nome do arquivo do laboratório afirma.
Material (zircônia × E-Max etc.) só é citado quando o próprio laboratório o nomeou.
"""

CATS = [('total', 'Prótese total'),
        ('implante', 'Sobre implantes e barra clip'),
        ('coroas', 'Coroas e facetas'),
        ('metalo', 'Metalocerâmica'),
        ('ppr', 'PPR: Metal Roach e Dental D'),
        ('flexite', 'Prótese flexível (Flexite)'),
        ('placas', 'Placas, aparelhos e anti-ronco'),
        ('lab', 'Bancada e impressão 3D')]

DRIVE = [
 dict(id='d282', cat='total', pasta='DENTADURAS', src='DENTADURAS/IMG_20250415_174014544_HDR.jpg',
      slug='proteses-totais-cartao-lda',
      alt='Par de próteses totais com gengiva caracterizada, ao lado do cartão do Laboratório Dental Araújo',
      cap='Próteses totais com gengiva caracterizada',
      reg=(0.1, 0.08, 0.9, 0.98), var={'h': None, 'w': (0.08, 0.1, 0.92, 0.66), 'g': None}),
 dict(id='d270', cat='total', pasta='DENTADURAS', src='DENTADURAS/IMG_20250414_163953707.jpg',
      slug='proteses-totais-em-oclusao',
      alt='Par de próteses totais em oclusão, fotografado de frente',
      cap='Próteses totais em oclusão',
      reg=(0.06, 0.18, 0.92, 0.82), var={'w': None, 'g': None}),
 dict(id='d002', cat='implante', pasta='BARRA CLIP', src='BARRA CLIP/IMG-20241205-WA0025.jpg',
      slug='barra-clip-sobre-modelo', pre=(0.0, 0.0, 1.0, 0.88),
      alt='Barra clip sobre o modelo de gesso, com a base rosa da prótese ao fundo',
      cap='Barra clip sobre o modelo',
      reg=(0.05, 0.06, 0.86, 1.0), var={'w': None, 'g': None}),
 dict(id='d005', cat='coroas', pasta='COROA - FACETAS - AFINS', src='COROA - FACETAS - AFINS/Coroa E-Max 001.jpeg',
      slug='coroas-e-max-modelo-caixa-lda',
      alt='Coroas posteriores em E-Max sobre o modelo de gesso, diante da caixa do Laboratório Dental Araújo',
      cap='Coroas posteriores em E-Max',
      reg=(0.2, 0.02, 0.73, 0.95), var={'h': None, 'w': (0.04, 0.0, 0.96, 0.95), 'g': (0.08, 0.0, 0.92, 0.95)}),
 dict(id='d006', cat='coroas', pasta='COROA - FACETAS - AFINS', src='COROA - FACETAS - AFINS/Facetas E-max 001.jpeg',
      slug='facetas-e-max-sobre-modelo',
      alt='Facetas em E-Max nos dentes anteriores, sobre o modelo de gesso',
      cap='Facetas em E-Max',
      reg=(0.27, 0.22, 0.81, 0.9), var={'h': None, 'w': None, 'g': None}),
 dict(id='d123', cat='ppr', pasta='METAL ROACH', src='METAL ROACH/IMG_20240412_173903.jpg',
      slug='armacoes-metal-roach-modelos',
      alt='Várias armações metálicas de PPR prontas, cada uma sobre o seu modelo de gesso',
      cap='Armações metálicas de PPR (Metal Roach)',
      reg=(0.0, 0.14, 1.0, 0.92), var={'w': (0.0, 0.16, 1.0, 0.72), 'g': None}),
 dict(id='d130', cat='ppr', pasta='METAL ROACH', src='METAL ROACH/IMG_20240611_181512825_HDR.jpg',
      slug='ppr-pronta-armacao-metalica',
      alt='Prótese parcial removível pronta, com armação metálica e dentes artificiais, sobre superfície espelhada',
      cap='PPR pronta, com armação metálica',
      reg=(0.06, 0.35, 0.94, 0.74), var={'w': None, 'g': None}),
 dict(id='d131', cat='ppr', pasta='METAL ROACH', src='METAL ROACH/IMG_20240611_181526175_HDR.jpg',
      slug='ppr-pronta-vista-de-cima',
      alt='Prótese parcial removível pronta com armação metálica, vista de cima sobre superfície espelhada',
      cap='PPR pronta, vista de cima',
      reg=(0.04, 0.36, 0.96, 0.7), var={'w': None, 'g': None}),
 dict(id='d143', cat='ppr', pasta='DENTAL D', src='DENTAL D/02.6.jpg',
      slug='grampo-estetico-dental-d',
      alt='Prótese parcial com grampo estético Dental D, na cor do dente, montada sobre os modelos',
      cap='Grampo estético Dental D',
      reg=(0.0, 0.22, 1.0, 0.86), var={'w': (0.0, 0.25, 1.0, 0.8), 'g': None}),
 dict(id='d156', cat='flexite', pasta='FLEXITE', src='FLEXITE/IMG-20230818-WA0029.jpg',
      slug='protese-flexivel-flexite',
      alt='Prótese parcial flexível (Flexite) com grampos em resina rosa, sobre superfície espelhada',
      cap='Prótese flexível (Flexite)',
      reg=(0.02, 0.18, 0.98, 0.86), var={'h': None, 'w': (0.02, 0.22, 0.98, 0.8), 'g': None}),
 dict(id='d157', cat='flexite', pasta='FLEXITE', src='FLEXITE/IMG-20230818-WA0030.jpg',
      slug='protese-flexivel-flexite-lateral',
      alt='Prótese parcial flexível (Flexite) vista de lado, com grampos da mesma resina',
      cap='Prótese flexível (Flexite), vista lateral',
      reg=(0.0, 0.28, 1.0, 0.86), var={'w': None, 'g': None}),
 dict(id='d085', cat='placas', pasta='ODONTOAPNEIA', src='ODONTOAPNEIA/IMG_20240305_120840.jpg',
      slug='aparelho-odontoapneia',
      alt='Aparelho anti-ronco (Odonto Apneia) em acrílico transparente, com as peças superior e inferior',
      cap='Aparelho anti-ronco (Odonto Apneia)',
      reg=(0.04, 0.22, 0.94, 0.86), var={'h': None, 'w': None, 'g': None}),
 dict(id='d166', cat='lab', pasta='3D', src='3D/IMG_20260709_113129892.jpg',
      slug='modelos-impressos-3d',
      alt='Modelos das arcadas impressos em 3D no laboratório',
      cap='Modelos impressos em 3D',
      reg=(0.0, 0.08, 1.0, 0.88), var={'w': (0.0, 0.16, 1.0, 0.86), 'g': None}),
 dict(id='d207', cat='lab', pasta='3D/Maquinário', src='3D/Maquinário/IMG_20260731_084514430_HDR.jpg',
      slug='impressoras-3d-laboratorio',
      alt='Impressoras 3D de resina na bancada do Laboratório Dental Araújo',
      cap='Impressoras 3D do laboratório',
      reg=(0.0, 0.07, 1.0, 0.66), var={'h': None, 'g': None}),
]

FOTOS = [
 dict(id='70c0', cat='total', slug='proteses-totais-gengiva-caracterizada', grupo='Prótese total',
      alt='Par de próteses totais com gengiva caracterizada, feitas no Laboratório Dental Araújo',
      cap='Próteses totais com gengiva caracterizada',
      reg=(0.12, 0.33, 0.87, 0.72), var={'h': None, 'w': None, 'g': None}),
 dict(id='0153', cat='total', slug='proteses-totais-sobre-modelos', grupo='Prótese total', fill='crop',
      alt='Próteses totais superior e inferior em oclusão, montadas sobre os modelos de gesso',
      cap='Próteses totais montadas sobre os modelos',
      reg=(0.0, 0.12, 1.0, 1.0), var={'h': (0.0, 0.2, 1.0, 0.9), 'w': (0.0, 0.33, 1.0, 0.77), 'g': None}),
 dict(id='0f03', cat='implante', slug='protese-sobre-implantes-e-modelo', grupo='Sobre implantes',
      alt='Prótese de arcada total sobre implantes ao lado do modelo com componentes metálicos',
      cap='Prótese sobre implantes e modelo com componentes',
      reg=(0.15, 0.2, 0.88, 0.93), var={'h': None, 'w': (0.15, 0.2, 0.88, 0.72), 'g': None}),
 dict(id='445f', cat='implante', slug='protese-superior-sobre-implantes', grupo='Sobre implantes', maxw=900,
      alt='Prótese superior sobre implantes com gengiva caracterizada, à frente do modelo com análogos',
      cap='Prótese superior sobre implantes e modelo com análogos',
      reg=(0.15, 0.05, 0.86, 0.84), var={'w': None, 'g': None}),
 dict(id='72c6', cat='coroas', slug='coroas-anteriores-modelos-articulados', grupo='Coroas e pontes', fill='crop',
      alt='Coroas anteriores superiores sobre modelos de gesso articulados',
      cap='Coroas anteriores sobre modelos articulados',
      reg=(0.0, 0.28, 1.0, 0.72), var={'h': None, 'w': (0.0, 0.31, 1.0, 0.68), 'g': (0.0, 0.27, 1.0, 0.73)}),
 dict(id='1ea3', cat='coroas', slug='coroas-anteriores-gengiva-artificial', grupo='Coroas e pontes',
      alt='Coroas anteriores superiores sobre modelo com gengiva artificial',
      cap='Coroas anteriores sobre modelo com gengiva artificial',
      reg=(0.0, 0.2, 1.0, 0.72), var={'w': (0.0, 0.38, 1.0, 0.63), 'g': None}),
 dict(id='280c', cat='coroas', slug='coroas-anteriores-superficie-espelhada', grupo='Coroas e pontes', maxw=1000,
      alt='Coroas anteriores prontas, fotografadas sobre superfície espelhada',
      cap='Coroas anteriores prontas',
      reg=(0.06, 0.0, 0.94, 1.0), var={'w': (0.05, 0.03, 0.95, 0.57), 'g': (0.05, 0.0, 0.95, 0.62)}),
 dict(id='18fb', cat='coroas', slug='coroas-anteriores-sobre-modelo', grupo='Coroas e pontes',
      alt='Coroas anteriores superiores sobre modelo de gesso',
      cap='Coroas anteriores sobre modelo de gesso',
      reg=(0.0, 0.13, 1.0, 0.74), var={'g': None}),
 dict(id='d8c0', cat='coroas', slug='pontes-fixas', grupo='Coroas e pontes',
      alt='Duas pontes fixas prontas sobre fundo escuro',
      cap='Pontes fixas',
      reg=(0.04, 0.33, 0.95, 0.79), var={'w': None, 'g': None}),
 dict(id='369d', cat='metalo', slug='pontes-metaloceramicas', grupo='Metalocerâmica',
      alt='Pontes metalocerâmicas com a estrutura metálica visível por dentro das coroas',
      cap='Pontes metalocerâmicas',
      reg=(0.0, 0.31, 0.98, 0.71), var={'w': None, 'g': None}),
 dict(id='ee07', cat='metalo', slug='estruturas-metalicas-sobre-modelos', grupo='Metalocerâmica',
      alt='Estruturas metálicas (casquetes) sobre modelos de gesso articulados',
      cap='Estruturas metálicas sobre modelos articulados',
      reg=(0.03, 0.03, 0.97, 0.81), var={'h': None, 'w': (0.0, 0.31, 1.0, 0.65), 'g': None}),
 dict(id='ed14', cat='ppr', slug='armacoes-metalicas-ppr', grupo='PPR',
      alt='Armações metálicas de prótese parcial removível com grampos, sobre modelos de gesso',
      cap='Armações metálicas de PPR',
      reg=(0.08, 0.2, 0.94, 0.85), var={'h': None, 'w': None, 'g': None}),
 dict(id='694c', cat='ppr', slug='enceramento-armacoes-ppr', grupo='PPR',
      alt='Padrões em cera das armações de PPR sobre modelos',
      cap='Enceramento das armações de PPR',
      reg=(0.02, 0.13, 0.98, 0.94), var={'w': (0.05, 0.13, 0.98, 0.565), 'g': None}),
 dict(id='d9f0', cat='ppr', slug='protese-parcial-sem-grampos-aparentes', grupo='Removíveis',
      alt='Prótese parcial inferior com base rosa translúcida, sem grampos metálicos aparentes, sobre o modelo',
      cap='Prótese parcial sem grampos metálicos aparentes',
      reg=(0.14, 0.45, 0.86, 0.89), var={'h': None, 'w': None, 'g': None}),
 dict(id='0541', cat='placas', slug='dispositivo-acrilico-conector-metalico', grupo='Placas e ortodontia',
      alt='Dispositivo intraoral em acrílico transparente e azul com conector metálico',
      cap='Dispositivo em acrílico com conector metálico',
      reg=(0.02, 0.33, 0.99, 0.82), var={'h': None, 'w': None, 'g': None}),
 dict(id='4316', cat='placas', slug='aparelhos-removiveis-sobre-modelos', grupo='Placas e ortodontia',
      alt='Aparelhos ortodônticos removíveis com arco vestibular sobre modelos de gesso',
      cap='Aparelhos removíveis sobre modelos',
      reg=(0.01, 0.34, 1.0, 0.88), var={'w': None, 'g': None}),
 dict(id='4ff7', cat='lab', slug='modelo-com-coroas-nas-maos', grupo='Bancada', fill='crop',
      alt='Técnico do laboratório segurando o modelo com coroas anteriores prontas',
      cap='Conferência das coroas no modelo',
      reg=(0.0, 0.18, 1.0, 0.85), var={'w': None, 'g': (0.0, 0.0, 1.0, 1.0)}),
 dict(id='0043', cat='lab', slug='modelos-troquelizados-trabalhos-posteriores', grupo='Bancada',
      alt='Modelos de gesso troquelizados com trabalhos posteriores em andamento',
      cap='Trabalhos posteriores sobre modelos troquelizados',
      reg=(0.0, 0.41, 1.0, 0.81), var={'w': None, 'g': None}),
]

for f in DRIVE: f.setdefault('fill', 'crop')
for f in FOTOS: f.setdefault('pasta', None)
FOTOS = DRIVE + FOTOS

# variantes realmente usadas no site (o resto não é exportado: dist mais leve)
USO = {'d282': 'hwg', 'd270': 'wg', 'd002': 'wg', 'd005': 'hwg', 'd006': 'wg', 'd123': 'g', 'd130': 'wg',
       'd131': 'wg', 'd143': 'g', 'd156': 'hwg', 'd157': 'wg', 'd085': 'wg', 'd166': 'g', 'd207': 'hg',
       '70c0': 'hwg', '0153': 'g', '0f03': 'hwg', '445f': 'wg', '72c6': 'g', '1ea3': 'g', '280c': 'wg',
       '18fb': 'g', 'd8c0': 'g', '369d': 'wg', 'ee07': 'hwg', 'ed14': 'hwg', '694c': 'g', 'd9f0': 'g',
       '0541': 'g', '4316': 'wg', '4ff7': 'wg', '0043': 'wg'}
for f in FOTOS:
    f['var'] = {k: v for k, v in f['var'].items() if k in USO[f['id']]}
    assert set(f['var']) == set(USO[f['id']]), f['id']
POR_ID = {f['id']: f for f in FOTOS}
POR_SLUG = {f['slug']: f for f in FOTOS}
assert len(POR_ID) == len(FOTOS) and len(POR_SLUG) == len(FOTOS)
assert all(f['cat'] in dict(CATS) for f in FOTOS)

# faixa "Na bancada" da home (variante 'g', ordem de exibição)
FAIXA_REAL = ['d282', 'd005', 'd002', 'd123', 'd006', '0f03', 'd130', 'd085', '369d', 'd156', 'd166', 'ee07']
