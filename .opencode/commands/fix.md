---
description: Hypothesis testing and issue resolution when tests are failing
agent: build
---

Hypothesis-testing and issue-resolution workflow.

### Purpose

When tests are failing, code is broken, or assumptions need verification.

### Workflow

1. **Identify failure**:
   - Read test output, error messages, stack traces
   - Understand what's expected vs. actual

2. **Formulate hypothesis**:
   - Create theory about root cause
   - Define success criteria

3. **Test hypothesis**:
   - Invoke `coder` subagent with:
     - The hypothesis to test
     - Available tools/languages
     - Success criteria

4. **Apply fix**:
   - Modify code to resolve the issue
   - Don't patch symptoms — fix the root cause

5. **Verify**:
   - Run tests until they pass
   - Small commits for each logical fix

### Reporting

After fix completion, report:
- Root cause identified
- Fix applied
- Verification (tests passing)

### Key Mandates
- **Fix the root cause** — Don't patch symptoms
- **Test-driven** — Write failing test first if applicable
- **Small commits** — Each fix is a logical unit
