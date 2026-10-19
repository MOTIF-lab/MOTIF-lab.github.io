#!/usr/bin/env python3
"""port_showcase.py --src /path/to/WangYuHang-cmd.github.io [--pages all|tridrive adasto …] [--dry-run] [--report out.json]

Ports the five kit project pages from the personal Jekyll site into Hugo leaf bundles:
  content/projects/<lab-slug>/index.html   front matter (stub fields merged textually + generated head fields) + the source <body> inner HTML
  content/projects/<lab-slug>/static/…     only the files the page can reach (manifest files ∪ body refs ∪ og image ∪ preloads)
Rewrites links to the lab's URL space, regenerates the More-works menu from one table, swaps brand/author/footer to MOTIF Lab,
verifies manifest hashes, writes SHA256SUMS, runs the FORBIDDEN scan, deletes the stub .md and prints a report. Exit 1 on any failure."""
import argparse, html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from showcase_lib import SLUG, KIT_PAGES, SUMS_NAME, SECRETS_ONLY, scan_forbidden, sha256_file, write_sums, is_text

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ["openlka", "adasto", "tridrive", "drivedna", "drivemotion", "baton", "vlalert"]
DD_EXTRA = ('<a href="/datasets/"><b>All datasets &amp; benchmarks</b><span>MOTIF Lab releases · access tiers · citations</span></a>')
BRAND_OLD = '<a class="pj-brand" href="/">Yuhang <b>Wang</b></a>'
BRAND_NEW = ('<a class="pj-brand" href="/" aria-label="MOTIF Lab home"><img src="/img/logo/motif-lockup-white-h-640.png" '
             'alt="MOTIF Lab · University of South Florida" width="640" height="160"></a>')
EXTRA_OLD = '<li class="pj-site-extra"><a href="/">Home</a></li><li class="pj-site-extra"><a href="/projects/">Projects</a></li>'
EXTRA_NEW = ('<li class="pj-site-extra"><a href="/">Home</a></li><li class="pj-site-extra"><a href="/datasets/">Datasets</a></li>'
             '<li class="pj-site-extra"><a href="/projects/">Projects</a></li>')
FOOT_NEW = ('<footer class="pj-foot"><div class="pj-wrap"><b>MOTIF Lab</b> · University of South Florida · Civil &amp; Environmental Engineering · CUTR'
            '<div class="pj-foot__links"><a href="/">Home</a><a href="/datasets/">Datasets &amp; Benchmarks</a><a href="/projects/">Projects</a>'
            '<a href="/publications/">Publications</a><a href="/news/">News</a></div></div></footer>')
ALLOWED_LOCAL = re.compile(r"^/$|^/(projects/([\w-]+/)?(#[\w-]+)?|datasets/|publications/|news/|team/[\w-]+/|img/[\w./-]+|assets/proj/[\w./-]+)$")
REF_RX = re.compile(r'(?:src|href|poster|data-src|data-video|data-poster|data-zoom)="(static/[^"#?]+)')

class Fail(Exception): pass

def sub(s, old, new, n, regex=False, label=""):
    cnt = len(re.findall(old, s, flags=re.S)) if regex else s.count(old)
    if cnt != n: raise Fail(f"{label or old[:40]!r}: expected {n} match(es), found {cnt}")
    return re.sub(old, new, s, flags=re.S) if regex else s.replace(old, new)

def meta(head, attr, key, default=None):
    m = re.search(rf'<meta {attr}="{re.escape(key)}" content="([^"]*)"', head)
    return html.unescape(m.group(1)) if m else default

def more_table(src):
    """Union of the More-works entries across the five source pages → {personal_slug: (name, blurb)}."""
    out = {}
    for p in KIT_PAGES:
        s = open(os.path.join(src, p, "index.html"), encoding="utf8").read()
        for m in re.finditer(r'<a href="/(\w+)/"><b>([^<]+)</b><span>([^<]+)</span></a>', s):
            out.setdefault(m.group(1), (m.group(2), m.group(3)))
    missing = [k for k in ORDER if k not in out]
    if missing: raise Fail(f"More-works table incomplete: {missing}")
    return out

def stub_frontmatter(lab_slug):
    p = os.path.join(LAB, "content", "projects", f"{lab_slug}.md")
    if not os.path.exists(p): return "", None
    s = open(p, encoding="utf8").read()
    m = re.match(r"---\n(.*?)\n---\n", s, flags=re.S)
    if not m: raise Fail(f"{p}: no front matter")
    lines = [l for l in m.group(1).split("\n") if "Project page:" not in l]   # drop the link to the personal page
    return "\n".join(lines), p

def jdump(v): return json.dumps(v, ensure_ascii=False, separators=(", ", ": "))

def port_kit(src, pslug, more, dry):
    lab = SLUG[pslug]; sdir = os.path.join(src, pslug); s = open(os.path.join(sdir, "index.html"), encoding="utf8").read()
    head = s[s.index("<head>") + 6:s.index("</head>")]
    body = s[s.index("<body"):]; body = body[body.index(">") + 1:body.rindex("</body>")].strip("\n")
    rep = {"page": pslug, "lab_slug": lab, "rewrites": {}}
    # ---- front matter fields from the source head
    title = html.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    fm = {"type": "showcase", "kit": True, "proj": pslug, "showcase_title": title,
          "meta_description": meta(head, "name", "description"), "keywords": meta(head, "name", "keywords"),
          "authors": [a.strip() for a in (meta(head, "name", "author") or "").split(",") if a.strip()], "theme_color": "#03150f",
          "og": {"title": meta(head, "property", "og:title"), "description": meta(head, "property", "og:description")},
          "twitter": {"title": meta(head, "name", "twitter:title"), "description": meta(head, "name", "twitter:description")}}
    ogimg = meta(head, "property", "og:image") or ""
    m = re.match(rf"https://wangyuhang-cmd\.github\.io/{pslug}/(static/.+)$", ogimg)
    if not m: raise Fail(f"og:image not under the page: {ogimg}")
    fm["image"] = m.group(1)
    fm["preload"] = re.findall(r'<link rel="preload" href="(static/[^"]+)" as="image"', head)
    cit = {"title": meta(head, "name", "citation_title"), "authors": re.findall(r'<meta name="citation_author" content="([^"]*)"', head),
           "date": meta(head, "name", "citation_publication_date"), "arxiv": meta(head, "name", "citation_arxiv_id"),
           "conference": meta(head, "name", "citation_conference_title")}
    fm["citation"] = {k: v for k, v in cit.items() if v}
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    if ld:
        d = json.loads(ld.group(1)); sc = {"type": d.get("@type", "Dataset"), "name": d.get("headline") or d.get("name"),
                                           "description": d.get("description")}
        for k in ("datePublished", "sameAs", "keywords", "citation", "isAccessibleForFree"):
            if k in d: sc[k] = d[k]
        lic = d.get("license")
        if isinstance(lic, str):
            sc["license"] = re.sub(rf"^https://wangyuhang-cmd\.github\.io/{pslug}/", "", lic) if lic.startswith("https://wangyuhang-cmd") else lic
            if sc["license"].startswith("#") is False and not sc["license"].startswith("http"): sc["license"] = "#" + sc["license"].lstrip("#")
        if "distribution" in d:
            sc["distribution"] = [{k: v for k, v in x.items() if k != "@type"} for x in d["distribution"]]
        fm["schema"] = {k: v for k, v in sc.items() if v is not None}
    # ---- body rewrites
    sib = re.compile(r'href="/(tridrive|adasto|drivedna|drivemotion|baton|openlka|vlalert)/(#[\w-]*)?"')
    n = len(sib.findall(body)); body = sib.sub(lambda m: f'href="/projects/{SLUG[m.group(1)]}/{m.group(2) or ""}"', body); rep["rewrites"]["sibling_links"] = n
    th = re.compile(r'src="/images/th_(\w+)\.jpg"'); n = len(th.findall(body))
    body = th.sub(lambda m: f'src="/img/projects/th_{SLUG[m.group(1)]}.jpg"', body); rep["rewrites"]["thumbnails"] = n
    body = sub(body, BRAND_OLD, BRAND_NEW, 1, label="brand")
    body = sub(body, '<a href="/">Yuhang Wang</a>', '<a href="/team/yuhang-wang/">Yuhang Wang</a>', 1, label="author link")
    body = sub(body, EXTRA_OLD, EXTRA_NEW, 1, label="site-extra")
    menu = "".join(f'<a href="/projects/{SLUG[k]}/"><b>{more[k][0]}</b><span>{more[k][1]}</span></a>' for k in ORDER if k != pslug) + DD_EXTRA
    body = sub(body, r'<div class="pj-dd__menu">.*?</div>', f'<div class="pj-dd__menu">{menu}</div>', 1, regex=True, label="more-works")
    body = sub(body, r'<footer class="pj-foot">.*?</footer>', FOOT_NEW, 1, regex=True, label="footer")
    n = body.count("https://wangyuhang-cmd.github.io/"); rep["rewrites"]["personal_domain"] = n
    body = re.sub(r"https://wangyuhang-cmd\.github\.io/(tridrive|adasto|drivedna|drivemotion|baton|openlka|vlalert)/", lambda m: f"/projects/{SLUG[m.group(1)]}/", body)
    body = body.replace("https://wangyuhang-cmd.github.io/", "/team/yuhang-wang/")
    bad = [u for u in re.findall(r'(?:href|src)="(/[^"]*)"', body) if not ALLOWED_LOCAL.match(u)]
    if bad: raise Fail(f"unexpected root-relative refs left: {sorted(set(bad))[:10]}")
    if re.search(r"\{\{[<%]|[%>]\}\}", body): raise Fail("shortcode delimiters in body")
    # ---- copy set
    man_p = os.path.join(sdir, "static", "data", "manifest.json"); man = json.load(open(man_p, encoding="utf8"))
    want = {v["path"] for v in man["files"].values()} | {"static/data/manifest.json", fm["image"]} | set(fm["preload"]) | set(REF_RX.findall(body))
    for it in man.get("items", []):
        for v in (it.get("files") or {}).values(): want.add(v)
    want = {w for w in want if w.startswith("static/")}
    bad_rev = [it["id"] for it in man.get("items", []) if (it.get("privacy") or {}).get("manual_review") != "ok"]
    if bad_rev: raise Fail(f"manifest items not reviewed ok: {bad_rev}")
    for v in man["files"].values():
        p = os.path.join(sdir, v["path"])
        if not os.path.exists(p): raise Fail(f"manifest path missing: {v['path']}")
        if sha256_file(p) != v["sha256"] or os.path.getsize(p) != v["bytes"]: raise Fail(f"manifest hash/bytes mismatch: {v['path']}")
    missing = [w for w in want if not os.path.exists(os.path.join(sdir, w))]
    if missing: raise Fail(f"referenced files missing in source: {missing}")
    # ---- front matter text
    stub_txt, stub_path = stub_frontmatter(lab)
    gen = [f"{k}: {jdump(v)}" for k, v in fm.items()]
    summary = None
    if stub_txt:
        m = re.search(r'(?m)^description:\s*"(.*)"\s*$', stub_txt)
        if m: summary = m.group(1)
    if summary is None: summary = fm["meta_description"]
    gen.insert(0, f"summary: {jdump(summary)}")
    front = "---\n" + (stub_txt + "\n" if stub_txt else f"title: {jdump(title)}\ndescription: {jdump(fm['meta_description'])}\n") + \
            "# ---- generated by tools/port_showcase.py (showcase port); the stub fields above are the lab's own ----\n" + "\n".join(gen) + "\n---\n"
    out_dir = os.path.join(LAB, "content", "projects", lab); index_out = front + body + "\n"
    hits = scan_forbidden(index_out)
    if hits: raise Fail(f"FORBIDDEN in index.html: {hits[:5]}")
    rep.update(files=len(want), bytes=sum(os.path.getsize(os.path.join(sdir, w)) for w in want), stub_removed=bool(stub_path))
    if dry: return rep
    if os.path.isdir(os.path.join(out_dir, "static")): shutil.rmtree(os.path.join(out_dir, "static"))
    os.makedirs(out_dir, exist_ok=True)
    for w in sorted(want):
        dst = os.path.join(out_dir, w); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(os.path.join(sdir, w), dst)
        if is_text(dst):
            h = scan_forbidden(open(dst, encoding="utf8", errors="replace").read())
            if h: raise Fail(f"FORBIDDEN in {w}: {h[:5]}")
    rep["sums_entries"] = write_sums(os.path.join(out_dir, "static"))
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf8").write(index_out)
    if stub_path: os.remove(stub_path)
    return rep

LK_BRAND_OLD = '<a class="lk-brand" href="/">Yuhang <b>Wang</b></a>'
LK_BRAND_NEW = ('<a class="lk-brand" href="/" aria-label="MOTIF Lab home"><img src="/img/logo/motif-lockup-green-h-640.png" '
                'alt="MOTIF Lab · University of South Florida" width="640" height="160"></a>')
LK_ALLOW_RX = [r"https://www\.dropbox\.com/scl/fo/[A-Za-z0-9]+/?", r"Dropbox(?![/\\])"]   # public release host, prose mentions

def tune_openlka_css(text):
    """Lab copy only: the dark CAN band of OpenLKA's own stylesheet moves from navy to the lab's deep greens (same tokens as showcase-theme.css)."""
    reps = [("--cl-bg:#070d1d;--cl-bg-1:#0a1428;--cl-bg-2:#0f2044;", "--cl-bg:#03150f;--cl-bg-1:#06231a;--cl-bg-2:#082c20;"),
            ("rgba(7,13,29,", "rgba(3,21,15,"), ("rgba(61,123,255,", "rgba(46,125,92,"), ("#0b1730", "#0a2d21"), ("#0e1c3c", "#0f3a2c"), ("#0a1428", "#06231a")]
    for a, b in reps:
        if a not in text: raise Fail(f"can.css tune: {a!r} not found (source changed?)")
        text = text.replace(a, b)
    text = re.sub(r"--cl-border:rgba\([^)]*\)", "--cl-border:rgba(207,196,147,.2)", text, count=1)
    text = re.sub(r"--cl-border-hi:rgba\([^)]*\)", "--cl-border-hi:rgba(207,196,147,.55)", text, count=1)
    return text

def port_openlka(src, more, dry):
    """OpenLKA keeps its own light USF-coloured CSS/JS; only the chrome and the links move to the lab."""
    pslug, lab = "openlka", "openlka"; sdir = os.path.join(src, pslug); s = open(os.path.join(sdir, "index.html"), encoding="utf8").read()
    head = s[s.index("<head>") + 6:s.index("</head>")]
    body = s[s.index("<body"):]; body = body[body.index(">") + 1:body.rindex("</body>")].strip("\n")
    rep = {"page": pslug, "lab_slug": lab, "rewrites": {}}
    title = html.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    fm = {"type": "showcase", "kit": False, "proj": pslug, "css": ["static/openlka.css", "static/can.css"], "showcase_title": title,
          "meta_description": meta(head, "name", "description"), "keywords": meta(head, "name", "keywords"),
          "authors": [a.strip() for a in (meta(head, "name", "author") or "").split(",") if a.strip()], "theme_color": "#ffffff",
          "og": {"title": meta(head, "property", "og:title"), "description": meta(head, "property", "og:description")},
          "twitter": {"title": meta(head, "name", "twitter:title"), "description": meta(head, "name", "twitter:description")},
          "image": "static/images/olka_og.jpg", "preload": []}
    cit = {"title": meta(head, "name", "citation_title"), "authors": re.findall(r'<meta name="citation_author" content="([^"]*)"', head),
           "date": meta(head, "name", "citation_publication_date"), "arxiv": meta(head, "name", "citation_arxiv_id"),
           "conference": meta(head, "name", "citation_conference_title")}
    fm["citation"] = {k: v for k, v in cit.items() if v}
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S); d = json.loads(ld.group(1))
    fm["schema"] = {"type": "Dataset", "name": d.get("name"), "description": d.get("description"), "license": "#access-terms",
                    "citation": d.get("citation"), "keywords": d.get("keywords"),
                    "distribution": [{k: v for k, v in x.items() if k != "@type"} for x in d.get("distribution", [])]}
    # ---- body rewrites
    sib = re.compile(r'href="/(tridrive|adasto|drivedna|drivemotion|baton|openlka|vlalert)/(#[\w-]*)?"')
    n = len(sib.findall(body)); body = sib.sub(lambda m: f'href="/projects/{SLUG[m.group(1)]}/{m.group(2) or ""}"', body); rep["rewrites"]["sibling_links"] = n
    th = re.compile(r'src="/images/th_(\w+)\.jpg"'); n = len(th.findall(body))
    body = th.sub(lambda m: f'src="/img/projects/th_{SLUG[m.group(1)]}.jpg"', body); rep["rewrites"]["thumbnails"] = n
    body = sub(body, LK_BRAND_OLD, LK_BRAND_NEW, 1, label="brand")
    menu = "".join(f'<li><a href="/projects/{SLUG[k]}/"><b>{more[k][0]}</b><span>{more[k][1]}</span></a></li>' for k in ORDER if k != pslug) + \
           '<li>' + DD_EXTRA + '</li>'
    body = sub(body, r'<ul class="lk-dd__menu" id="lk-more-menu">.*?</ul>', f'<ul class="lk-dd__menu" id="lk-more-menu">{menu}</ul>', 1, regex=True, label="more-works")
    body = sub(body, r'\s*<li class="lk-site-extra"><a href="/">About</a></li>(\s*<li class="lk-site-extra"><a href="/(?:awards|blogs|teams|hobbies)/">[^<]+</a></li>)+\s*<li><a class="lk-cv" href="/file/CV-Yuhang.pdf">CV</a></li>',
               '\n        <li class="lk-site-extra"><a href="/">Home</a></li>', 1, regex=True, label="personal nav items")
    body = sub(body, '<li><a href="/projects/">Projects</a></li>', '<li><a href="/datasets/">Datasets</a></li>\n        <li><a href="/projects/">Projects</a></li>', 1, label="site list")
    body = sub(body, '<a href="/">Home</a> · <a href="/projects/">Projects</a>', '<a href="/">Home</a> · <a href="/datasets/">Datasets &amp; Benchmarks</a> · <a href="/projects/">Projects</a>', 1, label="footer links")
    n = body.count("https://wangyuhang-cmd.github.io/"); rep["rewrites"]["personal_domain"] = n
    body = re.sub(r"https://wangyuhang-cmd\.github\.io/(tridrive|adasto|drivedna|drivemotion|baton|openlka|vlalert)/", lambda m: f"/projects/{SLUG[m.group(1)]}/", body)
    body = body.replace("https://wangyuhang-cmd.github.io/", "/team/yuhang-wang/")
    bad = [u for u in re.findall(r'(?:href|src)="(/[^"]*)"', body) if not ALLOWED_LOCAL.match(u)]
    if bad: raise Fail(f"unexpected root-relative refs left: {sorted(set(bad))[:10]}")
    if re.search(r"\{\{[<%]|[%>]\}\}", body): raise Fail("shortcode delimiters in body")
    # ---- copy set: direct refs ∪ all clips ∪ before/after scene images ∪ CAN index + everything it references ∪ og image
    want = set(REF_RX.findall(body)) | {fm["image"], "static/can/index.json"} | set(fm["css"])   # the stylesheets were in the source <head>
    want |= {"static/clips/" + f for f in os.listdir(os.path.join(sdir, "static", "clips"))}
    want |= {"static/images/" + f for f in os.listdir(os.path.join(sdir, "static", "images")) if f.startswith("olka_ba_")}
    idx = json.load(open(os.path.join(sdir, "static", "can", "index.json"), encoding="utf8"))
    want |= {"static/can/" + p for p in set(re.findall(r'"([^"]+\.(?:json|jpg|mp4|png|csv|bin|txt))"', json.dumps(idx)))}
    want = {w for w in want if w.startswith("static/") and not w.endswith("favicon.ico")}
    missing = [w for w in want if not os.path.exists(os.path.join(sdir, w))]
    if missing: raise Fail(f"referenced files missing in source: {sorted(missing)[:8]}")
    stub_txt, stub_path = stub_frontmatter(lab)
    summary = None
    if stub_txt:
        m = re.search(r'(?m)^description:\s*"(.*)"\s*$', stub_txt)
        if m: summary = m.group(1)
    gen = [f"summary: {jdump(summary or fm['meta_description'])}"] + [f"{k}: {jdump(v)}" for k, v in fm.items()]
    front = "---\n" + (stub_txt + "\n" if stub_txt else f"title: {jdump(title)}\ndescription: {jdump(fm['meta_description'])}\n") + \
            "# ---- generated by tools/port_showcase.py (showcase port); the stub fields above are the lab's own ----\n" + "\n".join(gen) + "\n---\n"
    index_out = front + body + "\n"
    strip = re.sub(r'<span class="rec__id mono">[^<]*</span>', "", re.sub(r'\sdata-dongle="[0-9a-f]{16}"', "", index_out))  # the lab's own recorder ids are shown by decision
    hits = scan_forbidden(strip, allow_rx=LK_ALLOW_RX)
    if hits: raise Fail(f"FORBIDDEN in index.html: {hits[:5]}")
    rep.update(files=len(want), bytes=sum(os.path.getsize(os.path.join(sdir, w)) for w in want), stub_removed=bool(stub_path))
    if dry: return rep
    out_dir = os.path.join(LAB, "content", "projects", lab)
    if os.path.isdir(os.path.join(out_dir, "static")): shutil.rmtree(os.path.join(out_dir, "static"))
    os.makedirs(out_dir, exist_ok=True)
    for w in sorted(want):
        dst = os.path.join(out_dir, w); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(os.path.join(sdir, w), dst)
        if w == "static/can.css":
            tuned = tune_openlka_css(open(dst, encoding="utf8").read())   # read first: open(dst, "w") truncates
            open(dst, "w", encoding="utf8").write(tuned); rep["rewrites"]["can_css_tuned"] = True
        if is_text(dst):
            txt = open(dst, encoding="utf8", errors="replace").read()
            rules = SECRETS_ONLY if (w.startswith("static/can/") or w == "static/can.js") else None   # recorder/route ids are public by decision
            h = scan_forbidden(txt, rules=rules, allow_rx=LK_ALLOW_RX)
            if h: raise Fail(f"FORBIDDEN in {w}: {h[:5]}")
    rep["sums_entries"] = write_sums(os.path.join(out_dir, "static"))
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf8").write(index_out)
    if stub_path: os.remove(stub_path)
    return rep

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); ap.add_argument("--pages", nargs="*", default=["all"])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--report")
    a = ap.parse_args(); pages = KIT_PAGES + ["openlka"] if a.pages == ["all"] else a.pages
    more = more_table(a.src); reports = []; ok = True
    for p in pages:
        if p not in KIT_PAGES and p != "openlka": print(f"{p}: not portable by script (VLAlert is hand-built on the kit)"); ok = False; continue
        try:
            r = port_openlka(a.src, more, a.dry_run) if p == "openlka" else port_kit(a.src, p, more, a.dry_run); reports.append(r)
            print(f"{p} → /projects/{r['lab_slug']}/ · {r['files']} files · {r['bytes']/1e6:.1f} MB · rewrites {r['rewrites']}" + (" (dry run)" if a.dry_run else f" · SUMS {r['sums_entries']}"))
        except Fail as e: print(f"{p}: FAIL — {e}"); ok = False
    if a.report: json.dump(reports, open(a.report, "w"), indent=1)
    sys.exit(0 if ok else 1)

if __name__ == "__main__": main()
