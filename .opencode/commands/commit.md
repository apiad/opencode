---
description: Group and commit uncommitted changes individually using Conventional Commits.
agent: build
---

Analyze all current uncommitted changes (including untracked files), group them into logical features, bugfixes, etc., and commit them one by one.

**Procedure:**
1. **Analyze Changes:**
   - Use `git status` and `git diff` to identify all modified and untracked files.
   - Group files that are related to a single logical change (e.g., feature, tests, docs).
2. **Proposal:**
   - Present the proposed commit groups and their commit messages to the user for approval.
   - Use Conventional Commits format: `<type>(<scope>): <subject>`.
   - Use `question` to confirm with the user before proceeding with the commits.
3. **Execution:**
   - After confirmation, for each group:
     a. Stage the files.
     b. Commit with the proposed message.
   - Report the successful commits.

If there are no changes to commit, let the user know.
