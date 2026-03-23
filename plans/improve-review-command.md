# Plan: Improve `/review` Command and `reviewer` Agent (Non-Destructive)

This plan outlines the migration and enhancement of the legacy `/revise` command into a more structured, non-destructive `/review` command, supported by an upgraded `reviewer` agent. The new workflow focuses on generating a detailed sidecar review report.

## Objective
Transition from the basic editing workflow to a rigorous, multi-phase review process that produces a comprehensive `<filename>.review.md` file. This ensures high-level structural integrity, concrete substance, and polished linguistic quality without modifying the original source.

## Architecture
- **Command Migration:** Rename `.gemini/commands/revise.toml` to `.gemini/commands/review.toml`.
- **Agent Migration:** Rename `.gemini/agents/editor.md` to `.gemini/agents/reviewer.md`.
- **Sidecar Reporting:** Instead of using `replace`, all findings are written to a `<filename>.review.md` file.
- **Workflow Orchestration:** Implements a strict sequential pipeline: **Setup -> Plan -> Phase 1 (Structural) -> Phase 2 (Substance) -> Phase 3 (Linguistic) -> Finalization**.

---

## Detailed Workflow

### Phase 0: Setup & Style Selection
- **File Selection:** Prompt the user to select a file for review.
- **Style Guide:** Ask the user if they want to provide a specific style guide or instructions. If not, propose `.gemini/style-guide.md` as the default.
- **Initialization:** Create/Overwrite `<filename>.review.md` with a header and metadata.

### Phase 1: Review Depth Planning
- **Goal:** Determine the review depth and phases based on the document's complexity and the Style Guide.
- **Action:** Read the target file and the selected style guide.
- **Review Plan:** Divide the review into phases (from abstract/high-level to concrete/low-level). For each phase, determine the specific points of interest and patterns to check.
- **Approval:** Present the plan to the user for approval. Save the approved plan to the `.review.md` file.

### Phases 1..N: Multi-Phase Review Execution
For each phase (e.g., Structural, Content, Linguistic):
- **Agent Invocation:** Invoke the `reviewer` agent with specific instructions for the current phase only.
- **Deep Analysis:** The `reviewer` reads the style guide and the document, performing targeted `grep_search` and `read_file` calls to find specific issues (e.g., "AI-isms", passive voice, weak hooks).
- **Report Generation:** The `reviewer` produces a comprehensive report for that phase, including specific examples and suggested fixes.
- **Persistence:** Append the phase report to the corresponding section in `<filename>.review.md`.

### Finalization
- **Goal:** Notify the user and suggest next steps.
- **Action:** Inform the user that the review is complete and the `.review.md` file is ready.
- **Next Steps:** Suggest the user to use the `/draft` command, attaching the newly created review file to apply the desired modifications.

---

## Implementation Steps

### Step 1: Rename and Refactor Files
1.  **Rename Command:** Move `.gemini/commands/revise.toml` to `.gemini/commands/review.toml`.
2.  **Rename Agent:** Move `.gemini/agents/editor.md` to `.gemini/agents/reviewer.md`.

### Step 2: Update `reviewer` Agent (`.gemini/agents/reviewer.md`)
1.  **Update Name:** Change name from `editor` to `reviewer`.
2.  **Capabilities:** Ensure it has access to `grep_search` and `read_file`.
3.  **Prompt:** Update the system prompt to reflect its role as a deep critic that produces structured reports for specific review phases.

### Step 3: Update `/review` Command (`.gemini/commands/review.toml`)
1.  **Orchestration Logic:** Rewrite the prompt to follow the non-destructive multi-phase workflow.
2.  **Persistence Logic:** Use `write_file` (initial) and `replace` (to append or fill sections) to manage the `<filename>.review.md` file.
3.  **Phase Management:** Ensure it loops through the approved phases, invoking the agent for each.

### Step 4: Cross-Reference Updates
1.  **Update `/draft` Command:** Modify `.gemini/commands/draft.toml` to reference `/review` and mention the capability to ingest `.review.md` files.
2.  **README/Docs:** Update documentation to reflect the new tool and workflow.

---

## Verification Strategy

### 1. Functional Testing
- **Non-Destructive:** Verify the original file is NEVER modified by the `/review` command.
- **File Creation:** Ensure `<filename>.review.md` is correctly created and populated.
- **Phase Sequence:** Confirm the command executes each phase as planned and approved.

### 2. Quality Audit
- **Grep Usage:** Verify the `reviewer` agent actually uses `grep_search` to find patterns (e.g., searching for "---" or specific "AI-ism" triads).
- **Style Alignment:** Check that the generated review reflects the rules in the selected Style Guide.
