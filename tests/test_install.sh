#!/usr/bin/env bash
# Test: Verify simplified install script meets requirements

set -e

SCRIPT_DIR="/home/apiad/Projects/personal/opencode"
INSTALL_SH="$SCRIPT_DIR/docs/install.sh"

echo "=== Install Script Test ==="

# Check 1: Script exists
echo -n "Checking install.sh exists... "
if [[ ! -f "$INSTALL_SH" ]]; then
    echo "FAIL: install.sh not found"
    exit 1
fi
echo "OK"

# Check 2: Script is executable
echo -n "Checking script is executable... "
if [[ ! -x "$INSTALL_SH" ]]; then
    echo "FAIL: script not executable"
    exit 1
fi
echo "OK"

# Check 3: Has banner function
echo -n "Checking banner function... "
if ! grep -q "banner\|BANNER\|OpenCode" "$INSTALL_SH"; then
    echo "FAIL: no banner found"
    exit 1
fi
echo "OK"

# Check 4: Checks git
echo -n "Checking git check... "
if ! grep -q "git" "$INSTALL_SH"; then
    echo "FAIL: no git check"
    exit 1
fi
echo "OK"

# Check 5: Checks uv
echo -n "Checking uv check... "
if ! grep -q "uv" "$INSTALL_SH"; then
    echo "FAIL: no uv check"
    exit 1
fi
echo "OK"

# Check 6: Checks opencode binary
echo -n "Checking opencode binary check... "
if ! grep -q "opencode" "$INSTALL_SH"; then
    echo "FAIL: no opencode binary check"
    exit 1
fi
echo "OK"

# Check 7: Checks git status is clean
echo -n "Checking git status clean check... "
if ! grep -q "git status\|status --porcelain" "$INSTALL_SH"; then
    echo "FAIL: no git status clean check"
    exit 1
fi
echo "OK"

# Check 8: Has copy mode
echo -n "Checking copy mode... "
if ! grep -q "clone\|copy" "$INSTALL_SH"; then
    echo "FAIL: no copy mode"
    exit 1
fi
echo "OK"

# Check 9: Has link/submodule mode
echo -n "Checking link/submodule mode... "
if ! grep -q "submodule\|link" "$INSTALL_SH"; then
    echo "FAIL: no link/submodule mode"
    exit 1
fi
echo "OK"

# Check 10: Creates .knowledge directories
echo -n "Checking .knowledge directory creation... "
if ! grep -q "mkdir.*.knowledge\|.knowledge.*mkdir" "$INSTALL_SH"; then
    echo "FAIL: no .knowledge directory creation"
    exit 1
fi
echo "OK"

# Check 11: References opencode-core
echo -n "Checking opencode-core reference... "
if ! grep -q "opencode-core" "$INSTALL_SH"; then
    echo "FAIL: no opencode-core reference"
    exit 1
fi
echo "OK"

# Check 12: Has prompt for mode selection
echo -n "Checking mode selection prompt... "
if ! grep -qE "mode|choose|select" "$INSTALL_SH"; then
    echo "FAIL: no mode selection prompt"
    exit 1
fi
echo "OK"

# Check 13: Script length is reasonable (< 200 lines)
LINE_COUNT=$(wc -l < "$INSTALL_SH")
echo -n "Checking script length (${LINE_COUNT} lines)... "
if [[ "$LINE_COUNT" -gt 200 ]]; then
    echo "FAIL: script too long (> 200 lines)"
    exit 1
fi
echo "OK"

echo ""
echo "=== All install script tests passed ==="
