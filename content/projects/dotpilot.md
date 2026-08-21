---
title: "DoTPilot: an open-source LLM agent framework for driving assistance"
description: "An open-source fork of sunnypilot/openpilot that integrates an LLM-based AI agent into the driving-assistance pipeline, giving generative AI a defined, auditable place to reason about and act on production ADAS."
weight: 4
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  # TODO Hao: add other contributors on this project
artifacts:
  - 'Code: <a href="https://github.com/HaoZhouGT/DoTPilot/tree/llm-agent" rel="noopener">github.com/HaoZhouGT/DoTPilot</a> (llm-agent branch)'
---

## What it is

**DoTPilot** is an open-source driving-assistance stack built on **sunnypilot** — itself a fork of comma.ai's **openpilot** — that supports 300+ production vehicle models. On top of that base, the lab's `llm-agent` branch integrates a large-language-model-based agent directly into the driving pipeline: the agent reads the vehicle's perception and control state and issues structured advisories that plug into openpilot's planner, giving generative AI a defined, auditable interface to a safety-certified ADAS stack rather than a bolt-on demo.

## Why it matters

Most experiments in LLM-assisted driving run in simulation or on a handful of purpose-built research vehicles, because there has been no standardized way for a generative model to both *reason about* and *act on* an everyday car without rewriting its safety-critical control path. Building on sunnypilot/openpilot's existing support for hundreds of vehicle models means the same integration pattern can, in principle, run on any of those cars — turning LLM-driving-agent research from a single-platform exercise into something reproducible across a wide vehicle fleet.

## Connections

DoTPilot is the open-source codebase underpinning the lab's broader push to give generative AI a safe, structured role in vehicle control — the same thesis behind [Scale-CDA](/projects/scale-cda/), which pairs an edge-deployed multimodal LLM with Openpilot planner hooks over a low-cost hardware retrofit. It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.

<!-- TODO Hao: confirm exactly how DoTPilot relates to Scale-CDA (same codebase / earlier stage / parallel effort?), and add a cover figure or architecture diagram. Drop into /static/img/projects/dotpilot/ and reference here. -->
