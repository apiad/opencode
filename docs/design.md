# Architecture & Systems

The **Gemini CLI Opinionated Framework** is not just a collection of scripts; it is an integrated system designed to empower AI agents while enforcing rigorous engineering standards.

## 🏗️ The Core Architecture

The project's "brain" resides in the `.gemini/` directory, which is organized into four primary systems:

### 1. The Hook System (`.gemini/hooks/`)
Hooks are Python-based scripts that intercept the Gemini CLI turn lifecycle. They are the framework's primary enforcement mechanism.
- **`session.py`:** Initializes the session and provides a project summary to the agent.
- **`journal.py`:** Enforces the mandatory daily journaling requirement for all significant changes.
- **`make.py`:** Automatically runs the `makefile` (tests/linting) to prevent regressions.
- **`cron.py`:** Synchronizes the project's background tasks with systemd user timers.
- **`utils.py`:** Provides a shared set of utilities for git status analysis and communication with the CLI.

### 2. The Command System (`.gemini/commands/`)
Commands define structured, multi-phase workflows that automate the development lifecycle. Each command is a TOML file containing specific instructions and context for the agent.
- **`/plan`:** An interactive workflow that transitions between clarification, analysis, and strategy generation.
- **`/research`:** A deep-dive exploration that produces exhaustive reports in the `research/` directory.
- **`/debug`:** Activates a forensic investigation mode for root-cause analysis.
- **`/docs`:** Analyzes the codebase and project state to update the documentation suite.
- **`/task`:** The primary execution engine, managing `TASKS.md` and enforcing the strict TCR (Test-Commit-Revert) loop and feature branch isolation.

### 🔌 Synergistic Validation
The `/task` command works in tandem with the `make.py` hook to ensure a "no-regression" policy. While `/task` enforces testing during the Red-Green-Verify cycle, the `make.py` hook provides a final, infrastructure-level check after every turn. If any turn (manual or automated) results in broken code, the framework immediately detects it, ensuring that the repository's "last known state" is always stable.

### 3. Specialized Agents (`.gemini/agents/`)
Instead of a single "do-it-all" AI, the framework delegates tasks to specialized sub-agents with restricted toolsets and focused personas (e.g., `planner`, `debugger`, `editor`, `reporter`). This ensures higher reliability and more consistent results.

### 4. State Management
The framework maintains internal state to optimize operations and ensure continuity:
- **`.gemini/last_make_run`**: Stores the timestamp of the last successful validation, allowing the framework to skip redundant tests.
- **`.gemini/last_journal_update`**: Tracks when the journal was last updated to intelligently enforce the journaling requirement.
- **`.gemini/settings.json`**: Configures the framework's global behavior and hook execution order.

## ⚙️ The Technology Stack

- **CLI Engine:** Gemini CLI (Interactive Node.js-based terminal).
- **Core Automation:** Python (Hooks and specialized scripts).
- **Validation & Health:** Make (Central source of truth for builds and tests).
- **State & Versioning:** Git (Change detection and history tracking).
- **Documentation:** Markdown (Universal format for journals, plans, and reports).

---

*Next: See [Development & Contribution](develop.md) for the rules of the road.*
