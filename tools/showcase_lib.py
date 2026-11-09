#!/usr/bin/env python3
"""Shared helpers for the showcase port + checks (stdlib only).
FORBIDDEN mirrors tools/projpipe/common.py in the personal repo: identifiers, locations, local paths and secrets that must
never reach the published site. Exemptions are by PATH (see privacy_scan.py), never by literal value."""
import hashlib, os, re, fnmatch

SLUG = {"tridrive": "tridrive", "adasto": "adas-to", "drivedna": "drivedna", "drivemotion": "drivemotion",
        "baton": "baton", "openlka": "openlka", "vlalert": "vlalert"}          # personal slug -> lab slug
KIT_PAGES = ["tridrive", "adasto", "drivedna", "drivemotion", "baton"]
SUMS_NAME = "SHA256SUMS"

FORBIDDEN = [
    ("dongle id", re.compile(r"(?<![0-9a-f.])[0-9a-f]{16}(?![0-9a-f])")),
    ("route id", re.compile(r"[0-9a-f]{8}--[0-9a-f]{10}")),
    ("route timestamp", re.compile(r"\d{4}-\d{2}-\d{2}--\d{2}-\d{2}-\d{2}")),
    ("uid", re.compile(r"[A-Z0-9_]+__[0-9a-f]{16}__")),
    ("session id", re.compile(r"\d{8}T\d{6}Z_[0-9a-f]{16}")),
    ("youtube id", re.compile(r"(?:[?&]v=|youtu\.be/)[\w-]{11}")),
    ("bilibili id", re.compile(r"\bBV[0-9A-Za-z]{10}\b")),
    ("gps key", re.compile(r"\"(?:lat|lon|latitude|longitude|gps_lat|gps_lon)\"\s*:")),
    ("local path", re.compile(r"/home/henry|/data/datasets|Dropbox")),
    ("hf token", re.compile(r"hf_[A-Za-z0-9]{20,}")),
    ("openai key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}")),
    ("mapbox token", re.compile(r"pk\.[A-Za-z0-9]{20,}\.[A-Za-z0-9]{10,}")),
]
SECRETS_ONLY = {"local path", "hf token", "openai key", "jwt", "mapbox token"}
DENY_FILES = ["*token*", "*id_map*.json", "*hash_map*", "*salt*", "*questionnaire*", "dcamera.mp4", "client_secret_*.json",
              "JWT.txt", "*.key", "*.pem", "*api_key*"]
TEXT_EXT = {".html", ".htm", ".md", ".json", ".css", ".js", ".mjs", ".yaml", ".yml", ".toml", ".txt", ".svg", ".xml", ".csv", ".py", ".sh"}

def is_text(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[1].lower() in TEXT_EXT or base == SUMS_NAME

def mask(text):
    text = re.sub(r"\"sha256\"\s*:\s*\"[0-9a-f]{64}\"", '"sha256":"<sha>"', text)
    text = re.sub(r"(?m)^[0-9a-f]{64}(?=  )", "<sha>", text)                    # SHA256SUMS lines
    text = re.sub(r"\"[A-Za-z0-9+/=]{160,}\"", '"<b64>"', text)               # opaque base64 payloads
    text = re.sub(r"integrity=\"sha(?:256|384|512)-[A-Za-z0-9+/=]+\"", 'integrity="<sri>"', text)
    return text

def scan_forbidden(text, rules=None, allow_rx=()):
    text = mask(text)
    for rx in allow_rx: text = re.sub(rx, "<allowed>", text)
    hits = []
    for name, rx in FORBIDDEN:
        if rules is not None and name not in rules: continue
        for m in rx.finditer(text): hits.append((name, m.group(0)[:40]))
    return hits

def denied_name(path):
    base = os.path.basename(path)
    return any(fnmatch.fnmatch(base, g) for g in DENY_FILES)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def write_sums(static_dir):
    """<hex>  <path relative to static/> for every file under static_dir except the sums file itself (sorted)."""
    lines = []
    for root, _, files in os.walk(static_dir):
        for fn in files:
            if fn == SUMS_NAME: continue
            p = os.path.join(root, fn); rel = os.path.relpath(p, static_dir).replace(os.sep, "/")
            lines.append(f"{sha256_file(p)}  {rel}")
    lines.sort(key=lambda l: l.split("  ", 1)[1])
    with open(os.path.join(static_dir, SUMS_NAME), "w", encoding="utf8") as f: f.write("\n".join(lines) + "\n")
    return len(lines)
