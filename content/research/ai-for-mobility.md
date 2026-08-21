---
title: "AI for mobility"
description: "Computer vision and machine learning for traffic monitoring, road hazard detection, and operations support."
weight: 3
---

Modern vision and learning systems extend the reach of traditional traffic monitoring. We develop and evaluate AI tools that turn dash-cam video, roadside cameras, and probe data into operational signals — vehicle counts, incident alerts, pavement and roadside hazard detections — at a fraction of the cost of fixed instrumentation.

Our emphasis is not on novelty in the model architecture alone but on closing the loop with traffic operations: what false-positive rate is tolerable for an alert that triggers a maintenance dispatch? How do edge-device and bandwidth constraints shape what is actually deployable? How do we evaluate detection performance against the messy ground truth available from agencies?

## Featured prototype: Scale-CDA

[**Scale-CDA**](/projects/scale-cda/) is an open-hardware / open-software toolchain that retrofits production cars for generative-AI-assisted cooperative driving automation using under US $1,000 of off-the-shelf parts. An edge-deployed multimodal LLM reads synchronized vision, CAN, and V2X streams and issues structured advisories to verified Openpilot planner hooks — end-to-end decision latency stayed below 60 ms in multi-vehicle road tests, with all inference kept on-board.

## Open-source: DoTPilot

[**DoTPilot**](/projects/dotpilot/) is the lab's open-source driving-assistance codebase — a fork of sunnypilot/openpilot with an LLM-based AI agent integrated directly into the driving pipeline, giving generative AI a defined, auditable interface into a safety-certified ADAS stack across the 300+ vehicle models the base project already supports.

## Selected papers

- **Zhou**, Yuan, Wang, Wen. [Scale-CDA: a scalable prototype to democratize AI-assisted cooperative driving automation (CDA) for production cars](https://arxiv.org/abs/2608.04235). *arXiv preprint*.
- **Zhou**, Laval, A. Zhou, Wang, Wu, Qing, Peeta. [Review of learning-based longitudinal motion planning for autonomous vehicles: implications on traffic congestion](https://journals.sagepub.com/doi/10.1177/03611981211035764). *Transportation Research Record*.
- Chen, Tang, **Zhou**, Cheng. [Extracting topographic data from online sources to generate a digital elevation model for highway preliminary geometric design](https://ascelibrary.org/doi/10.1061/JTEPBS.0000212). *Journal of Transportation Engineering, Part A*.
- Laval, **Zhou**. [Congested urban networks tend to be insensitive to signal settings: implications for learning-based control](https://ieeexplore.ieee.org/abstract/document/9913925). *IEEE Transactions on Intelligent Transportation Systems*.

<!-- TODO Hao: more recent AI-for-mobility papers (dash-cam vision, road hazard detection) — likely a few that haven't propagated to the live site yet. Send the references and I'll add them here and in /publications/. -->

See the full [publications page](/publications/) for the rest.
