# OpenCode Framework

Welcome to the **OpenCode Framework**, a cognitive partnership model designed to transform how you work with AI agents.

This project is more than just a template; it is a structured environment that elevates the AI from a simple "code generator" or "copilot" to a **Senior Architect and Critical Thinking Partner**.

## 🧠 The Core Philosophy

The framework is built on the belief that AI is most effective when it is constrained by rigorous engineering standards and empowered by deep project context. We operate on three fundamental pillars:

### 1. Critical Cognitive Partnership

The agent is mandated to challenge ideas before implementing them. It identifies technical flaws, security risks, or redundant logic, acting as a "peer reviewer" in real-time.

### 2. Journal-First Discipline (NEW)

All significant work must be preceded or accompanied by a structured journal entry. The framework enforces this via a **timestamp-based pre-commit hook**, ensuring that the project's history is an accurate, human-and-AI-readable audit trail of intent and execution.

### 3. Strategy-First (Discovery -> Plan -> Execute)

Every non-trivial change follows a strict, non-negotiable lifecycle. 
1. **Discovery & Audit:** The agent first researches the domain (`/research`), audits the codebase (`/audit`), or investigates bugs (`/debug`) without modifying anything.
2. **Strategy:** A detailed implementation plan is proposed (`/plan`) based on discovery artifacts and requires user approval.
3. **Execution:** Only then does the agent begin writing code (`/task`) or content (`/draft`). This is enforced by the **TCR (Test-Commit-Revert)** protocol, ensuring a "Green-only" development path.

### 4. Validation-as-Truth

The `makefile` is the ultimate source of truth for project health. Automated hooks ensure that every agent action is followed by a validation run (linting, testing, formatting) to prevent regressions.

### 5. Task Isolation (Feature Branching)

All development work is strictly performed on dedicated, auto-generated feature branches. This keeps the `main` branch protected and always in a deployable state, while providing a clean, granular history for every task.

## 🚀 Quick Start

The fastest way to bootstrap a new project or integrate the framework into an existing one is to run the following command in your terminal:

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
```

!!! success "Next Steps"
    After installation, run `opencode /onboard` to get an overview of the repository and start your first session.

## 🛠️ Key Capabilities

- **Deep Discovery:** Use `/research` for multi-phase domain investigations.
- **Architectural Design:** Use `/design` for architecture and system design work.
- **Literate Commands:** Create guided, multi-step workflows with variables and conditional logic.
- **Isolated Execution:** Run commands in sandboxed Docker environments for safety.
- **Forensic Debugging:** Use `/debug` for root-cause analysis without immediate (and potentially incorrect) fixes.
- **Evidence-Based Audits:** Use `/audit` to identify technical debt and architecture issues.
- **Procedural Roadmap Management:** Use `/todo` and the `todowrite` tool to maintain a structured project task list.

## 🔄 Project Lifecycle

1.  **Onboarding:** Run `/onboard` to get a high-signal overview of the repository.
2.  **Scaffolding:** Use `/scaffold` to initialize new project components with modern tooling.
3.  **Iterative Development:** Follow the Discovery -> Plan -> Execute cycle for every feature.
4.  **Quality Control:** Rely on the `pre-commit` hook to maintain codebase integrity.
5.  **Releasing:** Use `/release` to automate versioning, changelog updates, and git tagging.

---

*Next: See [Deployment & Setup](deploy.md) to get started.*
