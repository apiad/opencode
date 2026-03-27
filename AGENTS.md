# AGENT.md — Core Agent Constitution

This file is injected into every agent. It defines universal mandates,
conventions, and registries that apply everywhere.

---

## Universal Mandates

Every agent MUST follow these:

1. **Evidence-based** — Every claim must cite specific sources (files, docs, web)
2. **Explicit before implicit** — State assumptions, plans, and intentions clearly
3. **Read-only default** — Do not modify files unless explicitly authorized
4. **No subagents by default** — Only invoke subagents if explicitly allowed in your agent definition
5. **No file writes without protocol** — Document creation follows your agent's protocol
6. **Context before action** — Always understand before jumping to solutions

---

## Directory Conventions

| Path | Purpose | Created by |
|------|---------|------------|
| `.knowledge/notes/*` | Analysis outputs (research, audits, investigations) | analyze agent |
| `.knowledge/plans/` | Action plans | plan agent |
| `.knowledge/log/` | Chronological activity log | release agent |
| `.experiments/` | Subagent scratch space (gitignored) | subagents |
| `docs/` | Project documentation | build agent |

---

## Tool Assumptions

### Always Available
- `read`, `grep`, `glob` — File inspection
- `edit`, `write` — File modification (requires permission)
- `question` — Request user clarification

### External Dependencies
| Tool | Used by | Required? |
|------|---------|-----------|
| `git` | release, build | Yes |
| `gh` | analyze (todo) | No |
| `make` | build, release | Yes |
| `uv`/`npm`/`cargo` | project-specific | No |

---

## Primary Agent Registry (Modes)

| Agent | Purpose | Permissions |
|-------|---------|-------------|
| `analyze` | Understand, investigate, research | Read-only on project files; write to `.knowledge/notes/` |
| `plan` | Decide approach, design architecture | Read-only on project files; write to `.knowledge/plans/` |
| `build` | Execute, implement, create | Full write access to project files |
| `release` | Finalize, commit, publish | Full write access; git operations |

### Mode Detection

Modes are detected from user intent:
- Questions, research requests → **ANALYZE**
- Strategy discussions, "should we..." → **PLAN**
- Implementation requests → **BUILD**
- Commit/release requests → **RELEASE**

Users can also use explicit `/command` which runs in the corresponding mode.

---

## Subagent Registry

| Subagent | Purpose | Used By | Writes To |
|----------|---------|---------|-----------|
| `scout` | Web research | analyze | Returns to parent only |
| `investigator` | Codebase analysis | analyze, plan | Returns to parent only |
| `tester` | Hypothesis validation | build | `.experiments/tests/` |
| `drafter` | Content drafting | build | `.experiments/drafts/` |
| `critic` | Prose review | analyze, build | Returns to parent only |

### Subagent Rules

1. **Never write to project files** — Only parent agents commit changes
2. **Never write to `.knowledge/`** — Parent owns knowledge architecture
3. **Can write to `.experiments/`** — Scratch space, gitignored
4. **Must return structured output** — Parent synthesizes results
5. **60 second timeout** — Fast feedback
6. **No nesting** — Subagents cannot spawn subagents

---

## Command Registry

### ANALYZE Commands

| Command | Description |
|---------|-------------|
| `/research [topic]` | Deep research with parallel scouts |
| `/audit [scope]` | Comprehensive codebase audit |
| `/investigate [problem]` | Root cause analysis |
| `/todo` | List GitHub issues |
| `/onboard` | Project orientation |

### PLAN Commands

| Command | Description |
|---------|-------------|
| `/plan [description]` | Create structured plan |
| `/scaffold [template]` | Generate project structure |

### BUILD Commands

| Command | Description |
|---------|-------------|
| `/build [feature]` | TCR implementation |
| `/fix [bug]` | Bug fix with regression test |
| `/draft [content]` | Content creation |

### RELEASE Commands

| Command | Description |
|---------|-------------|
| `/commit [message]` | Commit with validation |
| `/publish [version]` | Version, tag, deploy |

### Freestyle vs Commands

- **Freestyle** (natural language) — Agent responds conversationally in detected mode
- **Commands** (`/research`, `/build`, etc.) — Structured workflows with rich prompts

Both work in any mode, but commands add discipline and constraints.

---

## YAML Frontmatter Standard

All `.knowledge/` files must include:

```yaml
---
id: kebab-case-identifier
created: YYYY-MM-DD
modified: YYYY-MM-DD
type: research | audit | investigation | plan | log
status: active | stale | archived
# Optional:
issue: 42
plan: plan-id
sources: [...]
tags: [...]
---
```

---

## Intelligent Decisions (No Hooks)

This framework uses **intelligent decisions** instead of deterministic enforcement:

- **No pre-commit hooks** — Agent decides if journaling is valuable
- **No forced TCR** — Agent explains discipline, user can freestyle
- **No mandatory planning** — Agent suggests, user decides

Agent explains its reasoning. User can override at any time.

---

*Framework Version: 2.0*
