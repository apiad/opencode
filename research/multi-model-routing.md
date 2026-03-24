# Best Practices for Multi-Model Configurations and Automatic Model Routing in Gemini CLI

## Executive Summary
This report defines the best practices for implementing multi-model configurations and dynamic model routing in the Gemini CLI (v0.34.0). Through native configurations (`settings.json`) and lifecycle hooks (`BeforeModel`, `BeforeAgent`), developers can create an intelligent routing system that automatically directs tasks to specialized models (e.g., `Thinker` for deep reasoning, `Executioner` for rapid coding). 

Key findings reveal that while the CLI natively supports static model selection via flags and configuration aliases, true dynamic routing requires careful hook implementation. Successful routing demands strict adherence to the expected JSON response schemas, safe parsing of the Gemini API's nested `parts` structures, and sequential hook execution to prevent race conditions. Furthermore, due to the CLI's lack of hot-reloading for configurations, developers must adopt robust, out-of-band logging and isolated testing scripts to iterate effectively without constant session restarts.

## Research Questions

### 1. Native Multi-Model Configuration in Gemini CLI
*For detailed findings, see [RQ1 Research Asset](multi-model-routing/rq1-native-config.md).*

**High-Level Overview:**
- **Native Configuration:** Gemini CLI uses `modelConfigs.customAliases` and `modelConfigs.overrides` in `.gemini/settings.json` to define model aliases, inherit parameters (via `extends`), and apply context-specific overrides (e.g., for specific agents). 
- **Dynamic Switching:** Models can be overridden dynamically using the `--model` (`-m`) CLI flag or the `GEMINI_MODEL` environment variable. The order of precedence is CLI Flags > Environment Variables > Project Settings > User Settings.
- **Fallback Behavior:** Governed by `ModelAvailabilityService`. Interactive sessions prompt the user when a model is unavailable, while background utilities use a strict fallback sequence (`flash-lite` -> `flash` -> `pro`). Fallback can be disabled via the `--no-model-fallback` flag or `disableModelFallback` setting.
- **Parameter Handling:** Configuration attributes like `temperature` and `maxOutputTokens` reside in `generateContentConfig`. When switching models or inheriting via aliases, parameters are deeply merged, prioritizing the most specific context.

### 2. Hook-Based Dynamic Model Routing
*For detailed findings, see [RQ2 Research Asset](multi-model-routing/rq2-hook-routing.md).*

**High-Level Overview:**
- **Reliable Hook Events:** In Gemini CLI v0.34.0, `BeforeModel` is the definitive hook for dynamic model routing. It executes after all prompt hydration and context assembly, making it the safest place to override the model before the API call. While `BeforeAgent` exists, it is prone to downstream overrides. (Note: The RCA highlighted issues with `BeforeModel` failing silently, which often stems from schema mismatches rather than the hook itself being unsupported, but `BeforeAgent` might be used as a fallback if modifying state earlier is required).
- **Override Schema:** To switch models, a hook must return a precise JSON structure. The expected schema typically involves returning an object with `hookSpecificOutput` containing an `llm_request` block that overrides the `model` property (e.g., `{"hookSpecificOutput": {"llm_request": {"model": "gemini-3.1-pro-preview"}}}`).
- **Safe History Parsing:** When analyzing previous turns for semantic signals (like `[Tier: Thinker]`), hooks must safely parse the `llm_request.messages` array. The Gemini API uses a `parts` array (e.g., `[{"text": "..."}]`) for structured content, especially during tool calls, rather than a simple `content` string. Fallback logic should check both.
- **Execution Order:** When chaining multiple hooks (e.g., a logger and a router), setting `sequential: true` in `settings.json` is critical. This guarantees synchronous execution, preventing race conditions where one hook's override might be lost or conflict with another's read/write operations.

### 3. Command and Subagent Routing Integration
*For detailed findings, see [RQ3 Research Asset](multi-model-routing/rq3-agent-routing.md).*

**High-Level Overview:**
- **Native TOML Commands:** Custom `.toml` commands (e.g., in `.gemini/commands/`) can natively define preferred models by including a `tier` or `model` attribute (e.g., `tier = "Thinker"`) in the file's frontmatter or configuration block. The CLI parses this and switches the session context prior to executing the command's prompts.
- **Subagent Specifications:** Similarly, subagents defined in `.gemini/agents/*.md` can statically declare their required model using YAML frontmatter (e.g., `tier: Executioner`). Subagents can also utilize dynamic signaling during multi-step executions if they need to shift cognitive modes.
- **Semantic Signaling & Context Management:** The best practice for dynamic routing is "Semantic Signaling" (e.g., appending `[Tier: Thinker]` to a response). To prevent context pollution and token waste, a `BeforeAgent` or `AfterModel` hook should detect the regex, update the routing state, and then strip the tag from the final message before it is saved to the persistent history or displayed to the user.
- **Robust User Feedback:** Model switching, particularly to heavier reasoning models, introduces latency. Hooks should return a `systemMessage` (e.g., "Switching to Thinker Tier...") which the CLI renders natively. For out-of-band awareness, scripts can execute system-level notifications (e.g., `notify-send`) via subprocesses.

### 4. Testing and Debugging Workflows for CLI Extensions
*For detailed findings, see [RQ4 Research Asset](multi-model-routing/rq4-testing-workflows.md).*

**High-Level Overview:**
- **Hot-Reloading Workarounds:** Because Gemini CLI (`v0.34.0`) caches `settings.json` on startup, hooks cannot be hot-reloaded dynamically during an active session. The best testing strategy is creating standalone mock scripts that simulate the CLI's `stdin` JSON payload, allowing developers to test hook logic (like JSON parsing and routing decisions) independently without restarting the CLI.
- **Standalone Stateful Logging:** Standard output (`stdout`) is consumed by the CLI to parse hook responses. Therefore, using standard `print()` statements for debugging will corrupt the JSON and crash the hook. Developers must implement a standalone logger (e.g., writing directly to `/tmp/gemini_hooks.log` or a dedicated `gemini_hooks.log` file) using Python's native file I/O or `logging` module to trace execution safely.
- **"Hello World" Validation:** The recommended pattern for new hook development is the "Probe Pattern". Before implementing complex routing, deploy a simple hook that catches the target event (e.g., `BeforeAgent`) and performs a basic file-write of the received `stdin` payload. This guarantees the event triggers in the current environment and provides the exact JSON schema you need to parse.

## Conclusions
Dynamic model routing in the Gemini CLI is highly achievable but requires precision. The primary pitfalls encountered in multi-model implementations stem from environmental misunderstandings (e.g., assuming `content` strings instead of `parts` arrays) and CLI lifecycle constraints (e.g., cached configurations preventing hot-reloading). By leveraging `BeforeModel` or `BeforeAgent` hooks, parsing the message history defensively, and injecting structured override JSON payloads, the CLI can seamlessly transition between cognitive tiers.

## Recommendations

### Immediate Actions
1. **Standardize Routing Hooks:** Implement a universal `tier_router.py` hook bound to the `BeforeAgent` or `BeforeModel` lifecycle event. Ensure it has `sequential: true` enabled in `settings.json`.
2. **Implement Defensive Parsing:** Update all historical message parsing logic to handle both `message.get("content")` and `message.get("parts")` to ensure compatibility across different API states (standard text vs. tool calling).
3. **Establish Out-of-Band Logging:** Create a dedicated logging utility for all custom hooks that writes directly to a standalone file (e.g., `gemini_hooks.log`) to prevent stdout corruption and facilitate debugging.

### Future Research
- Investigate the potential for a native "hot-reload" command within the Gemini CLI to refresh `settings.json` without dropping the active session.
- Explore creating a standardized Subagent framework that natively incorporates tier requirements, reducing the reliance on regex-based semantic signaling.