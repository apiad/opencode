# Execution Plan: Documentation and Test Synchronization

## Objective
Harmonize the project's documentation with its implementation by standardizing command names, filling documentation gaps, and replacing brittle tests with a dynamic synchronization verification suite.

## Architectural Impact
- **Consistency:** Ensures that users and AI agents have a single, accurate source of truth for command names and capabilities.
- **Maintainability:** Reduces test suite fragility by moving from hard-coded string matching to dynamic discovery.
- **Safety:** Strengthens the link between implementation (TOML/Markdown) and documentation (README/User Guide) through automated CI checks.

## File Operations

### Files to Modify:
- `README.md`: Update `/learn` description; ensure `/document` is correctly referenced.
- `docs/index.md`: Rename `/docs` references to `/document`.
- `docs/user-guide.md`:
    - Rename `/docs` to `/document`.
    - Add missing `/scaffold` and `/onboard` sections.
    - Remove redundant `/learn` section.
    - Explicitly identify `learner` and `debugger` as subagents.
- `tests/test_review_command.py`: Refactor to remove brittle string assertions.

### Files to Create:
- `tests/test_sync.py`: New dynamic test suite for implementation-documentation synchronization.

---

## Step-by-Step Execution

### Phase 1: Documentation Harmonization

#### Step 1.1: Update `docs/index.md`
- Replace the legacy `/docs` command reference with `/document` in the "Key Capabilities" section.

#### Step 1.2: Update `docs/user-guide.md`
- **Search & Replace:** Globally replace `/docs` with `/document`.
- **Deduplication:** Remove the second, redundant occurrence of the `### /learn` section.
- **Explicit Agent Identification:**
    - Update the `/learn` section to explicitly mention the `learner` subagent.
    - Update the `/debug` section to explicitly mention the `debugger` subagent.
- **Add Missing Commands:**
    - Add a `### /onboard` section under "The Discovery & Strategy Workflow".
    - Add a `### /scaffold` section under "The Software Development Workflow".

#### Step 1.3: Update `README.md`
- Update the `/learn` section under "Phase 1: Planning & Discovery" to explicitly mention the `learner` subagent (consistent with how `/debug` and `/plan` are described).

---

### Phase 2: Test Suite Refactoring

#### Step 2.1: Refactor `tests/test_review_command.py`
- Modify `test_reviewer_agent_has_grep_search` to verify file existence and basic Markdown structure (e.g., presence of a title) instead of specific tool names like `grep_search`.
- Modify `test_review_command_is_multiphase` to verify the TOML file contains `description` and `prompt` keys, rather than searching for specific "Phase X" strings.
- Simplify `test_maintenance_command_is_audit` and `test_planner_agent_read_only` to focus on existence and high-level role rather than internal implementation details.
- Retain "gone" file checks (e.g., `test_editor_agent_gone`) as they validate successful migrations.

---

### Phase 3: Dynamic Synchronization Implementation

#### Step 3.1: Create `tests/test_sync.py`
Implement a pytest-compatible script that performs the following:
1.  **Command Discovery:** Programmatically list all `.toml` files in `.gemini/commands/`.
2.  **Agent Discovery:** Programmatically list all `.md` files in `.gemini/agents/`.
3.  **Forward Sync Check:**
    - Verify every discovered command is mentioned as `/{command}` in both `README.md` and `docs/user-guide.md`.
    - Verify every discovered agent is mentioned in `docs/design.md` and `docs/user-guide.md`.
4.  **Reverse Sync Check:**
    - Parse `README.md` and `docs/user-guide.md` for any strings matching the `/{command}` pattern.
    - Assert that each found pattern (excluding known exceptions like `/docs`) has a corresponding `.toml` file in `.gemini/commands/`.
5.  **Agent Role Verification:**
    - Ensure `README.md` and `docs/user-guide.md` use the terms "agent" or "subagent" when describing the specialized roles (e.g., `planner`, `researcher`, `learner`).

---

## Testing Strategy

### 1. Manual Validation
- Inspect the modified `docs/user-guide.md` and `README.md` to ensure formatting is correct and descriptions are accurate.
- Verify that the `/document` command is used consistently across all files.

### 2. Automated Validation
- **Run the refactored suite:** Execute `pytest tests/test_review_command.py` to ensure the new, leaner assertions pass.
- **Run the synchronization suite:** Execute `pytest tests/test_sync.py`. This test is expected to fail initially if any commands were missed during the manual update phase, providing an automated "punch list" for completion.

### 3. CI/CD Integration
- Ensure these new tests are picked up by the `make test` target, which is triggered by the `pre-commit.py` hook and GitHub Actions.
