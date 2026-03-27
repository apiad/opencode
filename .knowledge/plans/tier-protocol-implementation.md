# Implementation Plan: Tier Protocol Model Routing System

This plan outlines the implementation of the "Tier Protocol" for the Gemini CLI, enabling dynamic model routing based on task complexity (Orchestration, Thinking, Execution).

## Objective
Establish a three-tier model routing system to optimize performance, cost, and reasoning quality by using specialized models for different phases of the agent's workflow.

## Architectural Impact
- **Middleware Integration**: Adds a `BeforeModel` hook (`tier_router.py`) that acts as a traffic controller for model selection.
- **Semantic Signaling**: Uses explicit `[Tier: *]` tags in assistant messages to communicate routing intent to the framework.
- **Centralized Configuration**: Standardizes model mapping and default settings in `.gemini/settings.json`.
- **System-level Feedback**: Integrates `notify-send` for real-time user visibility of tier switches.

## File Operations

| Action | File | Description |
| :--- | :--- | :--- |
| **Modify** | `GEMINI.md` | Define the Tier Protocol, models, signals, and usage guidelines. |
| **Create** | `.gemini/hooks/tier_router.py` | Implement the logic to parse signals and route models. |
| **Modify** | `.gemini/settings.json` | Register the `BeforeModel` hook and set the default model. |
| **Modify** | `.gemini/commands/*.toml` | Update command prompts to include tier signaling instructions. |

## Step-by-Step Execution

### Step 1: Document the Tier Protocol in `GEMINI.md`
Add a new section to `GEMINI.md` defining the protocol:

```markdown
## Tier Protocol

To optimize reasoning and execution, this project uses a multi-tier model routing system:

| Tier | Model | Use Case | Signal |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | `gemini-3-flash-preview` | Default routing, task management, and fast orchestration. | `[Tier: Orchestrator]` |
| **Thinker** | `gemini-3.1-pro-preview` | Deep architectural planning, RCA, and complex logic. | `[Tier: Thinker]` |
| **Executioner** | `gemini-2.5-flash` | High-velocity coding, boilerplate, and tool-heavy tasks. | `[Tier: Executioner]` |

**Guidelines:**
- **Implicit Default:** All sessions start in Orchestrator tier.
- **Explicit Switching:** Always emit the signal (e.g., `[Tier: Thinker]`) at the end of your response to route the *next* turn to that model.
- **Phase Transition:** Switch to **Thinker** for discovery/planning and **Executioner** for task implementation.
```

### Step 2: Implement the `tier_router` Hook
Create `.gemini/hooks/tier_router.py` with the following logic:

```python
import sys
import json
import re
import os
import subprocess

# Model Mapping
TIER_MAPPING = {
    "Orchestrator": "gemini-3-flash-preview",
    "Thinker": "gemini-3.1-pro-preview",
    "Executioner": "gemini-2.5-flash"
}

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"decision": "allow"}))
            return
        
        data = json.loads(input_data)
        history = data.get("history", [])
        
        # Identify target tier from last assistant message
        target_tier = None
        for message in reversed(history):
            if message.get("role") == "assistant":
                content = message.get("content", "")
                match = re.search(r"\[Tier:\s*(Orchestrator|Thinker|Executioner)\]", content)
                if match:
                    target_tier = match.group(1)
                    break
        
        # Prepare response
        response = {"decision": "allow"}
        
        if target_tier and target_tier in TIER_MAPPING:
            model_id = TIER_MAPPING[target_tier]
            response["model"] = model_id
            response["systemMessage"] = f"Tier Protocol: Active ({target_tier})"
            
            # User Notification
            try:
                subprocess.run([
                    "notify-send", 
                    "Gemini Tier Switch", 
                    f"Routing to {target_tier}: {model_id}", 
                    "-i", "dialog-information", "-t", "2000"
                ], check=False)
            except:
                pass

        print(json.dumps(response))
            
    except Exception as e:
        sys.stderr.write(f"Error in tier_router: {str(e)}\n")
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
```

### Step 3: Update `settings.json` Configuration
Register the hook and set the default model:

```json
{
  "model": "gemini-3-flash-preview",
  "hooks": {
    "BeforeModel": [
      {
        "matcher": "*",
        "hooks": [
          {
            "name": "tier-router",
            "type": "command",
            "command": "python3 .gemini/hooks/tier_router.py"
          }
        ]
      }
    ]
  }
}
```

### Step 4: Update Command Prompts for Signaling
Update `.gemini/commands/*.toml` to incorporate tier instructions.

#### Thinker-Heavy Commands
Add `[Tier: Thinker]` requirement to:
- `brainstorm.toml`: "Start by switching to `[Tier: Thinker]` to engage deep reasoning."
- `plan.toml`: "Use `[Tier: Thinker]` for architectural analysis phases."
- `research.toml`, `review.toml`, `learn.toml`, `issues.toml`, `document.toml`, `draft.toml`: Update to prioritize Thinker.

#### Executioner-Heavy Commands
Add `[Tier: Executioner]` requirement to:
- `commit.toml`: "Switch to `[Tier: Executioner]` for rapid change grouping and committing."
- `scaffold.toml`: "Use `[Tier: Executioner]` for boilerplate generation."

#### Hybrid Commands (Phase-based Routing)
- `debug.toml`:
  - **Phase 2 (Hypothesis):** Switch to `[Tier: Thinker]`.
  - **Phase 3 (Testing):** Switch to `[Tier: Executioner]` for diagnostic branch work.
- `task.toml`:
  - **Phase 3 (TCR Loop):** Instruct the Orchestrator to switch to `[Tier: Executioner]` for implementation steps.

## Testing Strategy
1. **Routing Logic Validation**: Use a mock session JSON (containing `[Tier: Thinker]`) and pipe it into `tier_router.py` to verify the output contains `"model": "gemini-3.1-pro-preview"`.
2. **Notification Test**: Trigger the hook and verify the `notify-send` desktop alert appears.
3. **End-to-End Command Test**: Run `/plan` and verify the first assistant turn ends with `[Tier: Thinker]`, followed by the model switch in the subsequent turn.
4. **Integration Test**: Verify `settings.json` registration doesn't interfere with existing hooks (e.g., `log.py`, `notify.py`).
