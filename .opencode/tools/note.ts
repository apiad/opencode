import { tool } from "@opencode-ai/plugin";
import { mkdir } from "fs/promises";

const NOTES_DIR = ".knowledge/notes";

interface NoteResult {
  frontmatter: Record<string, any>;
  body: string;
  suggested_tags: string[];
  suggested_links: string[];
  display: string;
  filename_suggestion: string;
}

function generateId(): string {
  const date = new Date().toISOString().split("T")[0];
  const random = Math.random().toString(36).substring(2, 8);
  return `${date}-${random}`;
}

function generateFilename(title: string): string {
  const slug = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
  return slug || `note-${generateId()}`;
}

function toYamlFrontmatter(data: Record<string, any>): string {
  const lines: string[] = ["---"];
  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) {
      lines.push(`${key}:`);
      for (const item of value) {
        lines.push(`  - ${item}`);
      }
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  lines.push("---");
  return lines.join("\n");
}

function structureNote(
  content: string,
  existingFrontmatter?: Record<string, any>
): NoteResult {
  // Extract or generate title
  let title = existingFrontmatter?.title || "";
  if (!title) {
    const firstLine = content.split("\n")[0].trim();
    if (firstLine.length < 100 && !firstLine.endsWith(".")) {
      title = firstLine;
    } else {
      const words = content.split(/\s+/).slice(0, 5).join(" ");
      title = words + "...";
    }
  }

  // Structure the body
  const lines = content.split("\n").filter((l) => l.trim());
  const structuredLines: string[] = [];
  let currentSection: string[] = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed === title) continue;

    // Detect headings: short, no period, capitalized
    if (
      trimmed.length < 60 &&
      !trimmed.endsWith(".") &&
      trimmed[0] === trimmed[0].toUpperCase()
    ) {
      if (currentSection.length > 0) {
        structuredLines.push("");
        structuredLines.push(...currentSection);
        currentSection = [];
      }
      structuredLines.push(`## ${trimmed}`);
    } else {
      currentSection.push(trimmed);
    }
  }

  if (currentSection.length > 0) {
    structuredLines.push("");
    structuredLines.push(...currentSection);
  }

  const body = structuredLines.join("\n").trim();

  // Suggest tags
  const contentLower = content.toLowerCase();
  const tags = new Set<string>(existingFrontmatter?.tags || []);
  
  const tagPatterns: Record<string, string[]> = {
    auth: ["auth", "oauth", "login", "authentication", "authorization"],
    api: ["api", "endpoint", "rest", "graphql"],
    design: ["design", "architecture", "pattern", "structure"],
    bug: ["bug", "issue", "fix", "error", "problem"],
    feature: ["feature", "add", "implement", "new"],
    refactor: ["refactor", "clean", "improve", "optimize"],
    test: ["test", "testing", "spec", "coverage"],
    docs: ["document", "docs", "readme", "documentation"],
  };

  for (const [tag, patterns] of Object.entries(tagPatterns)) {
    for (const pattern of patterns) {
      if (contentLower.includes(pattern)) {
        tags.add(tag);
        break;
      }
    }
  }

  // Suggest links from [[...]] and CapitalizedWords
  const links = new Set<string>();
  const linkPattern = /\[\[([^\]]+)\]\]/g;
  let match;
  while ((match = linkPattern.exec(content)) !== null) {
    links.add(`[[${match[1]}]]`);
  }

  const capitalized = content.match(/\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b/g) || [];
  for (const word of [...new Set(capitalized)]) {
    links.add(`[[${word}]]`);
  }

  const frontmatter = {
    id: existingFrontmatter?.id || generateId(),
    title,
    created: existingFrontmatter?.created || new Date().toISOString().split("T")[0],
    type: "note",
    tags: [...tags],
  };

  // Build display version
  const fullNote = `${toYamlFrontmatter(frontmatter)}\n\n# ${title}\n\n${body}`;
  
  const linksList = [...links];
  const display = `${fullNote}\n\n---\n\n**Suggested Tags:** ${[...tags].join(", ") || "none"}\n**Suggested Links:** ${linksList.join(", ") || "none"}`;

  return {
    frontmatter,
    body,
    suggested_tags: [...tags],
    suggested_links: linksList,
    display,
    filename_suggestion: generateFilename(title),
  };
}

export default tool({
  description:
    "Create and structure notes. The tool handles all formatting, tagging, and linking. " +
    "Actions: create (structure content), save (write to file), list (show notes), search (find notes). " +
    "For 'create', the tool structures the content, adds YAML frontmatter, suggests tags and [[links]], " +
    "and returns a formatted note ready for review.",
  args: {
    action: tool.schema
      .string()
      .describe('Action: "create", "save", "list", or "search"'),
    content: tool.schema
      .string()
      .optional()
      .describe("Raw content to structure (for create)"),
    mode: tool.schema
      .string()
      .optional()
      .describe('Mode for create: "draft" (return formatted) or "finalize" (save to file)'),
    title: tool.schema
      .string()
      .optional()
      .describe("Optional title override"),
    tags: tool.schema
      .string()
      .optional()
      .describe('Comma-separated tags to include'),
    modifications: tool.schema
      .string()
      .optional()
      .describe("Instructions for modifying the note (e.g., 'add section on X')"),
    filename: tool.schema
      .string()
      .optional()
      .describe("Filename without extension (for finalize mode)"),
    query: tool.schema
      .string()
      .optional()
      .describe("Search query (for search action)"),
  },
  async execute(args) {
    const action = args.action || "create";
    const mode = args.mode || "draft";

    // Ensure notes directory exists
    try {
      await mkdir(NOTES_DIR, { recursive: true });
    } catch {
      // Directory already exists
    }

    if (action === "create") {
      if (!args.content) {
        return "Error: --content is required for create action";
      }

      // Apply modifications if specified
      let content = args.content;
      if (args.modifications) {
        content = `${content}\n\n[User requested: ${args.modifications}]`;
      }

      // Build frontmatter from args
      const existingFrontmatter: Record<string, any> = {};
      if (args.title) existingFrontmatter.title = args.title;
      if (args.tags) existingFrontmatter.tags = args.tags.split(",").map((t) => t.trim()).filter(Boolean);

      const result = structureNote(content, existingFrontmatter);

      if (mode === "finalize") {
        const filename = args.filename || result.filename_suggestion;
        const filepath = `${NOTES_DIR}/${filename}.md`;

        // Check for existing file
        const file = Bun.file(filepath);
        if (await file.exists()) {
          return `Error: File ${filepath} already exists. Use a different filename.`;
        }

        const fullContent = `${toYamlFrontmatter(result.frontmatter)}\n\n# ${result.frontmatter.title}\n\n${result.body}`;
        await Bun.write(filepath, fullContent);

        return JSON.stringify({
          status: "saved",
          path: filepath,
          filename,
          frontmatter: result.frontmatter,
          preview: result.display.split("\n").slice(0, 10).join("\n") + "\n...",
        }, null, 2);
      }

      // Draft mode - return formatted note for review
      return JSON.stringify({
        status: "draft",
        frontmatter: result.frontmatter,
        body: result.body,
        full_note: `${toYamlFrontmatter(result.frontmatter)}\n\n# ${result.frontmatter.title}\n\n${result.body}`,
        suggested_tags: result.suggested_tags,
        suggested_links: result.suggested_links,
        filename_suggestion: result.filename_suggestion,
        message: "Review this note. Say 'save as <filename>' to finalize or provide modifications.",
      }, null, 2);
    }

    if (action === "save") {
      // Direct save (if content already formatted)
      if (!args.content) {
        return "Error: --content is required for save action";
      }

      const filename = args.filename || `note-${generateId()}`;
      const filepath = `${NOTES_DIR}/${filename}.md`;

      const file = Bun.file(filepath);
      if (await file.exists()) {
        return `Error: File ${filepath} already exists`;
      }

      await Bun.write(filepath, args.content);
      return `Saved note to: ${filepath}`;
    }

    if (action === "list") {
      try {
        const files = await readdir(NOTES_DIR);
        const notes = files
          .filter((f) => f.endsWith(".md"))
          .sort()
          .reverse();

        if (notes.length === 0) {
          return "No notes found";
        }

        return JSON.stringify({
          status: "success",
          count: notes.length,
          notes,
        });
      } catch {
        return "No notes directory found";
      }
    }

    if (action === "search") {
      if (!args.query) {
        return "Error: --query is required for search action";
      }

      try {
        const files = await readdir(NOTES_DIR);
        const results: string[] = [];

        for (const filename of files) {
          if (!filename.endsWith(".md")) continue;
          const content = await Bun.file(`${NOTES_DIR}/${filename}`).text();
          if (content.toLowerCase().includes(args.query.toLowerCase())) {
            results.push(filename);
          }
        }

        return JSON.stringify({
          status: "success",
          query: args.query,
          count: results.length,
          results,
        });
      } catch {
        return "No notes directory found";
      }
    }

    return `Unknown action: ${action}. Use: create, save, list, search`;
  },
});
