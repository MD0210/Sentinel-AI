# Sentinel AI

A secure, voice-authenticated AI work agent for Windows, automation, productivity, and developer workflows.

## Vision

Sentinel AI is designed to act as a local work assistant on a Windows machine. The user can activate Sentinel by voice, authenticate, ask questions or give tasks, and allow the agent to use controlled tools such as GitHub, VS Code, the local filesystem, and a terminal.

Azure Data Engineering integrations are planned for a later phase.

## Phase 1

The first milestone focuses on a small, testable end-to-end workflow:

1. **Wake word** — detect "Hey Sentinel".
2. **Voice verification** — verify the authorized speaker.
3. **Security Q&A fallback** — after a failed voice check, require two configured challenge questions.
4. **Authenticated session** — establish a temporary authorized Sentinel session.
5. **Speech-to-text** — convert the user's request into text.
6. **Agent orchestration** — interpret the request and select an explicit tool.
7. **GitHub integration** — begin with safe, read-only GitHub operations.
8. **Response** — return results by text and, later, text-to-speech.
9. **Audit logging** — record authentication attempts and tool activity locally.

## Planned Capabilities

- Voice activation and speaker verification
- Personal security challenge questions
- AI agent orchestration and tool routing
- GitHub repository and code workflows
- VS Code workspace inspection and controlled code changes
- Controlled Windows terminal and filesystem operations
- Local project/context memory
- Azure Data Engineering integrations in a later phase

## Security Principles

Sentinel AI should use layered security rather than trusting voice recognition alone.

- Read-only operations by default
- Explicit confirmation before consequential or destructive actions
- Least-privilege access to external services
- Security challenge answers stored as salted hashes, never plain text
- Authentication failures and tool activity recorded in an audit log
- Rate limiting and lockouts for repeated authentication failures
- Secrets kept outside source code and repository history

## High-Level Architecture

```mermaid
flowchart TD
    U[User Voice] --> W[Wake Word: "Hey Sentinel"]
    W --> V[Voice Verification]
    V -->|Verified| S[Authenticated Session]
    V -->|Failed| Q1[Security Question 1]
    Q1 -->|Correct| Q2[Security Question 2]
    Q1 -->|Incorrect| L[Lockout / Cooldown]
    Q2 -->|Correct| S
    Q2 -->|Incorrect| L
    S --> STT[Speech-to-Text]
    STT --> A[AI Agent / Orchestrator]
    A --> G[GitHub]
    A --> C[VS Code]
    A --> T[Controlled Windows Terminal]
    A --> F[Local Filesystem]
    G --> R[Result]
    C --> R
    T --> R
    F --> R
    R --> A
    A --> O[Text / Text-to-Speech]
```

## Development Approach

Sentinel AI will be built incrementally. The first goal is a reliable local authentication and agent loop, followed by GitHub and development-tool integrations. Azure services can then be added as explicit tools without changing the core agent architecture.

## Repository

GitHub: https://github.com/MD0210/Sentinel-AI

## Status

Early development. Architecture and the Phase 1 workflow are being established before implementation expands.
