# Plan: Implement Drafting and Editing Capabilities

This plan outlines the implementation of `/draft` and `/revise` commands to assist users in writing detailed white papers or research articles by leveraging existing project context and research.

## Objective
Enable a structured drafting and editing workflow that reuses existing subagents and follows a multi-phase process for content generation and refinement.

## Architectural Impact
- **Agent Refactoring**: Generalizes the `reporter` agent to be used across different contexts (research reports, white papers, etc.).
- **New Subagent**: Introduces an `editor` subagent specialized in linguistic and structural quality.
- **New Commands**: Adds `/draft` for interactive content generation and `/revise` for iterative refinement.
- **Workflow Integration**: Connects research, planning, and drafting into a cohesive pipeline.

## File Operations

### Modify
- `.gemini/agents/reporter.md`: Generalize the prompt to handle any source material and target files.

### Create
- `.gemini/agents/editor.md`: New subagent for structural and linguistic review.
- `.gemini/commands/draft.toml`: New command for the drafting workflow.
- `.gemini/commands/revise.toml`: New command for the revision workflow.

---

## Step-by-Step Execution

### Step 1: Refactor the `reporter` Subagent
Update `.gemini/agents/reporter.md` to be agnostic of specific file names (like `report.md`) or directories (like `research/`).
- **Action**: Modify `.gemini/agents/reporter.md`.
- **Changes**: Use general terms like "source materials" and "target document" instead of hardcoded paths. The caller (the main command) will provide specific context in its instructions.

### Step 2: Create the `editor` Subagent
Implement a new subagent specialized in refining drafts.
- **Action**: Create `.gemini/agents/editor.md`.
- **Role**: A Professional Editor focusing on grammar, structure, and technical writing style.
- **Tools**: `read_file`, `replace`, `list_directory`.

### Step 3: Implement the `/draft` Command
Define the multi-phase workflow for drafting.
- **Action**: Create `.gemini/commands/draft.toml`.
- **Phase 1 (Context Gathering)**: Search for existing context in `research/`, `plans/`, `TASKS.md`, and `journal/`. If no context is found, redirect the user to `/plan` or `/research`.
- **Phase 2 (Title & Location)**: Propose a title and path (e.g., `drafts/<title>.md`) and seek user approval.
- **Phase 3 (Outline Creation)**: Generate an initial outline, present it for user review, and refine based on feedback.
- **Phase 4 (Initialization)**: Create the skeleton file with placeholders for each section.
- **Phase 5 (Section-by-Section Drafting)**: Iteratively call the `reporter` subagent to fill each section using the gathered context.
- **Phase 6 (Conclusion)**: Summarize the result and suggest `/revise`.

### Step 4: Implement the `/revise` Command
Define the workflow for refining an existing draft.
- **Action**: Create `.gemini/commands/revise.toml`.
- **Phase 1 (File Selection)**: Prompt the user to select a file for revision.
- **Phase 2 (Analysis)**: Use the `editor` subagent to perform a structural and linguistic audit.
- **Phase 3 (Interactive Revision)**: Present findings and proposed changes to the user; apply improvements upon approval using `replace`.

---

## Testing Strategy

### 1. Functional Testing of `/draft`
- **Context Discovery**: Run `/draft` when `research/` or `plans/` are empty. Verify it suggests running `/plan` or `/research`.
- **Context Gathering**: Run `/draft` with existing research data. Verify it correctly identifies and summarizes the sources.
- **Interactive Outline**: Verify the `ask_user` loop for outline approval works as expected.
- **Iterative Drafting**: Verify that `reporter` correctly fills placeholders with detailed prose instead of summaries.

### 2. Functional Testing of `/revise`
- **Analysis**: Verify that the `editor` subagent identifies grammatical issues or awkward phrasing in a provided draft.
- **Refinement**: Verify that approved changes are correctly applied to the target file.
- **Style Adherence**: Check if the output follows technical writing standards (active voice, clarity, etc.).

### 3. Integration Testing
- **End-to-End Workflow**: Conduct a full cycle: `/research` -> `/plan` -> `/draft` -> `/revise`. Ensure the transitions between stages are smooth and context is preserved.
- **File Integrity**: Ensure that `replace` operations do not corrupt the markdown structure or accidentally delete sections.
