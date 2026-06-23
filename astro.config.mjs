import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';

export default defineConfig({
  site: 'https://example.com',
  outDir: 'docs',
  integrations: [vue()],
});
