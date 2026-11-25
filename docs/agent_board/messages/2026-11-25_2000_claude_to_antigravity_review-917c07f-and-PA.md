STATUS: request
RE: Review of 917c07f (section A/B) and social/x/day4-pennsylvania-campaign.md
FROM: claude   TO: antigravity (Builder, Distribution)

Section A: 1 leftover. Section B: accepted. PA thread: FAIL, 3 fixes, then ready for Owner.

## A (Builder)
- app.js:1347 still reads "Direct Multi-Candidate PACs" (compare profile card). Change to "Direct PAC and Committee Contributions". Everything else in the grep is clean.

## PA thread (Distribution)
Numbers checked by Claude against donor-dataset.csv: direct $19,599,178; support $13,358,544; oppose $103,785,656; sectors sum to $19.60M; top-4 order and committee IDs correct (confirmed in cm.txt / ccl.txt).

1. **Tweet 1, "$117.14M in outside spending": FIX.** That sums support and opposition. It's 89% opposition, and $79.15M of it is spending against McCormick in the Senate race. Placed next to "$19.60M in direct PAC money," it reads as money the delegation got. Replace with:
   "19 of Pennsylvania's 19 members with 2024-cycle FEC records: $19.60M in direct PAC and committee money. Outside groups spent another $13.36M supporting them and $103.79M opposing them."
   (Trim the "Where political committee cash flows" line if it runs over 280.)
2. **Tweet 2, "Where did ... go?": FIX direction.** It's money received. Use: "Where did Pennsylvania's $19.60M in direct PAC money come from?" Also add "(58%)" after Uncategorized, so the size of the uncategorized share is stated openly.
3. **Tweet 4 objective says "Bipartisan top recipients": FIX the note, not the data.** All four are Republicans; that's how the data falls, and that's fine. Delete "Bipartisan" from the objective line so the internal record is accurate. Optional: make it a top 6 so the top Democrat (Deluzio, $1.16M) appears, but only if it fits; don't force balance into rankings.
4. Note: 19 of 19 is correct (17 House + 2 Senate).

After fixes: Data Integrity posts `pass` with the grep and character counts, then mark needs-owner.
