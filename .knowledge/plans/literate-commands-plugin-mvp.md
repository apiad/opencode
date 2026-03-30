---
id: literate-commands-plugin-mvp
created: 2026-03-29
modified: 2026-03-29
type: plan
status: in_progress
phases:
  - name: Core Parsing & Step Execution
    done: false
    goal: Parse markdown, execute steps sequentially
  - name: Variable Substitution
    done: false
    goal: Support $ARGUMENTS, $TOPIC, $GLOB, $FILES
  - name: Question & Routing
    done: false
    goal: Implement question blocks with conditional routing
  - name: Code Execution
    done: false
    goal: Support {exec} and {subagent=X} code blocks
  - name: Testing & Refinement
    done: false
    goal: Test with research.md, fix issues
---

# Plan: Literate Commands Plugin MVP

## Context

Build a simple opencode plugin that executes commands defined as long-form markdown with step-by-step execution. Based on the `research.md` example in `examples/literate-commands/`.

## Architecture

**Single file**: `.opencode/plugins/literate-commands.ts`

```
.experiments/literate-commands/
├── literate-commands.ts   # Single plugin source (MVP)
└── test.md                # Test command file
```

### Hooks Used

| Hook | Purpose |
|------|---------|
| `command.execute.before` | Intercept command, load markdown, abort normal exec |
| `experimental.chat.messages.transform` | Inject step prompts, handle completions |
| `tool.execute.before/after` | Intercept question tool, inject responses |
| `event` | Listen for `session.idle` to advance steps |

## Phases

### Phase 1: Core Parsing & Step Execution

**Goal:** Parse markdown into steps, execute them sequentially

**Steps:**
1. Create plugin file with basic structure
2. Implement `parseLiterateMarkdown()`:
   - Split by `---` separators
   - Extract `{config}` YAML blocks
   - Extract prompt text
   - Extract code blocks with metadata
3. Implement `executeStep()`:
   - Inject step prompt into session via message transform
   - Wait for `session.idle`
4. Implement step queue:
   - Store steps in session state
   - Track current step index
   - Advance to next step on completion

**Deliverable:** Plugin that loads `research.md`, executes `define` → `planning` steps in order

---

### Phase 2: Variable Substitution

**Goal:** Support variable expansion in prompts

**Variables:**
| Variable | Source |
|----------|--------|
| `$ARGUMENTS` | User input to command |
| `$TOPIC`, `$TITLE`, etc. | From `parse:` section in define step |
| `$NAME` | From code execution results |
| `$FILES(path)` | File contents |
| `$GLOB(pattern)` | File list matching pattern |

**Steps:**
1. Implement `substituteVariables(text, context)`
2. Support `$ARGUMENTS` substitution
3. Support `parse:` in define step config:
   - Extract structured output from LLM response
   - Store as variables
4. Implement `$FILES()` and `$GLOB()` helpers
5. Test with `$TOPIC` in synthesize step

**Deliverable:** `$TOPIC`, `$ARGUMENTS`, `$GLOB` work in prompts

---

### Phase 3: Question & Routing

**Goal:** Implement question blocks with conditional routing

**Config syntax:**
```yaml
step: approval
question:
    title: Do you approve?
    options:
        Yes: collect
        No*: refine
```

**Steps:**
1. Detect `question:` in step config
2. Inject question tool call into message stream
3. Listen for user response
4. Route based on selected option
5. Support `No*` (editable feedback)
6. Implement `max-iter` for loop safety
7. Support `next:` for linear flow

**Deliverable:** User can approve/refine research plan, routes correctly

---

### Phase 4: Code Execution

**Goal:** Support `{exec}` and `{subagent=X}` code blocks

**Block types:**
| Syntax | Behavior |
|--------|----------|
| `{exec}` | Execute code, inject result |
| `{subagent=AGENT}` | Generator yields → spawn agents |
| `{exec subagent=AGENT}` | Both execute + yield spawns |

**Steps:**
1. Parse code blocks with metadata extraction
2. For `{exec}`:
   - Detect structured output from LLM
   - Execute Python code
   - Inject result into message stream
3. For `{subagent=AGENT}`:
   - Execute generator function
   - For each yielded string: `client.session.create()`
   - Wait for completion
4. Implement `$NAME` variable for execution results
5. Handle `$TOPIC` in yielded strings (subagent prompts)

**Deliverable:** Scout agents write to `research/$TOPIC/assets/`

---

### Phase 5: Testing & Refinement

**Goal:** Test with research.md, fix issues

**Test scenarios:**
1. `/research "AI frameworks"` → full flow
2. Approve plan → collect → synthesize
3. Reject plan → refine loop
4. Multiple subagents execute in parallel
5. Variables substitute correctly

**Deliverable:** Working research command

---

## Technical Decisions

### Code Execution (MVP)
- Use `Bun.shell` (`$`) for Python execution
- Pass data via stdin/stdout JSON
- No sandboxing for MVP

### Subagent Spawning
- Use `client.session.create()` 
- Pass agent type from `{subagent=AGENT}`
- Pass prompt from yielded string

### State Management
- In-memory Maps keyed by sessionID
- No persistence (session-scoped)

### Markdown Parsing
- Split by `---` (with optional whitespace trimming)
- Use regex to extract `{config}` YAML blocks
- Use regex to extract code blocks with `{meta}`

---

## Testing Methodology

### Test Infrastructure

```bash
# Directory structure for testing
.experiments/literate-commands/
├── literate-commands.ts   # Plugin source
├── commands/
│   └── test.md           # Test command file
└── test-runner.sh        # Optional: test automation script
```

### Running Tests

```bash
# 1. Create test command in .opencode/commands/
mkdir -p .opencode/commands
# Add test.md command file

# 2. Run the command directly (non-interactive)
cd /path/to/project
opencode run "/test AI frameworks"

# 3. With debug logging
opencode run --print-logs --log-level DEBUG "/test args" 2>&1 | tee test-output.log

# 4. Optional: Use a persistent server (faster startup for repeated tests)
# Terminal 1: Start server
opencode serve --port 4096

# Terminal 2: Run tests
opencode run --attach http://localhost:4096 "/test args"
```

### Test Scenarios

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | Basic step execution | `/test hello` | Executes steps in order |
| 2 | Variable substitution | `/test AI frameworks` | `$ARGUMENTS` replaced |
| 3 | Parse + variables | `/test "LLM stuff"` | `$TOPIC` synthesized |
| 4 | Question routing | Approve | Routes to next step |
| 5 | Loop routing | Reject | Routes to refine |
| 6 | Code execution | `/test code` | `{exec}` runs, result injected |
| 7 | Subagent spawn | `/research X` | Scouts write files |

### Debugging

| Flag | Purpose |
|------|---------|
| `--print-logs` | Show plugin logs in stderr |
| `--log-level DEBUG` | Verbose logging |
| `--format json` | Machine-parseable output |
| `--continue` | Continue last session |
| `--session ID` | Debug specific session |

### Test Command Example

Create `.opencode/commands/debug.md`:

```markdown
---
description: Debug test for literate-commands plugin
agent: analyze
---

```yaml {config}
step: start
```
This is a test. Args: $ARGUMENTS

---
```yaml {config}
step: end
```
Debug test complete.
```

---

## Open Questions

1. **Error handling:** What if code execution fails? Continue or abort?
2. **Timeout:** Subagent wait timeout?
3. **Subagent output:** Where do scouts write? Just prompt, or file path in yielded string?

---

## Next Steps After MVP

- Error recovery and retries
- More languages (JS, Bash)
- Persistence (resume interrupted commands)
- Custom question UI
- Structured output for parse sections
