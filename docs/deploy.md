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
- Extract the core `.gemini/` framework and configuration files.
- Create the standard project structure (`journal/`, `plans/`, `research/`, `drafts/`).
- Initialize baseline files (`README.md`, `CHANGELOG.md`, `TASKS.md`, `makefile`).
- Perform an initial "feat" commit.

### 2. Existing Project (Integration)
If run inside an existing project, the script will:
- **Validate:** Ensure you have a clean Git working tree.
- **Analyze:** Identify which framework files are missing or need updating.
- **Confirm:** Present a summary of all proposed changes and wait for your approval.
- **Integrate:** Add the `.gemini/` directory and core Markdown files without deleting your existing content.
- **Commit:** Create a descriptive "feat" or "chore" commit with the changes.

## 🛠️ Prerequisites

To ensure full functionality, your environment should have:
- **Git:** Required for state management and change detection hooks.
- **Node.js:** Necessary for running the `gemini` CLI.
- **Python 3.10+:** Required for executing the project's automation hooks (`.gemini/hooks/`).
- **Make:** Used for project validation and health checks.

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
