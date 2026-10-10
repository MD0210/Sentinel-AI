# 04 — Tasks, State, and Memory

## Purpose

Allow Sentinel to track work beyond a single request, recover task status, and retain relevant history in a controlled way.

## Scope

- Durable task records and lifecycle statuses.
- A local task queue and background worker.
- Retry and failure states with bounded behavior.
- Task history and result storage.
- Scoped memory separated by task, agent, or workspace where applicable.
- Offline/online task synchronization when supported.

## Related issues

- [#47 — Durable local task queue and background worker](https://github.com/MD0210/Sentinel-AI/issues/47)
- [#48 — Scoped local memory and task-history storage](https://github.com/MD0210/Sentinel-AI/issues/48)
- [#52 — Offline/online task synchronization](https://github.com/MD0210/Sentinel-AI/issues/52)

## Status

**Planned.** Start with the synchronous Core request loop, then introduce durable task execution when a concrete multi-step use case requires it.
