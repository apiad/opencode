---
id: ai-agent-friendly-cli-patterns
created: 2026-03-28
modified: 2026-03-28
type: research
status: active
tags: [cli, ai-agents, tool-design, mcp, self-discovery]
---

# Research: What Makes a CLI "AI-Agent-Friendly"?

## Overview

This research investigates patterns and principles that make CLI tools easily navigable by AI agents. Key sources include the GitHub CLI's `AGENTS.md`, the Model Context Protocol (MCP) specification, and established conventions for structured output and error handling.

## Key Principles for AI-Agent-Friendly CLIs

### 1. Provide Structured, Machine-Readable Output

**JSON Output Flags**
- Offer `--json` or `--format json` flags for structured data output
- Include `--jq` and `--template` flags for data manipulation (as GitHub CLI does)
- Output should be valid, parseable JSON that preserves type information

**Structured Content Patterns (from MCP)**
```json
{
  "type": "text",
  "text": "Tool result text"
}
// or for structured data:
{
  "type": "structured",
  "structuredContent": { ... }
}
```

### 2. Create an `AGENTS.md` or Developer Guide

GitHub CLI pioneered this pattern with their [`AGENTS.md`](https://github.com/cli/cli/blob/trunk/AGENTS.md) file. This file should include:

- **Architecture overview**: Entry points, key packages, command structure
- **Build/test instructions**: Commands for development and validation
- **Command patterns**: How commands are structured (`$ gh foo bar`)
- **Error types**: Specific error codes and what they mean
- **Testing patterns**: How to test changes

**Example structure from GitHub CLI:**
```markdown
# AGENTS.md

This is [tool-name], a command-line tool for [purpose].

## Build, Test, and Lint
\`\`\`bash
make              # Build
go test ./...     # Tests
\`\`\`

## Architecture
Entry point: `cmd/...`

## Error Handling
- `FlagErrorf(...)` — flag validation errors
- `SilentError` — exit 1, no message
- `CancelError` — user cancelled
- `NoResultsError` — empty results
```

### 3. Design Structured Error Messages

**Error Type Hierarchy (GitHub CLI pattern):**
```go
// Flag errors - show usage
FlagErrorf("invalid flag: %s", flag)

// Silent errors - exit 1 without message
var SilentError = errors.New("SilentError")

// Cancellation - user-initiated
var CancelError = errors.New("CancelError")

// No results - graceful empty state
type NoResultsError struct { message string }
```

**AI-friendly error messages should:**
- Be parseable and categorized
- Include error codes that map to specific failure modes
- Provide actionable information
- Distinguish between recoverable and fatal errors

### 4. Implement Consistent Exit Codes (POSIX Convention)

**Standard Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse/shell conflict |
| 126 | Command not executable |
| 127 | Command not found |
| 128+N | Terminated by signal N |

**Extended codes (BSD/sendmail convention):**
| Code | Meaning |
|------|---------|
| 64 | Usage error |
| 65 | Data format error |
| 66 | Cannot open input |
| 69 | Service unavailable |
| 70 | Internal software error |
| 78 | Configuration error |

### 5. Provide Self-Discovery Mechanisms

**Built-in Help That Scales**
- `--help` or `-h` for basic usage
- `--help --verbose` or `man` pages for detailed docs
- `--examples` flag showing common usage patterns
- `--tour` or interactive tutorials for complex tools

**Discovery via Structured Output:**
```bash
# List all available commands
$ tool --list --format json
$ tool --list-commands --json

# Show command schema
$ tool <subcommand> --help --json
```

### 6. Define Tool Schemas (MCP Pattern)

For tools that will be used via MCP or similar protocols:

```json
{
  "name": "get_weather",
  "title": "Weather Information Provider",
  "description": "Get current weather information for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code"
      }
    },
    "required": ["location"]
  }
}
```

### 7. Support Output Annotations

Include metadata that helps AI agents prioritize and route information:

```json
{
  "annotations": {
    "audience": ["user", "assistant"],
    "priority": 0.8,
    "lastModified": "2025-01-12T15:00:58Z"
  }
}
```

### 8. Design for Idempotency and Safety

**For AI agents that may retry commands:**
- Make operations idempotent where possible
- Provide `--dry-run` or `--preview` flags
- Support `--force` for intentional overwrites
- Use `--yes` or `-y` for non-interactive confirmation

### 9. Document Command Hierarchy Clearly

**Consistent Command Structure:**
```
tool                          # Root - overview, auth
tool <entity>                 # Entity commands
tool <entity> list            # List entities
tool <entity> get <id>        # Get specific entity
tool <entity> create          # Create new entity
tool <entity> update <id>    # Update entity
tool <entity> delete <id>     # Delete entity
```

### 10. Support Progressive Disclosure

**Verbose vs. Compact Output:**
```bash
$ tool --quiet          # Minimal output
$ tool                  # Normal output
$ tool --verbose        # Detailed output
$ tool --debug          # Debug information
```

## Resources and References

- [GitHub CLI AGENTS.md](https://github.com/cli/cli/blob/trunk/AGENTS.md) — Pioneer of AI-agent documentation
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — Standard for AI-tool integration
- [POSIX Exit Codes](https://pubs.opengroup.org/onlinepubs/9699919799/) — Unix exit status conventions
- [sysexits.h](https://www.freebsd.org/cgi/man.cgi?query=sysexits) — BSD exit code conventions

## Patterns to Avoid

1. **Unstructured error messages** — "Something went wrong" provides no actionable info
2. **Inconsistent exit codes** — Same error condition returning different codes
3. **No JSON output option** — Requiring text parsing for automation
4. **Hidden functionality** — Features only discoverable by reading source
5. **Non-idempotent operations** — `create` creates duplicates instead of failing gracefully
6. **Blocking interactive prompts** — No way to run headless in CI/automation

## Implementation Checklist

- [ ] Add `--json` output flag to all list/display commands
- [ ] Create `AGENTS.md` with architecture and patterns
- [ ] Define and document error codes
- [ ] Use POSIX exit code conventions (0=success, non-zero=failure)
- [ ] Add `--dry-run`/`--preview` flags for destructive operations
- [ ] Include `--list` or `--help` output suitable for programmatic parsing
- [ ] Add examples to all command help text
- [ ] Consider MCP server implementation for AI integration

---

*Research completed: 2026-03-28*
*Primary sources: GitHub CLI AGENTS.md, MCP Specification, POSIX Standards*
