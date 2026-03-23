# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.20.0] - 2026-03-23

### Added
- **Unified Discovery-Plan-Execute Lifecycle:** Formally established a strict three-phase architectural boundary (Discovery -> Plan -> Execution).
- **Modernized Test Suite (uv/pytest):** Replaced legacy testing infrastructure with `uv` for dependency management and `pytest` for automated validation.
- **Dynamic Structural Testing:** Implemented `tests/test_structure.py` for discover-based, schema-compliant verification of all 15 commands and 6 agents.
- **Documentation Overhaul:** Updated the entire documentation suite (`docs/index.md`, `docs/design.md`, `docs/develop.md`, `docs/user-guide.md`) to reflect the new unified lifecycle and technical stack.
- **Improved Content Creation:** Refactored the `/draft` command and evolved the `writer` agent for review-driven refinement.

### Changed
- **Read-Only Audit Workflows:** Refactored `/maintenance` and `/review` (formerly `/revise`) to be strictly read-only 'Discovery' commands that produce artifacts for `/plan`.
- **Review Command Evolution:** Evolved the `/review` command into a non-destructive, multi-phase audit workflow with sidecar reporting.
- **Agent Naming Alignment:** Renamed `editor` to `reviewer` and `reporter` to `writer` for improved semantic clarity.
- **Test Optimization:** Refactored `tests/test_review_command.py` and `tests/test_sync.py` to be dynamic and less brittle, removing hardcoded skips and string matches.

## [0.19.1] - 2026-03-20

### Changed
- **Documentation Suite Overhaul:** Major updates to the entire documentation suite (`index.md`, `deploy.md`, `design.md`, `develop.md`, `user-guide.md`, and `README.md`) to accurately reflect the framework's v0.19.0 improvements, including the `/learn` command, the dual-layer hook system, and the updated testing philosophy.

## [0.19.0] - 2026-03-20

### Added
- **Knowledge Mastering (/learn):** Introduced a new 4-phase grounded learning lifecycle (Audit, Research, Execution, Codification) to automate mastering new technologies.
- **Learner Sub-agent:** A specialized "Grounded Learning Specialist" agent that verifies library behavior through real-world code experimentation.
- **Skill System:** A permanent project knowledge base in `.gemini/skills/` with mandatory YAML frontmatter for autonomous agent activation.
- **Comprehensive Documentation Update:** Integrated the `/learn` command and skill system into the framework's documentation suite.

### Changed
- **Testing Philosophy:** Updated documentation to reflect a shift toward agent-driven validation and TCR (Test-Commit-Revert) protocols instead of traditional unit tests.

## [0.18.0] - 2026-03-20

### Added
- **Installer Boilerplate Generation:** `docs/install.sh` now generates clean, generic boilerplate for `README.md`, `CHANGELOG.md`, `TASKS.md`, and `makefile` instead of copying project-specific versions when scaffolding a new project.
- **Scientific Debugging Documentation:** Added comprehensive documentation for the `/debug` command's scientific, hypothesis-driven workflow in `docs/design.md` and `docs/user-guide.md`.

### Changed
- **Documentation Suite Overhaul:** Major updates to the entire documentation suite (`index.md`, `deploy.md`, `design.md`, `develop.md`, `user-guide.md`) to reflect recent framework changes, including the Journal-First philosophy, TCR (Test-Commit-Revert) loop details, and safe update logic.

## [0.17.1] - 2026-03-20

### Changed
- **Journal Logic Refinement:** Simplified the journal entry mechanism in `docs/install.sh` by consolidating logic to always utilize the project's internal `journal.py` script, ensuring consistent audit logs across environments.

## [0.17.0] - 2026-03-20

### Added
- **Safe Installation Update Logic:** Re-engineered `docs/install.sh` to prevent data loss. It now performs surgical updates of `.gemini/` subdirectories instead of full overwrites.
- **Project Configuration Protection:** Introduced a whitelist of protected files (e.g., `settings.json`, `style-guide.md`) that are preserved during framework updates.
- **Intelligent GEMINI.md Preservation:** The installation script now detects and preserves the "Project Notes" section within `GEMINI.md`, allowing for seamless framework updates without losing project-specific context.
- **Enhanced Installation Transparency:** Improved the install script's summary phase to explicitly list files being created, updated, or protected.

## [0.16.0] - 2026-03-20

### Added
- **Timestamp-Based Journal Validation:** Implemented an automated check in the `pre-commit.py` hook that parses the latest journal entry's ISO timestamp and compares it against the modification times of any changed files.
- **Journal Script Tooling:** Added `.gemini/scripts/journal.py`, a simple utility script for correctly formatting and appending new journal entries.
- **Hook Installation Check:** Added an automatic check to the `welcome.py` script that alerts the user if the project's pre-commit hooks are not installed.

### Changed
- **Improved Hook Robustness:** Enhanced the pre-commit script to correctly ignore the journal file's own modification when checking for pending documentation updates.

## [0.15.0] - 2026-03-20

### Added
- **Consolidated Lifecycle Hooks:** Integrated all project-specific lifecycle hooks into a single, efficient `pre-commit.py` script.
- **Enabled Gemini Lifecycle Hooks:** Enabled the Gemini CLI framework's automatic hook execution system in `.gemini/settings.json`.
- **Improved Hook Robustness:** Enhanced the pre-commit script to correctly detect staged files and automatically set the executable bit for required scripts.
- **Makefile Integration:** Added a new `install-hooks` target to the `makefile` for easy setup of the project's hook system.

### Changed
- **Refactored Hook System:** Simplified the hook architecture by moving from individual task-based hooks to a unified validation strategy.
- **Enhanced Hook Feedback:** Improved error messages and output formatting for all lifecycle hooks.

## [0.14.0] - 2026-03-18

### Added
- **Notification Hook:** Implemented a new `AfterAgent` hook (`notify.py`) that sends a desktop notification using `notify-send` and plays a system "ping" sound (via `paplay`) when the agent completes its turn.
- **Hook Robustness:** Improved project name detection in notifications by correctly identifying the git repository root.

### Changed
- **Hook Sequencing:** Refined the `AfterAgent` hook block to be sequential, ensuring notifications only trigger if preceding validation hooks (like `make` or `journal`) return an `allow` decision.

## [0.13.0] - 2026-03-18

### Added
- **Hypothesis-Driven Debugging:** Refactored the `/debug` command and `debugger` agent to implement a scientific, hypothesis-driven workflow. Includes status analysis, hypothesis formulation with user approval, and isolated testing in temporary `debug/hyp-*` branches.
- **Content:** Added a new blog post draft "Revenge of the Test-Driven Nerds" to the `drafts/` directory.

### Changed
- **Command Rename:** Renamed the `.gemini/commands/docs.toml` to `.gemini/commands/document.toml` for better semantic clarity.
- **Settings:** Removed the experimental `plan` setting from `.gemini/settings.json`.
- **Documentation:** Enhanced installation and setup documentation with detailed project scaffolding and integration steps.

## [0.12.0] - 2026-03-16

### Added
- Implemented a strict TCR (Test-Commit-Revert) protocol for the `/task work` command, enforcing Red-Green-Refactor development cycles on dedicated feature branches.

### Changed
- Refined `install.sh` to protect project scaffolding files (e.g., `README.md`, `TASKS.md`) from being overwritten while ensuring core framework files are always updated.
- Updated documentation and roadmap to reflect the new workflow improvements.

## [0.11.0] - 2026-03-11

### Added
- Unified `install.sh` script that handles both initial project bootstrapping and non-destructive framework updates/integrations in existing repositories.
- Automatic git environment validation (clean tree requirement) and post-install commits to `install.sh`.
- Interactive summary and confirmation of proposed changes (created vs. updated files) in the installer.
- **Documentation Suite:** Integrated MkDocs with Material theme and a comprehensive User Guide based on "The Architect in the Machine" philosophy.
- **Operational Safety:** Conditional `make` and journal hook execution based on file modification times.
- **Performance:** Simplified `/onboard` command using direct file analysis instead of sub-agents.
- **Refinement:** Strictly enforced non-execution mandate for `/plan` output.

### Removed
- `add-gemini.sh` script (its logic is now integrated into the unified `install.sh`).

### Changed
- Streamlined `README.md` with a single, unified "Quick Start" command for all use cases.
- Relocated `install.sh` to `docs/` to enable serving via GitHub Pages at `https://apiad.github.io/starter/install.sh`.

## [0.10.1] - 2026-03-03

### Changed
- Updated `install.sh` and `add-gemini.sh` to suggest running `gemini /onboard` instead of launching the CLI automatically.

### Fixed
- Improved ASCII art and version display in the banner function of installer scripts.

## [0.10.0] - 2026-03-03

### Added
- Implemented `install.sh` scaffolding script to automate project bootstrapping from the template.
- Implemented `add-gemini.sh` integration script for adding the framework to existing repositories.
- Added professional ASCII banners with versioning to all installer scripts for improved UX.

### Changed
- Refined `README.md` with streamlined Quick Start and new Integration sections.

## [0.9.0] - 2026-03-03

### Added
- Implemented `/debug` command and forensic `debugger` subagent for root-cause analysis (RCA).
- Created a specialized forensic investigation workflow for bug detection and documentation.

### Changed
- Refined `scaffold` and `revise` command instructions for better clarity and consistency.
- Improved README documentation and project metadata.

## [0.8.0] - 2026-03-02

### Added
- Implemented `/plan` command workflow and `planner` subagent for architectural planning.
- Added `/draft` and `/review` commands with `writer` and `reviewer` subagents for structured content generation.
- Created an actionable project style guide in `.gemini/style-guide.md`.
- Drafted the "The Architect in the Machine" Substack article showcasing the framework.

### Changed
- Overhauled the `/research` command into an extensible, executive-style reporting workflow with iterative updates and asset linking.
- Refactored `/draft` and `/review` commands to integrate step-by-step, style-driven audits.
- Refined `/plan` and `/task` workflows.

## [0.7.0] - 2026-03-02

### Added
- Implemented `/cron` command with `cron.toml` task configuration using systemd user timers for background execution.
- Project badges and emoji headers to `README.md` for better visual appeal.

### Changed
- Comprehensive overhaul of `README.md` with detailed command descriptions and common workflows.
- Cleaned up `.gemini/settings.json` by removing redundant plan path.

## [0.6.0] - 2026-03-02

### Added
- Automate `gh release create` in `/release` command.

### Changed
- Cleanup deleted maintenance typo file.
- Fix maintenance typo and simplify command descriptions.
- Update `/research` command and subagents for better organization.

### Fixed
- Remove unused `subproc` import in `welcome` hook.

## [0.5.0] - 2026-02-28

### Added
- New `/issues` command to manage project issues with GitHub CLI, supporting summaries, creation/updates, and work modes.

### Changed
- Updated `README.md` and `welcome.py` hook to include information about the `/issues` command.
- Internal documentation updates in `TASKS.md` and `journal/`.

## [0.4.0] - 2026-02-28

### Changed
- Refactored the hook system: centralized shared logic into `.gemini/hooks/utils.py` and renamed hook files for consistency (`session.py`, `log.py`, `make.py`, `journal.py`).
- Added PEP 257 docstrings to all hooks and improved internal documentation.

### Added
- Updated `TASKS.md` and `journal/2026-02-28.md` with details of the hook refactoring.
- Ignore `__pycache__` directories in `.gitignore`.

## [0.3.0] - 2026-02-28

### Added
- Refactored the `/research` command into a robust 3-phase workflow using specialized `researcher` and `writer` subagents.
- Rewrote the `README.md` to explain the opinionated framework, the agent's behavior, hooks, commands, journaling, and the project initialization workflow.

### Changed
- Improved the `/release` command logic to include `README.md` updates and fix formatting issues.

## [0.2.0] - 2026-02-28

### Added
- Added a new `/scaffold` command for project initialization with modern tooling (e.g., Python/uv, JS/npm).

### Changed
- Updated the `/release` command to include updating `README.md` and fixed a minor typo.

## [0.1.0] - 2026-02-28

### Added
- Consolidated `/task/*` commands into a single `/task` command in `.gemini/commands/task.toml`.
- Enhanced `/release` command to include version update steps.
- Initial project task tracking with `TASKS.md`.
- Daily journal tracking in `journal/`.

### Changed
- Refactoried `.gemini/hooks/welcome.py` to include new commands.
- Simplified `GEMINI.md` to a cleaner starter template.
- Updated `.gemini/commands/release.toml` to include dependency and source version updates.

### Fixed
- Typo in `release.toml` formatting.
