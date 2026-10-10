# Sentinel AI

**One intelligent core. An ecosystem of specialized AI agents.**

Sentinel AI is a personal AI platform in development, designed to help people interact with their digital environment, coordinate workflows, and build an ecosystem of specialized AI agents.

Sentinel serves as the primary interface: it interprets requests, coordinates tasks, applies security policies, and can delegate work to specialized agents through a unified system. The long-term vision is a modular platform that runs locally, integrates with cloud services when useful, and can eventually support secure deployments for individuals and businesses.

## Vision

Build an extensible AI platform where one intelligent core can create, configure, test, coordinate, and manage specialized agents—each with a defined purpose, permissions, and responsibilities.

## Core Components

- **Sentinel Core** — The primary assistant for understanding requests, coordinating actions, and presenting results.
- **AI Agent Factory** — A planned subsystem for creating, configuring, testing, and managing specialized AI agents.
- **Tool Integration Layer** — Connects agents to approved tools, applications, repositories, files, and development environments.
- **Security and Policy Engine** — Establishes permissions, approval requirements, and boundaries around sensitive operations.
- **Memory and Context** — A foundation for retaining useful information and supporting continuity across tasks.
- **Voice and Conversational Interface** — Supports natural interaction through voice and text.

These components describe the intended architecture; not all capabilities are implemented yet.

## Current Development Focus

The initial milestone focuses on a secure local Windows workflow:

1. Detect supported Sentinel wake-word transcript phrases.
2. Verify the authorized speaker as the voice-authentication work matures.
3. Use configured security questions as a fallback where implemented.
4. Establish an authenticated session.
5. Convert microphone input to text.
6. Route requests through an agent orchestration layer.
7. Start with safe, read-only GitHub operations.
8. Return results through text, with text-to-speech planned.
9. Record authentication attempts and tool activity locally.

Azure Data Engineering integrations and broader workflow automation are planned for later phases.

## Development Status

**Early development.** The repository contains a local authentication foundation, transcript wake phrases, microphone input and wake-word adapters, environment setup scripts, and security workflow components. A microphone smoke-test script is included for the available openWakeWord acoustic model.

The four Sentinel transcript phrases are supported, but acoustic models for those exact phrases and speaker biometric verification remain future work. The full AI reasoning, tool-execution, and agent-factory experience is still evolving. Treat planned capabilities below as roadmap items, not finished features.

## Roadmap

1. **Secure Sentinel Core** — Strengthen the local assistant and authentication workflow.
2. **Controlled tool use** — Build and validate permission-aware integrations, starting with read-only operations.
3. **Specialist agents** — Add agents with explicit scopes, instructions, and tests.
4. **AI Agent Factory** — Develop the workflow for creating, configuring, testing, and managing agents.
5. **Coordinated agent ecosystem** — Expand toward a larger set of cooperating specialist agents.
6. **Customer pilot readiness** — Add stronger isolation, observability, deployment, and support practices.
7. **Commercial evaluation** — Assess a hosted, multi-user service only after the security and reliability foundations are ready.

## Design Principles

- **Local-first development:** Keep local execution as the starting point, with optional hosted-model and cloud integrations.
- **Modular architecture:** Add agents and tools without rebuilding the core.
- **Least privilege:** Give each agent only the access it needs.
- **Human approval:** Require confirmation for consequential, destructive, or externally visible actions.
- **Testability and auditability:** Make agent behavior, tool activity, and failures easier to inspect.
- **Secure by design:** Keep secrets out of source code and apply layered controls instead of relying on voice recognition alone.

## Current Local Setup

Sentinel AI currently targets a Windows development environment using Python, a project-local `.venv`, and optional microphone/voice dependencies.

### Requirements

The microphone wake-word adapter uses packages listed in `requirements-voice.txt`, including:

- `openwakeword`
- `numpy`
- `PyAudioWPatch` (Windows)

### One-Click Environment Setup

The repository includes:

```text
scripts/setup_sentinel_env.bat
```

Run the batch file from Windows Explorer, Command Prompt, or PowerShell. The script checks for Python, may attempt to install Python 3.12 through Windows `winget` if Python is missing, prepares a local wheelhouse, recreates `.venv`, and installs the listed voice requirements.

### Local Wheelhouse

The `wheel/` directory is intentionally ignored by Git so large binary wheel files are not committed:

```text
wheel/*.whl
```

Wheel files are local to your machine. The setup script may access PyPI to download missing wheels; package installation then uses the local wheelhouse with `--no-index --find-links wheel`.

### Activate the Environment and Run Tests

From PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -p "test_*.py"
```

## Security Principles in Practice

The security design aims to include:

- Read-only operations by default where practical
- Explicit confirmation before consequential or destructive actions
- Least-privilege access to external services
- Security challenge answers stored as salted hashes, never plain text
- Local audit logs for authentication attempts and tool activity
- Rate limiting and lockouts for repeated authentication failures
- Secrets kept outside source code and repository history
- Local `.env` files excluded from Git

Security controls and integrations are being developed and should be reviewed before using Sentinel with sensitive data or real-world operations.

## High-Level Architecture

The following diagram shows the intended direction, not a claim that every component is complete.

```mermaid
flowchart TD
    user[User: Voice or Text] --> interface[Conversational Interface]
    interface --> core[Sentinel Core]
    core --> policy[Security and Policy Checks]
    policy -->|Allowed| factory[AI Agent Factory]
    policy -->|Approval required| approval[User Approval]
    approval --> factory
    factory --> agents[Specialist Agents]
    agents --> tools[Approved Tool Integrations]
    tools --> audit[Results and Audit Records]
    audit --> core
    core --> response[Response to User]
```

## Planned Integrations

Potential integrations include:

- GitHub repository and code workflows
- VS Code workspace inspection and controlled code changes
- Windows terminal and filesystem operations
- Local project and task context
- Azure Data Engineering workflows
- Optional hosted models and cloud infrastructure

Each integration should be added with explicit permissions, tests, and appropriate approval boundaries.

## Commercialization

The long-term commercial direction is to evaluate a product built around the Sentinel Core and AI Agent Factory. Multi-user hosting, tenant isolation, deployment, billing, and support are future work—not current capabilities.

See the [Sentinel AI Commercialization Plan](docs/SENTINEL_AI_COMMERCIALIZATION_PLAN.md) for the proposed phases, infrastructure options, security considerations, and initial business model.

## Repository

[GitHub: MD0210/Sentinel-AI](https://github.com/MD0210/Sentinel-AI)

## License

A license has not yet been specified. Confirm the intended licensing and distribution terms before redistributing or commercializing the project.
