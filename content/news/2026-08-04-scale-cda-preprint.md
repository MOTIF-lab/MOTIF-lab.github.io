---
title: "New preprint: Scale-CDA brings AI-assisted cooperative driving to production cars for under $1,000"
date: 2026-08-04
draft: false
category: "Publication"
description: "A new lab preprint introduces Scale-CDA, an open-hardware/open-software toolchain that retrofits ordinary production cars for generative-AI-assisted cooperative driving automation using off-the-shelf parts costing under US $1,000."
external:
  - label: "arXiv:2608.04235 — Scale-CDA: a scalable prototype to democratize AI-assisted cooperative driving automation (CDA) for production cars"
    outlet: "arXiv"
    date: 2026-08-04
    url: "https://arxiv.org/abs/2608.04235"
---

A new preprint from the lab — **Scale-CDA: a scalable prototype to democratize AI-assisted cooperative driving automation (CDA) for production cars**, by Hao Zhou, Shengming Yuan, Yuhang Wang, and Haibin Wen — is now on arXiv.

Cooperative driving automation research has long been gated by cost. Field trials have needed purpose-built instrumented vehicles, which caps most studies at a handful of cars. Scale-CDA takes the opposite approach: build on the community-maintained **OpenDBC** interface (300+ car models) and **Openpilot** Level-2 ADAS, and retrofit an ordinary car with off-the-shelf parts — an edge PC, a webcam, a CAN adapter, and optional LTE/Wi-Fi radios — for **under US $1,000**.

On top of that base, the paper adds a lightweight **MQTT-over-Wi-Fi-6/LTE V2X stack**, an **edge-deployed multimodal LLM** that reads synchronized vision, CAN, and V2X streams through a Model-Context-Protocol bridge, and a library of **meta-action executors** that translate the model's structured JSON advisories into verified Openpilot planner hooks — lane changes, gap management, emergency stops — without touching the safety-certified control core.

Field testing on a 7.5 km loop measured **5.25 ms** mean round-trip latency and link speeds near **100 Mb/s**; in multi-vehicle road tests the full stack held end-to-end decision latency **below 60 ms**, with all inference kept on-board so driving data never leaves the vehicle.

The bills-of-materials, connectivity APIs, and GenAI bridges will be released as open resources. More detail on the [project page](/projects/scale-cda/).
