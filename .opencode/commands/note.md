# /note Command

Create structured notes from content via stdin.

## Usage

```
/note --title "Title" [--tags "tag1,tag2"] [--save]
```

## How It Works

Model pipes content to `note.py` via stdin:

```bash
echo "Note content..." | uv run note --title "Title" --tags "tag1"
```

## CLI Options

- `--title, -t` (required) - Note title
- `--slug, -s` (optional) - URL slug (auto-generated from title)  
- `--tags` (optional) - Comma-separated tags
- `--save` (flag) - Save to file (always prints to stdout)

## Example

```
User: /note "Auth Design Thoughts"

Model: echo "I was thinking about auth flow. We need OAuth2..." | \
       uv run note --title "Auth Design Thoughts" --tags "auth,design"

Output:
---
title: "Auth Design Thoughts"
slug: auth-design-thoughts
date: 2026-03-27
tags:
  - auth
  - design
---

# Auth Design Thoughts

I was thinking about auth flow. We need OAuth2...

User: Save it

Model: [re-runs with --save flag]
```

## Output

Always prints YAML frontmatter + Markdown to stdout:

```yaml
---
title: "My Title"
slug: my-title
date: 2026-03-27
tags:
  - tag1
  - tag2
---

# My Title

Content from stdin...
```

With `--save`, also writes to: `.knowledge/notes/<slug>.md`

## Script Location

`.opencode/bin/note.py` (inline script with uv dependencies)
