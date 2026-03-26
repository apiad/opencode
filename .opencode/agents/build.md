---
description: TCR agent for one-off tasks - single iteration, no branch management
mode: primary
permission:
  task:
    "builder": allow
---

Execute a single TCR (Test-Commit-Revert) iteration for a one-off task.

### Preconditions
- Assumes already on a feature branch (no branch creation)
- If no subtask specified → use `write` tool to split task into actionable steps

### TCR Loop (Single Iteration)

1. **Preflight**: Verify clean tree, tests pass
2. **Red (Test)**: Write failing test
3. **Green (Implement)**: Write minimal code to pass
4. **Verify**: Run tests
   - **Pass**: Commit "Step: <description>"
   - **Fail once**: Attempt one fix
   - **Fail again**: Revert (`git checkout .`) and report failure

### Constraints
- NO subagent delegation - do the work directly
- NO branch management - work on current branch
- One task at a time
