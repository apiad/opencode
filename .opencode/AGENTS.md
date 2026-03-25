# OpenCode Agents

This file defines the project-specific instructions and configuration for OpenCode agents.

## Project Overview

This is a personal starter project using OpenCode for AI-assisted development.

## Agent Architecture

### Primary Agents (Thinking Modes)
- **plan**: Planning workflow - analyzes codebase, generates plans saved to `plans/`
- **build**: TCR (Test-Commit-Revert) coding workflow - manages tasks and delegates to builder
- **query**: Default agent for repo Q&A - invokes subagents as needed
- **research**: Research campaigns - parallel scout work with writer summaries
- **brainstorm**: Critical thinking and risk assessment
- **write**: Prose composition and refinement
- **review**: Multi-phase editorial review

### Subagents (Specialized Tasks)
- **builder**: TCR grunt coding (test-driven implementation)
- **scout**: Web research (parallelizable)
- **investigator**: Codebase architectural analysis
- **writer**: Prose refinement
- **reviewer**: Editorial audits
- **debugger**: RCA investigation

## Workflow Conventions

### Task Management
- Use the `task` tool to manage TASKS.md
- All task modifications must go through the tool
- Task format: `- [status] **ID** Label: Description (Complexity: X) [Deps: Y] (See plan: Z)`

### Journaling
- Use the `journal` tool to add daily entries
- Format: `[YYYY-MM-DDTHH:MM:SS] - description`
- Journal entries must be newer than recent changes for commits

### Planning
- Plans are saved to `plans/` directory
- Filenames: kebab-case (e.g., `plans/implement-auth.md`)
- Link plans to tasks via `task` tool

### Pre-commit Validation
- Run `git_precommit` tool before committing
- Validates: tests pass + journal is current

## Directory Structure
```
.opencode/
├── agents/          # Agent definitions
├── commands/        # High-level commands
├── tools/           # Custom tools
└── style-guide.md   # Prose style rules

plans/               # Saved plans
journal/             # Daily journal entries
research/           # Research assets
TASKS.md            # Project roadmap
```
