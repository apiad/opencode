import unittest
import sys
import os

# Add the script directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.gemini', 'scripts'))
from task import Task, parse_task_line, parse_tasks_file, format_task_to_line, format_tasks_to_markdown, topological_sort

class TestTaskScript(unittest.TestCase):

    # --- Parser Tests ---

    def test_parse_new_task_format(self):
        line = '- [todo] **B.1** Setup Database: Initialize the PostgreSQL schema (Complexity: 3) [Deps: ] (See plan: plans/db.md)'
        task = parse_task_line(line)
        self.assertIsNotNone(task)
        self.assertEqual(task.id, 'B.1')
        self.assertEqual(task.label, 'Setup Database')
        self.assertEqual(task.description, 'Initialize the PostgreSQL schema')
        self.assertEqual(task.complexity, 3)
        self.assertEqual(task.dependencies, [])
        self.assertEqual(task.status, 'todo')
        self.assertEqual(task.plan_path, 'plans/db.md')

    def test_parse_new_task_format_multiple_deps(self):
        line = '- [in_progress] **U.2** UI Components: Create shared buttons (Complexity: 1) [Deps: U.1, G.5]'
        task = parse_task_line(line)
        self.assertIsNotNone(task)
        self.assertEqual(task.dependencies, ['U.1', 'G.5'])
        self.assertEqual(task.status, 'in_progress')

    def test_parse_old_task_format(self):
        line = '- [ ] Implement auth system (See plan: plans/auth.md)'
        task = parse_task_line(line)
        self.assertIsNotNone(task)
        self.assertIsNone(task.id)
        self.assertEqual(task.description, 'Implement auth system')
        self.assertEqual(task.status, 'todo')
        self.assertEqual(task.plan_path, 'plans/auth.md')

    def test_parse_tasks_file_structure(self):
        content = """# Tasks

> WARNING: NEVER MODIFY BY HAND

## Active Tasks
### Backend
- [todo] **B.1** Task 1: Desc 1
- [todo] **B.2** Task 2: Desc 2

### Frontend
- [in_progress] **F.1** Task 3: Desc 3

## Archive
### Backend
- [done] **B.3** Task 4: Desc 4
"""
        tasks = parse_tasks_file(content)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].category, 'Backend')
        self.assertEqual(tasks[0].id, 'B.1')
        self.assertEqual(tasks[2].category, 'Frontend')
        self.assertEqual(tasks[3].category, 'Backend')
        self.assertEqual(tasks[3].status, 'done')

    # --- Formatting Tests ---

    def test_format_task_to_markdown_line(self):
        task = Task(
            id="T1",
            label="Task 1",
            description="Desc 1",
            category="Backend",
            complexity=1,
            dependencies=[],
            status="todo",
            plan_path="plans/t1.md"
        )
        expected_line = '- [todo] **T1** Task 1: Desc 1 (Complexity: 1) [Deps: ] (See plan: plans/t1.md)'
        formatted_line = format_task_to_line(task)
        self.assertEqual(formatted_line, expected_line)

    def test_format_task_to_markdown_line_with_zero_complexity(self):
        task = Task(
            id="T1",
            label="Task 1",
            description="Desc 1",
            category="Backend",
            complexity=0,
            dependencies=[],
            status="todo",
            plan_path="plans/t1.md"
        )
        expected_line = '- [todo] **T1** Task 1: Desc 1 [Deps: ] (See plan: plans/t1.md)'
        formatted_line = format_task_to_line(task)
        self.assertEqual(formatted_line, expected_line)

    def test_format_tasks_to_markdown_with_sorting_and_grouping(self):
        tasks = [
            Task(id="T3", label="Task C", description="Desc C", category="Frontend", complexity=1, status="done"),
            Task(id="T1", label="Task A", description="Desc A", category="Backend", complexity=2, dependencies=["T2"], status="todo"),
            Task(id="T2", label="Task B", description="Desc B", category="Backend", complexity=1, dependencies=[], status="todo"),
            Task(id="T4", label="Task D", description="Desc D", category="Frontend", complexity=2, status="in_progress"),
            Task(id="T5", label="Task E", description="Desc E", category="Backend", complexity=1, dependencies=["T1"], status="todo"),
        ]
        
        expected_markdown = """# Tasks

> **WARNING: NEVER MODIFY THIS FILE BY HAND. USE THE SCRIPT INSTEAD.**
> Run `python .gemini/scripts/task.py --help` for usage.

## Active Tasks
### Backend
- [todo] **T2** Task B: Desc B (Complexity: 1) [Deps: ]
- [todo] **T1** Task A: Desc A (Complexity: 2) [Deps: T2]
- [todo] **T5** Task E: Desc E (Complexity: 1) [Deps: T1]
### Frontend
- [in_progress] **T4** Task D: Desc D (Complexity: 2) [Deps: ]
## Archive
### Frontend
- [done] **T3** Task C: Desc C (Complexity: 1) [Deps: ]
"""
        markdown_output = format_tasks_to_markdown(tasks)
        self.assertEqual(markdown_output, expected_markdown)

    def test_format_tasks_to_markdown_with_unsorted_categories_and_mixed_statuses(self):
        tasks = [
            Task(id="T1", label="Task Alpha", description="Desc Alpha", category="Zebra", complexity=1, status="todo"),
            Task(id="T2", label="Task Beta", description="Desc Beta", category="Apple", complexity=2, dependencies=["T1"], status="in_progress"),
            Task(id="T3", label="Task Gamma", description="Desc Gamma", category="Zebra", complexity=3, status="done"),
            Task(id="T4", label="Task Delta", description="Desc Delta", category="Apple", complexity=1, status="todo"),
        ]
        
        expected_markdown = """# Tasks

> **WARNING: NEVER MODIFY THIS FILE BY HAND. USE THE SCRIPT INSTEAD.**
> Run `python .gemini/scripts/task.py --help` for usage.

## Active Tasks
### Apple
- [in_progress] **T2** Task Beta: Desc Beta (Complexity: 2) [Deps: T1]
- [todo] **T4** Task Delta: Desc Delta (Complexity: 1) [Deps: ]
### Zebra
- [todo] **T1** Task Alpha: Desc Alpha (Complexity: 1) [Deps: ]
## Archive
### Zebra
- [done] **T3** Task Gamma: Desc Gamma (Complexity: 3) [Deps: ]
"""
        markdown_output = format_tasks_to_markdown(tasks)
        self.assertEqual(markdown_output, expected_markdown)

    def test_format_tasks_to_markdown_with_no_tasks(self):
        tasks = []
        expected_markdown = """# Tasks

> **WARNING: NEVER MODIFY THIS FILE BY HAND. USE THE SCRIPT INSTEAD.**
> Run `python .gemini/scripts/task.py --help` for usage.

## Active Tasks
No active tasks.
## Archive
No archived tasks.
"""
        markdown_output = format_tasks_to_markdown(tasks)
        self.assertEqual(markdown_output, expected_markdown)

if __name__ == '__main__':
    unittest.main()
