#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: journal.py <description>")
        sys.exit(1)

    description = " ".join(sys.argv[1:])
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    today = now.strftime("%Y-%m-%d")
    
    os.makedirs("journal", exist_ok=True)
    journal_path = f"journal/{today}.md"
    
    entry = f"[{timestamp}] - {description}\n"
    
    with open(journal_path, "a") as f:
        f.write(entry)
    
    print(f"Added journal entry: {entry.strip()}")

if __name__ == "__main__":
    main()
