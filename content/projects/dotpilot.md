---
title: "DoTPilot: an in-vehicle AI platform for transportation agency fleets"
description: "An open-source in-vehicle system that turns an agency's existing fleet into a two-way link with the traffic management center — collecting roadway condition data on the uplink and delivering agency advisories to drivers on the downlink, for both daily operations and disaster response."
weight: 4
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""             # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  # TODO Hao: add other contributors on this project
partners: []          # TODO Hao: list agency partners for DoTPilot specifically (FDOT? Sarasota County?)
artifacts:
  - 'Code: <a href="https://github.com/HaoZhouGT/DoTPilot/tree/llm-agent" rel="noopener">github.com/HaoZhouGT/DoTPilot</a> (llm-agent branch)'
---

## What it is

**DoTPilot** is an open-source in-vehicle software system built for **state and county transportation agencies** — designed to run on the fleet vehicles an agency already owns and operates. It turns each of those vehicles into a two-way link with the agency:

- **Uplink — the vehicle reports the road.** An AI dashcam continuously analyzes the forward view, detecting roadway conditions of operational interest and generating structured reports without any manual data entry by the driver.
- **Downlink — the agency advises the driver.** DoTPilot ingests agency data feeds — travel advisories, work zone locations, incident and closure reports — and delivers the relevant ones to the driver as timely, in-vehicle warnings.

The same platform serves an agency's **daily operations** and its **disaster response**, which is deliberate: a system that only comes out during a hurricane is a system nobody is trained on when the hurricane arrives.

<figure>
  <img src="/img/projects/dotpilot/road-inspection-mode.jpg"
       alt="A windshield-mounted DoTPilot unit running in Road Inspection Mode. The display shows the forward camera view of a residential street overlaid with a maintenance finding card reading &quot;DRAINAGE ISSUE — location: near field, right, curb/gutter — detail: standing water along the right curb in the near field,&quot; alongside the current speed and posted speed limit."
       loading="lazy">
  <figcaption><strong>DoTPilot running in Road Inspection Mode.</strong> The on-board agent classifies what it sees, localizes it relative to the vehicle, and writes a plain-language description — here, standing water along the right curb flagged as a drainage issue. Findings like this accumulate into the inspection report and searchable visual record the agency receives.</figcaption>
</figure>

Each finding is emitted as a **structured record** — finding type, location relative to the roadway, and a written description — rather than as raw video an analyst has to review afterward. That is what makes the output usable directly by an agency's maintenance and reporting workflows.

## Applications

**Post-storm roadway damage inspection and reporting** *(in development).* An automated pipeline that detects potholes, flooding, downed trees, and damaged signage as maintenance and inspection vehicles drive their routes, then compiles inspection reports and a searchable visual record of each corridor for the agency. This is the lab's [AI dashcam storm-recovery work](/projects/ai-dashcam-hurricane/), which compresses a roadway damage sweep from roughly three days to six to eight hours.

**Work zone safety warnings** *(in development).* Pulling active work zone data from agency feeds and pushing advance, location-aware warnings to drivers approaching a work zone — including the agency's own crews and contractors, who are the people most exposed to work zone crashes.

**Traffic incident management** *(in development).* Relaying incident, closure, and detour information from the traffic management center to vehicles in the affected area, and returning what the vehicle observes at the scene, so the agency's operating picture and the driver's picture stay in sync.

## Why it matters

Transportation agencies face a structural mismatch: they are responsible for continuous awareness of thousands of centerline miles, but their instrumentation is concentrated at fixed points — signals, detectors, roadside cameras — on a small fraction of the network. Filling the gaps means either procuring specialized survey equipment or sending staff out to look, and after a major storm, staffing is exactly the constraint that binds.

Meanwhile, every agency already operates a fleet that drives those roads every day. DoTPilot's premise is that this fleet is the most underused sensing and communication asset an agency has. Making it useful should not require new vehicles, new procurement, or new staff time — it should require software the agency can install on what it already owns, and can inspect and modify because it is open source.

The two-way design matters as much as the sensing. Agencies already publish advisories, work zone data, and incident feeds; those feeds mostly reach drivers through channels drivers are not supposed to be looking at while driving. Delivering them through an in-vehicle system closes that loop, and doing so on the same platform that reports conditions back means the agency's field picture and its driver-facing messaging are built from one system rather than two.

## Technical foundation

DoTPilot builds on **sunnypilot** — a fork of comma.ai's **openpilot** — which supports **300+ production vehicle models** through the community-maintained OpenDBC interface. That base is what makes fleet deployment tractable: agencies run mixed fleets, and the platform has to work across them rather than on one instrumented test vehicle.

The lab's `llm-agent` branch integrates an **LLM-based agent** into that pipeline. The agent reads the vehicle's synchronized perception and control state alongside the ingested agency data, and issues **structured advisories** through defined interfaces — so generative AI has an auditable place to reason and act without modifying the safety-certified control core. Inference runs **on-board**, so driving data stays in the vehicle.

## Connections

DoTPilot is the agency-facing platform built on the technical approach the lab developed in [Scale-CDA](/projects/scale-cda/) — an edge-deployed multimodal LLM reasoning over vision, CAN, and connectivity streams and acting through verified planner hooks — and in [AI-CDA4All](/publications/2025-ai-cda4all/) before it. Its instrumentation lineage runs back to the [OpenLKA](/projects/openlka/) data-collection work. It sits in the lab's [AI for mobility](/research/ai-for-mobility/) and [Vehicle technologies](/research/vehicle-technologies/) threads.

<!-- TODO Hao: an architecture diagram of the two-way agency↔fleet flow would complement the Road Inspection Mode photo well. Drop additional figures into /static/img/projects/dotpilot/. -->
