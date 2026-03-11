# Execution Plan: Conditional 'make' Hook with State Persistence

This plan outlines the modifications needed to implement conditional execution for the `.gemini/hooks/make.py` hook. The goal is to prevent redundant test/lint runs by only executing `make` when changes have been detected in the workspace since the last successful run.

## Objective
Modify the `make` hook logic to use file modification times (`mtime`) and `git` status to determine if a full validation run is necessary.

## Architectural Impact
- **Efficiency:** Reduces resource consumption and agent wait times by skipping redundant validations.
- **State Management:** Introduces a lightweight persistence mechanism in `.gemini/last_make_run`.
- **Environment Agnostic:** Decouples the hook from the Python environment manager (`uv`) by calling `make` directly.

## File Operations

### 1. Create `.gemini/.gitignore`
- **Action:** Create a new file at `.gemini/.gitignore`.
- **Content:**
  ```text
  last_make_run
  ```
- **Rationale:** Ensures that the state file used for tracking the last successful run is not committed to the repository.

### 2. Modify `.gemini/hooks/make.py`
- **Action:** Update the existing hook script to include change detection logic.
- **Key Logic Changes:**
    - Calculate `STATE_FILE` path relative to the hook's directory (likely `.gemini/last_make_run`).
    - Use `git status --porcelain` or `git ls-files` to identify modified and untracked files.
    - Compare file `mtime` against the timestamp stored in `last_make_run`.
    - Run `make` directly (without `uv run`).
    - Update `last_make_run` with the current Unix timestamp only upon successful execution.
    - Return an `allow` decision with a skip message if no changes are detected.

### 3. Update `TASKS.md`
- **Action:** Add a new entry to the `Archive` or `Active Tasks` section.
- **Task Description:** `Implement conditional 'make' hook execution based on file modification times.`

## Step-by-Step Execution

### Step 1: Initialize State Ignoring
1. Create `.gemini/.gitignore`.
2. Append `last_make_run` to it.

### Step 2: Implement the Enhanced Hook
1. Open `.gemini/hooks/make.py`.
2. Replace the current `main` function and script logic with the following implementation:
    - Add `import time`.
    - Define `STATE_FILE` path.
    - Implement logic to read/write the timestamp.
    - Use `subprocess` to get modified and untracked files from `git`.
    - Implement `should_run_make()` to perform the comparison.
    - Refactor `main()` to use `should_run_make()` and call `make` directly.

### Step 3: Verify and Document
1. Update `TASKS.md` to reflect the completed work.
2. Ensure PEP 257 docstrings are maintained/added for clarity.

## Testing Strategy

### Automated/Manual Validation Scenarios
1.  **Fresh Workspace:** Remove `.gemini/last_make_run`. Verify that `make` runs correctly.
2.  **No Changes:** Run the hook again immediately. Verify that it skips `make`.
3.  **Modification:** Update a source file. Verify that `make` runs.
4.  **Addition:** Create a new dummy file. Verify that `make` runs.
5.  **Failure Recovery:** Modify a file so that `make` fails. Verify that `last_make_run` is **not** updated.
