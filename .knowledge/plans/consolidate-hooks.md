# Plan: Consolidate Project Hooks (Pre-commit)

## Objective
Enforce project standards by consolidating validation logic into a Git pre-commit hook. This ensures that every commit is backed by a successful build (make) and an updated journal entry, moving away from agent-side enforcement to repository-level enforcement.

## Requirements
- **Standardized Validation:** Run make and verify journal updates before every commit.
- **Modern Logic:** Use Python 3.12+ for the hook implementation.
- **Inclusive Change Detection:** Track staged and untracked (but not ignored) files.
- **Journal Mtime Rule:** The journal for today must be the most recently modified "meaningful" file.
- **Concise Feedback:** Print only status summaries; avoid flooding the commit output.

## Technical Strategy

### 1. Hook Implementation (.gemini/hooks/pre-commit.py)
A Python script will:
- **Determine Today's Journal:** journal/$(date +%Y-%m-%d).md.
- **Scan for Changes:** Use git ls-files --modified --others --exclude-standard to find all files to check.
- **Validate Mtimes:**
    - Calculate max(mtime) for all changed files (excluding .gemini/ and the journal).
    - If today_journal.mtime < max_mtime, abort the commit with an "Updated journal required" message.
- **Run Make:**
    - If meaningful changes exist, execute make.
    - If make fails, abort with a concise error.

### 2. Installation (makefile)
Add a target to link the hook:
```makefile
install-hooks:
	ln -sf ../../.gemini/hooks/pre-commit.py .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
```

## Tasks
- [ ] Create .gemini/hooks/pre-commit.py.
- [ ] Update makefile with install-hooks target.
- [ ] Run make install-hooks.
- [ ] Verify: Test with outdated journal (should fail).
- [ ] Verify: Test with failing make (should fail).
- [ ] Verify: Test with updated journal and passing make (should succeed).