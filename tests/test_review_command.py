import os

def test_reviewer_agent_exists():
    assert os.path.exists(".gemini/agents/reviewer.md")

def test_editor_agent_gone():
    assert not os.path.exists(".gemini/agents/editor.md")

def test_review_command_exists():
    assert os.path.exists(".gemini/commands/review.toml")

def test_revise_command_gone():
    assert not os.path.exists(".gemini/commands/revise.toml")

def test_reviewer_agent_has_grep_search():
    with open(".gemini/agents/reviewer.md", "r") as f:
        content = f.read()
    assert "grep_search" in content

if __name__ == "__main__":
    # Simple manual runner for now
    try:
        test_reviewer_agent_exists()
        test_editor_agent_gone()
        test_review_command_exists()
        test_revise_command_gone()
        test_reviewer_agent_has_grep_search()
        print("Tests Passed")
    except AssertionError as e:
        print(f"Test Failed: {e}")
        exit(1)
