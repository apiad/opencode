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
| `plans/*.md` | Planning outputs | plan agent |
| `research/<topic>/*` | Research campaigns | research agent |
| `journal/<date>.yaml` | Daily journal entries | any agent |
| `todo.yaml` | Task list | any agent |
| `docs/*` | Project documentation | review agent |

---

## Tool Assumptions

### Always Available
- `read`, `grep`, `glob` — File inspection
- `edit`, `write` — File modification (requires permission)
- `question` — Request user clarification

### Custom Tools
- `journal` — Add/list journal entries (action: add or list)
- `todo` — Task management (action: add, start, cancel, archive, attach-plan, list)

### External Dependencies
| Tool | Used by | Required? |
|------|---------|-----------|
| `git` | ship, build | Yes |
| `gh` | ship, issues | No |
| `make` | ship (pre-commit hook) | Yes |
| `uv`/`npm`/`cargo` | project-specific | No |

---

## Subagent Registry

| Subagent | Purpose | Allowed in |
|----------|---------|------------|
| `investigator` | Codebase structure analysis | review, plan |
| `reviewer` | Structured document review (3 phases) | review |
| `scout` | Web search and fetch | research |
| `writer` | Document section drafting | build |
| `coder` | Hypothesis testing with code | build |

### Subagent Invocation Protocol

When invoking a subagent:
1. Provide clear, specific instructions
2. Specify expected output format
3. Do NOT chain subagents (no subagent calling subagent)

---

## Command Registry

### Mode Switches
| Command | Agent | Behavior |
|---------|-------|----------|
| `/brainstorm` | brainstorm | New in brainstorm, infer context or ask |
| `/plan` | plan | New in plan, infer context or ask |
| `/research` | research | New in research, infer context or ask |
| `/review` | review | New in review, infer context or ask |
| `/build` | build | New in build, infer context or ask |
| `/ship` | ship | New in ship, infer context or ask |

### One-offs (run in their mode)
| Command | Mode | Behavior |
|---------|------|----------|
| `/scaffold` | plan | Create project architecture |
| `/audit` | review | Deep codebase audit |
| `/onboard` | review | Orient new developer |
| `/docs` | review | Generate/update documentation |
| `/fix` | build | Hypothesis testing & issue resolution |
| `/draft` | build | Write/refine documents |
| `/commit` | ship | Group and commit changes |
| `/release` | ship | Version bump, tag, publish |
| `/issues` | ship | GitHub issue management |
