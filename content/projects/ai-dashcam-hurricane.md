---
title: "AI dashcam for post-hurricane roadway damage assessment"
description: "An AI dashcam that turns any ordinary vehicle into a roadway inspection platform — automatically detecting potholes, flooding, downed trees, and damaged signs so agencies can assess storm damage in hours instead of days."
weight: 2
status: "active"
sponsor: ""           # TODO Hao: confirm sponsor / funding source(s)
role: "PI"
start: ""            # TODO Hao: add project start (YYYY-MM)
end: ""
team:
  - "Hao Zhou (PI)"
  # TODO Hao: add student researchers on this project
partners:
  - "Florida Department of Transportation"
  - "Sarasota County Transportation"
artifacts:
  - 'Media: <a href="https://www.usf.edu/news/2026/new-hurricane-recovery-technology-being-tested-on-florida-roads-during-peak-season.aspx" rel="noopener">USF News — How AI could speed hurricane recovery</a> (Aug 11, 2026)'
  - 'Media: <a href="https://www.fox13news.com/news/usf-researchers-test-ai-dashcam-track-hurricane-road-damage" rel="noopener">FOX 13 Tampa Bay — USF researchers test AI dashcam to track hurricane road damage</a> (Aug 14, 2026)'
  - 'Code: open-source release planned — TODO Hao: link the repo under <a href="https://github.com/MOTIF-Lab" rel="noopener">github.com/MOTIF-Lab</a> when public'
---

## What it is

An **AI dashcam** that turns an ordinary vehicle into a roadway damage inspection platform. As the vehicle drives, the system records and analyzes the forward view in place, automatically identifying **potholes, flooding, fallen trees, and damaged signage**, generating inspection reports, and building a searchable visual record of the corridor — with no manual data entry by the driver.

The software runs on any vehicle from model year **2015 or newer**, so an agency can deploy it across a fleet it already owns rather than procuring specialized survey equipment. It will be released **open source** so counties across Florida can run it on their own municipal fleets.

## Why it matters

The project came out of the recovery from **Hurricanes Helene and Milton**. Working with the Florida Department of Transportation and Sarasota County afterward surfaced a constraint that no amount of modeling fixes: the bottleneck in post-storm recovery is rarely knowing *what* to repair, it is having enough trained people available to go out and look. Damage assessment is slow, labor-intensive, and performed on roads that are still hazardous.

Compressing a roadway damage sweep from roughly **three days to six to eight hours** changes the recovery timeline directly — repair crews and materials can be dispatched to the right places on the first day rather than the third, and fewer staff hours are spent driving hazardous corridors to produce the picture.

## Companion tools

The dashcam is one of three AI tools the lab is building with Florida transportation agencies for storm response:

1. **AI dashcam** — automated damage detection, reporting, and visual database (this project).
2. **Routing and scheduling optimization** — sequencing traffic signal restoration and roadway inspections so crews are dispatched in the order that restores mobility fastest.
3. **Social media analysis** — surfacing and prioritizing citizen reports of flooded streets, blocked routes, and other transportation disruptions as a real-time complement to agency field data.

## Status

Field testing is under way through **fall 2026**, deliberately timed to peak hurricane season and to heavy rainfall events that stress the detection models under the conditions that matter. After testing concludes, the lab will bring the system to state and county transportation agencies.

## Connections

The damage inspection and reporting pipeline runs on [**DoTPilot**](/projects/dotpilot/), the lab's open-source in-vehicle platform for transportation agency fleets — so the same installation that produces storm damage reports also serves the agency's daily operations, including work zone safety warnings and traffic incident management.

This project sits in the lab's [AI for mobility](/research/ai-for-mobility/) thread and builds on the affordable-dashcam, open-source-software approach developed in the lab's [AI-CDA4All](/publications/2025-ai-cda4all/) work.

<!-- TODO Hao: add a cover figure — e.g. a dashcam detection frame (pothole/flooding/downed tree bounding boxes) or the in-vehicle rig. Drop into /static/img/projects/ai-dashcam-hurricane/ and reference here. -->
