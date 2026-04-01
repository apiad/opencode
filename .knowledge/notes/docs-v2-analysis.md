# Documentation Analysis: v2.0.0

Analysis date: 2026-04-01
Purpose: Identify documentation updates needed for v2.0.0 release

## v2.0.0 New Features

1. **Literate Commands** - Multi-step guided workflows
   - Variable collection with types
   - Conditional logic support
   - In-place array mutation for command abort
   - Phase-based execution (parse → substitute → route → execute)

2. **Sandbox Plugin** - Docker-based isolation
   - Mode-specific command routing
   - Isolated execution context
   - `.opencode/sandbox/` directory

3. **Enhanced Agent Architecture**
   - 4 modes: analyze, plan, build, release
   - Lit-commands subagent for literate command processing

## Documentation Status

### `index.md` - NEEDS UPDATE
| Section | Status | Notes |
|---------|--------|-------|
| Key Capabilities | ❌ Incomplete | Missing literate commands, sandbox |
| Project Lifecycle | ❌ Incomplete | References `/release` but not documented |

### `user-guide.md` - NEEDS UPDATE
| Section | Status | Notes |
|---------|--------|-------|
| Agent Architecture | ❌ Incomplete | Missing `design` mode |
| Phase 3 Execution | ❌ Incomplete | `/fix`, `/release` not documented |
| `/commit` | ⚠️ Truncated | Line 84 cuts off mid-section |
| Full Walkthrough | ❌ Missing | No literate commands walkthrough |

### `design.md` - NEEDS UPDATE
| Section | Status | Notes |
|---------|--------|-------|
| Primary Agents | ❌ Incomplete | Missing `design` mode column |
| Subagents | ❌ Incomplete | Missing `lit-commands` subagent |
| Commands Table | ❌ Incomplete | Missing `/sandbox`, `/commit` |
| Sandbox Plugin | ❌ Missing | New feature not documented |
| Literate Commands | ❌ Missing | New feature not documented |

### `develop.md` - OK
No significant changes needed.

### `deploy.md` - OK
Already reflects current architecture.

### `updating.md` - OK
Already references v2.0.0.

## Required Updates

### High Priority
1. Add `design` mode to agent architecture tables
2. Document `/sandbox` command
3. Document literate commands concept
4. Fix truncated `/commit` section in user-guide.md
5. Add sandbox to Key Capabilities in index.md

### Medium Priority
1. Add literate commands to design.md architecture section
2. Document sandbox plugin in design.md
3. Add walkthrough for literate commands workflow

### Low Priority
1. Update prerequisites if sandbox has new requirements (Docker)

## Estimated Effort
- **High Priority**: ~1-2 hours
- **Medium Priority**: ~2-3 hours
- **Low Priority**: ~1 hour

## Notes
- `lib/opencode-literate-commands/` submodule contains literate-commands implementation
- `.opencode/plugins/sandbox.js` contains sandbox implementation
- Need to verify if Docker is required for sandbox (check prerequisites)
