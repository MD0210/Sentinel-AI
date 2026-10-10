# Sentinel AI: Personal Build to Commercial SaaS Plan

> **Status:** Planning document  
> **Purpose:** Build Sentinel AI as a personal voice assistant and AI Agent Factory, then commercialize it for customers.  
> **Cost basis:** All prices below are illustrative planning estimates in Philippine pesos (PHP), not vendor quotes or guaranteed bills. Revalidate provider pricing and measure real usage before selling plans.

## Product vision

**Sentinel is the core assistant.** It is the user's primary conversational interface for understanding requests, coordinating tasks, enforcing security policies, and supervising specialist agents. Sentinel should have its own distinct product identity, with configurable voice and text interaction rather than relying on comparisons to other fictional assistants.

The **AI Agent Factory** is a subsystem Sentinel uses to create, configure, test, version, run, and manage specialist agents.

Specialist agents use approved tools and have explicit purposes, model settings, memory scopes, and permissions. Ten agents do **not** require ten servers or ten separate models: agent definitions can share a model runtime and execution infrastructure, subject to resource and concurrency limits.

## Sentinel AI GUI and Hierarchical Agent Command Center

The planned GUI is the user's visual command center for Sentinel Core, specialist agents, sub-agents, integrations, and coordinated work. Treat this as product scope for the roadmap, not as an implemented feature.

### Agent hierarchy and identity

The interface should represent a hierarchy with **Sentinel AI as the master orchestrator**, specialist agents beneath it, and optional sub-agents beneath specialist agents. Each agent should have a configurable profile containing:

- Stable ID, display name, and role (for example, **Marc Thomas — CFO** or **John Doe — Marketing Analyst**).
- Purpose, instructions, parent agent, and delegated responsibilities.
- Model/provider settings, autonomy level, allowed tools, memory scope, and execution limits.
- Enabled/disabled state, runtime or heartbeat status, current task, and recent execution history.

Parent-child placement determines organizational relationships and delegation paths only. It must not automatically grant a child the parent's connector permissions, credentials, or memory access.

### Integration tiles

Display approved connectors as icon-based tiles on the Sentinel dashboard and on each agent's profile. Example services include SharePoint, Stripe, Azure, HubSpot, and Facebook Ads. Each tile should communicate:

- Connection and credential status, including expired or disconnected states.
- The operations supported by that connector and the permission scope granted.
- Which agents can access it, and whether access is read-only or includes approved write operations.
- Last successful check or use, plus relevant errors.

An icon or configured connector entry is not proof that a live account is connected. Only show a healthy/connected state after a real authorized connection check.

### Agent-to-agent communications

Sentinel should coordinate agents through the orchestrator and task system rather than relying on invisible, unbounded conversations. For example:

1. A user asks Sentinel for a business performance summary.
2. Sentinel delegates financial analysis to Marc Thomas (CFO).
3. Marc requests campaign metrics from John Doe (Marketing Analyst).
4. John retrieves authorized HubSpot or Facebook Ads data and returns a structured result.
5. Marc combines the results with authorized financial information and reports back to Sentinel.
6. Sentinel presents the final answer and links to the relevant task history.

The GUI should show message and task handoffs, who initiated each action, the source agent and recipient, status, results, failures, and any approval requests. Agent communication should be bounded by task scopes, tool permissions, timeouts, and execution limits; retrieved content must be treated as untrusted data.

### Main GUI views

- **Overview:** system and worker status, agent health, queued/running/failed tasks, pending approvals, recent activity, and integration health.
- **Agent hierarchy:** expandable tree or node graph for navigating parent agents and sub-agents.
- **Agent details:** edit identity, role, parent, instructions, model, autonomy limits, permissions, and memory scope.
- **Integrations:** connector catalog and per-agent access management, with explicit scopes and connection status.
- **Communications and task trace:** chronological view of delegation, messages, tool calls, results, and audit events.
- **Approvals:** review and approve or reject sensitive actions with appropriate re-authentication.
- **Execution location:** show whether a task runs on the local device or a hosted worker and whether it is waiting for the laptop, network, model, or user approval.

### Implementation and security sequence

1. Define the agent and hierarchy data model, connector registry, and task/message event schema.
2. Build a read-only hierarchy and agent-detail view using sample data before connecting real accounts.
3. Connect the GUI to Sentinel's authenticated API; do not expose arbitrary shell access or a local laptop directly to the public internet.
4. Add real agent/task status, connector health, and communication/audit events.
5. Add controlled agent editing, connector permission management, and approval workflows only after backend authorization is enforced and tested.
6. Add secure remote/mobile access and hosted workers as separate milestones; tasks continue only while their assigned execution environment and dependencies are available.

This GUI should make Sentinel's hierarchy and collaboration understandable without weakening the existing principles of least privilege, tenant isolation, human approval, and auditable execution.

---

## Guiding principles

1. Build and prove the local product before paying for cloud infrastructure.
2. Use a local-first, hybrid model architecture: local models for development and suitable tasks; hosted models when quality or capability justifies the cost.
3. Keep model providers interchangeable behind a provider interface.
4. Treat prompts as instructions, not as a security boundary. Enforce permissions in code outside the model.
5. Default to read-only tools. Require explicit approval for writes, destructive operations, deployments, external messages, and other sensitive actions.
6. Isolate each customer's data, memory, credentials, files, execution logs, and usage.
7. Meter usage by customer and agent run. Apply timeouts, tool-call limits, retry limits, concurrency limits, and spending caps.
8. Do not enable autonomous production actions until they have specific tests, approval gates, and audit logging.
9. Do not promise unlimited AI usage under a fixed subscription.
10. Keep personal/local mode and hosted customer environments separate.
11. Design for offline usefulness: local memory, a durable task queue, and local-model support should work without internet when the laptop is powered on.
12. Treat business integrations as permissioned connectors shared by the core and agents, not as ad hoc credentials embedded in individual agents.
13. Connect employer and customer systems only with explicit authorization; isolate credentials, content, memory, and logs by user or tenant.

---

## Sentinel as the First Customer of Its Own Agent Factory

**Strategic priority:** use Sentinel's first development team to help build and test Sentinel itself, then reuse the same workflow to help create other SaaS products. This is a planned capability, not an implemented autonomous coding system.

### Development-team roles

- **Sentinel Core / Team Lead:** receives a goal, decomposes it into bounded work, delegates tasks, tracks dependencies, and reports progress.
- **Product Manager:** defines user stories, acceptance criteria, and issue updates.
- **Software Architect:** proposes architecture and reviews technical trade-offs before implementation.
- **Developer Agent:** implements one approved task at a time in an isolated branch/worktree or sandbox.
- **QA Engineer:** runs the allowed test suite and maps results to acceptance criteria.
- **Security Reviewer:** checks authorization, secrets, dependency risks, unsafe execution, and the proposed diff.
- **DevOps Engineer:** helps prepare CI/CD and deployment changes, with production operations kept approval-gated.

For the MVP, these can be role profiles performed by a small number of model sessions; do not create a separate server or model for each role by default.

### Initial end-to-end workflow

1. Select a GitHub issue or submit a development goal.
2. Retrieve only the authorized repository files, issue context, and documentation needed for the task.
3. Generate a plan with dependencies, acceptance criteria, affected areas, and a risk classification.
4. Ask for approval when the plan is ambiguous, broad, or high-risk.
5. Execute one scoped change in an isolated workspace with a restricted tool allowlist.
6. Run repository-approved tests and capture their actual output.
7. Have a separate review step inspect the diff, test results, and security implications.
8. Present a summary of changes, test outcomes, limitations, and risks.
9. After explicit approval, create a branch or draft pull request if that capability has been implemented and enabled. Merging and production deployment remain separate human-approved actions.

### Security requirements

- Start with read-only GitHub access; expand to branch/PR writes only when necessary.
- Never expose tokens, secrets, or raw credentials to model prompts or logs.
- Enforce authorization in the tool execution layer, independent of agent instructions.
- Treat repository content, issue comments, and retrieved documents as untrusted data, not policy instructions.
- Run generated code and tests in an isolated environment with resource and network restrictions.
- Do not permit unrestricted host shell access, self-granted permissions, automatic merges, or unattended production deployment.
- Record task IDs, agent handoffs, tool calls, permission decisions, test outcomes, changed files, and approval events.
- Keep repository access scoped to explicitly authorized repositories and organizations.

### Definition of the first useful milestone

Sentinel can read a selected issue, produce a plan with acceptance criteria, and help prepare one small tested code change in a controlled workspace. The user can inspect the diff and test output before any merge. This milestone is more valuable than building a large agent roster or a polished dashboard before the development workflow is reliable.

### Related GitHub issues

- [#45 — Working Sentinel Core model-response loop](https://github.com/MD0210/Sentinel-AI/issues/45)
- [#46 — Permission-aware tool registry and execution policy](https://github.com/MD0210/Sentinel-AI/issues/46)
- [#50 — GitHub read-only connector with audit logging](https://github.com/MD0210/Sentinel-AI/issues/50)
- [#63 — Governed hierarchical-agent prototype](https://github.com/MD0210/Sentinel-AI/issues/63)
- [#64 — Build Sentinel's AI software-development team](https://github.com/MD0210/Sentinel-AI/issues/64)

## Phase 1 — Build Sentinel for personal use

**Goal:** Make Sentinel useful on the developer's Windows laptop before commercial hosting.

### Hardware available

- 16 GB system RAM
- NVIDIA RTX 3060 Laptop GPU with 6 GB VRAM

This hardware is suitable for development and testing with appropriately sized quantized local models. Actual model performance depends on context size, quantization, GPU memory use, and other applications running at the same time.

### Suggested initial stack

| Area | Initial choice | Notes |
|---|---|---|
| Language | Python | Reuse the current Sentinel AI codebase |
| API (when needed) | FastAPI | Add after the core runtime is stable |
| Validation | Pydantic | Validate agent definitions and tool inputs |
| Local model runtime | Ollama | Begin with a small quantized model; benchmark locally |
| Voice | Existing Sentinel voice modules, plus local speech-to-text and text-to-speech | Keep voice components replaceable |
| Tests | pytest or existing unittest suite | Reuse current tests and add regression tests |
| Initial storage | Local files and SQLite | Do not add cloud storage merely because agents are added |
| Version control / CI | GitHub and GitHub Actions | Run tests on changes; protect secrets |

### Build milestones

#### 1A. Sentinel + 2 specialist agents

Build and validate:

- Wake-word and voice interaction, with text input as a reliable fallback.
- Authentication and a locked/unlocked state.
- A model-provider interface for local models.
- A tool registry with schemas and permissions.
- Agent definitions containing at least:
  - ID and name
  - Purpose and instructions
  - Model/provider selection
  - Allowed tools
  - Memory scope
  - Autonomy level
  - Execution limits
- An execution record for every request.
- A confirmation gate for sensitive actions.

Suggested initial agents:

1. **GitHub / Code Review Agent** — inspect repositories and suggest improvements; read-only by default.
2. **Research Agent** — gather and summarize information from explicitly approved sources.

Acceptance criteria:

- Sentinel can respond using the configured model.
- Both agents can be selected and run through Sentinel.
- Invalid tool arguments are rejected.
- Unauthorized tools cannot run.
- Sensitive actions require explicit confirmation.
- Tests cover authentication, policy enforcement, model failures, and tool failures.

#### 1B. Expand to 4 agents

Add:

3. **Data Engineering Agent** — review SQL, Python, and pipeline designs; initially no production write access.
4. **Productivity Agent** — organize approved notes, draft tasks, and summarize user-provided material.

Add reusable templates, configuration validation, per-agent settings, structured logs, and test fixtures. Ensure agents share the runtime where appropriate without sharing private memory accidentally.

#### 1C. Expand to 10 agents

Add candidate agents such as:

5. Testing / QA Agent  
6. Documentation Agent  
7. Project Management Agent  
8. Reporting Agent  
9. SQL Analysis Agent  
10. Knowledge Retrieval Agent

Treat these as configurable agent definitions, not ten independent infrastructure deployments.

Add:

- Agent lifecycle: create, validate, test, enable, disable, version, and delete.
- Task queue or controlled scheduler for longer tasks.
- Timeouts, maximum tool calls, bounded retries, and concurrency limits.
- Error handling, audit logs, and a way to cancel work.
- Tests for prompt injection, permission escalation, cross-agent access, and untrusted tool output.
- A clear way for Sentinel to explain which agent acted and what it did.

**Cost target for personal development:** approximately **₱0–₱1,500/month** in optional AI/service fees if local models are used and paid usage is limited. This excludes electricity, existing internet costs, the value of development time, and optional hardware upgrades. It is a target, not a guarantee.

---

## Phase 2 — Prepare the engine for multiple customers

**Goal:** Separate the reusable engine from personal voice and local-device concerns.

Suggested logical modules (adapt to the existing repository rather than replacing working code wholesale):

```text
Sentinel-AI/
├── agent/                 # Existing Sentinel controller and core behavior
├── voice/                 # Wake word, speech recognition, text-to-speech
├── security/              # Authentication, policies, approvals, audit
├── tools/                 # Tool implementations and schemas
├── factory/
│   ├── registry.py        # Agent definitions and versions
│   ├── runtime.py         # Execute one agent run safely
│   ├── orchestrator.py    # Route and coordinate tasks
│   ├── tool_registry.py   # Approved tools and schemas
│   └── policies.py        # Autonomy and execution limits
├── providers/
│   ├── base.py            # Provider interface
│   ├── local.py           # Local model adapter
│   └── hosted.py          # Hosted model adapter
├── memory/                # Memory interfaces and scoped storage
├── api/                   # FastAPI routes, added when needed
├── app/                   # User interface
├── config/                # Safe configuration examples; no secrets
└── tests/                 # Unit, integration, security, and tenant tests
```

### Multi-tenant requirements

Before accepting customer data, implement and test:

- Customer/tenant identity on every relevant database record and request.
- Authorization checks on every API and tool execution.
- Tenant-scoped agent definitions, memory, files, logs, and integrations.
- Separate credentials per customer, stored in a secrets manager.
- Usage metering per tenant, agent, model, and execution.
- Data export and deletion workflows.
- Backup and recovery procedures.
- Rate limits and hard usage caps.
- Security logging and a process for handling incidents.
- Clear data retention, privacy, and trial-expiration policies.

Do not assume that separating records by a tenant ID alone is sufficient; enforce authorization in the API, database access layer, storage paths, and worker execution environment.

---

---

## Business Integration Layer

**Goal:** Let Sentinel Core and authorized specialist agents work across a user's approved business ecosystem through a consistent, auditable connector framework.

### Candidate integrations

| System | Initial read-oriented use cases | Higher-risk actions to gate |
|---|---|---|
| SharePoint / Microsoft 365 | Search authorized documents, summarize policies, retrieve project context | Editing or sharing documents, changing permissions |
| Azure | Inspect approved resources, pipeline status, logs, and monitoring data | Deployments, resource changes, deletion, production operations |
| GitHub | Read repositories, issues, pull requests, and code; prepare reviews | Pushing changes, merging pull requests, changing repository settings |
| Azure DevOps | Read assigned work items, sprint context, build and release status | Updating work items, changing pipelines, releases |
| Outlook / Teams | Summarize authorized messages and extract action items | Sending messages, invitations, or external communications |
| Data platforms / Power BI | Query approved datasets and summarize reporting results | Data writes, permission changes, production refresh or deployment |

Availability depends on the connector implementation, the provider's API, the user's permissions, organizational policies, and any required administrator consent.

### Recommended connector architecture

- **Connector registry:** declares each connector's identity, supported operations, input/output schemas, and risk level.
- **Identity and credential manager:** uses supported OAuth flows, managed identities, or securely stored customer credentials; never embed secrets in prompts or source code.
- **Policy enforcement:** checks the user, tenant, agent, requested operation, and resource before executing a tool.
- **Approval service:** requests explicit confirmation for writes and other consequential actions.
- **Audit trail:** records who or what requested an operation, the connector used, the decision, and the outcome without unnecessarily logging sensitive content.
- **Tenant-aware configuration:** scopes connectors, tokens, files, agent memory, and logs to the correct user or customer.
- **Connector tests:** include authorization failures, expired credentials, rate limits, malformed responses, prompt injection in retrieved content, and attempts to exceed granted permissions.

Start with read-only operations. Add write operations one at a time, with dedicated tests and approval rules. Treat content retrieved from SharePoint, email, repositories, and other external systems as untrusted data, not as instructions that can override Sentinel's security policy.

### Offline Intelligence Mode and synchronization

Sentinel should continue useful local work when the laptop is disconnected, as long as it is powered on, awake, and the required local processes and models are running.

Offline-capable tasks can include:
- Processing a durable local task queue when the task needs only local resources.
- Searching and summarizing local files and previously synchronized knowledge.
- Running a supported local model through a local runtime such as Ollama.
- Saving user feedback, task outcomes, and reusable workflow records to local storage.
- Preparing a draft or analysis for later review.

Cloud-dependent tasks should be marked as waiting for connectivity. When the device reconnects, Sentinel should refresh data and re-check authorization, freshness, and the continued validity of each queued action before running it. Do not blindly replay stale writes, external messages, deployments, or other consequential operations.

Offline does not mean always-on: a powered-off computer cannot run tasks, and sleep may pause background work. Local inference performance is constrained by available memory, GPU resources, model size, and other running applications.

### Suggested implementation sequence

1. Define a common connector interface and operation schema.
2. Implement one read-only connector first (GitHub is a practical starting point for this repository).
3. Add scoped credentials, policy checks, and audit events before expanding access.
4. Add SharePoint/Microsoft Graph and Azure connectors only with appropriate account and organizational authorization.
5. Add a durable local queue with explicit states such as `pending`, `waiting_for_network`, `needs_approval`, `running`, `succeeded`, `failed`, and `cancelled`.
6. Add synchronization and stale-action checks; require fresh approval where needed.
7. Add tenant isolation and integration security tests before a customer-hosted or SaaS pilot.

All integrations and background capabilities described in this section are roadmap items until implemented and tested.

## Phase 3 — First hosted customer trial

**Goal:** Support one customer with Sentinel and a selectable number of specialist agents.

### Recommended first deployment

- Web interface with chat; add browser microphone and spoken responses where reliable.
- FastAPI backend.
- A shared Business Integration Layer for approved SharePoint/Microsoft 365, Azure, GitHub, and other connectors, enabled only after authorization and security review.
- Managed PostgreSQL for accounts, tenant data, agent configurations, usage, and execution metadata.
- Object storage only if the product needs customer uploads, generated files, or durable artifacts.
- Azure Container Apps or a comparable managed container host for the API and background work.
- Azure Key Vault or an equivalent secrets manager.
- Hosted model API with per-customer usage limits, or a customer-provided API key.
- Automated tests and deployment through GitHub Actions.
- Monitoring, backups, and cost alerts.

The developer's laptop should be used for development, not as the production server for a remote customer. A local/customer-hosted edition can be offered separately if the customer has suitable hardware and accepts the maintenance responsibilities.

### Do you need cloud storage?

Not automatically.

- **Local proof of concept:** local files and SQLite may be enough.
- **Hosted trial without user file uploads:** a database may be enough initially.
- **Hosted trial with documents or generated artifacts:** add object storage such as Azure Blob Storage.
- **Customer-hosted edition:** data can remain on the customer's computer or server, subject to their backup and security arrangements.

Storage charges depend on capacity, operations, redundancy, and transfer; the number of agents is not by itself a storage-cost driver.

### One customer, ten agents

The customer may have one Sentinel core plus nine specialist agents. Share the model runtime and worker infrastructure where practical, but enforce independent permissions, memory scopes, quotas, and execution records. Use concurrency limits so one customer's workload cannot exhaust resources for others.

---

## Phase 4 — Example commercial plans

These are **starting hypotheses to test**, not validated market prices. They assume a shared hosted service, limited included usage, and no dedicated GPU server per customer.

| Plan | Included agents | Example monthly price | Intended customer |
|---|---:|---:|---|
| Low | Sentinel + 2 agents | ₱999 | Individual or small trial |
| Mid | Sentinel + 4 agents | ₱2,499 | Regular productivity use |
| High | Sentinel + 10 agents | ₱5,999 | Heavy workflows and more integrations |
| Pay as you go | Sentinel + customer-selected number of agents | ₱499 base + metered usage | Variable or experimental workloads |

### Plan limits

Each plan should specify both agent count and usage allowance. Consider limits for:

- Model input/output tokens or equivalent provider usage
- Agent runs per month
- Maximum duration and tool calls per run
- Concurrent runs
- File storage and retention
- Scheduled jobs
- Premium integrations
- Support level

Offer transparent usage alerts and a hard spending limit. Do not advertise unlimited use until measured costs and abuse controls support it.

### Cost assumptions per customer

Illustrative AI usage estimates for modest, controlled workloads:

| Plan | Possible AI cost to the platform per month |
|---|---:|
| Low | ₱100–₱350 |
| Mid | ₱400–₱1,000 |
| High | ₱1,000–₱2,500 |
| Pay as you go | Based on actual metered usage |

These ranges can be exceeded by long prompts, large contexts, frequent runs, voice processing, document processing, agent loops, or expensive models. Validate them with actual usage data before finalizing prices.

A bring-your-own-key option can let customers pay their model provider directly. It may lower the platform's AI expense, but requires secure credential handling and clear support boundaries.

---

## Phase 5 — Estimate operating costs

### One-customer hosted pilot

Illustrative monthly budget:

| Expense | Estimated monthly cost |
|---|---:|
| API hosting and background jobs | ₱0–₱1,500 |
| Database | ₱0–₱1,500 |
| Object storage and backups | ₱0–₱500 |
| Domain, email, monitoring, miscellaneous | ₱100–₱800 |
| **Illustrative base infrastructure** | **₱100–₱4,300** |
| Hosted AI usage | Add approximately ₱100–₱2,500+ |

For budgeting, reserve approximately **₱3,000–₱8,000/month** for a small pilot using some paid services and controlled model usage. This is a planning reserve, not a forecast or quote. A free-tier deployment may cost less; reliability, support, traffic, and model usage can make it cost more.

Check current regional pricing and free-tier conditions before deploying. Free tiers can change and are not a substitute for production reliability.

### Example High-tier unit economics

At a hypothetical subscription price of ₱5,999/month:

| Item | Example amount |
|---|---:|
| Subscription revenue | ₱5,999 |
| AI usage | −₱1,500 |
| Allocated infrastructure | −₱500 |
| **Contribution before other expenses** | **₱3,999** |

This excludes payment processing, taxes, customer support, sales, development, refunds, and unexpected usage. It is not net profit.

### Scaling to more customers

Shared infrastructure can serve multiple tenants, so infrastructure does not always scale linearly with customer count. AI usage, storage, database load, concurrency, support, and security requirements do increase with use. Track cost per tenant and per successful agent run; introduce dedicated environments only when customer needs or risk justify them.

---

## Phase 6 — Trial-to-paid launch checklist

- [ ] Sentinel works locally with two useful specialist agents.
- [ ] Four-agent and ten-agent configurations are tested.
- [ ] Authentication and authorization are enforced outside the LLM.
- [ ] Read-only access is the default.
- [ ] Sensitive actions require explicit approval.
- [ ] Agent runs have bounded time, tool calls, retries, and concurrency.
- [ ] Tenant isolation tests prove that customers cannot access one another's data.
- [ ] Secrets are stored outside source code and prompts.
- [ ] Usage metering, alerts, and hard caps work.
- [ ] Backups, export, deletion, and trial-expiration procedures are tested.
- [ ] Customer-facing privacy, retention, acceptable-use, and pricing terms are ready.
- [ ] One pilot customer validates usefulness and real cost before broad launch.
- [ ] Subscription prices are reviewed against measured usage, support burden, and applicable taxes.

## Recommended order of execution

1. **Make Sentinel useful to its own developer:** implement the model-response loop, task model, and clear failure handling.
2. **Secure the execution foundation:** add permission-aware tools, approval gates, audit events, and automated security tests.
3. **Connect GitHub read-only:** let Sentinel retrieve repository files, issues, and pull-request context without write access.
4. **Build the AI development team:** plan from an issue, implement one scoped change in an isolated workspace, run tests, review the diff, and present results for approval.
5. **Prove hierarchical delegation and add the dashboard:** make handoffs visible and permissions independent across parent and child agents.
6. **Expand the Agent Factory:** add more role profiles and specialist agents as repeatable configurations, not separate servers by default.
7. **Add local/offline execution and selected business integrations:** verify queue recovery, stale-action checks, and connector authorization.
8. **Prepare for customers:** introduce tenant isolation, usage metering, deployment, privacy operations, backups, and support only after the personal workflow is dependable.
9. **Validate a paid pilot:** measure real model and infrastructure costs, test with a small number of users, and then refine pricing.

## Pricing and vendor references

Recheck these official sources before spending or setting customer prices:

- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [Azure Blob Storage cost estimation](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-storage-estimate-costs)
- [Azure Container Apps pricing](https://azure.microsoft.com/pricing/details/container-apps/)
- [Supabase pricing](https://supabase.com/pricing)

---

**Bottom line:** Build one secure Sentinel core, a reusable Agent Factory, and a shared execution platform. Agents are capabilities, not separate servers. Start local, prove value with two agents, scale to ten, then add multi-tenant hosting and paid plans after measuring real usage.
