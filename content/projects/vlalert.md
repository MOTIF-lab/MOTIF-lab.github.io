---
title: "VLAlert: vision-language models for adaptive driver alerting"
description: "A vision-language framework and benchmark for adaptive driver alerting — deciding per second whether a driving system should stay silent, observe, or alert, across nearly 193,000 labeled one-second segments."
weight: 10
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Lingyao Li (University of Arizona)"
artifacts:
  - 'Preprint: Wang, Zhou. <em>Bridging human oversight and black-box driver assistance: vision-language models for predictive alerting in lane keeping assist systems</em>. <a href="https://arxiv.org/abs/2505.11535" rel="noopener">arXiv:2505.11535</a> — see also the <a href="/publications/2025-vlm-predictive-alerting-lka/">publication page</a>'
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/vlalert/" rel="noopener">wangyuhang-cmd.github.io/vlalert</a>'
  - 'Dataset: <a href="https://huggingface.co/datasets/HenryYHW/VLAlert" rel="noopener">huggingface.co/datasets/HenryYHW/VLAlert</a>'
  - "Venue: Conference on Robot Learning (CoRL) 2026"
  - "License: CC-BY-4.0"
---

## What it is

**VLAlert** (VLAlert-Bench) is a vision-language framework and a unified per-tick benchmark for adaptive driver alerting: each second, a model looks at the last 8 frames of video and decides whether to stay **silent**, **observe**, or **alert**. The benchmark integrates six driving-event datasets — Nexar Collision, DoTA, DAD, DADA-2000, ADAS-TO-Critic, and a Kaggle accident set — into **13,534 videos** and **192,892 labeled one-second ticks**.

## Why it matters

Most driver-assistance systems treat alerting as binary and reactive: an alert fires once risk crosses a threshold, with no notion of building attention gradually or holding back when a driver is already responding appropriately. VLAlert's three-state framing — and pooling six disparate event datasets into one labeling scheme — makes it possible to train and evaluate alerting policies that escalate the way an attentive human passenger would, rather than defaulting to blunt binary warnings.

## Connections

VLAlert applies the alerting problem that [TriDrive](/projects/tridrive/)'s driver-forecasting work targets from the world-model side, and its underlying event sources overlap with [ADAS-TO](/projects/adas-to/). It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.
