# Claude Handoff: Required Fixes, Voice Rules, Pennsylvania Gate
**From:** Claude (Cowork) | **To:** Antigravity + all desk subagents (Site, Reddit, X, Facebook) | **Date:** 2026-11-25
**Approved by:** Owner (owner). Voice change is his decision; the fixes below are accuracy items.
**Reply to:** `docs/agent_board/` (see README there). Post one message per completed item.

---

## A. Required fixes on the site (commit 9c9923b) - BLOCKS Pennsylvania

These are accuracy problems, not tone. Fix before State #4 goes out.

| # | Where | Current | Problem | Replace with |
|---|---|---|---|---|
| A1 | `app.js` social card | "DIRECT MULTI-CANDIDATE PAC RECEIPTS (CAPPED)" and "Under 52 U.S.C. § 30116(a)(2)(A), capped at $5,000 per election" | Legally wrong. The $5,000 limit is per PAC, per election. A member's total is not capped. Dataset also includes party and other committees (all 24K/24Z), not only multicandidate PACs. | "DIRECT PAC AND COMMITTEE CONTRIBUTIONS" and delete the statute line. |
| A2 | `scripts/generate_sankey_diagram.py` (line ~105) and `fl-sankey-flow.png` | "$18.28M (52 U.S.C. § 30116 Capped)" | Same error. | "$18.28M direct PAC and committee contributions". Regenerate the PNG. |
| A3 | Sankey subtitle (line ~78) | "Direct Multi-Candidate PAC Contributions" | Same scope error. | "Direct PAC and Committee Contributions". |
| A4 | `index.html` modal banner | "Official FEC Public Record:" | Implies FEC endorsement; same overclaim the correction apologized for. | "Built from FEC public records:" |
| A5 | `index.html` compare modal | "7-Sector Head-to-Head Comparison" | There are 8 sectors including Uncategorized (Rule 2). | "Sector Comparison" and confirm Uncategorized renders in the bars. |
| A6 | `harness/README.md` | "Verify FEC dataset bundle integrity (539 members, 7 sectors)" | 8 sectors. | Update count. |

**Done when:** grep for `CAPPED`, `Capped`, `30116`, `Official FEC`, `7-Sector`, `7 sectors` in `app.js`, `index.html`, `scripts/`, `harness/` returns nothing, and the FL Sankey PNG is regenerated. Post the grep output to the board.

---

## B. Voice rules (new Standing Rule 8) - merge into `docs/50_STATES_STANDING_RULES.md`

Owner has approved a sharper, slightly snarky voice for social posts. Mission: make it easy for people to click a card and see who their reps are influenced, or could be influenced, by. **We give the data; people decide.** Snark serves that; it never replaces accuracy.

**Rule 8: Voice and Snark**
1. **Mock the money, not the member.** Fine: "Florida's delegation pulled in $18.28M from PACs last cycle." Never: "bought," "owned," "paid off," "in the pocket of," or anything implying a quid pro quo. The data shows contributions, not wrongdoing. (Defamation risk.)
2. **Hit both parties evenly.** Snark that only lands on one side destroys the nonpartisan credibility that makes the data believable. Rotate targets; top-5 lists show both parties as the data falls.
3. **Every number carries its source link.** Snarky or not.
4. **Snark lives in original posts only.** Replies to critics, corrections, reporters, and "so it was fake?" stay straight (Rule 4 unchanged). Anything argumentative still goes to Owner first.
5. **No snark on caveated numbers.** Any member listed in `data/documented_variances.json` (e.g., McCormick, Mackenzie) gets plain wording plus the caveat, or is left out of rankings.
6. **Leading questions: allowed but keep them open.** Prefer prompts that send people to the data over ones that hand them a conclusion.
   - Weaker: "Who takes more corporate and defense PAC money?"
   - Stronger: "Same state, same Congress, very different donors. See for yourself: [link]"
7. **Rule 5 amendment:** Rule 5's banned-word list stays. "Editorial language" is now permitted in tone (wit, sarcasm about the system) but never in factual claims or labels.

**1v1 share text (`app.js` ~line 362):** owner's call; recommended replacement:
> `${A} (${amtA}) vs ${B} (${amtB}) in 2024 direct PAC and committee money. Same Congress, different donors. Compare their FEC filings side by side: ${url}`

---

## C. Pennsylvania (State #4) gate

Claude ran the numbers check independently on 2026-11-25:
- 19 members, total $19,599,178 (matches "$19.60M").
- 17 of 19 within 10% of weball24. Two outliers, both documented:
  - **McCormick (S2PA00661): $2,501,980 vs FEC summary $1,066,344 (+134.6%)**, LEADERSHIP_JFC_TRANSFER.
  - **Mackenzie (H8PA15195): $340,685 vs $429,249 (-20.6%)**, TIMING_RECEIPT_LATENCY.

**Requirements before posting:**
1. Commit the full Pennsylvania thread text to `social/` so Claude can review it. It is not in the repo yet.
2. If McCormick is named or ranked (he is #2 by total), the post must carry the caveat: "FEC's own summary shows $1.07M direct; the difference likely reflects PAC money routed through joint fundraising." Otherwise drop him from rankings.
3. Section A fixes are deployed.
4. Owner approves the final copy.

---

## D. Process reminder

New public-facing features or new copy (like commit 9c9923b) need the owner's sign-off before deploy. Post a summary to the board and wait for approval.
