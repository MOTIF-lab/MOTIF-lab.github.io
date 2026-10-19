#!/usr/bin/env python3
"""privacy_scan.py [--paths DIR…] [--files FILE…] [--exempt PREFIX…] [--spans FILE…] [--allow-rx RX…] [--secrets-only PREFIX…]
Scans text files for FORBIDDEN patterns (tools/showcase_lib.py). Exit 1 on any hit.
  --exempt        path prefixes skipped entirely (e.g. content/projects/openlka/static/can)
  --spans         files in which the OpenLKA recorder spans (data-dongle="…", <span class="rec__id mono">…</span>) are stripped first
  --secrets-only  path prefixes where only the secret/path rules apply (lab news may legitimately embed YouTube ids)
  --allow-rx      regexes replaced by <allowed> before scanning (e.g. public Dropbox release folders)"""
import argparse, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from showcase_lib import scan_forbidden, is_text, denied_name, SECRETS_ONLY

SPAN_RX = [re.compile(r'\sdata-dongle="[0-9a-f]{16}"'), re.compile(r'<span class="rec__id mono">[^<]*</span>')]

def iter_files(paths, files):
    for f in files: yield f
    for p in paths:
        if os.path.isfile(p): yield p; continue
        for root, dirs, fns in os.walk(p):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "public", "resources")]
            for fn in fns: yield os.path.join(root, fn)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--paths", nargs="*", default=[]); ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--exempt", nargs="*", default=[]); ap.add_argument("--spans", nargs="*", default=[]); ap.add_argument("--allow-rx", nargs="*", default=[])
    ap.add_argument("--secrets-only", nargs="*", default=[]); ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(); bad = 0; n = 0
    norm = lambda p: os.path.normpath(p).replace(os.sep, "/")
    for f in iter_files(a.paths, a.files):
        fp = norm(f)
        if any(fp.startswith(norm(e)) for e in a.exempt): continue
        if fp.endswith(('tools/privacy_scan.py', 'tools/showcase_lib.py')): continue   # the rule definitions themselves
        if denied_name(fp): print(f"DENY_FILES name: {fp}"); bad += 1; continue
        if not is_text(fp) or not os.path.exists(fp): continue
        try: text = open(fp, encoding="utf8", errors="replace").read()
        except OSError: continue
        if fp in map(norm, a.spans):
            for rx in SPAN_RX: text = rx.sub("", text)
        rules = SECRETS_ONLY if any(fp.startswith(norm(e)) for e in a.secrets_only) else None
        hits = scan_forbidden(text, rules, a.allow_rx); n += 1
        if hits:
            bad += len(hits); agg = {}
            for k, v in hits: agg.setdefault(k, []).append(v)
            print(f"{fp}: " + "; ".join(f"{k} ×{len(v)} e.g. {v[0]!r}" for k, v in agg.items()))
    if not a.quiet: print(f"scanned {n} text files · {bad} problem(s)")
    sys.exit(1 if bad else 0)

if __name__ == "__main__": main()
