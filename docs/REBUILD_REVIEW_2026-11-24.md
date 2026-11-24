# Rebuild Review: Independent Check (Claude, 2026-11-24)

**Verdict:** real progress, NOT ready to relaunch. Do not post the correction or unfreeze the campaign until the items below pass.

## Confirmed good
- Data now built from FEC bulk files (pas2, cm, cn, ccl, weball), hashes in SOURCES.json.
- Generator archived; contributions (24K/24Z) and independent expenditures (24E/24A) kept separate.
- Amendment de-dup on (CMTE_ID, TRAN_ID) by highest FILE_NUM; filing-image links present.
- Old GitHub token revoked (Owner, 2026-11-24).

## Must fix
1. **Reconciliation fails.** Against weball24 (OTHER_POL_CMTE_CONTRIB + POL_PTY_CONTRIB), of 499 matched members: 337 within 5%, **56 off by more than 15%**. Examples: Slotkin $1,332,460 vs FEC $16,000; Scalise $1,903,755 vs $187,000; Blunt Rochester $2,975,411 vs $465,300. Likely causes: members with multiple FEC candidate IDs (office changes, e.g. House to Senate) joined to the wrong ID or mixed; possible inclusion of rows where the member's own committee is the giver. Use the candidate ID active for the cycle (via ccl/cn) and only rows where CAND_ID is the recipient.
2. **Negative "direct contributions" totals** (Mike Lee -$86,337, Eli Crane -$143,701, John Kennedy -$55,485, Ro Khanna -$5,550). Investigate before display; never show a negative "received" total without explanation.
3. **validate_rebuild.py must fail** when any member deviates more than a set tolerance (suggest 10%) without a documented reason. "100% reconciliation" was not accurate.
4. **Cycle label wrong.** Data is the 2023-2024 cycle, through 2024-12-31. Site title, badge, JSON-LD, and footer say "2024-2026." Fix everywhere, or ingest the 2026 cycle files separately.
5. **Sector coverage: 92.4% of direct dollars are "Uncategorized."** Map the top PACs by dollar volume (a few hundred committees covers most money) in sector_map.csv with a checkable basis, and show "Uncategorized" as a visible slice in every chart and ranking.
6. **Methodology copy** still says it aggregates "Schedule A (individual conduit/earmarked donations)." The build uses pas2 only. Rewrite to match Section 7 of OPENFEC_REBUILD_SPEC.md.
7. **donor-dataset.js is 41.6 MB** and loads on every page view. Ship summary data only on load; fetch per-member transactions on demand.
8. **Remove official state seals** from infographics (state laws restrict seal use; implies endorsement). Regenerate infographics after items 1-5 pass.
9. **Park monetization** (Reddit Contributor KYC, Pro data tier, projections) until relaunch is clean.

## Re-check script (run after fixes)
```python
import csv, statistics
w = {}
for line in open('data/fec_raw/extracted/weball24.txt', encoding='latin-1'):
    f = line.rstrip('\n').split('|')
    w[f[0]] = float(f[25] or 0) + float(f[26] or 0)   # other committee + party contributions
rows = list(csv.DictReader(open('data/donor-dataset.csv')))
out = []
for r in rows:
    ref = w.get(r['fec_candidate_id'])
    if not ref: continue
    pct = (float(r['direct_contributions_total']) - ref) / ref * 100
    if abs(pct) > 10: out.append((r['name'], r['fec_candidate_id'], round(float(r['direct_contributions_total'])), round(ref), round(pct)))
neg = [r['name'] for r in rows if float(r['direct_contributions_total']) < 0]
print('over 10%:', len(out), ' negatives:', neg)
for o in sorted(out, key=lambda x: -abs(x[4]))[:25]: print(o)
```
Relaunch gate: zero unexplained members over 10%, zero unexplained negatives, cycle labels correct, uncategorized visible.
