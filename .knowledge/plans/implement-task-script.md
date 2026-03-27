# Execution Plan: Task Management Script Implementation

## Objective
Implement a procedural task management system by adding a Python script (`.gemini/scripts/task.py`) that acts as the single source of truth for `TASKS.md`. This will introduce dynamic categories, dependency tracking, complexity metrics, and automated structural formatting to project tasks.

## Architectural Impact
- **Single Source of Truth:** `TASKS.md` transitions from a manually edited document to an auto-generated artifact strictly managed by `.gemini/scripts/task.py`.
- **Workflow Enforcement:** The AI agents and developers will be explicitly forbidden from modifying `TASKS.md` directly. `.gemini/commands/task.toml` will be rewritten to interface exclusively with the new CLI.
- **Enhanced Task Metadata:** Introduces robust task properties (ID, dependencies, complexity, and categories) to improve task delegation, prioritization, and dependency resolution during agent workflows.

## File Operations
1. **Create:** `.gemini/scripts/task.py` (The core task management CLI).
2. **Modify:** `TASKS.md` (Add the strict warning header and run initial migration).
3. **Modify:** `.gemini/commands/task.toml` (Update instructions to force agent usage of the script).
4. **Create:** `tests/test_task_script.py` (Unit tests for the script's parser and logic).

---

## Step-by-Step Execution

### Step 1: Develop `.gemini/scripts/task.py`
Implement a Python CLI script using `argparse` to handle all task lifecycle events.

**1. Data Model & State Management:**
- Define a `Task` class with fields: `id`, `label`, `description`, `category`, `complexity`, `dependencies`, `status`, and `plan_path`.
- **Parser:** Implement a robust regex-based parser that reads `TASKS.md` into memory. The script must parse tasks formatted as: 
  `- [Status] **[ID]** Label: Description (Complexity: X) [Deps: Y] (See plan: Z)`
- **Formatter:** Implement a serializer that writes the entire list of tasks back to `TASKS.md`. It must:
  - Preserve the "NEVER MODIFY THIS FILE BY HAND" warning block.
  - Group tasks into two main sections: `## Active Tasks` and `## Archive`.
  - Within `Active Tasks`, dynamically generate `### <Category Name>` headers.
  - **Sorting:** Compute a global topological level (depth) for each task based on its `dependencies`. Within each category group, sort tasks primarily by their topological level, and secondarily by `complexity`.

**2. Subcommands:**
- `add`: Accepts `--label`, `--description`, `--category`, `--complexity`, and `--dependencies`. 
  - *Logic:* Dynamically creates categories. Generates a unique ID using the category's first initial + auto-incrementing integer (e.g., `UX` -> `U.1`, `U.2`).
- `start`: Accepts `--task-id`. Updates task status to `[/]` (In Progress).
- `cancel`: Accepts `--task-id`. Updates task status to `[-]` (Cancelled).
- `archive`: Accepts `--task-id`. Updates task status to `[x]` (Done) and flags it to be moved to the `## Archive` section upon rendering.
- `attach-plan`: Accepts `--task-id` and `--plan-path`. Updates the task's linked plan.

### Step 2: Initialize & Migrate `TASKS.md`
- Embed a fallback migration routine in the parser to handle the current, unstructured `TASKS.md` format.
- Existing active and archived tasks should be assigned to a default `General` category, receiving generated IDs (e.g., `G.1`, `G.2`).
- Prepend the file with a prominent warning header:
  ```markdown
  # Tasks

  > **WARNING: NEVER MODIFY THIS FILE BY HAND. USE THE SCRIPT INSTEAD.**
  > Run `python .gemini/scripts/task.py --help` for usage.
  ```

### Step 3: Update `.gemini/commands/task.toml`
- Modify the system prompt to explicitly restrict the agent from using file-editing tools on `TASKS.md`.
- Replace the current manual instructions with CLI execution commands:
  - **Action Create:** Run `python .gemini/scripts/task.py add --label "..." --description "..." --category "..." ...`
  - **Action Work:** Run `python .gemini/scripts/task.py start --task-id <ID>` before beginning work.
  - **Action Update/Complete:** Run `python .gemini/scripts/task.py archive --task-id <ID>` upon successful completion.

### Step 4: Implement Tests
Create `tests/test_task_script.py` using `pytest`.
- **Graph Logic:** Test the topological sorting algorithm and ensure circular dependencies trigger a clear validation error.
- **Parsing/Formatting:** Assert that parsing an expected markdown output and re-serializing it results in an exact string match (no data loss).
- **ID Generation:** Validate the auto-incrementing logic when injecting new tasks into existing or novel categories.

---

## Testing Strategy
1. **Unit Testing:** Execute `pytest tests/test_task_script.py` to validate core logic (parsing, sorting, cycle detection) in isolation.
2. **Migration Dry-Run:** Backup the current `TASKS.md`, invoke the script's migration function, and verify that all current tasks are preserved under the `General` category with new IDs.
3. **End-to-End CLI Test:** Manually execute a full lifecycle on a test file: `add` -> `attach-plan` -> `start` -> `archive`. Verify the task remains in `Active Tasks` until the `archive` command moves it to `Archive`.
4. **Agent Workflow Validation:** Trigger the agent via `ai task create "Refactor UI"` and observe the tool calls to confirm it strictly invokes the Python script rather than editing the markdown file directly.
