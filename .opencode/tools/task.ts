import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description: "Manage TASKS.md with CRUD operations: add, start, cancel, archive tasks, or attach plans",
  args: {
    action: tool.schema.string().describe("Action: add, start, cancel, archive, or attach-plan"),
    taskId: tool.schema.string().optional().describe("Task ID (for start, cancel, archive, attach-plan)"),
    label: tool.schema.string().optional().describe("Task label (for add)"),
    description: tool.schema.string().optional().describe("Task description (for add)"),
    category: tool.schema.string().optional().describe("Task category (for add)"),
    complexity: tool.schema.number().optional().describe("Task complexity 0-10 (for add)"),
    dependencies: tool.schema.string().optional().describe("Comma-separated task IDs (for add)"),
    planPath: tool.schema.string().optional().describe("Plan path to attach (for add or attach-plan)"),
  },
  async execute(args) {
    const script = ".opencode/tools/task.py"
    const parts = ["python3", script, args.action]

    if (args.taskId) parts.push("--task-id", args.taskId)
    if (args.label) parts.push("--label", args.label)
    if (args.description) parts.push("--description", args.description)
    if (args.category) parts.push("--category", args.category)
    if (args.complexity !== undefined) parts.push("--complexity", String(args.complexity))
    if (args.dependencies) parts.push("--dependencies", args.dependencies)
    if (args.planPath) parts.push("--plan-path", args.planPath)

    const result = await $`${parts.join(" ")}`.text()
    return result
  },
})
