# Fonte estática do site

Este diretório é a fonte publicada do site estático. O build Node combina o
shell comum em `layout/` com cada rota em `pages/` e copia os arquivos técnicos
de `files/` para `dist/`.

Não há servidor de aplicação, banco de dados, API ou backend. A Cloudflare
recebe apenas os arquivos resultantes do build.
