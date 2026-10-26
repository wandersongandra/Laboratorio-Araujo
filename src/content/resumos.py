"""
Textos curtos da versão "enxuta" do site (rodada de 26/10/2026).

- TAG: rótulo curto de cada serviço nos cartões da home (até ~5 palavras).
- RESUMO: 3–4 tópicos visíveis no topo de cada página de serviço. O texto completo continua
  no HTML (servicos.py → body), recolhido em acordeões <details>.
- RESUMO_SOBRE / RESUMO_ENVIO: o mesmo para /sobre/ e /envio-para-todo-brasil/.

Regra: só fatos que já estão no texto completo da página (nada novo aqui).
"""

TAG = {
    'protese-sobre-implante': 'Protocolo, barra clips, guia cirúrgico',
    'zirconia-e-max': 'Facetas, coroas e pontes prontas',
    'metaloceramica': 'Coroas, pontes, RMF e núcleos',
    'protese-parcial-removivel-ppr': 'Armação Roach, Wisil, Flexidy',
    'protese-total': 'PTR, Coloform, dupla prensagem, STG',
    'protese-flexivel-flexite': 'Sem grampo metálico aparente',
    'resinas-e-provisorios': 'Ceramage, fibra e provisórios',
    'placas-de-bruxismo-e-ortodontia': 'Bruxismo, anti-ronco, ortodontia',
}

RESUMO = {
    'protese-sobre-implante': [
        'Barra de protocolo em duas faixas: até 4 elementos e de 5 a 6 elementos.',
        'Também barra clips, guia cirúrgico e coroa sobre implante.',
        'Acompanhamos cada etapa clínica e devolvemos o trabalho pronto para a próxima consulta.',
        'Componentes protéticos e metais são orçados à parte.',
    ],
    'zirconia-e-max': [
        'Faceta, coroa e restaurado em E-Max ou zircônia; ponte fixa em zircônia.',
        'Entregues prontos: coping, aplicação de porcelana e glaze.',
        'A ponte em zircônia é orçada por elemento.',
        'Envie cor, fotos com a escala e registro de mordida.',
    ],
    'metaloceramica': [
        'Coroa e ponte metalocerâmica entregues prontas: coping, porcelana e glaze.',
        'Restaurados metálicos, coroa total metálica, veneer e núcleo.',
        'Ponte orçada por elemento; o metal é orçado à parte, conforme a liga.',
    ],
    'protese-parcial-removivel-ppr': [
        'Armação Roach nacional, tipo Wisil, em Dental D ou em Flexidy.',
        'Roach nacional e tipo Wisil incluem metal, plano, montagem e prensagem.',
        'A peça é entregue pronta; os dentes são orçados à parte.',
    ],
    'protese-total': [
        'PTR simples, palato incolor, Coloform especial, dupla prensagem ou Sistema Tomas Gomes.',
        'Todas as opções incluem chapa, montagem e prensagem.',
        'Entregue pronta, com acabamento e polimento; dentes orçados à parte.',
    ],
    'protese-flexivel-flexite': [
        'Parcial Flexite unilateral ou bilateral, sem grampo metálico aparente.',
        'Os grampos são do próprio material, na cor da gengiva.',
        'Parciais em acrílico: simples, palato incolor, Coloform especial e dupla prensagem.',
        'Entregues prontas; os dentes são orçados à parte.',
    ],
    'resinas-e-provisorios': [
        'Coroas, pontes com fibra e restaurados em Ceramage, resina popular ou acrílico.',
        'Provisórios de longa duração e soluções de transição.',
        'Alternativa estética de custo menor que a cerâmica.',
    ],
    'placas-de-bruxismo-e-ortodontia': [
        'Placa de bruxismo cristal, emborrachada ou acrílica prensada.',
        'Placas de clareamento, protetores para esporte e aparelho anti-ronco.',
        'Aparelhos ortodônticos móveis, contenções e todos os tipos de ortodontia e ortopedia.',
        'Feitas sobre o modelo, a partir da moldagem enviada pelo consultório.',
    ],
}

RESUMO_SOBRE = [
    'Fundado em 1976 no Centro de Belo Horizonte: 50 anos em 2026.',
    'Mais de 35 técnicos em cerca de 400 m² no Edifício Mesbla.',
    'Atende cirurgiões-dentistas e clínicas, em todas as áreas da prótese.',
    'Coleta e entrega em Minas Gerais; casos recebidos de todo o Brasil.',
]

RESUMO_ENVIO = [
    'Em Minas Gerais, o laboratório faz coleta e entrega.',
    'De outros estados, o caso chega pelos Correios ou por transportadora.',
    'Prazo médio de 7 dias úteis por etapa, mais o tempo de transporte.',
    'Antes de enviar, combine pelo WhatsApp a forma de retorno e o frete.',
]
