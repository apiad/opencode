# Architecture & Systems

The **Gemini CLI Opinionated Framework** uses **OpenCode** as its agent orchestration layer. The core framework resides in the `.opencode/` directory.

## 🏗️ The OpenCode Architecture

### Primary Agents (`.opencode/agents/`)

| Agent | Purpose |
|-------|---------|
| `plan` | Planning workflow - analyzes codebase, generates plans to `plans/` |
| `build` | TCR coding workflow - manages tasks and delegates to builder |
| `query` | Default agent for repo Q&A - invokes subagents as needed |
| `research` | Research campaigns - parallel scout work with writer summaries |
| `brainstorm` | Critical thinking and risk assessment |
| `write` | Prose composition and refinement |
| `review` | Multi-phase editorial review |

### Subagents (`.opencode/agents/subagents/`)

| Subagent | Purpose |
|----------|---------|
| `builder` | TCR grunt coding (test-driven implementation) |
| `scout` | Web research (parallelizable) |
| `investigator` | Codebase architectural analysis |
| `writer` | Prose refinement |
| `reviewer` | Editorial audits |
| `debugger` | RCA investigation |

### Commands (`.opencode/commands/`)

Commands define structured, multi-phase workflows that automate the development lifecycle:

| Command | Phase | Description |
|---------|-------|-------------|
| `/research` | Discovery | Deep-dive exploration producing Markdown reports |
| `/maintenance` | Discovery | Non-destructive codebase audit |
| `/review` | Discovery | Multi-phase linguistic and structural audit |
| `/debug` | Discovery | Scientific, hypothesis-driven forensic investigation |
| `/brainstorm` | Discovery | Interactive critical-thinking sessions |
| `/plan` | Strategy | Mandatory bridge to execution plans |
| `/task` | Execution | TCR loop and feature branch isolation |
| `/draft` | Execution | Content transformation into finished documents |
| `/document` | Execution | Documentation synchronization |
| `/onboard` | All | Project orientation for new developers |
| `/scaffold` | All | Project initialization with modern tooling |
| `/commit` | Shipping | Conventional commits with grouped changes |
| `/release` | Shipping | Version bump, changelog, git tagging |
| `/issues` | All | GitHub CLI integration |

### The Unified Lifecycle Flow

The framework enforces a strict architectural boundary between discovering what to do and actually doing it. Data flows unidirectionally:

1. **Discovery:** `/research`, `/maintenance`, `/review`, `/debug` create read-only artifacts
2. **Strategy:** `/plan` generates actionable roadmaps in `plans/`
3. **Execution:** `/task` (code) or `/draft` (prose) perform actual work

## 🔄 TCR (Test-Commit-Revert) Protocol

The `/task work` command enforces a high-discipline development lifecycle through a strict TCR loop:

1. **Pre-flight Verification:** Ensures a clean `main` branch and passing tests.
2. **Isolation:** All work occurs on an auto-generated, kebab-case feature branch.
3. **The Loop (Red-Green-Verify):**
   - **Red:** A failing test is written to define the step's goal.
   - **Green:** Minimal code is written to pass the test.
   - **Verify:** If the test fails, the agent is allowed **one quick fix**. If it fails again, the change is **automatically reverted** (`git checkout .`), preserving the last known stable state.
4. **Integration:** Upon completion, the feature branch is merged, the roadmap is updated, and the branch is deleted.

## 📝 Procedural Task Management

The `TASKS.md` file is managed exclusively via `.opencode/tools/task.py`:

- **Single source of truth** for project roadmap
- **State lifecycle:** `add` (Todo) → `start` (In Progress) → `archive` (Done)
- **Never edit `TASKS.md` by hand** — always use the task script

### Usage

```bash
python .opencode/tools/task.py --help
python .opencode/tools/task.py add --label "Feature X" --description "..."
python .opencode/tools/task.py start --task-id G.1
python .opencode/tools/task.py archive --task-id G.1
```

## 🔍 Scientific Debugging (`/debug`)

The `/debug` command implements a principled approach to problem-solving:

1. **Status & Context Analysis:** Gather error logs, stack traces, and recent changes.
2. **Hypothesis Formulation:** Propose a specific root cause hypothesis.
3. **Isolated Testing:** Create a temporary diagnostic branch (`debug/hyp-*`).
4. **RCA Synthesis:** Generate a Root Cause Analysis report.

## ⚓ Pre-Commit Validation

The framework uses a timestamp-based git hook to enforce journaling:

- **Hook location:** `.opencode/tools/git-precommit.py`
- **Install:** `make install-hooks`
- **Rule:** Journal entry timestamp must be newer than file modifications

## 📁 Directory Structure

```
.opencode/
├── agents/          # Primary agent definitions
│   └── subagents/  # Specialized subagents
├── commands/        # High-level commands
├── tools/           # Utilities (task.py, journal.py, git-precommit.py)
└── style-guide.md   # Prose style rules

plans/               # Saved execution plans
journal/             # Daily journal entries (YYYY-MM-DD.md)
research/           # Research artifacts
drafts/             # Content drafts
TASKS.md            # Project roadmap (managed by task.py)
```

## ⚙️ Technology Stack

- **CLI Engine:** OpenCode (Node.js-based agent framework)
- **Core Automation:** Python (Scripts in `.opencode/tools/`)
- **Validation & Health:** Make (source of truth for builds/tests)
- **State & Versioning:** Git
- **Documentation:** Markdown (journals, plans, reports)

---

*Next: See [Development & Contribution](develop.md) for the rules of the road.*
