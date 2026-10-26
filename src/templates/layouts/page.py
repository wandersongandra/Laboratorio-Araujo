"""Layout comum: header, footer e page.

A implementação permanece em `scripts.build.site` para preservar a saída HTML.
Novos layouts devem entrar neste pacote e ser importados pelo build.
"""

from scripts.build.site import footer, header, page

__all__ = ["header", "footer", "page"]
