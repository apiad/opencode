# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
