# Sentinel AI Workstreams

This directory separates Sentinel AI's roadmap into independently manageable workstreams. Each workstream README defines its purpose, scope, related GitHub issues, and current status.

## Workstreams

| Workstream | Purpose | Status |
|---|---|---|
| [01 — Sentinel Core](./01-sentinel-core/README.md) | Model interface, request/response loop, and orchestration | **Active focus** |
| [02 — Security and Reliability](./02-security-reliability/README.md) | Authentication, permissions, safe failure handling, and regression coverage | Planned / deferred by current prioritization |
| [03 — Tools and Integrations](./03-tools-integrations/README.md) | Governed tool registry and external-system connectors | Planned |
| [04 — Tasks, State, and Memory](./04-tasks-state-memory/README.md) | Durable task execution, history, and scoped memory | Planned |
| [05 — AI Development Team](./05-ai-development-team/README.md) | Product, architecture, development, QA, security review, and DevOps specialists | Planned |
| [06 — Agent Factory](./06-agent-factory/README.md) | Create, configure, evaluate, and manage specialist agents | Planned |
| [07 — Dashboard and SaaS](./07-dashboard-saas/README.md) | User experience, workspaces, usage, deployment, and commercialization | Planned |

## Working conventions

- Keep each workstream's scope and acceptance criteria in its README and track implementation work in GitHub Issues.
- Use small, focused branches and pull requests; avoid mixing unrelated workstreams in one change.
- Keep shared interfaces and cross-workstream dependencies documented.
- Existing automated tests and CI remain in use while feature development focuses on Sentinel Core.
- "Planned" means not the current implementation focus; it does not imply the work is implemented.
- These folders organize planning and documentation. They do not require every source-code module to be moved into matching folders.

## Current priority

Start with [Sentinel Core](./01-sentinel-core/README.md), beginning with the real model-response loop tracked in [Issue #45](https://github.com/MD0210/Sentinel-AI/issues/45).
