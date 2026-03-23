import os

def test_reviewer_agent_exists():
    assert os.path.exists(".gemini/agents/reviewer.md")

def test_editor_agent_gone():
    assert not os.path.exists(".gemini/agents/editor.md")

def test_review_command_exists():
    assert os.path.exists(".gemini/commands/review.toml")

def test_revise_command_gone():
    assert not os.path.exists(".gemini/commands/revise.toml")

if __name__ == "__main__":
    # Simple manual runner for now
    try:
        test_reviewer_agent_exists()
        test_editor_agent_gone()
        test_review_command_exists()
        test_revise_command_gone()
        print("Tests Passed")
    except AssertionError as e:
        print(f"Test Failed: {e}")
        exit(1)
