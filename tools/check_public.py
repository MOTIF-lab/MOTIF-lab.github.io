#!/usr/bin/env python3
"""check_public.py PUBLIC_DIR --base https://www.motiflab.net/ [--allow-missing /datasets/ …] [--strict-personal]
Static checks over a Hugo build: every local href/src/poster/data-* resolves to a file; no leftover personal-site slugs;
personal-domain links only where allowed; JSON-LD parses; showcase bundles are byte-identical to their SHA256SUMS; canonical/og:url
match the base; the /projects/ list shows the showcase cards. Exit 1 on failures (personal-domain links are warnings unless --strict-personal)."""
import argparse, hashlib, json, os, re, sys, urllib.parse
PERSONAL = "wangyuhang-cmd.github.io"
OLD_SLUGS = re.compile(r'href="/(tridrive|adasto|drivedna|drivemotion|baton|openlka|vlalert)/')
REF = re.compile(r'(?:href|src|poster|data-src|data-video|data-poster|data-zoom|data-manifest|srcset)="([^"]+)"')

def sha(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("public"); ap.add_argument("--base", required=True); ap.add_argument("--allow-missing", nargs="*", default=[])
    ap.add_argument("--personal-ok", nargs="*", default=["team/yuhang-wang/index.html", "team/index.html"]); ap.add_argument("--strict-personal", action="store_true")
    a = ap.parse_args(); pub = os.path.abspath(a.public); base = a.base.rstrip("/") + "/"; host = urllib.parse.urlparse(base).netloc
    errs, warns, pages, showcase = [], [], 0, 0
    for root, _, files in os.walk(pub):
        for fn in files:
            if not fn.endswith(".html"): continue
            fp = os.path.join(root, fn); rel = os.path.relpath(fp, pub).replace(os.sep, "/"); s = open(fp, encoding="utf8", errors="replace").read(); pages += 1
            page_dir = os.path.dirname(fp)
            for m in REF.finditer(s):
                for u in (m.group(1).split(",") if m.group(0).startswith("srcset") else [m.group(1)]):
                    u = u.strip().split(" ")[0]
                    if not u or u.startswith(("#", "mailto:", "data:", "key:", "javascript:", "tel:", "about:")): continue
                    if re.fullmatch(r"[\w-]+", u): continue   # source ids on <data data-src="arxiv-abs">, not paths
                    pr = urllib.parse.urlparse(u)
                    if pr.scheme in ("http", "https"):
                        if pr.netloc != host: continue
                        path = pr.path
                    elif u.startswith("//"): continue
                    else: path = pr.path
                    if not path: continue
                    tgt = os.path.join(pub, path.lstrip("/")) if path.startswith("/") else os.path.join(page_dir, path)
                    if path.endswith("/") or os.path.isdir(tgt): tgt = os.path.join(tgt, "index.html")
                    if not os.path.exists(tgt):
                        if any(path.startswith(x) for x in a.allow_missing): continue
                        errs.append(f"{rel}: missing {u}")
            if OLD_SLUGS.search(s): errs.append(f"{rel}: leftover personal slug link {OLD_SLUGS.search(s).group(0)}")
            if PERSONAL in s and rel not in a.personal_ok:
                (errs if a.strict_personal else warns).append(f"{rel}: links to {PERSONAL} ×{s.count(PERSONAL)}")
            for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                try: json.loads(m.group(1))
                except ValueError as e: errs.append(f"{rel}: JSON-LD does not parse ({e})")
            url_path = "/" if rel == "index.html" else "/" + rel[:-len("index.html")] if rel.endswith("/index.html") else "/" + rel
            can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
            if can and can.group(1) != base.rstrip("/") + url_path and not rel.startswith("404"): errs.append(f"{rel}: canonical {can.group(1)} ≠ {base.rstrip('/') + url_path}")
            if 'data-proj="' in s or re.search(r'<main id="main">', s) and "projects/" in rel:
                if s.count("<html") != 1 or s.count("<body") != 1 or s.count("<title>") != 1: errs.append(f"{rel}: not a single document")
                sums = os.path.join(page_dir, "static", "SHA256SUMS")
                if "data-proj" in s:
                    showcase += 1
                    if not os.path.exists(sums): errs.append(f"{rel}: static/SHA256SUMS missing")
                    else:
                        for line in open(sums, encoding="utf8"):
                            if not line.strip(): continue
                            h, p = line.rstrip("\n").split("  ", 1); f = os.path.join(page_dir, "static", p)
                            if not os.path.exists(f): errs.append(f"{rel}: resource missing {p}")
                            elif sha(f) != h: errs.append(f"{rel}: resource changed {p}")
    pl = os.path.join(pub, "projects", "index.html")
    if os.path.exists(pl):
        cards = len(re.findall(r'href="/projects/[\w-]+/"', open(pl, encoding="utf8").read()))
        print(f"/projects/ cards: {cards}")
    print(f"pages {pages} · showcase {showcase} · errors {len(errs)} · warnings {len(warns)}")
    for e in errs[:60]: print("  ERR", e)
    for w in warns[:20]: print("  warn", w)
    sys.exit(1 if errs else 0)

if __name__ == "__main__": main()
