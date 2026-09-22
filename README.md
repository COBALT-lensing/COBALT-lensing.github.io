# COBALT website

The COBALT consortium's static website, built with Python, Pelican and a custom
black-background theme. Python dependencies are managed by uv and locked in
`uv.lock`. No Ruby or Jekyll installation is needed.

## Local development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
these commands from the repository root:

```sh
uv sync --locked
uv run pelican content -s pelicanconf.py --autoreload --listen
```

Open <http://localhost:8000>. Stop the server with Ctrl-C. The local configuration
uses root-relative links and does not generate feeds. Restart the server after
changing configuration files.

## Production build and checks

```sh
uv run --locked pelican content -s publishconf.py
uv run --locked python scripts/check_site.py
uv run --locked python -m unittest discover -s tests
```

The production build replaces `output/` and uses the public site URL in
`publishconf.py`. The checker verifies the migrated URLs, internal links and
anchors, page headings, image alt attributes, equation markup and Atom feed.
Build locally with `pelicanconf.py` again for a preview whose links stay local.

## Editing content

- `content/pages/`: homepage, project pages and member biographies.
- `content/articles/`: dated news articles.
- `content/assets/images/`: images, published at `/assets/images/`.
- `themes/cobalt/`: Jinja templates, CSS and MathJax configuration.
- `content/legacy/`: original raw biography files, retained at their old `.md`
  URLs for compatibility. Edit the HTML biographies in `content/pages/` instead.

Pages use Pelican metadata above a blank line:

```markdown
Title: About COBALT
URL: about/
Save_as: about/index.html

Page text in Markdown.
```

News articles need a `Title`, `Date: YYYY-MM-DD` and `Slug`. Article URLs keep
the original `/YYYY/MM/DD/slug.html` format. The homepage remains `/`, the news
listing is `/news/`, and the Atom feed remains `/feed.xml`. Preserve the explicit
page URL metadata, including capitalisation, when editing existing pages.

Use Pelican content links such as `[Dr Adam Ingram]({filename}Adam.md)` from
another page in the same directory. Add a biography with `Template: member` and
`Status: hidden`, then link it from `content/pages/bio.md`. Hidden pages are still
published; they simply do not appear in automatic page lists.

For maths, add `Math: true` to the page metadata. Use `$...$` for inline expressions
and `$$` on separate lines around display expressions. The Markdown extension
protects TeX during rendering; MathJax 3.2.2 is loaded from jsDelivr only on maths
pages. Rendering equations requires browser access to that CDN.

The theme uses system fonts and inline SVG artwork, without external font dependencies.
The homepage diagram shows two Keplerian ellipses with a shared barycentric focus
and opposite periapses. Body radii are illustrative, not to scale.
Its colours and responsive layouts are in `themes/cobalt/static/css/site.css`.
The navigation order is defined by `MENUITEMS` in `pelicanconf.py`.

Asset URLs in generated HTML and Atom article content receive a `?v=<hash>`
query parameter, calculated from each file's contents. This covers CSS,
JavaScript, images and other linked files under `theme/` and `assets/`, in both
local and production builds. Changes invalidate that file's browser cache;
unchanged files keep the same URL. Original filenames remain accessible.
External URLs (including the explicitly versioned MathJax CDN URL) are unchanged.
This is handled automatically by `plugins/cache_bust.py`; no manual version bump
is required. The plugin processes `href`, `src` and `poster` HTML attributes.

## GitHub Pages setup

The workflow builds and checks pull requests. Pushes to `master` and manual
runs on `master` additionally deploy the generated artifact to GitHub Pages.

After merging/pushing the migration:

1. Open **Settings → Pages → Build and deployment** and select **GitHub Actions**
   as the source.
2. Ensure repository/organisation Actions policies allow the actions used by
   `.github/workflows/publish.yml`.
3. If the `github-pages` environment has deployment branch restrictions, allow
   `master`. Existing required reviewers still apply.
4. Run the workflow, or push a commit to `master`, and check the deployed site.

The workflow declares the required deployment permissions (`pages: write` and
`id-token: write`); no personal access token, generated-output branch or committed
build directory is needed. Update the workflow branch filters and deployment
conditions if the default branch changes. The existing GitHub Pages address stays
the same. Set any custom domain in Pages settings and update `SITEURL` if needed.

Before publishing, review the homepage and narrow-screen navigation, science
equations, member portraits, news pages and the 404 page in a browser. Some
original biographies are placeholders and some scientific/project updates are
historical; the migration does not update those claims. The science page's
existing missing code URL is now visible as a placeholder instead of an invalid
HTML tag.
