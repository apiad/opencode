# User Guide: The Architect in the Machine

Welcome to the **Gemini CLI Opinionated Framework**. This guide is based on the original design philosophy ("The Architect in the Machine") and explains how to use the framework to achieve a high-velocity, AI-assisted development workflow.

The framework is not just a set of scripts; it is a principled system designed to take you from ideation to execution at the fastest responsible speed, without sacrificing safety or maintainability.

---

## 🧠 Principles of Effective AI-Assisted Work

The most pressing limitation of modern LLMs is context saturation. When you work on a single project for a long time, the model can lose track of important details, leading to hallucinations or drift. 

This framework solves this problem by enforcing three core principles:

1.  **The important things should be made explicit:** We keep track of everything important in Markdown files. Ideas are committed to `plans/`, research is summarized in `research/`, and all changes are logged in the `journal/`. This physical "long-term memory" prevents the agent from forgetting context.
2.  **Resist the urge to guess:** We favor explicit commands over implicit actions. If you want the model to make a plan, you use the `/plan` command, which invokes a carefully crafted workflow rather than relying on the agent's default behavior.
3.  **Delegate, delegate, delegate:** We use specialized sub-agents (`planner`, `researcher`, `reporter`, `editor`). These agents run complex, multi-step tasks in private contexts, preventing their internal reasoning (e.g., browsing 20 web pages) from polluting the main session's context window.

---

## 🔍 The Discovery & Strategy Workflow

The most critical phase of any project occurs before you write a single line of code. This framework moves away from impulsive execution toward a deliberate, architected approach.

### `/research`
Your primary tool for gathering external knowledge.
- **How it works:** When triggered, the `researcher` subagent scours the web for technical documentation, APIs, or case studies. It synthesizes this data into granular summaries saved in the `research/` directory.
- **When to use:** Use this when you need to understand a new library, a technical specification, or gather data for an article.

### `/plan`
Your tool for internal strategy and architectural design.
- **How it works:** The `planner` subagent conducts a thorough analysis of your codebase and journal. After clarifying the goal with you interactively, it produces a comprehensive Markdown plan in the `plans/` directory.
- **Crucial Rule:** The `/plan` command *never* executes the code. It maps the territory and provides a step-by-step execution roadmap for you to approve first.

---

## 💻 The Software Development Workflow

Once you have a solid strategy in `plans/`, you can move into execution. These commands eliminate the friction of context-switching between your IDE and terminal.

### `/issues`
Your gateway to GitHub.
- **How it works:** Interfaces with the GitHub CLI to analyze open issues and recommend what to tackle next based on strategic impact.

### `/task`
Your roadmap manager.
- **How it works:** Manages a living `TASKS.md` document. Use it to `create` new tasks, `work` on existing ones, or `report` on the project's current status.

### `/commit`
Brings order to your version history.
- **How it works:** Instead of monolithic "WIP" commits, this command analyzes your `git diff` and logically groups modifications into cohesive units. It proposes a series of atomic, Conventional Commits (e.g., separating a feature update from a documentation tweak) for your approval.

### `/release`
Automates the deployment process.
- **How it works:** Verifies workspace integrity (clean git tree, passing tests via `make`), analyzes commit history to propose the next version bump, drafts a `CHANGELOG.md` entry, and publishes the final tag to GitHub.

---

## ✍️ The Content Creation Workflow

The framework is uniquely suited for writing high-quality documentation and long-form articles, built on the same cognitive foundation as the development path.

### `/draft`
Turns research into structured prose.
- **How it works:** Performs a deep scan of `research/` and `plans/` to identify key themes. It collaboratively generates a Markdown outline. Once approved, the `reporter` subagent expands the outline section-by-section, drawing directly from your validated research to ensure evidence-based writing.

### `/revise`
Provides professional editing and polish.
- **How it works:** Uses the `editor` subagent to perform a structural and linguistic audit based on your `.gemini/style-guide.md`. It identifies logical gaps and awkward phrasing, presenting specific improvements for you to review interactively.

---

## ⚙️ Background Tasks & Maintenance

The real magic of AI-assisted development is what happens when you're not looking or when dealing with technical debt.

### `/cron`
Your background automation layer.
- **How it works:** Uses the `cron.toml` file to define scheduled tasks via systemd user timers. You can schedule natural language prompts (e.g., "Scour the web for new developments in X") to run overnight, ensuring your knowledge base is fresh by morning.

### `/maintenance`
Your defense against context rot.
- **How it works:** Performs a comprehensive audit of the codebase to identify technical debt, outdated implementations, or deviations between code and documentation. It presents a detailed refactoring plan for your approval before making any changes, ensuring the repository remains a clean environment for the AI to operate within.

---

*This framework is not a "one-size-fits-all" solution; it is a starting point. Every command and subagent is a living document meant to be tweaked to suit your unique mental model.*
