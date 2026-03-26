---
description: Switch to ship mode for lifecycle management
agent: ship
---

Switch to ship mode.

## Behavior

Check current state (git status, recent journal entries) to infer what needs shipping.
Present options if multiple apply:
- Commit pending changes
- Release a new version
- Manage issues

Ask the user: "What would you like to ship?" if unclear.
