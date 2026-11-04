import test from 'node:test';
import assert from 'node:assert/strict';
import { DEFAULT_SITE_BASE, normalizeSiteBase, resolveSiteBase } from '../scripts/site-base.mjs';

test('aceita domínio HTTPS na raiz e normaliza a barra final', () => {
  assert.equal(normalizeSiteBase('https://exemplo.com.br/'), 'https://exemplo.com.br');
  assert.equal(resolveSiteBase({ SITE_BASE: ' https://www.exemplo.com.br/ ' }), 'https://www.exemplo.com.br');
});

test('SITE_BASE explícito prevalece sobre o domínio automático de Pages', () => {
  assert.equal(resolveSiteBase({ SITE_BASE: 'https://exemplo.com.br', CF_PAGES_URL: 'https://teste.pages.dev' }), 'https://exemplo.com.br');
  assert.equal(resolveSiteBase({ CF_PAGES_URL: 'https://teste.pages.dev' }), 'https://teste.pages.dev');
});

test('usa como fallback o domínio existente em vez de gerar SEO relativo', () => {
  assert.equal(resolveSiteBase({ WORKERS_CI: '1' }), DEFAULT_SITE_BASE);
});

test('rejeita origens inseguras, URLs relativas e subdiretórios', () => {
  for (const value of ['', 'http://exemplo.com.br', 'https://exemplo.com.br/blog/',
    'https://exemplo.com.br:8443', 'https://exemplo.com.br/?preview=1',
    'https://usuario:senha@exemplo.com.br', 'https://exemplo.com.br/#x']) {
    assert.throws(() => normalizeSiteBase(value), /SITE_BASE/);
  }
  assert.throws(() => resolveSiteBase({ SITE_BASE: 'https://exemplo.com.br/blog/' }), /SITE_BASE/);
});
