#!/usr/bin/env python3
"""check_showcase.py [--allow-missing /datasets/ …]
Static gates for the showcase bundles content/projects/<slug>/index.html (lab port of the kit's check_pages.py):
  refs      every local src/href/poster/data-* resolves (bundle file, static/ file, or a content route)
  motion    no literal durations/beziers in page HTML
  venue     no submission-venue / anonymity leakage (public acceptances exempt)
  claims    superlatives only inside data-claim
  numbers   every <data class="n" value> matches data/numbers.json for the page's registry section
  tiers     data-hf text ("manual" / "auto" / "open") matches data/hf_meta.json
  contrast  page accent vs the deep-green theme tokens (bg, bg-1, bg-2, surface over bg-2) ≥ 4.5
  chrome    More-works menus list every sibling + /datasets/ identically"""
import argparse, html, json, os, re, sys
from html.parser import HTMLParser
LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENUE_RX = re.compile(r"\b(KDD|WACV|ICLR|NeurIPS|CVPR|anonymous authors?|anonymi[sz]ed for review|double-blind|under submission|submitted to)\b", re.I)
ACCEPTED = ["WACV 2027", "Winter Conference on Applications of Computer Vision (WACV)", "CoRL 2026", "ITSC 2026", "ITSC 2025", "ACCIDENT @ CVPR 2026"]
ACCEPTED_RX = re.compile("|".join(re.escape(v) for v in ACCEPTED), re.I)
SUPERLATIVE_RX = re.compile(r"\b(the first|the only|state[- ]of[- ]the[- ]art|SOTA|the largest|the best|unprecedented|novel)\b", re.I)
MOTION_RX = re.compile(r"\b\d+(?:\.\d+)?m?s\b(?=[^<]*[;\"])|cubic-bezier\(")
SLUGS = ["tridrive", "adas-to", "drivedna", "drivemotion", "baton", "openlka", "vlalert"]
ROUTES = {"/": "content/_index.md", "/projects/": "content/projects/_index.md", "/publications/": "content/publications/_index.md",
          "/news/": "content/news/_index.md", "/team/": "content/team/_index.md", "/datasets/": "content/datasets.md"}

def rel_lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contrast(a, b): la, lb = rel_lum(a), rel_lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)
def blend(fg, al, bg):
    f = [int(fg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]; b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(f[i] * al + b[i] * (1 - al)):02x}" for i in range(3))
def strip_tags(s): return html.unescape(re.sub(r"<[^>]+>", " ", s))

class _Claims(HTMLParser):
    VOID = {"br", "img", "meta", "link", "input", "hr", "source", "wbr"}
    def __init__(self): super().__init__(); self.depth = 0; self.out = []; self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag in self.VOID: return
        self.stack.append(any(k == "data-claim" for k, _ in attrs))
        if self.stack[-1]: self.depth += 1
    def handle_endtag(self, tag):
        if tag in self.VOID or not self.stack: return
        if self.stack.pop(): self.depth -= 1
    def handle_data(self, d):
        if self.depth > 0: self.out.append(d)
def claim_text(body): p = _Claims(); p.feed(body); return " ".join(p.out)

def front_matter(src):
    m = re.match(r"---\n(.*?)\n---\n", src, re.S); fm = {}
    for line in m.group(1).split("\n"):
        mm = re.match(r"^(\w+):\s*(.*)$", line)
        if mm: fm[mm.group(1)] = mm.group(2).strip()
    return fm, src[m.end():]

def route_exists(u, allow_missing):
    if any(u.startswith(x) for x in allow_missing): return True
    path = u.split("#")[0]
    if path in ROUTES: return os.path.exists(os.path.join(LAB, ROUTES[path]))
    m = re.match(r"^/projects/([\w-]+)/$", path)
    if m: return os.path.exists(os.path.join(LAB, "content", "projects", m.group(1), "index.html")) or os.path.exists(os.path.join(LAB, "content", "projects", m.group(1) + ".md"))
    m = re.match(r"^/team/([\w-]+)/$", path)
    if m: return os.path.exists(os.path.join(LAB, "content", "team", m.group(1) + ".md"))
    return os.path.exists(os.path.join(LAB, "static", path.lstrip("/")))

def check(slug, numbers, hf, theme, allow_missing):
    P = []; d = os.path.join(LAB, "content", "projects", slug); path = os.path.join(d, "index.html")
    if not os.path.exists(path): return [f"{slug}: index.html missing"]
    src = open(path, encoding="utf8").read(); fm, body = front_matter(src); kit = fm.get("kit") == "true"; proj = fm.get("proj", "").strip('"')
    for m in re.finditer(r'(?:src|href|poster|data-src|data-video|data-poster|data-zoom)="([^"#][^"]*)"', body):
        u = m.group(1).split("?")[0]
        if u.startswith(("http", "mailto:", "data:", "key:", "//", "javascript:", "about:")): continue
        if re.fullmatch(r"[\w-]+", u): continue
        if u.startswith("/"):
            if not route_exists(u, allow_missing): P.append(f"ref missing: {u}")
        elif not os.path.exists(os.path.join(d, u)): P.append(f"ref missing: {u}")
    scanned = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.S)
    for m in MOTION_RX.finditer(re.sub(r"<style[^>]*>.*?</style>", "", scanned, flags=re.S)):
        ctx = scanned[max(0, m.start() - 20):m.end() + 10]
        if 'style="' in ctx or "transition" in ctx or "animation" in ctx: P.append(f"literal motion value: …{ctx.strip()}…")
    text = strip_tags(re.sub(r"<(script|style)[^>]*>.*?</\1>", "", body, flags=re.S))
    acc = [(a.start(), a.end()) for a in ACCEPTED_RX.finditer(text)]
    for m in VENUE_RX.finditer(text):
        if any(a <= m.start() < b for a, b in acc): continue
        P.append(f"venue/anonymity leakage: '{m.group(0)}' …{text[max(0, m.start()-30):m.end()+30].strip()}…")
    if kit:
        allowed = claim_text(body)
        for m in SUPERLATIVE_RX.finditer(text):
            if re.sub(r"\s+", " ", m.group(0).lower()) in re.sub(r"\s+", " ", allowed.lower()): continue
            P.append(f"superlative outside data-claim: …{text[max(0, m.start()-40):m.end()+40].strip()}…")
        vals = [float(v["value"]) for k, v in numbers.items() if k.startswith(proj + ".") and isinstance(v.get("value"), (int, float))]
        for m in re.finditer(r'<data class="n" value="([^"]+)"', body):
            v = float(m.group(1).replace(",", ""))
            if not any(abs(v - rv) <= max(1e-9, abs(rv) * 1e-6) for rv in vals): P.append(f"number {m.group(1)} not in numbers.json[{proj}.*]")
        for m in re.finditer(r'data-hf="([^"]+)"[^>]*>(.*?)</', body, flags=re.S):
            repo, inner = m.group(1), strip_tags(m.group(2)).lower(); info = hf.get(repo)
            if not info: P.append(f"hf repo {repo} not in hf_meta.json"); continue
            want = "auto" if info["gated"] == "auto" else "manual" if info["gated"] == "manual" else "open"
            if want not in inner: P.append(f"{repo}: page says '{inner.strip()[:40]}', hf_meta says gated={info['gated']}")
        css = open(os.path.join(LAB, "static", "assets", "proj", "proj.css"), encoding="utf8").read()
        a = re.search(r'body\[data-proj="%s"\]\{--pj-accent:(#[0-9a-f]{6})' % proj, css)
        if a:
            for name, b in (("bg", theme["--cl-bg"]), ("bg-1", theme["--cl-bg-1"]), ("bg-2", theme["--cl-bg-2"]), ("surface/bg-2", blend("#ffffff", .045, theme["--cl-bg-2"]))):
                c = contrast(a.group(1), b)
                if c < 4.5: P.append(f"accent {a.group(1)} on {name} contrast {c:.2f} < 4.5")
        else: P.append(f"no accent block for data-proj={proj} in proj.css")
    return P

def check_chrome():
    P = []; menus = {}
    for slug in SLUGS:
        p = os.path.join(LAB, "content", "projects", slug, "index.html")
        if not os.path.exists(p): continue
        s = open(p, encoding="utf8").read(); m = re.search(r'class="(?:pj|lk)-dd__menu"[^>]*>(.*?)</(?:div|ul)>', s, re.S)
        if not m: P.append(f"{slug}: no More-works menu"); continue
        ent = re.findall(r'href="(/[^"]+)"><b>([^<]+)</b><span>([^<]+)</span>', m.group(1))
        want = {f"/projects/{x}/" for x in SLUGS if x != slug} | {"/datasets/"}
        got = {e[0] for e in ent}
        if got != want: P.append(f"{slug}: More-works set differs: missing {sorted(want - got)} extra {sorted(got - want)}")
        for e in ent: menus.setdefault(e[0], set()).add((e[1], e[2]))
    for k, v in menus.items():
        if len(v) > 1: P.append(f"More-works text for {k} differs across pages: {sorted(v)}")
    return P

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("slugs", nargs="*"); ap.add_argument("--allow-missing", nargs="*", default=[]); a = ap.parse_args()
    numbers = json.load(open(os.path.join(LAB, "data", "numbers.json"), encoding="utf8"))["numbers"]
    hf = json.load(open(os.path.join(LAB, "data", "hf_meta.json"), encoding="utf8"))["repos"]
    theme = dict(re.findall(r"(--cl-bg(?:-[12])?):(#[0-9a-f]{6})", open(os.path.join(LAB, "assets", "css", "showcase-theme.css"), encoding="utf8").read()))
    bad = False
    for slug in a.slugs or SLUGS:
        pr = check(slug, numbers, hf, theme, a.allow_missing)
        print(f"== {slug}: {'ok' if not pr else str(len(pr)) + ' problem(s)'}"); [print("   -", x) for x in pr]; bad |= bool(pr)
    pr = check_chrome(); print(f"== chrome: {'ok' if not pr else ''}"); [print("   -", x) for x in pr]; bad |= bool(pr)
    sys.exit(1 if bad else 0)

if __name__ == "__main__": main()
