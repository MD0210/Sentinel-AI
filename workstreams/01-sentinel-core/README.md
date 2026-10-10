# 01 — Sentinel Core

## Purpose

Build the central request-processing engine that accepts a user request, calls a configured language model, interprets the result, and eventually coordinates tools and specialist agents.

## Scope

1. Replace placeholder or echo behavior with a real model-response loop.
2. Define a provider-neutral interface for hosted and local models.
3. Add a configurable local-model adapter, starting with Ollama.
4. Keep model configuration outside source code and prompts.
5. Normalize responses and handle provider errors predictably.
6. Evolve the request loop toward planning, tool selection, delegation, and response synthesis.

## Initial milestone

A configured model can generate a response through Sentinel's existing request path. Automated tests use mocked providers and do not require a live model, microphone, or hosted-model API key.

## Acceptance criteria

- The request handler uses the configured provider instead of returning a placeholder response.
- Provider selection and model settings are configurable.
- Success, unavailable-provider, timeout, and malformed-response paths are tested.
- Provider-specific details are isolated behind an interface.
- Existing tests and GitHub Actions continue to run.
- The change is delivered in a focused pull request.

## Related issues

- [#45 — Implement a working Sentinel Core model-response loop](https://github.com/MD0210/Sentinel-AI/issues/45)

## Status

**Active workstream.** Start by inspecting the existing request path and tests, then implement the smallest end-to-end model call. Agent delegation and tool execution are later milestones, not prerequisites for the first working response loop.

## Out of scope for the first milestone

- Full multi-agent orchestration.
- Autonomous repository writes or deployments.
- Building the entire Agent Factory.
- Dashboard or multi-tenant SaaS features.
