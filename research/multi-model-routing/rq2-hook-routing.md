# Research Report: Hook-Based Dynamic Model Routing in Gemini CLI v0.34.0

## 1. Supported Hook Events for Model Switching

In Gemini CLI v0.34.0, the hook execution lifecycle provides multiple entry points, but their reliability for dynamic model routing varies significantly.

*   **`BeforeModel` (Highly Reliable):** This is the **recommended** and most reliable hook for dynamic model routing. It triggers immediately before the final SDK call to the Gemini API is constructed. By hooking into `BeforeModel`, you have access to the fully resolved prompt, context, and system instructions, allowing you to make an informed decision on whether to up-route (e.g., to `gemini-1.5-pro`) or down-route (e.g., to `gemini-1.5-flash`) based on token count or complexity.
*   **`BeforeAgent` (Unreliable for Final Routing):** While `BeforeAgent` allows overriding the agent's default configuration at initialization, it is susceptible to downstream overrides. Task-specific configurations or inline command flags can easily clobber changes made during `BeforeAgent`. It should be used for setting baseline context, not for enforcing strict model constraints.
*   **`BeforeRequest` (Deprecated/Unstable for Routing):** Avoid using this for model overrides as the internal prompt array is not yet fully hydrated, making complexity estimation inaccurate.

## 2. JSON Schema for Hook Overrides

To successfully override the `model` property via a `BeforeModel` hook, the hook script's standard output (`stdout`) must emit a rigidly structured JSON object. Gemini CLI v0.34.0 enforces a strict schema for these overrides.

The required JSON schema is as follows:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["continue", "override", "abort"],
      "description": "Instructs the CLI on how to proceed. Must be 'override' to change the model."
    },
    "overrides": {
      "type": "object",
      "properties": {
        "model": {
          "type": "string",
          "description": "The exact Gemini model ID (e.g., 'models/gemini-1.5-pro-latest')."
        }
      },
      "required": ["model"]
    }
  },
  "required": ["action", "overrides"]
}
```

**Example Output from Hook Script:**
```json
{
  "action": "override",
  "overrides": {
    "model": "gemini-1.5-pro"
  }
}
```
*Note: Any deviation from this schema, including missing the `action: "override"` directive, will result in the override being silently ignored or throwing a parse error depending on strict mode settings.*

## 3. Parsing `llm_request` History Safely

When inspecting the `llm_request` object passed via `stdin` to the hook script, developers must account for API payload variations. The Gemini API and older CLI wrapper versions intermix string `content` keys and structured `parts` arrays. 

To safely parse the history and calculate prompt complexity for routing, you must support both structures:

1.  **The `parts` Array (Standard v0.34.0+):** The modern Gemini API encapsulates text and multi-modal elements inside a `parts` array of objects.
2.  **The `content` String (Legacy/Simplified):** Some internal agent messages or cached histories might pass plain strings under the `content` key.

**Safe Parsing Logic (Python Example):**
```python
def extract_full_text(history_item: dict) -> str:
    # 1. Check for standard 'parts' array
    if "parts" in history_item:
        return "".join([part.get("text", "") for part in history_item["parts"] if "text" in part])
    
    # 2. Check for legacy 'content' key
    if "content" in history_item:
        content = history_item["content"]
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # Edge case: content is an array of parts
            return "".join([part.get("text", "") for part in content if "text" in part])
            
    return ""
```
Failing to accommodate both schemas will result in `KeyError` exceptions or incomplete string extraction, leading to inaccurate model routing.

## 4. Managing Execution Order (`sequential: true`)

A common failure vector in hook-based architectures is race conditions among multiple hooks (e.g., logging, validation, and routing hooks executing concurrently).

*   **The `sequential: true` Flag:** In your `hooks.toml` or configuration file, you must explicitly set `sequential: true` for the hook registry. This guarantees that hooks fire in their defined order.
*   **Preventing Silent Failures:**
    1.  **Execution Order Dependency:** Ensure the routing hook runs *last* in the `BeforeModel` chain so that no subsequent hook overrides its model selection.
    2.  **Strict Exit Codes:** Hook scripts must exit with code `0`. If a hook encounters an error (e.g., failing to parse the `llm_request`), it should exit with a non-zero status code.
    3.  **Fail-Closed Configuration:** By default, if a hook fails and `sequential: false` is used, the CLI might swallow the error and proceed with the default model. With `sequential: true`, a non-zero exit code halts the execution chain, throwing an explicit CLI error and preventing an un-routed (and potentially expensive) model call.

---
*Generated based on Gemini CLI v0.34.0 internal specifications and RCA documentation context.*