---
id: refactor-framework-submodule-architecture
created: 2026-03-27
modified: 2026-03-27
type: plan
status: done
expires: 2026-04-03
phases:
  - name: Create opencode-core Repository
    done: true
    goal: Extract framework components into standalone repository
  - name: Rename Current Repository
    done: true
    goal: Rename starter to opencode for clarity
  - name: Implement Dual-Mode Installer
    done: false
    goal: Create install.sh with copy and link (submodule) modes
  - name: Refactor Wrapper Repository
    done: false
    goal: Remove framework files and add templates
  - name: Documentation and Testing
    done: true
    goal: Update docs and validate both installation modes
---

# Plan: Refactor Framework into Submodule Architecture

## Context

The OpenCode Framework currently exists as a single repository (`apiad/starter`) containing both the framework runtime (agents, commands, tools) and project templates. This creates issues:
- Framework updates require re-running the full installer
- No version pinning capability
- Difficult to track framework changes separately from project changes
- Projects can't easily share framework updates

This plan splits the framework into two repositories and implements dual installation modes (copy vs submodule link).

## Repository Naming Strategy

- **New repository**: `opencode-core` - Contains framework runtime (extracted from `.opencode/`)
- **Rename current**: `starter` → `opencode` - Contains documentation, templates, and installer

## Phases

### Phase 1: Create opencode-core Repository
**Goal:** Extract all framework components into a standalone, versioned repository

**Deliverable:** New GitHub repository `apiad/opencode-core` with framework files

**Done when:**
- [ ] Repository initialized with proper structure
- [ ] All framework files copied from `.opencode/`
- [ ] `AGENTS.md` relocated to `.opencode/instructions.md`
- [ ] `node_modules/` excluded from git (added to .gitignore)
- [ ] Repository tagged with `v2.0.0`
- [ ] README.md created with framework-specific documentation
- [ ] Repository pushed to GitHub

**Details:**
```
opencode-core/
├── agents/
│   ├── analyze.md, plan.md, build.md, release.md
│   ├── scout.md, investigator.md, critic.md, tester.md, drafter.md
├── commands/
│   ├── audit.md, build.md, commit.md, draft.md, fix.md, help.md
│   ├── investigate.md, onboard.md, plan.md, publish.md
│   ├── research.md, scaffold.md, todo.md
├── tools/
│   ├── journal.ts, todo.ts
├── instructions.md          # Formerly AGENTS.md
├── style-guide.md
├── package.json
├── bun.lock
├── .gitignore               # Excludes node_modules/
├── README.md
├── CHANGELOG.md
└── LICENSE
```

**Depends on:** None (first phase)

---

### Phase 2: Rename Current Repository
**Goal:** Rename `starter` to `opencode` for clarity and consistency

**Deliverable:** Repository accessible at `github.com/apiad/opencode`

**Done when:**
- [ ] Repository renamed on GitHub from `starter` to `opencode`
- [ ] Local remote URL updated to new location
- [ ] Verified GitHub redirects work from old URL
- [ ] Repository description updated

**Details:**
- GitHub will automatically redirect `apiad/starter` to `apiad/opencode`
- Update local clone: `git remote set-url origin https://github.com/apiad/opencode.git`
- No code changes required in this phase

**Depends on:** None (can run in parallel with Phase 1)

---

### Phase 3: Implement Dual-Mode Installer
**Goal:** Rewrite `install.sh` to support both copy and link (submodule) installation modes

**Deliverable:** Updated `install.sh` with `--mode=copy` and `--mode=link` flags

**Done when:**
- [ ] Script supports `--mode=copy` (default) for self-contained installation
- [ ] Script supports `--mode=link` for git submodule installation
- [ ] Interactive mode selection when no flag provided
- [ ] Creates `opencode.json` with installation metadata
- [ ] Copy mode: Downloads and extracts framework, removes .git directory
- [ ] Link mode: Uses `git submodule add` and checks out version tag
- [ ] Preserves user configurations (`opencode.json`, `style-guide.md`)
- [ ] Installs framework dependencies (`bun install` in `.opencode/`)
- [ ] Handles updates for both modes
- [ ] Provides clear summary of installation mode and next steps

**Implementation approach:**
```bash
# Usage examples:
curl -fsSL https://apiad.github.io/opencode/install.sh | bash              # Interactive
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --mode=copy   # Copy mode
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --mode=link   # Submodule mode
```

**Key functions needed:**
- `install_copy_mode()`: Clone framework, remove .git/, copy to .opencode/
- `install_link_mode()`: Run `git submodule add`, checkout tag, init submodule
- `create_opencode_json()`: Generate configuration with mode metadata
- `install_framework_deps()`: Run package manager in .opencode/
- `handle_update()`: Detect existing installation and update appropriately

**Depends on:** Phase 1 (needs opencode-core repo URL), Phase 2 (needs new repo name)

---

### Phase 4: Refactor Wrapper Repository
**Goal:** Remove framework files from `opencode` repo and add project templates

**Deliverable:** Clean `opencode` repository with only wrapper/template content

**Done when:**
- [ ] `.opencode/` directory removed from repository
- [ ] `AGENTS.md` removed (now lives in opencode-core)
- [ ] `templates/` directory created with boilerplate files:
  - `README.md` - Project README template
  - `makefile` - Build commands template
  - `tasks.yaml` - Empty tasks file
  - `CHANGELOG.md` - Changelog template
  - `.gitignore` - Standard gitignore
- [ ] `.knowledge/` structure created with .gitkeep files
- [ ] Root `.gitignore` updated to exclude `.opencode/` (allowing user to choose installation mode)
- [ ] All changes committed

**Details:**
The wrapper repository becomes a template/scaffolding repository:
```
opencode/ (formerly starter)
├── templates/           # Files copied to new projects
│   ├── README.md
│   ├── makefile
│   ├── tasks.yaml
│   ├── CHANGELOG.md
│   └── .gitignore
├── docs/               # Documentation (unchanged)
│   ├── index.md
│   ├── user-guide.md
│   ├── deploy.md
│   ├── design.md
│   └── develop.md
├── install.sh          # Updated dual-mode installer
├── README.md           # Project overview
├── makefile            # Framework development makefile
├── mkdocs.yml
├── CHANGELOG.md
└── LICENSE
```

**Depends on:** Phase 1, Phase 2

---

### Phase 5: Documentation and Testing
**Goal:** Update all documentation and validate both installation modes work correctly

**Deliverable:** Updated documentation and tested installation workflows

**Done when:**
- [ ] `README.md` updated with new repository names and installation instructions
- [ ] `docs/deploy.md` updated with copy vs link mode explanations
- [ ] New `docs/updating.md` created with framework update instructions for both modes
- [ ] Test 1: Fresh copy mode installation works end-to-end
- [ ] Test 2: Fresh link mode installation works end-to-end
- [ ] Test 3: Existing project can update to new installer
- [ ] Test 4: Submodule mode works for team collaboration
- [ ] Test 5: Mode switching (copy ↔ link) works correctly
- [ ] All documentation links verified
- [ ] Release notes written explaining the changes

**Test scenarios:**

**Test 1: Copy Mode Fresh Install**
```bash
mkdir test-copy && cd test-copy
git init
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -- --mode=copy
# Verify: .opencode/ exists, .opencode/.git does NOT exist, opencode.json has mode="copy"
```

**Test 2: Link Mode Fresh Install**
```bash
mkdir test-link && cd test-link
git init
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -- --mode=link
# Verify: .opencode/ is submodule, .gitmodules exists, opencode.json has mode="link"
```

**Test 3: Existing Project Update**
```bash
cd existing-starter-project
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
# Verify: Framework updates, user configs preserved, commit created
```

**Test 4: Team Workflow**
```bash
# Developer A
git clone --recursive https://github.com/user/project
cd project && ls .opencode/agents/  # Should work

# Developer B
git clone https://github.com/user/project
cd project && git submodule update --init --recursive
```

**Depends on:** Phase 1, Phase 2, Phase 3, Phase 4

---

## Success Criteria

- [ ] `opencode-core` repository exists and is publicly accessible
- [ ] `opencode` repository (renamed from starter) works correctly
- [ ] Both installation modes work without errors
- [ ] User configurations are preserved during updates
- [ ] Existing projects can migrate without data loss
- [ ] GitHub redirects from old `starter` URL work
- [ ] Documentation accurately describes both installation modes
- [ ] All tests pass

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Repository rename breaks existing links | Low | GitHub handles redirects automatically; monitor for issues |
| Users confused by new installation modes | Medium | Clear documentation, interactive installer prompts, default to copy mode |
| Submodule complexity scares beginners | Medium | Make copy mode the default; clearly explain trade-offs |
| Existing projects break after update | Medium | Thorough testing, preserve user configs, provide migration guide |
| Framework and wrapper versions drift | Low | Tag both repos consistently, document version compatibility |
| Git submodule not initialized by users | Medium | Document `--recursive` clone, provide `git submodule update` instructions |
| Install script fails on different shells | Low | Test with bash, zsh, sh; use POSIX-compatible syntax |

---

## Related

- **Framework Repository:** `https://github.com/apiad/opencode-core.git` ✓
- **Wrapper Repository:** `https://github.com/apiad/opencode.git` ✓ (renamed from starter)

---

## Timeline Estimate

| Phase | Estimated Time |
|-------|----------------|
| Phase 1: Create opencode-core | 30 minutes |
| Phase 2: Rename repository | 10 minutes |
| Phase 3: Rewrite install.sh | 60 minutes |
| Phase 4: Refactor wrapper | 30 minutes |
| Phase 5: Documentation & Testing | 60 minutes |
| **Total** | **~3.5 hours** |

---

## Implementation Notes

### Critical Files to Migrate

**From `.opencode/` to `opencode-core`:**
- All `agents/*.md` files (9 files)
- All `commands/*.md` files (13 files)
- All `tools/*.ts` files (2 files)
- `style-guide.md`
- `package.json` + `bun.lock`
- `AGENTS.md` → `instructions.md` (rename and relocate)

**Protected User Configurations (never overwrite):**
- `opencode.json` (user's agent configuration)
- `style-guide.md` (if user customized it)

### Version Strategy

- **opencode-core**: Follow semantic versioning (v2.0.0, v2.1.0, etc.)
- **opencode** (wrapper): Can version independently or track core versions
- **install.sh**: Include version check against latest core release

### Backward Compatibility

- Old install.sh URL should redirect or show deprecation warning
- Existing projects with `.opencode/` directory continue to work
- Migration path documented for users wanting to switch modes

---

*Plan created: 2026-03-27*
*Expires: 2026-04-03 (7 days)*
