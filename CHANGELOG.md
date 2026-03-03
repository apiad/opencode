# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Added `/draft` and `/revise` commands with `reporter` and `editor` subagents for structured content generation.
- Created an actionable project style guide in `.gemini/style-guide.md`.
- Drafted the "The Architect in the Machine" Substack article showcasing the framework.

### Changed
- Overhauled the `/research` command into an extensible, executive-style reporting workflow with iterative updates and asset linking.
- Refactored `/draft` and `/revise` commands to integrate step-by-step, style-driven audits.
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
- Refactored the `/research` command into a robust 3-phase workflow using specialized `researcher` and `reporter` subagents.
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
- Refactored `.gemini/hooks/welcome.py` to include new commands.
- Simplified `GEMINI.md` to a cleaner starter template.
- Updated `.gemini/commands/release.toml` to include dependency and source version updates.

### Fixed
- Typo in `release.toml` formatting.
