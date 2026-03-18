# Hypothesis-Driven Debugging Workflow Plan

Implemented a sophisticated, scientific debugging workflow for the `.gemini/` framework.

## Objective
Refactor the `/debug` command and `debugger` agent to use a hypothesis-driven approach involving isolated diagnostic branches and automated testing.

## Architectural Impact
- **Structured Logic:** Moves debugging from "search and trace" to "hypothesize and experiment".
- **Isolation:** Uses temporary git branches (`debug/hyp-*`) for all diagnostic changes, ensuring the `main` branch remains stable.
- **Tooling:** Grants the `debugger` agent `write_file` access for diagnostic purposes only.

## File Operations

### 1. `.gemini/agents/debugger.md`
- **Change:** Add `write_file` to `tools`.
- **Change:** Update instructions to allow code modification for diagnostic purposes (e.g., adding logs, reproduction scripts).
- **Change:** Implement a structured reporting format (Hypothesis, Actions, Observations, Conclusion).

### 2. `.gemini/commands/debug.toml`
- **Change:** Implement Phase 1: Context & Status Analysis (including `makefile`/auto-detect test check).
- **Change:** Implement Phase 2: Hypothesis Formulation & `ask_user` approval loop.
- **Change:** Implement Phase 3: Hypothesis Testing Loop with mandatory `git branch` creation and cleanup.
- **Change:** Implement Phase 4: Synthesis and RCA report generation.

## Execution Steps

### Step 1: Update Debugger Agent
Modify `.gemini/agents/debugger.md` to enable the experimental mandate. The agent will now be instructed to prove or disprove hypotheses by adding diagnostic code and running tests.

### Step 2: Refactor Debug Command Logic
Update `.gemini/commands/debug.toml` with the new orchestration prompt. This includes the logic for:
- Detecting test runners (Makefile vs Auto-detect).
- Generating and switching between temporary branches.
- Managing the user approval flow for hypotheses.
- Synthesizing subagent reports into a final RCA.

## Testing & Validation
- **Dry Run:** Trigger `/debug` with a simulated issue to verify the hypothesis formulation stage.
- **Branch Verification:** Confirm the command creates `debug/hyp-` branches and successfully deletes them after the subagent returns.
- **Cleanup Check:** Verify that Phase 1 correctly identifies and offers to clean up "stale" debug branches from previous interrupted sessions.
- **RCA Verification:** Ensure the final output follows the Root Cause Analysis format and suggests a `/plan` for the fix.
