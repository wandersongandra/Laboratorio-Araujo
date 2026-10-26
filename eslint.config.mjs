// ESLint (flat config) — JavaScript do site: navegador, ES2022, script clássico (não módulo).
import js from '@eslint/js';
import globals from 'globals';

export default [
  { ignores: ['dist/**', 'node_modules/**'] },
  js.configs.recommended,
  {
    files: ['_build/static/assets/js/**/*.js'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'script', globals: { ...globals.browser } },
    rules: {
      'no-unused-vars': ['error', { args: 'none' }],
      'no-implied-eval': 'error',
      'no-eval': 'error',
      'no-new-func': 'error',
      'no-restricted-properties': ['error',
        { property: 'innerHTML', message: 'Use textContent/replaceChildren (ver docs/SEGURANCA.md).' },
        { property: 'outerHTML', message: 'Use DOM nodes.' },
        { object: 'document', property: 'write', message: 'Proibido.' }],
      eqeqeq: ['error', 'smart'],
      'prefer-const': 'error',
    },
  },
  {
    files: ['tools/**/*.mjs', 'eslint.config.mjs'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'module', globals: { ...globals.node } },
  },
];
