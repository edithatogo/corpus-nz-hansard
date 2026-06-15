import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://edithatogo.github.io',
  base: '/corpus-nz-hansard/',
  integrations: [
    mdx(),
    sitemap(),
    starlight({
      title: 'Corpus NZ Hansard',
      description: 'Legal NZ documentation portal for Corpus NZ Hansard.',
      sidebar: [
        { label: 'Start', items: ['index', 'docs-tooling-audit'] },
      ],
    }),
  ],
});
