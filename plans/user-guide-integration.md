# Execution Plan: Comprehensive User Guide Integration

This plan outlines the steps to create a formal User Guide for the Gemini CLI Opinionated Framework, based on the philosophy and workflows described in the `drafts/architect-in-the-machine.md` document.

## Objective
To add a comprehensive `docs/user-guide.md` that detail the framework's core principles, command workflows (Discovery & Strategy, Software Development, Content Creation, Background Tasks), and practical usage examples, while integrating it into the MkDocs navigation.

## Architectural Impact
- **Documentation Enhancement:** Provides a central, user-centric guide to using the framework.
- **Workflow Formalization:** Translates informal blog-post-style drafts into structured documentation.
- **Improved Discoverability:** Integrates new content into the existing MkDocs site navigation.

## File Operations

### Create
- `docs/user-guide.md`: The new user guide content.

### Modify
- `mkdocs.yml`: Add the new page to the navigation.

---

## Step-by-Step Execution

### Step 1: Content Extraction & Structure
Extract the following key elements from `drafts/architect-in-the-machine.md`:
- **Philosophical Principles:**
    1.  The important things should be made explicit (explicit context).
    2.  Resist the urge to guess (intentional actions).
    3.  Delegate (specialized sub-agents).
- **Sub-Agent Roles:** `planner`, `researcher`, `reporter`, `editor`.
- **Context Architecture:** The roles of `journal/`, `plans/`, `research/`, and `TASKS.md`.

### Step 2: Implement `docs/user-guide.md`
Create the file with the following sections:

1.  **Introduction:** Briefly explain the "Architect in the Machine" concept and the goal of high-velocity development with AI.
2.  **Core Principles:** Detailed section on the three principles mentioned above.
3.  **The Discovery & Strategy Workflow:**
    -   **/research:** Explain its use for external knowledge gathering and synthesis.
    -   **/plan:** Explain the interactive analysis of the codebase and creation of the execution roadmap.
4.  **The Software Development Workflow:**
    -   **/issues:** How to use the GitHub CLI integration for strategic prioritization.
    -   **/task:** Managing the `TASKS.md` roadmap.
    -   **/commit:** The process for creating atomic, Conventional Commits from `git diff`.
    -   **/release:** Automating versioning, changelogs, and tagging.
5.  **The Content Creation Workflow:**
    -   **/draft:** Detail the multi-phase process (context scan, outline creation, section expansion).
    -   **/revise:** Explain the structural and linguistic audit process using the `editor` agent and `style-guide.md`.
6.  **The Background Tasks Workflow:**
    -   **/cron:** How to configure and run scheduled natural language tasks via `cron.toml`.
    -   **/maintenance:** Strategies for managing technical and "contextual" debt.

### Step 3: Update `mkdocs.yml`
Modify the `nav` section to include the User Guide. Suggested placement:

```yaml
nav:
  - Home: index.md
  - User Guide: user-guide.md
  - Setup & Deployment: deploy.md
  - Architecture & Design: design.md
  - Development & Contribution: develop.md
```

### Step 4: Final Review & Refinement
- Ensure the tone is formal yet accessible.
- Verify that all command descriptions align with their actual implementations.
- Cross-reference with `docs/design.md` and `docs/develop.md` to ensure consistency.

---

## Testing Strategy
1.  **Markdown Validation:** Verify that `docs/user-guide.md` follows standard GFM and has no broken links.
2.  **MkDocs Integration:** Run `mkdocs build` to ensure the site compiles without errors.
