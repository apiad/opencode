# 🤖 Gemini CLI Opinionated Framework

<div align="center">

[![Release](https://img.shields.io/github/v/release/apiad/starter?style=for-the-badge&color=blue)](https://github.com/apiad/starter/releases)
[![License](https://img.shields.io/github/license/apiad/starter?style=for-the-badge&color=success)](LICENSE)
[![Template](https://img.shields.io/badge/Repository-Template-blueviolet?style=for-the-badge&logo=github)](https://github.com/apiad/starter/generate)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/apiad/starter/graphs/commit-activity)

**Transform how you work with AI agents.**

*A cognitive partnership model that enforces rigorous engineering standards, strategic planning, and continuous validation.*

</div>

---

## 🧠 The Core Philosophy: AI as a Senior Partner

In this framework, the AI agent is not just a "code generator" or a "copilot". It is a **Senior Architect and Critical Thinking Partner**.

*   **🛡️ Critical Feedback First:** The agent is instructed to challenge unsafe, redundant, or poorly conceived ideas *before* writing a single line of code.
*   **📋 Research -> Plan -> Execute:** Every non-trivial change follows a strict lifecycle. The agent first researches context, proposes a detailed plan, waits for your explicit approval, and only then begins implementation.
*   **✅ Validation-Always:** The framework uses `make` as a source of truth. The agent is hooked into the `makefile` to ensure every change is validated (linted and tested) before being finalized.

## 🛠️ Powerful Commands

The `.gemini/commands/` directory defines specialized workflows that automate the entire development lifecycle:

### 📁 Project Management & Discovery
*   **`/onboard`**: Summarizes the project's architecture, standards, and current state to quickly orient a new developer (or the agent itself).
*   **`/task`**: Manages the project roadmap in `TASKS.md`. Use it to `create` new tasks, `work` on existing ones (marks as In Progress), `report` on priorities, or `update` the roadmap.
*   **`/issues`**: Integrates with the GitHub CLI (`gh`) to list, create, or update issues. It can transition from an issue directly into an implementation **Plan**.

### 🏗️ Development & Maintenance
*   **`/scaffold`**: Initializes a new project from scratch using modern, standard tooling (Python/uv, TS/npm, Rust/cargo, etc.) and sets up a compatible `makefile`.
*   **`/research <topic>`**: A deep, 3-phase investigation workflow (Planning -> Data Gathering -> Reporting) that produces exhaustive Markdown reports in the `research/` directory.
*   **`/maintenance`**: Performs a deep scan of the codebase to identify refactoring opportunities, improve documentation, and increase test coverage.
*   **`/docs`**: Analyzes the codebase and journals to generate or update comprehensive project documentation in the `docs/` folder.
*   **`/cron`**: Manages repetitive background tasks (e.g., daily reports, health checks) using **systemd user timers**.

### 🚀 Shipping & Quality
*   **`/commit`**: Analyzes changes, groups them into logical features or fixes, and guides you through committing them individually using **Conventional Commits**.
*   **`/release`**: Automates the final shipping steps: running tests, determining the next version (semver), updating the `CHANGELOG.md`, and tagging the release.

## 🔄 Common Workflows

This framework shines when you combine these commands into cohesive workflows:

### 1️⃣ Feature Lifecycle: From Idea to Ship
1.  **Discovery:** `/research "best way to implement X"`
2.  **Planning:** `/task create "Implement X based on research"`
3.  **Implementation:** `/task work "Implement X"`
4.  **Refining:** `/docs` to ensure documentation is up-to-date.
5.  **Committing:** `/commit` to logically group and commit changes.
6.  **Releasing:** `/release` to bump the version and tag the code.

### 2️⃣ Routine Maintenance & Health
1.  **Investigation:** `/maintenance` to identify technical debt.
2.  **Automation:** `/cron "daily maintenance"` to run linting or small refactorings during off-hours.
3.  **Reporting:** `/task report` to see pending roadmap items.

### 3️⃣ Collaboration & Issue Tracking
1.  **Triage:** `/issues summary` to see what needs attention.
2.  **Deep Dive:** `/issues work 42` to research issue #42 and propose a fix.
3.  **Onboarding:** New collaborators run `/onboard` to get up to speed in seconds.

## ⚓ The Hook System: Staying in Sync

The framework uses a robust hook system (`.gemini/hooks/`) that synchronizes the agent with your project state:

*   **`session.py`**: Initializes the environment and provides a project summary.
*   **`journal.py`**: Ensures a journal entry exists for the current date (`journal/YYYY-MM-DD.md`).
*   **`make.py`**: Automatically runs `make` after critical agent actions to prevent regressions.
*   **`cron.py`**: Synchronizes `cron.toml` tasks with **systemd user timers**.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
