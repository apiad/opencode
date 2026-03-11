# Development & Contribution

The **Gemini CLI Opinionated Framework** enforces a high-discipline development lifecycle. Whether you are a human or an AI contributor, adherence to these standards is mandatory.

## 🔄 The Mandatory Workflow Lifecycle

Every non-trivial change must follow this strict three-phase process:

### 1. Research & Analysis
Before proposing a change, use the `/research` command to gather context, analyze the current codebase, and identify potential risks.

### 2. Strategic Planning
A feature is not considered "active" until a persistent Markdown plan has been created in the `plans/` directory. Use the `/plan` command to generate this strategy and synchronize it with `TASKS.md`.

### 3. Execution & Validation
- **Incremental Implementation:** Break features into small, testable commits.
- **Continuous Validation:** After every implementation turn, the framework automatically runs the `makefile`. Do not attempt to bypass this process.
- **Journaling:** A brief, one-line technical log must be added to the daily journal for every significant turn.

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
