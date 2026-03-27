---
id: framework-submodule-architecture
created: 2026-03-27
modified: 2026-03-27
type: plan
status: active
tags: [architecture, git-submodule, install]
---

# Framework Submodule Architecture Plan

## Overview

Restructure the OpenCode Framework into two repositories:
1. **Framework Core** (`opencode-framework-core`): Contains only `.opencode/` contents (agents, commands, tools)
2. **Framework Wrapper** (`starter`): Contains documentation, install.sh, examples, and project templates

## Motivation

1. **Central Updates**: Framework can be updated centrally via git submodule
2. **Version Pinning**: Projects can pin to specific framework versions
3. **Clean Separation**: Framework logic separate from project-specific documentation
4. **Flexible Installation**: Users choose between submodule (tracked) or copy (standalone) mode

---

## New Repository Structure

### Repository 1: `opencode-framework-core` (New)

The core framework files that will be installed into projects as `.opencode/`:

```
opencode-framework-core/
├── agents/
│   ├── analyze.md
│   ├── plan.md
│   ├── build.md
│   ├── release.md
│   ├── scout.md
│   ├── investigator.md
│   ├── tester.md
│   ├── drafter.md
│   └── critic.md
├── commands/
│   ├── research.md
│   ├── plan.md
│   ├── build.md
│   ├── audit.md
│   ├── investigate.md
│   ├── onboard.md
│   ├── todo.md
│   ├── commit.md
│   ├── publish.md
│   ├── draft.md
│   ├── fix.md
│   ├── scaffold.md
│   └── help.md
├── tools/
│   ├── journal.ts
│   └── todo.ts
├── package.json          # Framework dependencies
├── bun.lock
├── .gitignore
└── style-guide.md        # Default style guide (user can override)
```

**Key Points:**
- No `node_modules/` in repo (gitignored, installed on first use)
- No `opencode.json` (created by install.sh in target project)
- Versioned independently (semantic versioning)

### Repository 2: `starter` (Current, Refactored)

The wrapper repository containing project scaffolding and documentation:

```
starter/
├── docs/                   # MkDocs documentation
│   ├── index.md
│   ├── user-guide.md
│   ├── design.md
│   ├── deploy.md
│   └── develop.md
├── templates/              # Project templates
│   ├── README.md
│   ├── makefile
│   ├── tasks.yaml
│   └── CHANGELOG.md
├── examples/               # Example projects
├── install.sh              # Unified installer (updated)
├── AGENTS.md               # Core agent constitution
├── opencode.json.example   # Example configuration
├── README.md               # Project README
├── makefile                # Framework development makefile
├── mkdocs.yml              # Documentation config
└── CHANGELOG.md
```

**Key Points:**
- No `.opencode/` directory (fetched at install time)
- Documentation is versioned with wrapper
- Contains project boilerplate templates

---

## Installation Modes

### Mode 1: Git Submodule (Recommended for Teams)

**Use case**: You want to track framework updates and control when to update

```bash
# In your project:
git submodule add https://github.com/apiad/opencode-framework-core.git .opencode
git submodule update --init --recursive
```

**Benefits:**
- Framework updates are explicit (`git submodule update`)
- Can pin to specific commit/version
- Shared across team members
- Clean history of framework changes

**Workflow:**
```bash
# Update framework
cd .opencode && git pull origin main && cd ..
git add .opencode
git commit -m "chore: update opencode framework to v1.2.3"
```

### Mode 2: Copy Mode (Recommended for Solo/Quick Start)

**Use case**: You want a standalone project with no external dependencies

```bash
# Copies framework files into .opencode/
# No git tracking of framework separately
```

**Benefits:**
- Self-contained project
- No submodule complexity
- Works offline
- Simpler for beginners

---

## Updated install.sh Flow

### Phase 1: Environment Setup
1. Check prerequisites (git, node)
2. Initialize git if needed
3. Verify clean working tree

### Phase 2: Mode Selection
```
📦 OpenCode Framework Installer v2.0

How would you like to install the framework?

1) Git Submodule - Track framework updates (recommended for teams)
2) Copy Mode - Standalone installation (recommended for solo projects)

Select mode [1/2]: 
```

### Phase 3: Installation (Submodule Mode)
1. Check if `.opencode` already exists
2. If submodule exists: offer to update
3. If not: `git submodule add <repo> .opencode`
4. Initialize submodule: `git submodule update --init`

### Phase 4: Installation (Copy Mode)
1. Clone framework repo to temp directory
2. Copy contents to `.opencode/`
3. Remove temp directory

### Phase 5: Post-Installation (Both Modes)
1. **Create `opencode.json`** if missing:
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "default_agent": "analyze",
     "agent": {
       "analyze": {},
       "plan": {},
       "build": {},
       "release": {}
     },
     "framework": {
       "version": "2.0.0",
       "mode": "submodule"  // or "copy"
     }
   }
   ```

2. **Create scaffolding files** if missing:
   - `README.md` (boilerplate)
   - `CHANGELOG.md` (boilerplate)
   - `tasks.yaml` (empty)
   - `makefile` (with hooks setup)

3. **Create directories**:
   - `.knowledge/notes/`
   - `.knowledge/plans/`
   - `.knowledge/log/`
   - `.experiments/`
   - `journal/` (optional, based on config)

4. **Install framework dependencies**:
   ```bash
   cd .opencode && bun install && cd ..
   ```

5. **Create initial commit**:
   - Mode: `feat: integrate opencode framework (submodule mode)`
   - Mode: `feat: integrate opencode framework (copy mode)`

### Phase 6: Summary
```
✅ OpenCode Framework installed successfully!

Mode: Submodule (tracking https://github.com/apiad/opencode-framework-core)
Location: .opencode/
Version: v2.0.0

Next steps:
1. Run 'gemini /onboard' to explore your project
2. Customize opencode.json to set your preferred agents
3. Run 'make install-hooks' to enable git hooks

To update framework later:
  cd .opencode && git pull && cd ..
```

---

## opencode.json Enhancements

Add framework metadata section:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "analyze",
  "agent": { ... },
  "framework": {
    "version": "2.0.0",
    "mode": "submodule",
    "repository": "https://github.com/apiad/opencode-framework-core",
    "last_updated": "2026-03-27"
  },
  "project": {
    "name": "My Project",
    "type": "python",
    "hooks_enabled": false
  }
}
```

---

## Migration Strategy

### For Existing Projects

**Option A: Convert to Submodule (Keep History)**
```bash
# Backup current framework
mv .opencode .opencode.backup

# Add as submodule
git submodule add https://github.com/apiad/opencode-framework-core.git .opencode

# Restore custom configs
cp .opencode.backup/opencode.json .opencode/  # if exists
cp .opencode.backup/style-guide.md .opencode/  # if customized

# Clean up
rm -rf .opencode.backup
git add .gitmodules .opencode
git commit -m "chore: convert framework to git submodule"
```

**Option B: Stay with Copy Mode**
- Just run updated install.sh in copy mode
- No changes needed

---

## Implementation Tasks

### Task 1: Create Framework Core Repository
- [ ] Create new repo `opencode-framework-core`
- [ ] Extract `.opencode/` contents (exclude node_modules)
- [ ] Set up CI/CD for framework releases
- [ ] Create framework-specific README
- [ ] Add version tagging

### Task 2: Refactor Wrapper Repository
- [ ] Remove `.opencode/` from this repo
- [ ] Create `templates/` directory with boilerplate files
- [ ] Update main README.md
- [ ] Move documentation to docs/
- [ ] Add `.gitignore` for framework directory

### Task 3: Update install.sh
- [ ] Add interactive mode selection
- [ ] Implement submodule installation logic
- [ ] Implement copy installation logic
- [ ] Create opencode.json generation
- [ ] Add framework metadata tracking
- [ ] Update version checking
- [ ] Add migration helpers

### Task 4: Documentation Updates
- [ ] Update deploy.md with new install options
- [ ] Create submodule workflow guide
- [ ] Document version pinning
- [ ] Add troubleshooting section
- [ ] Update user-guide.md

### Task 5: Testing
- [ ] Test submodule mode on fresh project
- [ ] Test copy mode on fresh project
- [ ] Test migration from existing project
- [ ] Test framework update workflow
- [ ] Test with team (multiple clones)

---

## Benefits Summary

| Aspect | Before | After (Submodule) | After (Copy) |
|--------|--------|-------------------|--------------|
| **Updates** | Re-run install.sh | `git submodule update` | Re-run install.sh |
| **Version Control** | All copied | Separate tracking | All copied |
| **Team Sync** | Manual | Automatic via git | Manual |
| **Disk Usage** | Duplicated | Shared (if multiple projects) | Duplicated |
| **Offline Work** | Yes | Requires initial clone | Yes |
| **Complexity** | Low | Medium | Low |
| **Customization** | Per-project | Per-project + framework updates | Per-project |

---

## Open Questions

1. Should we support multiple framework channels (stable, beta, dev)?
2. How to handle breaking changes in framework updates?
3. Should the wrapper repo have a `package.json` for CLI tooling?
4. Do we need a `opencode doctor` command to diagnose installation issues?
5. Should we support partial framework installation (e.g., only agents, no commands)?

---

## Success Criteria

- [ ] New project can be initialized in under 30 seconds
- [ ] Submodule mode works seamlessly for teams
- [ ] Copy mode works offline
- [ ] Existing projects can migrate without data loss
- [ ] Framework updates don't break custom configurations
- [ ] Documentation is clear for both modes

---

## Next Steps

1. Review this plan
2. Decide on repository names
3. Create framework core repo
4. Implement install.sh changes
5. Test both modes thoroughly
6. Write migration guide
7. Announce to users
