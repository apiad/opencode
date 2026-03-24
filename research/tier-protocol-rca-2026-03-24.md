# Root Cause Analysis: Tier Protocol Implementation Failure (2026-03-24)

## Symptom
The Tier Protocol failed to switch models dynamically. Despite the agent emitting semantic signals like `[Tier: Thinker]`, the system remained on the default `gemini-3-flash-preview` model. No "Tier Switch" notifications or specific routing logs were produced during the implementation attempts.

## Investigation Points

### 1. Hook Non-Activation
- **Findings**: The `BeforeModel` hook, while documented in some versions of Gemini CLI, appeared to be inactive or non-functional in the current environment (v0.34.0).
- **Verification**: `grep` searches for `--- BEFOREMODEL ---` in `gemini.log` returned no structural headers, only references within model responses.
- **Impact**: The `tier_router.py` script was never invoked by the CLI at the intended interception point.

### 2. Restart Requirement
- **Findings**: Changes to `.gemini/settings.json` and hook scripts are not "hot-reloaded". They require a full termination and restart of the Gemini CLI process to take effect.
- **Verification**: Changes to the logging format and hook paths only appeared in the logs after manual restarts.
- **Impact**: Initial testing cycles were invalid as they were running against stale configurations, leading to "feedback ghosting".

### 3. API Structure Mismatch
- **Findings**: The initial `tier_router.py` logic attempted to find signals using `message.get("content", "")`.
- **Verification**: In the Gemini API (especially during turns involving tool calls), the model response is stored in a `parts` list (e.g., `[{"text": "..."}]`).
- **Impact**: Even if the hook had fired, the regex search would have failed to find the `[Tier: ...]` signal because it was looking in the wrong field.

### 4. Logging Invisibility
- **Findings**: `utils.log_message` defaults to `gemini.log` in the current working directory.
- **Verification**: If the hook fails to start (due to path issues or interpreter errors), no log entry is created. 
- **Impact**: The lack of "start" logs in the hook made it difficult to distinguish between a "hook not firing" and a "hook crashing".

### 5. Hook Chain and Sequential Execution
- **Findings**: Multiple hooks registered for the same event (e.g., `BeforeAgent`) may not behave as expected if they depend on each other's output or side effects unless `sequential: true` is explicitly set.
- **Impact**: Potential race conditions or silent failures when chaining `log.py` and `tier_router.py`.

## Root Causes
1. **Environment/Documentation Mismatch**: Implementation targeted the `BeforeModel` hook which was inactive in the current CLI runtime.
2. **Schema Ignorance**: The routing logic was not resilient to the `parts`-based message structure of the Gemini API.
3. **Workflow Friction**: The requirement for manual restarts was not integrated into the TDD/TCR cycle, leading to long debug loops on stale code.

## Recommendations for Future Implementation
1. **Validation First**: Create a "Hello World" hook for any new event type to confirm it triggers before implementing complex logic.
2. **Robust Content Extraction**: Always check both `content` and `parts` fields when parsing message history.
3. **Absolute Pathing**: Use absolute paths for all hook commands in `settings.json` to avoid ambiguity across different execution contexts.
4. **Restart Automation**: If possible, implement a script that modifies settings and restarts the CLI to ensure a clean state.
5. **Stateful Debugging**: Use a dedicated, independent log file (e.g., `/tmp/gemini_hooks.log`) for low-level hook debugging to bypass the main session log's constraints.

---
**Status**: Implementation branch `feature/tier-protocol` discarded. Workspace reverted to `main`.
**Author**: Gemini CLI (Thinker Tier)
**Date**: 2026-03-24
