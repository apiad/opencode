#!/bin/bash
set -e

# --- Configuration ---
REPO_URL="https://github.com/apiad/starter.git"
VERSION="0.16.0"

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
# Files that are ALWAYS updated (Core Framework)
CORE_FILES=("GEMINI.md")
# Files that are ONLY created if missing (Scaffolding)
SCAFFOLD_FILES=("README.md" "TASKS.md" "CHANGELOG.md" "makefile")
# Directories that are ensured
CONTENT_DIRS=("journal" "plans" "research" "drafts")
# Files within .gemini/ that are PROTECTED (Never overwritten)
PROTECTED_GEMINI_FILES=("settings.json" "style-guide.md")

WILL_CREATE=()
WILL_UPDATE=()
WILL_PROTECT=()

# 1. .gemini Directory Logic
if [[ ! -d ".gemini" ]]; then
  WILL_CREATE+=(".gemini/ (core framework)")
else
  # Check for protected files
  for f in "${PROTECTED_GEMINI_FILES[@]}"; do
    if [[ -f ".gemini/$f" ]]; then
      WILL_PROTECT+=(".gemini/$f (user configuration)")
    fi
  done
  WILL_UPDATE+=(".gemini/ (hooks, scripts, core commands)")
fi

# 2. Core Files Logic (GEMINI.md)
for f in "${CORE_FILES[@]}"; do
  if [[ -e "$f" ]]; then
    WILL_UPDATE+=("$f (will preserve 'Project Notes' section if possible)")
  else
    WILL_CREATE+=("$f (core framework)")
  fi
done

# 3. Project Scaffolding Check
for f in "${SCAFFOLD_FILES[@]}"; do
  if [[ ! -e "$f" ]]; then
    WILL_CREATE+=("$f (new scaffolding)")
  else
    WILL_PROTECT+=("$f (existing project file)")
  fi
done

# 4. Content Directories Check
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
  echo -e "\033[1;34mExisting files to update:\033[0m"
  for f in "${WILL_UPDATE[@]}"; do echo "  ~ $f"; done
fi

if [[ ${#WILL_PROTECT[@]} -gt 0 ]]; then
  echo -e "\033[1;35mFiles to preserve (will NOT be modified):\033[0m"
  for f in "${WILL_PROTECT[@]}"; do echo "  # $f"; done
fi

echo ""
confirm "Do you want to proceed with these changes?"

# --- Execution ---
IS_UPDATE=false
if [[ -d ".gemini" ]]; then
  IS_UPDATE=true
fi

echo "🛠️  Applying changes..."

# 1. Update .gemini (Surgical Update)
mkdir -p .gemini
# Copy subdirectories one by one, preserving protected files
for subdir in agents commands hooks scripts; do
  if [[ -d "$TEMP_DIR/.gemini/$subdir" ]]; then
    mkdir -p ".gemini/$subdir"
    cp -r "$TEMP_DIR/.gemini/$subdir/." ".gemini/$subdir/"
  fi
done

# Restore protected files if they existed in temp (preventing accidental overwrite if cp -r was used)
for f in "${PROTECTED_GEMINI_FILES[@]}"; do
  if [[ -f "$TEMP_DIR/.gemini/$f" && ! -f ".gemini/$f" ]]; then
    cp "$TEMP_DIR/.gemini/$f" ".gemini/$f"
  fi
done

# 2. Update Core Files with preservation
for f in "${CORE_FILES[@]}"; do
  if [[ "$f" == "GEMINI.md" && -f "GEMINI.md" ]]; then
    # Try to preserve the section after "## Project Notes"
    # We take the header and core mandates from TEMP, and append the user's notes
    NOTES_START=$(grep -n "## Project Notes" GEMINI.md | cut -d: -f1 || echo "")
    if [[ -n "$NOTES_START" ]]; then
      TEMP_CORE=$(sed "/## Project Notes/q" "$TEMP_DIR/GEMINI.md")
      USER_NOTES=$(sed "1,$NOTES_START d" GEMINI.md)
      echo "$TEMP_CORE" > GEMINI.md
      echo "$USER_NOTES" >> GEMINI.md
    else
      cp "$TEMP_DIR/$f" .
    fi
  else
    cp "$TEMP_DIR/$f" .
  fi
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
if $IS_UPDATE; then
  MSG="Updated Gemini CLI framework to version $VERSION."
  COMMIT_MSG="chore: update Gemini CLI framework to v$VERSION"
else
  MSG="Integrated Gemini CLI framework version $VERSION."
  COMMIT_MSG="feat: integrate Gemini CLI framework v$VERSION"
fi

# Use the project's journal script if it exists
if [[ -f ".gemini/scripts/journal.py" ]]; then
  python3 .gemini/scripts/journal.py "$MSG"
else
  TODAY=$(date +%Y-%m-%d)
  echo -e "\n## Gemini CLI Integration\n- $MSG" >> "journal/$TODAY.md"
fi

# --- Post-Install ---
git add .
git commit -m "$COMMIT_MSG" -q

echo "✅ Gemini CLI framework $( [ "$IS_UPDATE" = true ] && echo "updated" || echo "integrated" ) successfully!"
echo "🚀 Run 'gemini /onboard' to get started!"
