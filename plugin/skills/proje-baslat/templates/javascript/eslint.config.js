import js from '@eslint/js';

export default [
  { ignores: ['coverage/**', 'dist/**'] },
  js.configs.recommended,
  {
    languageOptions: { globals: { console: 'readonly' } },
    rules: {
      indent: ['error', 2],
      quotes: ['error', 'single'],
      semi: ['error', 'always'],
    },
  },
];
