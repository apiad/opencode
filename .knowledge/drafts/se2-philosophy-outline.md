---
title: The Philosophy of Software Engineering 2.0
subtitle: Outline with Talking Points
status: draft
---

# Part I: The Philosophy of Software Engineering 2.0

## 1. Introduction: The Paradigm Shift

### The Context Saturation Problem
- **Talking point:** No matter how large the context window (1M tokens, 10M tokens), we will eventually saturate it
- **Talking point:** LLMs don't forget—they *drift*. They reinterpret based on lossy, blurry context
- **Talking point:** Symptoms: 95% done, but the last 5% requires arguing with the LLM to get it right
- **Talking point:** The real problem isn't memory—it's *meaning*. Models lose track of what's important

### Why Traditional SE Isn't Enough
- **Talking point:** SE1.0 principles (DRY, YAGNI, SOLID) assume human readers
- **Talking point:** These principles optimize for human comprehension, not AI comprehension
- **Talking point:** New principles needed that work for both humans and AI
- **Talking point:** The shift: from "write code for humans" to "design systems for intelligibility" (bidirectional)

### Thesis: Agent-as-Collaborator
- **Talking point:** AI is not a tool to be wielded—it's a collaborator to be organized
- **Talking point:** The relationship changes: from human-drives-AI to human-and-AI-drive-together
- **Talking point:** This requires rethinking processes, not just prompts
- **Talking point:** SE2.0 = SE1.0 principles extended to include AI as a first-class participant

---

## 2. Good AI Users Are Good Managers

### The Parallel to People Management
- **Talking point:** All the science of people management applies to AI management
- **Talking point:** Clear roles and responsibilities, explicit documentation, don't assume—ask
- **Talking point:** The same skills that make a good manager make a good AI orchestrator
- **Talking point:** Example: You don't micromanage good employees; you don't micromanage well-designed AI workflows

### SE1.0: Processes for People
- **Talking point:** SE1.0's insight: the most critical aspect of software is people
- **Talking point:** Processes exist to help people collaborate effectively
- **Talking point:** Code review, standups, planning poker—all designed for human cognition and communication
- **Talking point:** These processes worked because they accounted for human limitations (memory, attention, context switching)

### SE2.0: Processes for AI-as-Collaborator
- **Talking point:** AI has different limitations: context drift, hallucination, inability to recover gracefully from errors
- **Talking point:** AI has different strengths: parallel processing, perfect memory (when designed right), tireless execution
- **Talking point:** SE2.0 extends SE1.0's insight: make processes work for AI *in addition to* people
- **Talking point:** The goal: create systems where human + AI together are more effective than either alone

---

## 3. Principle One: Make Important Things Explicit

### Context Engineering
- **Talking point:** There are two kinds of context: what you put in, and what the model retains
- **Talking point:** The art: don't pollute context with noise, but re-inject what's relevant
- **Talking point:** This is a tradeoff, not a solution—and being conscious of it is the first step
- **Talking point:** Example: In a long project, the model forgets *why* a decision was made months ago

### Files as Long-Term Memory
- **Talking point:** Important decisions should be committed to writing before acted upon
- **Talking point:** Plans in markdown files = physical source of truth
- **Talking point:** Research summaries stored in real-time prevent re-research
- **Talking point:** The journal pattern: chronological record of decisions for future reference
- **Talking point:** These files serve both human and AI—shared understanding

### The Cost of Implicit Knowledge
- **Talking point:** "It should be obvious from the code" fails when context is saturated
- **Talking point:** Explicit documentation isn't just for humans—it's for AI continuity
- **Talking point:** The cost of implicit: model invents plausible but wrong explanations
- **Talking point:** Example: Why did we use library X over library Y? If it's not documented, the AI will guess

---

## 4. Principle Two: Resist the Urge to Guess

### Explicit Commands Over Implicit Skills
- **Talking point:** Implicit skills (auto-activated based on context) are powerful but uncontrollable
- **Talking point:** Explicit commands: `/plan`, `/research`, `/build`—you invoke them, you control them
- **Talking point:** Example: Instead of hoping the model knows to make a plan, explicitly invoke `/plan`
- **Talking point:** The tradeoff: explicit is more verbose, but more controllable

### Agents Should Ask, Not Assume
- **Talking point:** A good collaborator asks when uncertain—this applies to AI too
- **Talking point:** Design systems where asking is cheap and rewarded, not penalized
- **Talking point:** Example: A model that asks "should I research this library's API?" is more trustworthy than one that guesses
- **Talking point:** The failure mode: models that seem confident but are wrong (hallucination)

### Planning Before Execution
- **Talking point:** The `/plan` cycle: understand → plan → execute
- **Talking point:** Plans should be physical files, not mental states
- **Talking point:** Plans serve as contracts between human intent and AI execution
- **Talking point:** Example: "Read the plan, follow the plan, update the plan if needed"

---

## 5. Principle Three: Delegate, Delegate, Delegate

### Context Isolation
- **Talking point:** The key insight: subagents have *private* context that doesn't pollute the main session
- **Talking point:** Example: A 30-minute research loop with hundreds of web pages returns only a summary
- **Talking point:** This enables long-running tasks without context exhaustion
- **Talking point:** The cost: you only get back what the subagent summarizes—but that's usually enough

### Specialists and Subagents
- **Talking point:** Different tasks need different thinking styles
- **Talking point:** Subagents can be specialized: researcher, planner, writer, reviewer
- **Talking point:** Each subagent has a clear role and boundary—don't overlap contexts unnecessarily
- **Talking point:** Example: The researcher scours the web; returns synthesized findings. The main agent builds on them.

### Preserving Reasoning Without Pollution
- **Talking point:** Internal reasoning should be kept private, summarized results shared
- **Talking point:** This is the opposite of "think step by step" prompting—it's "think privately, report cleanly"
- **Talking point:** The agent shouldn't have to remember *how* the research was done, only *what* was found
- **Talking point:** This principle enables scaling: 10 subagents working in parallel, one main agent synthesizing

---

## 6. Tools That Enable Agency

### Instructions, Not Data
- **Talking point:** Traditional tools return data: "Here's the result"
- **Talking point:** Agent-friendly tools return instructions: "Here's the result, and here's what to do next"
- **Talking point:** Example pattern: `.explain()` — generates exact command strings with hydrated arguments
- **Talking point:** The shift: from "return a value" to "return a next step"

### Self-Discoverable Interfaces
- **Talking point:** Tools should be explorable without documentation
- **Talking point:** Example: `--tour` mode that walks through all commands and their possible next steps
- **Talking point:** Agents can discover capabilities at runtime, not just at design time
- **Talking point:** This enables agents to learn new tools without human intervention

### Explicit Interfaces (No Implicits)
- **Talking point:** CLI tools for agents should have no implicit defaults, no positional arguments—all explicit
- **Talking point:** One way to call a tool: `tool.py --flag value` is the only pattern, always
- **Talking point:** Why: agents can't guess defaults or remember argument order; they need exact invocations
- **Talking point:** Example: `--name "value"` instead of positional `"value"`, `--save` flag instead of implicit behavior
- **Talking point:** Consistency enables predictability: if every tool follows the same interface pattern, agents can generalize

### Enforced Next Steps (Design Principle)
- **Talking point:** Every command should return `m.ok` or `m.fail` with a `next=` parameter specifying what to do next
- **Talking point:** The principle: tools should never leave agents wondering "what now?"
- **Talking point:** This isn't just convention—it should be enforced by the tool framework
- **Talking point:** Example: `m.fail("Preview mode", next="Run with --save to apply")` or `m.ok("Created", next="Run --deploy to publish")`
- **Talking point:** The agent never invents next steps—the tool provides them, always

### Descriptive Failures
- **Talking point:** Silent failures are the enemy of agentic workflows
- **Talking point:** Example: `m.fail("Docker not installed")` tells the agent exactly what went wrong
- **Talking point:** Failure modes should be documented in the tool itself, not just the docs
- **Talking point:** The goal: when something fails, the agent knows exactly why and what to do

### The Two-Phase Pattern
- **Talking point:** Preview → Confirm → Execute
- **Talking point:** Example: "Preview mode. Run with --save to apply"
- **Talking point:** This pattern enables safety without friction—human-in-the-loop when it matters
- **Talking point:** Agents can explore and preview without breaking things

---

## 7. Meta-Tooling: Agents Creating Tools

### The Feedback Loop
- **Talking point:** Agents that use tools can improve tools
- **Talking point:** The cycle: agent uses tool → identifies friction → builds better tool → uses it
- **Talking point:** This is the key to self-improving systems
- **Talking point:** Example: An agent that notices repetitive workflows can create a new command

### Tools That Help Agents Build Tools
- **Talking point:** Meta-tools: tools that help agents create other tools
- **Talking point:** Example: A scaffolding command that generates boilerplate for new commands
- **Talking point:** The agent doesn't need to know everything—it needs to know how to delegate tool creation
- **Talking point:** This extends the "delegate, delegate, delegate" principle to tooling itself
- **Talking point:** Implementation detail: MicroCLI enforces `m.ok`/`m.fail` with `next=` via AST parsing at decorator time
- **Talking point:** The framework is a meta-tool that enforces tool quality—developers can't forget to return next steps

### Self-Improving Systems
- **Talking point:** The long-term vision: systems that evolve based on usage patterns
- **Talking point:** Agents identify inefficiencies and create solutions
- **Talking point:** This requires tools that are designed for modification, not just use
- **Talking point:** The open question: how much autonomy to give agents in tool creation?

---

## 8. The Human Touch

### What AI Automates (The 80%)
- **Talking point:** AI handles the first 80%: compilation, research synthesis, draft generation
- **Talking point:** This 80% is valuable precisely because it's repetitive and time-consuming
- **Talking point:** AI is good at: gathering, organizing, drafting, iterating fast
- **Talking point:** Example: Research that would take a day can be synthesized in minutes

### What Remains Irreducibly Human (The 20%)
- **Talking point:** The final 20%: taste, judgment, personal voice, ethical reasoning
- **Talking point:** AI drafts are "AI-ish"—they lack the human fingerprint that makes work original
- **Talking point:** The 20% is where the real work happens: polishing, questioning, reimagining
- **Talking point:** Example: "This article is probably 80% different from what the AI gave me"

### The Collaboration That Works
- **Talking point:** The best results come from human + AI, not either alone
- **Talking point:** AI amplifies human capability; it doesn't replace human judgment
- **Talking point:** The key: knowing when to use AI and when to override it
- **Talking point:** SE2.0 isn't about replacing human engineers—it's about making them more effective

### The Principles Endure
- **Talking point:** These principles work for people too, not just AI
- **Talking point:** SE2.0 extends SE1.0—it doesn't replace it
- **Talking point:** The future: agents creating agents, humans orchestrating teams of agents
- **Talking point:** The constants: clarity, intentionality, good judgment

---

## Summary: The Principles of SE2.0

### Core Three Principles
1. **Make important things explicit** — Context engineering, files as memory, no implicit knowledge
2. **Resist the urge to guess** — Explicit commands, agents should ask, plan before execute
3. **Delegate, delegate, delegate** — Context isolation, specialists, preserve reasoning

### Tool Design Principles
4. **Design for agency** — Instructions > data, self-discoverable, explicit interfaces, no implicits
5. **Enforced next steps** — Every command returns `m.ok`/`m.fail` with `next=`; framework enforces this
6. **Enable self-improvement** — Meta-tooling, agents creating tools, self-improving systems

### The Human Principle
6. **Human in the loop** — AI amplifies, human judges; the 80/20 split
