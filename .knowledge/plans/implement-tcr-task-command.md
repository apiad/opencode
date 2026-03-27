# Plan: Implement TCR Workflow for `/task`

## Objective
Refactor the `task` command in `.gemini/commands/task.toml` to prioritize a strict Test-Commit-Revert (TCR) protocol for the 'Work' action, ensuring all development happens on feature branches with granular, verified commits.

## Context & Requirements
- **Strict Pre-requisites:** Clean working tree, on `main` branch, all tests pass (`make`).
- **Isolation:** All work must occur on an auto-generated feature/bugfix branch.
- **TCR Protocol:**
  - Break tasks into granular steps.
  - **Red:** Write a failing test and verify failure.
  - **Green:** Implement solution.
  - **Commit:** If tests pass, commit immediately.
  - **Revert:** If tests fail (after brief leeway), revert to the last green state.
- **User Interaction:** Frequent checkpoints using `ask_user` after each step and before final merge.
- **Finalization:** Full test run on branch before merging/rebasing to `main`.

## Proposed Changes

### 1. Refactor `.gemini/commands/task.toml`
Update the `Action: Work` section of the prompt to explicitly define the TCR workflow phases:

- **Phase 1: Pre-flight Verification**
  - Use `git status --porcelain` to ensure a clean tree.
  - Use `git branch --show-current` to ensure the branch is `main`.
  - Run `make` to establish a green baseline.
- **Phase 2: Task Setup**
  - Update `TASKS.md` status.
  - Generate a kebab-case branch name from the task description.
  - Create and switch to the branch (`git checkout -b <branch-name>`).
- **Phase 3: The TCR Loop**
  - Divide the task into small, testable increments.
  - For each increment:
    1. Write a failing test.
    2. Run tests to confirm failure.
    3. Implement the minimal code to pass.
    4. Run `make`.
    5. If pass: `git add . && git commit -m "Step: <step-description>"`.
    6. If fail: Attempt quick fix; if failure persists, `git checkout .` to revert.
    7. Use `ask_user` to report status and confirm the next increment.
- **Phase 4: Integration**
  - Run the full test suite one final time.
  - Use `ask_user` to request permission to merge/rebase.
  - Perform the merge/rebase to `main`, switch back to `main`, and clean up the feature branch.

## Verification Strategy
- **Logical Consistency:** Review the prompt to ensure instructions are unambiguous and cover all edge cases (e.g., failure during merge).
- **Manual Walkthrough:** Simulate the workflow with a dummy task to verify the agent correctly identifies when to commit versus revert.
- **Git State Audit:** Confirm that the final state results in a clean `main` branch with all tests passing.
