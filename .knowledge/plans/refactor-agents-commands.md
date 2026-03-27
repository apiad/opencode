# Plan: Agent/Command Architecture Refactor

**Date:** 2026-03-26
**Status:** Ready for Execution

## Objective
Refactor `.opencode/agents/` and `.opencode/commands/` to implement a clean separation between thinking modes (primary agents), targeted tasks (subagents), and step-by-step workflows (commands).

## Architecture Summary

### Primary Agents (5) - Thinking Modes
| Agent | Mode | Subagents |
|-------|------|-----------|
| build | Doing - coding, writing, implementing | writer, coder |
| plan | Planning - strategy, formalize discussions | investigator |
| review | Understanding - Q&A, audit, onboard | reviewer |
| brainstorm | Critical thinking - challenges, what-ifs | (none) |
| research | Deep research - exhaustive campaigns | scout |

### Subagents (5) - Targeted Task Workers
| Subagent | Purpose | Returns |
|----------|---------|---------|
| writer | Write/refine specific document sections | content/edits |
| coder | Non-permanent code for hypotheses | scripts, bash, experiments |
| investigator | Answer "what does X?" about codebase | targeted file/component analysis |
| scout | Search web for answers | research findings |
| reviewer | Review phases (structural/substance/linguistic) | review reports |

### Commands (11) - Step-by-Step Workflows
| Command | Agent | Purpose |
|---------|-------|---------|
| /build | build | Full TCR implementation |
| /commit | build | Group & commit changes |
| /release | build | Version bump, changelog, tag, push |
| /draft | build | Write/refine documents |
| /debug | build | Test hypotheses (uses coder subagent) |
| /scaffold | plan | Project architecture (no business logic) |
| /onboard | review | Orient to project |
| /docs | review | Generate documentation |
| /audit | review | Deep codebase audit (renamed from maintenance) |
| /issues | build | GitHub integration |
| /plan | plan | Formalize discussions into a plan |

## Files to DELETE (6 files)
- `.opencode/agents/builder.md`
- `.opencode/agents/write.md`
- `.opencode/agents/query.md`
- `.opencode/agents/debugger.md`
- `.opencode/agents/review.md`
- `.opencode/commands/task.md`

## Implementation Order
1. Delete 6 files
2. Create/update 5 primary agents
3. Create/update 5 subagents
4. Create/update 11 commands
5. Update opencode.json if needed
