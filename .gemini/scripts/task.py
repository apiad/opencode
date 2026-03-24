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
        self.status = status # e.g., "todo", "in_progress", "done"
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
NEW_TASK_REGEX = re.compile(
    r'^- \[(?P<status>[^\]]+)\] \*\*(?P<id>[^ ]+)\*\* (?P<label>[^:]+): (?P<description>.*?)(?: \(Complexity: (?P<complexity>\d+)\))?(?: \[Deps: (?P<dependencies>.*?)\])?(?: \(See plan: (?P<plan_path>.*?)\))?$'
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
    if not line or line.startswith('#') or line.startswith('>'):
        return None

    new_match = NEW_TASK_REGEX.match(line)
    if new_match:
        data = new_match.groupdict()
        deps_str = data.get('dependencies')
        dependencies = []
        if deps_str:
            dependencies = [dep.strip() for dep in deps_str.split(',') if dep.strip()]
        
        complexity = int(data.get('complexity')) if data.get('complexity') else 0
        return Task(
            id=data.get('id'),
            label=data.get('label'),
            description=data.get('description'),
            category=None,
            complexity=complexity,
            dependencies=dependencies,
            status=data.get('status'),
            plan_path=data.get('plan_path')
        )

    old_match = OLD_TASK_REGEX.match(line)
    if old_match:
        data = old_match.groupdict()
        status = data.get('status').strip()
        if not status: status = "todo"
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
    current_category = None
    lines = file_content.splitlines()

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("## Active Tasks"):
            current_category = None
            continue
        elif stripped_line.startswith("## Archive"):
            current_category = None
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
    if task.id is not None:
        complexity_str = f" (Complexity: {task.complexity})" if task.complexity != 0 else ""
        deps_str = f" [Deps: {', '.join(task.dependencies)}]"
        plan_path_str = f" (See plan: {task.plan_path})" if task.plan_path else ""
        return f"- [{task.status}] **{task.id}** {task.label}: {task.description}{complexity_str}{deps_str}{plan_path_str}"
    else:
        plan_path_str = f" (See plan: {task.plan_path})" if task.plan_path else ""
        return f"- [{task.status}] {task.description}{plan_path_str}"

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
    # Add tasks with IDs that were not in the sort (cycles)
    remaining_with_ids = sorted([t for t in tasks if t.id and t.id not in sorted_tasks_ids], key=lambda t: (t.complexity, t.id))
    # Add tasks without IDs
    without_ids = sorted([t for t in tasks if not t.id], key=lambda t: (t.complexity, t.description))
    
    return sorted_tasks + remaining_with_ids + without_ids

def format_tasks_to_markdown(tasks):
    active_tasks = [t for t in tasks if t.status != "done"]
    archive_tasks = [t for t in tasks if t.status == "done"]

    def group_by_category(task_list):
        grouped = defaultdict(list)
        for t in task_list:
            cat = t.category if t.category else "Uncategorized"
            grouped[cat].append(t)
        return grouped

    active_grouped = group_by_category(active_tasks)
    archive_grouped = group_by_category(archive_tasks)

    lines = [HEADER_WARNING.strip(), ""]
    
    lines.append("## Active Tasks")
    if not active_tasks:
        lines.append("No active tasks.")
    else:
        for cat in sorted(active_grouped.keys()):
            lines.append(f"### {cat}")
            for t in topological_sort(active_grouped[cat]):
                lines.append(format_task_to_line(t))
    
    lines.append("## Archive")
    if not archive_tasks:
        lines.append("No archived tasks.")
    else:
        for cat in sorted(archive_grouped.keys()):
            lines.append(f"### {cat}")
            # Archive sorted by complexity then id/description
            cat_tasks = sorted(archive_grouped[cat], key=lambda t: (t.complexity, t.id if t.id else t.description))
            for t in cat_tasks:
                lines.append(format_task_to_line(t))
    
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser(description="Task management script for TASKS.md.")
    # For now we just implement the reformat on call
    tasks_file_path = "TASKS.md"
    try:
        with open(tasks_file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        sys.exit(1)

    tasks = parse_tasks_file(content)
    formatted = format_tasks_to_markdown(tasks)
    with open(tasks_file_path, 'w') as f:
        f.write(formatted)

if __name__ == "__main__":
    main()
