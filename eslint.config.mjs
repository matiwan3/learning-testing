import globals from "globals";
import pluginJs from "@eslint/js";
import stylisticJs from '@stylistic/eslint-plugin-js';

export default {
  plugins: {
    '@stylistic/js': stylisticJs
  },
  rules: {
    '@stylistic/js/indent': ['error', 2],
    // ...
  },
  languageOptions: {
    globals: globals.browser
  },
  extends: [
    pluginJs.configs.recommended
  ]
};
