# Documentation Update Plan: v2.0.0

**Created:** 2026-04-01  
**Version:** v2.0.0  
**Status:** Draft

---

## Problem

The OpenCode Framework v2.0.0 introduced major new features (literate commands, sandbox plugin, design mode) but the documentation has not been updated to reflect these changes. Users cannot discover or understand how to use the new capabilities.

---

## Scope

### Documents Affected
1. `docs/design.md` - Architecture & Systems
2. `docs/user-guide.md` - User Guide
3. `docs/index.md` - Landing page

### New Features to Document
| Feature | Description | Complexity |
|---------|-------------|------------|
| Literate Commands | Multi-step guided workflows with variables & conditionals | High |
| Sandbox Plugin | Docker-based isolated execution | Medium |
| Design Mode | New agent mode for planning/design work | Low |
| `/commit` Command | Validation-aware commit workflow | Low |
| `/sandbox` Command | Sandbox management command | Medium |

---

## Solution Approach

**Strategy:** Incremental, file-by-file updates with review checkpoints. Each document updated in isolation to minimize merge conflicts and allow focused review.

---

## Phases

### Phase 1: Fix Critical Issues
**Estimated time:** 30 minutes

1. **Fix truncated `/commit` section** in `user-guide.md`
   - Complete the truncated content at line 84
   - Document full validation workflow

2. **Add missing commands to design.md**
   - Add `/commit` to commands table
   - Add `/sandbox` to commands table

**Deliverables:**
- [ ] `user-guide.md` `/commit` section complete
- [ ] `design.md` commands table updated

---

### Phase 2: Update Agent Architecture
**Estimated time:** 1 hour

1. **Add `design` mode** to Primary Agents tables
   - `docs/design.md`: Add column/row for `design` mode
   - `docs/user-guide.md`: Add to Agent Architecture section

2. **Add `lit-commands` subagent** to subagents table
   - Document purpose: Processes literate command files

3. **Update Key Capabilities** in `docs/index.md`
   - Add literate commands
   - Add sandbox capability

**Deliverables:**
- [ ] `design.md` Primary Agents table includes `design` mode
- [ ] `design.md` Subagents table includes `lit-commands`
- [ ] `user-guide.md` Agent Architecture updated
- [ ] `index.md` Key Capabilities updated

---

### Phase 3: Document Literate Commands
**Estimated time:** 2-3 hours

1. **Create new section** in `design.md`
   ```
   ## 📜 Literate Commands
   ```
   - Explain concept: `.md` files with executable code blocks
   - Document frontmatter options:
     - `literate: true`
     - `variables: []`
     - `conditions: {}`
   - Explain phase execution model:
     1. Parse → 2. Substitute → 3. Route → 4. Execute

2. **Add `/scaffold` documentation** for literate commands
   - Show how to scaffold a literate command
   - Document file structure

3. **Add walkthrough** in `user-guide.md`
   - Step-by-step example of creating a literate command
   - Show variable collection and conditional branching

4. **Update commands table** in `design.md`
   - Add literate-commands command
   - Reference new section

**Deliverables:**
- [ ] `design.md` Literate Commands section created
- [ ] `user-guide.md` Literate Commands walkthrough added
- [ ] Commands table includes literate-commands entry

---

### Phase 4: Document Sandbox Plugin
**Estimated time:** 1-2 hours

1. **Create new section** in `design.md`
   ```
   ## 🐳 Sandbox Plugin
   ```
   - Explain purpose: Docker-based isolation
   - Document mode-specific routing
   - List sandbox directories:
     - `.opencode/sandbox/sandbox.sh`
     - `.opencode/plugins/sandbox.js`

2. **Add prerequisites** section in `deploy.md`
   - Add Docker to requirements list
   - Document sandbox setup command: `/sandbox`

3. **Update Key Capabilities** in `index.md`
   - Add "Isolated Execution" capability

4. **Add sandbox management** to `user-guide.md`
   - Document `/sandbox` command usage
   - Explain when sandbox is used automatically

**Deliverables:**
- [ ] `design.md` Sandbox Plugin section created
- [ ] `deploy.md` Docker prerequisite added
- [ ] `index.md` Isolated Execution capability added
- [ ] `user-guide.md` sandbox documentation added

---

### Phase 5: Review & Polish
**Estimated time:** 1 hour

1. **Cross-reference checks**
   - Ensure all commands mentioned in one doc exist in design.md table
   - Verify all modes in index.md appear in design.md

2. **Update navigation**
   - Ensure "Next:" links at bottom of each doc point to correct files
   - Verify TOC if using mkdocs-autodocs

3. **Link verification**
   - Check internal links between documents
   - Verify code snippets are accurate

4. **Add to CHANGELOG.md**
   - Document documentation updates as a minor item

**Deliverables:**
- [ ] All cross-references verified
- [ ] Navigation links verified
- [ ] CHANGELOG.md updated

---

## Implementation Order

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
   ↓          ↓         ↓          ↓          ↓
  Quick      Agent     Literate   Sandbox    Polish
  Fixes     Updates   Commands   Plugin
```

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Sandbox details change during implementation | Medium | Low | Write generically; reference source code for specifics |
| Literate commands API evolves | Medium | Medium | Focus on concept over implementation details |
| Docker prerequisite may limit adoption | Low | Medium | Clearly document when sandbox is optional |
| Merge conflicts if concurrent edits | Low | High | Work file-by-file, commit after each phase |

---

## Success Criteria

1. **Completeness:** All new features (literate commands, sandbox, design mode) have dedicated documentation sections
2. **Discoverability:** Index page lists all key capabilities
3. **Accuracy:** Code snippets and command examples work
4. **Navigation:** Users can follow "Next:" links through the documentation
5. **Consistency:** Terminology matches across all documents

---

## Verification Commands

After implementation, verify:
```bash
# Check all referenced commands exist
grep -h "/commit\|/sandbox\|/release\|/fix" docs/*.md | sort -u

# Check all modes documented
grep -h "analyze\|plan\|build\|release\|design" docs/*.md | sort -u

# Check new features mentioned
grep -l "literate\|sandbox\|sandbox.sh" docs/*.md
```

---

## Estimated Total Time

| Phase | Time | Cumulative |
|-------|------|------------|
| Phase 1 | 30 min | 30 min |
| Phase 2 | 1 hour | 1.5 hours |
| Phase 3 | 2-3 hours | 3.5-4.5 hours |
| Phase 4 | 1-2 hours | 4.5-6.5 hours |
| Phase 5 | 1 hour | 5.5-7.5 hours |

**Total: ~6-8 hours**

---

## Next Steps

1. **Approve this plan** → Switch to Create mode to implement
2. **Prioritize phases** → Decide if Phases 3-4 can be deferred
3. **Assign ownership** → Determine who reviews each phase

---

*Plan created by design agent. Ready for implementation.*
