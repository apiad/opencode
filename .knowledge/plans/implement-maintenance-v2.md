# Implementation Plan: Dynamic Structural Testing and Documentation Sync

## 1. Objective
This plan addresses the gaps identified in `research/maintainance-report-2026-03-23-v2.md`. It implements a scalable, dynamic testing strategy for all commands and agents, refactors brittle legacy tests to focus on migration integrity, and ensures full documentation synchronization for the `/scaffold` and `/onboard` commands.

## 2. Architectural Impact
- **Dynamic Validation:** Replaces hardcoded individual tests with a discovery-based suite (`tests/test_structure.py`) that automatically covers new commands/agents.
- **Maintenance Efficiency:** Reduces test code volume by removing redundant structural checks from specialized test files.
- **Documentation Integrity:** Enforces a 1:1 mapping between available commands and the User Guide, eliminating brittle "skip lists" in the synchronization tests.

## 3. File Operations

| Action | File Path | Description |
| :--- | :--- | :--- |
| **Create** | `tests/test_structure.py` | New test file using `pytest.mark.parametrize` for blanket coverage. |
| **Modify** | `tests/test_review_command.py` | Cleanup of structural/content assertions; retain migration checks. |
| **Modify** | `docs/user-guide.md` | Add/Update documentation for `/scaffold` and `/onboard`. |
| **Modify** | `tests/test_sync.py` | Remove hardcoded skips for `scaffold` and `onboard`. |

## 4. Step-by-Step Execution

### Step 1: Implement Dynamic Structural Testing
Create `tests/test_structure.py` with the following requirements:
- **Command Discovery:** Use `os.listdir(".gemini/commands/")` to find all `.toml` files.
- **Command Logic:** Verify each command is valid TOML and has non-empty `description` and `prompt` strings.
- **Agent Discovery:** Use `os.listdir(".gemini/agents/")` to find all `.md` files.
- **Agent Logic:** Verify each agent is valid Markdown and contains the agent's name (filename without extension) in the content.

### Step 2: Refactor `tests/test_review_command.py`
- **Delete:** `test_reviewer_agent_exists`, `test_review_command_exists`, `test_reviewer_agent_is_valid_markdown`, `test_review_command_is_valid_toml`, `test_maintenance_command_is_audit`, `test_planner_agent_read_only`, `test_writer_agent_exists`, `test_draft_command_is_multimode`.
- **Retain:** `test_editor_agent_gone`, `test_revise_command_gone`, `test_reporter_agent_gone` to ensure migration state persists.

### Step 3: Documentation Sync
- **Update `docs/user-guide.md`**: Ensure the `/scaffold` and `/onboard` sections have consistent "How it works" and "Why it works" formatting.
- **Update `tests/test_sync.py`**: Remove the exclusion list in `test_commands_synced_in_user_guide` so that `scaffold` and `onboard` are strictly checked for documentation presence.

### Step 4: Final Validation
- Run the full test suite using `make test`.
- Verify the total number of tests in `test_structure.py` matches the number of files in `.gemini/commands/` (15) and `.gemini/agents/` (6).

## 5. Testing Strategy
1. **Dynamic discovery check:** Add a dummy command `temp_test.toml` and verify `make test` automatically picks it up and fails (due to lack of content).
2. **Sync check:** Temporarily remove `/scaffold` from `docs/user-guide.md` and verify `tests/test_sync.py` fails.
3. **Migration check:** Ensure `tests/test_review_command.py` passes, confirming legacy files have not been reintroduced.
