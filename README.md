# MOTIF Lab — Website

Source for the MOTIF Lab website at the University of South Florida.
**MOTIF** = *Mobility Optimized by Traditional Ideas and Frontier technologies.*

Built with [Hugo](https://gohugo.io). Layouts and styles live at the project root (no external theme — easier to maintain and fully USF-branded). Deploys to GitHub Pages via GitHub Actions on every push to `main`.

---

## Quick start

### 1. Install Hugo (extended)

You need the **extended** build of Hugo, version 0.135 or newer.

- macOS: `brew install hugo`
- Windows: `choco install hugo-extended` or `scoop install hugo-extended`
- Linux: download the latest `hugo_extended_*_linux-amd64.deb` from the [releases page](https://github.com/gohugoio/hugo/releases) and `sudo dpkg -i` it.

Verify: `hugo version` — output should include the word `extended`.

### 2. Clone and run locally

```bash
git clone https://github.com/<your-github-username>/motif-lab.git
cd motif-lab
hugo server -D     # -D includes draft pages
```

Open <http://localhost:1313>. The site live-reloads as you edit files.

### 3. Configure your repo

Open `hugo.toml` and set:

- `baseURL` — for now, `https://<your-github-username>.github.io/motif-lab/` (replace later when you wire up the custom domain).
- The PI / lab info under `[params]` — Google Scholar, ORCID, GitHub, LinkedIn URLs, etc.
- `title`, `description`, `address` if anything is wrong.

### 4. Push to GitHub

Create an empty repo on GitHub named `motif-lab` (or whatever you prefer; just match `baseURL`).

```bash
git init
git add .
git commit -m "Initial MOTIF Lab site"
git branch -M main
git remote add origin https://github.com/<your-github-username>/motif-lab.git
git push -u origin main
```

### 5. Enable GitHub Pages

In the repo on GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions.**

That's it. The included workflow (`.github/workflows/hugo.yml`) will build and deploy automatically on every push to `main`. Within ~1 minute the site is live at `https://<your-github-username>.github.io/motif-lab/`.

---

## Adding content

You can either copy an existing file in `content/` or use Hugo's `new` command, which uses the archetypes in `archetypes/`:

```bash
hugo new team/jane-smith.md          # new lab member
hugo new publications/2026-mixed-traffic-stability.md
hugo new projects/fdot-acc-impacts.md
hugo new news/paper-accepted-trc.md
```

Each new file starts with `draft: true`. Set it to `false` (or remove the line) to publish.

### Lab member entries

Each member is a markdown file in `content/team/`. Frontmatter fields:

```yaml
title: "Jane Smith"
role: "PhD Student"     # PI | Postdoc | PhD Student | MS Student | Undergraduate | Visitor | Alumni
weight: 10              # lower = appears first within the role group
affiliation: "USF Civil and Environmental Engineering"
email: "jane@usf.edu"
photo: "/img/team/jane-smith.jpg"   # put the image in static/img/team/
scholar: "https://scholar.google.com/..."
github: "https://github.com/..."
linkedin: ""
website: ""
interests:
  - "Mixed-traffic flow"
  - "Microsimulation calibration"
education:
  - "M.S., Transportation Engineering, USF, 2025"
```

The `role` is matched case-sensitively against the groups on the team page. Stick to the values in the comment above.

Photos go in `static/img/team/` and are referenced as `/img/team/filename.jpg`. Square crops at ~600×600 look best.

### Publications

Each paper is a markdown file in `content/publications/`. Key fields:

```yaml
title: "Paper title"
year: 2026
authors:
  - "Hao Zhou"
  - "Co-author"
venue: "Transportation Research Part C"
doi: "10.1016/j.trc.2026.xxxxx"
pdf: "/pdf/2026-paper.pdf"          # optional, file goes in static/pdf/
code: "https://github.com/..."
preprint: "https://arxiv.org/..."
slides: ""
abstract: "Short abstract."
```

Papers are auto-grouped by `year` on the publications page.

### Projects, teaching, news

Same pattern — see the sample files in `content/projects/`, `content/teaching/`, and `content/news/` for the available frontmatter fields.

---

## Datasets, showcase pages and numbers (added Oct 2026)

- **Showcase project pages** (`content/projects/<slug>/index.html`, `type: showcase`) are HTML content bundles ported from
  Yuhang's personal site by `tools/port_showcase.py --src /path/to/WangYuHang-cmd.github.io --pages all` (TriDrive, ADAS-TO,
  DriveDNA, DriveMotion, BATON, OpenLKA) and `tools/build_vlalert.py` (VLAlert). Re-run the scripts instead of editing the
  bundles by hand; each run copies only the files the page can reach, rewrites links to `/projects/…`, verifies manifest hashes,
  regenerates `static/SHA256SUMS` and runs the privacy scan. The kit (`static/assets/proj/`) and the deep-green theme
  (`assets/css/showcase-theme.css`) are shared by the five kit pages; OpenLKA keeps its own light stylesheet.
  Hugo ≥ 0.162 denies `text/html` content by default — keep `HUGO_VERSION` pinned or allow it in `[security]`.
- **Datasets & Benchmarks hub** (`/datasets/`): `content/datasets.md` + `layouts/_default/datasets.html`. Descriptive fields
  live in `data/datasets.yaml`; **every number** comes from `data/numbers.json`, generated by
  `tools/build_numbers.py --kit /path/to/WangYuHang-cmd.github.io` from that repo's `tools/projpipe/registry.yaml`
  (the single source of truth, with arXiv / Hugging Face sources). `partials/num.html` renders a number with a provenance chip
  (P paper · R release card · L lab log). Never type numbers into templates.
- **News**: `category` is one of Accepted paper · Preprint · Award · Media · Milestone (`data/news_categories.yaml`);
  `date_precision: month` when only the month is known; `external` (outside links) and `links` (project pages) render as pills.
  `hugo new news/<slug>.md` uses `archetypes/news.md`.
- **Images**: photos live under `assets/img/` and are processed at build time by `partials/img.html` (WebP + JPEG `srcset`).
  New photos go through `tools/normalize_images.py` first (sRGB JPEG, max 2000 px, EXIF/GPS stripped).
- **Checks before pushing** (CI builds on push to `main`):
  `hugo --minify --panicOnWarning --printPathWarnings -d /tmp/public` ·
  `python3 tools/check_public.py /tmp/public --base https://www.motiflab.net/ --strict-personal` ·
  `python3 tools/check_showcase.py` · `python3 tools/privacy_scan.py --paths content layouts static assets data hugo.toml tools
  --exempt content/projects/openlka/static/can --secrets-only content/projects/openlka/static/can.js
  --spans content/projects/openlka/index.html --allow-rx 'pii/S\d{16}' 'https://www\.dropbox\.com/scl/fo/[A-Za-z0-9]+/?' 'Dropbox(?![/\\])'` ·
  `node tools/cdp.mjs <url> 1400x900 --scroll` (console/exception check) · `node tools/measure.mjs <url>` (first view ≤ 3 MB).

## Customizing the look

- **Colors**: edit the CSS variables at the top of `assets/css/main.css`. The defaults are official USF green (`#006747`) and academic deep gold (`#B79F4D`).
- **Navigation**: edit `[menu]` entries in `hugo.toml`.
- **Homepage**: edit `layouts/index.html` to change which sections appear and how many recent items are shown.
- **Footer**: edit `layouts/partials/footer.html`.
- **Header**: edit `layouts/partials/header.html`.

A note on the gold: white text on USF deep gold fails accessibility contrast (~2.6:1). The CSS uses *dark green text on gold* throughout, never white on gold. If you reskin, keep this rule.

---

## Custom domain (e.g., `motif.eng.usf.edu`)

Once you're ready:

1. Coordinate with USF IT to add a CNAME record pointing the subdomain to `<your-github-username>.github.io`.
2. Add a file `static/CNAME` whose only contents are the domain (e.g., `motif.eng.usf.edu`).
3. Update `baseURL` in `hugo.toml` to `https://motif.eng.usf.edu/`.
4. In **Settings → Pages**, fill in the custom domain and check **Enforce HTTPS** once GitHub finishes verifying.

---

## Local development tips

- `hugo server -D` shows drafts; `hugo server` hides them (matches what the deployed site shows).
- `hugo --minify` produces the production build in `public/`. The Action does this for you.
- Add `.draft: true` to a frontmatter to keep something out of the production build while you work.

---

## Project structure

```
.
├── archetypes/             # frontmatter templates for `hugo new`
├── assets/css/main.css     # all site styles (USF green + gold)
├── content/                # all markdown content
│   ├── _index.md           # homepage frontmatter
│   ├── team/
│   ├── research/
│   ├── publications/
│   ├── projects/
│   ├── teaching/
│   ├── news/
│   └── join.md
├── layouts/                # Hugo templates
│   ├── _default/
│   ├── partials/
│   ├── index.html          # homepage
│   ├── team/
│   ├── publications/
│   ├── projects/
│   └── teaching/
├── static/                 # files served as-is (favicon, images, PDFs)
├── .github/workflows/hugo.yml
└── hugo.toml
```
