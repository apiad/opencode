---
description: Group and commit uncommitted changes using Conventional Commits
agent: ship
---

Group and commit uncommitted changes.

### Preconditions
- Git hook passes (pre-commit validation)
- If hook fails → redirect to build mode with `/fix`

### Workflow

1. **Analyze changes**:
   - Use `git status` and `git diff` to identify all modified and untracked files
   - Group files that are related to a single logical change

2. **Propose**:
   - Present proposed commit groups with Conventional Commits format: `<type>(<scope>): <subject>`
   - Use `question` to confirm before proceeding

3. **Execute**:
   - For each group: stage files, commit with proposed message

4. **Journal**:
   - Use `journal add` to update journal after commits

If no changes to commit, inform the user.

### Constraints
- Never touch source code — commit metadata only
- Enforce pre-commit hook before proceeding
