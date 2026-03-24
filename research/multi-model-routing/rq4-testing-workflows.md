# RQ4: Testing and Debugging Workflows for CLI Extensions

This research note outlines the optimal workflows for testing and debugging hooks within the Gemini CLI environment, addressing challenges identified in the `tier-protocol-rca-2026-03-24.md` analysis, specifically regarding silent failures and environment visibility during multi-model routing.

## 1. Strategy: Testing Hooks without CLI Restarts

Testing hooks by repeatedly running the full CLI cycle is inefficient and often fails to isolate hook logic from core CLI state. The recommended strategy is **Direct Script Invocation with Environment Mocking**.

### Isolation via Mocking
Since Gemini CLI hooks are standalone Python scripts (located in `.gemini/hooks/`), they can be executed independently of the main CLI binary. This bypasses the need to restart the CLI or navigate complex command-tree states.

**Key Steps:**
1.  **Identify Required Context:** Determine which environment variables (e.g., `GEMINI_MODEL`, `GEMINI_CONTEXT`, `GEMINI_API_KEY`) the hook expects.
2.  **Create a Runner Script:** Use a shell script or a Python utility to invoke the hook with mock data.
3.  **Automated Triggering:** Use a file watcher (like `entr` or `watchman`) to re-run the hook on save.

**Example Runner (`tests/test_hook_runner.sh`):**
```bash
#!/bin/bash
# Mock the environment variables passed by the CLI
export GEMINI_MODEL="gemini-1.5-pro"
export GEMINI_PROMPT_TOKENS=1024
export GEMINI_HOOK_DEBUG=true

# Invoke the hook directly
python3 .gemini/hooks/pre-commit.py --dry-run
```

## 2. Standalone Hook Logging (`gemini_hooks.log`)

Standard Output (`stdout`) is unreliable for debugging hooks because:
-   The CLI often redirects `stdout` for piping or UI rendering.
-   Hooks may run in background processes (e.g., `cron.py`).
-   Multi-model routing logs might clutter the main terminal output.

### Implementation Pattern
Implement a dedicated logger in `.gemini/hooks/utils.py` that writes to a persistent log file in the workspace or the user's home directory.

**Recommended Setup (`.gemini/hooks/utils.py`):**
```python
import logging
import os
from pathlib import Path

def get_hook_logger(name: str):
    """
    Returns a logger that writes to a standalone file, bypassing CLI stdout.
    """
    log_path = Path.home() / ".gemini" / "gemini_hooks.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
```

**Usage in Hooks:**
```python
from utils import get_hook_logger

logger = get_hook_logger("routing-hook")
logger.info("Analyzing model tier for prompt...")
```

To monitor logs in real-time:
```bash
tail -f ~/.gemini/gemini_hooks.log
```

## 3. "Hello World" Validation Pattern

When implementing a new hook, use the following "Probe" pattern to validate connectivity and environment propagation before adding complex logic.

### The Validation Script (`.gemini/hooks/hello_world.py`)
```python
import sys
import os
import json
from utils import get_hook_logger

logger = get_hook_logger("hello-world")

def validate():
    # 1. Capture Environment
    context = {
        "args": sys.argv[1:],
        "env": {k: v for k, v in os.environ.items() if k.startswith("GEMINI_")},
        "cwd": os.getcwd()
    }
    
    # 2. Log Detailed State
    logger.info("=== Hook Validation Started ===")
    logger.debug(f"Context: {json.dumps(context, indent=2)}")
    
    # 3. Validation Logic
    if not context["env"].get("GEMINI_MODEL"):
        logger.warning("GEMINI_MODEL environment variable is missing!")
        return False

    logger.info("Hook connectivity valid.")
    return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
```

### Integration Test
Add the hook to the CLI configuration and trigger a command. Verify the log entry appears in `gemini_hooks.log` with the correct timestamp and environment metadata. This confirms the CLI's hook-loading mechanism is functioning as expected.

## Summary of Findings
- **Testing:** Isolation is superior to CLI-level integration testing for rapid iteration.
- **Logging:** A persistent, file-based logging system is essential to diagnose issues in routed environments where `stdout` is captured.
- **Validation:** Use a structured "Probe" pattern to audit the environment before executing core hook logic.
