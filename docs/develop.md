# Development & Contribution

The **Gemini CLI Opinionated Framework** enforces a high-discipline development lifecycle. Whether you are a human or an AI contributor, adherence to these standards is mandatory.

## 🔄 The Mandatory Workflow Lifecycle

Every non-trivial change must follow this strict three-phase process:

### 1. Research & Analysis

Before proposing a change, use the `/research` command to gather context, analyze the current codebase, and identify potential risks.

### 2. Strategic Planning

A feature is not considered "active" until a persistent Markdown plan has been created in the `plans/` directory. Use the `/plan` command to generate this strategy and synchronize it with `TASKS.md`.

### 3. Execution & Validation (TCR Protocol)

The `/task work on ...` command implements a strict **TCR (Test-Commit-Revert)** protocol to ensure high-velocity, high-quality code.

#### **Phase 1: Pre-flight Verification**

The agent verifies that the working tree is clean, the current branch is `main`, and `make test` passes as a baseline.

#### **Phase 2: Task Isolation**

A dedicated feature branch (e.g., `feature/task-name`) is auto-generated and checked out. All subsequent work for this task occurs here.

#### **Phase 3: The Red-Green-Verify Loop**

For every granular step of the implementation:

1.  **Red:** Write a failing test and verify failure with `make test`.
2.  **Green:** Implement the minimal code to pass.
3.  **Verify:** Run `make test`.
    - **Pass:** `git commit` the step.
    - **Fail:** Attempt one quick fix; if it still fails, **revert** to the last green state (`git checkout .`).

#### **Phase 4: Integration**

Once all steps are complete, a final test run is performed. Upon user approval, the branch is merged back to `main` and the roadmap in `TASKS.md` is updated.

## ✅ Testing & Quality Standards

- **Source of Truth:** The `makefile` is the central definition of project health.
- **Mandatory Commands:** Ensure `make test`, `make lint`, and `make format` pass before committing.
- **Documentation-as-Code:** Any new feature must be accompanied by relevant updates to the `docs/` directory.

## 🌲 Git & Source Control

### 1. Clean Working Tree

The framework requires a clean working tree for critical actions. Commit often to avoid merge conflicts or large, unmanageable diffs.

### 2. Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

- **`feat:`**: A new feature for the user.
- **`fix:`**: A bug fix for the user.
- **`docs:`**: Documentation-only changes.
- **`chore:`**: Maintenance, dependencies, or internal tooling updates.
- **`refactor:`**: Code changes that neither fix a bug nor add a feature.

### 3. Commit Scoping

When possible, provide a scope to the commit message (e.g., `feat(onboard): add documentation discovery`).

## ✍️ Documentation Style

- **Markdown:** All documentation and logs must be in GitHub-flavored Markdown.
- **Kebab-case:** Use kebab-case for all filenames in the `docs/`, `plans/`, and `research/` directories.
- **Direct & Technical:** Documentation should be concise, high-signal, and technically rigorous.

---

*Return to the [Project Overview](index.md).*
