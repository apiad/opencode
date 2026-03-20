#!/usr/bin/env python3
import os
import subprocess
import sys
from datetime import date, datetime

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

def main():
    today = date.today().strftime("%Y-%m-%d")
    journal_path = f"journal/{today}.md"

    # Scan for changes (staged, modified, untracked)
    res = run_command("git status --porcelain")
    changed_files = [line[3:] for line in res.stdout.strip().splitlines() if line]

    if not changed_files:
        return 0

    # Run make test (if makefile exists)
    if os.path.exists("makefile"):
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
        # git status might show deleted files, check if exists
        if os.path.exists(f):
            mtime = os.path.getmtime(f)
            if mtime > max_mtime:
                max_mtime = mtime

    # Check journal entry
    if not os.path.exists(journal_path):
        print(f"Error: Updated journal required. Please read the latest entries in journal/ to understand context,")
        print(f"then use: python3 .gemini/scripts/journal.py 'one line summary of changes'")
        return 1

    with open(journal_path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if not lines:
        print(f"Error: Journal {journal_path} is empty.")
        print(f"Please use: python3 .gemini/scripts/journal.py 'one line summary of changes'")
        return 1

    last_line = lines[-1]
    # Expected format: [timestamp ISO] - description
    if not (last_line.startswith("[") and "] - " in last_line):
        print(f"Error: Invalid journal entry format in {journal_path}: '{last_line}'")
        print(f"Expected format: '[YYYY-MM-DDTHH:MM:SS] - description'")
        print(f"Please use: python3 .gemini/scripts/journal.py 'one line summary of changes'")
        return 1

    try:
        ts_str = last_line[1:last_line.index("]")]
        last_entry_time = datetime.fromisoformat(ts_str).timestamp()
    except (ValueError, IndexError):
        print(f"Error: Could not parse timestamp from journal entry: '{last_line}'")
        print(f"Please use: python3 .gemini/scripts/journal.py 'one line summary of changes'")
        return 1

    if last_entry_time < max_mtime:
        print(f"Error: Last journal entry is older than recent changes.")
        print(f"Please read {journal_path} to catch up, then add a summary of your latest work using:")
        print(f"python3 .gemini/scripts/journal.py 'one line summary of changes'")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
