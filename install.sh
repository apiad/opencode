#!/bin/bash
set -e

# --- Configuration ---
REPO_URL="https://github.com/apiad/starter.git"
VERSION="0.9.0"

# --- Functions ---
banner() {
  echo -e "\033[1;34m"
  echo "  ____               _       _ "
  echo " / ___| ___ _ __ ___(_)_ __ (_)"
  echo "| |  _ / _ \ '_ \' _ \ | '_ \| |"
  echo "| |_| |  __/ | | | | | | | | | |"
  echo " \____|\___|_| |_| |_|_|_| |_|_|"
  echo -e "\033[0m"
  echo -e "\033[1;32m   Gemini CLI Starter v$VERSION\033[0m"
  echo "------------------------------------------"
}

error() {
  echo -e "\033[0;31m❌ Error: $1\033[0m" >&2
  exit 1
}

# --- Check Prerequisites ---
for cmd in git node; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd is not installed. Please install it and try again."
  fi
done

# --- Inputs ---
# We use /dev/tty for input because curl | bash takes over stdin
banner

echo -n "Enter project name: "
read PROJECT_NAME < /dev/tty

if [[ -z "$PROJECT_NAME" ]]; then
  error "Project name cannot be empty."
fi

# Sanitize project name for default target directory
DEFAULT_TARGET=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')
echo -n "Enter target directory [$DEFAULT_TARGET]: "
read TARGET_DIR < /dev/tty

TARGET_DIR=${TARGET_DIR:-$DEFAULT_TARGET}

if [[ -d "$TARGET_DIR" ]]; then
  error "Directory '$TARGET_DIR' already exists. Choose a different directory or delete the existing one."
fi

# --- Execution ---
echo "🚀 Scaffolding new project: $PROJECT_NAME in $TARGET_DIR..."

# Clone the template
git clone --depth 1 "$REPO_URL" "$TARGET_DIR" || error "Failed to clone template repository."

cd "$TARGET_DIR"

# Reset Git History
rm -rf .git
git init -q

# Reset Core Markdown Files
cat <<EOF > README.md
# $PROJECT_NAME

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
  if [[ -d "$dir" ]]; then
    find "$dir" -maxdepth 1 -type f ! -name ".gitkeep" -delete
    touch "$dir/.gitkeep"
  fi
done

# Create first journal entry
TODAY=$(date +%Y-%m-%d)
cat <<EOF > "journal/$TODAY.md"
# $TODAY - Initial Kickoff

Started the project "$PROJECT_NAME" using the Gemini CLI framework.
EOF

# --- Post-Install ---
git add .
git commit -m "Initial commit" -q

echo "✅ Project $PROJECT_NAME scaffolded successfully!"
echo "🚀 Starting Gemini CLI..."

# Run the gemini CLI
if command -v gemini >/dev/null 2>&1; then
  exec gemini
else
  echo "⚠️  'gemini' command not found. Please ensure the Gemini CLI is installed and in your PATH."
fi
