# /note Command

Transform raw thoughts into structured, Obsidian-compatible notes.

## Usage

```
/note <your raw thoughts>
```

## Flow

1. **Create** - User provides raw content
2. **Structure** - Tool structures into YAML + Markdown with tags and [[links]]
3. **Review** - Model presents formatted note
4. **Iterate** - User can request modifications (re-runs tool)
5. **Save** - User says "save" → Tool writes to file

## Tool Actions

### `create` - Structure content

```typescript
note_tool(
  action: "create",
  content: "your raw thoughts...",
  mode: "draft",           // Returns formatted note for review
  title?: string,          // Optional title override
  tags?: string,           // Comma-separated tags
  modifications?: string    // Instructions for changes
)
```

Returns:
- `frontmatter` - YAML metadata (id, title, created, type, tags)
- `body` - Structured markdown body
- `suggested_tags` - Auto-detected tags
- `suggested_links` - Detected [[WikiLinks]]
- `filename_suggestion` - Auto-generated filename

### `create` with `mode: "finalize"` - Save directly

```typescript
note_tool(
  action: "create",
  content: "...",
  mode: "finalize",
  filename?: string        // Optional, auto-generated if not provided
)
```

### Other actions

- `save` - Write pre-formatted content directly
- `list` - Show existing notes
- `search` - Search note contents

## Example Session

```
User: /note "I was thinking about the auth flow. We need to handle OAuth2 
            and API keys. Error handling is important but I'm not sure 
            where it fits."

Model: [Calls note_tool(action="create", content="...", mode="draft")]

---
id: 2026-03-27-a1b2c3
title: Auth Flow Design Thoughts
created: 2026-03-27
type: note
tags:
  - auth
  - oauth
  - api
---

## Auth Flow Design Thoughts

## Authentication Methods
We need to handle OAuth2 and API keys for the new feature.

## Error Handling Questions
Error handling is important but I'm not sure where it fits.

**Suggested Tags:** auth, oauth, api  
**Suggested Links:** [[OAuth2]], [[API Keys]], [[Error Handling]]  
**Suggested Filename:** auth-flow-design-thoughts

Want me to save this, or would you like modifications?

User: Add a section about OAuth2 implementation details

Model: [Calls note_tool(action="create", content="...", mode="draft", 
                       modifications="Add section about OAuth2 implementation")]

[Returns updated note with new section]

User: Save as auth-design

Model: [Calls note_tool(action="create", content="...", mode="finalize", 
                       filename="auth-design")]

✅ Saved to .knowledge/notes/auth-design.md
```

## How It Works

The **tool** does all the work:
- Parses raw content
- Extracts/generates title
- Structures into sections (## headings)
- Generates YAML frontmatter
- Suggests tags based on keywords
- Identifies [[WikiLinks]]
- Formats Obsidian-compatible output

The **model** just:
- Calls the tool
- Presents the result
- Handles user feedback
- Re-calls tool for modifications

## Output Location

All notes saved to: `.knowledge/notes/<filename>.md`

## Related

- [[.knowledge]] - Knowledge directory
- [[/research]] - Deep research (requires workflow state)
- [[/plan]] - Structured planning (requires workflow state)
