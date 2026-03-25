#!/usr/bin/env python3

import re
import sys
import argparse
from collections import defaultdict, deque

class Task:
    def __init__(self, id=None, label=None, description=None, category=None, complexity=0, dependencies=None, status="todo", plan_path=None):
        self.id = id
        self.label = label
        self.description = description
        self.category = category
        self.complexity = complexity
        self.dependencies = dependencies if dependencies is not None else []
        self.status = status # e.g., "todo", "in_progress", "done", "cancelled"
        self.plan_path = plan_path

    def __repr__(self):
        return (f"Task(id={self.id!r}, label={self.label!r}, description={self.description!r}, category={self.category!r}, "
                f"complexity={self.complexity!r}, dependencies={self.dependencies!r}, status={self.status!r}, plan_path={self.plan_path!r})")

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (self.id == other.id and
                self.label == other.label and
                self.description == other.description and
                self.category == other.category and
                self.complexity == other.complexity and
                self.dependencies == other.dependencies and
                self.status == other.status and
                self.plan_path == other.plan_path)

# --- Regex Patterns ---
# New format: - [Status] **[ID]** Label: Description (Complexity: X) [Deps: Y] (See plan: Z)
# Note: Label is optional in some contexts but the script expects it for new format
NEW_TASK_REGEX = re.compile(
    r'^- \[(?P<status>[^\]]*)\] \*\*(?P<id>[^ ]+)\*\*(?: (?P<label>[^:]+):)? (?P<description>.*?)(?: \(Complexity: (?P<complexity>\d+)\))?(?: \[Deps: (?P<dependencies>.*?)\])?(?: \(See plan: (?P<plan_path>.*?)\))?$'
)
# Old format: - [ ] Description (See plan: ...)
OLD_TASK_REGEX = re.compile(
    r'^- \[(?P<status>[^\]]*)\] (?P<description>.*?)(?: \(See plan: (?P<plan_path>.*?)\))?$'
)

HEADER_WARNING = """# Tasks

> **WARNING: NEVER MODIFY THIS FILE BY HAND. USE THE SCRIPT INSTEAD.**
> Run `python .gemini/scripts/task.py --help` for usage.
"""

# --- Parser Functions ---

def parse_task_line(line):
    line = line.strip()
    if not line or not line.startswith('- ['):
        return None

    new_match = NEW_TASK_REGEX.match(line)
    if new_match:
        data = new_match.groupdict()
        deps_str = data.get('dependencies')
        dependencies = []
        if deps_str:
            dependencies = [dep.strip() for dep in deps_str.split(',') if dep.strip()]
        
        complexity = int(data.get('complexity')) if data.get('complexity') else 0
        
        status_char = data.get('status')
        status_map = {" ": "todo", "/": "in_progress", "x": "done", "-": "cancelled"}
        status = status_map.get(status_char, "todo")

        label = data.get('label')
        if label:
            label = label.strip()

        return Task(
            id=data.get('id'),
            label=label,
            description=data.get('description').strip(),
            category=None,
            complexity=complexity,
            dependencies=dependencies,
            status=status,
            plan_path=data.get('plan_path')
        )

    old_match = OLD_TASK_REGEX.match(line)
    if old_match:
        data = old_match.groupdict()
        status_char = data.get('status').strip()
        if status_char == 'x': status = "done"
        elif status_char == '/': status = "in_progress"
        elif status_char == '-': status = "cancelled"
        else: status = "todo"

        return Task(
            id=None,
            label=None,
            description=data.get('description'),
            category=None,
            complexity=0,
            dependencies=[],
            status=status,
            plan_path=data.get('plan_path')
        )
    return None

def parse_tasks_file(file_content):
    tasks = []
    current_category = "General"
    lines = file_content.splitlines()

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith("## Active Tasks"):
            continue
        elif stripped_line.startswith("## Archive"):
            continue
        elif stripped_line.startswith("### "):
            current_category = stripped_line[4:].strip()
            continue
        
        task = parse_task_line(line)
        if task:
            task.category = current_category
            tasks.append(task)
    return tasks

# --- Formatter Functions ---

def format_task_to_line(task):
    status_map = {"todo": " ", "in_progress": "/", "done": "x", "cancelled": "-"}
    status_str = status_map.get(task.status, task.status)
    
    if task.id is not None:
        complexity_str = f" (Complexity: {task.complexity})" if task.complexity != 0 else ""
        deps_str = ""
        if task.dependencies: # Only add [Deps: ...] if there are dependencies
            deps_str = f" [Deps: {', '.join(task.dependencies)}]"
        plan_path_str = f" (See plan: {task.plan_path})" if task.plan_path else ""
        label_str = f" {task.label}:" if task.label else ""
        return f"- [{status_str}] **{task.id}**{label_str} {task.description}{complexity_str}{deps_str}{plan_path_str}"
    else:
        plan_path_str = f" (See plan: {task.plan_path})" if task.plan_path else ""
        return f"- [{status_str}] {task.description}{plan_path_str}"

def topological_sort(tasks):
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    task_map = {task.id: task for task in tasks if task.id}

    for tid in task_map:
        in_degree[tid] = 0

    for task in tasks:
        if task.id:
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    adj[dep_id].append(task.id)
                    in_degree[task.id] += 1

    queue = deque(sorted([tid for tid in in_degree if in_degree[tid] == 0]))
    sorted_tasks_ids = []

    while queue:
        u = queue.popleft()
        sorted_tasks_ids.append(u)
        for v in sorted(adj[u]):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    sorted_tasks = [task_map[tid] for tid in sorted_tasks_ids]
    remaining_with_ids = sorted([t for t in tasks if t.id and t.id not in sorted_tasks_ids], key=lambda t: (t.complexity, t.id))
    without_ids = sorted([t for t in tasks if not t.id], key=lambda t: (t.complexity, t.description))
    
    return sorted_tasks + remaining_with_ids + without_ids

def format_tasks_to_markdown(tasks):
    active_tasks = [t for t in tasks if t.status != "done"]
    archive_tasks = [t for t in tasks if t.status == "done"]

    def group_by_category(task_list):
        grouped = defaultdict(list)
        for t in task_list:
            cat = t.category if t.category else "General"
            grouped[cat].append(t)
        return grouped

    active_grouped = group_by_category(active_tasks)
    archive_grouped = group_by_category(archive_tasks)

    lines = [HEADER_WARNING.strip(), ""]
    
    lines.append("## Active Tasks")
    if not active_tasks:
        lines.append("No active tasks.")
    else:
        # Sort categories alphabetically for consistent output
        for cat in sorted(active_grouped.keys()):
            lines.append("")
            lines.append(f"### {cat}")
            for t in topological_sort(active_grouped[cat]):
                lines.append(format_task_to_line(t))
    
    lines.append("")
    lines.append("## Archive")
    if not archive_tasks:
        lines.append("No archived tasks.")
    else:
        # Sort categories alphabetically for consistent output
        for cat in sorted(archive_grouped.keys()):
            lines.append("")
            lines.append(f"### {cat}")
            cat_tasks = sorted(archive_grouped[cat], key=lambda t: (t.complexity, t.id if t.id else t.description))
            for t in cat_tasks:
                lines.append(format_task_to_line(t))
    
    return "\n".join(lines) + "\n"

def generate_next_task_id(tasks, category):
    prefix = category[0].upper()
    max_num = 0
    for task in tasks:
        if task.id and task.id.startswith(prefix + "."):
            try:
                num_part = task.id.split('.')[-1]
                current_num = int(num_part)
                if current_num > max_num:
                    max_num = current_num
            except ValueError:
                continue
    return f"{prefix}.{max_num + 1}"

def add_task(tasks, label, description, category, complexity, dependencies, plan_path):
    new_task_id = generate_next_task_id(tasks, category)
    new_task = Task(
        id=new_task_id,
        label=label,
        description=description,
        category=category,
        complexity=complexity,
        dependencies=dependencies,
        status='todo',
        plan_path=plan_path
    )
    tasks.append(new_task)
    return tasks

# --- New Functionality ---

def update_task(tasks, task_id, **kwargs):
    """
    Searches for a task by its ID and updates the specified attributes.
    If the task is not found, prints a warning to sys.stderr.
    Returns the potentially modified list of tasks.
    """
    task_found = False
    for task in tasks:
        if task.id == task_id:
            for key, value in kwargs.items():
                setattr(task, key, value)
            task_found = True
            break # Assuming task IDs are unique
    if not task_found:
        print(f"Warning: Task with ID {task_id} not found.", file=sys.stderr)
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Task management script for TASKS.md.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('--label', required=True)
    parser_add.add_argument('--description', required=True)
    parser_add.add_argument('--category', required=True)
    parser_add.add_argument('--complexity', type=int, default=0)
    parser_add.add_argument('--dependencies', type=str, default="")
    parser_add.add_argument('--plan-path', type=str, default=None)

    # New commands: start, cancel, archive, attach-plan
    parser_start = subparsers.add_parser('start', help='Set task status to in_progress')
    parser_start.add_argument('--task-id', required=True)

    parser_cancel = subparsers.add_parser('cancel', help='Set task status to cancelled')
    parser_cancel.add_argument('--task-id', required=True)

    parser_archive = subparsers.add_parser('archive', help='Set task status to done')
    parser_archive.add_argument('--task-id', required=True)

    parser_attach_plan = subparsers.add_parser('attach-plan', help='Set the task\'s plan path')
    parser_attach_plan.add_argument('--task-id', required=True)
    parser_attach_plan.add_argument('--plan-path', required=True)

    args = parser.parse_args()

    # Use environment variable to override TASKS.md for testing
    import os
    tasks_file_path = os.environ.get("GEMINI_TASKS_FILE", "TASKS.md")

    try:
        with open(tasks_file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = HEADER_WARNING + "\n"

    tasks = parse_tasks_file(content)

    # Migration: Assign IDs to tasks that don't have them
    for task in tasks:
        if task.id is None:
            task.id = generate_next_task_id(tasks, task.category if task.category else "General")

    if args.command == 'add':
        deps = [d.strip() for d in args.dependencies.split(',') if d.strip()]
        tasks = add_task(tasks, args.label, args.description, args.category, args.complexity, deps, args.plan_path)
    
    # Handle new commands
    elif args.command == 'start':
        tasks = update_task(tasks, args.task_id, status="in_progress")
    elif args.command == 'cancel':
        tasks = update_task(tasks, args.task_id, status="cancelled")
    elif args.command == 'archive':
        tasks = update_task(tasks, args.task_id, status="done")
    elif args.command == 'attach-plan':
        tasks = update_task(tasks, args.task_id, plan_path=args.plan_path)

    formatted = format_tasks_to_markdown(tasks)
    with open(tasks_file_path, 'w') as f:
        f.write(formatted)

if __name__ == "__main__":
    main()
