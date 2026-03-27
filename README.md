# OpenCode

<div align="center">

[![Release](https://img.shields.io/github/v/release/apiad/opencode?style=for-the-badge&color=blue)](https://github.com/apiad/opencode/releases)
[![License](https://img.shields.io/github/license/apiad/opencode?style=for-the-badge&color=success)](LICENSE)

**An intelligent, multi-agent CLI framework for software engineering automation.**

*This repository provides the installer, templates, and documentation. The actual framework lives in [opencode-core](https://github.com/apiad/opencode-core).*

</div>

---

## Quick Start

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
```

## Installation Modes

The installer supports two modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| `--mode=copy` | Copy framework files into your project | Self-contained, no external dependencies |
| `--mode=link` | Link to opencode-core as a git submodule | Auto-updates with the framework |

```bash
# Interactive mode (prompts for mode selection)
curl -fsSL https://apiad.github.io/opencode/install.sh | bash

# Explicit copy mode
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --mode=copy

# Explicit link mode
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --mode=link
```

Run `--help` for all options.

## Architecture

OpenCode uses a two-repository architecture:

| Repository | Purpose |
|------------|---------|
| [opencode](https://github.com/apiad/opencode) (this repo) | Installer, templates, documentation |
| [opencode-core](https://github.com/apiad/opencode-core) | Framework runtime, agents, commands |

When you install OpenCode, the script pulls templates from this repository and links them with the core framework.

## Features

- **Disciplined Workflows** — Agents follow structured phases: discovery → planning → execution → verification
- **Test-Commit-Revert (TCR)** — Built-in TDD discipline for all code changes
- **Evidence-Based** — Every claim cites specific sources
- **Configurable** — Customize agents, commands, and style guidelines

## Documentation

- [User Guide](docs/user-guide.md) — Getting started and usage
- [Developer Guide](docs/develop.md) — Contributing and development
- [Deployment](docs/deploy.md) — Installation modes and hosting
- [Updating](docs/updating.md) — Keeping your installation up-to-date

## License

MIT License - see [LICENSE](LICENSE) file for details.
