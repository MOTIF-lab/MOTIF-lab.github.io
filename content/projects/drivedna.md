---
title: "DriveDNA: a naturalistic driving-style dataset and benchmark"
description: "A large-scale multimodal naturalistic driving dataset and benchmark for driving-style identification — over 4,100 drives from 465 drivers across 115 vehicle models, isolating driver-specific behavior from environment and vehicle factors."
weight: 8
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Lingyao Li"
artifacts:
  - 'Paper: Wang, Li, Zhou. <em>DriveDNA: a large-scale multimodal naturalistic driving dataset and benchmark for driving style identification</em>. <a href="https://arxiv.org/abs/2607.23822" rel="noopener">arXiv:2607.23822</a> — see also the <a href="/publications/2026-drivedna-driving-style-dataset/">publication page</a>'
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/drivedna/" rel="noopener">wangyuhang-cmd.github.io/drivedna</a>'
  - 'Code: <a href="https://github.com/WangYuHang-cmd/DriveDNA" rel="noopener">github.com/WangYuHang-cmd/DriveDNA</a>'
  - 'Dataset: <a href="https://huggingface.co/datasets/HenryYHW/DriveDNA" rel="noopener">huggingface.co/datasets/HenryYHW/DriveDNA</a>'
---

## What it is

**DriveDNA** treats driving style as a consistent, driver-specific behavioral pattern in how a vehicle moves under similar conditions — and builds the dataset and benchmark needed to measure it. It spans over **4,100 drives** from **465 drivers** across **115 vehicle models**, with nearly **1,000 hours** of recorded driving, and supports tasks including driver re-identification and behavior prediction.

## Why it matters

Driving-style research has been held back by confounds: without controlling for vehicle and environment, it is difficult to tell whether an observed behavioral difference reflects the driver or the conditions they were driving in. DriveDNA's scale across drivers, vehicles, and drives is what makes it possible to isolate driver-specific style from those confounds instead of assuming it away.

## Connections

DriveDNA extends the lab's driver-behavior modeling work alongside [TriDrive](/projects/tridrive/) and [DriveMotion](/projects/drivemotion/), and draws on the same production-vehicle instrumentation lineage as [OpenLKA](/projects/openlka/). It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Traffic flow theory](/research/traffic-flow-theory/) threads.
