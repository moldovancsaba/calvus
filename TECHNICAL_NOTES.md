
# Technical Notes (Modularized)

👇 This file has been modularized as of version 2.0 — Sections below now live in `/documents`:

- [Technical Architecture](technical-architecture.md)
- [Performance Optimizations & Edge Cases](performance-optimizations.md)
- [Security & Scalability](security-scalability.md)

## Quick Index:

- [User Guide (README)](README.md)
- [Technical Architecture](technical-architecture.md)
- [Performance Optimizations](performance-optimizations.md)
- [Security & Scalability](security-scalability.md)
- [Changelog](CHANGELOG.md)

> **TIP:** All docs are in `/documents` for fast reference.

---

_Last updated: 2025-06-14_

<!--
CURRENT DATA MODEL:
- Each triangle's last state is stored as a "snapshot row" (see `CHANGELOG.md`)
- No incremental logs: mesh is always rebuilt from the latest per-triangle snapshots (faster and resilient)
- The base triangle mesh is 18 triangles total
- All app and doc references standardized as of this update
-->
