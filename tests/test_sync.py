import os
import re
import pytest

def get_commands():
    return [f.replace(".toml", "") for f in os.listdir(".gemini/commands/") if f.endswith(".toml")]

def get_agents():
    return [f.replace(".md", "") for f in os.listdir(".gemini/agents/") if f.endswith(".md")]

def test_commands_synced_in_readme():
    commands = get_commands()
    with open("README.md", "r") as f:
        content = f.read()
    for cmd in commands:
        assert f"/{cmd}" in content

def test_commands_synced_in_user_guide():
    commands = get_commands()
    with open("docs/user-guide.md", "r") as f:
        content = f.read()
    for cmd in commands:
        assert f"/{cmd}" in content

def test_no_legacy_docs_command():
    # Only checks documentation files where /docs might be mentioned as a command.
    files_to_check = ["README.md", "docs/index.md", "docs/user-guide.md"]
    for file_path in files_to_check:
        with open(file_path, "r") as f:
            content = f.read()
        # Should not mention /docs as a command (e.g., /docs followed by space or end of line or punctuation)
        # Avoid matching /docs/ in a path.
        assert not re.search(r"/docs[ \t\r\n\.,\?!\)\}\]]", content)
