# The Architect in the Machine: How I Built a High-Velocity AI Development Workflow

I know, this is the probably the twentieth article you've read this week on "how I am using AI to automate my whole life/work/whatever". Me too. But please, give me a couple of minutes to tell why this article might be different, and thus interesting to you.

But even if you don't have two minutes to spare, please check the [repository](https://github.com/apiad/starter) where all I'm going to tell you about is implemented, ready for your taking. Clone it and play with it, then if you like it, come back and read the rationale behind it.

Done? Ok, here we go.

So yes, this is another article trying to explain to you how I use AI coding agents (specifically Gemini CLI, but the specifics don't matter) to enhance my workflows. Here are a couple of reasons why I think you might be interested---and why this article might be different to so many lookalikes out there.

First, I'm not an enthusiastic techbro who just discovered AI. If you've read this blog before, you know I'm a longtime researcher in AI---way before LLMs were a thing---and also a self-proclaimed AI anti-hypist. I'm not just overexcited about this shiny new toy. I've been using generative AI since day one for everything, and I've been telling you exactly how it sucks at almost anything important since day one. Coding has been the same until very recently. I can tell you the change in productivity is real, provided you are responsible and considerate.

Second, my approach to incorporating AI into my workflows is one, very careful and two, grounded in healthy skepticism. I know firsthand how these things fail, so my approach attempts to be very robust to hallucinations and context drift and all the plagues of even the most powerful LLMs.

Third, I have a thing for systems. What I'm going to show is not just a set of hacks or clever prompts or productivity tips. It's a principled system to go from ideation to research and planning to execution at the fastest responsible speed, without sacrificing on safety or maintainability.

And fourth, I have kind of a unique position in that I'm both heavily invested into coding as well as technical writing. I'm a college professor, so I do a lot of research, writing, and editing; but I also run a small AI startup, small enough that I get to do a large part of the coding. So my system attempts to bridge these two facets---code and prose creation---with the same unified principles of careful deliberation and planning, and robust tracking of the project evolution.

If you're curious already, let me start by exposing the overall principles behind this approach, and then we'll dive (not delve, but close) into the details.

## Principles of Effective AI-Assisted Work

By far the most pressing limitation of modern, top-tier LLMs for my line of work is context saturation. What I mean by this, is no matter how many tokens your model can fit (Gemini 3 claims to chug as much as 1 million tokens), when you work for a considerable amount of time on a single project, you will exhaust this context. And even if the context window isn't full, the model will quickly lose the capability to keep track of the important bits of context, and will start to deviate from your instructions and make up its own agenda. Not out of evilness but simple probabilities.

The way you see this problem when using Claude Code, Gemini CLI, Codex, Copilot, or anything similar is twofold. The model will either forget midtask what is was supposed to do, but it won't simply fail; it will reinterpret the task based on its faulty, lossy, blurry viewpoint given the available context and it will do something close, but not quite what you wanted. Or, the model will make faulty assumptions and forget to ask relevant questions, again behaving close but not quite exactly as you intended.

The result is always the same, you get frustrated that you achieved 95% of what you needed, but the remaining 5% is harder to fix than to just try again. And what could have been a happy working session where you get important and difficult things done quickly derails into a session of arguing with an LLM trying to convince it (him/her/pick your side) to do things the way you want.

Barring any fundamental paradigm shifts in the near future, under the assumption that LLMs will keep working as they are, the only way to fix this is to be very conscious and careful about the context---what has been dubbed context engineering---in two senses: First, do not pollute the context with unnecessary details. And second, re-inject into the context whatever is relevant for any given task, so it doesn't get forgotten.

I know, kind of contradictory, but tradeoffs are what engineering is all about. In my system, I've applied three principles to help me manage these tradeoffs effectively.

1. The important things should be made explicit.
2. Resist the urge to guess.
3. Delegate, delegate, delegate (yeah, three times).

Here's how that works. For principle one, we will keep track of everything important in markdown files in the repository. This means ideas are committed to plans in markdown files before acting on them, research is summarized and stored in real time, and everything that changes in the project is logged to a long-lived journal, so the model remembers why we made some decision months ago.

For principle two, we will favor using explicit commands that are translated into explicit prompts, instead of relying on implicitly activated skills that you have little control of. So if you want the model to make a plan, you will prompt it with "/plan lets design feature X", and the `/plan` command will invoke a carefully crafted prompt that says how plans work, where they are stored, etc.

And principle three means using sub-agents a lot. This is a Gemini CLI specific feature---but every other coding agent has a similar thing---where you can launch a complicated task as a "sub-agent"---which basically means a custom prompt---but here is the important part: All the context of that sub-agent is kept private, not shared with the main agent, so the internal reasoning the sub-agent needed to run to find 20 different sources in Google does not pollute the main context. We only receive back the summarized responses. This allows running very long tasks (my record is a 30 minutes long research loop, involving hundreds of retrieved web pages) on a single agent turn, without exhausting the context.

I use four sub-agents in different commands. The `planner` is the lead architect. It’s a read-only agent that walks through your codebase and reads everything necessary to understand architecture, design decisions, etc., given a specific task. It then produces a detailed Markdown plan in the `plans/` directory---a physical source of truth that you can review before any code is touched, and that the main agent will follow step-by-step. This separation prevents the system from "guessing" its way through your codebase.

When I need external knowledge---like a library’s latest API or a specific technical specification---the `researcher` agent takes over. It scours the web to fetch relevant documentation, which it then synthesizes into granular summaries in the `research/` directory. This raw data is then handed off to the main agent to build an executive report annotated and linked to all relevant sources, again all stored already in your repository.

And there are two more agents, specifically designed for technical writing. The `reporter` agent takes an outline, and a folder of content, and it will write section by section, a detailed account of what the outline requested.

Unlike a standard LLM that might provide a high-level summary, the `reporter` is trained to expand specific placeholders with deep, evidence-based paragraphs. It draws directly from your `research/` files and the project `journal/` to ensure every sentence is grounded in the project's actual state. Finally, the `editor` provides the final polish, auditing the draft for structural gaps and linguistic tics. It is grounded in a customizable style guide to make sure it always respects your style.

This distributed intelligence is held together by a central nervous system of context files, as per principle one. A `journal/` directory provides a chronological record of decisions and progress, acting as a long-term memory for the project. The `plans/` directory stores the strategic intent, while a `TASKS.md` file provides a high-level overview of the project's current status. This structured environment allows the subagents to maintain a high degree of situational awareness without needing to ingest the entire repository in every turn.

Now that we have the key pieces in place, you can start to see why I think this approach is powerful. It is very extensible---you can add new agents triggered by specific commands to customize any kind of workflow---and it mostly solves the main pain point of modern LLMs, which is precisely the brittleness of long contexts.

## Workflow Details

With all that, let me show you the specific commands and workflows I have currently implemented, but keep in mind what follows is but one example of the kind of powerful workflows we can start to automate.

I will divide the rest of the article into a few major areas, and explain the commands and agents that I use in each case, and a bit of the high-level instructions given to each of them.

### Discovery & Strategy

The most critical phase of any project occurs before I write a single line of code. I call this the "Discovery and Strategy" phase, powered by the `/research` and `/plan` commands. By formalizing this process, I’ve moved away from impulsive execution toward a deliberate, architected approach.

The `/research` command is my primary tool for external knowledge. When triggered, the `researcher` scours the web for technical documentation and relevant case studies, synthesizing them into granular summaries in the `research/` directory. These files become a persistent knowledge base, allowing me to reference verified facts without leaving my terminal.

Complementing this is the `/plan` command, which focuses on internal strategy. The `planner` conducts a thorough analysis of the codebase and the `journal/` to understand the system's current state. After an interactive dialogue to resolve any ambiguity, it produces a comprehensive Markdown plan in the `plans/` directory. This document maps out the technical territory and provides a step-by-step execution roadmap.

The strength of this workflow lies in the synergy between these two tools. A `/plan` operation might reveal a gap in my understanding of a specific library, prompting a targeted `/research` session. Conversely, a new research finding might shift my technical direction, leading to a refined plan.

### Software Development

Once I have a solid strategy in my `plans/` directory, I can move into execution. Let's focus now on software development. I’ve designed four core commands---`/issues`, `/task`, `/commit`, and `/release`---to eliminate the friction of context-switching between my IDE and my terminal.

The cycle starts with `/issues` and `/task`. The `/issues` command acts as an expert project lead, interfacing directly with the GitHub CLI to analyze open issues and recommend what to tackle next based on strategic impact. For roadmap tracking, the `/task` command manages a living `TASKS.md` document. It assesses the value of pending work to ensure my efforts are always aligned with the project's goals.

As I translate the plan into code, the `/commit` command brings order to my workspace. Instead of a monolithic "wip" commit that hides the logic of my changes, the system analyzes the `git diff` and logically groups modifications into cohesive units. It separates a core feature update from a documentation tweak, then proposes a series of atomic, Conventional Commits for my approval. This keeps my version history pristine and easy to navigate.

The final stage is deployment. Manual releases are fragile processes fraught with repetitive checklists: bumping versions and running tests before managing tags. The `/release` command automates this entire sequence. It verifies the workspace integrity by ensuring a clean git tree and passing tests via `make`. It then analyzes the commit history to propose the next version bump, drafts a `CHANGELOG.md` entry, and publishes the final tag to GitHub. This transforms a tedious afternoon of housekeeping into a single-command operation.

But, as you've seen, everything happens in tandem with those principles. No important action is taken without my confirmation, and everything gets logged into the filesystem, so all future decisions are grounded in past experience.

### Content Creation

Now let's focus on writing high-quality documentation and long-form articles. This is perhaps the most sensible part of the article (and the system) because people are *very* sensitive today with the topic of AI writing---and rightly so. Again, my intention here is to enhance how I work and get stuff done. If you're writing for the pleasure of doing it, that's totally fine, you probably don't want any help there.

Anyway, the approach is built on the same cognitive foundation as the development path: the research and plans gathered during the discovery phase should serve as grounding for writing.

It starts with the `/draft` command. In its initial phase, the system performs a deep scan of the `research/` and `plans/` directories to identify the key themes relevant to the requested topic. If the foundation is too thin, the system will pause and suggest a `/research` or `/plan` cycle to ensure the draft has sufficient substance. Once the context is validated, the workflow enters an interactive "Outline Creation" phase. Rather than guessing at a structure, the system proposes a detailed Markdown outline. This collaborative step allows me to set the narrative arc and logical flow that I want, iterating on the high-level structure of, say, a technical article, before committing on the details.

Once the outline is locked, the `/draft` process initializes a skeleton file---complete with section headers and strategic placeholders---and then moves into an iterative, section-by-section expansion. Here, the `reporter` subagent takes the lead. Guided by the specific context of each section, the `reporter` weaves together research summaries and technical specifications into professional prose, all grounded on a style guide document.

Because the expansion happens in granular steps, the system maintains a high level of detail that a single-shot generation would inevitably lose. The result is a first draft that is structurally sound and rich with technical depth.

However, a first draft is rarely the final word. It will always sound AI-ish, and for many other reasons, it is rarely good enough. To achieve professional quality, I use the `/revise` command, which runs a structural and linguistic audit powered by the `editor` subagent following the same style guide.

Unlike a simple "check my writing" prompt, the `editor` performs a deep analysis of the document's flow and tone. It identifies logical gaps where more evidence might be needed and highlights awkward phrasing that could obscure my intent. And crucially, this isn't an automated "fix-all" tool; it's an interactive process. The system presents its findings and proposes specific improvements, which I can then review or approve.

This collaborative refinement process ensures the final output maintains a consistent, professional voice while benefiting from the speed of the AI. By using `/revise`, I can surgically improve the text to enhance clarity and impact without losing control over the narrative.

But, in any case, I always find necessary a manual review and editing after all the AI enhancements. It shouldn't be a surprise to you that this article is written in this way, but what you're reading now is probably 80% different to what the final `/revise` iteration gave me. There is only so much you can prompt an AI, and that final human touch is not part of it.

But that's good. This automates the first 80% or so of compiling a gazillion sources into a coherent narrative, and leaves the remaining 80% of polishing for me, which is the part I actually enjoy about writing.

### Background Tasks

But there's more. All of the above is what happens during, let's say, the work day. That's me sitting in front of the terminal, typing commands, approving stuff, fixing and redirecting, etc. Being an orchestrator.

But the real magic of AI-assisted development is what happens when you're not looking. How you can leave you AI assistant working through the night, compiling sources, fixing bugs and proposing pull requests, enhancing the test suite, burning tokens your behalf.

To achieve this, I built an automation layer via the `/cron` command. The heart of this automation is the `cron.toml` file. This configuration file allows me to define scheduled tasks with a simple, declarative syntax. Each task specifies a name, an execution schedule, and a natural language prompt for the AI to execute.

For instance, I can schedule a task to perform "Background Research" every midnight on the unfinished tasks, scouring the web for new developments in a specific technical niche or finding specific sources to deal with the recently discovered bugs. By offloading these repetitive tasks, I ensure the knowledge base remains fresh and the project's momentum never stalls. When the morning arrives, we have a lot of new context to start planning the day's bugfixes and feature developments.

## Maintenance & Refactoring

Now, for the final touch, here's how I deal with technical debt and feature rot. As a project evolves---and especially, as fast as AI-powered projects evolve---it accumulates technical debt---outdated implementations, untested paths, and plain old useless features---but also, contextual debt--—outdated plans and completed tasks that clutter the roadmap, and research we never acted upon.

Without deliberate intervention, this noise degrades the AI's performance, leading to context rot. The `/maintenance` command is my primary defense against this entropy. It treats the development environment as a living instrument that I must regularly tune and sharpen to maintain its efficiency.

The `/maintenance` workflow follows the same plan-first architecture as the rest of the system. When invoked, the AI performs a comprehensive audit of the codebase, focusing on improvements like code readability and performance optimization. It identifies opportunities to apply the DRY (Don't Repeat Yourself) principle and ensures that every function is documented with high-quality docstrings. But it also fixes deviations between the documentation and the actual implementation.

Crucially, this is an interactive process: the system presents a detailed refactoring plan for my approval before making any changes. This ensures that I remain in control while the machine handles the labor of cleaning the code.

Beyond code refactoring, I maintain system health through disciplined repository hygiene. A key component is the management of the `TASKS.md` file. By regularly moving completed items into the "Archive" section, I ensure that my primary operational view remains focused on what is relevant. This simple act of archiving prevents the "Active Tasks" list from becoming a source of distraction.

The goal of these maintenance practices is to provide the AI with the cleanest possible line of sight into the project's state. When the repository is cluttered with stale research, the subagents are forced to sift through irrelevant data, increasing the risk of hallucinations. By treating maintenance as a first-class citizen, I ensure that every interaction, whether a `/plan` or a `/draft`, is grounded in a precise context.

## Conclusion

This system is far from done, and as models improve in capabilities I'm sure we'll unlock new areas for automation and augmentation that we cannot think about today. But for me, the key principles will remain valid for a long time. These are principles of robust engineering and management, after all. You can read them thinking of a completely human-based organization, and it's all valid:

1. The important things should be made explicit.
2. Resist the urge to guess.
3. Delegate, delegate, delegate (yeah, three times).

And this is the key insight for me. Good AI users are basically good managers. All the science and engineering behind good practices for people management also apply to good AI management. And then there are of course technical considerations because AIs are not people, and perhaps never will.

So this is perhaps the most philosophical take-away from this article. Sorry to have made you read so long for this!

Now, on the technical side, please do check the [repository](https://github.com/apiad/starter) and play with it.

This repository is not a "one-size-fits-all" solution. It is a starting point. The commands and subagents provided here represent a particular opinion on how modern development should look, but they are not the only way. The power of this framework lies in its extensibility. Every system prompt for agents and commands is a living document, meant to be tweaked and rewritten to suit your unique mental model.

So if you do try it out, please let me know in the comments. And if you have a different (or similar) system set up for yourself, please share with all us your experience and your thoughts. We are all learners in this era of AI, and we can only help each other.

Stay curious.
