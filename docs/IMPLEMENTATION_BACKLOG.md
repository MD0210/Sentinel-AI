# Sentinel AI — Implementation Backlog and Repository Audit

**Last reviewed:** 2026-10-10  
**Purpose:** Convert the current repository audit into a practical, dependency-aware implementation sequence. This is a planning document, not evidence that the listed capabilities have been implemented or tested.

## Executive assessment

Sentinel AI is an early-stage Python prototype with an authentication/voice foundation and tests. It is not yet a complete AI agent orchestrator or AI Agent Factory. The immediate objective is a small, reliable vertical slice: **submit a task → get a real model response → check permissions → read repository context → produce a plan → test a scoped change → present it for human review**.

Do not start with a large multi-agent system, public dashboard, or multi-tenant SaaS deployment. First establish a working core, reproducible tests, and a safe execution boundary.

## Audit findings to resolve

| Finding | Why it matters | Tracking issue |
|---|---|---|
| Request handling currently includes placeholder/echo behavior instead of a verified model-response loop | Sentinel cannot yet provide real model-driven assistance through the core path | [#45](https://github.com/MD0210/Sentinel-AI/issues/45) |
| Tool policy is not yet a complete per-tool, per-agent, per-repository authorization layer | Prompt instructions alone cannot prevent unauthorized tool calls | [#46](https://github.com/MD0210/Sentinel-AI/issues/46) |
| Authentication boundary needs hardening; an authentication helper must not create an authenticated session without verifying credentials | Could become an authentication bypass if reused by an API or remote interface | [#49](https://github.com/MD0210/Sentinel-AI/issues/49) |
| GitHub connector is still a planned capability / placeholder in the inspected code | Sentinel cannot yet safely retrieve repository context through its own tool interface | [#50](https://github.com/MD0210/Sentinel-AI/issues/50) |
| No root-level core dependency manifest or configured CI workflow was identified in the audit | Clean installs and regressions are harder to verify consistently | [#65](https://github.com/MD0210/Sentinel-AI/issues/65) |
| Durable task queue, scoped memory, and task recovery are not implemented as a complete workflow | Long-running tasks and restart recovery are not reliable yet | [#47](https://github.com/MD0210/Sentinel-AI/issues/47), [#48](https://github.com/MD0210/Sentinel-AI/issues/48) |
| Wake-word detection, microphone input, and authentication are not yet one complete verified activation flow | Separate adapters should not be mistaken for a fully integrated voice experience | [#49](https://github.com/MD0210/Sentinel-AI/issues/49) |
| Agent hierarchy, dashboard, and SaaS runtime are planned rather than implemented | Roadmap descriptions must not imply these capabilities are available today | [#53](https://github.com/MD0210/Sentinel-AI/issues/53), [#62](https://github.com/MD0210/Sentinel-AI/issues/62), [#63](https://github.com/MD0210/Sentinel-AI/issues/63), [#64](https://github.com/MD0210/Sentinel-AI/issues/64) |

**Verification note:** This is a source/metadata audit, not a local execution report. No claim is made here that the test suite passes. Run tests locally and through CI before treating a change as verified.

## Recommended implementation order

### P0 — Make development reproducible and close the authentication boundary

1. **#65 — Base dependency manifest and CI**
   - Define core vs optional dependencies.
   - Add a clean-install path and CI for the existing tests.
   - Keep CI independent of microphone hardware, private credentials, and hosted-model API keys.
2. **#49 — Authentication correctness**
   - Ensure no helper or future API can establish an authenticated session without a verified credential result.
   - Separate wake-word detection from identity verification.
   - Add tests for success, failure, lockout, session expiry, and fallback behavior.
3. **#56 — Security and regression tests**
   - Add tests around authorization, secret redaction, untrusted repository content, and audit completeness.

**Exit gate:** A clean environment can install dependencies and run tests; authentication failure never grants a session; CI provides repeatable results.

### P1 — Build the usable Sentinel Core

4. **#45 — Real model-response loop**
   - Define a provider interface for hosted and local models.
   - Add timeout, cancellation, unavailable-provider, malformed-output, and safe-error handling.
   - Keep provider credentials out of source, prompts, and logs.
5. **#46 — Permission-aware tool registry**
   - Use typed schemas and validate tool arguments.
   - Enforce per-agent and per-operation permissions in code.
   - Require approval for sensitive writes, deployments, external messages, destructive operations, and permission changes.
6. **#47 and #48 — Durable task state and scoped memory**
   - Persist tasks and safe execution state.
   - Add bounded retries, cancellation, restart recovery, and deduplication.
   - Scope memory by user, agent, and task; support inspection and deletion.

**Exit gate:** Sentinel can answer through a configured model, reject unauthorized operations, preserve task state safely, and explain errors without leaking secrets.

### P2 — Make Sentinel repository-aware

7. **#50 — Read-only GitHub connector**
   - Read repository files, issues, and pull-request context with least-privilege access.
   - Treat repository content as untrusted data, not policy instructions.
   - Log the operation, authorization decision, and outcome without logging credentials.
8. **#64 — AI software-development team**
   - Start with issue analysis and a structured implementation plan.
   - Use an isolated workspace/branch and a narrow tool allowlist for any code execution.
   - Run tests, review the diff independently, and present the result for approval.
   - Human approval remains required before merge or release.

**Exit gate:** Sentinel can read one issue, make a bounded plan, and prepare one tested change in a controlled workspace without unrestricted host access.

### P3 — Demonstrate agent delegation

9. **#63 — Governed hierarchical-agent prototype**
   - Start with synthetic data and mock/read-only tools.
   - Demonstrate one bounded parent-to-child delegation chain.
   - Ensure hierarchy never grants inherited permissions automatically.
10. **#53 and #54 — Agent Factory lifecycle and initial specialists**
    - Validate versioned agent manifests.
    - New agents receive no tools by default.
    - Add specialists only when their tasks, tools, memory scopes, and tests are defined.
11. **#62 — Dashboard**
    - Build a read-only view over real task and audit data first.
    - Clearly label sample data and disconnected integrations.
    - Do not let the GUI act as the authorization boundary.

**Exit gate:** A reviewer can follow a task from Sentinel to a specialist and back, see tool decisions, and verify that unauthorized calls are blocked and recorded.

### P4 — Prepare for real users and SaaS

12. Add selected business connectors through a shared registry (#51), then safe offline/online synchronization (#52).
13. Benchmark local models (#55) and implement pluggable authentication (#60) as needed.
14. Design tenant isolation, quotas, usage metering, secret handling, backups, retention/deletion, monitoring, and support before a customer pilot (#58–#59).
15. Validate a pilot with measured cost and explicit customer consent before advertising multi-tenant or unattended execution.

**Exit gate:** Tenant isolation and operational controls have automated evidence; pricing is based on observed usage, not assumptions alone.

## Non-negotiable safety rules

- Start with read-only external access.
- Authorization is enforced by the tool/runtime layer, never only by agent instructions.
- Agents cannot grant themselves permissions or inherit credentials from parent agents.
- Treat repository files, issues, pull requests, and external content as untrusted input.
- Never expose secrets to model prompts, logs, source control, or generated reports.
- Execute generated code in an isolated workspace with resource limits; no unrestricted host shell.
- Require explicit approval before merge, deployment, release, permission changes, destructive operations, and consequential external writes.
- Record task IDs, agent handoffs, tool calls, authorization decisions, test results, approvals, and failures.
- Do not represent a laptop-dependent worker as always-on. Sleeping or powered-off devices cannot execute local work.
- Mark any feature as implemented only after code, tests, and documentation support that claim.

## First milestone to complete

Complete **#65 + #49 + #45 + #46 + #50** in dependency-aware order, then demonstrate the smallest end-to-end flow:

1. User selects a GitHub issue.
2. Sentinel retrieves it using read-only access.
3. A configured model returns a structured plan.
4. Sentinel identifies tools needed and checks permissions.
5. No code executes until an isolated execution path and tests are ready.
6. Sentinel reports the plan, risks, and next action.

The initial milestone is **not** autonomous merging or production deployment. It is reliable, safe repository-aware assistance with a human-controlled path to code changes.

## Related tracking

- [Open issues](https://github.com/MD0210/Sentinel-AI/issues)
- [#45 Working Sentinel Core model-response loop](https://github.com/MD0210/Sentinel-AI/issues/45)
- [#46 Permission-aware tool registry](https://github.com/MD0210/Sentinel-AI/issues/46)
- [#49 Authentication and fallback security](https://github.com/MD0210/Sentinel-AI/issues/49)
- [#50 Read-only GitHub connector](https://github.com/MD0210/Sentinel-AI/issues/50)
- [#56 Security and regression test coverage](https://github.com/MD0210/Sentinel-AI/issues/56)
- [#64 AI software-development team](https://github.com/MD0210/Sentinel-AI/issues/64)
- [#65 Dependencies and CI](https://github.com/MD0210/Sentinel-AI/issues/65)
