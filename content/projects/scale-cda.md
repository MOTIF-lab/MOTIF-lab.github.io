---
title: "Scale-CDA: democratizing AI-assisted cooperative driving automation for production cars"
description: "An open-hardware, open-software toolchain that retrofits ordinary production cars for generative-AI-assisted cooperative driving automation with under US $1,000 of off-the-shelf parts."
weight: 3
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  - "Shengming Yuan"
  - "Yuhang Wang"
  - "Haibin Wen"      # TODO Hao: confirm affiliation / role for the team list
artifacts:
  - 'Paper: Zhou, Yuan, Wang, Wen. <em>Scale-CDA: a scalable prototype to democratize AI-assisted cooperative driving automation (CDA) for production cars</em>. <a href="https://arxiv.org/abs/2608.04235" rel="noopener">arXiv:2608.04235</a> (Aug 2026)'
  - 'Hardware: bill-of-materials, connectivity APIs, and GenAI bridges released as open resources — TODO Hao: link the repo under <a href="https://github.com/MOTIF-Lab" rel="noopener">github.com/MOTIF-Lab</a> when public'
---

## What it is

**Scale-CDA** is an open-hardware / open-software toolchain that turns an ordinary production car into a working platform for **generative-AI-assisted cooperative driving automation (CDA)**. It is built on two community-maintained foundations — the **OpenDBC** interface, which covers 300+ car models, and **Openpilot** Level-2 ADAS — so retrofitting is plug-and-play using off-the-shelf parts: an edge PC, a webcam, a CAN adapter, and optional LTE / Wi-Fi radios, for **under US $1,000** total.

The stack has three layers:

- **Connectivity.** A lightweight vehicle-to-everything (V2X) stack running MQTT over Wi-Fi 6 / LTE provides bidirectional messaging between vehicles and infrastructure.
- **Intelligence.** An edge-deployed **multimodal large language model** ingests synchronized vision, CAN, and V2X streams through a Model-Context-Protocol (MCP) bridge, then emits structured JSON advisories and motion primitives. Inference stays on-board, so driving data never leaves the vehicle.
- **Actuation.** A library of meta-action executors translates those high-level commands into verified Openpilot planner hooks — lane changes, gap management, emergency stops — **without modifying the safety-certified core**.

## Field results

Testing on a **7.5 km loop** measured mean round-trip latency of **5.25 ms** and link speeds near **100 Mb/s**, which supports Wi-Fi 6 as a viable low-cost medium for non-safety-critical CDA messaging. In multi-vehicle road tests, the full perception → reasoning → action stack held end-to-end decision latency **below 60 ms**.

## Why it matters

CDA research has been gated by two practical barriers rather than theoretical ones. First, the hardware: cooperative-driving field trials have historically required instrumented research vehicles, which caps experiments at a handful of cars and puts large-scale deployment studies out of reach for most agencies and labs. Second, the interface: there has been no standardized way for a generative AI model to both *reason about* and *act on* an everyday vehicle without rewriting its safety-critical control path.

Scale-CDA targets both. Cheap, interoperable retrofits make fleet-scale field trials tractable, and the MCP bridge plus meta-action executors give GenAI a defined, auditable place to intervene. Releasing the bills-of-materials, connectivity APIs, and AI bridges openly gives transportation agencies and researchers a blueprint they can rebuild rather than a demo they can only read about.

## Connections

Scale-CDA extends the affordable-hardware, open-source-software approach the lab developed in [AI-CDA4All](/publications/2025-ai-cda4all/), and shares its instrumentation lineage with the [OpenLKA](/projects/openlka/) data-collection work. It sits at the intersection of the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.

<!-- TODO Hao: add a cover figure — e.g. the retrofit rig (edge PC + webcam + CAN adapter), the test-loop map, or a multi-vehicle field-test photo. Drop into /static/img/projects/scale-cda/ and reference here. -->
