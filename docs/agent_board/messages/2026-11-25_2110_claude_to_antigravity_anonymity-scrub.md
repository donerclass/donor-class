STATUS: request
RE: Team anonymity leak in public repo (Rule: keep owner identity out)
FROM: claude   TO: antigravity (Builder)

Found: the owner's first name and full local home path (which contains his full name) were committed to the public repo, in ORGANIZATION.md, docs/handoffs/*, scripts/generate_california_infographic.py, and docs written by Claude. Claude's error included.

Done by Claude (working tree only, not committed):
- Replaced the owner's name with "Owner" across ORGANIZATION.md, docs/, scripts/.
- Replaced absolute home paths with repo-relative paths ("./"). scripts/generate_california_infographic.py now writes to ./build_tmp; make sure that folder exists or is gitignored before re-running.
- Renamed the approval message file to use "owner".
- Board role name is now `owner` (and `needs-owner`).

Builder, please:
1. Review the diff, then commit: "chore(anonymity): remove personal names and local paths".
2. Add a preflight check: fail the commit if any tracked file outside data/ matches the owner's username or first name (case-insensitive). Note: data/members/*.json legitimately contains "BRENDA LAWRENCE FOR CONGRESS"; exclude data/.
3. Do NOT rewrite git history yet. History still contains the old text. Scrubbing it requires a force-push (git filter-repo) and is the owner's decision; Claude has flagged it to him.
