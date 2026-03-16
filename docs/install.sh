#!/bin/bash
set -e

# --- Configuration ---
REPO_URL="https://github.com/apiad/starter.git"
VERSION="0.11.0"

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
    echo "Aborted by user."
    exit 0
  fi
}

# --- Check Prerequisites ---
for cmd in git node; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd is not installed. Please install it and try again."
  fi
done

# --- Git Environment Validation ---
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "📂 Initializing git repository..."
  git init -q
fi

if [[ -n $(git status --porcelain) ]]; then
  error "Working tree is not clean. Please commit or stash your changes before running this script."
fi

# --- Inputs ---
banner

# --- Acquisition ---
echo "🚀 Fetching latest framework from $REPO_URL..."
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

git clone --depth 1 -q "$REPO_URL" "$TEMP_DIR" || error "Failed to clone template repository."

# --- Discovery ---
CORE_FILES=("GEMINI.md")
SCAFFOLD_FILES=("README.md" "TASKS.md" "CHANGELOG.md" "makefile")
CONTENT_DIRS=("journal" "plans" "research" "drafts")

WILL_CREATE=()
WILL_UPDATE=()

# 1. Core Framework Check
if [[ -d ".gemini" ]]; then
  WILL_UPDATE+=(".gemini/ (core framework)")
else
  WILL_CREATE+=(".gemini/ (core framework)")
fi

for f in "${CORE_FILES[@]}"; do
  if [[ -e "$f" ]]; then
    WILL_UPDATE+=("$f (core framework)")
  else
    WILL_CREATE+=("$f (core framework)")
  fi
done

# 2. Project Scaffolding Check
for f in "${SCAFFOLD_FILES[@]}"; do
  if [[ ! -e "$f" ]]; then
    WILL_CREATE+=("$f (new scaffolding)")
  fi
done

# 3. Content Directories Check
for d in "${CONTENT_DIRS[@]}"; do
  if [[ ! -d "$d" ]]; then
    WILL_CREATE+=("$d/ (new content directory)")
  fi
done

# --- Summary & Confirmation ---
echo -e "\033[1;33mProposed Changes:\033[0m"
if [[ ${#WILL_CREATE[@]} -gt 0 ]]; then
  echo -e "\033[1;32mNew files/folders to create:\033[0m"
  for f in "${WILL_CREATE[@]}"; do echo "  + $f"; done
fi

if [[ ${#WILL_UPDATE[@]} -gt 0 ]]; then
  echo -e "\033[1;34mExisting files/folders to update (core framework):\033[0m"
  for f in "${WILL_UPDATE[@]}"; do echo "  ~ $f"; done
fi

echo ""
confirm "Do you want to proceed with these changes?"

# --- Execution ---
IS_UPDATE=false
if [[ -d ".gemini" ]]; then
  IS_UPDATE=true
fi

echo "🛠️  Applying changes..."

# 1. Update .gemini (non-destructive for user files)
mkdir -p .gemini
cp -r "$TEMP_DIR/.gemini/." .gemini/

# 2. Update Core Files (Always)
for f in "${CORE_FILES[@]}"; do
  cp "$TEMP_DIR/$f" .
done

# 3. Create Scaffolding Files (Only if missing)
for f in "${SCAFFOLD_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    cp "$TEMP_DIR/$f" .
  fi
done

# 4. Ensure Content Directories & .gitkeep
for d in "${CONTENT_DIRS[@]}"; do
  mkdir -p "$d"
  if [[ -f "$TEMP_DIR/$d/.gitkeep" ]]; then
    cp "$TEMP_DIR/$d/.gitkeep" "$d/"
  fi
done

# 5. Journal Entry
TODAY=$(date +%Y-%m-%d)
mkdir -p journal
JOURNAL_FILE="journal/$TODAY.md"
if [[ ! -f "$JOURNAL_FILE" ]]; then
  echo "# $TODAY" > "$JOURNAL_FILE"
fi

if $IS_UPDATE; then
  echo -e "\n## Gemini CLI Update\n- Updated framework to version $VERSION." >> "$JOURNAL_FILE"
  COMMIT_MSG="chore: update Gemini CLI framework to v$VERSION"
else
  echo -e "\n## Gemini CLI Integration\n- Integrated Gemini CLI framework v$VERSION." >> "$JOURNAL_FILE"
  COMMIT_MSG="feat: integrate Gemini CLI framework v$VERSION"
fi

# --- Post-Install ---
git add .
git commit -m "$COMMIT_MSG" -q

echo "✅ Gemini CLI framework $( [ "$IS_UPDATE" = true ] && echo "updated" || echo "integrated" ) successfully!"
echo "🚀 Run 'gemini /onboard' to get started!"
