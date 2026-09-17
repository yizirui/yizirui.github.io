# Yizirui Fang — research and engineering website

Source for [yiziruifang.com](https://yiziruifang.com/), Yizirui (Easey) Fang's personal website. Built with Hugo 0.136.5 Extended and the pinned [Hugo Blox Academic CV theme](https://github.com/HugoBlox/theme-academic-cv).

## Build and preview

```sh
hugo --environment production --minify --cleanDestinationDir
python3 scripts/check_agent_discovery.py public
```

The first build downloads the pinned Go/Hugo modules. The checker requires Python 3.9+ and no third-party dependencies. It verifies page links, citation metadata, and abstract consistency across HTML, Markdown, and the paper catalog.

Run `hugo server` for a local preview. Run the checker against a production build so it can verify canonical URLs. GitHub Pages builds and checks the site on pushes to `main`.

## Content

- `content/authors/admin/_index.md`: biography, public profiles, experience, and education.
- `content/project/`: project descriptions and related papers, code, and other resources.
- `content/publication/`: paper records, full abstracts, PDF links, and BibTeX citations.
- `content/research.md`: research themes and related papers.

Keep titles, author order, venues, and dates consistent with the linked paper. Preserve abstracts verbatim and identify their source version. Update the abstract and PDF together when changing versions; keep source and license information with each record. The 2024 Learning to Defer workshop paper and the 2026 TMLR article have separate records.

HTML, Markdown, and `papers.json` are generated from the same content. `llms.txt` provides a text index. The site also generates citation metadata, a sitemap, and an RSS feed.

Keep `config/_default/hugo.yaml`, `CNAME`, and the GitHub Pages custom domain aligned. Rebuild with `--cleanDestinationDir` after removing pages. Set `lastmod` when a page's content changes. The academic CV is labeled as an archived snapshot; update it before presenting it as current.
