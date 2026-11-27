# Methodology

## DONOR CLASS: How the Dataset Was Built

**Version:** 1.0.0-data-2024  
**Cycle:** 2023–2024 FEC election cycle  
**Coverage:** 539 members of the 119th U.S. Congress

---

## 1. Source Data

All figures derive from Federal Election Commission (FEC) bulk data files downloaded from `fec.gov/data/bulk-downloads/`. SHA-256 hashes and download URLs are documented in `SOURCES.json`.

| File | Contents |
|------|----------|
| `itpas2.txt` (from `pas224.zip`) | Itemized PAC-to-candidate and independent expenditure disbursements |
| `cm.txt` (from `cm24.zip`) | Committee Master: committee IDs, names, types, connected organization names |
| `cn.txt` (from `cn24.zip`) | Candidate Master: candidate IDs, names, parties, offices, states, districts |
| `ccl.txt` (from `ccl24.zip`) | Candidate-Committee Linkage: maps each candidate to their authorized committees |
| `weball24.txt` (from `weball24.zip`) | FEC Candidate Summary: aggregate receipts as reported by candidates |

---

## 2. Member List

The member list comprises all individuals serving in the 119th Congress (January 2025 inauguration). Members are identified by Congressional Bioguide ID and matched to FEC Candidate IDs via the Candidate Master and Candidate-Committee Linkage files. Members who served partial terms or held multiple offices during the cycle may have more than one FEC Candidate ID; each is documented in the member's individual JSON file.

---

## 3. Contribution Extraction

From `itpas2.txt`, we extract all records where:
- `transaction_tp` is `24K` (contribution to candidate) or `24Z` (in-kind contribution to candidate)
- `cand_id` matches a 119th Congress member's FEC Candidate ID

The sum of these records constitutes `direct_contributions_total` for each member.

**What is not included:**
- Individual contributor donations (covered by FEC's individual contributions file, not this dataset)
- Party committee transfers
- Candidate self-funding
- Independent expenditures (these are reported separately in `ie_support_total` and `ie_oppose_total`)

---

## 4. Independent Expenditure Tracking

Independent expenditures (IEs) are extracted from the same `itpas2.txt` file but kept entirely separate:
- `24E` = IE in support of candidate → `ie_support_total`
- `24A` = IE against candidate → `ie_oppose_total`

**IEs are never summed with direct contributions.** They represent expenditures made independently by outside committees, not money received by the candidate's campaign. Combining them would misrepresent both figures.

---

## 5. Sector Classification

Each contributing committee is classified into one of eight sectors using `sector_map.csv`. Classification is based on the committee's name, its connected organization name (from the Committee Master), and the committee's stated purpose in FEC filings.

Sectors: Defense, Pharma/Health, Finance, Energy, Tech, Foreign Policy, Labor, Uncategorized.

Committees not yet assigned to a named sector are classified as Uncategorized. As of this release, approximately 56% of total direct contribution dollars come from Uncategorized committees. The `uncategorized_top500.csv` file in `docs/academic/` lists the 500 largest unclassified committees by dollar volume and is provided to support community classification efforts.

Sector totals are non-overlapping and sum to `direct_contributions_total`.

---

## 6. Reconciliation

For each member, we compare our `direct_contributions_total` to the FEC Candidate Summary total from `weball24.txt`. 433 of 517 members (members with meaningful direct PAC contribution data) match within 10%.

Known categories of variance:
- **Off-cycle senators** (Class 2 and 3 not on the 2024 ballot): The FEC Candidate Summary reflects partial filings; the `pas2` file captures all itemized disbursements by PACs during the calendar years 2023–2024.
- **Joint fundraising committees**: PAC money routed through joint fundraising committees (JFCs) is captured in `pas2` disbursements but may appear as a transfer in the candidate's FEC Summary, causing apparent divergence.
- **Multi-office transitions**: Members who moved from House to Senate during the cycle may have two FEC Candidate IDs; a single-ID summary misses one office's receipts.

All variances above 10% are documented in `RECONCILIATION_AUDIT.md`.

---

## 7. Reproducibility

The full pipeline is implemented in Python scripts in the `scripts/` directory of the GitHub repository. All source file hashes are recorded in `SOURCES.json`. The rebuild specification is in `docs/OPENFEC_REBUILD_SPEC.md`.

---

*Donor Class Team — donorclass.info — 2026*
