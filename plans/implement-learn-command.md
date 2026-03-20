# Plan: Implement `/learn` Command and `learn.md` Agent

## Objective
Implement a new `/learn` command and a specialized `learn.md` agent to automate the process of exploring new technologies, experimenting with them, and codifying that knowledge into reusable "skills" within the project.

## Architectural Impact
- **New Workflow**: Introduces a structured learning lifecycle (Research -> Experiment -> Codify).
- **Knowledge Management**: Systematically populates `.gemini/skills/` with vetted information and idiomatic examples.
- **Agent Specialization**: Adds a `learner` agent to the existing suite of specialized agents (`planner`, `researcher`, etc.).

## Step-by-Step Execution


### Step 1: Create the Command Definition

Create `.gemini/commands/learn.toml`:
- **Description**: "Explore and master a new library or topic, generating a permanent project skill."
- **Prompt**: Direct the agent to initialize the `learn` agent with the provided library/topic name.

### Step 2: Create the Learning Agent

Consult `cli_help` to determine the exact expected structure for a skill.

Create `.gemini/agents/learn.md` with a high-discipline system prompt:
- **Tools Required**: `google_web_search`, `web_fetch`, `read_file`, `write_file`, `list_directory`, `ask_user`, and the `learner` subagent.
- **Phase 1: Environment Audit**: Check if the library is already installed (e.g., checking `pyproject.toml`, `package.json`, or using `pip show`).
- **Phase 2: Research and Mapping**:
    - Use `google_web_search` and `web_fetch` to identify core concepts, API surface, and common patterns.
    - **Survey local source files briefly** to see if the library is already being used or if there are specific integration points.
- **Phase 3: User Approval (Checkpoint)**: Present a structured "Learning Map" to the user for approval before proceeding.
- **Phase 4: Grounded Experimentation**:
    - Use the `learner` subagent to write and run small test scripts.
    - Verify "gotchas," performance quirks, and idiomatic usage through actual code execution.
- **Phase 5: Skill Generation**:
    - Create `.gemini/skills/<skill-name>/SKILL.md` and optional `reference-*.md` files.
    - Populate with a concise reference, common patterns, and links to example scripts.
- **Phase 6: Asset Management & Cleanup**:
    - Move successful experiment scripts to the skill's assets folder.
    - Delete temporary files and artifacts.

### Step 3: Align with Project Standards
- Ensure the agent follows idiomatic preferences according to the language/framework/etc, but also aligned with the current project idioms if present.

## Testing Strategy
1. **Initial Run**: Execute `/learn httpx`.
2. **Verification of Approval**: Ensure the agent stops and presents a structured "Learning Map" including local context if relevant.
3. **Skill Validation**: Check that `.gemini/skills/httpx/SKILL.md` is created correctly.
4. **Asset Check**: Verify that the skill directory contains at least one working example script.
5. **Cleanliness**: Ensure no temporary experiment files remain in the root directory.
