---
id: opencode-sdk-plugin-research
created: 2026-03-29
modified: 2026-03-29
type: research
status: active
tags: [opencode, sdk, plugin, typescript, api]
sources:
  - https://github.com/anomalyco/opencode/tree/dev/packages/sdk
  - https://github.com/anomalyco/opencode/tree/dev/packages/plugin
---

# OpenCode SDK & Plugin Package Research

## Repository
**URL**: https://github.com/anomalyco/opencode (branch: `dev`)
**132k stars, 14k forks** — The open source AI coding agent.

---

## Package Structure

### SDK (`packages/sdk/js`)
The SDK is a **client/server architecture** for interacting with OpenCode programmatically.

**Source**: `packages/sdk/js/src/`
- `index.ts` — Main entry point, exports `createOpencode()`, `createOpencodeClient()`, `createOpencodeServer()`
- `client.ts` — Client factory with directory header rewriting
- `server.ts` — Server implementation (auto-starts on port 4096)
- `gen/` — Auto-generated from OpenAPI spec (`@hey-api/openapi-ts`)
- `v2/` — Second version of the SDK client/server
- `example/example.ts` — Usage example

**SDK Package**: `@opencode-ai/sdk` (published on npm)

### Plugin (`packages/plugin`)
Defines the plugin interface for extending OpenCode's functionality.

**Source**: `packages/plugin/src/`
- `index.ts` — Main Plugin type + Hooks interface
- `tool.ts` — Tool definition helper (Zod-based)
- `tui.ts` — TUI plugin types (separate TuiPlugin interface)
- `shell.ts` — BunShell interface for shell operations
- `example.ts` — Example plugin implementation

**Plugin Package**: `@opencode-ai/plugin`

---

## Plugin Interface

### Server Plugin Type

```typescript
// packages/plugin/src/index.ts
export type PluginInput = {
  client: ReturnType<typeof createOpencodeClient>
  project: Project
  directory: string
  worktree: string
  serverUrl: URL
  $: BunShell
}

export type PluginOptions = Record<string, unknown>

export type Config = Omit<SDKConfig, "plugin"> & {
  plugin?: Array<string | [string, PluginOptions]>
}

export type Plugin = (input: PluginInput, options?: PluginOptions) => Promise<Hooks>

export type PluginModule = {
  id?: string
  server: Plugin
  tui?: never
}
```

### TUI Plugin Type (Separate from Server Plugin)

```typescript
// packages/plugin/src/tui.ts
export type TuiPlugin = (
  api: TuiPluginApi, 
  options: PluginOptions | undefined, 
  meta: TuiPluginMeta
) => Promise<void>

export type TuiPluginModule = {
  id?: string
  tui: TuiPlugin
  server?: never
}
```

---

## Hooks System

The `Hooks` interface defines all available lifecycle hooks:

```typescript
// packages/plugin/src/index.ts
export interface Hooks {
  // Core hooks
  event?: (input: { event: Event }) => Promise<void>
  config?: (input: Config) => Promise<void>
  
  // Tool registration
  tool?: {
    [key: string]: ToolDefinition
  }
  
  // Authentication
  auth?: AuthHook
  
  // Chat hooks
  "chat.message"?: (
    input: {
      sessionID: string
      agent?: string
      model?: { providerID: string; modelID: string }
      messageID?: string
      variant?: string
    },
    output: { message: UserMessage; parts: Part[] },
  ) => Promise<void>
  
  "chat.params"?: (
    input: { sessionID: string; agent: string; model: Model; provider: ProviderContext; message: UserMessage },
    output: { temperature: number; topP: number; topK: number; options: Record<string, any> },
  ) => Promise<void>
  
  "chat.headers"?: (
    input: { sessionID: string; agent: string; model: Model; provider: ProviderContext; message: UserMessage },
    output: { headers: Record<string, string> },
  ) => Promise<void>
  
  // Permission hooks
  "permission.ask"?: (input: Permission, output: { status: "ask" | "deny" | "allow" }) => Promise<void>
  
  // Command hooks
  "command.execute.before"?: (
    input: { command: string; sessionID: string; arguments: string },
    output: { parts: Part[] },
  ) => Promise<void>
  
  // Tool hooks
  "tool.execute.before"?: (
    input: { tool: string; sessionID: string; callID: string },
    output: { args: any },
  ) => Promise<void>
  
  "tool.execute.after"?: (
    input: { tool: string; sessionID: string; callID: string; args: any },
    output: {
      title: string
      output: string
      metadata: any
    },
  ) => Promise<void>
  
  "tool.definition"?: (input: { toolID: string }, output: { description: string; parameters: any }) => Promise<void>
  
  // Shell hooks
  "shell.env"?: (
    input: { cwd: string; sessionID?: string; callID?: string },
    output: { env: Record<string, string> },
  ) => Promise<void>
  
  // Experimental hooks
  "experimental.chat.messages.transform"?: (
    input: {},
    output: {
      messages: { info: Message; parts: Part[] }[]
    },
  ) => Promise<void>
  
  "experimental.chat.system.transform"?: (
    input: { sessionID?: string; model: Model },
    output: { system: string[] },
  ) => Promise<void>
  
  "experimental.session.compacting"?: (
    input: { sessionID: string },
    output: { context: string[]; prompt?: string },
  ) => Promise<void>
  
  "experimental.text.complete"?: (
    input: { sessionID: string; messageID: string; partID: string },
    output: { text: string },
  ) => Promise<void>
}
```

### Hook Summary Table

| Hook Name | Input | Output | Purpose |
|-----------|-------|--------|---------|
| `event` | `{ event: Event }` | void | General event handling |
| `config` | `Config` | void | Config modification |
| `tool` | — | `ToolDefinition[]` | Register custom tools |
| `auth` | — | `AuthHook` | Custom authentication |
| `chat.message` | `{ sessionID, agent, model, ... }` | `{ message, parts }` | Modify incoming messages |
| `chat.params` | `{ sessionID, agent, model, ... }` | `{ temperature, topP, topK, options }` | Modify LLM params |
| `chat.headers` | `{ sessionID, agent, model, ... }` | `{ headers }` | Add request headers |
| `permission.ask` | `Permission` | `{ status }` | Control permissions |
| `command.execute.before` | `{ command, sessionID, arguments }` | `{ parts }` | Modify command parts |
| `tool.execute.before` | `{ tool, sessionID, callID }` | `{ args }` | Modify tool args |
| `tool.execute.after` | `{ tool, sessionID, callID, args }` | `{ title, output, metadata }` | Modify tool output |
| `tool.definition` | `{ toolID }` | `{ description, parameters }` | Modify tool schema |
| `shell.env` | `{ cwd, sessionID, callID }` | `{ env }` | Add/modify env vars |
| `experimental.chat.messages.transform` | `{}` | `{ messages }` | Transform all messages |
| `experimental.chat.system.transform` | `{ sessionID, model }` | `{ system }` | Modify system prompt |
| `experimental.session.compacting` | `{ sessionID }` | `{ context, prompt }` | Customize compaction |
| `experimental.text.complete` | `{ sessionID, messageID, partID }` | `{ text }` | Transform completed text |

---

## Tool Definition

```typescript
// packages/plugin/src/tool.ts
export type ToolContext = {
  sessionID: string
  messageID: string
  agent: string
  directory: string      // Current project directory
  worktree: string      // Project worktree root
  abort: AbortSignal
  metadata(input: { title?: string; metadata?: { [key: string]: any } }): void
  ask(input: AskInput): Promise<void>
}

type AskInput = {
  permission: string
  patterns: string[]
  always: string[]
  metadata: { [key: string]: any }
}

export function tool<Args extends z.ZodRawShape>(input: {
  description: string
  args: Args
  execute(args: z.infer<z.ZodObject<Args>>, context: ToolContext): Promise<string>
}) {
  return input
}
tool.schema = z

export type ToolDefinition = ReturnType<typeof tool>
```

---

## Key SDK Types

### Message Types

```typescript
// packages/sdk/js/src/gen/types.gen.ts

export type UserMessage = {
  id: string
  sessionID: string
  role: "user"
  time: { created: number }
  summary?: { title?: string; body?: string; diffs: Array<FileDiff> }
  agent: string
  model: { providerID: string; modelID: string }
  system?: string
  tools?: { [key: string]: boolean }
}

export type AssistantMessage = {
  id: string
  sessionID: string
  role: "assistant"
  time: { created: number; completed?: number }
  error?: ProviderAuthError | UnknownError | MessageOutputLengthError | MessageAbortedError | ApiError
  parentID: string
  modelID: string
  providerID: string
  mode: string
  path: { cwd: string; root: string }
  summary?: boolean
  cost: number
  tokens: { input: number; output: number; reasoning: number; cache: { read: number; write: number } }
  finish?: string
}

export type Message = UserMessage | AssistantMessage
```

### Part Types

```typescript
export type Part = 
  | TextPart          // type: "text"
  | ReasoningPart      // type: "reasoning"
  | FilePart          // type: "file"
  | ToolPart          // type: "tool"
  | StepStartPart     // type: "step-start"
  | StepFinishPart    // type: "step-finish"
  | SnapshotPart      // type: "snapshot"
  | PatchPart         // type: "patch"
  | AgentPart         // type: "agent"
  | RetryPart         // type: "retry"
  | CompactionPart    // type: "compaction"
  | { type: "subtask", prompt, description, agent }  // inline subtask

// Key part structures:
export type TextPart = {
  id: string; sessionID: string; messageID: string
  type: "text"; text: string
  synthetic?: boolean; ignored?: boolean
  time?: { start: number; end?: number }
  metadata?: { [key: string]: unknown }
}

export type ToolPart = {
  id: string; sessionID: string; messageID: string
  type: "tool"; callID: string; tool: string
  state: ToolStatePending | ToolStateRunning | ToolStateCompleted | ToolStateError
  metadata?: { [key: string]: unknown }
}

export type ToolStateCompleted = {
  status: "completed"
  input: { [key: string]: unknown }
  output: string
  title: string
  metadata: { [key: string]: unknown }
  time: { start: number; end: number; compacted?: number }
  attachments?: Array<FilePart>
}
```

### Session Type

```typescript
export type Session = {
  id: string
  projectID: string
  directory: string
  parentID?: string
  summary?: {
    additions: number; deletions: number; files: number
    diffs?: Array<FileDiff>
  }
  share?: { url: string }
  title: string
  version: string
  time: { created: number; updated: number; compacting?: number }
  revert?: { messageID: string; partID?: string; snapshot?: string; diff?: string }
}
```

### Project Type

```typescript
export type Project = {
  id: string
  worktree: string
  vcsDir?: string
  vcs?: "git"
  time: { created: number; initialized?: number }
}
```

### Model & Provider Types

```typescript
export type Model = {
  id: string
  providerID: string
  api: { id: string; url: string; npm: string }
  name: string
  capabilities: {
    temperature: boolean; reasoning: boolean; attachment: boolean; toolcall: boolean
    input: { text: boolean; audio: boolean; image: boolean; video: boolean; pdf: boolean }
    output: { text: boolean; audio: boolean; image: boolean; video: boolean; pdf: boolean }
  }
  cost: { input: number; output: number; cache: { read: number; write: number } }
  limit: { context: number; output: number }
  status: "alpha" | "beta" | "deprecated" | "active"
  options: { [key: string]: unknown }
  headers: { [key: string]: string }
}

export type Provider = {
  id: string; name: string
  source: "env" | "config" | "custom" | "api"
  env: Array<string>; key?: string
  options: { [key: string]: unknown }
  models: { [key: string]: Model }
}
```

### Permission Type

```typescript
export type Permission = {
  id: string; type: string
  pattern?: string | Array<string>
  sessionID: string; messageID: string; callID?: string
  title: string
  metadata: { [key: string]: unknown }
  time: { created: number }
}
```

### Event Types

```typescript
export type Event = 
  | EventServerInstanceDisposed
  | EventInstallationUpdated
  | EventInstallationUpdateAvailable
  | EventLspClientDiagnostics
  | EventLspUpdated
  | EventMessageUpdated
  | EventMessageRemoved
  | EventMessagePartUpdated
  | EventMessagePartRemoved
  | EventPermissionUpdated
  | EventPermissionReplied
  | EventSessionStatus
  | EventSessionIdle
  | EventSessionCompacted
  | EventFileEdited
  | EventTodoUpdated
  | EventCommandExecuted
  | EventSessionCreated
  | EventSessionUpdated
  | EventSessionDeleted
  | EventSessionDiff
  | EventSessionError
  | EventFileWatcherUpdated
  | EventVcsBranchUpdated
  | EventTuiPromptAppend
  | EventTuiCommandExecute
  | EventTuiToastShow
  | EventPtyCreated
  | EventPtyUpdated
  | EventPtyExited
  | EventPtyDeleted
  | EventServerConnected
```

---

## Example Plugin

```typescript
// packages/plugin/src/example.ts
import { Plugin, tool } from "./index.js"

export const ExamplePlugin: Plugin = async (ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string().describe("foo"),
        },
        async execute(args) {
          return `Hello ${args.foo}!`
        },
      }),
    },
  }
}
```

---

## Example SDK Usage

```typescript
// packages/sdk/js/example/example.ts
import { createOpencodeClient, createOpencodeServer } from "@opencode-ai/sdk"
import { pathToFileURL } from "bun"

const server = await createOpencodeServer()
const client = createOpencodeClient({ baseUrl: server.url })

// Create a new session
const session = await client.session.create()

// Send a prompt with files
await client.session.prompt({
  path: { id: session.data.id },
  body: {
    parts: [
      {
        type: "file",
        mime: "text/plain",
        url: pathToFileURL("file.ts").href,
      },
      {
        type: "text",
        text: "Write tests for this file.",
      },
    ],
  },
})

// List sessions
const sessions = await client.session.list()

// Get session messages
const messages = await client.session.messages({
  path: { id: sessionId },
})

// Subscribe to events
for await (const event of client.global.event()) {
  console.log(event)
}
```

---

## SDK Client API Methods

The `OpencodeClient` class provides:

```typescript
// Generated from OpenAPI - packages/sdk/js/src/gen/sdk.gen.ts
class OpencodeClient {
  global: Global        // Event subscriptions
  project: Project      // Project management
  pty: Pty             // PTY session management
  config: Config        // Config get/update
  tool: Tool            // Tool listing
  instance: Instance    // Instance disposal
  path: Path            // Path info
  vcs: Vcs              // VCS info
  session: Session      // Session CRUD + operations
  command: Command      // Command listing
  provider: Provider    // Provider management + OAuth
  find: Find            // Search (text, files, symbols)
  file: File            // File operations
  app: App              // App logging + agents
  mcp: Mcp              // MCP server management
  lsp: Lsp              // LSP status
  formatter: Formatter  // Formatter status
  tui: Tui              // TUI control
  auth: Auth            // Auth management
  event: Event          // Event subscriptions
}
```

### Session API (Most Important)

```typescript
session.list()                    // List all sessions
session.create()                  // Create new session
session.get({ path: { id } })     // Get session details
session.delete({ path: { id } })  // Delete session
session.status({ path: { id } })  // Get status (idle/busy/retry)
session.messages({ path: { id } }) // List messages
session.prompt({ path, body })    // Send message
session.promptAsync({ path, body }) // Send message (non-blocking)
session.command({ path, body })   // Send command
session.shell({ path, body })     // Run shell command
session.diff({ path: { id } })     // Get session diff
session.summarize({ path, body }) // Summarize session
session.abort({ path: { id } })   // Abort session
session.fork({ path, body })      // Fork session
session.revert({ path, body })    // Revert message
session.share({ path: { id } })   // Share session
session.unshare({ path: { id } }) // Unshare session
session.compact()                 // Compact session
```

---

## TUI Plugin API

The `TuiPluginApi` provides rich UI integration:

```typescript
// packages/plugin/src/tui.ts
export type TuiPluginApi = {
  app: TuiApp
  command: {
    register: (cb: () => TuiCommand[]) => () => void
    trigger: (value: string) => void
  }
  route: {
    register: (routes: TuiRouteDefinition[]) => () => void
    navigate: (name: string, params?: Record<string, unknown>) => void
    readonly current: TuiRouteCurrent
  }
  ui: {
    Dialog, DialogAlert, DialogConfirm, DialogPrompt, DialogSelect
    Prompt, toast, dialog
  }
  keybind: { match, print, create }
  state: TuiState  // Config, provider, session state
  theme: TuiTheme
  client: OpencodeClient
  scopedClient: (workspaceID?: string) => OpencodeClient
  workspace: TuiWorkspace
  event: TuiEventBus
  renderer: CliRenderer
  slots: TuiSlots  // UI extension points
  plugins: {
    list, activate, deactivate, add, install
  }
  lifecycle: TuiLifecycle
}
```

---

## Shell Interface

```typescript
// packages/plugin/src/shell.ts
export interface BunShell {
  (strings: TemplateStringsArray, ...expressions: ShellExpression[]): BunShellPromise
  braces(pattern: string): string[]
  escape(input: string): string
  env(newEnv?: Record<string, string | undefined>): BunShell
  cwd(newCwd?: string): BunShell
  nothrow(): BunShell
  throws(shouldThrow: boolean): BunShell
}

export interface BunShellPromise extends Promise<BunShellOutput> {
  stdin: WritableStream
  cwd(newCwd: string): this
  env(newEnv: Record<string, string>): this
  quiet(): this
  lines(): AsyncIterable<string>
  text(encoding?: BufferEncoding): Promise<string>
  json(): Promise<any>
  arrayBuffer(): Promise<ArrayBuffer>
  blob(): Promise<Blob>
  nothrow(): this
  throws(shouldThrow: boolean): this
}
```

---

## File Links

### Plugin Package
- Main entry: https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts
- Tool definition: https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tool.ts
- TUI types: https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tui.ts
- Shell interface: https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/shell.ts
- Example: https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/example.ts

### SDK Package
- Main entry: https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/index.ts
- Client: https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/client.ts
- Types (auto-generated): https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts
- SDK client class: https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/sdk.gen.ts
- Example: https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/example/example.ts

---

## Additional Notes

1. **Plugin vs TUI Plugin**: There are TWO separate plugin types:
   - `Plugin` (server) — For server-side functionality (tools, hooks, auth)
   - `TuiPlugin` (client) — For TUI/UI extensions

2. **OpenAPI-generated**: The SDK is auto-generated from an OpenAPI spec using `@hey-api/openapi-ts`

3. **Bun Runtime**: Plugins run on Bun runtime (uses `BunShell` for shell operations)

4. **Zod for validation**: Tools use Zod schemas for argument validation

5. **Experimental hooks**: Many powerful hooks are marked experimental and may change
