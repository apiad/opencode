---
id: taskflow-implementation
created: 2026-03-28
modified: 2026-03-28
type: plan
status: done
expires: 2026-04-04
phases:
  - name: Scaffold taskflow app
    done: false
    goal: Create runnable microcli app with basic structure
  - name: Implement YAML storage layer
    done: false
    goal: Task CRUD operations with YAML persistence
  - name: Implement core commands
    done: false
    goal: All 5 commands (create, list, start, done, delete) functional
  - name: Add output formatting
    done: false
    goal: Kanban-style output with next-step hints
  - name: Add integration tests
    done: false
    goal: Tests for all commands pass
---

# Plan: taskflow - Task Management CLI for AI Agents

## Context

Create a simple task management CLI tool (`taskflow`) that serves as a guardrail for AI agents during development. The tool provides structure without intelligence - agents are smart, taskflow just keeps them honest about what they're doing.

Based on microcli framework. Storage: `tasks.yaml` in cwd. Commands: create, list, start, done, delete.

## Design Summary

**Task fields**: id (auto-int), title, description, status (todo|in-progress|done), created, started, finished

**Storage**: `tasks.yaml` - auto-created if missing, YAML format

**Commands**:
- `create "title" [--description TEXT]` → Task created, hint to run `start`
- `list [--status STATUS] [--search TEXT]` → Kanban-style grouped output
- `start N` → Begin task, hint to run `done`
- `done N` → Complete task
- `delete N` → Remove task

## Phases

### Phase 1: Scaffold taskflow app

**Goal:** Create runnable microcli app with basic structure

**Deliverable:** `examples/taskflow/taskflow.py` - a microcli app that runs and responds to `--help`

**Done when:**
- [ ] File exists at `examples/taskflow/taskflow.py`
- [ ] `python taskflow.py --help` shows usage
- [ ] No commands registered yet (scaffold only)

**Depends on:** None

---

### Phase 2: Implement YAML storage layer

**Goal:** Task CRUD operations with YAML persistence

**Deliverable:** Helper functions for reading/writing tasks.yaml

**Done when:**
- [ ] `tasks.yaml` auto-created if missing (on any command)
- [ ] `load_tasks()` returns list of task dicts
- [ ] `save_tasks(tasks)` writes YAML correctly
- [ ] `next_id()` returns next auto-increment ID

**Depends on:** Phase 1

---

### Phase 3: Implement core commands

**Goal:** All 5 commands functional

**Deliverable:** Working create, list, start, done, delete commands

**Done when:**
- [ ] `create "Fix bug" --description "Login page"` creates task
- [ ] `list` shows all tasks grouped by status
- [ ] `list --status todo` filters correctly
- [ ] `list --search "bug"` filters by text match
- [ ] `start 1` changes status to in-progress, sets started timestamp
- [ ] `done 1` changes status to done, sets finished timestamp
- [ ] `delete 1` removes task from list

**Depends on:** Phase 2

---

### Phase 4: Add output formatting

**Goal:** Human-readable, consistent output that's also AI-friendly

**Deliverable:** Kanban-style list output with next-step command hints

**Done when:**
- [ ] List shows tasks grouped: TODO, IN PROGRESS, DONE
- [ ] Tasks displayed with ID, title, description (if exists)
- [ ] After `create`: "Task #N created. Run `taskflow start N` to begin work."
- [ ] After `start`: "Task #N started. Run `taskflow done N` when finished."
- [ ] After `done`: "Task #N completed."
- [ ] After `delete`: "Task #N deleted."
- [ ] After `list` (empty): Shows friendly message with create hint

**Depends on:** Phase 3

---

### Phase 5: Add integration tests

**Goal:** All commands tested via integration tests

**Deliverable:** `examples/taskflow/tests/` with integration tests

**Done when:**
- [ ] `test_create_command` - creates task, verifies in YAML
- [ ] `test_list_empty` - shows empty state message
- [ ] `test_list_with_tasks` - shows Kanban output
- [ ] `test_list_filter_status` - filters work
- [ ] `test_list_filter_search` - search works
- [ ] `test_start_command` - status and timestamp updated
- [ ] `test_done_command` - status and timestamp updated
- [ ] `test_delete_command` - task removed
- [ ] All tests pass

**Depends on:** Phase 4

---

## Success Criteria

1. Agent can run `taskflow create "My task"` without reading any docs
2. Agent can run `taskflow list` and understand the output
3. Agent knows what to do next after each command (hints work)
4. `tasks.yaml` is valid YAML that agent can read directly
5. All integration tests pass

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| YAML formatting issues with timestamps | Low | Use ISO format strings, test round-trip |
| microcli command parsing edge cases | Low | Use simple patterns, test edge cases |
| ID collision after delete | Low | IDs are sequential, gaps are okay |
| Concurrent access (two agents) | Medium | Single-user assumption, not a concern for now |

## Technical Notes

- Based on microcli framework (`from microcli import command, main, ok, fail, info, read, write`)
- Uses `from microcli import yaml` for YAML operations
- Commands use `@command` decorator
- Arguments: no default = positional, has default = optional flag
- Command names: underscores → hyphens (e.g., `create_with_desc` → `create-with-desc`)

## Related

- Research: `ai-agent-friendly-cli-patterns` - patterns that informed this design
- Framework: microcli at `lib/microcli/`
