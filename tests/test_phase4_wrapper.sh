#!/usr/bin/env bash
# Test script for Phase 4: Refactor Wrapper Repository
# Verifies all completion criteria for Phase 4

set -e

REPO_DIR="/home/apiad/Projects/personal/opencode"

echo "=== Phase 4: Wrapper Repository Test ==="

# Check 1: .opencode/ is now a git submodule (not in .gitignore)
echo -n "Checking .opencode/ is a git submodule... "
if [[ ! -f "$REPO_DIR/.gitmodules" ]]; then
    echo "FAIL: .opencode is not a submodule (.gitmodules missing)"
    exit 1
fi
if ! grep -q "path = \.opencode" "$REPO_DIR/.gitmodules" 2>/dev/null; then
    echo "FAIL: .opencode not registered as submodule"
    exit 1
fi
echo "OK"

# Check 2: AGENTS.md removed (in opencode-core now)
echo -n "Checking AGENTS.md removed... "
if [[ -f "$REPO_DIR/AGENTS.md" ]] && [[ $(git -C "$REPO_DIR" ls-files | grep -c "^AGENTS.md$" 2>/dev/null || echo 0) -gt 0 ]]; then
    echo "FAIL: AGENTS.md still tracked"
    exit 1
fi
echo "OK"

# Check 3: templates/ directory created
echo -n "Checking templates/ directory exists... "
if [[ ! -d "$REPO_DIR/templates" ]]; then
    echo "FAIL: templates/ directory not found"
    exit 1
fi
echo "OK"

# Check 4: Required template files exist
echo -n "Checking template files... "
REQUIRED_TEMPLATES=(
    "templates/README.md"
    "templates/makefile"
    "templates/tasks.yaml"
    "templates/CHANGELOG.md"
    "templates/.gitignore"
)
for tpl in "${REQUIRED_TEMPLATES[@]}"; do
    if [[ ! -f "$REPO_DIR/$tpl" ]]; then
        echo "FAIL: $tpl not found"
        exit 1
    fi
done
echo "OK (${#REQUIRED_TEMPLATES[@]} files)"

# Check 5: .knowledge/ structure with .gitkeep
echo -n "Checking .knowledge/ structure... "
for subdir in notes plans log drafts; do
    if [[ ! -d "$REPO_DIR/.knowledge/$subdir" ]]; then
        echo "FAIL: .knowledge/$subdir not found"
        exit 1
    fi
    # Check for .gitkeep or any content
    if [[ -z "$(ls -A "$REPO_DIR/.knowledge/$subdir" 2>/dev/null)" ]]; then
        echo "WARN: .knowledge/$subdir is empty (no .gitkeep)"
    fi
done
echo "OK"

# Check 6: install.sh still present
echo -n "Checking install.sh present... "
if [[ ! -f "$REPO_DIR/install.sh" ]]; then
    echo "FAIL: install.sh not found"
    exit 1
fi
echo "OK"

# Check 7: README.md updated
echo -n "Checking README.md mentions new architecture... "
if ! grep -q "opencode-core\|dual-mode\|--mode=copy\|--mode=link" "$REPO_DIR/README.md" 2>/dev/null; then
    echo "FAIL: README.md not updated for new architecture"
    exit 1
fi
echo "OK"

# Check 8: docs/ structure preserved
echo -n "Checking docs/ preserved... "
if [[ ! -d "$REPO_DIR/docs" ]]; then
    echo "FAIL: docs/ directory not found"
    exit 1
fi
echo "OK"

# Check 9: node_modules/ gitignored
echo -n "Checking node_modules/ gitignored... "
if ! grep -q "^node_modules/" "$REPO_DIR/.gitignore" 2>/dev/null; then
    echo "FAIL: node_modules/ not in .gitignore"
    exit 1
fi
echo "OK"

echo ""
echo "=== All Phase 4 checks passed ==="
