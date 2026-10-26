# -*- coding: utf-8 -*-
"""Conteúdo das páginas de serviço. Fatos do laboratório: Tabela 2026 oficial (arquivada em private/arquivo/, não publicada).
O site não mostra valores: tudo é sob orçamento.
Texto clínico em linguagem geral, voltado ao cirurgião-dentista (B2B)."""

PRAZO = 'O prazo médio é de 7 dias úteis por etapa, podendo variar conforme a demanda do laboratório. Trabalhos com urgência têm acréscimo de 30% em cada etapa.'
GARANTIA = 'Garantia de até 6 meses para defeito comprovado na confecção, válida para serviços 100% realizados no laboratório.'

SERVICOS = [
# ------------------------------------------------------------------ 1
dict(
 slug='protese-sobre-implante', nav='Prótese sobre implante e protocolo',
 title='Prótese Protocolo e sobre Implante em BH | LDA',
 desc='Laboratório em BH de prótese protocolo sobre implante: barra de protocolo, overdenture com barra clips, guia cirúrgico e coroa sobre implante. Envio ao Brasil.',
 kicker='Implantes e protocolo', h1='Prótese protocolo e sobre implante <span class="hl">em BH</span>',
 lead='Barra de protocolo, barra clips, guia cirúrgico e coroa metalocerâmica sobre implante, confeccionados no Centro de Belo Horizonte para dentistas de BH, de Minas Gerais e de todo o Brasil.',
 img='real/protese-sobre-implantes-e-modelo', img_alt='Prótese de arcada total sobre implantes ao lado do modelo com componentes metálicos',
 fig='real/barra-clip-sobre-modelo', fig_alt='Barra clip sobre o modelo de gesso, com a base rosa da prótese ao fundo',
 fig_cap='Barra clip sobre o modelo',
 primary='prótese protocolo sobre implante', secondary=['barra de protocolo', 'overdenture com barra clip', 'guia cirúrgico para implante', 'coroa sobre implante', 'laboratório de prótese sobre implante BH'],
 cats=['implantes'], service_type='Prótese sobre implante: protocolo, overdenture com barra clips e guia cirúrgico',
 blurb='Barra de protocolo até 6 elementos, barra clips, guia cirúrgico e coroa sobre implante.',
 body='''
<h2>Laboratório de prótese protocolo em BH</h2>
<p>O <strong>Laboratório Dental Araújo</strong> faz barras de protocolo para dentistas e clínicas desde que a reabilitação sobre implantes se popularizou no Brasil. Atuamos no Centro de Belo Horizonte desde 1975 e trabalhamos com uma equipe de mais de 40 profissionais. A <strong>prótese protocolo</strong> é uma das áreas que mais cresceram no laboratório. Recebemos o caso do consultório, acompanhamos cada etapa clínica e devolvemos o trabalho pronto para a próxima consulta, com coleta e entrega em Minas Gerais e envio para outros estados.</p>
<p>A barra de protocolo é feita em duas faixas: <strong>até 4 elementos</strong> e <strong>de 5 a 6 elementos</strong>. O valor de cada caso é informado sob orçamento. Componentes protéticos e metais são orçados à parte, porque variam de acordo com o sistema de implante e a liga escolhida pelo profissional.</p>

<h2>O que é a prótese protocolo e quando ela é indicada</h2>
<p>A prótese tipo protocolo é uma prótese total fixa, parafusada sobre implantes, normalmente formada por uma infraestrutura (a barra) e por dentes e gengiva artificiais. É uma solução clássica para pacientes edêntulos totais que desejam sair da dentadura convencional e ter uma prótese fixa, sem a necessidade de remoção diária pelo paciente. O número de implantes, a distribuição no arco e o tipo de componente são decisões do cirurgião-dentista. O laboratório executa o planejamento protético a partir das moldagens, dos registros e das informações enviadas na requisição.</p>
<h2>Protocolo ou overdenture com barra clips?</h2>
<p>No protocolo, a prótese é fixa e parafusada: o paciente não a remove. Na <strong>overdenture com barra clips</strong>, a barra une os implantes e a prótese total, removível, se encaixa por clipes de retenção, o que melhora a estabilidade, principalmente na mandíbula. A escolha entre uma e outra depende do número de implantes, do espaço protético, do suporte labial e da higiene do paciente, e é sempre do cirurgião-dentista. O laboratório faz barra clips de até 3 elementos.</p>

<h2>Serviços sobre implante disponíveis</h2>
<ul>
<li><strong>Barra de protocolo</strong> para até 4 elementos ou de 5 a 6 elementos.</li>
<li><strong>Barra clips</strong> para overdentures, até 3 elementos.</li>
<li><strong>Guia cirúrgico</strong> para orientar o posicionamento dos implantes.</li>
<li><strong>Coroa metalocerâmica sobre implante</strong> (componentes e metal orçados à parte).</li>
<li>Coroas unitárias e pontes em <a href="/servicos/zirconia-e-max/">zircônia e E-Max</a>, quando indicadas pelo dentista.</li>
</ul>

<h2>Como funciona o fluxo de um protocolo com o laboratório</h2>
<p>Cada caso tem suas particularidades, mas o fluxo mais comum envolve as etapas abaixo. Cada etapa de laboratório tem prazo médio de 7 dias úteis.</p>
<ol class="steps">
<li><strong>Transferência e modelo de trabalho:</strong> o dentista envia a moldagem de transferência (moldeira aberta ou fechada) com os análogos ou componentes, o registro e a requisição preenchida.</li>
<li><strong>Base de prova e montagem dos dentes:</strong> o laboratório monta os dentes em cera para prova estética, fonética e de dimensão vertical no paciente.</li>
<li><strong>Infraestrutura (barra):</strong> após a aprovação da montagem, a barra é confeccionada e enviada para prova de assentamento passivo, quando o protocolo clínico prevê essa etapa.</li>
<li><strong>Acrilização e acabamento:</strong> com tudo aprovado, a prótese é finalizada, polida e conferida antes de voltar ao consultório.</li>
</ol>
<p>Explicamos as etapas em detalhe no artigo <a href="/blog/barra-de-protocolo-etapas-e-prazos/">etapas e prazos da barra de protocolo</a>.</p>

<h2>Prazos, urgência e garantia</h2>
<p>{PRAZO} {GARANTIA} Recados e informações extras devem ser enviados por escrito junto com a requisição, o que reduz o risco de retrabalho e garante que a equipe siga exatamente o que foi planejado.</p>

<h2>Atendimento para dentistas de BH, Minas Gerais e todo o Brasil</h2>
<p>Fazemos a coleta e a entrega em Minas Gerais e recebemos casos de outros estados. Veja como embalar e enviar seu trabalho na página <a href="/envio-para-todo-brasil/">Envio para todo o Brasil</a>. Para tirar dúvidas sobre componentes, ligas ou prazos de um caso específico, fale com o atendimento pelo WhatsApp (31) 98652-1387.</p>
''',
 faq=[
  ('Quanto custa uma barra de protocolo no Laboratório Dental Araújo?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. A barra é feita para até 4 elementos ou de 5 a 6 elementos, e componentes e metais são orçados à parte.'),
  ('O laboratório faz guia cirúrgico para implantes?', 'Sim. O laboratório faz guia cirúrgico para orientar o posicionamento dos implantes. Peça um orçamento pelo WhatsApp (31) 98652-1387.'),
  ('Qual a diferença entre protocolo e overdenture com barra clip?', 'A barra de protocolo sustenta uma prótese total fixa, parafusada sobre os implantes. Na overdenture, a barra clips une os implantes e retém, por meio de clipes, uma prótese total que o paciente remove para higienizar.'),
  ('Quais são as etapas da prótese protocolo no laboratório?', 'O fluxo mais comum tem modelo de trabalho e base de prova, montagem dos dentes, confecção e prova da barra e, por fim, acrilização e acabamento. Cada etapa de laboratório leva em média 7 dias úteis; o total depende de quantas provas clínicas o caso exige.'),
  ('O que enviar para o laboratório fazer um protocolo?', 'A moldagem de transferência com os transferentes, os análogos compatíveis, a indicação do sistema, da plataforma e dos componentes, o registro de mordida, a cor dos dentes e a requisição preenchida.'),
 ],
 related=['zirconia-e-max', 'metaloceramica', 'protese-total'],
),
# ------------------------------------------------------------------ 2
dict(
 slug='zirconia-e-max', nav='Zircônia e E-Max',
 title='Coroa de Zircônia e E-Max em BH | Lab. Dental Araújo',
 desc='Coroa de zircônia, ponte fixa de zircônia e faceta ou coroa em E-Max (dissilicato de lítio), entregues prontas por laboratório em BH. Envio ao Brasil.',
 kicker='Porcelana pura', h1='Coroa de zircônia e E-Max <span class="hl">em Belo Horizonte</span>',
 lead='Facetas, coroas, restaurados e pontes fixas em porcelana pura, entregues prontos (coping, aplicação de porcelana e glaze) para consultórios de BH e de todo o Brasil.',
 img='real/coroas-e-max-modelo-caixa-lda', img_alt='Coroas posteriores em E-Max sobre o modelo de gesso, diante da caixa do Laboratório Dental Araújo',
 fig='real/facetas-e-max-sobre-modelo', fig_alt='Facetas em E-Max nos dentes anteriores, sobre o modelo de gesso', fig_cap='Facetas em E-Max',
 primary='coroa de zircônia', secondary=['coroa e faceta em E-Max', 'ponte fixa de zircônia', 'dissilicato de lítio', 'prótese metal free', 'laboratório de zircônia BH'],
 cats=['porcelana'], service_type='Prótese fixa em cerâmica pura (zircônia e dissilicato de lítio)',
 blurb='Facetas, coroas, restaurados e pontes em zircônia e E-Max, prontos com glaze.',
 body='''
<h2>Coroa de zircônia e E-Max feitas em BH</h2>
<p>O <strong>Laboratório Dental Araújo</strong>, no Centro de Belo Horizonte, faz <strong>coroas de zircônia</strong>, pontes de zircônia e peças em <strong>E-Max</strong> para cirurgiões-dentistas. Atuamos desde 1975, temos mais de 40 profissionais e todos os trabalhos de porcelana pura são entregues prontos: coping, aplicação de porcelana e glaze.</p>
<p>Fazemos faceta ou coroa em E-Max, restaurado em E-Max, faceta ou coroa em zircônia, restaurado em zircônia e ponte fixa em zircônia. O valor é informado sob orçamento, de acordo com o material e o número de elementos.</p>

<h2>Zircônia ou E-Max: como escolher o material</h2>
<p>As duas cerâmicas são livres de metal (metal free) e têm ótimo resultado estético, mas o comportamento clínico é diferente. A escolha é sempre do dentista, que avalia o caso. Em geral:</p>
<div class="table-wrap"><table>
<thead><tr><th>Critério</th><th>E-Max (dissilicato de lítio)</th><th>Zircônia</th></tr></thead>
<tbody>
<tr><td>Ponto forte</td><td>Translucidez e naturalidade</td><td>Resistência mecânica</td></tr>
<tr><td>Indicações comuns</td><td>Facetas, coroas anteriores, restaurados</td><td>Coroas posteriores, pontes, pacientes com bruxismo</td></tr>
<tr><td>Substrato escurecido</td><td>Pode exigir cuidado na seleção da pastilha</td><td>Maior capacidade de mascarar</td></tr>
<tr><td>Cimentação</td><td>Costuma ser adesiva</td><td>Aceita protocolos adesivos ou convencionais, conforme o caso</td></tr>
</tbody></table></div>
<p>Fizemos um guia completo sobre o tema no blog: <a href="/blog/zirconia-ou-e-max-qual-indicar/">zircônia ou E-Max, qual indicar</a>. Se a dúvida é entre cerâmica pura e infraestrutura metálica, veja <a href="/blog/metaloceramica-ou-zirconia/">metalocerâmica ou zircônia</a>.</p>

<h2>Facetas e coroas em E-Max</h2>
<p>O E-Max é muito usado em <strong>facetas</strong> e coroas da região anterior, onde a translucidez faz diferença no sorriso. Também atende bem restaurados (inlays, onlays e overlays) quando o dentista quer preservar estrutura dental. Para um bom resultado, envie a cor do remanescente, a cor desejada e fotos com escala de cor sempre que possível.</p>

<h2>Coroas e pontes de zircônia</h2>
<p>A zircônia é a escolha frequente para coroas posteriores e <strong>pontes fixas</strong>, pela alta resistência à fratura. Também é usada sobre dentes escurecidos ou núcleos metálicos, por mascarar melhor o fundo. A ponte em zircônia é orçada por elemento.</p>

<h2>O que enviar para um trabalho de porcelana pura</h2>
<ul>
<li>Moldagem ou modelo com o preparo bem definido e o antagonista.</li>
<li>Registro de mordida.</li>
<li>Cor (escala utilizada) e, se possível, fotos com a escala posicionada ao lado do dente.</li>
<li>Requisição com o material escolhido, os elementos e qualquer observação por escrito.</li>
</ul>
<p>Veja o passo a passo completo em <a href="/blog/como-enviar-um-caso-para-o-laboratorio-de-protese/">como enviar um caso para o laboratório de prótese</a>.</p>

<h2>Prazos e garantia</h2>
<p>{PRAZO} {GARANTIA}</p>

<h2>Outras opções de coroa</h2>
<p>Quando o caso pede uma solução com infraestrutura metálica, veja a <a href="/servicos/metaloceramica/">coroa metalocerâmica</a>. Para soluções provisórias ou de menor custo, consulte <a href="/servicos/resinas-e-provisorios/">resinas e provisórios</a>. Sobre implantes, a coroa também pode ser feita em zircônia ou metalocerâmica (veja <a href="/servicos/protese-sobre-implante/">prótese sobre implante</a>).</p>
''',
 faq=[
  ('Quanto custa uma coroa de zircônia no laboratório?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. A coroa de zircônia é entregue pronta, com coping, aplicação de porcelana e glaze.'),
  ('Zircônia ou E-Max: qual é melhor?', 'Depende do caso. O E-Max (dissilicato de lítio) se destaca pela translucidez e costuma ser indicado em facetas, coroas anteriores e restaurados; a zircônia se destaca pela resistência e é frequente em coroas posteriores e pontes. A escolha é do cirurgião-dentista.'),
  ('O laboratório faz ponte fixa de zircônia?', 'Sim. A ponte fixa em zircônia é entregue pronta e orçada por elemento.'),
  ('Vocês fazem faceta em E-Max e em zircônia?', 'Sim. Fazemos faceta ou coroa em E-Max e faceta ou coroa em zircônia, além de restaurados nos dois materiais, todos entregues prontos.'),
  ('Vocês recebem casos de zircônia de outros estados?', 'Sim. Atendemos dentistas de todo o Brasil. Combine o envio pelo WhatsApp (31) 98652-1387.'),
 ],
 related=['metaloceramica', 'protese-sobre-implante', 'resinas-e-provisorios'],
),
# ------------------------------------------------------------------ 3
dict(
 slug='metaloceramica', nav='Metalocerâmica e RMF',
 title='Coroa Metalocerâmica e RMF em BH | Lab. Dental Araújo',
 desc='Coroa e ponte metalocerâmica, núcleo metálico fundido, restaurado metálico e coroa veneer feitos em BH pelo Laboratório Dental Araújo. Envio ao Brasil.',
 kicker='Metalocerâmica', h1='Coroa metalocerâmica e RMF: <span class="hl">laboratório em BH</span>',
 lead='Coroas e pontes metalocerâmicas prontas, restaurados metálicos, coroas totais metálicas, veneer e núcleos, com a experiência de quem faz prótese em Belo Horizonte desde 1975.',
 img='real/estruturas-metalicas-sobre-modelos', img_alt='Estruturas metálicas (casquetes) sobre modelos de gesso articulados',
 fig='real/pontes-metaloceramicas', fig_alt='Pontes metalocerâmicas com a estrutura metálica visível por dentro das coroas', fig_cap='Pontes metalocerâmicas',
 primary='coroa metalocerâmica', secondary=['ponte metalocerâmica', 'núcleo metálico fundido', 'metalocerâmica sobre implante', 'restaurado metálico', 'coroa veneer'],
 cats=['metaloceramica', 'rmf'], service_type='Prótese fixa metalocerâmica e restaurações metálicas fundidas (RMF)',
 blurb='Coroa e ponte metalocerâmica, restaurado e coroa metálica, veneer e núcleo.',
 body='''
<h2>Metalocerâmica ainda é uma boa indicação?</h2>
<p>Sim. A <strong>coroa metalocerâmica</strong> tem décadas de acompanhamento clínico e continua sendo uma solução previsível, principalmente em pontes posteriores, em casos com espaço protético reduzido para cerâmica pura ou quando o dentista prefere uma infraestrutura metálica. O <strong>Laboratório Dental Araújo</strong> faz metalocerâmica desde os primeiros anos de atuação em Belo Horizonte, e esse know-how se reflete no ajuste e na estética das peças.</p>
<p>A <strong>coroa metalocerâmica unitária</strong> e a <strong>ponte metalocerâmica</strong> (orçada por elemento) são entregues prontas: coping, aplicação de porcelana e glaze. O <strong>metal é orçado à parte</strong>, de acordo com a liga escolhida.</p>

<h2>Restaurações metálicas fundidas (RMF) e similares</h2>
<p>Além da metalocerâmica, o laboratório confecciona trabalhos metálicos e híbridos:</p>
<ul>
<li><strong>Restaurado metálico</strong>, pronto.</li>
<li><strong>Coroa total metálica</strong>, pronta.</li>
<li><strong>Coroa veneer</strong> com face em acrílico.</li>
<li><strong>Núcleo metálico</strong>, pronto.</li>
</ul>
<p>Em todos esses itens, o metal é orçado à parte.</p>

<h2>Quando escolher metalocerâmica, zircônia ou E-Max</h2>
<p>A decisão é clínica e cabe ao cirurgião-dentista. De forma geral, a metalocerâmica é considerada quando:</p>
<ul>
<li>o caso exige pontes extensas na região posterior;</li>
<li>a altura ou o espaço interoclusal limitam a espessura da cerâmica pura;</li>
<li>o dentista prefere uma infraestrutura metálica por histórico clínico ou custo.</li>
</ul>
<p>Comparamos os dois materiais, com base em revisões sistemáticas, no artigo <a href="/blog/metaloceramica-ou-zirconia/">metalocerâmica ou zircônia</a>. Quando a prioridade é estética livre de metal, veja <a href="/servicos/zirconia-e-max/">coroa de zircônia e E-Max</a>. Para coroas parafusadas ou cimentadas sobre implantes, a <strong>coroa metalocerâmica sobre implante</strong> (componentes e metais orçados à parte) está detalhada em <a href="/servicos/protese-sobre-implante/">prótese sobre implante</a>.</p>

<h2>Núcleo metálico fundido: o que enviar</h2>
<p>Para o núcleo, envie a moldagem do conduto bem copiada (ou o padrão em resina, se for o seu protocolo), o modelo do arco, o antagonista e a indicação do elemento. Se o núcleo e a coroa forem feitos em sequência, descreva o plano na requisição para que a equipe já considere o espaço da coroa.</p>

<h2>Como garantimos o ajuste</h2>
<p>A equipe confere a adaptação marginal no troquel, os contatos proximais e a oclusão no articulador antes de liberar cada peça. Por isso, modelos bem vazados, registro de mordida estável e antagonista completo fazem diferença no resultado. Troquéis e vazamentos, quando feitos pelo laboratório, são orçados à parte.</p>

<h2>Prazos, garantia e pagamento</h2>
<p>{PRAZO} {GARANTIA} O pagamento é feito até o dia 10 de cada mês.</p>
''',
 faq=[
  ('Quanto custa uma coroa metalocerâmica?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. A coroa é entregue pronta, e o metal é orçado à parte.'),
  ('Metalocerâmica ou zircônia: qual escolher?', 'As duas têm boa sobrevida em coroas unitárias. A metalocerâmica segue como referência em pontes posteriores e em espaço protético reduzido; a zircônia evita a cinta metálica e tende a ter menos complicações estéticas. A escolha é do cirurgião-dentista.'),
  ('O laboratório faz núcleo metálico fundido?', 'Sim. O núcleo metálico é entregue pronto, com o metal orçado à parte.'),
  ('Vocês fazem coroa metalocerâmica sobre implante?', 'Sim. Componentes protéticos e metais são orçados à parte, conforme o sistema de implante e a liga escolhida.'),
  ('A ponte metalocerâmica é orçada por elemento?', 'Sim. A ponte metalocerâmica é orçada por elemento, com o metal à parte.'),
 ],
 related=['zirconia-e-max', 'protese-sobre-implante', 'resinas-e-provisorios'],
),
# ------------------------------------------------------------------ 4
dict(
 slug='protese-parcial-removivel-ppr', nav='PPR (Roach)',
 title='PPR – Prótese Parcial Removível em BH | Lab. Araújo',
 desc='PPR (prótese parcial removível) com armação metálica Roach nacional ou tipo Wisil, Dental D e Flexidy, feita em BH pelo Lab. Dental Araújo. Envio ao Brasil.',
 kicker='Prótese parcial removível', h1='PPR: prótese parcial removível <span class="hl">em BH</span>',
 lead='Prótese parcial removível com armação metálica Roach (nacional ou tipo Wisil) ou em Dental D e Flexidy, entregue pronta para dentistas de Belo Horizonte, de Minas Gerais e de todo o Brasil.',
 img='real/armacoes-metalicas-ppr', img_alt='Armações metálicas de prótese parcial removível com grampos, sobre modelos de gesso',
 fig='real/ppr-pronta-armacao-metalica', fig_alt='Prótese parcial removível pronta, com armação metálica e dentes artificiais, sobre superfície espelhada', fig_cap='PPR pronta, com armação metálica',
 primary='PPR prótese parcial removível', secondary=['armação metálica de PPR', 'PPR Roach', 'grampo Roach', 'PPR Wisil', 'laboratório de PPR BH'],
 cats=['ppr-roach'], service_type='Prótese parcial removível (PPR) com armação metálica',
 blurb='PPR com armação Roach nacional, tipo Wisil, Dental D ou Flexidy.',
 body='''
<h2>Laboratório de PPR em Belo Horizonte</h2>
<p>O <strong>Laboratório Dental Araújo</strong> faz <strong>prótese parcial removível (PPR)</strong> para cirurgiões-dentistas desde 1975. A PPR continua sendo uma das reabilitações mais solicitadas: tem custo acessível, é reversível e devolve função e estética a pacientes parcialmente desdentados. Nossa equipe faz a armação, o plano de cera, a montagem dos dentes e a prensagem, e entrega a peça pronta.</p>

<h2>Tipos de PPR Roach</h2>
<ul>
<li><strong>Roach bilateral nacional</strong> com prensagem simples, pronta.</li>
<li><strong>Roach bilateral tipo Wisil</strong> com prensagem simples, pronta.</li>
<li><strong>Roach bilateral em Dental D</strong>, pronta.</li>
<li><strong>Roach bilateral em Flexidy</strong>, pronta.</li>
</ul>
<p>A Roach nacional e a tipo Wisil incluem metal, plano, montagem e prensagem. A Roach em Dental D e em Flexidy inclui metal, montagem e prensagem/aplicação. <strong>Em todos os casos, os dentes são orçados à parte.</strong> O valor de cada PPR é informado sob orçamento.</p>

<h2>Armação metálica Roach: o que é</h2>
<p>A armação Roach é a estrutura metálica fundida da PPR, com grampos de retenção do tipo barra (grampos Roach), apoios e conectores. O desenho, com a escolha dos dentes pilares, dos apoios, dos retentores e do conector maior, deve ser definido pelo dentista após o planejamento no delineador. O laboratório pode sugerir ajustes técnicos, mas segue sempre o que está escrito na requisição.</p>
<h3>Nacional, tipo Wisil, Dental D ou Flexidy?</h3>
<p>As opções se diferenciam pela liga ou pelo material de base e pelo acabamento. A versão nacional atende bem a maioria dos casos com ótimo custo-benefício. A tipo Wisil usa uma liga de referência no mercado, e as opções em Dental D e Flexidy são indicadas quando o dentista prefere esses materiais pela estética ou pelo conforto da base. Em caso de dúvida, fale com o atendimento antes de enviar o caso.</p>

<h2>Etapas de laboratório de uma PPR</h2>
<ol class="steps">
<li><strong>Modelo de trabalho e planejamento:</strong> o dentista envia a moldagem funcional e o desenho da armação, ou solicita que o laboratório faça o delineamento para aprovação.</li>
<li><strong>Armação metálica:</strong> a estrutura é fundida, ajustada e enviada para prova no paciente.</li>
<li><strong>Plano de cera e montagem dos dentes:</strong> após o registro intermaxilar, os dentes são montados para prova.</li>
<li><strong>Prensagem e acabamento:</strong> com a montagem aprovada, a PPR é prensada, polida e devolvida pronta.</li>
</ol>
<p>Cada etapa tem prazo médio de 7 dias úteis. Trabalhos com urgência têm acréscimo de 30% por etapa.</p>

<h2>PPR sem grampo metálico aparente</h2>
<p>Se o paciente tem restrição estética ao grampo metálico, a prótese parcial em resina flexível pode ser uma alternativa. Veja <a href="/servicos/protese-flexivel-flexite/">prótese flexível Flexite e parciais em acrílico</a> e o comparativo <a href="/blog/ppr-ou-protese-flexivel/">PPR ou prótese flexível</a>. Para pacientes totalmente desdentados, consulte <a href="/servicos/protese-total/">prótese total</a>.</p>

<h2>Garantia e informações importantes</h2>
<p>{GARANTIA} Recados e informações extras devem ser enviados por escrito junto com a requisição. Dentes, soldas, componentes e ligas especiais são orçados à parte.</p>
''',
 faq=[
  ('Quanto custa uma PPR Roach no laboratório?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766, e varia conforme o tipo: nacional, tipo Wisil, Dental D ou Flexidy. Os dentes são orçados à parte.'),
  ('Os dentes estão incluídos na PPR?', 'Não. Em todas as PPR Roach os dentes são orçados à parte.'),
  ('PPR ou prótese flexível: qual indicar?', 'A PPR com armação metálica tem apoios oclusais e conector rígido, o que favorece a estabilidade, principalmente em extremidade livre. A flexível não tem grampo metálico aparente e costuma ser considerada em casos estéticos, de transição ou de alergia ao metal. A indicação é do cirurgião-dentista.'),
  ('Quantas etapas tem uma PPR?', 'Normalmente prova da armação, prova da montagem dos dentes e entrega final, com média de 7 dias úteis por etapa.'),
 ],
 related=['protese-flexivel-flexite', 'protese-total', 'placas-de-bruxismo-e-ortodontia'],
),
# ------------------------------------------------------------------ 5
dict(
 slug='protese-total', nav='Prótese total (PTR)',
 title='Prótese Total Removível (PTR) em BH | Lab. Dental Araújo',
 desc='Prótese total removível simples, palato incolor, caracterizada (Coloform especial), dupla prensagem e STG, feita em BH pelo Lab. Dental Araújo.',
 kicker='Prótese total removível', h1='Prótese total: <span class="hl">laboratório em BH</span>',
 lead='Prótese total removível (PTR) simples, com palato incolor, Coloform especial, dupla prensagem ou pelo Sistema Tomas Gomes (STG), feita no Centro de Belo Horizonte desde 1975.',
 img='real/proteses-totais-cartao-lda', img_alt='Par de próteses totais com gengiva caracterizada, ao lado do cartão do Laboratório Dental Araújo',
 fig='real/proteses-totais-em-oclusao', fig_alt='Par de próteses totais em oclusão, fotografado de frente', fig_cap='Próteses totais em oclusão',
 primary='prótese total removível', secondary=['PTR', 'prótese total caracterizada', 'prótese total palato incolor', 'prótese total STG', 'laboratório de prótese total BH'],
 cats=['ptr'], service_type='Prótese total removível',
 blurb='PTR simples, palato incolor, Coloform, dupla prensagem e Sistema Tomas Gomes.',
 body='''
<h2>Laboratório de prótese total em BH</h2>
<p>A <strong>prótese total</strong> foi um dos primeiros trabalhos do <strong>Laboratório Dental Araújo</strong>, fundado em 1975 no Centro de Belo Horizonte, e segue entre os mais pedidos pelos dentistas parceiros. Com mais de 40 profissionais, cuidamos da chapa, da montagem dos dentes e da prensagem, e entregamos a prótese pronta, com acabamento e polimento.</p>

<h2>Opções de PTR</h2>
<ul>
<li><strong>PTR simples</strong>, pronta.</li>
<li><strong>PTR palato incolor</strong>, pronta.</li>
<li><strong>PTR Coloform especial</strong>, pronta.</li>
<li><strong>PTR dupla prensagem</strong>, pronta.</li>
<li><strong>PTR STG – Sistema Tomas Gomes</strong>, pronta.</li>
</ul>
<p>Todas as opções incluem chapa, montagem e prensagem. <strong>Os dentes são orçados à parte</strong>; consulte as opções com o atendimento. O valor de cada caso é informado sob orçamento.</p>

<h2>Como escolher entre as opções</h2>
<h3>PTR simples</h3>
<p>É a prótese total convencional em resina acrílica rosa, a opção mais econômica e indicada para a maioria dos casos.</p>
<h3>Palato incolor</h3>
<p>O palato em resina transparente deixa a prótese superior mais discreta e permite visualizar a mucosa por baixo da base, o que alguns profissionais usam para conferir áreas de compressão.</p>
<h3>Coloform especial (base caracterizada)</h3>
<p>É a <strong>prótese total caracterizada</strong>: a base recebe uma caracterização de cor que imita a gengiva natural, com resultado estético superior nas áreas que aparecem ao sorrir.</p>
<h3>Dupla prensagem</h3>
<p>A técnica usa duas etapas de prensagem para combinar cores ou materiais na base, com melhor acabamento.</p>
<h3>Sistema Tomas Gomes (STG)</h3>
<p>É um método de montagem e oclusão bastante difundido entre protesistas brasileiros e é a opção mais completa de prótese total do laboratório.</p>

<h2>Etapas da prótese total com o laboratório</h2>
<ol class="steps">
<li><strong>Modelo e moldeira individual</strong>, a partir da moldagem anatômica, quando o seu protocolo prevê essa etapa.</li>
<li><strong>Base de prova e plano de orientação</strong> em cera, para o registro da dimensão vertical e da relação cêntrica no consultório.</li>
<li><strong>Montagem dos dentes</strong> no articulador e prova estética e funcional no paciente.</li>
<li><strong>Prensagem, acabamento e polimento</strong> após a aprovação.</li>
</ol>
<p>Cada etapa tem prazo médio de 7 dias úteis. Com urgência, há acréscimo de 30% por etapa.</p>

<h2>Prótese total ou protocolo sobre implantes?</h2>
<p>Para pacientes que buscam uma solução fixa, a reabilitação sobre implantes é uma alternativa. Veja <a href="/servicos/protese-sobre-implante/">prótese protocolo e barra clips</a>. Para desdentados parciais, consulte <a href="/servicos/protese-parcial-removivel-ppr/">PPR</a> e <a href="/servicos/protese-flexivel-flexite/">prótese flexível</a>.</p>

<h2>Garantia</h2>
<p>{GARANTIA} Trabalhos não iniciados ou não finalizados no laboratório não têm garantia.</p>
''',
 faq=[
  ('Quanto custa uma prótese total no laboratório?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766, e depende da opção escolhida: simples, palato incolor, Coloform especial, dupla prensagem ou STG. Os dentes são orçados à parte.'),
  ('O que está incluído na PTR?', 'Chapa, montagem e prensagem. Os dentes são orçados à parte.'),
  ('O laboratório faz prótese total caracterizada?', 'Sim. A PTR Coloform especial tem a base caracterizada, com cor que imita a gengiva natural.'),
  ('Qual a diferença entre a PTR simples e a de palato incolor?', 'A simples tem a base toda em resina acrílica rosa. Na de palato incolor, o palato da prótese superior é em resina transparente, mais discreto.'),
  ('O que é PTR STG?', 'É a prótese total feita pelo Sistema Tomas Gomes, um método de montagem e oclusão, e é a opção mais completa de prótese total do laboratório.'),
 ],
 related=['protese-sobre-implante', 'protese-parcial-removivel-ppr', 'protese-flexivel-flexite'],
),
# ------------------------------------------------------------------ 6
dict(
 slug='protese-flexivel-flexite', nav='Prótese flexível (Flexite)',
 title='Prótese Flexível Flexite e Parcial em BH | LDA',
 desc='Prótese flexível Flexite unilateral e bilateral, sem grampo metálico aparente, e parciais em acrílico, feitas em BH pelo Lab. Dental Araújo. Envio ao Brasil.',
 kicker='Parcial e flexível', h1='Prótese flexível Flexite e parcial em acrílico <span class="hl">em BH</span>',
 lead='Parciais removíveis em resina flexível Flexite, sem grampo metálico aparente, e parciais em acrílico (simples, palato incolor, Coloform especial e dupla prensagem), entregues prontas.',
 img='real/protese-flexivel-flexite', img_alt='Prótese parcial flexível (Flexite) com grampos em resina rosa, sobre superfície espelhada',
 fig='real/protese-flexivel-flexite-lateral', fig_alt='Prótese parcial flexível (Flexite) vista de lado, com grampos da mesma resina', fig_cap='Prótese flexível (Flexite), vista lateral',
 primary='prótese flexível', secondary=['Flexite unilateral', 'prótese parcial removível flexível', 'parcial provisória em acrílico', 'prótese sem grampo metálico', 'laboratório de prótese flexível BH'],
 cats=['ppr-parcial'], service_type='Prótese parcial removível flexível (Flexite) e parcial em acrílico',
 blurb='Parcial Flexite unilateral e bilateral e parciais em acrílico.',
 body='''
<h2>O que é a prótese flexível Flexite?</h2>
<p>A <strong>prótese flexível</strong> é uma prótese parcial removível feita em resina termoplástica flexível. A <strong>Flexite</strong> é um dos materiais mais conhecidos desse tipo. Os grampos são feitos no próprio material, na cor da gengiva, então a prótese não tem grampos metálicos aparentes. Por isso, é muito procurada por pacientes que priorizam a estética e o conforto.</p>
<p>O <strong>Laboratório Dental Araújo</strong> confecciona <strong>parciais Flexite unilaterais e bilaterais</strong>, entregues prontas. Os dentes são orçados à parte, e o valor de cada caso é informado sob orçamento.</p>

<h2>Parciais em acrílico: opções</h2>
<p>Para casos provisórios, de transição ou de menor custo, o laboratório também faz parciais em resina acrílica:</p>
<ul>
<li><strong>Parcial simples</strong>, pronta.</li>
<li><strong>Parcial palato incolor</strong>, pronta.</li>
<li><strong>Parcial Coloform especial</strong>, pronta.</li>
<li><strong>Parcial dupla prensagem</strong>, pronta.</li>
</ul>
<p>Em todas as parciais, <strong>os dentes são orçados à parte</strong>.</p>

<h2>Quando indicar a prótese flexível</h2>
<p>A decisão é do cirurgião-dentista, que avalia o suporte, o número de dentes remanescentes e a higiene do paciente. Situações em que a parcial flexível costuma ser considerada:</p>
<ul>
<li>pacientes com exigência estética e restrição ao grampo metálico aparente;</li>
<li>alergia ou sensibilidade a componentes metálicos, quando confirmada pelo profissional;</li>
<li>casos de transição, como o período de osseointegração de implantes;</li>
<li>espaços protéticos curtos, com poucos dentes a repor.</li>
</ul>
<p>Em casos extensos, com extremidade livre ou que exigem apoio oclusal bem definido, a <a href="/servicos/protese-parcial-removivel-ppr/">PPR com armação Roach</a> tende a dar mais estabilidade. Vale discutir o caso com o laboratório antes da moldagem. Reunimos o que a literatura diz sobre as duas opções em <a href="/blog/ppr-ou-protese-flexivel/">PPR ou prótese flexível: quando indicar</a>.</p>

<h2>Unilateral ou bilateral?</h2>
<p>A parcial unilateral repõe dentes de apenas um lado do arco e é menor e mais simples. A bilateral se estende pelos dois lados e distribui melhor as forças quando há falhas dos dois lados. Indique na requisição os elementos a repor, a cor dos dentes e a cor da base.</p>

<h2>Como enviar um caso de prótese flexível</h2>
<ol class="steps">
<li>Moldagem do arco com boa cópia dos dentes pilares e do fundo de vestíbulo.</li>
<li>Moldagem do antagonista e registro de mordida.</li>
<li>Cor dos dentes e observações por escrito na requisição.</li>
<li>Prova da montagem dos dentes, quando o caso exigir, e finalização.</li>
</ol>
<p>{PRAZO}</p>

<h2>Garantia</h2>
<p>{GARANTIA}</p>
<p>Para pacientes totalmente desdentados, veja <a href="/servicos/protese-total/">prótese total</a>. Para placas e aparelhos removíveis, veja <a href="/servicos/placas-de-bruxismo-e-ortodontia/">placas e ortodontia</a>.</p>
''',
 faq=[
  ('Quanto custa uma prótese flexível Flexite?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. Fazemos Flexite unilateral e bilateral, e os dentes são orçados à parte.'),
  ('A prótese flexível tem grampo de metal?', 'Não. Os grampos são feitos na própria resina flexível, na cor da gengiva.'),
  ('Vocês fazem prótese flexível unilateral?', 'Sim. Fazemos a parcial Flexite unilateral, para repor dentes de um lado do arco, e a bilateral. Os dentes são orçados à parte.'),
  ('Quando usar a parcial em acrílico?', 'Ela costuma ser usada em casos provisórios, de transição ou de menor custo. A indicação é sempre do cirurgião-dentista.'),
 ],
 related=['protese-parcial-removivel-ppr', 'protese-total', 'resinas-e-provisorios'],
),
# ------------------------------------------------------------------ 7
dict(
 slug='resinas-e-provisorios', nav='Resinas e provisórios',
 title='Coroa de Resina Ceramage e Provisórios em BH | LDA',
 desc='Coroa de resina Ceramage, ponte fixa com fibra, restaurado em resina e coroa provisória em acrílico, feitos em BH pelo Laboratório Dental Araújo.',
 kicker='Resinas foto e acrílica', h1='Coroa de resina e provisórios: <span class="hl">laboratório em BH</span>',
 lead='Coroas totais, pontes com fibra e restaurados em resina Ceramage, resina popular ou acrílico, além de coroas provisórias, para casos estéticos, de transição ou com orçamento mais curto.',
 img='foto/escultura-resina', img_alt='Técnico trabalhando uma peça em resina sobre o modelo',
 fig='foto/modelo-gesso-maos', fig_alt='Modelo de gesso com dentes nas mãos do técnico', fig_cap='Provisórios bem adaptados protegem o preparo até a peça definitiva.',
 primary='coroa de resina Ceramage', secondary=['coroa provisória de laboratório', 'ponte fixa com fibra', 'restaurado em resina', 'provisório em acrílico'],
 cats=['resinas'], service_type='Prótese em resina laboratorial e provisórios em acrílico',
 blurb='Coroas, pontes com fibra e restaurados em Ceramage, resina popular e acrílico.',
 body='''
<h2>Resinas no laboratório: para que servem</h2>
<p>As resinas laboratoriais ocupam um espaço importante entre a cerâmica e o provisório de consultório. Elas permitem coroas e pontes estéticas com custo menor, restaurados indiretos, provisórios de longa duração e soluções de transição durante tratamentos com implantes ou ortodontia. O <strong>Laboratório Dental Araújo</strong>, em Belo Horizonte, trabalha com <strong>resina Ceramage</strong>, resina popular e resina acrílica.</p>

<h2>O que fazemos em resina foto e acrílica</h2>
<h3>Coroas</h3>
<ul>
<li>Coroa total em resina Ceramage, com ou sem fibra.</li>
<li>Coroa total em resina popular, com ou sem fibra.</li>
<li>Coroa em acrílico.</li>
<li>Coroa provisória em acrílico.</li>
</ul>
<h3>Pontes (orçadas por elemento)</h3>
<ul>
<li>Ponte fixa com fibra em resina Ceramage.</li>
<li>Ponte fixa com fibra em resina popular.</li>
<li>Ponte fixa com fibra acrílica.</li>
<li>Ponte provisória com fibra acrílica.</li>
</ul>
<h3>Restaurados</h3>
<ul>
<li>Restaurado em resina Ceramage, com ou sem fibra.</li>
<li>Restaurado em resina popular.</li>
</ul>
<p>Consulte os tipos de resina disponíveis. Fale com o atendimento para alinhar a melhor opção para o caso e pedir o orçamento.</p>

<h2>Ceramage, resina popular ou acrílico?</h2>
<p>A <strong>Ceramage</strong>, da Shofu, é uma resina composta de uso laboratorial, com carga cerâmica, conhecida pela boa estética e pela facilidade de reparo. É indicada para coroas e restaurados quando o dentista quer um resultado estético com custo menor que a cerâmica. A <strong>resina popular</strong> é a alternativa mais econômica para coroas definitivas de menor exigência estética. O <strong>acrílico</strong> é o material clássico dos provisórios e das pontes de transição.</p>
<p>A <strong>fibra</strong> reforça a estrutura de coroas e pontes em resina e aumenta a resistência à fratura, principalmente em pontes e em pacientes com maior carga oclusal.</p>

<h2>Provisórios de laboratório</h2>
<p>Um provisório bem feito protege o preparo, mantém a saúde gengival, preserva os espaços e permite testar a estética antes da peça definitiva. Os provisórios de laboratório costumam ter melhor adaptação, polimento e durabilidade que os feitos diretamente no consultório, o que é útil em tratamentos longos, como reabilitações com implantes. Veja também <a href="/servicos/protese-sobre-implante/">prótese sobre implante</a>.</p>

<h2>Quando partir para a cerâmica</h2>
<p>Para resultados definitivos de alta estética e longevidade, a cerâmica costuma ser a escolha. Compare em <a href="/servicos/zirconia-e-max/">zircônia e E-Max</a> e <a href="/servicos/metaloceramica/">metalocerâmica</a>.</p>

<h2>Prazos e garantia</h2>
<p>{PRAZO} {GARANTIA}</p>
''',
 faq=[
  ('Quanto custa uma coroa em resina Ceramage?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. A coroa em Ceramage pode ser feita com ou sem fibra.'),
  ('Quanto custa uma coroa provisória de laboratório?', 'Sob orçamento, pelo WhatsApp ou pelo telefone. O laboratório faz coroas e pontes provisórias em acrílico.'),
  ('A ponte em resina é orçada por elemento?', 'Sim. As pontes em resina e em acrílico são orçadas por elemento.'),
  ('O que é a resina Ceramage?', 'É uma resina composta de uso laboratorial, com carga cerâmica, fabricada pela Shofu. É usada em coroas e restaurados quando se busca estética com custo menor que a cerâmica.'),
 ],
 related=['zirconia-e-max', 'metaloceramica', 'protese-sobre-implante'],
),
# ------------------------------------------------------------------ 8
dict(
 slug='placas-de-bruxismo-e-ortodontia', nav='Placas e ortodontia',
 title='Placa de Bruxismo e Ortodontia em BH | Lab. Araújo',
 desc='Placa de bruxismo rígida em acrílico, cristal ou emborrachada, placa de clareamento, protetor bucal, anti-ronco e contenções, feitos por laboratório em BH.',
 kicker='Placas, ortodontia e ortopedia', h1='Placa de bruxismo e ortodontia: <span class="hl">laboratório em BH</span>',
 lead='Placas de bruxismo, clareamento e esporte, aparelho anti-ronco, aparelhos ortodônticos móveis e contenções. Confeccionamos todos os tipos e modelos de ortodontia e ortopedia.',
 img='real/aparelho-odontoapneia', img_alt='Aparelho anti-ronco (Odonto Apneia) em acrílico transparente, com as peças superior e inferior',
 fig='real/aparelhos-removiveis-sobre-modelos', fig_alt='Aparelhos ortodônticos removíveis com arco vestibular sobre modelos de gesso', fig_cap='Aparelhos removíveis sobre modelos',
 primary='placa de bruxismo (laboratório)', secondary=['placa miorrelaxante em acrílico', 'placa de clareamento', 'protetor bucal personalizado', 'contenção ortodôntica', 'aparelho anti-ronco'],
 cats=['placas'], service_type='Placas oclusais, protetores bucais e aparelhos ortodônticos removíveis',
 blurb='Placas de bruxismo, clareamento e esporte, anti-ronco, aparelhos e contenções.',
 body='''
<h2>Laboratório que faz placa de bruxismo em BH</h2>
<p>O <strong>Laboratório Dental Araújo</strong> confecciona <strong>placas de bruxismo</strong> e outros dispositivos intraorais para dentistas de Belo Horizonte e de todo o Brasil. Há três opções: cristal, emborrachada e acrílico prensada. A placa é feita sobre o modelo do paciente, a partir da moldagem enviada pelo consultório, com acabamento e polimento para o conforto do uso noturno.</p>

<h2>Placas que o laboratório faz</h2>
<ul>
<li>Placa de clareamento.</li>
<li>Placa de bruxismo cristal.</li>
<li>Placa de bruxismo emborrachada.</li>
<li>Placa de bruxismo em acrílico prensada.</li>
<li>Placa para esportes comuns.</li>
<li>Placa para luta.</li>
</ul>

<h2>Cristal, emborrachada ou acrílico prensada?</h2>
<p>A <strong>placa cristal</strong> é rígida e transparente, termoformada a partir do modelo. É uma opção prática e econômica. A <strong>emborrachada</strong> é mais macia e costuma ser escolhida pelo conforto. A <strong>acrílica prensada</strong> é a opção mais robusta e permite ajuste oclusal preciso no consultório, por isso é a mais usada como placa miorrelaxante. A escolha depende do diagnóstico do dentista.</p>

<h2>Protetor bucal personalizado para esporte e luta</h2>
<p>Os protetores feitos em laboratório, sobre o modelo do atleta, se adaptam melhor e incomodam menos que os modelos pré-fabricados, o que estimula o uso. Fazemos duas opções: placa para esportes comuns e placa para luta, esta com proteção reforçada para esportes de contato.</p>

<h2>Aparelho anti-ronco (Odonto Apneia)</h2>
<p>O aparelho anti-ronco é um dispositivo intraoral de avanço mandibular usado no tratamento do ronco e da apneia obstrutiva do sono, sempre com indicação e acompanhamento profissional.</p>

<h2>Ortodontia e ortopedia</h2>
<ul>
<li>Aparelho ortodôntico móvel.</li>
<li>Contenção em fio.</li>
<li>Contenção ortodôntica estética (transparente).</li>
<li>Contenção 3x3.</li>
</ul>
<p>Confeccionamos todos os tipos e modelos de ortodontia e ortopedia funcional dos maxilares. Para aparelhos que não estão listados, envie a prescrição e solicite um orçamento pelo WhatsApp.</p>

<h2>O que enviar</h2>
<ol class="steps">
<li>Moldagem (ou modelo) do arco e, quando necessário, do antagonista.</li>
<li>Registro de mordida para placas oclusais e aparelhos de avanço mandibular.</li>
<li>Prescrição detalhada: tipo de placa, espessura, arco, desenho do aparelho e elementos ativos.</li>
</ol>
<p>{PRAZO}</p>

<h2>Garantia e outras soluções</h2>
<p>{GARANTIA} Para próteses removíveis, veja <a href="/servicos/protese-parcial-removivel-ppr/">PPR</a> e <a href="/servicos/protese-flexivel-flexite/">prótese flexível</a>.</p>
''',
 faq=[
  ('Quanto custa uma placa de bruxismo no laboratório?', 'O valor é informado sob orçamento, pelo WhatsApp (31) 98652-1387 ou pelo telefone (31) 3271-9766. Há três opções: cristal, emborrachada e acrílico prensada.'),
  ('Qual placa de bruxismo o laboratório faz: rígida ou macia?', 'As duas. A placa em acrílico prensada e a cristal são rígidas; a emborrachada é macia. A acrílica prensada permite ajuste oclusal preciso no consultório. O tipo é definido pelo diagnóstico do dentista.'),
  ('Vocês fazem aparelho anti-ronco?', 'Sim. O laboratório confecciona o aparelho anti-ronco (Odonto Apneia), sempre com indicação e acompanhamento do dentista. Peça um orçamento pelo WhatsApp.'),
  ('Vocês fazem todos os tipos de aparelho ortodôntico?', 'Sim. O laboratório confecciona todos os tipos e modelos de ortodontia e ortopedia. Envie a prescrição e solicite um orçamento.'),
 ],
 related=['protese-flexivel-flexite', 'resinas-e-provisorios', 'protese-parcial-removivel-ppr'],
),
]

def porque(s):
    """Bloco comum 'por que o LDA' com o nome do serviço (complementa o conteúdo original de cada página)."""
    return f'''
<h2>Por que dentistas escolhem o Laboratório Dental Araújo para {s["nav"][0].lower() + s["nav"][1:] if s["nav"][1:2].islower() else s["nav"]}</h2>
<ul>
<li><strong>Desde 1975:</strong> estamos no Centro de Belo Horizonte há 50 anos, com sede própria no Edifício Mesbla.</li>
<li><strong>Equipe:</strong> mais de 40 profissionais qualificados, em 10 salas com maquinário de última geração.</li>
<li><strong>Orçamento direto:</strong> peça pelo WhatsApp ou pelo telefone, informando o tipo de trabalho, o material e os elementos.</li>
<li><strong>Logística:</strong> coleta e entrega em Minas Gerais e atendimento a dentistas de todo o Brasil.</li>
<li><strong>Comunicação direta:</strong> atendimento por telefone e WhatsApp para alinhar cor, material, prazos e detalhes técnicos antes de começar o trabalho.</li>
</ul>
<p>Para pedir um orçamento, veja os <a href="/contato/">canais de contato</a>. Dúvidas sobre prazos, urgência, garantia e envio estão nas <a href="/perguntas-frequentes/">perguntas frequentes</a>.</p>
'''
