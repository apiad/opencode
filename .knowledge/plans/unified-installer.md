# Gemini CLI Installer Consolidation Plan

This plan outlines the steps to merge `install.sh` and `add-gemini.sh` into a single, robust entry point for both initial setup and framework updates within a Gemini-based project.

## Objective
The goal is to create a unified `install.sh` script that can:
1.  **Initialize** the Gemini CLI framework in a new or existing project directory.
2.  **Update** an existing Gemini installation to the latest version.
3.  Operate **in-place** (no new directory creation).
4.  Ensure **safety** through git status checks and automatic commits.
5.  Provide **transparency** through a summary of changes and user confirmation.

## Architectural Impact
- **Streamlined Workflow:** Users only need to know one command for setup and updates.
- **Project Integrity:** The "clean git tree" requirement ensures that framework changes can be easily reverted.
- **Configuration Persistence:** The update logic explicitly preserves user-created files within the `.gemini/` directory.

## File Operations
- **Modify:** `install.sh`
- **Delete:** `add-gemini.sh`
- **Modify:** `TASKS.md` (Update tasks to reflect the change)

## Step-by-Step Execution

### Step 1: Initialize New `install.sh` Structure
- Start with the existing `install.sh` framework (v0.10.1).
- Update the version and include utility functions from both scripts (`banner`, `error`, `confirm`).
- Remove the "Enter project name" and "Target directory" prompts.

### Step 2: Implement Environment Validation
- **Prerequisites Check:** Ensure `git` and `node` are installed.
- **Git Initialization:** If the current directory is not a git repository, run `git init`.
- **Clean Tree Check:** Use `git status --porcelain` to ensure there are no uncommitted changes. Error out if the tree is dirty.

### Step 3: Implement Framework Acquisition
- Use `mktemp -d` to create a temporary directory.
- Clone the latest starter repository into this temporary directory:
  ```bash
  git clone --depth 1 -q "$REPO_URL" "$TEMP_DIR"
  ```
- Ensure the temporary directory is cleaned up on script exit using `trap`.

### Step 4: Implement Change Discovery & User Confirmation
- Define lists for:
    - **Core Framework:** `.gemini/`
    - **Top-level Files:** `GEMINI.md`, `makefile`, `TASKS.md`, `CHANGELOG.md`, `README.md`
    - **Content Directories:** `journal/`, `plans/`, `research/`, `drafts/`
- Scan the current directory to determine:
    - Which files/directories will be **created**.
    - Which files/directories will be **overwritten** (updated).
- Present a clear summary of these changes to the user.
- Wait for explicit confirmation (`y/N`) before proceeding.

### Step 5: Implement Update/Installation Logic
- **Framework Core (`.gemini/`):**
    - Copy the contents of the temp `.gemini` folder to the local one:
      ```bash
      cp -r "$TEMP_DIR/.gemini/." .gemini/
      ```
    - This overwrites framework files but preserves any unique user files.
- **Top-Level Files:**
    - For `GEMINI.md`, `makefile`, `TASKS.md`, `CHANGELOG.md`, and `README.md`:
        - If they exist and the user confirmed the update, overwrite them with the versions from `$TEMP_DIR`.
        - If they don't exist, create them from `$TEMP_DIR`.
- **Content Directories:**
    - For `journal/`, `plans/`, `research/`, and `drafts/`:
        - Ensure they exist using `mkdir -p`.
        - Copy `.gitkeep` from the temp clone to ensure they are tracked by git.
        - **Do not** delete or modify any existing user content in these directories.
- **Journal Logging:**
    - Create (or append to) a journal entry for the current date.
    - Log whether this was an "Initial Integration" or a "Framework Update".

### Step 6: Implement Finalization & Git Commit
- Determine the commit message:
    - If `.gemini/` did not exist previously: `feat: integrate Gemini CLI framework`
    - If `.gemini/` already existed: `chore: update Gemini CLI framework`
- Execute `git add .` and `git commit -m "$MESSAGE"`.
- Provide a success message and guidance on running `gemini /onboard`.

### Step 7: Cleanup
- Delete `add-gemini.sh` from the repository.

## Testing Strategy
1.  **Fresh Install:**
    - Run `install.sh` in an empty directory.
    - Verify git is initialized, files are created, and a "feat" commit is made.
2.  **Existing Project Integration:**
    - Run `install.sh` in a non-Gemini git project.
    - Verify files are added and a "feat" commit is made.
3.  **Framework Update:**
    - Run `install.sh` in an existing Gemini project.
    - Verify `.gemini` files are updated, custom files in `.gemini` remain, and a "chore" commit is made.
4.  **Confirmation Test:**
    - Run `install.sh` and select `N` at the confirmation prompt. Verify no changes were made.
5.  **Safety Test:**
    - Run `install.sh` with uncommitted changes in the repository. Verify it exits with an error.
6.  **Cleanup Test:**
    - Verify `add-gemini.sh` is no longer present in the root directory.
