# RQ3: Command and Subagent Routing Integration

This research explores the integration of multi-model routing within the Gemini CLI, focusing on how custom commands and subagents can request specific model tiers and how to manage these transitions seamlessly.

## 1. Custom `.toml` Commands and Tier Requesting

Custom commands defined in `.toml` files (located in `.gemini/commands/`) can natively request a preferred model tier by including a `tier` or `model` field within the `[command]` configuration block.

### Implementation Pattern
The CLI command parser should be extended to look for a `tier` key. When a command is invoked, the CLI should pre-emptively switch the session's active model to the one associated with that tier.

**Example `research.toml`:**
```toml
[command]
name = "research"
description = "Perform deep research on a topic"
tier = "Thinker"  # Requests the high-reasoning model
agent = "researcher"
```

**Workflow:**
1. User runs `gemini research "topic"`.
2. CLI reads `research.toml`.
3. CLI identifies `tier = "Thinker"`.
4. CLI switches the session model to `gemini-3.1-pro-preview` (or the current Thinker model).
5. CLI invokes the `researcher` agent.

## 2. Subagent Tier Specification

Subagents (defined in `.gemini/agents/*.md`) require a standard way to declare their optimal tier. This ensures that when an agent is invoked (either via a command or a subagent call), it operates at the necessary performance/cost/reasoning level.

### Frontmatter Specification (Recommended)
The most robust pattern is using YAML frontmatter in the agent's markdown file.

**Example `researcher.md`:**
```markdown
---
name: Researcher
tier: Thinker
capabilities: [search, web_fetch, synthesis]
---

# Researcher Agent
You are a senior researcher. Your goal is to gather detailed information...
```

### Dynamic Signaling
Agents can also request a tier switch mid-conversation by emitting a semantic signal (see below). This is useful for "Orchestrator" agents that decide to delegate a complex task to a "Thinker" or "Executioner" step.

## 3. Semantic Signaling and Context Pollution

Semantic signaling allows the model to communicate routing instructions to the CLI wrapper. The current best practice uses the `[Tier: <TierName>]` pattern.

### The Signal Pattern
- **Signal:** `[Tier: Orchestrator]`, `[Tier: Thinker]`, or `[Tier: Executioner]`.
- **Placement:** The signal should be placed at the end of the agent's response to signify the tier for the *subsequent* turn.

### Avoiding Context Pollution
To prevent the signal from "polluting" the conversation history (which might cause the model to hallucinate or repeat the signal unnecessarily), the following measures should be implemented:

1. **Detection Hook:** A hook in `session.py` or `log.py` should intercept the agent's output.
2. **Regex Extraction:** Use a regex like `r"\[Tier:\s*(\w+)\]"` to extract the tier name.
3. **State Update:** Update the session's `active_model` based on the mapping (e.g., `Thinker -> gemini-3.1-pro-preview`).
4. **Stripping (Optional but Recommended):** The CLI should strip the signal from the message before:
   - Displaying it to the user (unless in debug mode).
   - Storing it in the long-term `session.json` history.
   - Sending it back to the model in the next turn's prompt.

## 4. User Feedback and Notifications

Switching tiers often involves a change in latency and behavior. Providing clear feedback prevents user confusion.

### UI Messages
The CLI should provide immediate visual feedback when a tier switch occurs:
- **Color-coded Status:** Print `(Switching to Thinker Tier...)` in a distinct color (e.g., Cyan).
- **Prefixes:** Prefix subsequent outputs with the current tier, e.g., `[Thinker] > Thinking...`.

### Desktop Notifications
For long-running tasks where the user might have switched windows:
- **`notify.py` Hook:** A dedicated hook that triggers system-level notifications (e.g., `notify-send` on Linux, `display notification` on macOS).
- **Threshold-based:** Only notify if the switch is to a "heavy" tier like **Thinker**, which implies a longer wait time.

### Example Notification Implementation
```python
# .gemini/hooks/notify.py
import os

def on_tier_switch(new_tier):
    if new_tier == "Thinker":
        os.system(f'notify-send "Gemini CLI" "Switching to Thinker Tier for deep reasoning..."')
```

## Conclusion

Integrating routing into commands and subagents via TOML config, Markdown frontmatter, and semantic signals provides a flexible and powerful way to manage model resources. By implementing robust signal stripping and user notifications, the Gemini CLI can maintain a clean context and a responsive user experience.
