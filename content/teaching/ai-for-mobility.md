---
title: "AI for Mobility"
code: "TTE 6XXX"
weight: 10
level: "Graduate"
semester: "Tentative — Fall 2026 / Spring 2027"
credits: 3
format: "Lectures + hands-on labs"
instructor: "Hao Zhou"
prereqs: "Working knowledge of Python; introductory transportation engineering or willingness to ramp up quickly"
audience: "Graduate students in transportation, civil, computer, or electrical engineering. Advanced undergraduates by permission."
tagline: "Foundation models, AI agents, and AI-enabled sensors applied end-to-end to transportation problems — from the dash-cam to the digital twin."
status: "Draft syllabus — content is evolving and will be refined before the course is offered."
description: "A graduate course on applying contemporary AI — foundation models, agents, embeddings, and AI-enabled sensors — to real transportation engineering problems. Heavy emphasis on labs using open hardware (dash-cams, edge computers) and open software (openpilot, SUMO, CARLA, Claude Code)."
---

## Course overview

AI is now a working tool for transportation researchers and practitioners, not a research curiosity. This course teaches graduate students how to **apply foundation models, AI agents, and AI-enabled sensors to mobility problems** — and how to be honest about where these tools fail.

The course is heavy on labs. By the end of the semester students will have used commercial driver-assist datasets (OpenLKA), customized openpilot longitudinal control with their own car-following logic, instrumented a dash-cam with an edge AI computer, simulated a corridor in SUMO with an AI-built scenario, and run an auto-research workflow on a transportation problem of their choice.

Three threads run through every module:

1. **Real artifacts.** Every lab produces something runnable, deployable, or measurable — not a slide deck.
2. **Domain rigor.** AI techniques are evaluated against the traffic flow theory, vehicle dynamics, and human factors literature that defines what "good" means in mobility.
3. **Honest limits.** Each module ends with a short discussion of where the tool breaks, what it cannot do, and what the open research questions are.

## Learning outcomes

By the end of the course, students will be able to:

- Explain how foundation models, embeddings, and agents work at a level sufficient to choose the right tool for a transportation problem.
- Build context-engineered prompts, retrieval pipelines, and agent harnesses tailored to mobility data and workflows.
- Instrument a vehicle or roadside sensor with AI-enabled hardware and reason about its data quality, latency, and edge-case failure modes.
- Modify production driver-assist software (openpilot) to integrate domain knowledge from car-following and lane-changing theory.
- Use AI to accelerate transportation simulation, crash reconstruction, and digital-twin workflows — and critique the resulting artifacts against ground truth.

## Modules

### Module 1 — AI fundamentals

How modern AI actually works, with just enough depth to make later labs meaningful.

- **What AI is and how foundation models are trained**
  - Neural networks and how they learn (gradient descent in plain English)
  - Embeddings and representation learning
  - Transformers and large language models
  - World models — what they are, why mobility cares
- **How to prompt AI**
  - Context engineering and chain-of-thought
  - Mobility-specific RAG (retrieval-augmented generation)
  - Harness engineering and AI agents

### Module 2 — AI tools for mobility

Vibe coding, agents, and personal knowledge systems applied to a transportation engineer's actual workflow.

- **Vibe coding for mobility software**
  - **Lab.** Claude Code for SUMO customization
  - **Lab.** Codex / Claude for openpilot personalization
- **Agentic AI in transportation**
  - **Lab.** OpenCLAW and Hermes
- **Building mobility skills for AI**
  - **Lab.** Distill traffic flow theories into reusable skills
  - **Lab.** Encode transportation-agency professional skills
- **Building a mobility wiki as your second brain (Obsidian)**
  - **Lab.** Build an Obsidian vault of mobility knowledge for AI
  - How AI performance changes when given a domain knowledge base
- **Auto-research of mobility issues**
  - Designing an auto-research workflow
  - **Lab.** Auto-research a mobility problem of your choice
  - Gaps, limitations, and opportunities of the auto-research paradigm

### Module 3 — AI sensors for mobility

Cheap hardware, big implications. How dash-cams, pole cameras, RF, and lidar become AI sensors.

- **AI cameras**
  - Vehicle dash-cams for roadway inspection
  - Pole-mounted cameras for crash-precursor detection
  - **Lab.** Raspberry Pi and portable cameras
  - **Lab.** AI edge computers (Jetson Orin, Orin Nano) paired with dash-cams
  - **Lab.** Can AI reliably distinguish normal pedestrian behavior from dangerous jaywalking and railway trespassing?
- **WiFi and Bluetooth**
  - **Lab.** Sensing motion and occupancy from WiFi alone
- **Radar and lidar**
  - **Lab.** Reconstructing surrounding vehicles from radar streams
  - **Lab.** Lidar point clouds for scene reconstruction

### Module 4 — AI for mobility data collection and analysis

Putting AI on the unglamorous but high-impact data side of transportation safety.

- **AI for safety data collection and analysis**
  - AI to draft crash reports
  - AI to generate forensic crash video from written reports

### Module 5 — Connectivity and C-V2X

How vehicle and infrastructure connectivity actually works, where it's deployed, and what it can do for traffic.

- **Connectivity hardware and how it works**
- **Connectivity experiments**
  - Cellular connectivity measurement among students in class
  - WiFi connectivity testing across the USF campus
- **Connectivity practice and safety implications**
  - U.S. and Florida deployment landscape
- **Using connectivity for congestion mitigation**
  - Customized traveler advisories from F511 and WZDX feeds

### Module 6 — Autonomous driving

The largest module — production-grade ADAS and AV systems opened up, instrumented, and modified.

- **Longitudinal control**
  - Longitudinal control by model-predictive control (MPC)
  - End-to-end longitudinal control experiments with openpilot
- **Lane-keeping assist (LKA)**
  - Lane line detection with OpenLane and openpilot
  - Real-world LKA data and the performance gaps it reveals
  - Building a complementary LKA alert system
- **Next-generation data collection from production vehicles**
  - CAN-bus telematics
  - Processing radar streams
  - Energy data collection
- **Full self-driving (FSD)**
  - Data, issues, and research gaps in FSD and Waymo
  - Driver exploitation of AVs and risk compensation
- **Integrating mobility domain knowledge into AVs**
  - **Lab.** Customized car-following and lane-changing inside openpilot
  - **Lab.** Integrate your own AI chatbot into openpilot

### Module 7 — Advanced traffic simulation and digital twins

What today's simulation tools can and cannot do, and how AI fills the gap.

- **Recent traffic simulation tools**
  - Flaws, limitations, and AI remedies
  - Micro / meso / macro tools and when to use each
  - Integrated infrastructure simulation for disaster decision-making
- **Crash reconstruction with AI**
  - AI for roadway feature extraction
  - Using crash reports to generate forensic video
- **Transportation digital twins — concepts and state of the art**
  - Sensors, data, and applications
  - **Lab.** SUMO + CARLA digital twin
  - **Lab.** openpilot + OpenDRIVE integration

### Module 8 — Electric vehicles *(backup / elective content)*

Drawn on if pace allows, or offered as project topics.

- EV unique kinematics from real-world evidence
- Implications of EV characteristics for safety and efficiency
  - Regenerative braking and one-pedal driving
  - Rear-end collision risk and traffic stability concerns
- Integrating EVs and AVs for enhanced mobility
  - Leveraging EV agility for traffic-beneficial maneuvering
  - System-level impact on energy and policy

### Module 9 — Advanced air mobility *(survey)*

A short look forward at the next mode.

- eVTOL technologies
- Total mobility and the integration of multiple transportation modes

## Assessment *(planned, subject to revision)*

- Lab notebooks and runnable artifacts — **50%**
- A semester research/build project of the student's choosing, scoped with the instructor — **30%**
- Two short take-home reflections (one mid-semester, one final) on where AI helped, where it failed, and what to do about it — **20%**

There are no traditional exams. Every assessment results in something the student can put on a CV or in a portfolio.

## Tooling and hardware

Students will use a mix of:

- **Software.** Python, openpilot, SUMO, CARLA, Claude Code, Obsidian, RAG / agent frameworks.
- **Hardware (lab loaner pool).** Raspberry Pi, NVIDIA Jetson Orin / Orin Nano, dash-cams, comma3X for openpilot, USRP / SDR for WiFi sensing, lidar and radar evaluation kits.
- **Vehicles.** MOTIF lab instrumented vehicles for select on-road labs.

## Course philosophy

This is a course about **using AI honestly to do better transportation engineering**. We will not treat AI as a black-box oracle, and we will not treat traditional traffic flow theory as obsolete. The course is built on the premise that domain knowledge plus modern AI tools, applied with discipline, produces better mobility outcomes than either one alone — and the labs are designed to let students prove that to themselves.

---

*This page is a working draft of the syllabus. Topics, labs, and assessment weights will be revised as the course is finalized. Questions or suggestions are welcome — please email Hao.*
