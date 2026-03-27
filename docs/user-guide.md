# User Guide

Welcome to the **OpenCode Framework**. This guide explains how to use the framework to achieve a high-velocity, AI-assisted development workflow.

The framework is not just a set of scripts; it is a principled system designed to take you from ideation to execution at the fastest responsible speed, without sacrificing safety or maintainability.

---

## 🧠 Principles of Effective AI-Assisted Work

The most pressing limitation of modern LLMs is context saturation. When you work on a single project for a long time, the model can lose track of important details, leading to hallucinations or drift.

This framework solves this problem by enforcing core principles:

1.  **The important things should be made explicit:** We keep track of everything important in Markdown files. Ideas are committed to `.knowledge/plans/`, research is summarized in `.knowledge/notes/`, and all changes are logged in `.knowledge/log/`. This physical "long-term memory" prevents the agent from forgetting context.
2.  **Resist the urge to guess:** We favor explicit commands over implicit actions. If you want the model to make a plan, you use the `/plan` command, which invokes a carefully crafted workflow rather than relying on the agent's default behavior.
3.  **Evidence-based:** Every claim cites specific sources and findings are actionable.

---

## 🔍 Phase 1: Discovery & Audit

The most critical phase of any project occurs before you write a single line of code. This phase uses read-only commands to gather information safely.

### `/research`

Your tool for deep domain exploration.
- **How it works:** Gathers documentation and synthesizes it into `.knowledge/notes/` reports.

### `/debug`

Your primary tool for forensic, scientific investigation.

- **How it works:** When a bug is detected, the `/debug` command implements a principled approach to problem-solving using the specialized `debugger` subagent. It moves through four distinct phases: Context Analysis, Hypothesis Formulation, Isolated Testing on a temporary branch (`debug/hyp-*`), and finally a Synthesis of the findings into a **Root Cause Analysis (RCA)** report.
- **Why it works:** It forces the agent to identify the root cause *before* attempting a fix, preventing "guess-and-check" coding that can lead to regressions.

---

## 🌉 Phase 2: Strategy & Planning

Once you have gathered discovery artifacts, you must synthesize them into an actionable strategy.

### `/plan`

Your tool for internal strategy and architectural design.

- **How it works:** The `plan` agent conducts a thorough analysis of your codebase. After clarifying the goal with you interactively, it produces a comprehensive Markdown plan in the `.knowledge/plans/` directory.
- **Crucial Rule:** The `/plan` command *never* executes the code. It maps the territory and provides a step-by-step execution roadmap for you to approve first.

### `/onboard`

Your tool for rapid project orientation.

- **How it works:** Provides a high-signal overview of the repository's architecture, standards, and current state. 
- **Why it works:** It ensures that you (and the agent) are always aligned with the project's unique conventions before starting a session.

---

## 🚀 Phase 3: Execution & Implementation

Once you have a solid strategy in `.knowledge/plans/`, you can move into execution. These commands eliminate the friction of context-switching between your IDE and terminal.

### `/issues`

Your gateway to GitHub.

- **How it works:** Interfaces with the GitHub CLI to analyze open issues and recommend what to tackle next based on strategic impact.


### `/scaffold`

Your tool for project initialization.

- **How it works:** Scaffolds new components or entire projects using modern, standard tooling (TS, Python, Rust, etc.) and integrates the framework's standards and `makefile` from the start.

### `/todo`

Your task management tool.

- **How it works:** Manages project tasks via the `todowrite` tool. Use it to track work items, set priorities, and mark completion.
- **Why it works:** Keeps a structured task list visible to both user and agent, ensuring nothing falls through the cracks.

### `/commit`
...
## 🌲 Agent Architecture

The framework uses **OpenCode** with specialized agents that handle different cognitive workloads:

### Primary Agents (Modes)
- **`analyze`**: Research, investigation, and audits
- **`plan`**: Strategy and architectural design
- **`build`**: Implementation with TCR discipline
- **`release`**: Publishing and versioning

### Subagents
- **`investigator`**: Codebase analysis
- **`scout`**: Web research
- **`tester`**: Hypothesis validation
- **`drafter`**: Content creation
- **`critic`**: Prose review

## 🔄 A Full Feature Development Walkthrough


- **How it works:** Instead of monolithic "WIP" commits, this command analyzes your `git diff` and logically groups modifications into cohesive units. It proposes a series of atomic, Conventional Commits (e.g., separating a feature update from a documentation tweak) for your approval.

### `/release`

Automates the deployment process.

- **How it works:** Verifies workspace integrity (clean git tree, passing tests via `make`), analyzes commit history to propose the next version bump, drafts a `CHANGELOG.md` entry, and publishes the final tag to GitHub.

## 🔄 A Full Feature Development Walkthrough

A complete, principled development cycle follows the **Discovery -> Plan -> Execute** lifecycle.

### **Step 1: Discovery with `/research` or `/audit`**

Before acting, you must gather context. For example, if you are integrating a new authentication library, you start by researching the technical requirements.

- Use `/research` to gather documentation and synthesize it into `.knowledge/notes/auth-library-deep-dive.md`.
- Use `/audit` to audit the codebase or existing documents.

### **Step 2: Strategy with `/plan`**

Once you understand the requirements, you trigger the `/plan` command.

- The `plan` agent analyzes the codebase and generates `.knowledge/plans/implement-auth.md`, mapping out the specific architectural changes and testing strategy.

### **Step 3: Execute with `/build`**

The approved plan is linked to a task. You trigger the execution:

- **Pre-flight:** The agent verifies the tree is clean on `main`.
- **Isolation:** A feature branch is created.
- **Loop (Red-Green-Verify):**
    The `/build` command breaks the plan into granular steps:
    1.  Write a failing test based on the step.
    2.  Implement the minimal logic to pass.
    3.  Verify with `make test`. If successful, commit the step.
    4.  If it fails, revert the step and report the failure.
    5.  The loop repeats for every granular step defined in the plan.

### **Step 4: Review & Integrate**

After all steps pass, the agent presents the final work. Upon your approval, it merges back to `main` and cleans up the feature branch.

### Step 5: Document & Release

Finally, update the technical documentation as needed and use `/release` to publish the new version.
## 🔍 Walkthrough: Solving a Bug with `/debug`

When a bug is detected, the `/debug` command ensures a scientific resolution:

1.  **Analyze Context:** The agent gathers all relevant logs and context.
...
2.  **Formulate Hypothesis:** The agent proposes a root cause hypothesis (e.g., "The auth token is not being correctly passed to the header").
3.  **Isolate & Test:** The agent creates a temporary branch to implement a minimal reproduction script or logging.
4.  **RCA Synthesis:** Once confirmed, the agent generates a **Root Cause Analysis (RCA)** report. This report is used as the basis for the subsequent `/build` to implement the fix.

## ✍️ Maintaining your Journal

The framework's most powerful feature is its automated audit trail. This is enforced by a **timestamp-based pre-commit hook** that ensures your code never gets ahead of your documentation.

### The Rule of Temporal Consistency

Every code change should be documented in `.knowledge/log/YYYY-MM-DD.yaml`. If you modify a file at 10:00 AM, you should have a journal entry with a timestamp of 10:00 AM or later before you can commit.

### Using the Note Tool

To simplify this, use the `/note` command:

```bash
opencode /note "Brief description of your work"
```

This adds an entry to the daily journal with a precise timestamp.

---

## ✍️ The Content Creation Workflow

Beyond code, this framework excels at generating high-quality technical content through a principled, multi-stage pipeline.

### `/draft`

Your primary tool for long-form technical writing.

- **How it works:** The `/draft` command follows a structured workflow: Context Gathering (from `.knowledge/notes/` or `.knowledge/plans/`), Title & Metadata Selection, Outline Creation (aligned with the Style Guide), Initialization of the file, Section-by-Section Drafting, and finally, a Conclusion with next steps.
- **Why it works:** It forces structural integrity and prevents the "AI-ish" monotone by building the document incrementally based on project-specific research.

### `/fix`

Your tool for bug fixes with regression prevention.

- **How it works:** Uses `/debug` to find root cause, then applies TCR discipline to implement the fix with a regression test.
- **Why it works:** It separates investigation from implementation, ensuring fixes are grounded in understanding.

---

---

*This framework is not a "one-size-fits-all" solution; it is a starting point. Every command and subagent is a living document meant to be tweaked to suit your unique mental model.*
