# User Guide: The Architect in the Machine

Welcome to the **Gemini CLI Opinionated Framework**. This guide is based on the original design philosophy ("The Architect in the Machine") and explains how to use the framework to achieve a high-velocity, AI-assisted development workflow.

The framework is not just a set of scripts; it is a principled system designed to take you from ideation to execution at the fastest responsible speed, without sacrificing safety or maintainability.

---

## 🧠 Principles of Effective AI-Assisted Work

The most pressing limitation of modern LLMs is context saturation. When you work on a single project for a long time, the model can lose track of important details, leading to hallucinations or drift.

This framework solves this problem by enforcing three core principles:

1.  **The important things should be made explicit:** We keep track of everything important in Markdown files. Ideas are committed to `plans/`, research is summarized in `research/`, and all changes are logged in the `journal/`. This physical "long-term memory" prevents the agent from forgetting context.
2.  **Resist the urge to guess:** We favor explicit commands over implicit actions. If you want the model to make a plan, you use the `/plan` command, which invokes a carefully crafted workflow rather than relying on the agent's default behavior.
3.  **Delegate, delegate, delegate:** We use specialized sub-agents (`planner`, `researcher`, `writer`, `reviewer`). These agents run complex, multi-step tasks in private contexts, preventing their internal reasoning (e.g., browsing 20 web pages) from polluting the main session's context window.

---

## 🔍 The Discovery & Strategy Workflow

The most critical phase of any project occurs before you write a single line of code. This framework moves away from impulsive execution toward a deliberate, architected approach.

### `/debug`

Your primary tool for forensic, scientific investigation.

- **How it works:** When a bug is detected, the `/debug` command implements a principled approach to problem-solving. It moves through four distinct phases: Context Analysis, Hypothesis Formulation, Isolated Testing on a temporary branch (`debug/hyp-*`), and finally a Synthesis of the findings into a **Root Cause Analysis (RCA)** report.
- **Why it works:** It forces the agent to identify the root cause *before* attempting a fix, preventing "guess-and-check" coding that can lead to regressions.

### `/plan`

Your tool for internal strategy and architectural design.

- **How it works:** The `planner` subagent conducts a thorough analysis of your codebase and journal. After clarifying the goal with you interactively, it produces a comprehensive Markdown plan in the `plans/` directory.
- **Crucial Rule:** The `/plan` command *never* executes the code. It maps the territory and provides a step-by-step execution roadmap for you to approve first.

### `/learn`

Your tool for mastering new technologies and codifying them into project skills.

- **How it works:** Implements a "Grounded Learning" philosophy through a 4-phase lifecycle:
    1.  **Environment Audit:** Automatically detects if the library is already installed or has local integration points.
    2.  **Strategic Mapping:** Researches the topic and defines 3-5 granular Learning Objectives (the "Learning Map"). **Requires user approval via `ask_user`.**
    3.  **Grounded Execution:** The specialized `learner` sub-agent performs real-world experiments (writing and running scripts) to verify "gotchas," performance, and idiomatic patterns.
    4.  **Skill Codification:** Consolidates all findings into a permanent project skill in `.gemini/skills/<name>/`, including a mandatory `SKILL.md` file and reference documents.
- **Why it works:** It transforms ephemeral research into a permanent, machine-readable knowledge base that future agents can autonomously activate.

---

## 💻 The Software Development Workflow

Once you have a solid strategy in `plans/`, you can move into execution. These commands eliminate the friction of context-switching between your IDE and terminal.

### `/issues`

Your gateway to GitHub.

- **How it works:** Interfaces with the GitHub CLI to analyze open issues and recommend what to tackle next based on strategic impact.


### `/learn`

Your tool for mastering new technologies and codifying them into project skills.

- **How it works:** Implements a "Grounded Learning" philosophy through a 4-phase lifecycle:
    1.  **Environment Audit:** Automatically detects if the library is already installed or has local integration points.
    2.  **Strategic Mapping:** Researches the topic and defines 3-5 granular Learning Objectives (the "Learning Map"). **Requires user approval via `ask_user`.**
    3.  **Grounded Execution:** The specialized `learner` sub-agent performs real-world experiments (writing and running scripts) to verify "gotchas," performance, and idiomatic patterns.
    4.  **Skill Codification:** Consolidates all findings into a permanent project skill in `.gemini/skills/<name>/`, including a mandatory `SKILL.md` file and reference documents.
- **Why it works:** It transforms ephemeral research into a permanent, machine-readable knowledge base that future agents can autonomously activate.

### `/task`

Your roadmap manager.

- **How it works:** Manages a living `TASKS.md` document. Use it to `create` new tasks, `work` on existing ones, `report` on priorities, or `update` statuses.

### `/commit`

Brings order to your version history.

- **How it works:** Instead of monolithic "WIP" commits, this command analyzes your `git diff` and logically groups modifications into cohesive units. It proposes a series of atomic, Conventional Commits (e.g., separating a feature update from a documentation tweak) for your approval.

### `/release`

Automates the deployment process.

- **How it works:** Verifies workspace integrity (clean git tree, passing tests via `make`), analyzes commit history to propose the next version bump, drafts a `CHANGELOG.md` entry, and publishes the final tag to GitHub.

## 🔄 A Full Feature Development Walkthrough

A complete, principled development cycle follows the **Research -> Plan -> Execute** lifecycle.

### **Step 1: Research with `/research`**

You are integrating a new authentication library. You start by researching the technical requirements.

- The `researcher` subagent gathers documentation and synthesizes it into `research/auth-library-deep-dive.md`.

### **Step 2: Strategy with `/plan`**

Once you understand the requirements, you trigger the `/plan` command.

- The `planner` subagent analyzes the codebase and generates `plans/implement-auth.md`, mapping out the specific architectural changes and testing strategy.

### **Step 3: Execute with `/task work`**

The approved plan is linked to a task. You trigger the execution:

- **Pre-flight:** The agent verifies the tree is clean on `main`.
- **Isolation:** A `feature/auth-integration` branch is created.
- **Loop (Red-Green-Verify):**
    1.  Agent writes a failing `test_auth_logic.py` based on the plan.
    2.  Agent implements the minimal logic to pass.
    3.  Agent runs `make test`. If successful, the step is committed.
    4.  If it fails, the agent tries **one quick fix**. If it fails again, the change is **automatically reverted**, preserving the last stable state.
    5.  The loop repeats for every granular step defined in the plan.

### **Step 4: Review & Integrate**

After all steps pass, the agent presents the final work. Upon your approval, it merges back to `main` and cleans up the feature branch.

### Step 5: Document & Release with `/docs` & `/release`

Finally, use `/docs` to update the technical documentation and `/release` to publish the new version.

## 🔍 Walkthrough: Solving a Bug with `/debug`

When a bug is detected, the `/debug` command ensures a scientific resolution:

1.  **Analyze Context:** The agent gathers all relevant logs and context.
2.  **Formulate Hypothesis:** The agent proposes a root cause hypothesis (e.g., "The auth token is not being correctly passed to the header").
3.  **Isolate & Test:** The agent creates a temporary branch `debug/hyp-auth-token`. It implements a minimal reproduction script or logging.
4.  **RCA Synthesis:** Once confirmed, the agent generates a **Root Cause Analysis (RCA)** report. This report is used as the basis for the subsequent `/task work` to implement the fix on a feature branch.

## ✍️ Maintaining your Journal

The framework's most powerful feature is its automated audit trail. This is enforced by a **timestamp-based pre-commit hook** that ensures your code never gets ahead of your documentation.

### The Rule of Temporal Consistency

Every code change must be documented in `journal/YYYY-MM-DD.md`. If you modify a file at 10:00 AM, you must have a journal entry with a timestamp of 10:00 AM or later before you can commit.

### Using the Journal Tool

To simplify this, the framework includes a dedicated script. Always use it instead of manual editing:

```bash
python3 .gemini/scripts/journal.py "Brief description of your work"
```

This tool automatically:
1.  Detects the current date and finds/creates the correct journal file.
2.  Generates a precise ISO timestamp.
3.  Appends the entry in the standard `[timestamp] - description` format.

By following this discipline, you ensure that the AI agent always has an up-to-date "long-term memory" to draw from in future sessions.

---

## ✍️ The Content Creation Workflow

Beyond code, this framework excels at generating high-quality technical content through a principled, multi-stage pipeline.

### `/draft`

Your primary tool for long-form technical writing.

- **How it works:** Instead of generating a single large blob of text, the `/draft` command follows a strict 6-phase workflow: Context Gathering (from `research/` or `plans/`), Title & Metadata Selection, Outline Creation (aligned with the Style Guide), Initialization of the file, Section-by-Section Drafting (using the `writer` subagent), and finally, a Conclusion with next steps.
- **Why it works:** It forces structural integrity and prevents the "AI-ish" monotone by building the document incrementally based on project-specific research.

### `/review`

Your tool for deep, multi-phase editorial audits.

- **How it works:** Replaces the legacy `/revise` command with a non-destructive, evidence-based reporting workflow. It uses the `reviewer` subagent to audit a file in three distinct phases:
    1.  **Structural Audit:** Narrative arc and header hierarchy.
    2.  **Substance Audit:** Concreteness and technical depth.
    3.  **Linguistic Audit:** Removing "AI-isms" and polishing the prose.
- **Why it works:** It produces a sidecar `<filename>.review.md` report instead of modifying the original file, allowing you to choose which suggestions to apply during the next `/draft` or `/task work` iteration.

---

## ⚙️ Background Tasks & Maintenance


The real magic of AI-assisted development is what happens when you're not looking or when dealing with technical debt.

### `/cron`

Your background automation layer.

- **How it works:** Uses the `cron.toml` file to define scheduled tasks via systemd user timers. You can schedule natural language prompts (e.g., "Scour the web for new developments in X") to run overnight, ensuring your knowledge base is fresh by morning.

### `/maintenance`

Your defense against context rot.

- **How it works:** Performs a comprehensive, read-only audit of the codebase to identify technical debt, outdated implementations, or documentation gaps using the `codebase_investigator`. It generates a "Maintenance Report Card" in the `research/` directory.
- **Why it works:** It separates the audit from the implementation, ensuring the codebase remains a clean environment. After an audit, use the `/plan` command to safely execute the suggested improvements.

---

*This framework is not a "one-size-fits-all" solution; it is a starting point. Every command and subagent is a living document meant to be tweaked to suit your unique mental model.*
