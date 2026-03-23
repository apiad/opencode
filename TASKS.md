# Tasks

Legend:

- [ ] Todo
- [/] In Progress (@user) <-- indicates who is doing it
- [x] Done

**INSTRUCTIONS:**

Keep task descriptions short but descriptive. Do not add implementation details, those belong in task-specific plans. When adding new tasks, consider grouping them into meaningful clusters such as UX, Backend, Logic, Refactoring, etc.

Put done tasks into the Archive.

---

---

## Active Tasks

- [ ] Improve the `/review` command and evolve the `reviewer` agent to a non-destructive, multi-phase audit workflow. (See plan: plans/improve-review-command.md)

---

## Archive

- [x] Implement the new `/learn` command and specialized `learner` agent with a 2-layer orchestration system for technology exploration and skill codification. (2026-03-20) (See plan: plans/implement-learn-command.md)

- [x] Consolidate project hooks into a single Git pre-commit hook (2026-03-20) (See plan: plans/consolidate-hooks.md)

- [x] Implement the hypothesis-driven debugging workflow for the `/debug` command and `debugger` agent. (2026-03-18) (See plan: plans/hypothesis-driven-debug-command.md)

- [x] Draft the blog article "Revenge of the Test-Driven Nerds" exploring the shift from human-driven to AI-agent-driven TCR. (2026-03-16)
- [x] Update the core documentation suite (index, develop, design, user-guide) to incorporate the new TCR protocol and task isolation principles. (2026-03-16)
- [x] Refine `install.sh` to protect existing scaffolding files (README, TASKS, etc.) while ensuring the core framework (.gemini, GEMINI.md) is updated. (2026-03-16) (See plan: plans/refine-install-script.md)
- [x] Refactor the `/task` command to prioritize a strict TCR (Test-Commit-Revert) protocol for working on tasks. (2026-03-16) (See plan: plans/implement-tcr-task-command.md)

- [x] Update `install.sh` to be served via GitHub Pages and update all references to use the new URL. (2026-03-11)
- [x] Create comprehensive User Guide (`docs/user-guide.md`) based on "The Architect in the Machine" philosophy. (2026-03-11) (See plan: plans/user-guide-integration.md)
- [x] Refine `/plan` command to strictly enforce a non-execution mandate for generated plans. (2026-03-11)
- [x] Integrate MkDocs with Material theme and setup automatic GitHub Pages deployment via CI/CD. (2026-03-11) (See plan: plans/mkdocs-integration.md)
- [x] Create comprehensive project documentation in `docs/` (Overview, Deployment, Design, Development). (2026-03-11)
- [x] Refine `/onboard` command to include documentation or source code discovery. (2026-03-11)
- [x] Simplify `/onboard` command to use direct file analysis instead of sub-agents. (2026-03-11)
- [x] Implement conditional journal hook enforcement based on file modification times. (2026-03-11) (See plan: plans/conditional-journal-enforcement.md)
- [x] Implement conditional `make` hook execution based on file modification times. (2026-03-11) (See plan: plans/conditional-make-hook.md)
- [x] Consolidate `add-gemini.sh` into a unified, non-destructive `install.sh` for setup and updates. (2026-03-11) (See plan: plans/unified-installer.md)
- [x] Implement the `install.sh` scaffolding script for new projects. (2026-03-03) (See plan: plans/install-script-scaffolding.md)
- [x] Refactor the `/research` command to follow a more extensible, executive-style reporting workflow with iterative updates and asset linking. (2026-03-02)
- [x] Implement drafting (`/draft`) and editing (`/revise`) capabilities using specialized subagents. (2026-03-02) (See plan: plans/drafting-and-editing-capabilities.md)
- [x] Implement a custom `/plan` command workflow and a `planner` sub-agent for repository analysis and plan generation in `plans/`. (2026-03-02)
- [x] Implement a `/cron` command and synchronization hook with systemd user timers for scheduled tasks. (2026-03-02)
- [x] Add the /issues command to manage project issues with GitHub CLI. (2026-02-28)
- [x] Refactor the hook system: centralize shared logic into `.gemini/hooks/utils.py` and add PEP 257 docstrings. (2026-02-28)
- [x] Rewrite the `README.md` to explain the opinionated framework and its key features. (2026-02-28)
- [x] Refactor the `/research` command into a 3-phase workflow with researcher and reporter subagents. (2026-02-28)
- [x] Consolidate the `/task/*` commands into a single `/task` command. (2026-02-28)

> Done tasks go here, in the order they where finished, with a finished date.
