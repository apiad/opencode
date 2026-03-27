---
id: audit-documentation-2026-03-27
created: 2026-03-27
type: audit
scope: documentation
status: active
---

# Audit: Documentation

## Executive Summary

**Health: ⚠️ Critical Issues**

The documentation has significant drift from the current implementation. Multiple commands referenced don't exist, directory structures are outdated, and install URLs are inconsistent across files. New users following the docs would encounter broken commands and incorrect paths.

## Architecture Overview

### Documentation Files
- `docs/index.md` — Landing page, philosophy, quick start
- `docs/deploy.md` — Installation & setup
- `docs/design.md` — Architecture & systems
- `docs/develop.md` — Contribution guidelines
- `docs/updating.md` — Update procedures
- `docs/user-guide.md` — Usage walkthrough
- `docs/install.sh` — Installer script

### Actual Command Set (`.opencode/commands/`)
```
audit, build, commit, draft, fix, help, investigate, 
note, onboard, plan, publish, research, scaffold, todo
```

---

## Findings

### Strengths
- Clean structure with separate concern files
- Good use of YAML frontmatter standards
- README.md accurately reflects two-repo architecture
- Install script is functional and recent

### Concerns

| Area | Severity | Description | Location | Recommendation |
|------|----------|-------------|----------|----------------|
| Directory Structure | **high** | `design.md` shows old dirs (`plans/`, `journal/`, `research/`, `drafts/`) but actual is `.knowledge/plans/`, `.knowledge/log/`, `.knowledge/notes/`, `.knowledge/drafts/` | `docs/design.md:115-127` | Update to show `.knowledge/*` structure |
| Missing Commands | **high** | `/maintenance`, `/document`, `/brainstorm`, `/cron`, `/learn` are documented but don't exist | Multiple docs | Either implement or remove from docs |
| Install URLs | **high** | Inconsistent URLs: `apiad.github.io/starter` vs `apiad.github.io/opencode` | `docs/index.md:39`, `docs/deploy.md:76-91` | Standardize to `apiad.github.io/opencode` |
| CLI Name | **high** | Docs reference `gemini` CLI but actual CLI is `opencode` | `docs/deploy.md:146,157` | Replace all `gemini` with `opencode` |
| Wrong Install Flag | **medium** | `docs/deploy.md` shows `--mode=link` but install.sh uses `--link` | `docs/deploy.md:76,79` | Update to match actual flag syntax |
| Agent-Command Mismatch | **medium** | `design.md` shows agents not in commands, e.g., `query`, `write`, `review` | `docs/design.md:7-17` | Document actual commands or reconcile |
| Missing `/revise` | **low** | Referenced as "legacy" but implementation unclear | `docs/user-guide.md:227` | Clarify if this command exists |

### Technical Debt

1. **Orphaned Plans** — Multiple `.knowledge/plans/` files for features that may not be implemented:
   - `add-brainstorm-command.md` — `/brainstorm` not implemented
   - `implement-learn-command.md` — `/learn` not implemented
   - `implement-maintenance-v2.md` — `/maintenance` not implemented

2. **Outdated Terminology**
   - "Tier Protocol" in `docs/index.md:49` — no corresponding implementation
   - "Context Minifier" in `docs/develop.md:75` and `docs/user-guide.md:18` — no documented implementation

3. **Install Script Issues**
   - Uses `--link` but docs show `--mode=link` and `--mode=copy`
   - `REPO_URL` points to `opencode-core` but should document which repo

---

## Recommendations

### Priority 1: Fix Critical Path Issues

1. **Update install URL everywhere** to `https://apiad.github.io/opencode/install.sh`
   - `docs/index.md:39`
   - `docs/deploy.md:76,79,91`
   - `docs/updating.md:14,26,40,52,62,122,156`

2. **Replace CLI name** `gemini` → `opencode` in:
   - `docs/deploy.md:146,157`
   - Any other occurrences

3. **Fix `--mode=` → `--link`/`--copy`** in `docs/deploy.md:76-79` and `docs/updating.md`

4. **Update directory structure** in `docs/design.md:115-127`:
   ```diff
   - plans/               # Saved execution plans
   - journal/             # Daily journal entries (YYYY-MM-DD.yaml)
   - research/           # Research artifacts
   - drafts/             # Content drafts
   + .knowledge/
   + ├── plans/          # Saved execution plans
   + ├── notes/          # Research artifacts and notes
   + ├── log/            # Daily journal entries (YYYY-MM-DD.yaml)
   + └── drafts/        # Content drafts
   ```

### Priority 2: Reconcile Command Inventory

5. **Decision needed:** Should these commands be implemented or removed from docs?
   - `/maintenance` — mentioned in multiple docs
   - `/document` — referenced in develop.md, user-guide.md
   - `/brainstorm` — has a plan file
   - `/cron` — mentioned in user-guide.md
   - `/learn` — has a plan file

### Priority 3: Cleanup

6. Remove or archive orphaned plan files for unimplemented commands
7. Remove or clarify "Tier Protocol" and "Context Minifier" mentions if no implementation
8. Add `docs/install.sh` usage examples to match actual `--link` flag

---

## Evidence

### Files Referencing Non-Existent Commands
- `docs/develop.md:19` — `/maintenance`
- `docs/develop.md:84-106` — `/learn`
- `docs/user-guide.md:58-66` — `/learn`
- `docs/user-guide.md:38-44` — `/brainstorm`
- `docs/user-guide.md:224-232` — `/review`
- `docs/user-guide.md:240-252` — `/cron`, `/maintenance`
- `docs/index.md:48` — `/learn`
- `docs/index.md:53` — `/document`

### Install URL Inconsistency
```bash
# docs/index.md:39
curl -fsSL https://apiad.github.io/starter/install.sh | bash

# docs/deploy.md:91  
curl -fsSL https://apiad.github.io/starter/install.sh | bash

# README.md:19
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
```
