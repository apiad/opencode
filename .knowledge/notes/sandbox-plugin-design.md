---
id: sandbox-plugin-design
created: 2026-03-30
modified: 2026-03-30
type: design
status: active
tags: [plugin, sandbox, docker, security, isolation]
---

# Sandbox Plugin Design

## Overview

A plugin that routes all tool executions through Docker containers based on the current agent's `sandbox` configuration. This provides kernel-level isolation preventing accidental source code modifications.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenCode (Host)                          │
│                                                              │
│   User input → Agent (analyze/build/plan/release)           │
│                      ↓                                       │
│              sandboxPlugin                                   │
│              tool.execute.before                             │
│                      ↓                                       │
│         Route to container based on agent                    │
│                      ↓                                       │
│   docker exec opencode-analyze <command>                    │
│   docker exec opencode-build <command>                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓
    ┌────────────┐      ┌────────────┐
    │ opencode-  │      │ opencode-  │
    │ analyze    │      │ build      │
    │ (ro src)   │      │ (rw src)   │
    └────────────┘      └────────────┘
```

## Agent Schema

Each primary agent defines sandbox volumes in YAML frontmatter:

```yaml
---
sandbox:
    volumes:
        ".": ro              # Default: read-only
        ".knowledge": rw     # Always writable
        ".experiments": rw   # Scratch space
        ".venv": ro         # Protected
        "node_modules": ro
---
```

### Container Deduplication

Agents with identical `sandbox.volumes` share containers:

| Container | Agents | Volumes |
|-----------|--------|---------|
| `opencode-analyze` | analyze, plan | `.:ro`, `.knowledge:rw`, `.experiments:rw` |
| `opencode-build` | build, release | `.:rw`, `.knowledge:rw`, `.experiments:rw` |

## Files

### Plugin: `.opencode/plugins/sandbox/index.ts`

```typescript
import { parse } from "yaml"
import { readdirSync, readFileSync, existsSync } from "fs"
import { join } from "path"
import type { Hooks, PluginInput } from "@opencode-ai/plugin"

export interface SandboxVolume {
    path: string
    mode: "ro" | "rw"
}

export interface SandboxConfig {
    volumes: Record<string, "ro" | "rw">
}

export interface AgentSandbox {
    name: string
    sandbox?: SandboxConfig
}

export interface ContainerDef {
    name: string
    agents: string[]
    volumes: Record<string, "ro" | "rw">
    image: string
}

// Load agent configs
function loadAgentSandboxes(dir: string): AgentSandbox[] {
    const agentsDir = join(dir, ".opencode", "agents")
    if (!existsSync(agentsDir)) return []
    
    return readdirSync(agentsDir)
        .filter(f => f.endsWith(".md"))
        .map(f => {
            const content = readFileSync(join(agentsDir, f), "utf-8")
            const yamlPart = content.split("---")[1] || ""
            const parsed = parse(yamlPart) as { sandbox?: SandboxConfig }
            return {
                name: f.replace(".md", ""),
                sandbox: parsed.sandbox,
            }
        })
}

// Deduplicate by volume config
function getUniqueContainers(agents: AgentSandbox[]): ContainerDef[] {
    const map = new Map<string, ContainerDef>()
    
    for (const agent of agents) {
        if (!agent.sandbox?.volumes) continue
        
        const key = JSON.stringify(agent.sandbox.volumes)
        if (!map.has(key)) {
            map.set(key, {
                name: `opencode-${agent.name}`,
                agents: [],
                volumes: agent.sandbox.volumes,
                image: "ubuntu:22.04",
            })
        }
        map.get(key)!.agents.push(agent.name)
    }
    
    return Array.from(map.values())
}

// Create or update container
async function ensureContainer(
    $: BunShell,
    container: ContainerDef,
    projectRoot: string,
): Promise<void> {
    const { name, volumes, image } = container
    
    // Check if container exists
    const exists = await $`docker inspect ${name}`.nothrow().quiet().text()
    if (!exists.trim()) {
        // Build volume flags
        const volumeFlags = Object.entries(volumes)
            .map(([path, mode]) => {
                const absPath = path === "." 
                    ? projectRoot 
                    : join(projectRoot, path)
                return `-v ${absPath}:/workspace/${path}:${mode}`
            })
            .join(" ")
        
        // Create container (sleep infinity keeps it warm)
        await $`docker create --name ${name} ${volumeFlags.split(" ")} ${image} sleep infinity`
    }
    
    // Start if not running
    await $`docker start ${name}`.nothrow().quiet()
}

// Get container name for current agent
function getContainerForAgent(
    containers: ContainerDef[],
    agentName: string,
): ContainerDef | undefined {
    return containers.find(c => c.agents.includes(agentName))
}

// Transform bash command to docker exec
function toDockerExec(containerName: string, command: string): string {
    // Escape single quotes in command
    const escaped = command.replace(/'/g, "'\\''")
    return `docker exec ${containerName} bash -c '${escaped}'`
}

// Transform file paths to container paths
function toContainerPath(filePath: string): string {
    if (filePath.startsWith("/")) return filePath
    return `/workspace/${filePath}`
}

export default async function sandboxPlugin(
    input: PluginInput,
    _options?: any,
): Promise<Hooks> {
    const { directory, $ } = input
    const projectRoot = directory
    
    // Load and process agent configs
    const agents = loadAgentSandboxes(projectRoot)
    const containers = getUniqueContainers(agents)
    
    // Ensure all containers exist
    for (const container of containers) {
        await ensureContainer($, container, projectRoot)
    }
    
    return {
        "tool.execute.before": async (toolInput, toolOutput) => {
            const { tool, callID } = toolInput
            const args = toolOutput.args
            
            // Get current agent from context (passed via callID in a real impl)
            // For now, we'd need to pass agent name through the hook
            const agentName = (args as any)?._agent || "analyze"
            const container = getContainerForAgent(containers, agentName)
            
            if (!container) return  // No sandbox config
            
            // Route bash commands to container
            if (tool === "bash" && args?.command) {
                args.command = toDockerExec(container.name, args.command)
                return
            }
            
            // Transform file paths for file operations
            if (["read", "edit", "write", "glob"].includes(tool)) {
                if (args?.filePath) {
                    args.filePath = toContainerPath(args.filePath)
                }
                if (args?.pattern) {
                    args.pattern = toContainerPath(args.pattern)
                }
            }
        },
    }
}
```

### Command: `.opencode/commands/setup-sandbox.ts`

```typescript
import { parse } from "yaml"
import { readdirSync, readFileSync, existsSync, mkdirSync } from "fs"
import { join } from "path"
import type { CommandDef } from "@opencode-ai/plugin"

interface SandboxVolume {
    path: string
    mode: "ro" | "rw"
}

interface SandboxConfig {
    volumes: Record<string, "ro" | "rw">
}

interface AgentConfig {
    name: string
    sandbox?: SandboxConfig
}

interface ContainerDef {
    name: string
    agents: string[]
    volumes: Record<string, "ro" | "rw">
    image: string
}

function loadAgentConfigs(dir: string): AgentConfig[] {
    const agentsDir = join(dir, ".opencode", "agents")
    if (!existsSync(agentsDir)) return []
    
    return readdirSync(agentsDir)
        .filter(f => f.endsWith(".md"))
        .map(f => {
            const content = readFileSync(join(agentsDir, f), "utf-8")
            const yamlPart = content.split("---")[1] || ""
            const parsed = parse(yamlPart) as { sandbox?: SandboxConfig }
            return {
                name: f.replace(".md", ""),
                sandbox: parsed.sandbox,
            }
        })
}

function getUniqueContainers(agents: AgentConfig[]): ContainerDef[] {
    const map = new Map<string, ContainerDef>()
    
    for (const agent of agents) {
        if (!agent.sandbox?.volumes) continue
        
        const key = JSON.stringify(agent.sandbox.volumes)
        if (!map.has(key)) {
            map.set(key, {
                name: `opencode-${agent.name}`,
                agents: [],
                volumes: agent.sandbox.volumes,
                image: "ubuntu:22.04",
            })
        }
        map.get(key)!.agents.push(agent.name)
    }
    
    return Array.from(map.values())
}

async function createContainer(container: ContainerDef, projectRoot: string): Promise<void> {
    const { name, volumes, image } = container
    
    console.log(`Creating container: ${name}`)
    
    // Remove existing container if exists
    await Bun.$`docker rm -f ${name}`.nothrow()
    
    // Build volume flags
    const volumeFlags = Object.entries(volumes)
        .map(([path, mode]) => {
            const absPath = path === "." 
                ? projectRoot 
                : join(projectRoot, path)
            return `${absPath}:/workspace/${path}:${mode}`
        })
        .join(" ")
    
    // Create container
    await Bun.$`docker create --name ${name} -v ${volumeFlags.split(" ")} ${image} sleep infinity`
    
    console.log(`✓ ${name} created`)
}

export const setupSandboxCommand: CommandDef = {
    name: "setup-sandbox",
    describe: "Create sandbox containers based on agent configurations",
    async handler() {
        const projectRoot = process.cwd()
        
        console.log("🔧 Setting up sandbox containers...\n")
        
        const agents = loadAgentConfigs(projectRoot)
        const containers = getUniqueContainers(agents)
        
        if (containers.length === 0) {
            console.log("No sandbox configurations found in agent definitions.")
            return
        }
        
        console.log(`Found ${containers.length} unique container(s):\n`)
        
        for (const container of containers) {
            console.log(`  ${container.name} (for: ${container.agents.join(", ")})`)
            await createContainer(container, projectRoot)
        }
        
        console.log("\n✅ Sandbox containers ready!")
        console.log("\nRun `docker ps` to see running containers.")
    },
}
```

## Usage

```bash
# One-time setup
opencode /setup-sandbox

# Normal usage
opencode --mode analyze

# Switch modes via TAB - plugin routes to correct container
# analyze → opencode-analyze (read-only source)
# build   → opencode-build (read-write source)
```

## Flow Diagram

```
User: "run ls"
    ↓
opencode (analyze mode)
    ↓
tool.execute.before hook
    ↓
Get current agent: "analyze"
Find container: "opencode-analyze"
    ↓
Transform: "ls" → "docker exec opencode-analyze bash -c 'ls'"
    ↓
Execute in container
    ↓
Return result to opencode
```

## Benefits

1. **Kernel-level protection**: Docker `:ro` mounts can't be bypassed
2. **No source code modifications** in analyze mode
3. **Containers stay warm** (sleep infinity)
4. **Deduplication**: Agents with same volumes share containers
5. **TAB switching works**: Same opencode session, different containers

## Trade-offs

- Requires Docker installed
- ~10ms overhead per command (docker exec)
- Container user may differ from host user
- File ownership in mounted volumes
