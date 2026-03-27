# Execution Plan: Conditional Journal Hook Enforcement

This plan outlines the modifications needed to implement conditional enforcement for the `.gemini/hooks/journal.py` hook. The goal is to only require a journal update if new changes have been detected in the workspace since the last recorded journal update.

## Objective
Modify the `journal` hook logic to use file modification times (`mtime`) and `git` status to determine if a journal update is strictly necessary.

## Architectural Impact
- **Efficiency:** Reduces friction by only requiring journal entries when new work has actually been performed.
- **State Management:** Introduces a lightweight persistence mechanism in `.gemini/last_journal_update`.

## File Operations

### 1. Modify `.gemini/.gitignore`
- **Action:** Add `last_journal_update` to the existing `.gemini/.gitignore`.
- **Content:**
  ```text
  last_make_run
  last_journal_update
  ```

### 2. Modify `.gemini/hooks/journal.py`
- **Action:** Update the existing hook script to include change detection and timestamp logic.
- **Key Logic Changes:**
    - Define `STATE_FILE` path (e.g., `.gemini/last_journal_update`).
    - Use `git status --porcelain=v1` to identify all modified and untracked files.
    - Implement `get_last_journal_update()` and `update_last_journal_update()` for state persistence.
    - If the current daily journal is in the list of modified files, update the `STATE_FILE` with the current time and return `allow`.
    - If any other modified or untracked file has an `mtime > last_journal_update`, return `deny` with a request to update the journal.
    - Return `allow` if no newer changes are found.

### 3. Update `TASKS.md`
- **Action:** Add a new entry to the `Archive` or `Active Tasks` section.
- **Task Description:** `Implement conditional journal hook enforcement based on file modification times.`

## Step-by-Step Execution

### Step 1: Update State Ignoring
1. Open `.gemini/.gitignore`.
2. Append `last_journal_update` to it.

### Step 2: Implement the Enhanced Hook
1. Open `.gemini/hooks/journal.py`.
2. Replace the current logic with the new implementation:
    - Add `import time`.
    - Define `STATE_FILE`.
    - Implement `should_require_journal_update()` to perform the comparison.
    - Refactor `main()` to use the new logic and update the timestamp when the journal is modified.

### Step 3: Verify and Document
1. Update `TASKS.md` to reflect the completed work.
2. Ensure PEP 257 docstrings are maintained/added for clarity.

## Testing Strategy

### Automated/Manual Validation Scenarios
1.  **Fresh Workspace:** Remove `.gemini/last_journal_update`. Modify a file. Verify it requires a journal entry.
2.  **Journal Updated:** Update the journal. Verify the hook now returns `allow` and creates/updates the state file.
3.  **No New Changes:** Run the hook again immediately. Verify it returns `allow`.
4.  **New Modification:** Update another source file. Verify it requires a journal entry again (since its `mtime > last_journal_update`).
5.  **Deleted File:** Delete a file. Verify it requires a journal entry (detected via parent directory `mtime`).
