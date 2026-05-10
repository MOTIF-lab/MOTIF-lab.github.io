---
title: "OpenLKA: open dataset of lane keeping assist from market autonomous vehicles"
description: "The first open dataset benchmarking production lane-keeping-assist (LKA) behavior across multiple market vehicles, with synchronized CAN, video, and perception data."
weight: 1
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: "2024-05"
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Abdulaziz Alhuraish"
  - "Shengming Yuan"
  - "Shuyi Wang"
artifacts:
  - 'Paper: Wang, Alhuraish, Yuan, Wang, Zhou. <em>OpenLKA: an open dataset of lane keeping assist from market autonomous vehicles</em>. <a href="https://arxiv.org/abs/2501.03287" rel="noopener">arXiv:2501.03287</a>'
  - 'Lab GitHub: <a href="https://github.com/MOTIF-Lab" rel="noopener">github.com/MOTIF-Lab</a> (TODO: link directly to OpenLKA repo when ready)'
---

## What it is

**OpenLKA** is the first open benchmark dataset of lane-keeping-assist (LKA) behavior collected from a wide range of *production* autonomous vehicles in real driving. Released in January 2025, it pairs CAN-bus signals with synchronized forward-facing video and lane-perception output, captured across multiple market vehicles under varied roadway and weather conditions in the Tampa, Florida region.

## Why it matters

Lane-keeping assist is one of the most widely deployed ADAS features, but its real-world performance is opaque: most public benchmarks are built on simulated environments or single-vehicle test fleets, and the behavior of production LKA systems differs widely between manufacturers. Without an open, multi-vehicle dataset, researchers cannot calibrate microsimulations of mixed-autonomy traffic, evaluate disengagement risk, or model the variance in LKA-equipped vehicle behavior that capacity and safety analyses now have to contend with.

OpenLKA addresses this gap by capturing **how production vehicles actually behave** — not how a single test platform behaves — with the supporting signals (CAN, video, perception) needed to reverse-engineer LKA decision logic.

## Data collection

The dataset was built during the lab's summer 2024 data-collection campaign, which used rental cars to systematically sample a wide range of market vehicles. The same campaign also produced two companion datasets that build on shared instrumentation:

- A **CAN-level vehicle control dynamics** dataset
- An **EV regenerative braking** dataset

## Connections

This project is a flagship release for the lab's [Vehicle technologies](/research/vehicle-technologies/) thread. It also feeds back into the [Traffic flow theory](/research/traffic-flow-theory/) thread — production-LKA car-following data is precisely what calibrating mixed-autonomy fundamental diagrams requires.

<!-- TODO Hao: add cover figure (e.g. data-collection rig, sensor diagram, or a representative CAN+video stack) — drop into /static/img/projects/openlka/ and reference here. -->
