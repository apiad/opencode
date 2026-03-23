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

def test_review_command_is_multiphase():
    with open(".gemini/commands/review.toml", "r") as f:
        content = f.read()
    assert "Phase 1" in content
    assert "Phase 2" in content
    assert "Phase 3" in content
    assert "reviewer" in content

def test_draft_command_suggests_review():
    with open(".gemini/commands/draft.toml", "r") as f:
        content = f.read()
    assert "/review" in content
    assert "/revise" not in content

def test_docs_updated():
    files_to_check = ["README.md", ".gemini/style-guide.md", "docs/user-guide.md", "docs/design.md"]
    for f_path in files_to_check:
        with open(f_path, "r") as f:
            content = f.read()
        assert "review" in content.lower()
        assert "reviewer" in content.lower()
        assert "writer" in content.lower()
        assert "reporter" not in content.lower()

def test_writer_agent_exists():
    assert os.path.exists(".gemini/agents/writer.md")

def test_reporter_agent_gone():
    assert not os.path.exists(".gemini/agents/reporter.md")

def test_writer_agent_has_replace():
    with open(".gemini/agents/writer.md", "r") as f:
        content = f.read()
    assert "replace" in content

def test_draft_command_is_multimode():
    with open(".gemini/commands/draft.toml", "r") as f:
        content = f.read()
    assert "Refinement" in content
    assert "Initial Drafting" in content
    assert "writer" in content
    assert "reporter" not in content

def test_maintenance_command_is_audit():
    with open(".gemini/commands/maintenance.toml", "r") as f:
        content = f.read()
    assert "codebase_investigator" in content
    assert "Maintenance Report Card" in content
    assert "research/maintainance-report-" in content
    assert "Phase 3" in content
    # Ensure it doesn't mention Step-by-Step Implementation or modification
    assert "Step-by-Step Implementation" not in content

if __name__ == "__main__":
    # Simple manual runner for now
    try:
        test_reviewer_agent_exists()
        test_editor_agent_gone()
        test_review_command_exists()
        test_revise_command_gone()
        test_reviewer_agent_has_grep_search()
        test_review_command_is_multiphase()
        test_draft_command_suggests_review()
        test_docs_updated()
        
        test_writer_agent_exists()
        test_reporter_agent_gone()
        test_writer_agent_has_replace()
        test_draft_command_is_multimode()

        test_maintenance_command_is_audit()
        
        print("Tests Passed")
    except AssertionError as e:
        print(f"Test Failed: {e}")
        exit(1)
