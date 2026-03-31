---
id: setup-env-command-design
created: 2026-03-30
modified: 2026-03-30
type: design
status: active
tags: [command, docker, environment, sandbox]
---

# /setup-env Command Design

## Overview

A command that auto-detects project dependencies and builds a Docker image for sandboxed shell execution.

## Command Flow

```
User: /setup-env
    ↓
1. Auto-detect project dependencies
    ↓
2. Generate Dockerfile from template
    ↓
3. Build image with project hash tag
    ↓
4. Write tag to .env-image file
    ↓
5. Done - ready to use
```

## Auto-Detection

Check for these files to determine what's needed:

| File | Tool(s) to add |
|------|----------------|
| `package.json` | node, npm, pnpm, yarn |
| `requirements.txt`, `pyproject.toml`, `setup.py` | python, pip, uv |
| `Cargo.toml` | rust, cargo |
| `go.mod` | go |
| `Gemfile` | ruby, bundler |
| `Makefile` | make |
| `.venv/`, `venv/` | python (detect version from python --version) |
| `*.cabal`, `stack.yaml` | haskell |
| `*.cabal`, `package.yaml` | haskell |
| `composer.json` | php |
| `pom.xml`, `build.gradle` | java, maven, gradle |

Always include: `git`, `grep`, `findutils`, `coreutils`, `curl`, `wget`, `jq`, `sed`, `gawk`, `bash`

## Image Naming

```
Tag: {project-name}-{hash5}
Where:
  - project-name: sanitized project directory name (lowercase, alphanumeric, hyphens)
  - hash5: first 5 chars of MD5 hash of project root path (for uniqueness)
```

Example: `myproject-a7f3b`

## .env-image File

Simple text file with just the tag:

```
opencode-env-myproject-a7f3b
```

## Generated Dockerfile Template

```dockerfile
FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install base tools (always needed)
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
    manpages \
    vim-tiny \
    && rm -rf /var/lib/apt/lists/*

# Install Python (if detected)
# ... conditional based on pyproject.toml, requirements.txt, etc.

# Install Node.js (if detected)
# ... conditional based on package.json

# Install Rust (if detected)
# ... conditional based on Cargo.toml

# Install Go (if detected)
# ... conditional based on go.mod

# Install other languages as detected...
```

## Command Code Sketch

```typescript
// .opencode/commands/setup-env.ts

import { readdirSync, existsSync, readFileSync, writeFileSync, statSync } from "fs"
import { join, basename } from "path"
import { createHash } from "crypto"

interface DetectedDeps {
    python?: boolean
    node?: boolean
    rust?: boolean
    go?: boolean
    ruby?: boolean
    make?: boolean
    [key: string]: boolean | undefined
}

function detectDependencies(projectRoot: string): DetectedDeps {
    const deps: DetectedDeps = {}
    
    const files = readdirSync(projectRoot)
    
    // Python detection
    if (files.includes("requirements.txt") ||
        files.includes("pyproject.toml") ||
        files.includes("setup.py")) {
        deps.python = true
    }
    
    // Node detection
    if (files.includes("package.json")) {
        deps.node = true
    }
    
    // Rust detection
    if (files.includes("Cargo.toml")) {
        deps.rust = true
    }
    
    // Go detection
    if (files.includes("go.mod")) {
        deps.go = true
    }
    
    // Make detection
    if (files.includes("Makefile")) {
        deps.make = true
    }
    
    // Check for .venv
    if (files.some(f => f.includes("venv") || f.includes(".venv"))) {
        deps.python = true
    }
    
    return deps
}

function generateDockerfile(deps: DetectedDeps): string {
    const lines = [
        "FROM ubuntu:24.04",
        "",
        "ENV DEBIAN_FRONTEND=noninteractive",
        "",
        "# Base tools (always)",
        "RUN apt-get update && apt-get install -y \\",
        "    git \\",
        "    curl \\",
        "    wget \\",
        "    jq \\",
        "    ripgrep \\",
        "    grep \\",
        "    findutils \\",
        "    coreutils \\",
        "    sed \\",
        "    gawk \\",
        "    bash \\",
        "    vim-tiny \\",
        "    && rm -rf /var/lib/apt/lists/*",
        "",
    ]
    
    // Python
    if (deps.python) {
        lines.push(
            "# Python",
            "RUN apt-get update && apt-get install -y \\",
            "    python3 \\",
            "    python3-pip \\",
            "    python3-venv \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
            // Optional: uv
            "RUN curl -LsSf https://astral.sh/uv/install.sh | sh",
            "ENV PATH=\"/root/.local/bin:$PATH\"",
            "",
        )
    }
    
    // Node
    if (deps.node) {
        lines.push(
            "# Node.js",
            "RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \\",
            "    && apt-get install -y nodejs \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
        )
    }
    
    // Rust
    if (deps.rust) {
        lines.push(
            "# Rust",
            "RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
            "ENV PATH=\"/root/.cargo/bin:$PATH\"",
            "",
        )
    }
    
    // Go
    if (deps.go) {
        lines.push(
            "# Go",
            "RUN curl -fsSL https://go.dev/dl/go1.22.linux-amd64.tar.gz | tar -C /usr/local -xzf -",
            "ENV PATH=\"/usr/local/go/bin:$PATH\"",
            "",
        )
    }
    
    // Make
    if (deps.make) {
        lines.push(
            "# Make",
            "RUN apt-get update && apt-get install -y make \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
        )
    }
    
    return lines.join("\n")
}

function generateTag(projectRoot: string): string {
    const name = basename(projectRoot)
        .toLowerCase()
        .replace(/[^a-z0-9-]/g, "-")
        .replace(/-+/g, "-")
    
    const hash = createHash("md5")
        .update(projectRoot)
        .digest("hex")
        .substring(0, 5)
    
    return `opencode-env-${name}-${hash}`
}

export const setupEnvCommand = {
    name: "setup-env",
    describe: "Build sandbox Docker image for this project",
    
    async handler() {
        const projectRoot = process.cwd()
        
        console.log("🔍 Detecting project dependencies...")
        const deps = detectDependencies(projectRoot)
        console.log("Found:", Object.entries(deps)
            .filter(([, v]) => v)
            .map(([k]) => k)
            .join(", ") || "none (base image only)")
        
        // Generate Dockerfile
        const dockerfile = generateDockerfile(deps)
        const dockerfilePath = join(projectRoot, "env.dockerfile")
        writeFileSync(dockerfilePath, dockerfile)
        console.log(`📝 Generated ${dockerfilePath}`)
        
        // Build image
        const tag = generateTag(projectRoot)
        console.log(`\n🐳 Building image: ${tag}`)
        
        await Bun.$`docker build -t ${tag} -f ${dockerfilePath} ${projectRoot}`
        
        // Write .env-image
        const envImagePath = join(projectRoot, ".env-image")
        writeFileSync(envImagePath, tag)
        console.log(`\n✅ Image tag written to .env-image`)
        
        // Cleanup Dockerfile (optional - keep for rebuilds?)
        // unlinkSync(dockerfilePath)
        
        console.log("\nDone! Plugin will use this image for sandboxed shell execution.")
    }
}
```

## File Outputs

```
project/
├── .env-image          # Contains: opencode-env-myproject-a7f3b
├── env.dockerfile      # Generated, can be committed or gitignored
└── ...
```

## Plugin Usage

The plugin reads `.env-image` to get the image name, then uses it for both containers with different volume mounts:

```typescript
// Read image tag
const imageTag = readFileSync(".env-image", "utf-8").trim()

// Container for analyze mode
docker create --name opencode-analyze \
    -v $(pwd):/workspace:ro \
    -v $(pwd)/.experiments:/workspace/.experiments:rw \
    -v $(pwd)/.knowledge:/workspace/.knowledge:rw \
    ${imageTag} sleep infinity

// Container for build mode
docker create --name opencode-build \
    -v $(pwd):/workspace:rw \
    -v $(pwd)/.experiments:/workspace/.experiments:rw \
    -v $(pwd)/.knowledge:/workspace/.knowledge:rw \
    ${imageTag} sleep infinity
```

## Edge Cases

| Case | Handling |
|------|----------|
| No deps detected | Build minimal image (just base tools) |
| Docker not installed | Error with install instructions |
| Docker build fails | Show error, keep Dockerfile for debugging |
| Project path changes | Hash changes, new image built |
| Missing language version | Use latest LTS from official sources |

## Future Enhancements

- Cache base layers separately
- Support custom Dockerfile template override
- Multi-stage builds for smaller images
- Integration with existing project Dockerfiles
