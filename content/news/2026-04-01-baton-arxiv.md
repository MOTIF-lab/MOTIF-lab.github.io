---
title: "BATON: benchmarking bidirectional human–automation control transitions"
date: 2026-04-01
draft: false
category: "Preprint"
description: "A multimodal benchmark of handovers and takeovers in naturalistic driving-automation routes; the July 2026 v2 reports 781 routes, 173 drivers and 204.9 hours, with a frozen benchmark of 565 routes and 3,593 events."
external:
  - {label: "arXiv:2604.07263 — BATON", outlet: "arXiv", url: "https://arxiv.org/abs/2604.07263"}
  - {label: "BATON on Hugging Face", outlet: "Hugging Face", url: "https://huggingface.co/datasets/HenryYHW/BATON"}
links:
  - {label: "BATON project page", url: "/projects/baton/"}
---

**BATON** (Yuhang Wang, Yiyao Xu, Chaoyun Yang, Lingyao Li, Jingran Sun, Hao Zhou) observes control transitions in both directions on the same synchronized streams — road and cabin video, decoded CAN, radar, the driver monitor and the planner — and scores takeover twice: onset detection, where the driver's inputs are visible, and pre-override anticipation, where they are withheld. The v2 preprint (27 July 2026) covers 781 routes, 173 drivers and 204.9 hours; the frozen benchmark on Hugging Face holds 565 routes and 3,593 events. See the [project page](/projects/baton/).
