import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description: "Add a journal entry with timestamp for today's date",
  args: {
    description: tool.schema.string().describe("Journal entry description"),
  },
  async execute(args) {
    const script = ".opencode/tools/journal.py"
    const result = await $`python3 ${script} ${args.description}`.text()
    return result
  },
})
