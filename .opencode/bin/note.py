#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "typer", "pyyaml"
# ]
# ///

"""Create structured notes.

Usage:
  uv run note --title "My Note" [--slug my-note] [--tags "tag1,tag2"] < content.txt
  uv run note --title "My Note" --save < content.txt
"""
import sys
from datetime import datetime
from pathlib import Path

import typer

app = typer.Typer(help="Create structured notes")
NOTES_DIR = Path(".knowledge/notes")


def slugify(title: str) -> str:
    """Convert title to URL-safe slug."""
    import re
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def format_note(title: str, slug: str, tags: list[str], content: str) -> str:
    """Format note with YAML frontmatter."""
    date = datetime.now().strftime("%Y-%m-%d")

    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"slug: {slug}")
    lines.append(f"date: {date}")
    lines.append("tags:")
    for tag in tags:
        lines.append(f"  - {tag}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(content)

    return "\n".join(lines)


@app.command()
def main(
    title: str = typer.Option(..., "--title", "-t", help="Note title"),
    slug: str | None = typer.Option(None, "--slug", "-s", help="URL slug (auto-generated from title if not provided)"),
    tags: str = typer.Option("", "--tags", help="Comma-separated tags"),
    save: bool = typer.Option(False, "--save", help="Save to file (prints to stdout regardless)"),
):
    """Create a structured note from stdin content."""
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
    app()
