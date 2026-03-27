# Architecture & Systems

The **OpenCode Framework** uses **OpenCode** as its agent orchestration layer. The core framework resides in the `.opencode/` directory.

## 🏗️ The OpenCode Architecture

### Primary Agents (Modes)

| Agent | Purpose |
|-------|---------|
| `analyze` | Research, investigation, and audits |
| `plan` | Strategy and architectural design |
| `build` | TCR implementation discipline |
| `release` | Publishing and versioning |

### Subagents

| Subagent | Purpose |
|----------|---------|
| `investigator` | Codebase architectural analysis |
| `scout` | Web research (parallelizable) |
| `tester` | Hypothesis validation |
| `drafter` | Content creation |
| `critic` | Prose review |
| `general` | General-purpose coding tasks | |

### Commands (`.opencode/commands/`)

Commands define structured, multi-phase workflows that automate the development lifecycle:

| Command | Phase | Description |
|---------|-------|-------------|
| `/research` | Discovery | Deep-dive exploration producing Markdown reports |
| `/audit` | Discovery | Codebase audit for tech debt and architecture |
| `/debug` | Discovery | Scientific, hypothesis-driven forensic investigation |
| `/investigate` | Discovery | Root cause analysis |
| `/plan` | Strategy | Mandatory bridge to execution plans |
| `/build` | Execution | TCR loop implementation |
| `/fix` | Execution | Bug fix with regression prevention |
| `/draft` | Execution | Content creation into finished documents |
| `/onboard` | All | Project orientation for new developers |
| `/scaffold` | All | Project initialization with modern tooling |
| `/commit` | Shipping | Conventional commits with grouped changes |
| `/release` | Shipping | Version bump, changelog, git tagging |
| `/todo` | All | Task management |
| `/note` | All | Journal entry creation |

### The Unified Lifecycle Flow

The framework enforces a strict architectural boundary between discovering what to do and actually doing it. Data flows unidirectionally:

1. **Discovery:** `/research`, `/audit`, `/debug` create read-only artifacts in `.knowledge/notes/`
2. **Strategy:** `/plan` generates actionable roadmaps in `.knowledge/plans/`
3. **Execution:** `/build` (code) or `/draft` (prose) perform actual work

## 🔄 TCR (Test-Commit-Revert) Protocol

The `/build` command enforces a high-discipline development lifecycle through a strict TCR loop:

1. **Pre-flight Verification:** Ensures a clean `main` branch and passing tests.
2. **Isolation:** All work occurs on an auto-generated, kebab-case feature branch.
3. **The Loop (Red-Green-Verify):**
   - **Red:** A failing test is written to define the step's goal.
   - **Green:** Minimal code is written to pass the test.
   - **Verify:** If the test fails, the agent is allowed **one quick fix**. If it fails again, the change is **automatically reverted** (`git checkout .`), preserving the last known stable state.
4. **Integration:** Upon completion, the feature branch is merged, the roadmap is updated, and the branch is deleted.

## 📝 Task Management

Tasks are managed via the `todowrite` tool within agent sessions:

- **Visible task list** for both user and agent
- **State lifecycle:** pending → in_progress → completed
- **Priority levels:** high, medium, low

### Usage

Use the `/todo` command or `todowrite` tool directly to manage tasks.

## 🔍 Scientific Debugging (`/debug`)

The `/debug` command implements a principled approach to problem-solving:

1. **Status & Context Analysis:** Gather error logs, stack traces, and recent changes.
2. **Hypothesis Formulation:** Propose a specific root cause hypothesis.
3. **Isolated Testing:** Create a temporary diagnostic branch (`debug/hyp-*`).
4. **RCA Synthesis:** Generate a Root Cause Analysis report.

## ⚓ Pre-Commit Validation

The framework uses a timestamp-based git hook to enforce journaling:

- **Hook location:** `.opencode/tools/pre-commit.py`
- **Install:** `make install-hooks`
- **Rule:** Journal entry timestamp must be newer than file modifications

## 📁 Directory Structure

```
.opencode/            # Framework runtime (agents, commands, tools)
├── agents/          # Primary agent definitions
│   └── subagents/  # Specialized subagents
├── commands/        # High-level commands
├── tools/           # Utilities (pre-commit.py, etc.)
├── style-guide.md   # Prose style rules
└── README.md        # Framework self-documentation

.knowledge/
├── plans/           # Saved execution plans
├── notes/           # Research artifacts and analysis notes
├── log/             # Daily journal entries (YYYY-MM-DD.yaml)
└── drafts/          # Content drafts

tasks.yaml           # Project roadmap (managed by task tool)
```

## ⚙️ Technology Stack

- **CLI Engine:** OpenCode (Node.js-based agent framework)
- **Core Automation:** Python (Scripts in `.opencode/tools/`)
- **Validation & Health:** Make (source of truth for builds/tests)
- **State & Versioning:** Git
- **Documentation:** Markdown (journals, plans, reports)

---

*Next: See [Development & Contribution](develop.md) for the rules of the road.*
