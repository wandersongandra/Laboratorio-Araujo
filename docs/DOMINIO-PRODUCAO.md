# Preparação do domínio de produção — Laboratório Dental Araújo

## Estado antes da compra

- A versão atual usa `https://laboratorio-araujo.gandratecnologia.workers.dev` como origem padrão de SEO. Isto mantém os builds existentes com URLs absolutas e sem depender de variável na Cloudflare.
- **A compra do domínio não foi realizada neste projeto.** Não trocar `SITE_BASE` nem dados publicados por um endereço hipotético.
- Para publicar com a marca própria, escolher **um único domínio canônico** (ex.: domínio raiz *ou* `www`, mas não ambos). As outras variantes devem responder com redirecionamento permanente para a versão escolhida.

## Após a compra, antes de liberar o novo endereço

1. Adicionar o domínio ao Cloudflare e concluir a verificação da zona/DNS, ou seguir o fluxo de domínio gerenciado no painel. Evitar apontar registros conflitantes para provedores de hospedagem anteriores.
2. No painel **Workers & Pages → Worker `laboratorio-araujo` → Settings → Domains & Routes**, vincular o domínio canônico como **Custom Domain**. Validar TLS/HTTPS ativo e acesso a `/`, `/servicos/`, `/trabalhos/` e `/contato/`.
3. Na **configuração do build** do projeto conectado ao Git, definir `SITE_BASE=https://DOMINIO-CANONICO` (sem barra final, caminho ou parâmetros). Não confundir variável de build com variável de execução do Worker: `scripts/build.mjs` precisa dela ao gerar os arquivos.
4. Fazer novo build e conferir os artefatos: canonical exato para cada rota; `sitemap.xml` e `robots.txt` usando exclusivamente o domínio novo; URLs de imagem/negócio no JSON-LD corretas. Executar `node tools/qa-static.mjs` e `node tools/qa-srcset.mjs` (este último requer ImageMagick).
5. Configurar redirecionamento 301 de `www` para raiz ou raiz para `www` **na zona sob seu controle**, conforme o canônico escolhido. A origem `*.workers.dev` é diferente: regras de redirecionamento da zona do domínio novo **não a controlam**. Para ela, avaliar redirecionamento implementado no Worker ou desativação do subdomínio, depois de testar sem perder acesso administrativo. Não supor que o domínio antigo já redireciona.
6. Publicar primeiro a versão de teste; conferir desktop/celular, botões WhatsApp, menu, galeria, mapa, todas as rotas e página 404. Depois monitorar logs e métricas de erro do Worker; manter identificada a versão anterior para reversão.
7. No Google Search Console, verificar o domínio, enviar o novo sitemap, inspecionar algumas URLs e acompanhar cobertura/indexação. Atualizar a URL do site no Perfil da Empresa no Google e nos demais cadastros, preservando nome, endereço e telefone consistentes.

## Gate editorial e responsabilidade

**Não declarar liberação comercial final** até o laboratório confirmar: inscrição CRO-MG do estabelecimento, nome e CRO do responsável técnico, CEP oficial do endereço e escopo real de recepção de arquivos digitais. Preencher `src/site/data/site.json` somente com informações verificadas. Depoimentos publicados devem corresponder fielmente às avaliações originais, sem inventar texto ou atribuição profissional.

## Regressão e reversão

Em caso de erro crítico pós-publicação: restaurar a versão anterior do Worker pelo mecanismo de versões do Cloudflare, conferir novamente host, certificado e conteúdo de rotas; não reverter DNS indiscriminadamente sem conhecer os registros que foram alterados. A troca de domínio deve ter uma janela de observação e captura de erros 404/5xx.
