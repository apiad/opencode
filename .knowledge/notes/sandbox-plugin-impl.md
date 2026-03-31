---
id: sandbox-plugin-impl
created: 2026-03-30
modified: 2026-03-30
type: implementation
status: active
tags: [plugin, sandbox, docker, tool]
---

# Sandbox Plugin Implementation

## Files to Create

```
.opencode/
├── plugins/
│   └── sandbox/
│       └── index.js       # The plugin
├── commands/
│   └── setup-env.md      # The markdown command
└── agents/
    └── analyze.md         # Add sandbox: config
```

## 1. Plugin: `.opencode/plugins/sandbox/index.js`

```javascript
import { readFileSync, existsSync } from "fs"
import { join } from "path"
import { tool } from "@opencode-ai/plugin"

// Current agent (set by chat.message hook)
let currentAgent = "analyze"

function getEnvImagePath(directory) {
    return join(directory, ".env-image")
}

function readEnvImage(directory) {
    const path = getEnvImagePath(directory)
    if (!existsSync(path)) {
        return null
    }
    return readFileSync(path, "utf-8").trim()
}

function getVolumeConfig(agent) {
    // Based on agent's sandbox config in YAML
    if (agent === "build" || agent === "release") {
        return {
            source: ".:rw",
            ".knowledge": "rw",
            ".experiments": "rw",
        }
    }
    // analyze, plan, etc - read-only source
    return {
        source: ".:ro",
        ".knowledge": "rw",
        ".experiments": "rw",
    }
}

function buildDockerCommand(directory, image, agent, command) {
    const volumes = getVolumeConfig(agent)
    const volumeFlags = []
    
    for (const [path, mode] of Object.entries(volumes)) {
        const absPath = path === "." 
            ? directory 
            : join(directory, path)
        volumeFlags.push("-v", `${absPath}:/workspace/${path}:${mode}`)
    }
    
    // Escape command for shell
    const escaped = command.replace(/'/g, "'\\''")
    
    // Build docker run command
    // -i: interactive, -t: pseudo-TTY, -w: working dir
    return [
        "docker", "run", "--rm", "-i",
        ...volumeFlags,
        "-w", "/workspace",
        image,
        "bash", "-c", `'${escaped}'`
    ].join(" ")
}

export const SandboxPlugin = async ({ directory, $ }) => {
    const image = readEnvImage(directory)
    
    if (!image) {
        console.log("[sandbox] No .env-image found. Run /setup-env first.")
    } else {
        console.log(`[sandbox] Using image: ${image}`)
    }
    
    return {
        // Track current agent from messages
        "chat.message": async (input, output) => {
            if (input.agent) {
                currentAgent = input.agent
            }
        },
        
        // Custom bash tool that runs in docker
        tool: {
            bash: tool({
                description: "Execute a bash command in the sandboxed environment",
                args: {
                    command: tool.schema.string(),
                },
                async execute(args, context) {
                    const { directory: dir } = context
                    
                    if (!image) {
                        return {
                            error: "No sandbox environment. Run /setup-env first to create env.dockerfile and build the image.",
                        }
                    }
                    
                    const dockerCmd = buildDockerCommand(dir, image, currentAgent, args.command)
                    
                    try {
                        const result = await $`${dockerCmd}`.nothrow().text()
                        return result
                    } catch (e) {
                        return {
                            error: e.message || String(e),
                        }
                    }
                },
            }),
        },
    }
}
```

## 2. Command: `.opencode/commands/setup-env.md`

```markdown
---
description: Build sandbox Docker image for this project
agent: analyze
---

# Setup Environment

This command analyzes your project and creates a sandbox Docker image for secure shell execution.

## Analysis

First, detect what tools your project needs:

1. **Check for dependency files:**
   - `package.json` → Node.js/npm
   - `requirements.txt`, `pyproject.toml`, `setup.py` → Python
   - `Cargo.toml` → Rust
   - `go.mod` → Go
   - `Gemfile` → Ruby
   - `Makefile` → Make

2. **Check for runtime directories:**
   - `.venv/`, `venv/` → Python virtual environment
   - `node_modules/` → Node dependencies

3. **Detect installed tools:**
   Run these to check what's available:
   ```
   git --version
   python3 --version
   node --version
   rustc --version
   go version
   ```

## Generate env.dockerfile

Create `env.dockerfile` based on detected dependencies:

```dockerfile
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# === BASE TOOLS (always needed) ===
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    jq \
    ripgrep \
    grep \
    findutils \
    coreutils \
    sed \
    gawk \
    bash \
    vim-tiny \
    manpages \
    && rm -rf /var/lib/apt/lists/*

# === PYTHON (if requirements.txt, pyproject.toml, setup.py, or .venv/) ===
# Check for python files and add:
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# === NODE.JS (if package.json) ===
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# === RUST (if Cargo.toml) ===
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# === GO (if go.mod) ===
RUN curl -fsSL https://go.dev/dl/go1.22.linux-amd64.tar.gz | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:$PATH"

# === RUBY (if Gemfile) ===
RUN apt-get update && apt-get install -y ruby ruby-bundler && rm -rf /var/lib/apt/lists/*

# === MAKE (if Makefile) ===
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

# === PROJECT-SPECIFIC TOOLS ===
# Add any additional tools your project needs based on detection above
```

## Build the Image

1. **Generate image tag:**
   Create a unique tag based on project name and path:
   ```
   TAG="opencode-env-$(basename $PWD | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-')-$(echo $PWD | md5sum | cut -c1-5)"
   ```

2. **Build:**
   ```
   docker build -t $TAG -f env.dockerfile .
   ```

3. **Save tag:**
   ```
   echo "$TAG" > .env-image
   ```

## Verify

Check the image works:
```
docker run --rm -v $(pwd):/workspace:ro $TAG bash -c "git --version && python3 --version"
```

## Files Created

After running /setup-env, you should have:
- `env.dockerfile` - The generated Dockerfile
- `.env-image` - Contains the image tag

The sandbox plugin will automatically use this image for all bash commands.

## Troubleshooting

- **Build fails**: Check the generated Dockerfile syntax
- **Missing tools**: Add them to the Dockerfile and rebuild
- **Permission denied**: Ensure Docker daemon is running
- **Path issues**: The container mounts your project at /workspace
```

## 3. Updated Agent Config (analyze.md)

Add sandbox config to frontmatter:

```yaml
---
description: Understand, investigate, and research
mode: primary
sandbox:
    volumes:
        ".": ro
        ".knowledge": rw
        ".experiments": rw
permission:
    # ... existing
---
```

## 4. Plugin Registration

Add to `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [".opencode/plugins/sandbox"]
}
```

Or create `.opencode/plugins/index.js`:

```javascript
export { SandboxPlugin } from "./sandbox/index.js"
```

## Usage Flow

```
1. User: /setup-env
   → Analyzes repo, creates env.dockerfile, builds image, writes .env-image

2. User: opencode --mode analyze
   → Plugin loads, reads .env-image
   → bash tool → docker run with :ro mounts

3. User: TAB to switch to build
   → Plugin tracks agent change
   → bash tool → docker run with :rw mounts
```

## Key Features

- **Single image**: Built once per project
- **Mode-based mounts**: Read-only in analyze, read-write in build
- **Markdown command**: Self-documenting, easy to customize
- **No Docker complexity for users**: Just run /setup-env
