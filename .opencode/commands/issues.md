---
description: Manage project issues using GitHub CLI
agent: ship
---

Manage project issues using the `gh` (GitHub) CLI.

### Actions (infer from context)

#### Summary (Default)
If no specific action is requested, produce a strategic report of open issues.
1. Use `gh issue list --json number,title,labels,updatedAt,body` to fetch open issues
2. Provide a brief summary of each issue
3. Evaluate each issue based on **Feasibility** vs. **Impact**
4. Suggest which issues to tackle next
5. Ask if user wants to work on a specific issue or create a new one

#### Create
If user wants to create a new issue:
1. Check if similar issue exists: `gh issue list -S "<title>"`
2. Generate standard issue description:
   - **Executive Summary:** One-sentence goal
   - **Rationale:** Why this matters
   - **Implementation Ideas:** Technical details, potential paths
   - **Reproduction Steps (Bugfixes):** Clear steps to reproduce
3. Present via `question` for confirmation
4. Create with `gh issue create`

#### Update
If user wants to update an existing issue:
1. Fetch issue: `gh issue view <number> --json body`
2. Present proposed changes
3. Confirm and update with `gh issue edit`

#### Work On
If user asks to work on an issue (e.g., `/issues work 42`):
1. Fetch issue details: `gh issue view <number> --json title,body,labels`
2. Enter **Plan Mode** to create implementation plan
3. Present plan for approval

### Key Mandates
- **Never touch source code** — Issue tracking only
- **GitHub integration** — Requires `gh` authentication
- If `gh` not available → inform user and suggest `gh auth login`

### Constraints
- Requires GitHub CLI (`gh`) authentication
- If not authenticated → prompt user to run `gh auth login`
