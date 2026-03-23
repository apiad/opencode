import toml

def test_task_command_delegates_to_coder():
    with open(".gemini/commands/task.toml", "r") as f:
        config = toml.loads(f.read())
    
    prompt = config["prompt"]
    # Check that the "work" action (usually in the prompt) mentions delegation to the coder
    assert "coder" in prompt.lower()
    assert "subagent" in prompt.lower()
    assert "delegate" in prompt.lower()
