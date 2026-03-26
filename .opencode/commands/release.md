---
description: Automated release process - version bump, changelog update, git tag, GitHub release
agent: ship
---

Automated release workflow for publishing new versions.

### Preconditions
- Worktree must be clean (all changes committed)
- Git hook passes (pre-commit validation)
- If hook fails → redirect to build mode with `/fix`
- If worktree dirty → redirect to `/commit`

### Workflow

1. **Version Analysis**:
   - Find latest git tag
   - Analyze commits since last tag
   - Propose version bump (major/minor/patch) based on commit types
   - Use `question` to confirm version

2. **Version Bump**:
   - Update version file (pyproject.toml, package.json, etc.)
   - Update lock files if needed (uv lock, etc.)

3. **CHANGELOG Update**:
   - Create new entry for version with date
   - Summarize changes since last release
   - Follow existing CHANGELOG format

4. **Finalization**:
   - Commit changes: `chore(release): version X.Y.Z`
   - Create git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
   - Push to remote: `git push origin vX.Y.Z`
   - Create GitHub release via `gh release create` (if gh available)

5. **Journal**:
   - Log release to journal

6. **Report**:
   - Confirm successful release
   - Provide release URL if applicable

### Key Mandates
- **Never touch source code** — Version metadata only
- **Enforce clean worktree** — Release only from clean state
- **Enforce pre-commit hook** — Don't proceed if tests fail
