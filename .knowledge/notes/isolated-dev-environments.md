---
id: isolated-dev-environments-research
created: 2026-03-29
modified: 2026-03-29
type: research
status: active
tags: [docker, overlayfs, namespaces, distrobox, toolbox, isolation, development]
---

# Isolated Development Environments: Read-Only Source + Writable Overlays

## Executive Summary

This research explores patterns for creating development environments with **read-only base layers** and **writable overlays** — allowing developers to "write anywhere" while persisting changes only to designated directories. This pattern is particularly valuable for:

- Protecting source code from accidental modifications
- Enabling safe experimentation
- Maintaining clean separation between dependencies and project-specific changes
- Supporting ephemeral/disposable development environments

---

## 1. Docker-Based Solutions

### 1.1 Overlay Filesystem (OverlayFS)

The kernel-level mechanism that powers Docker's layered storage.

**How it works:**
```
Upper (writable)    ← Temporary changes, builds, generated files
       ↓
Lower (read-only)   ← Source code, base image layers
```

**Key characteristics:**
- **Copy-up on write**: When modifying a lower file, the entire file is copied to upper before modification
- **Whiteouts**: Deleted files are marked in upper layer (don't actually remove from lower)
- **Metadata-only copy**: With `metacopy=on`, only metadata copies up initially; data copies on actual write
- **Multiple lower layers**: Can stack multiple read-only layers using colon separators

**Docker implementation:**
```bash
# Source code as read-only volume
docker run -v /path/to/source:/app:ro \
           -v /app/build:/app/build \
           my-dev-image

# With docker-compose
services:
  dev:
    image: my-dev-image
    volumes:
      - ./source:/app:ro        # Read-only source
      - ./build:/app/build      # Writable build output
      - /tmp:/tmp               # Writable /tmp
```

**Pros:**
- Native to Linux kernel (no extra tools)
- Docker handles automatically
- Efficient storage through layering

**Cons:**
- Docker volumes are fully writable (can't restrict to specific paths)
- Overlayfs copy-up can be expensive for large files
- Not visible to developer which layer they're writing to

---

### 1.2 Read-Only Root Filesystem with Explicit Writable Mounts

```dockerfile
FROM base-image
VOLUME ["/workspace", "/var/cache", "/root/.cache"]
```

**Security-hardened approach:**
```bash
docker run --read-only \
           --tmpfs /tmp:rw \
           -v /persistent/data:/workspace:rw \
           my-image
```

**Key Docker flags:**
- `--read-only`: Makes root filesystem read-only
- `--tmpfs /path`: Mounts tmpfs (RAM-backed, ephemeral writes)
- `-v host:container:ro`: Read-only bind mount
- `--storage-opt size=X`: Limits container storage size

**Pros:**
- Strong security guarantees
- Clear documentation of writable paths
- Forces intentional data management

**Cons:**
- Some applications need to write to unexpected locations
- Debugging requires entering container
- tmpfs limited by available RAM

---

### 1.3 Development-Optimized Docker Patterns

**Pattern: Ephemeral dev containers**
```bash
docker run --rm -it \
           --read-only \
           --tmpfs /tmp \
           --tmpfs /var/cache \
           -v project-src:/src:ro \
           -v $(pwd)/.devcontainer/data:/data \
           dev-image
```

**Pattern: Configurable write locations**
```bash
# Set specific directories as writable
export WRITABLE_DIRS="/workspace:/build:/data"
docker run --read-only \
           $(for d in $WRITABLE_DIRS; do echo "-v $(pwd)/${d##*:}:${d%%:*}"; done) \
           dev-image
```

---

## 2. Lightweight Alternatives: Distrobox & Toolbox

### 2.1 Distrobox

**What it is**: A wrapper around Podman/Docker that creates tightly-integrated development containers.

**Key features:**
- Seamless host integration (shares home, Wayland, X11, SSH agent, etc.)
- Uses OCI images as base
- Written in POSIX shell (portable)
- Fast container entry (~400ms on weak hardware)
- 12k GitHub stars, active community

**Typical workflow:**
```bash
# Create a dev environment
distrobox create --name dev-ubuntu --image ubuntu:22.04

# Enter it (seamless, like local shell)
distrobox enter dev-ubuntu

# Or ephemeral (destroyed on exit)
distrobox ephemeral --image fedora:latest
```

**Writability control:**
- By default, home directory is **shared** with host (mutable)
- Custom home via `--home` flag
- Additional volumes can be read-only or read-write

```bash
distrobox create \
  --name secure-dev \
  --image ubuntu:22.04 \
  --home /path/to/custom/home \
  --additional-packages "build-essential,git"
```

**Pros:**
- Lightweight (no full VM overhead)
- Works with existing Docker/Podman
- Easy automation (shell scripts)
- Cross-distro (use any Linux distro inside another)

**Cons:**
- Not sandboxed by default (shares home, devices)
- Requires Podman or Docker
- Security not primary goal (unlike Flatpak)

**Home-writable approach for distrobox:**
Distrobox doesn't enforce read-only sources natively, but you can:
```bash
# Mount source as read-only
distrobox create \
  --name dev \
  --image ubuntu:22.04 \
  --additional-packages "build-essential" \
  --volume "/path/to/source:/workspace:ro"
```

---

### 2.2 Toolbox (Toolbx)

**What it is**: Official Fedora project, predecessor to Distrobox concepts. Built on Podman.

**Key differences from Distrobox:**
- Written in Go (not shell)
- Heavier integration with Fedora ecosystem
- Similar capabilities but less portable

**Usage:**
```bash
toolbox create --image fedora:42
toolbox enter
```

**For OSTree systems (Silverblue, etc.):**
- Designed for immutable base + mutable toolbox
- Home typically shared by default
- Can create custom home directories

---

### 2.3 Comparison: Distrobox vs Toolbox

| Aspect | Distrobox | Toolbox |
|--------|-----------|---------|
| Language | POSIX Shell | Go |
| Portability | High (any Linux) | Fedora-focused |
| Stars | 12k | 3.3k |
| Custom home | Yes | Yes |
| Host integration | Excellent | Excellent |
| Security focus | Low | Low |
| Dependencies | Podman/Docker | Podman |

---

## 3. OverlayFS Patterns (Kernel-Level)

### 3.1 Native OverlayFS Mount

For non-Docker approaches, direct overlayfs:

```bash
# Create directories
mkdir -p /overlay/upper /overlay/work /merged
mkdir -p /lower-ro/source /lower-ro/deps

# Mount overlay
mount -t overlay overlay \
  -olowerdir=/lower-ro:/lower-ro2,\
  upperdir=/overlay/upper,\
  workdir=/overlay/work \
  /merged

# Now /merged shows combined view
# - Source code from /lower-ro is read-only visible
# - Writes go to /overlay/upper
```

**Key mount options:**
- `lowerdir=path1:path2`: Stack multiple read-only layers (right = bottom)
- `upperdir=path`: Writable layer
- `workdir=path`: Required for read-write overlay (empty, same fs as upper)
- `metacopy=on`: Metadata-only copy-up (faster writes)
- `redirect_dir=on`: Enable directory renames across layers
- `volatile`: No fsync (faster, unsafe after crash)

### 3.2 Read-Only Source + Writable Home

```bash
# Source as lower, home as upper
mount -t overlay overlay \
  -olowerdir=/nfs/share/source:/base/packages,\
  upperdir=$HOME/.overlay/upper,\
  workdir=$HOME/.overlay/work \
  $HOME
```

This makes:
- `/nfs/share/source` → Read-only in home view
- `~/.overlay/upper` → Catches all writes (including new files)
- "Write anywhere" works, but changes persist only in upper

### 3.3 Selective Persistence Pattern

For specific writable directories only:

```bash
# Create per-directory overlays
for dir in workspace build cache; do
  mkdir -p ~/.overlay/upper/$dir ~/.overlay/work/$dir
  mount -t overlay overlay-$dir \
    -olowerdir=/ro/shared/$dir,\
    upperdir=~/.overlay/upper/$dir,\
    workdir=~/.overlay/work/$dir \
    ~/$dir
done
```

**Result:**
- `~/workspace` → Read-only source + writable overlay
- `~/build` → Writable build output
- `~/cache` → Writable cache

---

## 4. Namespace-Based Approaches

### 4.1 Linux Namespaces

More granular than containers:

```bash
# Create user namespace with custom uid mapping
unshare --user --map-root-user

# Mount namespace for filesystem isolation
unshare --mount --propagation private

# Mount read-only
mount --bind /path/to/ro /path/to/merged
mount -o remount,readonly /path/to/merged

# Or overlay within namespace
mount -t overlay overlay \
  -olowerdir=/ro,upperdir=/rw,workdir=/work \
  /merged
```

### 4.2 Chroot (Simple, Limited)

```bash
# Simple isolation
chroot /path/to/jail /bin/bash

# Combined with read-only mounts
mount --bind /ro/path /jail/path
mount -o remount,readonly /jail/path
```

**Pros:** No containers required
**Cons:** Basic isolation only, not security-hardened

---

## 5. Git-Based Sandbox Patterns

### 5.1 Git Worktrees for Source Isolation

```bash
# Create worktree with pristine source
git worktree add /workspace/project-copy main
cd /workspace/project-copy

# Changes isolated to worktree
# Can reset cleanly
git reset --hard HEAD
```

### 5.2 Git Read-Only Mounts

```bash
# Clone to read-only location
git clone --bare /repo.git /ro/nfs/repo

# Worktrees in writable location
git -C /ro/nfs/repo worktree list
```

---

## 6. Special Considerations

### 6.1 The "/tmp" Problem

Most dev workflows need temporary writable space:

| Solution | Pros | Cons |
|----------|------|------|
| `tmpfs` | Fast, in-memory | RAM-limited |
| Host `/tmp` bind | Unlimited space | Leakage possible |
| Per-container tmp | Isolated | Requires Docker flags |

**Recommended for read-only containers:**
```bash
docker run --read-only --tmpfs /tmp:size=2g my-image
```

### 6.2 Build Tool Cache Patterns

```bash
# Cache as separate writable layer
docker run --read-only \
           --tmpfs /tmp \
           -v $HOME/.cache:/root/.cache:rw \
           dev-image

# Or ephemeral cache
docker run --read-only \
           --tmpfs /tmp \
           --tmpfs /root/.cache \
           dev-image
```

### 6.3 Editor/IDE Considerations

- **VSCode Remote**: Handles workspace mounting well
- **Neovim/Emacs**: Work naturally with overlay
- **JetBrains**: Can configure project paths

---

## 7. Comparison Matrix

| Approach | Lightweight | Automation | Read-Only Source | Selective Persistence | Learning Curve |
|----------|-------------|------------|------------------|---------------------|---------------|
| Docker + `:ro` | Yes | Easy | Native | Via volumes | Low |
| Docker `--read-only` | Yes | Easy | Native | Via tmpfs | Low |
| Distrobox | Yes | Easy | Via volumes | Via volumes | Low |
| Toolbox | Yes | Moderate | Via volumes | Via volumes | Medium |
| Native OverlayFS | Yes | Hard | Native | Native | High |
| Namespaces | Yes | Hard | Native | Native | High |
| Chroot | Yes | Moderate | Manual | Manual | Low |

---

## 8. Recommended Approaches by Use Case

### For CI/CD Pipelines
**Docker `--read-only` + explicit volumes**
```bash
docker run --read-only \
           --tmpfs /tmp \
           -v source:/src:ro \
           -v build:/build \
           -v cache:/root/.cache \
           ci-image
```

### For Local Development
**Distrobox + read-only volumes**
```bash
distrobox create --name dev --image ubuntu:22.04
distrobox enter dev -- volume /path/to/source:/workspace:ro
```

### For Ephemeral Experimentation
**Native overlayfs or Docker ephemeral**
```bash
# Docker ephemeral
docker run --rm --read-only --tmpfs /tmp -v src:ro dev-image

# Overlayfs ephemeral
mount -t overlay overlay \
  -olowerdir=/ro/source,upperdir=/tmp/overlay,workdir=/tmp/work \
  /workspaceyu
```

### For Protecting Vendor Code
**Git worktrees + read-only bind**
```bash
git worktree add /workspace/worktree main
mount --bind /ro/vendored /workspace/worktree/vendor
mount -o remount,readonly /workspace/worktree/vendor
```

---

## 9. Key References

- [Linux Kernel OverlayFS Documentation](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html)
- [Docker Storage Documentation](https://docs.docker.com/storage/)
- [Distrobox GitHub](https://github.com/89luca89/distrobox)
- [Toolbx Project](https://containertoolbx.org/)
- [Fedora Silverblue Toolbox Docs](https://docs.fedoraproject.org/en_US/fedora-silverblue/)

---

## 10. Open Questions for Further Research

1. **Permission model interactions**: How do UID/GID mappings affect overlayfs copy-up?
2. **Performance benchmarks**: Copy-up vs. bind-mount for various workloads
3. **NFS compatibility**: Can overlayfs work over network filesystems?
4. **Container orchestration**: How do Kubernetes/OpenShift handle read-only root?
5. **IDE integration**: Best practices for VSCode Remote with overlay patterns

---

## Summary

**For most development workflows, the practical recommendation is:**

1. **Distrobox** for local development (easy, flexible, well-maintained)
2. **Docker `--read-only`** with explicit volume mounts for CI/CD
3. **Native overlayfs** for custom scripting or when Docker isn't available

The key insight is that **overlayfs is the underlying mechanism** that makes all these approaches work — Docker uses it internally, and Distrobox inherits this capability through Podman. The choice is about which abstraction level fits your workflow.
