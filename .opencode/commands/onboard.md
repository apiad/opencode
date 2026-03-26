---
description: Summarize architecture, standards, and state to onboard a new developer.
agent: query
---

Senior engineer onboarding a new developer. Provide a concise, high-signal orientation using direct observation.

**Phase 1: Direct Discovery**
1. **Read Core Docs:** Read `README.md`, `todo.yaml`, and the 2 most recent entries in `journal/`.
2. **Map Structure:** List files the root and key directories (e.g., `src/`) to understand the layout.
3. **Explore Context:**
   - If a `docs/` directory exists, read its contents to understand deeper project context.
   - If no `docs/` exists, identify and read 2-3 key source files (e.g., in `src/` or root) to understand implementation patterns.
4. **Identify Entry Points:** Quickly scan the `makefile` (if it exists) to see common commands.

**Phase 2: Lean Onboarding Report**
Produce a professional, welcoming summary:
- **Project Purpose:** What this project does (from README).
- **Architecture & Layout:** High-level mapping of directories and core technologies.
- **Workflow & Standards:** How to run, test, and commit (from README/makefile).
- **Deep Dive (if available):** Key insights from `docs/` or source code analysis.
- **Current State:** Recent activity and active tasks (from journal/todo.yaml).
- **First Steps:** 2-3 specific files or commands to start with.

Synthesize the report directly from your findings.
