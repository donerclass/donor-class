# Open Items

> 2026-11-27 18:17 PHT Antigravity: G1 shipped (commit 65479b2). U1, U2, U4, U5 done. Cron corrected to 0 23,11 * * * UTC (07:00/19:00 PHT). S3a answered. Pending: U3/U6 owner decisions, G2/G3 analytics, PA post, U6 signer.

> 2026-11-25 23:00 Antigravity: Re-scrub complete. Gate 5 externalized to private out-of-repo file. History counts: <USERNAME>=0, <FIRSTNAME>=0, base64=0. PA preflight PASS (all 5 gates). Force-pushed, forks=0, site=200.

| ID | Item | Owner | Status | Source |
|---|---|---|---|---|
| A1-A6 | Remove "capped"/§30116, "Official FEC", fix 7-sector labels; regenerate FL Sankey | site | done | CLAUDE_HANDOFF_2026-11-25 sec A |
| B | Merge Rule 8 (voice and snark) into 50_STATES_STANDING_RULES.md | antigravity | done | sec B |
| B-1v1 | Update 1v1 share text (owner's call) | site | done | sec B |
| C1 | Commit Pennsylvania thread text to social/ for Claude review | x | done | sec C |
| C2 | McCormick caveat or remove from PA rankings | x | done | sec C |
| C3 | Owner approval of final PA copy | owner | done (approved 2026-11-25, post after FL window) | sec C |
| R1 | Consolidate to 4-agent roster (Builder, Distribution, Data Integrity, Analytics/GEO) | antigravity | done | agent_skills/README.md |
| S1 | Commit working-tree anonymity cleanup + name/path preflight check | builder | done | messages/..._2110_... |
| S2 | Git history scrub + force push (Owner approved) | builder | done | messages/..._2130_... |
| S3 | Twice-daily Data Integrity sweep -> DIGEST.md | antigravity | done | messages/..._2130_... |
| G1 | Static pages + llms.txt + data downloads + sitemap | builder | done (commit 65479b2, 539 members, 56 states, 8 sectors, 606 sitemap URLs) | SKILL_static_pages_geo.md |
| G2 | AI referral + crawler tracking (weekly fyi) | analytics | open | SKILL_ai_visibility_metrics.md |
| G3 | Citation audits (question bank) | analytics | open (G1 shipped) | SKILL_ai_visibility_metrics.md |
| U1 | LICENSE, DATA_LICENSE, CITATION.cff, .zenodo.json | builder | done | HANDOFF_2026-11-27 U1 |
| U2 | Release package (data dictionary, methodology, limitations) | builder | done (release/ dir, build_release.py; tag pending U3) | U2 |
| U3 | Zenodo DOI: owner enables GitHub integration, then release v1.0.0-data-2024 | owner -> builder | needs-owner | U3 |
| U4 | Student project brief + uncategorized_top500.csv | builder | done | U4 |
| U5 | One-pager, target list, email template (nothing sent) | analytics + builder | done; outreach still blocked on U6 | U5 |
| U6 | Decide named contact for academic outreach (A public / B collaborator / C anonymous) | owner | needs-owner | U6 |
| S3a | Digest ran 09:54 not 07:00; confirm trigger and sleep behavior | antigravity | done (messages/2026-11-27_1817_...); cron corrected to 0 23,11 * * * UTC | messages/..._1000_... |
