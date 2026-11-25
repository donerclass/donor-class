# SKILL: Static Pages and AI Visibility (GEO)
**Owner:** Builder. **Reviewer:** Data Integrity. **Priority:** after handoff section A fixes ship.

## Problem (verified by Claude 2026-11-25)
- All figures render client-side via JavaScript. Most AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do not execute JS, so they see an empty shell.
- `sitemap.xml` lists 59 URLs (`/?state=XX`) that all return the same shell HTML.
- `robots.txt` already allows all bots (good; keep it).
- No `llms.txt`.

## Build (one script: `scripts/build_static_pages.py`)
Generate plain HTML at build time from `data/donor-dataset.csv` and `data/members/*.json`. No JS required to read any number.

```
/members/{bioguide_id}-{name-slug}/index.html   (~539)
/states/{xx}/index.html                         (50 + territories)
/sectors/{sector_id}/index.html                 (8, including uncategorized)
/methodology/index.html
/data/index.html                                (download links)
```

Each page must include:
1. `<h1>` with member name, party, state/district, chamber.
2. A real HTML `<table>`: direct PAC and committee contributions total; sector breakdown with Uncategorized row; independent spending supporting; independent spending opposing (separate, never summed).
3. Top PACs table: committee name, CMTE_ID, amount, link `https://www.fec.gov/data/committee/{CMTE_ID}/`.
4. Plain sentence: "FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings."
5. If the member is in `documented_variances.json`: show the FEC summary figure and the written explanation, visibly.
6. `<link rel="canonical">`, `<title>`, meta description with the actual total, and JSON-LD (`Dataset` on data pages; `Person` + `about` on member pages). No "verified" anywhere.
7. Link to the interactive view (`/?candidate=...`) for humans.

## Also
- `/llms.txt`: one-paragraph description, what the data is and is not, cycle, link list to /methodology, /data, /states, /sectors.
- `/data/`: link the CSV and a JSON export (`donor-dataset.json`, summary-level only, no individual donor data).
- Regenerate `sitemap.xml` with all static URLs and real `lastmod`.
- Keep pages small; no 2.9 MB bundle on static pages.

## Done when (Data Integrity checks)
- `curl -s https://donorclass.info/members/<any>/ | grep '<table'` returns a table with numbers (no JS).
- 20 random member pages: totals match `donor-dataset.csv` exactly.
- Every sector table includes Uncategorized; independent spending never added to contributions.
- Sitemap URL count = generated page count.
- Zero matches for `verified`, `CAPPED`, `30116`, `Official FEC` in generated HTML.
