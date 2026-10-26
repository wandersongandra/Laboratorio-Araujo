"""
Documentos legais do site: Política de Privacidade (LGPD) e Termos de Uso.

Cada documento é um dict com título, resumo e uma lista de seções (id, título, HTML).
O build gera o sumário ("Neste documento") a partir dos ids, por isso cada id precisa
ser único na página.

ATENÇÃO: estes textos são um modelo preparado a partir das informações públicas do
laboratório e da Lei 13.709/2018. Devem ser revisados pelo laboratório e, de preferência,
por um advogado antes de serem tratados como versão definitiva (ver docs/ARQUITETURA.md).
"""

VIGENCIA = '24/10/2026'
EMAIL = 'dentalaraujo@yahoo.com.br'
CONTROLADOR = ('Laboratório Dental Araújo Ltda, CNPJ 19.223.635/0001-86, Av. Afonso Pena, 262, 16º andar, '
               'sala 1602, Edifício Mesbla, Centro, Belo Horizonte/MG, CEP 30130-923')

_EXT = 'target="_blank" rel="noopener noreferrer"'
LGPD = f'<a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm" {_EXT}>Lei 13.709/2018 (LGPD)</a>'
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

PRIVACIDADE = {
    'path': '/politica-de-privacidade/',
    'name': 'Política de privacidade',
    'title': 'Política de Privacidade | Laboratório Dental Araújo',
    'desc': 'Como o Laboratório Dental Araújo trata dados pessoais no site e no atendimento a dentistas e clínicas, conforme a LGPD, e como exercer seus direitos.',
    'kicker': 'Documento · LGPD',
    'h1': 'Política de privacidade',
    'lead': 'Quais dados pessoais o site e o atendimento do laboratório tratam, para quê, com quem são compartilhados e como você exerce seus direitos.',
    'sections': [
        ('controlador', 'Quem é o controlador', f'''
<p>Esta política vale para o site do Laboratório Dental Araújo e para o atendimento a cirurgiões-dentistas e clínicas por telefone, WhatsApp e e-mail. O controlador dos dados pessoais tratados nesses canais é:</p>
<p><strong>{CONTROLADOR}</strong>.</p>
<p>Para qualquer assunto sobre dados pessoais, o canal de contato é o e-mail {MAIL}. O texto segue a {LGPD}.</p>'''),
        ('resumo', 'Resumo', '''
<table>
<caption>Visão geral do tratamento de dados</caption>
<thead><tr><th scope="col">Tema</th><th scope="col">Como funciona</th></tr></thead>
<tbody>
<tr><td>Formulários e cadastro no site</td><td>Não há. O contato é feito por WhatsApp, telefone ou e-mail.</td></tr>
<tr><td>Cookies e ferramentas de análise</td><td>O site não grava cookies próprios e não usa ferramentas de análise de audiência ou publicidade.</td></tr>
<tr><td>Registros técnicos</td><td>A hospedagem registra dados técnicos de acesso, como endereço IP e navegador.</td></tr>
<tr><td>Dados de pacientes</td><td>Chegam junto com o caso enviado pelo dentista e são usados só para confeccionar e identificar o trabalho.</td></tr>
<tr><td>Venda de dados</td><td>O laboratório não vende nem aluga dados pessoais.</td></tr>
</tbody>
</table>'''),
        ('dados-site', 'Dados tratados ao visitar o site', f'''
<p>O site é informativo e pode ser lido sem nenhum cadastro.</p>
<ul>
<li><strong>Registros de acesso.</strong> O provedor de hospedagem (Netlify) registra automaticamente dados técnicos de cada acesso, como endereço IP, data e hora, página pedida, navegador e sistema operacional. Esses registros servem para entregar as páginas, manter o site seguro e investigar falhas ou abusos. Veja a <a href="https://www.netlify.com/privacy/" {_EXT}>política de privacidade da Netlify</a>.</li>
<li><strong>Mapa.</strong> Na página de contato, o mapa do Google só é carregado quando você clica para abri-lo. A partir desse clique, o Google recebe dados do seu acesso conforme a <a href="https://policies.google.com/privacy" {_EXT}>política de privacidade do Google</a>.</li>
<li><strong>Links de contato.</strong> Os botões de WhatsApp, telefone e e-mail abrem o aplicativo correspondente no seu aparelho. O site não registra o conteúdo da conversa. No WhatsApp, vale também a <a href="https://www.whatsapp.com/legal/privacy-policy" {_EXT}>política de privacidade do WhatsApp</a>.</li>
<li><strong>Redes sociais.</strong> Os links para Instagram e Facebook levam a sites de terceiros, com políticas próprias.</li>
</ul>
<p>As fontes, imagens e scripts do site são servidos pelo próprio domínio, sem chamadas a serviços de terceiros antes de você clicar no mapa ou em um link externo.</p>'''),
        ('dados-dentistas', 'Dados de dentistas e clínicas', '''
<p>Quando você entra em contato ou envia um caso, o laboratório trata os dados necessários para atender e prestar o serviço:</p>
<ul>
<li>nome, CRO, nome da clínica, CPF ou CNPJ, quando necessários para identificação e faturamento;</li>
<li>telefone, número de WhatsApp, e-mail e endereço do consultório, para contato, coleta e entrega;</li>
<li>histórico de pedidos, requisições, orçamentos, prazos e recados por escrito sobre os trabalhos;</li>
<li>dados de pagamento e cobrança, como valores, vencimentos e comprovantes.</li>
</ul>'''),
        ('dados-pacientes', 'Dados de pacientes', '''
<p>A requisição e o material enviados pelo dentista podem conter dados do paciente, como nome ou iniciais, cor dos dentes, moldagens, modelos, fotografias intraorais e informações clínicas sobre o trabalho. Dados referentes à saúde são <strong>dados pessoais sensíveis</strong> e recebem proteção reforçada.</p>
<ul>
<li>O laboratório não atende pacientes diretamente. O relacionamento com o paciente é do cirurgião-dentista, que decide quais dados enviar e responde pelo atendimento clínico.</li>
<li>Os dados de pacientes são usados apenas para confeccionar, identificar, conferir e devolver o trabalho, e para atender à garantia.</li>
<li>Pedimos que a requisição traga só o necessário para identificar o caso. Iniciais ou um código interno da clínica costumam ser suficientes.</li>
<li>O tratamento se apoia na tutela da saúde, em procedimento realizado por profissionais de saúde ou serviços de saúde (art. 11, II, "f", da LGPD), e no exercício regular de direitos, inclusive em contrato (art. 11, II, "d").</li>
</ul>
<p>Pacientes que quiserem exercer seus direitos podem procurar o dentista responsável pelo tratamento ou escrever para o laboratório, que encaminhará o pedido ou responderá conforme o seu papel no caso.</p>'''),
        ('finalidades', 'Finalidades e bases legais', '''
<table>
<caption>Para que usamos os dados e com qual fundamento</caption>
<thead><tr><th scope="col">Finalidade</th><th scope="col">Base legal (LGPD)</th></tr></thead>
<tbody>
<tr><td>Responder contatos e preparar orçamentos</td><td>Procedimentos preliminares a contrato, a pedido do titular (art. 7º, V)</td></tr>
<tr><td>Confeccionar, entregar e dar garantia aos trabalhos</td><td>Execução de contrato (art. 7º, V); para dados de saúde, art. 11, II, "d" e "f"</td></tr>
<tr><td>Emitir notas, cobrar e manter registros fiscais e contábeis</td><td>Cumprimento de obrigação legal ou regulatória (art. 7º, II)</td></tr>
<tr><td>Manter o site no ar, seguro e com registros de acesso</td><td>Legítimo interesse (art. 7º, IX) e obrigação legal, quando aplicável (art. 7º, II)</td></tr>
<tr><td>Defender o laboratório em processos administrativos ou judiciais</td><td>Exercício regular de direitos (art. 7º, VI, e art. 11, II, "d")</td></tr>
</tbody>
</table>
<p>O laboratório não toma decisões baseadas unicamente em tratamento automatizado de dados pessoais.</p>'''),
        ('compartilhamento', 'Compartilhamento', '''
<p>Os dados são compartilhados apenas quando necessário para as finalidades acima:</p>
<ul>
<li><strong>Hospedagem do site</strong> (Netlify), que processa os registros técnicos de acesso.</li>
<li><strong>Correios e transportadoras</strong>, com os dados de endereço e identificação necessários para coleta, envio e devolução dos trabalhos.</li>
<li><strong>Google</strong>, se você abrir o mapa, e <strong>WhatsApp (Meta)</strong>, se escolher falar por esse canal.</li>
<li><strong>Prestadores de serviços contábeis e jurídicos</strong>, quando necessário para cumprir obrigações legais ou defender direitos.</li>
<li><strong>Autoridades públicas</strong>, mediante requisição legal ou ordem judicial.</li>
</ul>'''),
        ('transferencia', 'Transferência internacional', '''
<p>Alguns fornecedores, como a hospedagem do site e os aplicativos de mensagem, podem armazenar dados em servidores fora do Brasil. Nesses casos, a transferência ocorre nas hipóteses permitidas pelo art. 33 da LGPD, com fornecedores que adotam medidas de proteção compatíveis.</p>'''),
        ('retencao', 'Por quanto tempo guardamos', '''
<p>Os dados ficam guardados pelo tempo necessário para cumprir as finalidades desta política: atender ao pedido, cumprir o prazo de garantia, atender obrigações fiscais, contábeis e legais e permitir a defesa do laboratório enquanto houver prazo para reclamações. Os registros técnicos de acesso seguem os prazos do provedor de hospedagem e da legislação aplicável.</p>
<p>Terminado o prazo, os dados são eliminados ou anonimizados, salvo quando a lei permitir ou exigir a conservação.</p>'''),
        ('cookies', 'Cookies', '''
<p>O site não grava cookies próprios e não usa ferramentas de análise de audiência, publicidade ou remarketing. Serviços de terceiros abertos por você, como o mapa do Google ou o WhatsApp, podem usar cookies próprios, conforme as políticas desses serviços. Se o laboratório passar a usar ferramentas desse tipo, esta política será atualizada antes.</p>'''),
        ('seguranca', 'Segurança', '''
<p>O site é servido apenas por HTTPS, com HSTS e uma política de segurança de conteúdo (CSP) que bloqueia scripts de origens não autorizadas. No laboratório, o acesso a requisições, modelos e dados de clientes é restrito a quem precisa deles para o trabalho.</p>
<p>Nenhum sistema é totalmente imune a incidentes. Se ocorrer um incidente de segurança que possa gerar risco ou dano relevante aos titulares, o laboratório comunicará a Autoridade Nacional de Proteção de Dados (ANPD) e os titulares afetados, nos termos do art. 48 da LGPD.</p>'''),
        ('direitos', 'Seus direitos', '''
<p>Como titular de dados pessoais, você pode pedir ao laboratório, nos termos do art. 18 da LGPD:</p>
<ul>
<li>a confirmação de que existe tratamento dos seus dados;</li>
<li>o acesso aos dados;</li>
<li>a correção de dados incompletos, inexatos ou desatualizados;</li>
<li>a anonimização, o bloqueio ou a eliminação de dados desnecessários, excessivos ou tratados em desconformidade com a lei;</li>
<li>a portabilidade dos dados a outro fornecedor, observados os segredos comercial e industrial;</li>
<li>a eliminação dos dados tratados com base no seu consentimento, salvo as hipóteses de conservação previstas em lei;</li>
<li>informação sobre as entidades com as quais o laboratório compartilhou seus dados;</li>
<li>informação sobre a possibilidade de não fornecer consentimento e sobre as consequências da negativa;</li>
<li>a revogação do consentimento, quando ele for a base do tratamento.</li>
</ul>
<p>Você também pode se opor a tratamento feito com base em outra hipótese legal, se houver descumprimento da lei.</p>'''),
        ('exercer', 'Como exercer seus direitos', f'''
<p>Envie o pedido para {MAIL}, informando o seu nome, um meio de contato e o direito que deseja exercer. Para proteger seus dados, podemos pedir informações que confirmem a sua identidade antes de responder.</p>
<p>A confirmação de existência ou o acesso aos dados podem ser fornecidos de forma simplificada, imediatamente, ou por declaração completa em até 15 dias contados do pedido (art. 19 da LGPD). Se não for possível atender ao pedido, explicaremos o motivo.</p>
<p>Você também pode peticionar à <a href="https://www.gov.br/anpd/pt-br" {_EXT}>Autoridade Nacional de Proteção de Dados (ANPD)</a>.</p>'''),
        ('canal', 'Canal de comunicação', f'''
<p>O canal de comunicação com titulares e com a ANPD é o e-mail {MAIL}. As solicitações também podem ser entregues por escrito no endereço do laboratório, na Av. Afonso Pena, 262, sala 1602, Centro, Belo Horizonte/MG.</p>'''),
        ('publico', 'Público do site', '''
<p>O site é voltado a cirurgiões-dentistas, clínicas e profissionais da odontologia. Não é direcionado a crianças e adolescentes, e o laboratório não coleta intencionalmente dados desse público pelo site.</p>'''),
        ('alteracoes', 'Alterações desta política', f'''
<p>Esta política pode ser atualizada para refletir mudanças no site, nos serviços ou na legislação. A versão em vigor é sempre a publicada nesta página, com a data de atualização abaixo.</p>
<p><strong>Vigente desde {VIGENCIA}.</strong></p>'''),
    ],
}

TERMOS = {
    'path': '/termos-de-uso/',
    'name': 'Termos de uso',
    'title': 'Termos de Uso | Laboratório Dental Araújo',
    'desc': 'Termos de uso do site do Laboratório Dental Araújo: público profissional, orçamento, prazos, garantia, pagamento, propriedade intelectual e foro.',
    'kicker': 'Documento · Termos',
    'h1': 'Termos de uso',
    'lead': 'Regras de uso do site e as condições gerais de atendimento do laboratório a cirurgiões-dentistas e clínicas.',
    'sections': [
        ('sobre', 'Sobre estes termos', f'''
<p>Estes termos regulam o uso do site do Laboratório Dental Araújo. Ao navegar pelo site, você concorda com eles. Se não concordar, não utilize o site.</p>
<p>O site é mantido por <strong>{CONTROLADOR}</strong>.</p>'''),
        ('publico', 'Quem atendemos', '''
<p>O Laboratório Dental Araújo é um laboratório de prótese dentária. Os serviços são prestados a <strong>cirurgiões-dentistas e clínicas odontológicas</strong>, em relação entre profissionais e empresas. O laboratório não atende pacientes diretamente: a indicação clínica, o planejamento e a instalação dos trabalhos são de responsabilidade do cirurgião-dentista.</p>'''),
        ('uso', 'Uso permitido do site', '''
<p>Você pode navegar, ler e compartilhar os links do site. Não é permitido:</p>
<ul>
<li>usar o site para fins ilícitos ou que prejudiquem o laboratório ou terceiros;</li>
<li>tentar acessar áreas, sistemas ou dados sem autorização, ou interferir no funcionamento do site;</li>
<li>copiar o site ou partes dele para se passar pelo laboratório.</li>
</ul>'''),
        ('informativo', 'Conteúdo informativo', '''
<p>Textos, artigos e respostas publicados no site têm caráter informativo e geral. Não substituem a avaliação clínica do cirurgião-dentista, que é quem indica o material e o tipo de prótese para cada paciente. O laboratório procura manter as informações corretas e atualizadas, mas pode alterá-las a qualquer momento.</p>'''),
        ('orcamento', 'Valores e orçamento', '''
<p>O site não publica preços. Os valores dos serviços são informados <strong>sob orçamento</strong>, pelo WhatsApp (31) 98652-1387 ou pelos telefones (31) 3271-9766 e (31) 3271-9688. Dentes, soldas, componentes protéticos, ligas metálicas e outros itens indicados no atendimento são orçados à parte.</p>'''),
        ('prazos', 'Prazos e urgência', '''
<p>O prazo médio é de <strong>7 dias úteis por etapa</strong> e pode variar conforme a demanda. Trabalhos solicitados com urgência têm acréscimo de <strong>30% em cada etapa</strong>. Para casos enviados de outros estados, o tempo de transporte é somado ao prazo de laboratório.</p>'''),
        ('pedidos', 'Pedidos, requisição e envio', '''
<p>Cada caso deve vir com a requisição preenchida: material, elementos, cor, etapa e observações. Recados e informações extras devem ser enviados <strong>por escrito</strong>, junto com a requisição. O laboratório faz coleta e entrega em Minas Gerais. Para os demais estados, a forma de envio e de retorno é combinada no atendimento.</p>'''),
        ('garantia', 'Garantia', '''
<p>Os trabalhos têm garantia de até <strong>6 meses</strong> para defeito comprovado na confecção da peça, válida para serviços 100% realizados no laboratório. Trabalhos não iniciados ou não finalizados no laboratório não têm garantia.</p>'''),
        ('pagamento', 'Pagamento', '''
<p>O pagamento dos serviços deve ser feito até o <strong>dia 10</strong> de cada mês. Outras condições, quando houver, são combinadas diretamente com o laboratório.</p>'''),
        ('propriedade', 'Propriedade intelectual', '''
<p>Os textos, a marca, o logotipo, o projeto gráfico e a organização do conteúdo do site pertencem ao Laboratório Dental Araújo ou são usados com autorização. Você pode citar trechos com indicação da fonte e link para a página. Reproduzir o conteúdo para fins comerciais depende de autorização por escrito.</p>
<p>Algumas fotografias são ilustrativas, de bancos de imagens licenciados, e estão identificadas como tal. Elas não mostram trabalhos de pacientes do laboratório.</p>'''),
        ('links', 'Links para sites de terceiros', '''
<p>O site tem links para serviços de terceiros, como WhatsApp, Google Maps, Instagram e Facebook. Esses serviços têm termos e políticas próprios, e o laboratório não responde pelo conteúdo nem pelas práticas deles.</p>'''),
        ('responsabilidade', 'Limitação de responsabilidade', '''
<p>O laboratório se esforça para manter o site disponível e seguro, mas não garante funcionamento ininterrupto ou livre de erros. Na extensão permitida pela lei, o laboratório não responde por danos decorrentes de indisponibilidade temporária do site, do uso das informações gerais publicadas sem avaliação profissional ou de falhas em serviços de terceiros. Nada nestes termos afasta responsabilidades que a lei não permita limitar.</p>'''),
        ('privacidade', 'Privacidade', '''
<p>O tratamento de dados pessoais no site e no atendimento está descrito na <a href="/politica-de-privacidade/">política de privacidade</a>.</p>'''),
        ('alteracoes', 'Alterações destes termos', f'''
<p>Estes termos podem ser atualizados a qualquer momento. A versão em vigor é a publicada nesta página. <strong>Vigentes desde {VIGENCIA}.</strong></p>'''),
        ('foro', 'Lei aplicável e foro', '''
<p>Estes termos são regidos pela lei brasileira. Fica eleito o foro da Comarca de Belo Horizonte/MG para resolver questões relacionadas a eles, salvo disposição legal em contrário.</p>'''),
        ('contato', 'Contato', f'''
<p>Dúvidas sobre estes termos podem ser enviadas para {MAIL} ou tratadas pelos telefones (31) 3271-9766 e (31) 3271-9688. Veja também a página de <a href="/contato/">contato</a>.</p>'''),
    ],
}
