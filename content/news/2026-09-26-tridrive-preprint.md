---
title: "TriDrive: a real-time cockpit world model, now on arXiv"
date: 2026-09-26
draft: false
category: "Preprint"
description: "TriDrive jointly forecasts driver kinematics, vehicle dynamics and road demands from one automation-conditioned transition model, runs at 5 Hz on a comma four, and was validated in a 14-participant on-road study."
external:
  - {label: "arXiv:2609.33000 — TriDrive", outlet: "arXiv", url: "https://arxiv.org/abs/2609.33000"}
  - {label: "Code & model on Hugging Face", outlet: "Hugging Face", url: "https://huggingface.co/HenryYHW/TriDrive"}
links:
  - {label: "TriDrive project page", url: "/projects/tridrive/"}
---

**TriDrive: Joint Driver, Vehicle, and Road Modeling for Forecasting and Driver Monitoring** (Yuhang Wang, Jingxin Yang, Chuheng Wei, Yuechen Guo, Jinghan Xu, Zhao Han, Hao Zhou) is on arXiv. One transition model forecasts the driver, the vehicle and the road together; it reaches 48.05 All-MPJPE on the AIDE driver-kinematics benchmark (versus 71.47 for the previous best), runs with 177 ms p95 latency on a comma four with an external GPU, and its warnings were rated more appropriate and more timely by 14 drivers in an on-road study. Explore the three-stream forecast on the [project page](/projects/tridrive/).
