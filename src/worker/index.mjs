/**
 * Intercepta só o necessário antes dos assets estáticos.
 * O apex devolve a resposta do asset sem alteração, para manter _headers,
 * _redirects, 404 e a barra final. Ver docs/SEGURANCA.md.
 */
import { handleRequest } from './canonical.mjs';

export default {
  async fetch(request, env) {
    return handleRequest(request, env);
  },
};
