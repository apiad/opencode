#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "typer", "pyyaml"
# ]
# ///

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
import yaml

NOTES_DIR = Path(".knowledge/notes")

USAGE = """Create structured notes from stdin content.

USAGE:
  uv run note --title "My Note" [--slug my-note] [--tags "tag1,tag2"] < content.txt
  uv run note --title "My Note" --save < content.txt
  echo "Content..." | uv run note --title "Title" --tags "tag1"

OPTIONS:
  --title, -t TEXT     Note title (required)
  --slug, -s TEXT      URL slug (auto-generated from title if not provided)
  --tags TEXT          Comma-separated tags (optional)
  --save               Save to file (prints to stdout regardless)

OUTPUT:
  Always prints formatted note with YAML frontmatter to stdout.
  With --save, also writes to .knowledge/notes/<slug>.md

EXAMPLES:
  # Preview a note
  echo "Auth thoughts..." | uv run note --title "Auth Design" --tags "auth,design"

  # Save a note
  echo "Auth thoughts..." | uv run note --title "Auth Design" --save

  # Custom slug
  echo "Content..." | uv run note --title "Auth Design" --slug auth-2024
"""


def show_usage():
    print(USAGE, file=sys.stderr)
    raise typer.Exit(1)


def slugify(title: str) -> str:
    """Convert title to URL-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def format_note(title: str, slug: str, tags: list[str], content: str) -> str:
    """Format note with YAML frontmatter."""
    date = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "title": title,
        "slug": slug,
        "date": date,
        "tags": tags,
    }

    yaml_header = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False)

    return "\n".join(["---", yaml_header.rstrip(), "---", "", f"# {title}", "", content])


def main(
    title: Optional[str] = typer.Option(None, "--title", "-t", help="Note title"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="URL slug (auto-generated from title if not provided)"),
    tags: str = typer.Option("", "--tags", help="Comma-separated tags"),
    save: bool = typer.Option(False, "--save", help="Save to file (prints to stdout regardless)"),
):
    """Create a structured note from stdin content."""
    # Show usage if no title provided
    if title is None:
        show_usage()
    
    # After show_usage() check, title is guaranteed to be str
    title_str: str = title

    # Read content from stdin
    content = sys.stdin.read().strip()

    if not content:
        typer.echo("Error: No content provided via stdin", err=True)
        raise typer.Exit(1)

    # Generate slug if not provided
    if not slug:
        slug = slugify(title)

    # Parse tags
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    # Format the note
    formatted = format_note(title, slug, tag_list, content)

    # Print to stdout
    print(formatted)

    # Save if requested
    if save:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        filepath = NOTES_DIR / f"{slug}.md"

        if filepath.exists():
            typer.echo(f"\nError: File already exists: {filepath}", err=True)
            raise typer.Exit(1)

        filepath.write_text(formatted)
        typer.echo(f"\n✓ Saved to: {filepath}")


if __name__ == "__main__":
    typer.run(main)
