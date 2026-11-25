# STANDING OPERATIONAL RULES FOR 50 STATES IN 50 DAYS CAMPAIGN

These rules govern all data, asset generation, social distribution, and audience engagement across the remaining states of the 50 States in 50 Days rollout.

---

### Rule 1: Mandatory Pre-Flight Numbers Audit
- Before any state campaign thread or asset is staged or published, execute:
  ```bash
  python3 scripts/check_state_preflight.py --state <STATE_CODE>
  ```
- Every sitting lawmaker is compared directly against the Federal Election Commission's per-candidate summary file (`weball24.txt`).
- Any member with a variance exceeding 10% from the official summary must have a documented, factual explanation in `data/documented_variances.json`. If an outlier lacks a written reason, that member waits and cannot be published until verified and cataloged.

---

### Rule 2: Strict Primary Data Baseline & Sourcing Vocabulary
- **Zero Modeled Numbers:** All figures must be direct calculations from official FEC bulk data (`itpas2.txt` through Dec 31, 2024). No synthetic, weighted, or modeled distributions.
- **Prohibited Words:** Never use the word "verified" (e.g. "verified numbers", "verified filings").
- **Required Sourcing Language:** Always say:
  > *"Built directly from official FEC bulk files, with links to the source filings."*
- **Category Nomenclature:** Always spell out **"Pro-Israel & Foreign Policy PACs"** in full across all copy and infographics to prevent misinterpretation as foreign capital.
- **Uncategorized Visibility:** Always display the **"Uncategorized"** sector slice openly in charts and copy so totals reflect 100% of tracked PAC contributions.

---

### Rule 3: Honest Delegation Counts
- Always state the exact number of lawmakers with records in the specific cycle rather than assuming full statutory seats.
- Standard phrasing:
  > *"X of [State]'s Y members with 2024-cycle FEC records"*
  *(e.g., "29 of Florida's 30 members with 2024-cycle FEC records", "19 of Pennsylvania's 19 members with 2024-cycle FEC records").*

---

### Rule 4: Human Approval for Contentious Inquiries & Named Critics
- **Routine Inquiries:** Operators are authorized to reply autonomously only when providing the official FEC committee page link:
  `https://www.fec.gov/data/committee/<CMTE_ID>/`
  and pointing neutrally to the public audit on `donorclass.info`.
- **"So it was fake?" Pushback:** Use the single, standardized factual answer:
  > *"Yes, the launch numbers were modeled. Every figure is now from FEC filings, and the audit is public: https://donorclass.info"*
  Zero argument, debate, or follow-up past this statement.
- **Escalation Gate:** Any reply to a named critic, hostile quote-tweet, reporter question, or new inquiry vector MUST receive leadership approval prior to publication.

---

### Rule 5: Visual Integrity & Neutral Vocabulary
- **No State Seals:** Official state seals are strictly prohibited on all visual assets and infographics to respect statutory seal restrictions and eliminate endorsement implications. Use clean, nonpartisan circular badges.
- **No Partisan or Editorial Language:** Prohibit loaded words such as "blitz", "bought", "purchased", "corrupt", "shill", or "puppet".
- Outside spending must always be neutrally described as:
  > *"independent spending supporting members"* and *"independent spending opposing members"*.

---

### Rule 6: Monetization Parked
- The Reddit Contributor Program (Persona / Stripe KYC), Pro data tier subscriptions ($49/month), paid newsletters, and commercial sponsorship funnels remain 100% parked until approximately December 9, 2026 (two clean weeks post-relaunch).
- The entire platform remains free, open-source, and nonpartisan.

---

### Rule 7: Cycle Refresh Audit Protocol
- When transitioning to the 2025–2026 election cycle as ongoing FEC quarterly filings arrive:
  1. Re-run `scripts/fetch_fec_bulk.py` for the new cycle files.
  2. Execute the complete reconciliation comparison across all sitting members against the new cycle summary.
  3. Catalog 100% of new variances in `data/documented_variances.json`.
  4. Update every cycle and date label across the platform, metadata, and methodology documents before publishing new cycle data.

---

### Rule 8: Voice and Snark (Sharper Engagement with Objective Truth)
1. **Mock the money, not the member.** Fine: "Florida's delegation pulled in $18.28M from PACs last cycle." Never: "bought," "owned," "paid off," "in the pocket of," or anything implying a quid pro quo. The data shows contributions, not wrongdoing. (Defamation risk.)
2. **Hit both parties evenly.** Snark that only lands on one side destroys the nonpartisan credibility that makes the data believable. Rotate targets; top-5 lists show both parties as the data falls.
3. **Every number carries its source link.** Snarky or not.
4. **Snark lives in original posts only.** Replies to critics, corrections, reporters, and "so it was fake?" stay straight (Rule 4 unchanged). Anything argumentative still goes to Owner first.
5. **No snark on caveated numbers.** Any member listed in `data/documented_variances.json` (e.g., McCormick, Mackenzie) gets plain wording plus the caveat, or is left out of rankings.
6. **Leading questions: allowed but keep them open.** Prefer prompts that send people to the data over ones that hand them a conclusion.
   - Weaker: "Who takes more corporate and defense PAC money?"
   - Stronger: "Same state, same Congress, very different donors. See for yourself: [link]"
7. **Rule 5 amendment:** Rule 5's banned-word list stays. Editorial language is now permitted in tone (wit, sarcasm about the system) but never in factual claims or labels.
