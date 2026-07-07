# Camera Network Documentation
## Purpose of This Site

This site documents a multi-site camera system built on Ubiquiti UniFi hardware (Dream Machines, UniFi Protect, and associated wired/wireless cameras), and the API layer built on top of it for research use.

The documentation is split into two tracks, aimed at two different audiences:

  - **[System Administration Guide](admin/index.md)** — for whoever  inherits, maintains, or expands this system next. Covers network  topology, hardware inventory, console configuration, adoption  procedures, and operational maintenance.
  - **[Research API Guide](api/index.md)** — for grad students and  researchers who need to pull video, snapshots, or metadata from  cameras programmatically. Covers authentication, direct API calls to individual camera consoles, available endpoints, and example  code.
 
If you only want to *use* the cameras for a research project, start with the Research API Guide. If you need to understand *how the system is built*, start with the System Administration Guide.

---

## Project Background

!!! note "Status: Early / In Progress"

This system was inherited from a prior project and is being actively documented and reorganized. Sections marked **[TBD]** are placeholders pending completion of the discovery phase.

This deployment consists of:

- Two Ubiquiti Dream Machines (**[TBD: models/roles]**), each potentially running its own independent UniFi Protect instance
- A mix of wired and wireless UniFi cameras (**[TBD: models,  counts]**), possibly along with third-party wireless cameras
- Multiple network segments (**[TBD: VLAN/topology details]**)
 
The goal of the current effort is to:

1. Inventory and document the existing hardware and network topology
2. Decide on a consolidation vs. federation strategy for the two Protect consoles
3. Establish a stable, documented API layer for programmatic access to camera feeds and recorded footage
4. Produce documentation sufficient for ongoing system maintenance and independent research use

---

## Guiding Principles

This project favors approaches that are **sustainable, open, andlow-friction to hand off**, specifically:

- **Prefer official, supported interfaces** (Ubiquiti's local Protect  API) over reverse-engineered or fragile workarounds, where  possible.
- **Prefer open-source tooling** (e.g., the `uiprotect` Python  library) over custom low-level HTTP handling, to reduce long-term  maintenance burden.
- **Document as we go.** Every completed step in discovery, architecture decisions, or integration work should produce a corresponding documentation page — not be reconstructed after the  fact.
- **Design for handoff.** Assume the next person (system  administrator or researcher) has no prior context and needs to be  able to reconstruct decisions from the documentation alone.

---

## System Overview (High Level)

```
[Placeholder architecture diagram — to be completed after Discovery Phase using Mermaidjs]
Dream Machine A (site/network ??)        Dream Machine B (site/network ??)
     |-- Protect Console A                     |-- Protect Console B
     |     |-- Camera 1 (wired)                |     |-- Camera N (wired)
     |     |-- Camera 2 (wireless)             |     |-- Camera N+1 (wireless)
     |
  [ Researcher / API client tier ]
     |-- Queries Console A + Console B directly, per-camera
```

Each Dream Machine's Protect console is treated as an independent API endpoint. Researchers connecting to individual cameras will need to  know which console manages the camera(s) they're interested in — seethe [Camera Inventory](admin/inventory.md) page once available.

---

## Document Conventions

- **[TBD]** — marks a placeholder pending further work
- Code blocks show real, tested commands/API calls where possible;  untested or planned commands are marked `# planned, untested`
- Network diagrams will be added as SVG/PNG assets under  `docs/assets/diagrams/` as they're finalized

---

## Site Map

- [System Administration Guide](admin/index.md)
- Hardware Inventory *(pending)*
- Network Topology *(pending)*
- Console Configuration & Adoption *(pending)*
- Maintenance Procedures *(pending)*
- [Research API Guide](api/index.md) 
- Authentication & API Keys *(pending)* 
- Camera Inventory & Lookup *(pending)* 
- Live Streams & Snapshots *(pending)*
- Downloading Recorded Footage *(pending)*
- Example Scripts *(pending)*
- [Project Log / Decisions](log/index.md) *(pending)*

---
*Last updated: [TBD — set on commit]*