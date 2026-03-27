---
title: 'The Mode-Command-Tool Pattern: Framework Design Specification'
slug: mode-command-tool-pattern
date: '2026-03-27'
tags:
- framework
- design-pattern
- architecture
- agent-design
---

# The Mode-Command-Tool Pattern

## Overview

This document defines the canonical three-layer architecture for the opencode framework, establishing clear separation of concerns between **Modes** (behavioral philosophy), **Commands** (workflow entry points), and **Tools** (execution engines with state management).

---

## The Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: MODE (.opencode/agents/{mode}.md)                 │
│  └── Defines: Thinking style, behavioral principles         │
│      Permissions: Explicit allow/deny boundaries            │
│      Tone: Open-ended, exploratory, suggestive              │
│                                                             │
│       ↓ suggests at appropriate moments                     │
│                                                             │
│  LAYER 2: COMMAND (.opencode/commands/{cmd}.md)             │
│  └── Defines: Workflow entry point                          │
│      Structure: Minimal, delegates to tool                  │
│      Key Phrase: "Read the output and follow instructions"  │
│                                                             │
│       ↓ delegates execution                                 │
│                                                             │
│  LAYER 3: TOOL (.opencode/bin/{tool}.py)                    │
│  └── Defines: Validation, state management, continuation    │
│      Returns: Descriptive instructions for next steps       │
│      Guards: Safety checks, branching logic                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Mode Specification

### Correct Structure

**YAML Frontmatter:**
```yaml
---
description: Brief purpose statement
mode: primary|subagent
permissions:
    "*": deny
    read: allow
    [tool]: [scope]: allow|deny
---
```

**Content Sections:**
1. **Identity Statement** — "You are in X Mode — purpose"
2. **Thinking Style** — 3-5 bullet points (principles, not procedures)
3. **Subagents** — Clear role definitions
4. **Behavior** — Split: "If running command / If freestyle"
5. **Key Mandates** — Non-negotiable rules
6. **When to Suggest Commands** — Bridge to command layer

### Golden Rules for Modes

**DO:**
- Define thinking style (exploratory, analytical, disciplined)
- Use suggestive language: "Suggest `/command` when..."
- Set explicit permission boundaries
- Separate command-running vs freestyle behavior

**DON'T:**
- Define procedural workflows (Step 1, Step 2)
- Mandate commands ("Run `/command` now")
- Leave permissions implicit

---

## Layer 2: Command Specification

### Correct Structure

**YAML Frontmatter:**
```yaml
---
description: Brief purpose statement
agent: [mode-name]  # Which mode executes this
subagents: [list]    # Allowed subagents (optional)
---
```

**Content Pattern:**
```markdown
# /command-name

One-line description of what this command does.

## What to do next

Run: `uv run .opencode/bin/tool.py --arg1 [VAL]`

[Any stdin requirements]

**Read the output and follow instructions from there.**
```

### Critical: The Reactive Pattern

Commands use **reactive workflow delegation**:
- **NOT:** Enumerate all branches and steps
- **INSTEAD:** Delegate to tool, read output, follow instructions

**Key Phrase (Required):**
> "**Read the output and follow instructions from there.**"

This phrase signals to the agent that:
1. The tool will return descriptive messages
2. The agent should parse and act on those messages
3. The tool owns the workflow continuation logic

### Golden Rules for Commands

**DO:**
- Keep under 25 lines
- Provide only entry point and parameters
- Delegate all branching to tool
- Include the "follow instructions" phrase

**DON'T:**
- Define multi-phase workflows inline
- Enumerate if/then branches
- Try to predict all tool outputs

---

## Layer 3: Tool Specification

### Correct Characteristics

**Validation:**
- Check required inputs (stdin, args, files)
- Validate before acting (existence checks, format checks)
- Provide clear error messages

**State Management:**
- Track workflow state internally
- Return descriptive status messages
- Handle branching logic (draft→confirm→save)

**Output Format:**
- Human-readable instructions, not codes
- Tell the agent explicitly what to do next:
  - `"Draft mode. Ask user for changes, rerun with --save"`
  - `"✓ Saved to: {path}"`
  - `"Error: File exists. Choose different slug"`

**Safety Guards:**
- Prevent destructive actions without confirmation
- Two-phase patterns (draft → save)
- Exit codes for success/failure

### Example: note.py Pattern

```python
# 1. Validate required inputs
content = sys.stdin.read().strip()
if not content:
    print("Error: No content via stdin")
    exit(1)

# 2. Set defaults (reduce decision fatigue)
if not slug:
    slug = slugify(title)

# 3. Two-phase workflow (safety)
if not save:
    print("Draft mode. Review with user, then rerun with --save")
    exit(0)

# 4. Safety check
if filepath.exists():
    print("Error: File exists")
    exit(1)

# 5. Execute + confirm
filepath.write_text(content)
print(f"✓ Saved to: {filepath}")
```

### Golden Rules for Tools

**DO:**
- Validate all inputs
- Return descriptive next-step instructions
- Implement branching logic internally
- Use two-phase patterns for destructive ops

**DON'T:**
- Return silent success
- Return machine codes (JSON) instead of instructions
- Skip validation
- Assume agent will track state

---

## The Pattern Decision Framework

### When to Use Reactive (Tool-Driven) vs Prescriptive (Command-Driven)

**Use Reactive Pattern (like /note):**
- Requires user confirmation before final action
- Multiple exit states (draft, saved, error, conflict)
- Natural "review → confirm → execute" lifecycle
- Tool can validate better than agent (file existence, etc.)

**Use Prescriptive Pattern (like /build phases):**
- Linear workflow with few branches
- All info available upfront
- Steps are deterministic
- Complex logic handled by subagents

### Anti-Patterns to Avoid

**Mode Anti-Patterns:**
- Defining procedures instead of principles
- Missing "When to suggest commands" section
- Implicit permissions
- Mandating instead of suggesting

**Command Anti-Patterns:**
- Overly prescriptive (50+ lines of steps)
- Enumerating all branches inline
- Missing "follow instructions" phrase
- Owning branching logic that belongs in tool

**Tool Anti-Patterns:**
- Silent success (no confirmation)
- Returning data instead of instructions
- No validation
- No safety guards for destructive actions

---

## Summary: The Golden Rules

### 1. Modes Define Philosophy
- Thinking style > workflow steps
- Suggest commands, don't mandate them
- Permission boundaries explicit

### 2. Commands Are Entry Points
- Minimal workflow description
- Delegate to tools for execution
- **Key phrase:** "Read the output and follow instructions from there"

### 3. Tools Own The Workflow
- Validate everything
- Return descriptive instructions for next steps
- Handle branching logic internally
- Guide agent through state transitions

### 4. Progressive Disclosure
```
Mode:     "Be exploratory" (philosophy)
Command:  "Run this tool" (intent)
Tool:     "Draft mode, ask user, then rerun with --save" (execution)
```

---

## Examples in Framework

**Good Example:** analyze.md + note.md + note.py
- Mode: Suggests /note at right moments
- Command: "Run tool, read output, follow instructions"
- Tool: Validates, returns "draft mode" or "saved"

**Anti-Pattern:** build.md command spec
- Enumerates all TCR phases inline
- No tool delegation
- Agent must track state mentally
- Brittle to changes

---

## Application Guidelines

When creating new framework components:

1. **Start with Mode** — Define thinking style and when to suggest commands
2. **Create Command** — Minimal entry point with "follow instructions" phrase
3. **Build Tool** — Validation, state management, descriptive outputs
4. **Test Workflow** — Ensure tool messages guide agent correctly

The goal: **Agent reads tool output and knows exactly what to do next**, without the command spec enumerating all possibilities.