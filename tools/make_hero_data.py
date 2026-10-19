#!/usr/bin/env python3
"""make_hero_data.py — build assets/data/hero-signals.json (schema herosig/1) for the home-page "signal wall" from signal files
that are ALREADY public on the showcase pages (no meta.json fields, no identifiers). Values rounded to 2 dp; <= 15 KB."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from showcase_lib import scan_forbidden
LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = [
  ("content/projects/openlka/static/can/hero-trace.json", "OpenLKA · production lane keeping on a Tampa interstate", {"speed": "v_ego_mps", "steer": "steer_angle_deg", "lane": "lane_dev_m"}),
  ("content/projects/adas-to/static/data/signals_clip_brake.json", "ADAS-TO · a brake takeover, 10 s before and after", {"speed": "vEgo", "steer": "steer_rate", "brake": "act_brake", "gas": "act_gas"}),
  ("content/projects/tridrive/static/data/signals_ex01.json", "TriDrive · lab recorder, phone pickup", {"speed": "v_ego_mps", "steer": "steer_deg", "brake": "brake", "gas": "gas"}),
]
def cols_of(d):
    c = d["cols"]
    if isinstance(c, dict): return c
    # list of names + parallel "series" rows
    rows = d.get("series") or []
    return {name: [r[i] for r in rows] for i, name in enumerate(c)}
out = {"schema": "herosig/1", "note": "Public showcase signals, resampled for the home hero; see each project page for provenance.", "clips": []}
for path, title, keys in SRC:
    d = json.load(open(os.path.join(LAB, path), encoding="utf8")); cols = cols_of(d); hz = d.get("hz", 10)
    step = 2 if hz >= 10 else 1   # 5 Hz is plenty for a background drawing
    series = {}
    for k, col in keys.items():
        v = cols.get(col)
        if v is None: continue
        series[k] = [None if x is None else round(float(x), 2) for x in v[::step]]
    ev = []
    for e in d.get("events", []):
        t = e.get("t"); lab = e.get("label") or e.get("kind") or ""
        if t is None: continue
        ev.append({"t": round(float(t), 1), "label": re.sub(r"\s+", " ", str(lab))[:40]})
    out["clips"].append({"title": title, "hz": hz / step, "n": len(next(iter(series.values()))), "series": series, "events": ev[:12]})
s = json.dumps(out, separators=(",", ":"), ensure_ascii=False)
hits = scan_forbidden(s)
if hits: raise SystemExit(f"FORBIDDEN in hero data: {hits[:3]}")
open(os.path.join(LAB, "assets", "data", "hero-signals.json"), "w", encoding="utf8").write(s)
print(f"assets/data/hero-signals.json: {len(s)} bytes, {len(out['clips'])} clips, n = {[c['n'] for c in out['clips']]}, events = {[len(c['events']) for c in out['clips']]}")
