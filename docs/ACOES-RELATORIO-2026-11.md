# Ações verificadas — Auditoria de novembro de 2026

Este plano distingue correções no site de decisões que dependem do Laboratório Dental Araújo. **Não publicar depoimentos, números de CRO ou capacidades operacionais sem confirmação documental.**

## Implementado no código

- Cadastro de inscrição do laboratório (`laboratoryCro`) e de responsável técnico (`technicalLeadName` / `technicalLeadCro`) em `src/site/data/site.json`. Quando preenchidos e validados, o build mostra os registros no rodapé, na ficha técnica de `/sobre/` e nos dados estruturados LocalBusiness. Sem dados, os campos são omitidos e o build alerta; nenhum nome fictício aparece.
- Destaque discreto na home para consulta de envio digital; seção específica em `/envio-para-todo-brasil/#fluxo-digital` com orientação de compatibilidade STL/PLY/OBJ e contato pré-preenchido para confirmação, sem afirmar aceitação de arquivos.
- Correção dos textos que davam 50 anos completos em 2026, quando a fundação de 8/9/1975 já ultrapassa 50 anos.
- Seção de avaliações públicas na home: citação literal de Bruno A. Lopes Salles e nota de cinco estrelas de Thatiana Vieira, ambas conforme captura do Google fornecida em 4/11/2026. A segunda avaliação não tinha texto e não recebeu uma citação inventada. Não foi publicada média agregada, contagem de avaliações ou CRO não verificado. Avaliações de pessoas ligadas à empresa ou ao desenvolvimento do site não foram usadas como depoimentos independentes.
- Testes automatizados para não publicar RT parcial, escapar marcação e preservar o JSON-LD.
- Revisão de pré-produção: corrigidos descritores incorretos de imagens responsivas (`srcset`) e referências duplicadas; adicionada a conferência de dimensão real (`node tools/qa-srcset.mjs`, requer ImageMagick). Corrigido o estado `aria-expanded` do submenu ao fechá-lo com Escape ou com o menu mobile.
- URLs de SEO sempre usam uma origem HTTPS na raiz: domínio existente como fallback e `SITE_BASE` para a migração ao domínio próprio. Sitemap e canonicals passam a ser comparados rota a rota na QA local.
- Adicionada verificação automática de PR com instalação reproduzível, lint, testes, checagem de imagens e axe em desktop/celular. O primeiro resultado da execução no GitHub deve ser verificado antes de liberar a alteração.

## Confirmar com o laboratório antes da próxima publicação

1. **Prioridade legal:** número de inscrição do laboratório no CRO-MG, nome completo do responsável técnico e respectiva inscrição profissional. Depois, preencher `src/site/data/site.json` e verificar as saídas de build. Consultar o CRO-MG em caso de dúvida quanto à forma de identificação.
2. **Fluxo digital:** confirmar se recebe escaneamentos intraorais; quais formatos exatos (STL, PLY, OBJ), sistemas e plataformas; canal seguro de entrega, limite de tamanho, requisitos e tratamento de dados de pacientes. Só depois alterar o texto consultivo para uma afirmação de serviço confirmado.
3. **Prova social profissional:** a home já exibe avaliações públicas existentes, identificadas como tal, sem afirmar que os autores são dentistas. Para adicionar depoimentos de cirurgiões-dentistas, obter depoimentos autênticos de clientes com autorização específica para publicar nome, CRO e fala exata. Verificar com responsável técnico a pertinência da divulgação e as regras de publicidade odontológica. Não usar textos ou identidades de exemplo no site público.
4. **Google Business Profile:** conferir titularidade, categoria e endereço idêntico ao site, fotos reais, horário de funcionamento e avaliações autênticas. A revisão do perfil ocorre na conta do proprietário, não por alterações ao HTML.
5. **Simulador de prazos:** só especificar estimativas por tipo de prótese após obter dados validados da operação. Até lá, manter a média de 7 dias úteis *por etapa* e confirmação humana, sem prometer uma data final.

## Validação e publicação

Com Node.js: `SITE_BASE=https://DOMINIO-REAL npm run build`, `npm run test:registry`, `npm run test:base`, `node tools/qa-static.mjs` e `node tools/qa-srcset.mjs`. A suíte completa requer as dependências de desenvolvimento instaladas (`npm ci`, `npm run qa`). A publicação exige revisão do laboratório e execução de CI antes de merge. Para conectar o domínio, seguir [DOMINIO-PRODUCAO.md](./DOMINIO-PRODUCAO.md).
