---
description: Runs research in parallel and produces a report
agent: analyze
---

<!-- Zero-th block, let's interpret the user request -->

```yaml {config}
step: define
parse:
    TOPIC: A short, kebab-case slug for the research
    TITLE: A descriptive title for the research report
    PURPOSE: Descriptive purpose for the research objective
```

You are running the /research command, we are going to build a research plan and present it to the user first.

Based on:
- the user arguments: $ARGUMENTS
- the conversation context so far

Define the topic, title, and purpose of the research in a few words.

---

<!-- First this block is inserted, we wait for the LLM to finish.-->

```yaml {config}
# This is a configuration for the current block, so we can later reference it
step: planning
question:
    title: Do you approve the research plan?
    options:
        Yes: collect
        No*: refine
```

Based on the previous definition, generate a comprehensive research plan and present it to the user.

The plan must have 2-6 general research questions, separated into sub-questions.

<!-- Once the entire session finishes, with all its thinking and planning, we run the question and we route accordingly.  -->

---

```yaml {config}
step: refine
next: approval

# If the land for the fourth time in this block the command is cancelled.
max-iter: 3
```

The user is not ok with the plan. Refine the plan based on the user feedback.

---

<!-- This is the third block, we only land here if the user approved the plan -->

```yaml {config}
# These IDs are optional, by default we call them step-1, step-2, etc.
step: collect
next: synthesize
```

<!-- Here I want some way to split the plan into structured substeps, and invoke subagents, lets brainstorm that -->

Split the research plan into separate research objectives. Each objective must be a well-described prompt for a scout subagent to collect data.

```python {exec subagent=scout}
def collect_sources(objectives: list[str]):
    for obj in objectives:
        yield f"Research the following: {obj}\n\nSynthesize response into a Markdown report in research/$TOPIC/assets/"
```

---

<!-- This is the synthesize step -->

```yaml {config}
step: synthesize
```

Synthesize the findings in $GLOB(research/$TOPIC/assets/*.md) and write a structured report in `research/$TOPIC/report.md`.

---
