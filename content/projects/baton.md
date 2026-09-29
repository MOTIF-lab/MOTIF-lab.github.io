---
title: "BATON: bidirectional automation transition benchmark"
description: "A multimodal benchmark for bidirectional automation-transition observation in naturalistic driving — 136.6 hours of driving from 127 drivers across 380 routes, capturing both handoffs to and takeovers from automation."
weight: 7
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Yiyao Xu"
  - "C. Yang"
  - "L. Li"
  - "Jingran Sun"
artifacts:
  - 'Paper: Wang, Xu, Yang, Li, Sun, Zhou. <em>BATON: a multimodal benchmark for bidirectional automation transition observation in naturalistic driving</em>. <a href="https://arxiv.org/abs/2604.07263" rel="noopener">arXiv:2604.07263</a> — see also the <a href="/publications/2026-baton-bidirectional-automation-transition/">publication page</a>'
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/baton/" rel="noopener">wangyuhang-cmd.github.io/baton</a>'
  - 'Code: <a href="https://github.com/OpenLKA/BATON" rel="noopener">github.com/OpenLKA/BATON</a>'
  - 'Dataset: <a href="https://huggingface.co/datasets/HenryYHW/BATON" rel="noopener">huggingface.co/datasets/HenryYHW/BATON</a>'
---

## What it is

**BATON** is a multimodal benchmark that observes the full loop of human–automation control transitions — both directions, not just takeovers. It draws on **136.6 hours** of naturalistic driving from **127 drivers** across **380 routes**, with multiple synchronized sensor streams captured throughout each transition.

## Why it matters

Prior work on automation transitions has focused almost entirely on the takeover direction — the moment a driver must retake control. BATON's bidirectional framing captures the handoff *into* automation as well, which matters because how a driver disengages shapes how ready they are to re-engage. That symmetry is what makes BATON useful as a shared benchmark rather than a single-purpose dataset.

## Connections

BATON is one of the fleet sources behind [DriveMotion](/projects/drivemotion/)'s in-cabin motion corpus, and its transition events complement [ADAS-TO](/projects/adas-to/) and [TriDrive](/projects/tridrive/)'s driver-state forecasting. It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.
