---
title: "TriDrive: joint driver, vehicle, and road modeling for human-centered driving"
description: "A real-time world model for the cockpit — a single automation-conditioned transition model that jointly forecasts driver kinematics, vehicle dynamics, and road demands to power more timely, appropriate driver alerts."
weight: 5
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Yuhang Wang"
  - "Jingxin Yang (Stanford University)"
  - "Chuheng Wei (Purdue University)"
  - "Yuechen Guo"
  - "Jinghan Xu (Hunan University)"
  - "Zhao Han"
artifacts:
  - 'Project page: <a href="https://wangyuhang-cmd.github.io/tridrive/" rel="noopener">wangyuhang-cmd.github.io/tridrive</a>'
  - 'Code &amp; models: <a href="https://huggingface.co/HenryYHW/TriDrive" rel="noopener">huggingface.co/HenryYHW/TriDrive</a>'
  - "Status: under review (2026)"
---

## What it is

**TriDrive** is a single, automation-conditioned transition model that forecasts a driver, their vehicle, and the surrounding road together — a world model for the cockpit rather than three separate predictors bolted together. Modality-specific encoders for driver kinematics, vehicle dynamics, and road demand are combined through directed residual connections, letting the model capture how the three interact rather than treating them as independent signals. It is the first system to forecast all three jointly, and it is built to run in real time on in-vehicle hardware (a comma four), not just offline.

## Results

TriDrive sets a new state of the art on the **AIDE benchmark** for driver-kinematics forecasting (48.05 vs. 71.47 All-MPJPE against the prior best) while holding **177 ms p95 latency** on-device. In an on-road study with **14 drivers**, alerts driven by TriDrive's joint forecasts were rated more appropriate and better timed than alerts from baseline systems.

## Why it matters

Most driver-monitoring and alerting systems reason about the driver, the vehicle, and the road as separate streams, which forces alert logic to reconcile inconsistent, asynchronous signals after the fact. TriDrive's joint model gives an alerting system one coherent forecast of where the driver's attention, the vehicle's trajectory, and the road's demands are headed, which is what makes it possible to alert earlier and more selectively — the same problem [VLAlert](/publications/2025-vlm-predictive-alerting-lka/) approaches from the vision-language side.

## Connections

TriDrive shares its driver-behavior modeling lineage with [DriveMotion](/projects/drivemotion/) and [DriveDNA](/projects/drivedna/), and its takeover-relevant driver state connects to [ADAS-TO](/projects/adas-to/) and [BATON](/projects/baton/). It sits in the lab's [AI for mobility](/research/ai-for-mobility/) research thread.
