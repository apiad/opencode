---
id: literate-commands-implementation
created: 2026-03-30
modified: 2026-03-30
type: plan
status: active
expires: 2026-04-06
phases:
  - name: Core Plugin Structure & Acknowledgment
    done: false
    goal: Basic plugin that intercepts commands and injects acknowledgment
  - name: Markdown Parsing
    done: false
    goal: Parse command markdown into structured steps
  - name: Step-by-Step Injection
    done: false
    goal: Inject steps sequentially on session.idle
  - name: Variable Substitution
    done: false
    goal: Interpolate $variables from metadata into prompts
  - name: Script Execution
    done: false
    goal: Execute {exec} blocks with variable substitution
  - name: Structured Parsing & Routing
    done: false
    goal: Parse model responses and route based on conditions
---

# Plan: Literate Commands Implementation

## Context

Implement the literate-commands plugin from `.knowledge/notes/literate-commands-design.md`. User wants interactive testing after each sub-step, not fully autonomous implementation.

## File Structure

```
.opencode/
├── plugins/
│   └── literate-commands.js    # Single plugin file
└── commands/
    └── test.md                 # Test command for development
```

---

## Phase 1: Core Plugin Structure & Acknowledgment

**Goal:** Basic plugin skeleton that intercepts a command and injects acknowledgment.

**Deliverable:** Working plugin that catches any `/test` command and responds with acknowledgment.

**Done when:**
- [ ] Plugin loads without errors
- [ ] `/test` command triggers acknowledgment
- [ ] Model receives: "We are preparing to run the /test command. Stand by."

### Sub-steps

**1.1 Create plugin file skeleton**
```javascript
// .opencode/plugins/literate-commands.js
export default async function literateCommandsPlugin(input) {
    return {
        "command.execute.before": async (input, output) => { ... },
        event: async ({ event }) => { ... }
    }
}
```

**1.2 Intercept command**
- Hook into `command.execute.before`
- Check for `literate: true` in command frontmatter
- If not literate, return early (let normal execution happen)
- If literate, set up state and modify output

**1.3 Inject acknowledgment**
- Replace output.parts with acknowledgment message
- Set initial state with steps array (empty for now)
- Log setup for debugging

**1.4 Create test command**
```markdown
---
description: Test literate commands
agent: analyze
literate: true
---

First acknowledgment injected.

---

Step 1 content.

---

Step 2 content.
```

**1.5 Test manually**
```bash
opencode /test
# Should see acknowledgment
```

---

## Phase 2: Markdown Parsing

**Goal:** Parse command markdown into structured Step objects with config, prompt, and code blocks.

**Deliverable:** Parsed steps printed to logs, no execution yet.

**Done when:**
- [ ] `parseLiterateMarkdown()` extracts all steps
- [ ] Each step has config, prompt, and codeBlocks
- [ ] Code blocks are parsed with language and meta
- [ ] YAML config block is parsed correctly

### Sub-steps

**2.1 Implement split-by-separator**
```javascript
function parseLiterateMarkdown(content) {
    // Remove frontmatter
    // Split by /^---$/m
    // Return array of section strings
}
```

**2.2 Implement YAML config extraction**
```javascript
function parseConfig(section) {
    // Find ```yaml {config}...```
    // Parse YAML
    // Return config object
}
```

**2.3 Implement code block extraction**
```javascript
function parseCodeBlocks(section) {
    // Find all ```lang {meta}...```
    // Return array: { language, meta: [], code }
}
```

**2.4 Implement prompt extraction**
```javascript
function extractPrompt(section) {
    // Remove config block
    // Remove code blocks
    // Return remaining text trimmed
}
```

**2.5 Test parsing**
```bash
opencode /test
# Check logs for parsed step structure
```

---

## Phase 3: Step-by-Step Injection

**Goal:** On session.idle, inject next step's prompt via promptAsync.

**Deliverable:** All steps inject sequentially without waiting.

**Done when:**
- [ ] session.idle triggers step injection
- [ ] Step 1 prompt appears in chat
- [ ] Step 2 injects after model responds
- [ ] All steps complete, state cleaned up

### Sub-steps

**3.1 Set up state on command intercept**
```javascript
state = {
    steps: parsedSteps,
    currentStep: 0,
    metadata: {},
    sessionID: input.sessionID,
    commandName: command,
    arguments: args
}
```

**3.2 Implement step injection on idle**
```javascript
event: async ({ event }) => {
    if (event.type !== 'session.idle') return
    if (!state) return
    
    const step = state.steps[state.currentStep]
    if (!step) { cleanup(); return }
    
    await client.session.promptAsync({
        path: { id: sessionID },
        body: { parts: [{ type: 'text', text: step.prompt }] }
    })
    
    state.currentStep++
}
```

**3.3 Advance step index after injection**
- Increment `currentStep` after each injection
- No waiting for parse/routing yet (Phase 4)

**3.4 Test sequential injection**
```bash
opencode /test
# Should see: ack → step1 → step2 → ...
```

---

## Phase 4: Variable Substitution

**Goal:** Interpolate `$variables` from metadata into prompts and scripts.

**Deliverable:** `$TOPIC` renders as `"Topic Value"` in prompts.

**Done when:**
- [ ] `$ARGUMENTS` works
- [ ] `$varname` substitutes from metadata
- [ ] `$obj.nested` accesses nested values
- [ ] `$$` injects full metadata object
- [ ] Undefined vars render as `undefined`

### Sub-steps

**4.1 Implement JSON.stringify interpolation**
```javascript
function interpolate(text, metadata) {
    return text.replace(/\$(\$|[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)/g, (match, path) => {
        if (path === '$') return JSON.stringify(metadata)
        const value = getNestedValue(metadata, path)
        return JSON.stringify(value)
    })
}
```

**4.2 Implement nested path access**
```javascript
function getNestedValue(obj, path) {
    return path.split('.').reduce((o, k) => o?.[k], obj)
}
```

**4.3 Add $ARGUMENTS to initial metadata**
```javascript
metadata = { ARGUMENTS: args }
```

**4.4 Test variable substitution**
```markdown
---
literate: true
---

## Step 1
Args: $ARGUMENTS

---

## Step 2
Topic: $topic
```

---

## Phase 5: Script Execution

**Goal:** Execute `{exec}` code blocks before injecting step prompt.

**Deliverable:** Scripts run with variable substitution, output replaces block.

**Done when:**
- [ ] `{exec}` blocks are detected
- [ ] Custom interpreter parses (e.g., `{exec=uv run python}`)
- [ ] Variables substituted in script before execution
- [ ] mode=stdout replaces block with output
- [ ] mode=store parses JSON and merges into metadata
- [ ] mode=none runs silently

### Sub-steps

**5.1 Parse exec block metadata**
```javascript
function parseExecMeta(meta) {
    // {exec} → { interpreter: 'default', mode: 'stdout' }
    // {exec=python3} → { interpreter: 'python3', mode: 'stdout' }
    // {exec mode=store} → { interpreter: 'default', mode: 'store' }
}
```

**5.2 Implement variable substitution for scripts**
- Same as Phase 4 but applied to script code

**5.3 Implement script runner**
```javascript
async function runScript(code, interpreter, mode) {
    // Build command based on interpreter
    // Execute via Bun.$
    // Capture stdout
    // Handle mode:
    //   - stdout: return output
    //   - store: JSON.parse, merge into metadata
    //   - none: return ''
}
```

**5.4 Default interpreter mapping**
```javascript
const interpreters = {
    'python': 'python3',
    'python3': 'python3',
    'bash': 'bash',
    'sh': 'sh',
    'javascript': 'node',
    'js': 'node'
}
```

**5.5 Run scripts before step injection**
```javascript
// In idle handler, before promptAsync:
for (const block of step.codeBlocks) {
    if (block.meta.includes('exec')) {
        const output = await runScript(...)
        // Replace block in markdown with output
    }
}
```

**5.6 Test with test command**
```markdown
```bash {exec}
echo "Hello $ARGUMENTS"
```
```python {exec mode=store}
import json
print(json.dumps({"count": 5, "topic": "test"}))
```
```

---

## Phase 6: Structured Parsing & Routing

**Goal:** Parse model responses for variables, route based on conditions.

**Deliverable:** `parse:` block extracts variables, `match:` routes to correct step.

**Done when:**
- [ ] `parse:` extracts string variables
- [ ] `parse:` with `?` suffix extracts booleans
- [ ] `match:` routes based on pattern matching
- [ ] `match:` with boolean variables works
- [ ] `wait: true` pauses for user reply
- [ ] `question:` presents options and routes

### Sub-steps

**6.1 Implement JSON response extraction**
```javascript
function extractJSONResponse(text) {
    // Find ```json...``` or ```...```
    // Try JSON.parse
    // Return parsed object or null
}
```

**6.2 Implement variable extraction from parse: config**
```javascript
function extractVariables(response, parseConfig, metadata) {
    // Try JSON.parse on response
    // For each key in parseConfig:
    //   - If key ends with '?', extract boolean
    //   - Otherwise, extract string
    // Merge into metadata
}
```

**6.3 Implement pattern matching for routing**
```javascript
function matchRoute(metadata, matchConfig) {
    // For each key in matchConfig:
    //   - If key ends with '?':
    //     - If value is true, go to matchConfig[key]
    //   - Else if metadata[key] matches pattern:
    //     - Return matchConfig[key]
    // Return matchConfig.otherwise or null
}
```

**6.4 Implement wait for user reply**
```javascript
// In idle handler:
if (step.config.wait) {
    // Don't advance step index yet
    // Wait for next idle after user reply
    // Then parse variables and route
}
```

**6.5 Implement question routing**
```javascript
// If step.config.question exists:
// Present question via tool or injected prompt
// On response, route based on selected option
```

**6.6 Test with complex command**
```markdown
```yaml {config}
step: ask
wait: true
question:
    title: "Continue?"
    options:
        Yes: proceed
        No: stop
```
```

---

## Success Criteria

1. Plugin loads without errors
2. `/test` command executes through all steps
3. Variables interpolate correctly
4. Scripts execute and modify behavior
5. Routing works for all config options
6. State cleans up after completion

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| promptAsync timing issues | Medium | Add delays if needed |
| YAML parsing edge cases | Low | Use yaml library |
| Script injection security | None | Sandboxed env only |
| State cleanup on errors | Medium | Add try/finally |

## Related

- Design: `.knowledge/notes/literate-commands-design.md`
- Experiment: `.experiments/literate-commands/`
