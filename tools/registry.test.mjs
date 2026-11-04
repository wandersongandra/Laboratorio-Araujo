import test from 'node:test';
import assert from 'node:assert/strict';
import { injectRegistryJsonLd, registryFromSite, registryMarkup } from '../scripts/registry.mjs';

test('registros ausentes não geram identidade fictícia', () => {
  const registry = registryFromSite({});
  assert.deepEqual(registryMarkup(registry), { footer: '', facts: '' });
  assert.equal(injectRegistryJsonLd('<p>Original</p>', registry), '<p>Original</p>');
});

test('não aceita inscrição profissional sem nome, nem nome sem CRO', () => {
  assert.throws(() => registryFromSite({ technicalLeadName: 'Nome' }), /juntos/);
  assert.throws(() => registryFromSite({ technicalLeadCro: 'CRO-MG 123' }), /juntos/);
});

test('escapa conteúdo cadastral e preserva JSON-LD válido', () => {
  const registry = registryFromSite({
    laboratoryCro: 'LB 123', technicalLeadName: 'Teste <script>', technicalLeadCro: 'CRO-MG 123',
  });
  const parts = registryMarkup(registry);
  assert.match(parts.footer, /Teste &lt;script&gt;/);
  assert.doesNotMatch(parts.footer, /Teste <script>/);
  assert.match(parts.facts, /LB 123/);
  const html = '<script type="application/ld+json">' + JSON.stringify({
    '@context': 'https://schema.org', '@graph': [
      { '@type': 'LocalBusiness', '@id': 'https://exemplo.com/#laboratorio' },
      { '@type': 'WebPage', '@id': 'https://exemplo.com/#webpage' },
    ],
  }) + '</script>';
  const output = injectRegistryJsonLd(html, registry);
  assert.doesNotMatch(output, /Teste <script>/);
  const graph = JSON.parse(output.match(/<script type="application\/ld\+json">(.*?)<\/script>/)?.[1])['@graph'];
  assert.equal(graph[0].employee.name, 'Teste <script>');
  assert.equal(graph[0].identifier.value, 'LB 123');
  assert.equal(graph[1]['@type'], 'WebPage');
});
