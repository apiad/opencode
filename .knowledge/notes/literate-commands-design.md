---
id: literate-commands-design
created: 2026-03-30
modified: 2026-03-30
type: design
status: active
tags: [literate-commands, plugin, commands, opencode]
---

# Literate Commands Design

## Overview

A plugin that enables writing OpenCode commands as markdown documents with step-by-step execution. Commands are split into sections by `---`, allowing sequential prompting, structured data extraction, conditional branching, and inline script execution.

## Architecture

```
Command markdown (.opencode/commands/<name>.md)
         │
         ▼
┌─────────────────────────────────────┐
│  LiterateCommandsPlugin             │
│                                     │
│  1. Parse markdown into steps       │
│  2. Inject acknowledgment          │
│  3. On idle: inject step N         │
│  4. Handle user reply/script exec   │
│  5. Parse structured data          │
│  6. Route to next step              │
│  7. Repeat until done              │
└─────────────────────────────────────┘
         │
         ▼
   Step-by-step prompts injected via promptAsync
```

## Command Markdown Format

```markdown
---
description: Build something cool
agent: build
---

First acknowledgment is injected automatically.

---

```yaml {config}
step: define
```
This step defines the topic. Current topic: $TOPIC
```python {exec mode=store}
# script runs with $TOPIC interpolated
return {"topic": "$TOPIC", "items": ["a", "b"]}
```

---

```yaml {config}
step: confirm
wait: true
question:
    title: "Proceed with $TOPIC?"
    options:
        Yes: execute
        No*: refine
```
The topic is **$TOPIC**. Please confirm.

---

```yaml {config}
step: execute
next: done
```
Running deployment for $TOPIC...

---

```yaml {config}
step: refine
next: confirm
```
Please refine the topic. Type your changes.
```

## Step Configuration

Each step starts with a `---` separator and may contain a YAML config block:

```yaml {config}
step: stepName          # Required: unique identifier
wait: false             # Optional: wait for user reply (default: false)
next: step3             # Optional: explicit next step
parse:                  # Optional: extract structured data
    topic: "What is the main topic?"
    scope?: "Describe the scope (bool)"
question:                # Optional: ask user a question
    title: "Confirm?"
    options:
        Yes: nextStep
        No*: editStep
timeout: 30000           # Optional: script timeout in ms
```

### Config Fields

| Field | Type | Description |
|-------|------|-------------|
| `step` | string | Unique step identifier |
| `wait` | boolean | If true, wait for user reply before advancing |
| `next` | string | Jump to specific step (overrides sequential) |
| `parse` | object | Extract variables from model response |
| `question` | object | Present options to user |
| `timeout` | number | Script execution timeout in ms |

## Variable System

### Interpolation Syntax

Variables are referenced with `$NAME` and interpolated using `JSON.stringify`:

| Syntax | Result |
|--------|--------|
| `$topic` | `"Topic Value"` |
| `$topic.items[0]` | `"first item"` |
| `$$` | Full metadata object as JSON |

### Interpolation Rules

1. All values are JSON-stringified (quoted strings, proper arrays/objects)
2. Nested access via dot notation: `$obj.nested.value`
3. `$$` injects the entire metadata object
4. Undefined variables render as `undefined`

### Variable Extraction

The `parse:` block extracts variables from model responses:

```yaml {config}
parse:
    topic: "What is the topic?"
    scope?: "Is the scope wide or narrow?"
    count: "How many items?"
```

- Plain names → string value
- Names ending in `?` → boolean (model must reply true/false)
- JSON.parse is attempted; fallback to raw text if invalid

## Conditional Execution

### Question-Based Routing

```yaml {config}
question:
    title: "Continue?"
    options:
        Yes: nextStep
        No*: editStep
```

- Options with `*` suffix are editable
- Selected option becomes the `next` step

### Pattern-Based Routing

```yaml {config}
next: step3
match:
    scope: ".*wide.*"
    otherwise: step4
```

Pattern matching uses `.*pattern.*` (contains) semantics. First matching pattern wins.

### Boolean Routing

```yaml {config}
match:
    done?: "Is the work complete?"
    yes: finish
    no: continue
```

Variables ending in `?` are parsed as boolean. Model must reply `true` or `false`.

## Script Execution

### Block Syntax

````markdown
```python {exec}
# runs with default interpreter
```
```python {exec=uv run python}
# runs with custom command
```
```bash {exec mode=store}
echo '{"result": "data"}'
```
````

### Execution Modes

| Mode | Behavior |
|------|----------|
| `stdout` (default) | Replace script block with output |
| `store` | Parse JSON output, merge into metadata |
| `none` | Execute silently, no output |

### Variable Substitution

Before execution, scripts undergo variable substitution:

```python
# Original
return {"topic": "$topic", "count": $count}

# After substitution (assuming topic="AI", count=5)
return {"topic": "AI", "count": 5}
```

### Script Execution Order

Scripts in a step execute sequentially before the prompt is injected. Multiple `{exec}` blocks run in document order.

## Execution Flow

### 1. Command Intercepted

```
command.execute.before
  → Load .opencode/commands/<name>.md
  → Parse into steps
  → Set state for session
  → Inject acknowledgment
```

### 2. Acknowledgment Phase

Model receives:
```
We are preparing to run the /command command.
I will give you more instructions.
Please acknowledge and await.
```

### 3. Idle → Inject Step

```
session.idle
  → Get current step
  → Execute all {exec} blocks (with variable substitution)
  → Replace script blocks with output
  → Substitute variables in prompt
  → promptAsync(step.prompt)
  → Advance step index
```

### 4. Response Handling

If `wait: true`:
```
  → Await user reply
  → Route based on question options or match rules
  → Parse variables if parse: defined
  → Jump to next step
```

If `wait: false`:
```
  → Parse response for variables
  → Route based on match rules
  → Jump to next step
```

### 5. Completion

When step index exceeds step count:
```
  → Clean up state
  → Done
```

## State Management

```typescript
interface CommandState {
    steps: Step[]
    currentStep: number
    metadata: Record<string, any>
    sessionID: string
    commandName: string
    arguments: string
}

interface Step {
    config: StepConfig
    prompt: string
    codeBlocks: CodeBlock[]
}
```

State is stored in-memory, keyed by sessionID. No persistence across sessions.

## Hooks Used

| Hook | Purpose |
|------|---------|
| `command.execute.before` | Intercept command, parse markdown, inject acknowledgment |
| `event: session.idle` | Advance to next step, inject prompt |
| `tool.execute.before` | Capture question responses for routing |

## Error Handling

| Error | Behavior |
|-------|----------|
| Script timeout | Log error, continue with empty output |
| Script JSON parse fail (mode=store) | Log error, skip merge |
| Invalid YAML config | Skip config, use defaults |
| Missing variable | Render as `undefined` |
| Step not found (next) | Stop execution, log error |

## File Structure

```
.opencode/
├── plugins/
│   └── literate-commands.js    # Single plugin file
└── commands/
    └── <name>.md               # User-defined commands
```

## Example: Build Command

```markdown
---
description: Build and deploy
agent: build
---

We are preparing to run the /build command. Stand by.

---

```yaml {config}
step: setup
parse:
    project?: "Is this a new project? (true/false)"
```
What are we building?

```python {exec}
import json
print(json.dumps({"ready": True}))
```

---

```yaml {config}
step: confirm
wait: true
match:
    project?: true
    yes: build_new
    no: build_existing
```
Confirm build settings for $project.

---

```yaml {config}
step: build_new
next: deploy
```
Building new project: $project

---

```yaml {config}
step: build_existing
next: deploy
```
Building existing project: $project

---

```yaml {config}
step: deploy
```
Deployment complete.
```

## Implementation Notes

1. **No nested exec**: Scripts cannot contain `{exec}` blocks
2. **Idempotent step names**: Steps must have unique names for routing
3. **JSON-stringify always**: Even primitive values get quoted
4. **Sequential only**: No parallel script execution
5. **Single question per step**: Only one question block per step

## Future Enhancements

- Parallel script execution with `mode=parallel`
- Script exit code handling
- Retry logic for failed scripts
- Persistent state across sessions
- Custom question UI components
