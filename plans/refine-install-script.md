# Plan: Refine `install.sh` File Handling

## Objective
Update `docs/install.sh` to distinguish between core framework files (which should be extracted/updated) and project scaffolding files (which should only be created if they don't exist).

## Requirements
- **Core Framework (Always Extract):** `.gemini/`, `GEMINI.md`.
- **Project Scaffolding (Create If Missing):** `README.md`, `TASKS.md`, `CHANGELOG.md`, `makefile`.
- **Content Directories:** `journal/`, `plans/`, `research/`, `drafts/` (Ensure existence).

## Proposed Changes

### 1. Update `docs/install.sh`
- **Re-categorize variables:**
  - `CORE_FILES=("GEMINI.md")`
  - `SCAFFOLD_FILES=("README.md" "TASKS.md" "CHANGELOG.md" "makefile")`
  - `CONTENT_DIRS=("journal" "plans" "research" "drafts")`
- **Refine Summary Logic:**
  - Loop through `CORE_FILES` and `.gemini/` to mark as "Update" if they exist, or "Create" if they don't.
  - Loop through `SCAFFOLD_FILES` and mark as "Create" ONLY if they don't exist. If they exist, they should be ignored by the update process.
- **Refine Execution Logic:**
  - **Core:** `cp -r "$TEMP_DIR/.gemini/." .gemini/` and `cp "$TEMP_DIR/GEMINI.md" .` (Always overwrite).
  - **Scaffold:** Use `cp -n` (no-clobber) or `if [[ ! -f "$f" ]]; then cp ...; fi` for each file in `SCAFFOLD_FILES`.
  - **Directories:** Keep existing logic to ensure directories exist.

## Verification Strategy
- **Code Review:** Ensure the shell logic correctly uses `[[ ! -f "$f" ]]` or `cp -n` to prevent overwriting existing user project files.
- **Manual Test:** Run the script in a test environment to verify:
  - `GEMINI.md` is updated.
  - Existing `README.md` is preserved.
  - Missing `makefile` is created.
