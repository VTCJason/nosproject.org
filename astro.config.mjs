// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://nosproject.org',
  integrations: [
    mdx(),
    sitemap({
      customPages: [
        'https://nosproject.org/human-question/technical-demystification/',
        'https://nosproject.org/human-question/economics-labor-industry/',
        'https://nosproject.org/human-question/geopolitics-national-security/',
        'https://nosproject.org/human-question/ethics-society-human-impact/',
        'https://nosproject.org/human-question/existential-frontier/',
        'https://nosproject.org/human-question/regulatory-legal-governance/',
        'https://nosproject.org/human-question/safety-security-information-integrity/',
        'https://nosproject.org/human-question/infrastructure-environment/',
        'https://nosproject.org/human-question/science-knowledge-domains/',
        'https://nosproject.org/human-question/faith-identity-human-condition/',
      ],
    }),
  ],
});
