#!/usr/bin/env python3
"""build_numbers.py --kit /path/to/WangYuHang-cmd.github.io
Builds data/numbers.json (numbers/1-lab) from the personal repo's tools/projpipe/registry.yaml (the single source of truth for
every published number) and copies assets/proj/data/hf_meta.json → data/hf_meta.json. Every key is "<page>.<key>" and carries its
source so templates can render provenance chips. Family facts are derived here and say how."""
import argparse, json, os, re, shutil, sys
LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml(path):  # the registry's two-level mapping of flow-style dicts (same loader as the kit's check_pages.py)
    out, cur = {}, None
    for line in open(path, encoding="utf8"):
        if not line.strip() or line.lstrip().startswith("#"): continue
        if not line.startswith(" "): cur = line.split(":")[0].strip(); out[cur] = {}; continue
        key, _, rest = line.strip().partition(":"); rest = rest.strip()
        if rest.startswith("{") and rest.endswith("}"):
            d = {}
            for k, v in re.findall(r'(\w+):\s*("(?:[^"\\]|\\.)*"|[^,}]+)', rest[1:-1]):
                v = v.strip()
                if v.startswith('"'): v = v[1:-1]
                else:
                    try: v = float(v) if "." in v else int(v)
                    except ValueError: pass
                d[k] = v
            out[cur][key] = d
    return out

def source_of(src, hf_types):
    src = str(src)
    if src.startswith("arxiv:"):
        ref = src[6:]; return {"kind": "arxiv", "ref": ref, "url": f"https://arxiv.org/abs/{ref}"}
    if src.startswith("hf:") or src.startswith("hf-api:"):
        repo = src.split(":", 1)[1].split("#")[0]; typ = hf_types.get(repo, "dataset")
        return {"kind": "hf-card" if src.startswith("hf:") else "hf-api", "ref": repo, "url": f"https://huggingface.co/{'datasets/' if typ == 'dataset' else ''}{repo}"}
    if src.startswith("portal:"): return {"kind": "portal", "ref": src[7:], "url": src[7:]}
    if src.startswith("log:"): return {"kind": "log", "ref": src[4:], "url": None}
    return {"kind": "other", "ref": src, "url": None}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kit", required=True); a = ap.parse_args()
    reg = load_yaml(os.path.join(a.kit, "tools", "projpipe", "registry.yaml"))
    hf_src = os.path.join(a.kit, "assets", "proj", "data", "hf_meta.json"); hf = json.load(open(hf_src, encoding="utf8"))
    shutil.copy2(hf_src, os.path.join(LAB, "data", "hf_meta.json"))
    hf_types = {r: v.get("type", "dataset") for r, v in hf["repos"].items()}
    numbers = {}
    for page, keys in reg.items():
        for k, v in keys.items():
            if not isinstance(v, dict) or "value" not in v: continue
            e = {"value": v["value"], "fmt": v.get("fmt", "0"), "tag": v.get("tag", ""), "source": source_of(v.get("source", ""), hf_types)}
            for opt in ("unit", "locator", "note"):
                if opt in v: e[opt] = v[opt]
            numbers[f"{page}.{k}"] = e
    datasets = ["openlka", "adasto", "baton", "drivedna", "drivemotion", "vlalert"]
    family = {"datasets": {"value": len(datasets), "fmt": "0", "tag": "derived", "derived_from": datasets, "op": "count",
                           "note": "open datasets & benchmarks released by the lab: OpenLKA, ADAS-TO, BATON, DriveDNA, DriveMotion, VLAlert-Bench"},
              "hf_repos": {"value": len(hf["repos"]), "fmt": "0", "tag": "derived", "derived_from": sorted(hf["repos"]), "op": "count",
                           "source": {"kind": "hf-api", "ref": "hf_meta.json", "url": "https://huggingface.co/HenryYHW", "date": hf.get("fetched")}},
              "hf_downloads": {"value": sum(int(v.get("downloads") or 0) for v in hf["repos"].values()), "fmt": "0,0", "tag": "derived", "op": "sum",
                               "source": {"kind": "hf-api", "ref": "hf_meta.json", "url": "https://huggingface.co/HenryYHW", "date": hf.get("fetched")}}}
    for k, v in family.items(): numbers[f"family.{k}"] = v
    out = {"schema": "numbers/1-lab", "generated": "2026-10-19", "registry": "WangYuHang-cmd.github.io/tools/projpipe/registry.yaml", "hf_meta_fetched": hf.get("fetched"), "numbers": numbers}
    json.dump(out, open(os.path.join(LAB, "data", "numbers.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
    print(f"data/numbers.json: {len(numbers)} numbers from {len(reg)} pages; hf_meta {len(hf['repos'])} repos (fetched {hf.get('fetched')})")

if __name__ == "__main__": main()
