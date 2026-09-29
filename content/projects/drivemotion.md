---
title: "DriveMotion: a benchmark for driver motion forecasting"
description: "A large-scale, multi-source benchmark for driver body-motion sequence modeling and forecasting — 400 hours of in-cabin skeleton motion data from 360 drivers, standardized across heterogeneous monitoring sources with privacy protections."
weight: 9
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Chuheng Wei (Purdue University)"
  - "Jingxin Yang (Stanford University)"
  - "Xishun Liao (University of Central Florida)"
artifacts:
  - 'Paper: Wang, Wei, Yang, Liao, Zhou. <em>DriveMotion: a large-scale multi-source benchmark for driver motion sequence modeling and forecasting</em>. <a href="https://arxiv.org/abs/2609.08117" rel="noopener">arXiv:2609.08117</a>'
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/drivemotion/" rel="noopener">wangyuhang-cmd.github.io/drivemotion</a>'
  - 'Dataset: <a href="https://huggingface.co/datasets/HenryYHW/DriveMotion" rel="noopener">huggingface.co/datasets/HenryYHW/DriveMotion</a>'
  - "License: CC BY 4.0 (skeleton artifacts and code)"
---

## What it is

**DriveMotion** standardizes heterogeneous in-cabin monitoring sources into a single skeleton-motion representation for forecasting driver body movements. The benchmark combines the [BATON](/projects/baton/) fleet, a web corpus, and AIDE sources into **400 hours** of motion data at 10 Hz with **133 keypoints per frame** across **9,010 sequences** from **360 drivers** — synchronized with vehicle telemetry and camera context — and defines a forecasting task: observe 8 seconds of past motion, predict the next 4.

## Why it matters

In-cabin monitoring data comes from incompatible sources — different sensors, different skeleton conventions, different sampling rates — which has made it hard to pool data across studies or compare motion-forecasting models on common ground. DriveMotion's unified representation and privacy-preserving release turn that fragmented data into a reusable benchmark, with **680,082 forecasting windows** available for training and evaluation.

## Connections

DriveMotion draws on the same fleet instrumentation as [BATON](/projects/baton/) and complements [TriDrive](/projects/tridrive/)'s joint driver-vehicle-road forecasting and [DriveDNA](/projects/drivedna/)'s driving-style work. It sits in the lab's [AI for mobility](/research/ai-for-mobility/) research thread.
