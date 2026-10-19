#!/usr/bin/env python3
"""build_vlalert.py --src /path/to/WangYuHang-cmd.github.io
Authors the VLAlert showcase bundle on the kit (the personal page uses an old Bulma template that is not copied):
content/projects/vlalert/{index.html, static/data/*.json, static/SHA256SUMS}. Media (redacted demo MP4s + posters, figures)
must already be in content/projects/vlalert/static/media (tools/vlalert_media.sh + the figure conversion)."""
import argparse, hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from showcase_lib import SLUG, scan_forbidden, sha256_file, write_sums
from port_showcase import more_table, stub_frontmatter, jdump, ORDER, DD_EXTRA, BRAND_NEW, FOOT_NEW, EXTRA_NEW, Fail

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(LAB, "content", "projects", "vlalert")
TODAY = "2026-10-19"

SOURCES = {"schema": "sources/1", "sources": [
  {"id": "arxiv-abs", "kind": "arxiv", "url": "https://arxiv.org/abs/2609.08130v1", "version": "v1", "date": "2026-09-08", "locator": "Abstract",
   "quote": "casts warning generation as a tri-action policy over SILENT, OBSERVE, and ALERT"},
  {"id": "arxiv-daus", "kind": "arxiv", "url": "https://arxiv.org/abs/2609.08130v1", "version": "v1", "date": "2026-09-08", "locator": "Abstract",
   "quote": "DAUS 0.4878 compared with 0.4752 for Open-BADAS"},
  {"id": "arxiv-metrics", "kind": "arxiv", "url": "https://arxiv.org/abs/2609.08130v1", "version": "v1", "date": "2026-09-08", "locator": "Abstract",
   "quote": "improves AUROC, AP_tick, F1_t, and balanced accuracy from 0.610, 0.176, 0.276, and 0.581 to 0.689, 0.195, 0.297, and 0.648"},
  {"id": "arxiv-critic", "kind": "arxiv", "url": "https://arxiv.org/abs/2609.08130v1", "version": "v1", "date": "2026-09-08", "locator": "Abstract",
   "quote": "On 221 held-out ADAS-TO-Critic clips, VLAlert improves R@5s from 74.2% to 88.7% and F1 from 0.585 to 0.686"},
  {"id": "arxiv-model", "kind": "arxiv", "url": "https://arxiv.org/abs/2609.08130v1", "version": "v1", "date": "2026-09-08", "locator": "Abstract",
   "quote": "VLAlert uses Qwen3-VL-4B as a safety-evidence generator and pools hidden states from structured belief spans"},
  {"id": "hf-videos", "kind": "hf-card", "url": "https://huggingface.co/datasets/HenryYHW/VLAlert", "date": TODAY, "locator": "Dataset card · At a glance",
   "quote": "Videos 6,406 1,219 2,647 1,051 2,211 13,534"},
  {"id": "hf-ticks", "kind": "hf-card", "url": "https://huggingface.co/datasets/HenryYHW/VLAlert", "date": TODAY, "locator": "Dataset card · At a glance",
   "quote": "Ticks (1 Hz) 97,649 11,220 23,661 21,020 39,342 192,892"},
  {"id": "hf-sources", "kind": "hf-card", "url": "https://huggingface.co/datasets/HenryYHW/VLAlert", "date": TODAY, "locator": "Dataset card",
   "quote": "VLAlert-Bench integrates six driving-event datasets — Nexar Collision, DoTA, DAD, DADA-2000, ADAS-TO-Critic, and the Kaggle ACCIDENT @ CVPR 2026 challenge — into a single per-tick prediction task with three actions: SILENT (0) / OBSERVE (1) / ALERT (2)."},
  {"id": "hf-tick", "kind": "hf-card", "url": "https://huggingface.co/datasets/HenryYHW/VLAlert", "date": TODAY, "locator": "Dataset card",
   "quote": "A tick is a 1-second sliding-window record carrying 8 consecutive frame indices plus the action label at the window's last frame."},
  {"id": "hf-license", "kind": "hf-api", "url": "https://huggingface.co/datasets/HenryYHW/VLAlert", "date": TODAY, "locator": "repo metadata",
   "quote": "license: cc-by-4.0 · gated: manual"},
]}
NUMBERS = {"schema": "numbers/1", "page": "vlalert", "numbers": {
  "videos": {"value": 13534, "fmt": "0,0", "source": "hf-videos", "tag": "latest release"},
  "ticks": {"value": 192892, "fmt": "0,0", "source": "hf-ticks", "tag": "latest release"},
  "actions": {"value": 3, "fmt": "0", "source": "arxiv-abs", "tag": "in the paper"},
  "sources": {"value": 6, "fmt": "0", "source": "hf-sources", "tag": "latest release"},
  "daus": {"value": 0.4878, "fmt": ".0000", "source": "arxiv-daus", "tag": "in the paper"}, "daus_badas": {"value": 0.4752, "fmt": ".0000", "source": "arxiv-daus", "tag": "in the paper"},
  "auroc": {"value": 0.689, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"}, "auroc_base": {"value": 0.610, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"},
  "ap_tick": {"value": 0.195, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"}, "ap_tick_base": {"value": 0.176, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"},
  "f1_t": {"value": 0.297, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"}, "f1_t_base": {"value": 0.276, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"},
  "bal_acc": {"value": 0.648, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"}, "bal_acc_base": {"value": 0.581, "fmt": ".000", "source": "arxiv-metrics", "tag": "in the paper"},
  "critic_clips": {"value": 221, "fmt": "0", "source": "arxiv-critic", "tag": "in the paper"},
  "r5s": {"value": 88.7, "fmt": "0.0", "unit": "%", "source": "arxiv-critic", "tag": "in the paper"}, "r5s_base": {"value": 74.2, "fmt": "0.0", "unit": "%", "source": "arxiv-critic", "tag": "in the paper"},
  "f1_critic": {"value": 0.686, "fmt": ".000", "source": "arxiv-critic", "tag": "in the paper"}, "f1_critic_base": {"value": 0.585, "fmt": ".000", "source": "arxiv-critic", "tag": "in the paper"},
}}
SPLITS = [("Train", 6406, 97649), ("Val", 1219, 11220), ("Test", 2647, 23661), ("Extra: ADAS-TO", 1051, 21020), ("Extra: ACCIDENT", 2211, 39342)]
BARS = {"schema": "bars/1", "unit": "ticks", "max": None,
        "rows": [{"label": n, "v": t, "color": "accent" if n.startswith("Extra") else "mute", "emph": n == "Train", "note": f"{v:,} videos"} for n, v, t in SPLITS],
        "meta": {"title": "VLAlert-Bench · ticks per split (1 Hz)", "source": "hf-ticks"}}
DEMOS = [("vlalert_demo1", "Per-tick alert decision", "Alert decision on an approaching hazard: the policy stays SILENT until the risk builds, then alerts.", "520/440"),
         ("vlalert_demo3", "OBSERVE → ALERT escalation", "Escalation from OBSERVE to ALERT on a night-time highway scene.", "560/474"),
         ("vlalert_demo9", "Hazard-driven ALERT", "A safety-critical collision sequence; the red header marks the earliest alert.", "520/371")]
FIGS = [("fig_pipeline", "The VLAlert pipeline: a per-tick tri-action policy with an OBSERVE action that delays uncertain warnings and changes the next observation window.", 1500, 428),
        ("fig_arch", "Model architecture for per-tick alert decisions.", 1600, 763),
        ("fig_belief", "Belief spans over the SILENT / OBSERVE / ALERT states.", 1400, 528),
        ("fig_valdist", "Label distribution across the validation splits.", 1200, 657)]

def probe_dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    return round(float(out), 1) if out else None

def body(more):
    menu = "".join(f'<a href="/projects/{SLUG[k]}/"><b>{more[k][0]}</b><span>{more[k][1]}</span></a>' for k in ORDER if k != "vlalert") + DD_EXTRA
    demos = "\n".join(f'''      <figure class="pj-fig reveal tilt" style="--i:{i}"><img src="static/media/{n}.jpg" alt="{t}" width="{ar.split('/')[0]}" height="{ar.split('/')[1]}" loading="lazy">
        <figcaption><b>{t}.</b> {c}</figcaption>
        <div class="pj-cta"><button class="btn btn--sm" type="button" data-video="static/media/{n}.mp4" data-poster="static/media/{n}.jpg" data-title="VLAlert · {t}" data-caption="{c} Source: public dashcam research footage; platform watermark, uploader handle and the recorder's date/VIN strip are blacked out." data-ar="{ar}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5v14l12-7z"/></svg>Play</button></div></figure>''' for i, (n, t, c, ar) in enumerate(DEMOS))
    figs = "\n".join(f'      <figure class="pj-fig reveal" style="--i:{i}"><img src="static/media/{n}.jpg" alt="{c}" width="{w}" height="{h}" loading="lazy" data-zoom><figcaption>{c}</figcaption></figure>' for i, (n, c, w, h) in enumerate(FIGS[1:]))
    split_rows = "\n".join(f'<tr><td>{n}</td><td><data class="n" value="{v}" data-src="hf-videos">{v:,}</data></td><td><data class="n" value="{t}" data-src="hf-ticks">{t:,}</data></td></tr>' for n, v, t in SPLITS)
    return f'''<a class="pj-skip" href="#main">Skip to content</a>
<div class="pj-bg" aria-hidden="true"></div><div class="pj-stars" aria-hidden="true"></div>

<header class="pj-nav" id="nav">
  <div class="pj-nav__in">
    {BRAND_NEW}
    <nav class="pj-menu" aria-label="Page">
      <ul class="pj-anchors">
        <li><a href="#top">VLAlert</a></li><li><a href="#overview">Overview</a></li><li><a href="#signature">Demos</a></li><li><a href="#evidence">Evidence</a></li><li><a href="#method">Method</a></li><li><a href="#results">Results</a></li><li><a href="#data">Data</a></li><li><a href="#cite">Cite</a></li>
      </ul>
      <ul>
        {EXTRA_NEW}
        <li class="pj-dd"><button class="pj-dd__btn" type="button" aria-expanded="false" aria-haspopup="true">More works <svg class="ic ic-sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="pj-dd__menu">{menu}</div></li>
        <li><a class="btn btn--sm" href="https://arxiv.org/abs/2609.08130" target="_blank" rel="noopener"><span class="arxiv-mark">arXiv</span> 2609.08130</a></li>
      </ul>
    </nav>
    <button class="pj-burger" type="button" aria-expanded="false" aria-label="Open menu" aria-controls="nav"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
  <div class="pj-progress" aria-hidden="true"></div>
</header>

<main id="main">
<!-- ================= hero ================= -->
<section class="pj-hero" id="top">
  <div class="pj-wrap">
    <div class="pj-hero__grid">
      <div class="pj-hero__text">
        <p class="pj-eyebrow">Benchmark &amp; method · adaptive driver alerting · CoRL 2026</p>
        <h1 class="pj-h1"><span class="pj-wordmark">VLAlert</span><span class="pj-title">Observe Before You Alert: Adaptive Driver Alerting with Vision–Language Models</span></h1>
        <p class="pj-thesis">A unified per-tick benchmark for deciding when a driving system should stay <b>SILENT</b>, <b>OBSERVE</b>, or <b>ALERT</b> — and a vision–language policy in which <span data-claim="arxiv-abs">the OBSERVE action acts as an internal evidence-gathering decision that delays uncertain warnings</span>.</p>
        <p class="pj-lede">At each one-second tick a model sees the last eight frames and predicts the appropriate alert action. VLAlert-Bench joins six driving-event sources into one task — <data class="n" value="13534" data-src="hf-videos">13,534</data> videos and <data class="n" value="192892" data-src="hf-ticks">192,892</data> labelled ticks across five splits — and the VLAlert policy, built on Qwen3-VL-4B, is scored on it and on held-out ADAS-TO-Critic takeover clips.</p>
        <div class="pj-pills"><span class="pj-pill pj-pill--accent">CoRL 2026 · accepted · arXiv 2609.08130</span><span class="pj-pill">CoRL 2026 Travel Award</span><span class="pj-pill">CC BY 4.0 · gated, manual approval</span></div>
        <div class="pj-cta">
          <a class="btn btn--primary" href="#signature">Watch the demos</a>
          <a class="btn" href="https://arxiv.org/abs/2609.08130" target="_blank" rel="noopener"><span class="arxiv-mark">arXiv</span> Paper</a>
          <a class="btn" href="https://huggingface.co/datasets/HenryYHW/VLAlert" target="_blank" rel="noopener">Dataset</a>
        </div>
        <p class="pj-authors"><a href="/team/yuhang-wang/">Yuhang Wang</a><sup>1</sup><span class="sep">·</span>Lingyao Li<sup>2</sup><span class="sep">·</span><a href="https://sites.google.com/view/haozhou-cv" target="_blank" rel="noopener">Hao Zhou</a><sup>1</sup></p>
        <p class="pj-affil"><sup>1</sup>University of South Florida · MOTIF-Lab &nbsp; <sup>2</sup>University of Arizona</p>
      </div>
      <div class="pj-hero__stage">
        <div class="pj-sc__media" style="--ar:520/371"><video muted autoplay playsinline loop preload="metadata" poster="static/media/vlalert_demo9.jpg" src="static/media/vlalert_demo9.mp4" width="520" height="371" aria-label="Demo: a safety-critical collision sequence with the per-tick VLAlert decision overlaid"></video></div>
        <div class="pj-stage__cap"><span>demo · <b>per-tick decision</b> · 1 Hz</span><span class="pj-pill pj-pill--live">SILENT → OBSERVE → ALERT</span></div>
      </div>
    </div>
    <div class="pj-stats">
      <a class="stat" href="#f-bench"><span class="num" data-count="13534">13,534</span><span class="lbl">videos across five splits <data class="n" value="13534" data-src="hf-videos">(dataset card)</data></span></a>
      <a class="stat" href="#f-bench"><span class="num" data-count="192892">192,892</span><span class="lbl">one-second labelled ticks <data class="n" value="192892" data-src="hf-ticks">(dataset card)</data></span></a>
      <a class="stat" href="#f-bench"><span class="num" data-count="3">3</span><span class="lbl">alert actions: SILENT · OBSERVE · ALERT <data class="n" value="3" data-src="arxiv-abs">(paper)</data></span></a>
      <a class="stat" href="#f-bench"><span class="num" data-count="6">6</span><span class="lbl">source datasets <data class="n" value="6" data-src="hf-sources">(dataset card)</data></span></a>
    </div>
    <p class="stat-foot">The paper's abstract describes VLAlert-Bench as built from four real-world dashcam alert datasets; the released card adds the ADAS-TO-Critic and Kaggle ACCIDENT extra splits, bringing the sources to six.</p>
  </div>
</section>

<!-- ================= overview ================= -->
<section class="pj-section" id="overview">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">01 · OVERVIEW</span><h2>When is the evidence enough to warn?</h2><p class="sec-lede">The arXiv abstract, verbatim, beside what you need to know at a glance.</p></div>
    <div class="pj-overview">
      <div class="pj-abstract reveal" data-claim="arxiv-abs"><p>Driver alerting from dashcam video requires sequential decision-making under partial observability: a system must decide not only whether a scene is risky, but also when the evidence is sufficient to warn. Most existing accident anticipation models output a binary risk score, leaving ambiguous scenes to be handled by thresholding. We propose VLAlert, a vision-language alerting framework that casts warning generation as a tri-action policy over SILENT, OBSERVE, and ALERT. The OBSERVE action acts as an internal evidence-gathering decision that delays uncertain warnings and changes the next observation window, creating a lightweight perception-action loop for adaptive alerting. VLAlert uses Qwen3-VL-4B as a safety-evidence generator and pools hidden states from structured belief spans to form compact representations for danger estimation and policy prediction. We evaluate VLAlert on VLAlert-Bench, a unified per-tick benchmark from four real-world dashcam alert datasets, and further test transfer to held-out naturalistic ADAS takeover clips. On VLAlert-Bench validation, VLAlert achieves the highest deployment-oriented utility among tested baselines, with DAUS 0.4878 compared with 0.4752 for Open-BADAS, and improves AUROC, AP_tick, F1_t, and balanced accuracy from 0.610, 0.176, 0.276, and 0.581 to 0.689, 0.195, 0.297, and 0.648, respectively. On 221 held-out ADAS-TO-Critic clips, VLAlert improves R@5s from 74.2% to 88.7% and F1 from 0.585 to 0.686. These results indicate that adaptive observation and safety-focused VLM representations provide measurable gains for driver-facing alert decisions.</p></div>
      <aside class="pj-glance reveal" style="--i:1"><dl>
        <div><dt>Venue</dt><dd>Conference on Robot Learning (CoRL 2026) · accepted · CoRL 2026 Travel Award · arXiv 2609.08130 v1 · 8 Sep 2026</dd></div>
        <div><dt>Links</dt><dd><a href="https://arxiv.org/abs/2609.08130" target="_blank" rel="noopener">arXiv</a><a href="https://huggingface.co/datasets/HenryYHW/VLAlert" target="_blank" rel="noopener">Dataset</a><a href="#cite">BibTeX</a></dd></div>
        <div><dt>Task</dt><dd class="mono">1 Hz ticks · last 8 frames per tick · actions SILENT (0) / OBSERVE (1) / ALERT (2) · five splits with manifests</dd></div>
        <div><dt>Sources</dt><dd>Nexar Collision · DoTA · DAD · DADA-2000 · ADAS-TO-Critic · Kaggle ACCIDENT @ CVPR 2026</dd></div>
        <div><dt>License</dt><dd>CC BY 4.0 · <span data-hf="HenryYHW/VLAlert">gated, manual approval</span></dd></div>
        <div><dt>Privacy</dt><dd>Public dashcam research footage. The three demo clips on this page are shown with platform watermarks, uploader handles and the recorder's date/VIN strip blacked out.</dd></div>
      </dl></aside>
    </div>
  </div>
</section>

<!-- ================= demos ================= -->
<section class="pj-section pj-section--band" id="signature">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">02 · DEMOS</span><h2>Per-tick decisions on real driving-event footage</h2><p class="sec-lede">Each clip overlays the VLAlert decision (header) and the alert probability trace of VLAlert against the BADAS baseline (bottom). Red marks the earliest ALERT.</p></div>
    <div class="grid-3">
{demos}
    </div>
  </div>
</section>

<!-- ================= evidence ================= -->
<section class="pj-section" id="evidence">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">03 · EVIDENCE</span><h2>What the numbers rest on</h2></div>
    <div class="findings">
      <article class="finding reveal tilt" id="f-utility"><span class="finding__n">0.4878 <small>DAUS · Open-BADAS 0.4752</small></span><p class="finding__claim">Deployment-oriented utility is where the tri-action policy pays off.</p><p><span data-claim="arxiv-daus">On VLAlert-Bench validation, VLAlert achieves the highest deployment-oriented utility among tested baselines</span> — DAUS <data class="n" value="0.4878" data-src="arxiv-daus">0.4878</data> against <data class="n" value="0.4752" data-src="arxiv-daus">0.4752</data> for Open-BADAS; DAUS scores the usefulness of the alert stream rather than frame-level accuracy alone.</p></article>
      <article class="finding reveal tilt" id="f-metrics" style="--i:1"><span class="finding__n">.689 <small>AUROC · from .610</small></span><p class="finding__claim">Four frame-level metrics move together.</p><p>AUROC <data class="n" value="0.610" data-src="arxiv-metrics">.610</data> → <data class="n" value="0.689" data-src="arxiv-metrics">.689</data>, AP<sub>tick</sub> <data class="n" value="0.176" data-src="arxiv-metrics">.176</data> → <data class="n" value="0.195" data-src="arxiv-metrics">.195</data>, F1<sub>t</sub> <data class="n" value="0.276" data-src="arxiv-metrics">.276</data> → <data class="n" value="0.297" data-src="arxiv-metrics">.297</data>, balanced accuracy <data class="n" value="0.581" data-src="arxiv-metrics">.581</data> → <data class="n" value="0.648" data-src="arxiv-metrics">.648</data>.</p></article>
      <article class="finding reveal tilt" id="f-transfer" style="--i:2"><span class="finding__n">88.7 % <small>R@5s · from 74.2 %</small></span><p class="finding__claim">It transfers to the lab's own takeover clips.</p><p>On <data class="n" value="221" data-src="arxiv-critic">221</data> held-out ADAS-TO-Critic clips — naturalistic Level-2 takeovers recorded by the lab, not web uploads — recall within five seconds rises from 74.2 % to 88.7 % and F1 from <data class="n" value="0.585" data-src="arxiv-critic">.585</data> to <data class="n" value="0.686" data-src="arxiv-critic">.686</data>.</p></article>
      <article class="finding finding--wide reveal" id="f-bench" style="--i:3"><span class="finding__n">192,892 <small>ticks · five splits · six sources</small></span><p class="finding__claim">One per-tick task over six event datasets.</p><p><span data-claim="hf-tick">A tick is a 1-second sliding-window record carrying 8 consecutive frame indices plus the action label at the window's last frame.</span> The two extra splits — ADAS-TO (lab-recorded takeovers) and the Kaggle ACCIDENT challenge — are held out of training.</p>
        <div data-widget="bars" data-src="key:bars_splits" data-label="VLAlert-Bench ticks per split"><figure class="pj-fallback"><figcaption>Split table in the results section.</figcaption></figure></div></article>
    </div>
  </div>
</section>

<!-- ================= method ================= -->
<section class="pj-section pj-section--band" id="method">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">04 · METHOD</span><h2>A perception–action loop with an OBSERVE action</h2><p class="sec-lede"><span data-claim="arxiv-model">VLAlert uses Qwen3-VL-4B as a safety-evidence generator and pools hidden states from structured belief spans</span> to form compact representations for danger estimation and policy prediction.</p></div>
    <figure class="pj-fig reveal"><img src="static/media/fig_pipeline.jpg" alt="{FIGS[0][1]}" width="1500" height="428" loading="lazy" data-zoom><figcaption>{FIGS[0][1]}</figcaption></figure>
    <div class="grid-3">
{figs}
    </div>
  </div>
</section>

<!-- ================= results ================= -->
<section class="pj-section" id="results">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">05 · RESULTS</span><h2>Tables, baseline first</h2></div>
    <div class="tabs reveal">
      <div class="tabs__list" role="tablist" aria-label="Result tables"><button role="tab" id="t-val" aria-selected="true" aria-controls="tab-val">VLAlert-Bench validation</button><button role="tab" id="t-crit" aria-selected="false" aria-controls="tab-crit" tabindex="-1">Transfer · ADAS-TO-Critic</button><button role="tab" id="t-split" aria-selected="false" aria-controls="tab-split" tabindex="-1">Splits</button></div>
      <div class="tabs__panel" id="tab-val" role="tabpanel" aria-labelledby="t-val"><p class="tbl-cap">VLAlert-Bench validation · values as reported in the arXiv v1 abstract</p><div class="tbl-wrap"><table class="tbl tbl--num"><thead><tr><th>Metric</th><th>Reference</th><th>VLAlert</th></tr></thead><tbody>
        <tr><td>DAUS (deployment-oriented utility)</td><td>Open-BADAS <data class="n" value="0.4752" data-src="arxiv-daus">0.4752</data></td><td><b><data class="n" value="0.4878" data-src="arxiv-daus">0.4878</data></b></td></tr>
        <tr><td>AUROC</td><td><data class="n" value="0.610" data-src="arxiv-metrics">0.610</data></td><td><b><data class="n" value="0.689" data-src="arxiv-metrics">0.689</data></b></td></tr>
        <tr><td>AP<sub>tick</sub></td><td><data class="n" value="0.176" data-src="arxiv-metrics">0.176</data></td><td><b><data class="n" value="0.195" data-src="arxiv-metrics">0.195</data></b></td></tr>
        <tr><td>F1<sub>t</sub></td><td><data class="n" value="0.276" data-src="arxiv-metrics">0.276</data></td><td><b><data class="n" value="0.297" data-src="arxiv-metrics">0.297</data></b></td></tr>
        <tr><td>Balanced accuracy</td><td><data class="n" value="0.581" data-src="arxiv-metrics">0.581</data></td><td><b><data class="n" value="0.648" data-src="arxiv-metrics">0.648</data></b></td></tr>
      </tbody></table></div><p class="pj-note">The abstract names Open-BADAS for the DAUS comparison; the other reference values are quoted as the abstract gives them ("from … to …"). Full tables are in the paper.</p></div>
      <div class="tabs__panel" id="tab-crit" role="tabpanel" aria-labelledby="t-crit" hidden><p class="tbl-cap">Transfer to <data class="n" value="221" data-src="arxiv-critic">221</data> held-out ADAS-TO-Critic clips · arXiv v1 abstract</p><div class="tbl-wrap"><table class="tbl tbl--num"><thead><tr><th>Metric</th><th>Reference</th><th>VLAlert</th></tr></thead><tbody>
        <tr><td>R@5s</td><td><data class="n" value="74.2" data-src="arxiv-critic">74.2 %</data></td><td><b><data class="n" value="88.7" data-src="arxiv-critic">88.7 %</data></b></td></tr>
        <tr><td>F1</td><td><data class="n" value="0.585" data-src="arxiv-critic">0.585</data></td><td><b><data class="n" value="0.686" data-src="arxiv-critic">0.686</data></b></td></tr>
      </tbody></table></div></div>
      <div class="tabs__panel" id="tab-split" role="tabpanel" aria-labelledby="t-split" hidden><p class="tbl-cap">VLAlert-Bench splits · Hugging Face dataset card</p><div class="tbl-wrap"><table class="tbl tbl--num"><thead><tr><th>Split</th><th>Videos</th><th>Ticks (1 Hz)</th></tr></thead><tbody>
        {split_rows}
        <tr><td><b>Total</b></td><td><b><data class="n" value="13534" data-src="hf-videos">13,534</data></b></td><td><b><data class="n" value="192892" data-src="hf-ticks">192,892</data></b></td></tr>
      </tbody></table></div></div>
    </div>
    <figure class="pj-fig reveal" style="margin-top:16px"><img src="static/media/fig_valdist.jpg" alt="Label distribution across the validation splits" width="1200" height="657" loading="lazy" data-zoom><figcaption>Label distribution across the validation splits.</figcaption></figure>
    <details class="sources reveal"><summary>Sources &amp; notes</summary><ol data-auto></ol></details>
  </div>
</section>

<!-- ================= data ================= -->
<section class="pj-section pj-section--band" id="data">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">06 · DATA &amp; ACCESS</span><h2>Get the benchmark</h2></div>
    <div class="tiers">
      <div class="tier tier--hi reveal"><span class="badge badge--warn">On request</span><h3>VLAlert-Bench</h3><p>13,534 videos across five splits, 192,892 one-second labelled ticks, per-frame action labels and split manifests; the ADAS-TO-Critic mp4 corpus is hosted directly. <span data-hf="HenryYHW/VLAlert">Gated, manual approval</span>: request access with an institutional email and your intended use.</p><div class="pj-cta"><a class="btn btn--sm btn--primary" href="https://huggingface.co/datasets/HenryYHW/VLAlert" target="_blank" rel="noopener">Request on Hugging Face</a></div><p class="pj-note">License: CC BY 4.0 for the benchmark annotations and manifests; the source videos keep their original datasets' terms.</p></div>
      <div class="tier reveal" style="--i:1"><span class="badge badge--ok">Open</span><h3>Paper</h3><p>Observe Before You Alert: Adaptive Driver Alerting with Vision–Language Models — CoRL 2026; arXiv 2609.08130 (v1, 8 Sep 2026).</p><div class="pj-cta"><a class="btn btn--sm" href="https://arxiv.org/abs/2609.08130" target="_blank" rel="noopener"><span class="arxiv-mark">arXiv</span> Read</a><a class="btn btn--sm" href="#cite">BibTeX</a></div></div>
      <div class="tier reveal" style="--i:2"><span class="badge badge--crit">Not listed</span><h3>Model weights &amp; code</h3><p>No code or checkpoint release is listed on the dataset card as of October 2026. Contact the authors for the policy model.</p></div>
    </div>
  </div>
</section>

<!-- ================= cite ================= -->
<section class="pj-section" id="cite">
  <div class="pj-wrap">
    <div class="sec-head reveal"><span class="sec-num">07 · CITE</span><h2>Read the paper, cite the benchmark</h2></div>
    <div class="bib reveal"><div class="bib__head"><b>BibTeX</b><button class="btn btn--sm" type="button"><span>Copy</span></button></div><pre>@inproceedings{{wang2026vlalert,
  title     = {{Observe Before You Alert: Adaptive Driver Alerting with Vision–Language Models}},
  author    = {{Wang, Yuhang and Li, Lingyao and Zhou, Hao}},
  booktitle = {{Conference on Robot Learning (CoRL)}},
  year      = {{2026}},
  url       = {{https://arxiv.org/abs/2609.08130}}
}}</pre></div>
    <h3 class="sub-head">Related work from the lab</h3>
    <div class="family reveal">
      <a class="fam" href="/projects/adas-to/"><img src="/img/projects/th_adas-to.jpg" alt="" width="620" height="388" loading="lazy"><div><span class="fam__v">Dataset · ITSC 2026</span><h4>ADAS-TO</h4><p>The takeover moment at scale; ADAS-TO-Critic is one of VLAlert-Bench's six sources.</p></div></a>
      <a class="fam" href="/projects/tridrive/"><img src="/img/projects/th_tridrive.jpg" alt="" width="620" height="388" loading="lazy"><div><span class="fam__v">arXiv 2026</span><h4>TriDrive</h4><p>Driver, vehicle and road forecast together — in the car at 5 Hz.</p></div></a>
      <a class="fam" href="/projects/baton/"><img src="/img/projects/th_baton.jpg" alt="" width="620" height="388" loading="lazy"><div><span class="fam__v">Benchmark · arXiv 2026</span><h4>BATON</h4><p>Bidirectional human–automation control transitions on synchronized streams.</p></div></a>
    </div>
  </div>
</section>
</main>

{FOOT_NEW}
<button class="totop" type="button" aria-label="Back to top" hidden><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg></button>'''

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); a = ap.parse_args()
    more = more_table(a.src); data_dir = os.path.join(OUT, "static", "data"); media = os.path.join(OUT, "static", "media"); os.makedirs(data_dir, exist_ok=True)
    for n, _, _, _ in DEMOS:
        for ext in (".mp4", ".jpg"):
            if not os.path.exists(os.path.join(media, n + ext)): raise Fail(f"missing media {n}{ext} — run tools/vlalert_media.sh first")
    dumps = lambda o: json.dumps(o, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    for name, obj in (("sources.json", SOURCES), ("numbers.json", NUMBERS), ("bars_splits.json", BARS)):
        open(os.path.join(data_dir, name), "w", encoding="utf8").write(dumps(obj))
    files = {k: {"path": f"static/data/{k}.json"} for k in ("sources", "numbers", "bars_splits")}
    for k, v in files.items():
        p = os.path.join(OUT, v["path"]); v["sha256"] = sha256_file(p); v["bytes"] = os.path.getsize(p)
    items = []
    for n, t, c, ar in DEMOS:
        vp, pp = os.path.join(media, n + ".mp4"), os.path.join(media, n + ".jpg")
        it = {"id": n, "kind": "clip", "title": t, "files": {"video": f"static/media/{n}.mp4", "poster": f"static/media/{n}.jpg"},
              "bytes": {"video": os.path.getsize(vp), "poster": os.path.getsize(pp)}, "first_view": n == "vlalert_demo9", "duration_s": probe_dur(vp),
              "privacy": {"kind": "road", "source_pixels": True, "manual_review": "ok", "reviewed_by": "yuhang + claude-code frame review 2026-10-19", "reviewed_at": TODAY,
                          "note": "public dashcam research footage used in the paper's demo GIFs; platform watermark, uploader handle/avatar and the recorder's date/VIN strip blacked out (tools/vlalert_media.sh); vehicle plates in moving footage as in the source dataset"},
              "provenance": {"source": f"{n}.gif on the personal project page", "video": {"codec": "h264", "crf": 30, "fps": "10/1"}}}
        it["entry_hash"] = hashlib.sha1(dumps(it).encode()).hexdigest()[:40]; items.append(it)
    for n, c, w, h in FIGS:
        p = os.path.join(media, n + ".jpg")
        it = {"id": n, "kind": "figure", "title": c, "files": {"image": f"static/media/{n}.jpg"}, "bytes": {"image": os.path.getsize(p)}, "first_view": False,
              "privacy": {"kind": "figure", "source_pixels": False, "manual_review": "ok", "reviewed_by": "yuhang", "reviewed_at": TODAY, "note": "paper figure (PNG from the personal page, re-encoded as JPEG)"},
              "provenance": {"source": n.replace("fig_", "vlalert_") + ".png"}}
        it["entry_hash"] = hashlib.sha1(dumps(it).encode()).hexdigest()[:40]; items.append(it)
    used_first = sum(i["bytes"].get("video", 0) + i["bytes"].get("poster", 0) for i in items if i["first_view"])
    man = {"schema": "manifest/1", "page": "vlalert", "generated": TODAY, "pipeline_version": "lab-1",
           "budget": {"first_view_bytes": 3000000, "total_media_bytes": 25000000, "used_first_view": used_first,
                      "used_total": sum(sum(i["bytes"].values()) for i in items)}, "files": files, "items": items}
    open(os.path.join(data_dir, "manifest.json"), "w", encoding="utf8").write(dumps(man))
    stub_txt, stub_path = stub_frontmatter("vlalert")
    if stub_txt:
        stub_txt = re.sub(r"(?m)^  - 'Preprint: .*$", "  - 'Paper: Wang, Li, Zhou. <em>Observe Before You Alert: Adaptive Driver Alerting with Vision–Language Models</em>. Conference on Robot Learning (CoRL 2026). <a href=\"https://arxiv.org/abs/2609.08130\" rel=\"noopener\">arXiv:2609.08130</a>'", stub_txt)
    fm = {"type": "showcase", "kit": True, "proj": "vlalert", "showcase_title": "VLAlert · Observe Before You Alert: Adaptive Driver Alerting with Vision–Language Models",
          "meta_description": "VLAlert casts driver alerting as a per-tick policy over SILENT, OBSERVE and ALERT, and VLAlert-Bench joins six driving-event datasets into one task: 13,534 videos and 192,892 labelled ticks. CoRL 2026.",
          "keywords": "driver alerting, vision-language model, accident anticipation, dashcam, benchmark, SILENT OBSERVE ALERT, ADAS, CoRL 2026",
          "authors": ["Yuhang Wang", "Lingyao Li", "Hao Zhou"], "theme_color": "#03150f",
          "og": {"title": "VLAlert: Observe Before You Alert", "description": "A per-tick benchmark for deciding when a driving system should stay SILENT, OBSERVE or ALERT — 13,534 videos, 192,892 ticks, six sources. CoRL 2026."},
          "twitter": {"title": "VLAlert · Observe Before You Alert", "description": "Adaptive driver alerting with vision–language models: a tri-action policy and a unified per-tick benchmark. CoRL 2026."},
          "image": "static/media/fig_pipeline.jpg", "preload": ["static/media/vlalert_demo9.jpg"],
          "citation": {"title": "Observe Before You Alert: Adaptive Driver Alerting with Vision-Language Models", "authors": ["Wang, Yuhang", "Li, Lingyao", "Zhou, Hao"], "date": "2026", "arxiv": "2609.08130", "conference": "Conference on Robot Learning (CoRL)"},
          "schema": {"type": "ScholarlyArticle", "name": "Observe Before You Alert: Adaptive Driver Alerting with Vision-Language Models",
                     "description": "A vision-language alerting framework that casts warning generation as a tri-action policy over SILENT, OBSERVE, and ALERT, evaluated on VLAlert-Bench, a unified per-tick benchmark.",
                     "datePublished": "2026-09-08", "sameAs": ["https://arxiv.org/abs/2609.08130", "https://huggingface.co/datasets/HenryYHW/VLAlert"], "citation": "https://arxiv.org/abs/2609.08130",
                     "keywords": ["driver alerting", "vision-language models", "accident anticipation", "benchmark"]}}
    summary = re.search(r'(?m)^description:\s*"(.*)"\s*$', stub_txt).group(1) if stub_txt else fm["meta_description"]
    gen = [f"summary: {jdump(summary)}"] + [f"{k}: {jdump(v)}" for k, v in fm.items()]
    front = "---\n" + stub_txt + "\n# ---- generated by tools/build_vlalert.py (hand-built showcase page); the stub fields above are the lab's own ----\n" + "\n".join(gen) + "\n---\n"
    index_out = front + body(more) + "\n"
    hits = scan_forbidden(index_out)
    if hits: raise Fail(f"FORBIDDEN in index.html: {hits[:5]}")
    for root, _, fns in os.walk(os.path.join(OUT, "static", "data")):
        for fn in fns:
            h = scan_forbidden(open(os.path.join(root, fn), encoding="utf8").read())
            if h: raise Fail(f"FORBIDDEN in {fn}: {h[:5]}")
    open(os.path.join(OUT, "index.html"), "w", encoding="utf8").write(index_out)
    n = write_sums(os.path.join(OUT, "static"))
    if stub_path and os.path.exists(stub_path): os.remove(stub_path)
    print(f"vlalert → /projects/vlalert/ · {n} files in SUMS · first view {used_first/1e6:.2f} MB · items {len(items)}")

if __name__ == "__main__": main()
