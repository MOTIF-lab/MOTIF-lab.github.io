---
title: "ADAS-TO dataset released on Hugging Face"
date: 2026-11-24
draft: false
category: "Milestone"
description: "The full ADAS-TO release — 16,446 real-world takeover clips from Level-2 ADAS, 364 drivers, 179 vehicle models — is now available for non-commercial research through the MOTIF Lab Hugging Face organization."
external:
  - {label: "ADAS-TO on Hugging Face", outlet: "Hugging Face", url: "https://huggingface.co/datasets/MOTIF-Lab/ADAS-TO"}
  - {label: "arXiv:2603.06986 — ADAS-TO dataset paper", outlet: "arXiv", url: "https://arxiv.org/abs/2603.06986"}
  - {label: "arXiv:2611.08798 — Driver takeovers and longitudinal responses", outlet: "arXiv", url: "https://arxiv.org/abs/2611.08798"}
links:
  - {label: "ADAS-TO project page", url: "/projects/adas-to/"}
---

The full ADAS-TO dataset is now available through the lab's [Hugging Face organization](https://huggingface.co/datasets/MOTIF-Lab/ADAS-TO). ADAS-TO captures what happens when drivers take control back from production Level-2 driver-assistance systems on real roads.

The release contains 16,446 twenty-second takeover clips from 364 drivers, 179 vehicle models and 2,585 routes. Each clip is centered on the moment ADAS disengages (10 s before, 10 s after) and pairs front-view video with synchronized vehicle state, ADAS state, radar and IMU signals. It also includes scenario labels and a set of 749 manually reviewed safety-critical clips. Driver and route IDs are anonymized, and the signal files contain no GPS coordinates.

The data is free for non-commercial research under CC BY-NC 4.0. To download it, request access on Hugging Face using your institutional (.edu) email; requests are reviewed by hand.

The work is led by Yuhang Wang, with Yiyao Xu, Jingran Sun and Hao Zhou, and the dataset paper has been accepted to IEEE ITSC 2026. If you use ADAS-TO, please cite both papers:

- **ADAS-TO: A Large-Scale Multimodal Naturalistic Dataset and Empirical Characterization of Human Takeovers during ADAS Engagement** (Yuhang Wang, Yiyao Xu, Jingran Sun, Hao Zhou). [arXiv:2603.06986](https://arxiv.org/abs/2603.06986)
- **Driver Takeovers and Longitudinal Responses Analysis from Naturalistic Driving** (Yuhang Wang, Hao Zhou). [arXiv:2611.08798](https://arxiv.org/abs/2611.08798)

```bibtex
@article{wang2026adas,
  title={ADAS-TO: A Large-Scale Multimodal Naturalistic Dataset and Empirical Characterization of Human Takeovers during ADAS Engagement},
  author={Wang, Yuhang and Xu, Yiyao and Sun, Jingran and Zhou, Hao},
  journal={arXiv preprint arXiv:2603.06986},
  year={2026}
}

@article{wang2026driver,
  title={Driver Takeovers and Longitudinal Responses Analysis from Naturalistic Driving},
  author={Wang, Yuhang and Zhou, Hao},
  journal={arXiv preprint arXiv:2611.08798},
  year={2026}
}
```
