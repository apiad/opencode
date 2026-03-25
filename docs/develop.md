# Development & Contribution

The **Gemini CLI Opinionated Framework** enforces a high-discipline development lifecycle. Whether you are a human or an AI contributor, adherence to these standards is mandatory.

## 🔄 The Mandatory Workflow Lifecycle

Every non-trivial change must follow this strict three-phase process:

```text
[Phase 1: Discovery] -> [Phase 2: Strategy] -> [Phase 3: Execution]
(Audit/Research)        (Planning Bridge)      (Tasks/Drafting)
```

### 1. Discovery & Audit (Read-Only)

Before proposing a change, you must gather context and identify risks. Use the specialized discovery commands:
- **`/research`**: For domain knowledge and external libraries.
- **`/maintenance`**: To audit the codebase for technical debt.
- **`/debug`**: To perform a root-cause analysis (RCA) on a bug.
- **`/review`**: To audit a document's structure and prose.

*Crucially, these commands are read-only; they produce artifacts (`research/`, `*.review.md`), not code changes.*

### 2. Strategic Planning (The Bridge)

A feature or fix is not considered "active" until a persistent Markdown plan has been created in the `plans/` directory. Use the `/plan` command to synthesize the artifacts generated in Phase 1 into an actionable strategy, and synchronize it with `TASKS.md`.

### 3. Execution & Validation (Side-Effects)

Once a plan is approved, you move to execution. This is the **only** phase where files are modified.

#### For Code: The TCR Protocol
The `/task` command is the primary tool for repository execution:
- **`/task create`**: Adds a new task using the `task.py` script.
- **`/task work on ...`**: Implements a strict **TCR (Test-Commit-Revert)** protocol to ensure high-velocity, high-quality code. The orchestrator automatically uses `task.py` to mark the task as in-progress.
- **`/task report`**: Provides a summary of the roadmap and current priorities.
- **`/task update`**: Updates the status or plan-path of an existing task via the script.

**CLI-First Roadmap Discipline:**
The project roadmap (`TASKS.md`) must **never** be edited by hand. All task operations must be performed via the `.opencode/tools/task.py` script or the corresponding `/task` actions. This ensures structural integrity and a verifiable audit trail.

#### **The TCR Loop (Work Action)**

1.  **Phase 1 (Pre-flight Verification):** The agent verifies that the working tree is clean, the current branch is `main`, and `make test` passes as a baseline.
2.  **Phase 2 (Task Isolation):** A dedicated feature branch (e.g., `feature/task-name`) is auto-generated and checked out. All work occurs on this isolated branch.
3.  **Phase 3 (The Red-Green-Verify Loop):** For every granular step of the implementation:
    - **Red:** Write a failing test and verify failure with `make test`.
    - **Green:** Implement the minimal code to pass the test.
    - **Verify:** Run `make test`.
        - **Pass:** `git commit` the step.
        - **Fail:** Attempt **one quick fix**. If it fails again, the change is **automatically reverted** (`git checkout .`).
4.  **Phase 4 (Integration):** Once all steps are complete, the agent performs a final test run. Upon approval, the branch is merged into `main` and deleted.

### 4. Forensic Investigation (The Scientific Debugging Discipline)

When a bug is detected, the `/debug` command enforces a structured, scientific investigation:

1.  **Phase 1 (Status & Context):** Analyze the current environment and gather reproduction information.
2.  **Phase 2 (Hypothesis Formulation):** Formulate a specific hypothesis for the root cause.
3.  **Phase 3 (Isolated Testing):** Test the hypothesis on a temporary diagnostic branch (`debug/hyp-*`). Diagnostic code should be minimal and focused.
4.  **Phase 4 (Synthesis & RCA):** Summarize the investigation into a **Root Cause Analysis (RCA)** report. This report serves as the documentation for the subsequent fix.

### 5. Audit & Documentation (NEW)

Before merging or committing any final change, the work **must** be documented in the daily journal. This is enforced by a **timestamp-based git hook**. Use the following tool to satisfy the requirement:

```bash
python3 .opencode/tools/journal.py 'one-line description of the work'
```

Failure to do this will block your commit or turn execution.

## ✅ Testing & Quality Standards

- **Automated Context Minification:** To ensure maximum token efficiency and prevent context saturation during long sessions, the framework automatically identifies and replaces redundant `<instruction>` blocks from previous turns with a placeholder. Only the *latest* instruction is passed to the model in its full form, ensuring the agent stays focused on the current task while maintaining structural operational context.
- **Agent-Driven Validation:** This project maintains a **minimalist, transient testing philosophy**.
 Instead of a static suite of thousands of unit tests, it relies on high-discipline agent execution and **Grounded Experimentation** to verify behavior in real-time.
- **On-the-Fly Verification:** During the mandatory TCR (Test-Commit-Revert) loop, the agent is required to write specific, temporary test cases (e.g., `test_feature_x.py`) that verify the granular step being implemented.
- **Source of Truth:** The `makefile` is the central definition of project health. Even if it initially points to an empty `test` target, it serves as the hook point for the agent's automated validation.
- **The TCR Mandate:** The primary mechanism for ensuring "Green-only" development is the mandatory **Test-Commit-Revert** loop. If a change fails its temporary verification, it is instantly reverted, ensuring the `main` branch remains a "known-good" state.

## 🧠 Codifying Knowledge with Skills

The `/learn` command is the primary tool for expanding the project's long-term memory. When mastering a new technology, follow this workflow:

### 1. Grounded Learning Lifecycle
The agent follows a 4-phase process: **Audit** (environment check), **Strategic Mapping** (learning objectives), **Execution** (real-world experimentation), and **Codification**.

### 2. Mandatory Frontmatter (`SKILL.md`)

The root `SKILL.md` file **must** include a YAML block at the top. This allows the framework to autonomously recognize and activate the skill in future sessions.

```yaml
---
name: <unique-identifier>
description: <concise-summary-for-autonomous-activation>
---
```

### 3. Asset Management

All successful experiment scripts and idiomatic examples generated during the `/learn` phase should be moved to the `assets/` subdirectory within the skill folder. These serve as verified reference points for future agent turns.

## 🌲 Git & Source Control

### 1. Clean Working Tree

The framework requires a clean working tree for critical actions. Commit often to avoid merge conflicts or large, unmanageable diffs.

### 2. Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

- **`feat:`**: A new feature for the user (e.g., `feat(hooks): add notify-send alert`).
- **`fix:`**: A bug fix for the user.
- **`docs:`**: Documentation-only changes.
- **`chore:`**: Maintenance, dependencies, or internal tooling updates (e.g., `chore(release): version 0.17.1`).
- **`refactor:`**: Code changes that neither fix a bug nor add a feature.

### 3. Commit Scoping

When possible, provide a scope to the commit message (e.g., `feat(onboard): add documentation discovery`).

## ✍️ Documentation Style

- **Markdown:** All documentation and logs must be in GitHub-flavored Markdown.
- **Kebab-case:** Use kebab-case for all filenames in the `docs/`, `plans/`, and `research/` directories.
- **Direct & Technical:** Documentation should be concise, high-signal, and technically rigorous.

---

*Return to the [Project Overview](index.md).*
