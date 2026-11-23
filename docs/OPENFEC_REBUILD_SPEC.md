# DONOR CLASS: OpenFEC Data Rebuild Spec
**Author:** Claude (for Owner, Antigravity, infrastructure lead) | **Date:** 2026-11-23 | **Status:** ready to build

**Goal:** replace every modeled number with figures computed directly from FEC primary-source records, so that anyone can reproduce any number on the site from the public repo and FEC files.

**Hard rule:** no generated, estimated, weighted, or randomized dollar figures anywhere. If a value cannot be computed from FEC records, show "No itemized FEC records" instead of a number.

---

## 0. Before anything else (today)

1. **Revoke the old GitHub token** in GitHub Settings > Developer settings > Personal access tokens (the remote URL is already clean; the token itself is still valid until revoked).
2. **Replace the live dollar figures,** not just "freeze" them. Do not show the modeled numbers in a "read-only audit mode": they are not real records, and displaying them while saying "reconciliation in progress" still presents them as FEC data. Use the banner in Section 7 and hide member dollar figures, sector totals, rankings, and infographics until the rebuild ships.
3. **Delete or archive** the Texas/California/Florida infographics generated from the old dataset. Do not repost them.

---

## 1. Data sources (primary, public, free)

### Option A (recommended): FEC bulk files, cycle 2026 (covers 2025 to 2026)
Download from fec.gov > Campaign finance data > Bulk data. Each file has a separate header file and a published file description. Verify exact URLs on the bulk data page before scripting.

| File | Contents | Use |
|---|---|---|
| `pas2` (pas226.zip) | Contributions from committees to candidates **and** independent expenditures (itemized) | Core source for all PAC money per member |
| `cm` (cm26.zip) | Committee master: CMTE_ID, CMTE_NM, CMTE_TP, CMTE_DSGN, ORG_TP, CONNECTED_ORG_NM | Name and classify every PAC |
| `cn` (cn26.zip) | Candidate master: CAND_ID, name, party, office, state, district | Candidate identity |
| `ccl` (ccl26.zip) | Candidate-committee linkage | Map candidate to principal campaign committee |
| `weball` (weball26.zip) | All-candidates summary, including "contributions from other political committees" | Reconciliation check only (Section 6) |

### Option B: OpenFEC API (api.open.fec.gov), for refreshes and spot checks
Free key from api.data.gov. Relevant endpoints:
- `/v1/schedules/schedule_b/` (committee disbursements; filter by `recipient_committee_id` or `committee_id`)
- `/v1/schedules/schedule_e/` (independent expenditures; filter by `candidate_id`, `support_oppose_indicator`)
- `/v1/candidate/{candidate_id}/`, `/v1/candidate/{candidate_id}/committees/`, `/v1/committee/{committee_id}/`
Respect rate limits; cache responses in the repo build step, never at page load.

### Member roster
Use `unitedstates/congress-legislators` (`legislators-current.yaml`), which lists current members with their FEC candidate IDs. **Only current members.** Drop anyone who has left office or died (the old dataset included a member who died in 2022).

---

## 2. pas2 field mapping (from the FEC file description)

Columns, in order: CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP, ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION, TRANSACTION_DT (MMDDYYYY), TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM, MEMO_CD, MEMO_TEXT, SUB_ID.

- **Giver** = CMTE_ID (the PAC or committee spending the money). Join to `cm` for name and type.
- **Recipient candidate** = CAND_ID. Join to roster by FEC candidate ID.
- **Amount** = TRANSACTION_AMT (negative values are refunds; keep them so totals are net).
- **Election** = TRANSACTION_PGI (P = primary, G = general, etc.).
- **Proof link** = IMAGE_NUM, linkable to the FEC filing image so every row is checkable.

---

## 3. Classifying the money (the core fix)

Two separate measures, never added together:

| Measure | TRANSACTION_TP | What it means | Site label |
|---|---|---|---|
| **Direct PAC contributions** | 24K (contribution to candidate), 24Z (in-kind contribution) | Money given to the candidate's campaign | "Given to the campaign" |
| **Outside spending: support** | 24E | Independent expenditure advocating the candidate (super PACs, etc.) | "Spent supporting (outside groups)" |
| **Outside spending: oppose** | 24A | Independent expenditure opposing the candidate | "Spent opposing (outside groups)" |
| Other (24C coordinated party, 24F/24N communication costs, 24H, 24P, 24R) | as listed | Not PAC contributions | Exclude from both, or show in a footnote bucket |

Rules:
- **Never** describe independent expenditures as money a member "received" or was "funded" by. Super PACs spend independently of the campaign. (The old data put about $15.9M of super PAC spending under one member as "Total PACs.")
- **Amendments:** de-duplicate on (CMTE_ID, TRAN_ID), keeping the row with the highest FILE_NUM. Log how many rows were dropped.
- **Memo items (MEMO_CD = X):** follow the FEC file guidance; document the choice in the methodology and test that totals are not double-counted.
- **Party committees** (CMTE_TP party types) belong in their own "Party committees" bucket, not in an industry sector.

---

## 4. Sector mapping (replaces the hash-based allocation)

- Create `data/sector_map.csv` with columns: `cmte_id, cmte_name, sector, basis, reviewed_by, reviewed_date`.
- `basis` must be a checkable fact (for example the CONNECTED_ORG_NM from the committee master, or the committee's own website).
- Any PAC not in the map is shown as **"Uncategorized"**, never assigned a sector by guess.
- **Rename** "Foreign Policy / Lobby" to **"Pro-Israel and Foreign Policy PACs"** and state in the methodology that these are U.S. domestic committees. Never abbreviate this category to "Foreign" in charts or social copy.
- Publish the full map in the repo so readers can audit classifications.

---

## 5. Build pipeline

1. `scripts/fetch_fec_bulk.py`: download the cycle files, verify, record download date and file hashes in `data/SOURCES.json`.
2. `scripts/build_dataset.py`: parse, de-duplicate, classify per Section 3 and 4, aggregate per member, and write `data/donor-dataset.js` plus `data/donor-dataset.csv` (the CSV is the auditable version).
3. **Delete** `scripts/generate_donor_dataset.py`'s generation logic (`deterministic_float`, `STATE_WEIGHTS`, `PARTY_MODIFIERS`, PAC `avg` fields). Keep it out of the build entirely, or archive it under `archive/` with a README stating it produced modeled data and is not used.
4. Every member record carries: `fec_candidate_id`, `direct_contributions_total`, `sector_totals`, `top_pacs` (name, CMTE_ID, amount, link), `ie_support_total`, `ie_oppose_total`, `data_through` (latest transaction date), `source_files`.
5. Stamp the site with **"FEC data through [date], cycle 2025 to 2026, downloaded [date]."**

---

## 6. Validation gates (must pass before relaunch)

- [ ] Zero references to `deterministic_float`, random, seed, or weights in the build path.
- [ ] Spot-check 20 members (both parties, both chambers, including the top 5 by total) against their FEC.gov candidate pages. Direct contribution totals must reconcile with the `weball` "contributions from other political committees" figure within a documented tolerance, with differences explained.
- [ ] Spot-check 10 individual PAC-to-candidate rows by opening the FEC filing image.
- [ ] Flag (do not hide) any PAC-to-candidate total above $5,000 per election; most will be legitimate (primary plus general, redesignations, refunds), but each needs a note.
- [ ] Every number on the page and in every infographic traces to a row in `donor-dataset.csv`.
- [ ] No individual donor names or addresses are displayed (FEC rules restrict commercial use of individual contributor information; this dataset is committee-level only, keep it that way).
- [ ] Remove or truthfully relabel the "LIVE WIRE" ticker: either generate it from real recent filings or label it as editorial context with no dollar figures.
- [ ] Remove the ad slot claim and any "verified" language until gates pass.

---

## 7. Copy: banner, methodology, correction

### Maintenance banner (use now, instead of the "reconciliation" banner)
> **Data rebuild in progress.** Earlier figures on this site were modeled estimates, not line-item FEC records. We have taken them down and are rebuilding every number directly from official FEC filings. Verified data will return with links to the source filings.

Why this wording: the proposed "reconciliation in progress / read-only audit mode" banner implies the existing numbers are real records being double-checked. They are not, so that banner repeats the original problem.

### Methodology (for relaunch)
> **Source.** All figures come from Federal Election Commission bulk data for the 2025 to 2026 cycle (files: pas2, cm, cn, ccl), downloaded [date], covering filings through [date].
> **What we count.** "Given to the campaign" = contributions from PACs and other committees directly to a member's campaign (FEC transaction types 24K and 24Z), net of refunds. "Outside spending" = independent expenditures by groups such as super PACs supporting (24E) or opposing (24A) a member. Outside spending is not money the member received and is never added to contributions.
> **Sectors.** Each PAC is assigned a sector from its connected organization in FEC records; the full mapping is published in our repository. PACs we have not classified appear as "Uncategorized."
> **Verify us.** Every member page links to the FEC filings behind each number. Our code and data are open source at github.com/donerclass/donor-class.

### Correction post (for the Texas thread and X, at relaunch)
> Correction: our launch figures were modeled estimates, not line-item FEC records, and we should not have described them as verified filings. We took them down, rebuilt every number from official FEC bulk data, and now link each figure to the source filing. Code and data are public so anyone can check our work. [link]

---

## 8. Relaunch order
1. Gates in Section 6 pass.
2. Methodology and member pages live with source links.
3. Correction post published.
4. Only then restart the 50-state calendar, using infographics generated from the new CSV.
