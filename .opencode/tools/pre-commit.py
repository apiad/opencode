#!/usr/bin/env python3
import os
import subprocess
import sys
import re
from datetime import date, datetime

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True, stdin=subprocess.DEVNULL)
    return result

def main():
    today = date.today().strftime("%Y-%m-%d")
    journal_path = f"journal/{today}.yaml"

    res = run_command("git status --porcelain")
    changed_files = [line[3:] for line in res.stdout.strip().splitlines() if line]

    if not changed_files:
        return 0

    # Check if ONLY journal files changed - auto-commit and return
    journal_files = [f for f in changed_files if f.startswith("journal/")]
    # Normalize paths - .opencode appears as opencode in git status
    normalized = [f.lstrip(".") for f in changed_files]
    meaningful_files = [f for f in normalized if not f.startswith("journal/") and not f.startswith("gemini") and not f.startswith("opencode")]

    if journal_files and not meaningful_files:
        print("Journal-only change detected. Auto-committing...")
        res = run_command('git add journal/ && git commit -m "chore: update journal"')
        if res.returncode != 0:
            print(f"Auto-commit failed:\n{res.stdout}\n{res.stderr}")
            return 1
        print("Journal committed successfully.")
        return 0

    if os.path.exists("makefile"):
        print("Running validation (make test)...")
        res = run_command("make test")
        if res.returncode != 0:
            print("Validation failed:")
            print(res.stdout)
            print(res.stderr)
            return res.returncode

    meaningful_changes = [f for f in changed_files if not f.lstrip(".").startswith("gemini") and not f.lstrip(".").startswith("opencode") and f != journal_path and not f.endswith(".yaml")]

    if not meaningful_changes:
        return 0

    max_mtime = 0
    for f in meaningful_changes:
        if os.path.exists(f):
            mtime = os.path.getmtime(f)
            if mtime > max_mtime:
                max_mtime = mtime

    if not os.path.exists(journal_path):
        print(f"Error: Updated journal required. Please read the latest entries in journal/ to understand context,")
        print(f"then use: journal add \"one line summary of changes\"")
        return 1

    with open(journal_path, "r") as f:
        content = f.read()

    # Parse YAML to find last timestamp
    # Look for pattern: timestamp: "YYYY-MM-DDTHH:MM:SS"
    timestamps = re.findall(r'timestamp: "(.+)"', content)
    
    if not timestamps:
        print(f"Error: No journal entries found in {journal_path}")
        print(f"Please use: journal add \"one line summary of changes\"")
        return 1

    try:
        last_entry_time = datetime.fromisoformat(timestamps[-1]).timestamp()
    except (ValueError, IndexError):
        print(f"Error: Could not parse timestamp from journal entry: '{timestamps[-1]}'")
        print(f"Please use: journal add \"one line summary of changes\"")
        return 1

    if last_entry_time < max_mtime:
        print(f"Error: Last journal entry is older than recent changes.")
        print(f"Please read {journal_path} to catch up, then add a summary of your latest work using:")
        print(f"journal add \"one line summary of changes\"")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
