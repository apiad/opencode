---
id: framework-analysis-2026-03-27
created: 2026-03-27
modified: 2026-03-27
type: audit
status: active
sources:
  - AGENTS.md
  - .opencode/agents/*.md
  - .opencode/commands/*.md
  - .opencode/tools/*.ts
  - todo.yaml
  - README.md
tags:
  - framework
  - architecture
  - improvements
---

# OpenCode Framework Analysis & Improvement Suggestions

## Executive Summary

After analyzing the repository structure, agent configurations, tools, and current implementation, I've identified several areas for improvement ranging from architectural inconsistencies to tool reliability issues.

---

## Current Architecture Overview

### Directory Structure
```
/
├── AGENTS.md              # Core constitution (universal mandates)
├── README.md              # User-facing documentation
├── todo.yaml              # Task storage
├── .opencode/
│   ├── agents/            # Mode definitions (analyze, plan, build, release, etc.)
│   ├── commands/          # Command specifications
│   ├── tools/             # TypeScript tool implementations (journal.ts, todo.ts)
│   ├── style-guide.md
│   └── node_modules/
├── .knowledge/
│   ├── notes/             # Analysis outputs
│   └── plans/             # Action plans
├── plans/                 # Duplicated plans directory (confusion point)
├── journal/               # Daily journal entries
├── research/              # Research outputs
├── drafts/                # Draft content
└── docs/                  # Project documentation
```

### Core Components
1. **4 Primary Modes**: analyze, plan, build, release
2. **5 Subagents**: scout, investigator, critic, tester, drafter
3. **14+ Commands**: research, audit, plan, build, commit, etc.
4. **2 Tools**: todo.ts, journal.ts (TypeScript/Bun-based)

---

## Issues & Improvement Suggestions

### 1. **Critical: Permission System Not Enforced**

**Problem**: Agents have YAML frontmatter defining permissions, but there's no enforcement mechanism.

**Evidence**:
- `analyze.md` defines: `edit: .knowledge/notes*: allow`
- `plan.md` has a typo: `.knowledege/plans` (line 8)
- No validation that agents actually respect these constraints

**Impact**: The entire security model is declarative but not enforced, relying on agent "good behavior" which could fail.

**Suggestion**: 
- Implement a permission validation layer in the tool system
- Add tests that verify agents can't exceed their permissions
- Fix the typo in plan.md (`.knowledege` → `.knowledge`)

---

### 2. **Major: Tool Implementation is Brittle**

**Problem**: Custom YAML parsing in todo.ts and journal.ts using regex-based parsing.

**Evidence** (from todo.ts lines 34-91):
```typescript
function parseYaml(content: string): TasksData {
  const lines = content.split("\n");
  // ... 60 lines of regex-based YAML parsing
}
```

**Issues**:
- Doesn't handle multi-line strings
- No YAML spec compliance
- Fragile to formatting changes
- No schema validation
- Will break on edge cases (special characters in descriptions, etc.)

**Suggestion**:
- Use a proper YAML library (like js-yaml)
- Add JSON Schema validation
- Consider JSON for machine-readable files instead of YAML
- Add comprehensive tests for edge cases

---

### 3. **Major: Command/Tool Mismatch**

**Problem**: Two different task management systems with different purposes but similar names.

**Evidence**:
- `todo` tool: Manages `todo.yaml` - persistent project tasks
- `/todo` command: Lists GitHub issues (from `.opencode/commands/todo.md`)
- `todowrite` tool: Session-level task tracking

**User Confusion**:
- "Should I use the todo tool or the todo command?"
- "What's the difference between todo.yaml and session todos?"

**Suggestion**:
- Rename for clarity:
  - `todo` tool → `task` or `backlog` (project tasks)
  - `/todo` command → `/issues` or `/github-tasks`
  - `todowrite` → keep as is (session tasks are different)
- Add clear documentation explaining when to use each

---

### 4. **Medium: Directory Structure Inconsistency**

**Problem**: Plans exist in two places with no clear ownership.

**Evidence**:
- `AGENTS.md` line 26: `.knowledge/plans/` - created by plan agent
- Root `/plans/` directory exists with 15+ plan files
- No clear migration or organization strategy

**Suggestion**:
- Consolidate to single location
- Update AGENTS.md to reflect actual practice
- Add a symlink or README explaining the structure
- Consider: Are root `/plans/` user-facing? Are `.knowledge/plans/` agent-facing?

---

### 5. **Medium: Agent/Command Documentation Drift**

**Problem**: README.md describes many commands that don't exist in `.opencode/commands/`.

**Evidence** (commands in README but missing from .opencode/commands/):
- `/brainstorm` - mentioned in README line 61
- `/issues` - mentioned in README line 70
- `/debug` - mentioned in README line 71
- `/task` - mentioned in README line 72 (but there's a todo tool)
- `/document` - mentioned in README line 79
- `/cron` - mentioned in README line 80
- `/release` - mentioned in README line 84 (but has `/publish`)
- `/learn` - mentioned in README line 60

**Suggestion**:
- Audit all commands mentioned in README
- Either implement missing commands or remove from README
- Add CI check to prevent drift (e.g., verify all `/command` references have corresponding .md files)

---

### 6. **Medium: Subagent Rules Not Enforced**

**Problem**: Subagent rules in AGENTS.md lines 81-88 are guidelines, not enforced constraints.

**Evidence**:
- Rules listed: "Never write to project files", "Never write to .knowledge/"
- No technical enforcement mechanism
- Subagents use `task` tool which has no permission system

**Suggestion**:
- Add sandboxing or chroot for subagent file access
- Implement file system permissions in the tool layer
- Log and audit subagent file operations

---

### 7. **Low: Missing Error Handling**

**Problem**: Tools assume success and don't handle common error cases.

**Evidence** (from todo.ts):
- Line 23-24: `if (!await file.exists())` - good
- Line 31: `return parseYaml(content)` - no try/catch for malformed YAML
- No validation that task IDs are unique before adding
- No handling for circular dependencies

**Suggestion**:
- Add comprehensive error handling
- Validate task ID uniqueness
- Detect and prevent circular dependencies
- Add user-friendly error messages

---

### 8. **Low: No Migration Strategy**

**Problem**: Framework version 2.0 declared in AGENTS.md but no migration path from v1.

**Evidence**:
- Line 168: `*Framework Version: 2.0*`
- No CHANGELOG.md section for breaking changes
- No migration guide

**Suggestion**:
- Document breaking changes from v1 to v2
- Add migration scripts if needed
- Version the configuration files (e.g., `.opencode/config-v2.yaml`)

---

### 9. **Low: Style Guide Isolated**

**Problem**: `.opencode/style-guide.md` exists but isn't referenced in agent configs.

**Evidence**:
- No agent includes "read style-guide" in their setup
- Not mentioned in any command workflows
- drafter.md (content creation) doesn't reference it

**Suggestion**:
- Add style-guide to agent context where relevant
- Reference in `/draft` and `/review` commands
- Consider making it part of the system prompt for content agents

---

### 10. **Architectural: No Plugin System**

**Problem**: Tools are hardcoded TypeScript files; no extensibility.

**Evidence**:
- All tools in `.opencode/tools/*.ts`
- No dynamic loading mechanism
- Users can't add custom tools without modifying core

**Suggestion**:
- Design a plugin interface (JSON-based tool definitions?)
- Allow custom tools in `.opencode/custom-tools/`
- Document the tool API for extension

---

## Priority Matrix

| Issue | Priority | Effort | Impact |
|-------|----------|--------|--------|
| Permission system not enforced | Critical | High | Security |
| Brittle YAML parsing | Major | Medium | Reliability |
| Command/tool name confusion | Major | Low | Usability |
| Documentation drift | Medium | Low | Maintenance |
| Directory inconsistency | Medium | Low | Organization |
| Subagent rules not enforced | Medium | High | Security |
| Missing error handling | Low | Low | Reliability |
| No migration strategy | Low | Low | Maintenance |
| Style guide isolated | Low | Low | Quality |
| No plugin system | Low | High | Extensibility |

---

## Recommended Immediate Actions

1. **Fix the typo** in `.opencode/agents/plan.md` line 8: `.knowledege` → `.knowledge`

2. **Clarify naming**: Decide on final names for task management concepts and update all references

3. **Audit commands**: Create missing command files or remove from README

4. **Add YAML validation**: At minimum, add try/catch around parsing

5. **Document the dual plans directories**: Add README explaining `.knowledge/plans/` vs `/plans/`

---

## Questions for Framework Maintainers

1. Is the permission system in agent frontmatter aspirational or intended to be enforced?
2. What's the difference between root `/plans/` and `.knowledge/plans/`?
3. Are the README commands (brainstorm, issues, debug, etc.) planned or deprecated?
4. Should we migrate from YAML to JSON for machine-readable files?
5. Is there a roadmap for plugin/custom tool support?

---

*Analysis conducted on 2026-03-27 based on Framework Version 2.0*
