#!/usr/bin/env python3
import os
import subprocess
import sys
from datetime import date

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

def main():
    today = date.today().strftime("%Y-%m-%d")
    journal_path = f"journal/{today}.md"

    # Scan for changes (staged, modified, untracked)
    # git status --porcelain shows all changes
    res = run_command("git status --porcelain")
    changed_files = [line[3:] for line in res.stdout.strip().splitlines() if line]

    if not changed_files:
        return 0

    # Run make
    print("Running validation (make test)...")
    res = run_command("make test")
    if res.returncode != 0:
        print("Validation failed:")
        print(res.stdout)
        print(res.stderr)
        return res.returncode

    # Calculate max(mtime) for all changed files (excluding .gemini/ and the journal)
    meaningful_changes = [f for f in changed_files if not f.startswith(".gemini/") and f != journal_path]

    if not meaningful_changes:
        return 0

    max_mtime = 0
    for f in meaningful_changes:
        if os.path.exists(f):
            mtime = os.path.getmtime(f)
            if mtime > max_mtime:
                max_mtime = mtime

    # Check journal mtime
    if not os.path.exists(journal_path):
        print(f"Error: Updated journal required (create {journal_path} with a summary of recent changes).")
        return 1

    journal_mtime = os.path.getmtime(journal_path)

    if journal_mtime < max_mtime:
        print(f"Error: Updated journal required (update {journal_path} to include a summary of recent changes).")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
