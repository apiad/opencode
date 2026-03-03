# Objective: Implementation of `install.sh` Scaffolding Script

The objective is to provide a robust, interactive shell script at the root of the repository that allows users to quickly bootstrap new projects based on this opinionated Gemini CLI framework. The script is designed to be run via `curl` and piped to `bash`.

## Architectural Impact
- **Developer Experience:** Simplifies the onboarding process for new projects.
- **Project Structure:** Adds a new utility script (`install.sh`) to the repository root.
- **Framework Integrity:** Ensures that all necessary configuration files (specifically the `.gemini/` directory) are preserved while user-specific content is reset.

## File Operations
- **Created File:** `install.sh` at the repository root.

## Step-by-Step Execution

### 1. Script Drafting
Create `install.sh` with the following logic:
- **Environment Checks:** Verify that `git` and `node` are installed.
- **Interactive Prompts:** 
    - Use `/dev/tty` for `read` commands to ensure compatibility with `curl | bash` execution.
    - Ask for the `Project Name`.
    - Ask for the `Target Directory` (defaulting to a kebab-case version of the project name).
- **Core Scaffolding:**
    - Clone the `apiad/starter` repository using `--depth 1` for a fast, shallow clone.
    - Remove the `.git` directory and run `git init` to establish a new history.
- **Content Reset:**
    - Overwrite `README.md` with a minimal title and template reference.
    - Overwrite `CHANGELOG.md` with a clean header.
    - Clear all markdown files from `journal/`, `plans/`, and `drafts/` while preserving `.gitkeep` files.
    - Generate a first journal entry for the current date (`journal/YYYY-MM-DD.md`).
- **Finalization:**
    - Perform an initial `git add .` and `git commit -m "Initial commit"`.
    - Attempt to launch the `gemini` CLI command.

### 2. Permissions (Informational)
While the user will likely run this via `bash`, the script itself should be marked as executable in the repository for local use.

## Proposed `install.sh` Content

```bash
#!/bin/bash
set -e

# --- Configuration ---
REPO_URL="https://github.com/apiad/starter.git"

# --- Functions ---
error() {
  echo -e "\033[0;31m❌ Error: \$1\033[0m" >&2
  exit 1
}

# --- Check Prerequisites ---
for cmd in git node; do
  if ! command -v "\$cmd" >/dev/null 2>&1; then
    error "\$cmd is not installed. Please install it and try again."
  fi
done

# --- Inputs ---
# We use /dev/tty for input because curl | bash takes over stdin
echo -n "Enter project name: "
read PROJECT_NAME < /dev/tty

if [[ -z "\$PROJECT_NAME" ]]; then
  error "Project name cannot be empty."
fi

# Sanitize project name for default target directory
DEFAULT_TARGET=\$(echo "\$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')
echo -n "Enter target directory [\$DEFAULT_TARGET]: "
read TARGET_DIR < /dev/tty

TARGET_DIR=\${TARGET_DIR:-\$DEFAULT_TARGET}

if [[ -d "\$TARGET_DIR" ]]; then
  error "Directory '\$TARGET_DIR' already exists. Choose a different directory or delete the existing one."
fi

# --- Execution ---
echo "🚀 Scaffolding new project: \$PROJECT_NAME in \$TARGET_DIR..."

# Clone the template
git clone --depth 1 "\$REPO_URL" "\$TARGET_DIR" || error "Failed to clone template repository."

cd "\$TARGET_DIR"

# Reset Git History
rm -rf .git
git init -q

# Reset Core Markdown Files
cat <<EOF > README.md
# \$PROJECT_NAME

This project was bootstrapped from [apiad/starter](https://github.com/apiad/starter).
EOF

cat <<EOF > CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Initial project scaffold.
EOF

# Clear content directories but preserve .gitkeep
for dir in journal plans drafts; do
  if [[ -d "\$dir" ]]; then
    find "\$dir" -maxdepth 1 -type f ! -name ".gitkeep" -delete
    touch "\$dir/.gitkeep"
  fi
done

# Create first journal entry
TODAY=\$(date +%Y-%m-%d)
cat <<EOF > "journal/\$TODAY.md"
# \$TODAY - Initial Kickoff

Started the project "\$PROJECT_NAME" using the Gemini CLI framework.
EOF

# --- Post-Install ---
git add .
git commit -m "Initial commit" -q

echo "✅ Project \$PROJECT_NAME scaffolded successfully!"
echo "🚀 Starting Gemini CLI..."

# Run the gemini CLI
if command -v gemini >/dev/null 2>&1; then
  exec gemini
else
  echo "⚠️  'gemini' command not found. Please ensure the Gemini CLI is installed and in your PATH."
fi
```
