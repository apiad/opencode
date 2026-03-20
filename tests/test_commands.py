import os
import tomllib
import unittest

class TestCommands(unittest.TestCase):
    def test_learn_command_exists(self):
        path = ".gemini/commands/learn.toml"
        self.assertTrue(os.path.exists(path), f"{path} does not exist")
        
    def test_learn_command_structure(self):
        path = ".gemini/commands/learn.toml"
        if not os.path.exists(path):
            self.skipTest("learn.toml does not exist yet")
        with open(path, "rb") as f:
            data = tomllib.load(f)
            self.assertIn("description", data)
            self.assertIn("prompt", data)
            self.assertGreater(len(data["description"]), 0)
            self.assertGreater(len(data["prompt"]), 0)

    def test_learner_agent_exists(self):
        path = ".gemini/agents/learner.md"
        self.assertTrue(os.path.exists(path), f"{path} does not exist")

if __name__ == "__main__":
    unittest.main()
