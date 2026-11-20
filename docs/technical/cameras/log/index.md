# Architecture Decision Log

This page records the key technical decisions made during the design and build of the UBC DERC camera API system. Each entry documents the context at the time the decision was made, the decision itself, and its consequences — so that future maintainers can understand *why* the system is built the way it is, not just *how*.

## Decision Index

| ID | Title | Status | Date |
|---|---|---|---|
| [ADR-001](adr-001-api-layer.md) | Use unofficial Protect API for recorded footage access | Accepted | 2026-09-22 |
| [ADR-002](adr-002-gateway-host.md) | CalfTop as the researcher-facing API gateway host | Accepted | 2026-09-22 |
| [ADR-003](adr-003-gateway-api-design.md) | Gateway API design | Accepted | 2026-09-22 |

## How to Add a Decision

When a significant technical choice is made — especially one that could look surprising to a future reader, or one where a reasonable alternative was considered and rejected — add an entry here. Use the next sequential ADR number, copy the template below, and link it in the table above.

```markdown
# ADR-NNN: Short Title

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN

**Date:** YYYY-MM-DD

## Context

What situation or constraint prompted this decision?
What options were considered?

## Decision

What was decided, in one or two clear sentences.

## Consequences

What does this enable? What limitations or risks does it introduce?
What follow-on work does it create?
```
