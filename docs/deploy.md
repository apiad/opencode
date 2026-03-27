# Installation & Setup

Getting the **OpenCode Framework** up and running is an automated, non-interactive process. Whether you're starting a new project or integrating into an existing one, the `install.sh` script is your primary tool.

## Installation Modes

The framework supports two installation modes with different trade-offs:

### Copy Mode (Default)

The framework is downloaded and extracted without git tracking.

**Characteristics:**
- Framework files are a standalone copy
- No `.git/` directory in `.opencode/`
- Updates via re-running installer
- Each project has its own copy

**Trade-offs:**
- Pros:
  - Simple, no git knowledge required
  - Projects are independent
  - No risk of accidentally modifying framework files
- Cons:
  - Cannot rollback using git history
  - Must manually track framework updates
  - Cannot contribute to framework development

**Best for:**
- Projects that need stability
- Users unfamiliar with git submodules
- Production environments

### Link Mode (Submodule)

The framework is installed as a git submodule.

**Characteristics:**
- Framework is a git submodule linked to `opencode-core`
- Maintains `.git/` connection
- Updates via `git pull` or submodule commands
- Shares framework across projects

**Trade-offs:**
- Pros:
  - Easy updates via `git submodule update`
  - Can rollback using git history
  - Can contribute changes back to framework
- Cons:
  - More complex git workflow
  - Requires understanding of submodules
  - Framework changes affect all projects

**Best for:**
- Framework development
- Active development requiring latest features
- Users comfortable with git submodules

### When to Use Each Mode

| Scenario | Recommended Mode |
|----------|------------------|
| Production project, stability needed | Copy |
| Experimental project | Link |
| Contributing to framework | Link |
| New to git | Copy |
| Multiple projects sharing updates | Link |
| Isolated project | Copy |

### Switching Modes

To switch modes, run the installer with the desired mode:

```bash
# Copy to Link
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --link

# Link to Copy
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --copy
```

The installer runs non-interactively; use `--link` or `--copy` to specify the mode.

---

## 🚀 The Unified Installer

The fastest way to install or update the framework is to run the following command:

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
```

### 1. New Project (Scaffolding)

Running `install.sh` in an empty directory will:

- Initialize a fresh Git repository.
- Extract the core `.opencode/` framework and configuration files.
- Create the standard project structure (`.knowledge/log/`, `.knowledge/plans/`, `.knowledge/notes/`, `.knowledge/drafts/`).
- Initialize baseline files (`README.md`, `CHANGELOG.md`, `tasks.yaml`, `makefile`).
- Perform an initial "feat" commit.

### 2. Existing Project (Integration & Updates)

If run inside an existing project, the script performs a **Surgical Update**:

- **Validate:** Ensure a clean Git working tree to prevent data loss.
- **Surgical Sync:** Updates core framework components (`commands/`, `agents/`, `tools/`) individually.
- **Protection:** Explicitly preserves user configurations in **Protected Files**:
    - `opencode.json`
    - `.opencode/style-guide.md`
- **Confirm:** Presents a detailed summary of which files will be **created**, **updated**, or **protected** and waits for your approval.
- **Integrate:** Adds missing directory structures (`.knowledge/log/`, `.knowledge/plans/`, etc.) if they don't exist.
- **Commit:** Automatically creates a descriptive `chore` commit marking the update.

## 🛠️ Prerequisites & Setup

To ensure full functionality, your environment should have:

- **Git:** Required for state management and change detection hooks.
- **Node.js:** Necessary for running the `opencode` CLI.
- **Python 3.12+:** Required for executing the project's automation scripts in `.opencode/tools/`.
- **uv:** The required Python package and project manager.
- **Make:** Used for project validation and health checks (runs `uv run pytest`).

### Installing Git Hooks

After installation, you **must** link the framework's hooks to your git repository:

```bash
make install-hooks
```

This target creates a symbolic link from `.opencode/tools/pre-commit.py` to `.git/hooks/pre-commit`, enabling the automated journal and validation checks.

## 🚢 Getting Started

Once the installation is complete, follow these steps to orient yourself:

### 1. Run Onboarding

Execute the `/onboard` command to get a high-signal overview of the repository's architecture, standards, and current roadmap.

```bash
opencode /onboard
```

### 2. Initialize the Roadmap

Check the current task list and use the `/todo` command to define your project's initial goals.

### 3. Start a New Feature

For your first feature, follow the standard workflow:

- **Research:** `opencode /research [topic]`
- **Plan:** `opencode /plan` (follow the interactive prompts)
- **Implement:** Begin coding once the plan is saved in `.knowledge/plans/`.

---

*Next: See [Architecture & Systems](design.md) to understand how it works.*
