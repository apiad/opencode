# Execution Plan: MkDocs Integration for GitHub Pages

This plan outlines the steps to integrate MkDocs into the project for automatic GitHub Pages deployment via CI/CD.

### Objective
Provide a professional, web-based documentation portal at `https://apiad.github.io/starter` that is automatically synchronized with the codebase via CI/CD.

### Architectural Impact
- Introduces MkDocs as a static site generator for project documentation.
- Extends the GitHub Actions CI/CD pipeline to automatically build and deploy the `docs/` folder to GitHub Pages.
- Enhances local development tooling (`makefile`) to easily build and preview documentation.

### File Operations
- **`mkdocs.yml`** (Create): Core configuration file for MkDocs.
- **`.github/workflows/docs.yml`** (Create): GitHub Actions workflow for CI/CD deployment.
- **`docs/index.md`** (Modify): Add a prominent "Setup" or "Quick Start" section.
- **`makefile`** (Modify): Add `docs-serve` and `docs-build` commands.
- **`TASKS.md`** (Update): Add the new task to the appropriate section.
- **`journal/`** (Update): Add a journal entry to log the completion of this integration.

### Step-by-Step Execution

**Step 1: Create `mkdocs.yml`**
Create a `mkdocs.yml` file in the repository root with the following configuration:
- `site_name`: Gemini CLI Opinionated Framework
- `site_url`: `https://apiad.github.io/starter`
- `theme`: Material theme with dark mode support and search enabled.
- `plugins`: Include `search` and `mkdocstrings` (with Python handler).
- `nav`: Map the navigation to the existing `docs/` structure.

**Step 2: Setup CI/CD Deployment**
Create `.github/workflows/docs.yml` to automate deployment:
- Trigger on `push` to the `main` branch.
- Deploy to the `gh-pages` branch using `mkdocs gh-deploy --force`.

**Step 3: Refine `docs/index.md`**
- Add a prominent "Quick Start" section right after the philosophy to bring visibility to the primary installation command.
- Ensure the Markdown is compatible with MkDocs Material.

**Step 4: Update `makefile`**
Add the following targets:
- `docs-serve`: For local live-reloading preview.
- `docs-build`: To generate the static site locally.

**Step 5: Log Progress**
- Update `TASKS.md`: Add an entry under the Archive for MkDocs integration.
- Update the latest journal entry in `journal/` to log the changes.

### Testing Strategy
1. **Local Preview:** Run `make docs-serve` locally. Verify rendering, theme, and navigation.
2. **Build Verification:** Run `make docs-build` to ensure the site builds without warnings.
3. **CI/CD Testing:** Push to `main` and verify the GitHub Actions workflow completion.
4. **Live Site Verification:** Visit `https://apiad.github.io/starter`.
