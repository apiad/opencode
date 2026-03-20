import os
import unittest
import subprocess
import shutil
import time
from datetime import date

class TestPreCommitHook(unittest.TestCase):
    def setUp(self):
        self.test_dir = "temp_test_repo"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        os.chdir(self.test_dir)
        subprocess.run(["git", "init"], capture_output=True)
        # Configure user for testing
        subprocess.run(["git", "config", "user.email", "test@example.com"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True)
        
        os.makedirs(".gemini/hooks")
        os.makedirs("journal")
        
        # Initial commit
        with open(".gitignore", "w") as f:
            f.write("temp_test_repo/\n")
        subprocess.run(["git", "add", ".gitignore"], capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], capture_output=True)
        
    def tearDown(self):
        os.chdir("..")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_journal_mtime_validation(self):
        # Create a journal entry
        today = date.today().strftime("%Y-%m-%d")
        journal_path = f"journal/{today}.md"
        with open(journal_path, "w") as f:
            f.write("Journal entry")
        
        # Ensure mtime is set
        time.sleep(0.1)
        
        # Create a modified file
        with open("code.py", "w") as f:
            f.write("Code change")
            
        # Hook should fail because code.py is newer than journal
        # We'll run the pre-commit hook script directly
        result = subprocess.run(["python3", "../.gemini/hooks/pre-commit.py"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Updated journal required", result.stdout + result.stderr)

    def test_journal_mtime_validation_success(self):
        # Add a dummy makefile to the test repo to avoid failure when running make test
        with open("makefile", "w") as f:
            f.write("test:\n\t@echo 'Tests passed'")
            
        # Create a modified file
        with open("code.py", "w") as f:
            f.write("Code change")
            
        # Create a journal entry AFTER the file modification
        time.sleep(0.1)
        today = date.today().strftime("%Y-%m-%d")
        journal_path = f"journal/{today}.md"
        with open(journal_path, "w") as f:
            f.write("Journal entry updated")
            
        # Hook should succeed
        result = subprocess.run(["python3", "../.gemini/hooks/pre-commit.py"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Validation passed", result.stdout)

    def test_make_failure(self):
        # Add a failing makefile
        with open("makefile", "w") as f:
            f.write("test:\n\t@exit 1")
            
        # Create a journal entry
        today = date.today().strftime("%Y-%m-%d")
        journal_path = f"journal/{today}.md"
        with open(journal_path, "w") as f:
            f.write("Journal entry")
            
        # Ensure journal is newest
        time.sleep(0.1)
        os.utime(journal_path, None)
        
        # Hook should fail because make test fails
        result = subprocess.run(["python3", "../.gemini/hooks/pre-commit.py"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Validation failed", result.stdout)

    def test_ignore_gemini_files(self):
        # Create a journal entry
        today = date.today().strftime("%Y-%m-%d")
        journal_path = f"journal/{today}.md"
        with open(journal_path, "w") as f:
            f.write("Journal entry")
            
        time.sleep(0.1)
        
        # Modify a .gemini file
        with open(".gemini/settings.json", "w") as f:
            f.write("{}")
            
        # Hook should succeed because .gemini file is ignored in mtime check
        result = subprocess.run(["python3", "../.gemini/hooks/pre-commit.py"], capture_output=True, text=True)
        # It might fail because make test fails (no makefile)
        # But it shouldn't fail with "Updated journal required"
        self.assertNotIn("Updated journal required", result.stdout + result.stderr)

    def test_install_hooks(self):
        # Create a dummy pre-commit script in the test repo so the symlink is not dangling
        os.makedirs(".gemini/hooks", exist_ok=True)
        with open(".gemini/hooks/pre-commit.py", "w") as f:
            f.write("#!/usr/bin/env python3\npass")
            
        # Create a makefile with install-hooks target (the one we'll implement)
        # For now, we'll use the real makefile from the project
        shutil.copy("../makefile", "makefile")
        
        # Run make install-hooks
        result = subprocess.run(["make", "install-hooks"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        
        # Check if the hook is linked
        hook_path = ".git/hooks/pre-commit"
        self.assertTrue(os.path.exists(hook_path))
        self.assertTrue(os.access(hook_path, os.X_OK))

if __name__ == "__main__":
    unittest.main()
