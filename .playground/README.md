# Playground Directory

This folder is used for experimentation and temporary work.

- **Never committed to git** — automatically ignored
- **Never auto-purged** — user decides when to clean up
- **Analyze mode: read-write** — experiment freely here
- **Design mode: read-only** — no experiments in design mode
- **Create mode: read-write** — can experiment if needed

## Subfolders

- `tests/` — tester subagent writes hypothesis validation tests here
- `drafts/` — drafter subagent writes content sections here

## Cleanup

To clean up playground files:
```bash
rm -rf .playground/*
```

Or keep them for reference — they do no harm.
