#!/bin/bash
set -e

# --- Configuration ---
REPO_URL="https://github.com/apiad/starter.git"
VERSION="0.10.0"

# --- Functions ---
banner() {
  echo -e "\033[1;34m"
  echo "  ____                _       _ "
  echo " / ___| ___ _ __ ___ (_) __  (_)"
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

confirm() {
  echo -n "$1 [y/N]: "
  read CONFIRM < /dev/tty
  if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    error "Aborted by user."
  fi
}

# --- Check Prerequisites ---
for cmd in git node; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd is not installed. Please install it and try again."
  fi
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  error "Not a git repository. This script must be run inside an existing git repository."
fi

if [[ -n $(git status --porcelain) ]]; then
  error "Working tree is not clean. Please commit or stash your changes before running this script."
fi

# --- Inputs ---
banner

# --- Conflict Check ---
CONFLICTS=()
FILES_TO_EXTRACT=(
  ".gemini/"
  "GEMINI.md"
  "TASKS.md"
  "CHANGELOG.md"
  "makefile"
  "journal/"
  "plans/"
  "research/"
  "drafts/"
)

for f in "${FILES_TO_EXTRACT[@]}"; do
  if [[ -e "$f" ]]; then
    CONFLICTS+=("$f")
  fi
done

if [[ ${#CONFLICTS[@]} -gt 0 ]]; then
  echo -e "\033[0;33m⚠️  Warning: The following files/folders already exist:\033[0m"
  for c in "${CONFLICTS[@]}"; do
    echo "  - $c"
  done
  confirm "Do you want to overwrite them and proceed with the integration?"
fi

# --- Execution ---
echo "🚀 Integrating Gemini CLI framework..."

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# Clone the template to temp
git clone --depth 1 -q "$REPO_URL" "$TEMP_DIR" || error "Failed to clone template repository."

# Copy core files
cp -r "$TEMP_DIR/.gemini" .
cp "$TEMP_DIR/GEMINI.md" .

# Handle other files/folders
for f in TASKS.md CHANGELOG.md makefile journal plans research drafts; do
  if [[ -d "$TEMP_DIR/$f" ]]; then
    mkdir -p "$f"
    # Copy .gitkeep files if they exist
    find "$TEMP_DIR/$f" -name ".gitkeep" -exec cp {} "$f/" \; 2>/dev/null || true
  else
    cp "$TEMP_DIR/$f" .
  fi
done

# Reset TASKS.md and CHANGELOG.md to clean state
cat <<EOF > TASKS.md
# Tasks

Legend:

- [ ] Todo
- [/] In Progress (@user)
- [x] Done

---

## Active Tasks
- [ ] Initialize the project goals.

---

 ## Archive
EOF

cat <<EOF > CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Integrated Gemini CLI framework.
EOF

# Clear content directories but preserve .gitkeep
for dir in journal plans research drafts; do
  if [[ -d "$dir" ]]; then
    find "$dir" -maxdepth 1 -type f ! -name ".gitkeep" -delete
    touch "$dir/.gitkeep"
  fi
done

# Create first journal entry
TODAY=$(date +%Y-%m-%d)
cat <<EOF > "journal/$TODAY.md"
# $TODAY - Gemini CLI Integration

Integrated the Gemini CLI framework into this repository.
EOF

# --- Post-Install ---
git add .
git commit -m "feat: integrate Gemini CLI framework" -q

echo "✅ Gemini CLI framework integrated successfully!"
echo "🚀 Run 'gemini /onboard' to get started with your new project!"
