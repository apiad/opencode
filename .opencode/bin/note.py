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

import typer
import yaml

app = typer.Typer(help="Create structured notes")
NOTES_DIR = Path(".knowledge/notes")


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

    lines = ["---", yaml_header.rstrip(), "---", "", content]

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

    # Save if requested
    if save:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        filepath = NOTES_DIR / f"{slug}.md"

        if filepath.exists():
            typer.echo(f"\nError: File already exists: {filepath}", err=True)
            raise typer.Exit(1)

        filepath.write_text(formatted)
        typer.echo(f"\n✓ Saved to: {filepath}")
    else:
        typer.echo(f"\nNote has NOT being saved. It's in draft mode. Ask the user for changes, and rerun with --save when confirmed.")


if __name__ == "__main__":
    app()
