# Updating the Framework

This guide explains how to keep your OpenCode framework installation up to date, switch between installation modes, and troubleshoot common issues.

---

## Updating the Framework

### Copy Mode

In copy mode, the framework is downloaded and extracted without git tracking. To update:

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash
```

The installer will:
1. Detect the existing `.opencode/` directory
2. Clone the latest version from the repository
3. Preserve your protected files (`opencode.json`, `.opencode/style-guide.md`)
4. Show you what will be updated before proceeding

To update to a specific version:

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --version v2.0.0
```

### Link Mode (Submodule)

In link mode, the framework is installed as a git submodule. To update:

```bash
cd .opencode && git fetch && git checkout vX.Y.Z
```

Or use the installer to update the submodule:

```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --link --update
```

---

## Switching Between Modes

### Copy → Link

Run the installer with `--link`:
```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --link
```

> **Note:** This will convert your installation to a git submodule.

### Link → Copy

Run the installer with `--copy`:
```bash
curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --copy
```

> **Note:** This will remove the `.git/` directory from the framework, breaking the submodule connection. Your customizations will be preserved.

---

## Updating opencode-core

### For Link Mode

The framework repository (`opencode-core`) is tracked as a submodule. To update to a specific version:

```bash
cd .opencode
git fetch origin
git checkout v2.0.0
cd ..
git add .opencode
git commit -m "chore: update opencode-core to v2.0.0"
```

To switch back to the latest from a branch:

```bash
cd .opencode
git checkout main
```

### For Copy Mode

Simply re-run the installer. It will download the latest version and preserve your configurations.

---

## Troubleshooting

### Updates Break Things

If an update causes issues:

1. **Check the changelog** - Review `.opencode/CHANGELOG.md` for breaking changes
2. **Run diagnostics**:
   ```bash
   make doctor
   ```
3. **Check for dependency updates**:
   ```bash
   make install-deps
   ```

### Rolling Back

#### Copy Mode Rollback

Since copy mode doesn't track git history, you cannot rollback automatically. To restore a previous state:

1. Identify the version you need from the installer changelog
2. Reinstall that specific version:
   ```bash
   curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --version v1.9.0
   ```

#### Link Mode Rollback

Git submodules preserve history. To rollback:

```bash
cd .opencode
git log --oneline        # Find the previous commit
git checkout v1.9.0      # Rollback to previous version
cd ..
git add .opencode
git commit -m "chore: rollback opencode-core to v1.9.0"
```

To find available versions:

```bash
cd .opencode
git tag -l              # List all available versions
```

### Stuck in Broken State

If your installation is corrupted:

1. **Remove the framework directory:**
   ```bash
   rm -rf .opencode
   ```

2. **Reinstall:**
   ```bash
   curl -fsSL https://apiad.github.io/opencode/install.sh | bash -s -- --copy
   ```

3. **Restore your configurations** from backups (if available in `~/.opencode/`)

---

## Getting Help

- **Documentation:** See other files in `/docs/`
- **Issues:** Report bugs at https://github.com/apiad/opencode/issues
- **Framework Repo:** https://github.com/apiad/opencode-core

---

*See [deploy.md](deploy.md) for information about installation modes and when to use each.*
