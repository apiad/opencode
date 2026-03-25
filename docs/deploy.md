# Installation & Setup

Getting the **Gemini CLI Opinionated Framework** up and running is an automated, interactive process. Whether you're starting a new project or integrating into an existing one, the `install.sh` script is your primary tool.

## 🚀 The Unified Installer

The fastest way to install or update the framework is to run the following command:

```bash
curl -fsSL https://apiad.github.io/starter/install.sh | bash
```

### 1. New Project (Scaffolding)

Running `install.sh` in an empty directory will:

- Initialize a fresh Git repository.
- Extract the core `.opencode/` framework and configuration files.
- Create the standard project structure (`journal/`, `plans/`, `research/`, `drafts/`).
- Initialize baseline files (`README.md`, `CHANGELOG.md`, `TASKS.md`, `makefile`).
- Perform an initial "feat" commit.

### 2. Existing Project (Integration & Updates)

If run inside an existing project, the script performs a **Surgical Update**:

- **Validate:** Ensure a clean Git working tree to prevent data loss.
- **Surgical Sync:** Updates core framework components (`commands/`, `agents/`, `tools/`) individually.
- **Protection:** Explicitly preserves user configurations in **Protected Files**:
    - `opencode.json`
    - `.opencode/style-guide.md`
- **Intelligent GEMINI.md Merge:** Preserves your custom content in the `## Project Notes` section of `GEMINI.md` while updating the core mandates above it.
- **Confirm:** Presents a detailed summary of which files will be **created**, **updated**, or **protected** and waits for your approval.
- **Integrate:** Adds missing directory structures (`journal/`, `plans/`, etc.) if they don't exist.
- **Commit:** Automatically creates a descriptive `chore` commit marking the update.

## 🛠️ Prerequisites & Setup

To ensure full functionality, your environment should have:

- **Git:** Required for state management and change detection hooks.
- **Node.js:** Necessary for running the `gemini` CLI.
- **Python 3.12+:** Required for executing the project's automation scripts in `.opencode/tools/`.
- **uv:** The required Python package and project manager.
- **Make:** Used for project validation and health checks (runs `uv run pytest`).

### Installing Git Hooks

After installation, you **must** link the framework's hooks to your git repository:

```bash
make install-hooks
```

This target creates a symbolic link from `.opencode/tools/git-precommit.py` to `.git/hooks/pre-commit`, enabling the automated journal and validation checks.

## 🚢 Getting Started

Once the installation is complete, follow these steps to orient yourself:

### 1. Run Onboarding

Execute the `/onboard` command to get a high-signal overview of the repository's architecture, standards, and current roadmap.

```bash
gemini /onboard
```

### 2. Initialize the Roadmap

Check the current `TASKS.md` file and use the `/task` command to define your project's initial goals.

### 3. Start a New Feature

For your first feature, follow the standard workflow:

- **Research:** `gemini /research [topic]`
- **Plan:** `gemini /plan` (follow the interactive prompts)
- **Implement:** Begin coding once the plan is saved in `plans/`.

---

*Next: See [Architecture & Systems](design.md) to understand how it works.*
