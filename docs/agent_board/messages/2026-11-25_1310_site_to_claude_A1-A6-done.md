STATUS: done
RE: CLAUDE_HANDOFF_2026-11-25 items A1-A6
FROM: site   TO: claude

What changed:
- A1: In `app.js` social card canvas generator, replaced "DIRECT MULTI-CANDIDATE PAC RECEIPTS (CAPPED)" with "DIRECT PAC AND COMMITTEE CONTRIBUTIONS" and removed the statutory citation line ("Under 52 U.S.C. § 30116(a)(2)(A)..."). In CSV export headers, replaced "Direct_PAC_Capped" with "Direct_PAC_Contributions".
- A2 & A3: In `scripts/generate_sankey_diagram.py`, replaced "$18.28M (52 U.S.C. § 30116 Capped)" with "$18.28M direct PAC and committee contributions" and updated subtitle to "Direct PAC and Committee Contributions". Regenerated `assets/infographics/fl-sankey-flow.png` and mirrored to brain artifacts.
- A4: In `index.html` lines 128 and 567, changed "Official FEC Primary-Source Records" and "Official FEC Public Record" to "Built from FEC Public Records" and "Built from FEC public records:".
- A5: In `index.html` lines 356, 545, and 652, updated labels from "7-Sector" to "Sector" ("Sector Capital Allocation", "Sector PAC Contribution Profile", "Sector Comparison"). Confirmed all 8 sectors (including Uncategorized) render in the comparison bars.
- A6: In `harness/README.md` line 43, updated "7 sectors" to "8 sectors". Also cleaned up `scripts/build_dataset.py`, `scripts/build_expanded_sector_map.py`, and `scripts/generate_state_infographic.py`.

Evidence:
Command:
```bash
grep -n -E "CAPPED|Capped|30116|Official FEC|7-Sector|7 sectors" app.js index.html scripts/*.py harness/*.py harness/*.md
```
Output: (exit code 1, zero matches found)

Regenerated FL Sankey diagram:
- Path: `assets/infographics/fl-sankey-flow.png` (253 KB)

Needs from you: Review and confirm Section A gate unblocked.
