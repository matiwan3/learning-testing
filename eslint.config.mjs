// Installation:
// npm install --save-dev eslint @eslint/js
// npm i -D @stylistic/eslint-plugin-js
// npm install @stylistic/eslint-plugin-js
// restart the extension
import stylisticJs from '@stylistic/eslint-plugin-js';

export default {
  plugins: {
    '@stylistic/js': stylisticJs,
  },
  rules: {
    indent: ['warn', 2],
    quotes: ['warn', 'single'],
    semi: ['warn', 'always'],
    'arrow-parens': ['warn'],
    'object-curly-spacing': ['warn', 'always'],
    'no-trailing-spaces': ['warn'],
    'comma-dangle': [
      'warn',
      {
        arrays: 'always-multiline',
        objects: 'always-multiline',
        imports: 'always-multiline',
        exports: 'always-multiline',
        functions: 'always-multiline',
      },
    ],
    'space-before-blocks': ['warn'],
    'eol-last': ['warn'],
    'space-infix-ops': ['warn'],
    'padding-line-between-statements': [
      'warn',
      { blankLine: 'always', prev: ['const', 'let', 'var'], next: '*' },
      { blankLine: 'always', prev: 'import', next: '*' },
      { blankLine: 'never', prev: 'import', next: 'import' },
      {
        blankLine: 'any',
        prev: ['const', 'let', 'var'],
        next: ['const', 'let', 'var'],
      },
      { blankLine: 'always', prev: '*', next: 'return' },
    ],
    'no-multiple-empty-lines': ['warn', { max: 1 }],
    'no-multi-spaces': ['warn'],
    'prefer-template': ['warn'],
    '@typescript-eslint/no-extra-semi': 0,
    '@typescript-eslint/no-non-null-assertion': 0,
    '@typescript-eslint/interface-name-prefix': 0,
  },
};
