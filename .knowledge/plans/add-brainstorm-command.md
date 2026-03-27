# Execution Plan: Add `/brainstorm` Command

This plan outlines the steps to add a new `/brainstorm` command to the Gemini CLI framework. This command is designed for high-signal, critical-thinking sessions, providing a dedicated space for exploration and risk assessment without making any changes to the codebase.

## Objective
Implement a new `/brainstorm` command in `.gemini/commands/brainstorm.toml` that acts as a critical thinking partner, challenging ideas and identifying risks while strictly adhering to a "no side effects" mandate.

## Architectural Impact
- **Discovery Layer Enhancement**: Adds a dedicated tool for the "Discovery & Audit" phase of the project lifecycle.
- **Safety**: Reinforces the framework's philosophy of separating discovery/analysis from implementation/execution.
- **Documentation**: Updates the project's documentation to reflect the new capability.

## File Operations

### Create
- **`.gemini/commands/brainstorm.toml`**: The command definition file.

### Modify
- **`README.md`**: Update the "Phase 1: Planning & Discovery" section.
- **`docs/user-guide.md`**: Update the "Phase 1: Discovery & Audit" section.

---

## Step-by-Step Execution

### Step 1: Create the Command Definition
Create the file `.gemini/commands/brainstorm.toml` with the following content:

```toml
description = "Interactive brainstorming session to challenge ideas, identify risks, and explore alternatives without making changes."

prompt = \"\"\"
You are an expert critical thinking partner and strategic advisor. You are executing the custom `/brainstorm` command.

**CRITICAL MANDATE:** This command is strictly for exploration, risk assessment, and creative problem-solving. You MUST NOT modify, create, or delete any files in the repository. Your goal is to provide high-signal feedback and challenging questions.

Follow this interactive workflow:

### Phase 1: Context & Discovery (Optional)
1. If the brainstorming topic relates to existing code or documentation, use `list_directory`, `read_file`, `grep_search`, or `glob` to gather relevant context.
2. If external information is needed, use `web_search` and `web_fetch` to research state-of-the-art practices or similar problems.
3. Use `run_shell_command` only for read-only operations (e.g., `find`, `grep`, `ls`).

### Phase 2: Critical Exploration (The Loop)
1. **Analyze:** Evaluate the user's idea or problem statement. Look for hidden assumptions, potential edge cases, and architectural risks.
2. **Challenge:** Do not simply agree. Provide critical advice. If an idea seems flawed, explain why and suggest alternatives.
3. **Question:** Ask 1-3 hard, targeted follow-up questions to push the user's thinking further.
4. **Interactive Dialogue:** Use `ask_user` to present your critique and questions if they are structured. Or ask general questions. Keep the interaction fast and focused. Continue this loop until the user is satisfied or a natural conclusion is reached.

### Phase 3: Synthesis & Next Steps
1. Once the brainstorming session concludes, provide a concise summary of:
    - **Key Insights:** The most valuable takeaways from the session.
    - **Identified Risks:** Potential pitfalls or blockers discovered.
    - **Recommendations:** Actionable advice for the next phase.
2. **Propose Action:** Suggest that the user transition from brainstorming to planning by using the `/plan` command to turn these insights into a concrete technical strategy.

Start by asking the user for the topic or idea they want to brainstorm or infer from context if provided.
\"\"\"
```

### Step 2: Update Main README
Modify `README.md` to include `/brainstorm` in the "Phase 1: Planning & Discovery" section, after `/learn`:

```markdown
*   **`/brainstorm`**: An interactive, high-signal brainstorming session. The agent acts as a critical partner—challenging your assumptions, identifying architectural risks, and asking hard follow-up questions—without making any changes to the codebase.
```

### Step 3: Update User Guide
Modify `docs/user-guide.md` to include `/brainstorm` in the "Phase 1: Discovery & Audit" section, after `/debug`:

```markdown
### `/brainstorm`

Your tool for interactive, critical-thinking sessions.

- **How it works:** You present an idea, problem, or architectural choice. The agent uses discovery tools to gather context and then enters a "challenge loop" where it pushes back on weak points, identifies hidden risks, and asks tough questions.
- **Why it works:** It forces you to defend your ideas and refine them *before* they even reach the planning stage, ensuring higher-quality strategies.
```

---

## Testing Strategy

### 1. Functional Verification
Invoke the command:
```bash
gemini /brainstorm "Adding a new caching layer to the API"
```
**Expected Results:**
- The agent asks for more details or begins analyzing existing code using `list_directory` or `read_file`.
- The agent provides at least one critical observation (e.g., cache invalidation risks).
- The agent asks targeted follow-up questions.
- The agent *never* attempts to create or modify files.

### 2. Workflow Verification
- Ensure the session ends with a summary of insights and risks.
- Ensure the agent explicitly suggests using `/plan` at the end of the summary.

### 3. Documentation Verification
- Verify that the new command is listed correctly in the `README.md` and `docs/user-guide.md`.
- Verify that `gemini --help` (or equivalent) correctly displays the new command description if the CLI supports it.
