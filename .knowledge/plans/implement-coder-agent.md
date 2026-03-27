# Plan: Integrate `coder` Subagent into `/task work` Workflow

This plan outlines the steps to create a specialized `coder` subagent and refactor the `/task` command to delegate granular implementation tasks to it, following a strict Red-Green-Verify (TCR) protocol.

## Objective
Enhance the `/task work` workflow by introducing a `coder` subagent responsible for the "grunt work" of test-driven development. This separation of concerns allows the primary project manager (PM) agent to focus on high-level orchestration (branching, task tracking, integration) while the `coder` ensures rigorous implementation through a "test-first" mantra.

## Architectural Impact
- **Agentic Specialization:** Introduces a new `local` agent (`coder`) with full access to file modification and shell tools.
- **Workflow Orchestration:** Refactors the `/task` command to act as an orchestrator that delegates implementation steps to the `coder` subagent.
- **TCR Enforcement:** The `coder` agent is explicitly instructed to follow the Red-Green-Verify loop, ensuring all code is backed by tests and remains simple and maintainable.

## File Operations

### Create
1.  **.gemini/agents/coder.md**: Definition and instructions for the new `coder` subagent.
2.  **tests/test_task_command.py**: Integration tests to verify the `coder` subagent's role in the `/task` workflow.

### Modify
1.  **.gemini/commands/task.toml**: Update the `work` action to delegate implementation steps to the `coder`.
2.  **docs/user-guide.md**: Update the documentation to reflect the new agentic delegation in the `/task work` workflow.

## Step-by-Step Execution

### Step 1: Create the `coder` Subagent
Create `.gemini/agents/coder.md` with the following configuration:
- **Role:** Expert "grunt coder" specialized in granular, test-driven changes.
- **Mantra:** Red (Write failing test) -> Green (Implement minimal code) -> Verify (Run tests).
- **Style:** Simple, non-clever code, no premature optimization, PEP 257-compliant docstrings.
- **Tools:** `list_directory`, `read_file`, `grep_search`, `glob`, `write_file`, `replace`, `run_shell_command`.
- **Instruction:** Explicitly mandate that the agent must run tests before and after implementation and report success/failure back to the orchestrator.

### Step 2: Refactor the `/task` Command
Modify `.gemini/commands/task.toml` to update the `Work` action:
- **Delegation:** Change Phase 3 ("The TCR Loop") to instruct the orchestrator to:
    1. Break the task into granular steps.
    2. For each step, invoke the `coder` subagent.
    3. Based on the `coder`'s report, perform the corresponding Git operation (`git commit` on success, `git checkout .` on failure).
- **Control:** Ensure the orchestrator retains control over branching, merging, and user check-ins.

### Step 3: Update User Documentation
Modify `docs/user-guide.md`:
- Locate the `/task` and "Full Feature Development Walkthrough" sections.
- Update the description of the Red-Green-Verify loop to mention that implementation is handled by the specialized `coder` subagent.

### Step 4: Implement Validation Tests
Create `tests/test_task_command.py`:
- **Structure Test:** Verify `.gemini/agents/coder.md` exists and follows the framework's agent structure.
- **Integration Test:** Verify that `.gemini/commands/task.toml` contains a reference to the `coder` agent within its `prompt`.
- **Consistency Test:** Ensure the `coder` agent's toolset includes all required tools (`write_file`, `replace`, `run_shell_command`).

## Testing Strategy

### Automated Tests
- **Structural Integrity:** Run `pytest tests/test_structure.py` to ensure the new files match the framework's expectations.
- **Command/Agent Sync:** Run `pytest tests/test_sync.py` to ensure the new/updated commands are correctly documented in the README and User Guide.
- **Delegation Logic:** Run the newly created `pytest tests/test_task_command.py`.

### Manual Verification
- **Prompt Review:** Read the final `task.toml` prompt to ensure the delegation instructions are clear and the PM's role in the TCR loop (pre-flight, isolation, integration) is correctly defined.
- **Agent Instruction Review:** Read `coder.md` to ensure the Red-Green-Verify mantra is the central focus of the agent's behavior.
