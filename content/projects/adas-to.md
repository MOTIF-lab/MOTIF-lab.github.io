---
title: "ADAS-TO: naturalistic dataset of human takeovers during ADAS engagement"
description: "A large-scale multimodal naturalistic dataset and empirical characterization of over 15,000 real-world driver takeover events, spanning 327 drivers and 22 vehicle brands."
weight: 6
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Yiyao Xu"
  - "Jingran Sun"
artifacts:
  - 'Paper: Wang, Xu, Sun, Zhou. <em>ADAS-TO: a large-scale multimodal naturalistic dataset and empirical characterization of human takeovers during ADAS engagement</em>. <a href="https://arxiv.org/abs/2603.06986" rel="noopener">arXiv:2603.06986</a> — see also the <a href="/publications/2026-adas-to-takeover-dataset/">publication page</a>'
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/adasto/" rel="noopener">wangyuhang-cmd.github.io/adasto</a>'
  - 'Code: <a href="https://github.com/OpenLKA/ADAS-TO" rel="noopener">github.com/OpenLKA/ADAS-TO</a>'
  - 'Dataset: <a href="https://huggingface.co/datasets/HenryYHW/ADAS-TO" rel="noopener">huggingface.co/datasets/HenryYHW/ADAS-TO</a>'
---

## What it is

**ADAS-TO** is a large-scale multimodal naturalistic dataset documenting how drivers actually take back control from ADAS-engaged vehicles — over **15,000 takeover events**, recorded from **327 drivers** across **22 vehicle brands**, with synchronized video and vehicle telemetry for each event.

## Why it matters

Takeover behavior is one of the least-instrumented links in the human–automation chain: most existing datasets come from a small number of research vehicles or simulator studies, which cannot capture how takeover timing and quality vary across the production ADAS systems drivers actually own. ADAS-TO's scale and brand diversity make it possible to empirically characterize takeover performance the way it is encountered in the field, not just in a lab.

## Connections

ADAS-TO shares instrumentation lineage with [OpenLKA](/projects/openlka/) and feeds the same driver-state modeling questions as [TriDrive](/projects/tridrive/), [BATON](/projects/baton/), and [DriveMotion](/projects/drivemotion/). It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.
