# DATA DICTIONARY
## DONOR CLASS: Committee-to-Candidate Contributions, 119th Congress (2023-2024 FEC Cycle)

**Dataset:** `release/donor-dataset.csv`  
**Version:** 1.0.0-data-2024  
**Coverage:** 539 members of the 119th U.S. Congress (House and Senate)  
**Cycle:** January 1, 2023 – December 31, 2024

---

## Column Reference

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `bioguide_id` | string | — | Unique member identifier from the Congressional Bioguide. Used as primary key. Example: `A000055` |
| `fec_candidate_id` | string | — | FEC candidate identifier from the Candidate Master (cn24.txt). Links to FEC filings. Example: `H2AL04055` |
| `name` | string | — | Member full name as listed in FEC Candidate Master. |
| `state` | string | 2-letter USPS code | Member's state. `DC`, `PR`, `VI`, `GU`, `AS`, `MP` indicate non-voting delegates. |
| `district` | integer | — | Congressional district number. `0` = at-large; Senate members use `0`. |
| `chamber` | string | — | `House` or `Senate`. |
| `party` | string | — | `Republican`, `Democrat`, or `Independent`. As listed in FEC filings. |
| `direct_contributions_total` | float | USD | Sum of all itemized PAC-to-candidate contributions recorded in the FEC `pas2` (itpas2.txt) file for this member during the 2023-2024 cycle. Includes transaction types 24K (contribution) and 24Z (in-kind contribution). **Does not include individual contributions, candidate self-funding, party committee transfers, or independent expenditures.** |
| `ie_support_total` | float | USD | Sum of independent expenditures made in support of this candidate (transaction type 24E). These are expenditures by outside committees, not contributions to the candidate. **Never summed with `direct_contributions_total`.** |
| `ie_oppose_total` | float | USD | Sum of independent expenditures made in opposition to this candidate (transaction type 24A). These are expenditures by outside committees, not contributions to the candidate. **Never summed with `direct_contributions_total`.** |
| `sector_defense` | float | USD | Subset of `direct_contributions_total` from committees classified as Defense sector in `sector_map.csv`. |
| `sector_pharma` | float | USD | Subset of `direct_contributions_total` from committees classified as Pharma/Health sector. |
| `sector_finance` | float | USD | Subset of `direct_contributions_total` from committees classified as Finance sector. |
| `sector_energy` | float | USD | Subset of `direct_contributions_total` from committees classified as Energy sector. |
| `sector_tech` | float | USD | Subset of `direct_contributions_total` from committees classified as Tech sector. |
| `sector_foreign_policy` | float | USD | Subset of `direct_contributions_total` from committees classified as Foreign Policy sector. |
| `sector_labor` | float | USD | Subset of `direct_contributions_total` from committees classified as Labor sector. |
| `sector_uncategorized` | float | USD | Subset of `direct_contributions_total` from committees not yet assigned to any of the seven named sectors. Approximately 56% of total direct dollars fall in this category. |
| `transaction_count` | integer | — | Number of individual itemized transaction records in `pas2` contributing to `direct_contributions_total` for this member. |
| `data_through` | date | YYYY-MM-DD | End date of data coverage. All records use `2024-12-31`. |
| `notes` | string | — | Freeform notes on known data quality issues or methodology exceptions for this member. Blank for most members. |

---

## Sector Classification

The eight sectors are defined in `sector_map.csv`. Each committee (`cmte_id`) is manually classified by the team based on the committee's connected organization name, purpose, and industry. The Uncategorized sector contains all committees not yet classified.

**Sector identifiers:**

| Sector | Column | Description |
|--------|--------|-------------|
| Defense | `sector_defense` | Defense contractors, military industry, veterans PACs |
| Pharma/Health | `sector_pharma` | Pharmaceutical manufacturers, health insurance, medical associations |
| Finance | `sector_finance` | Banks, investment firms, insurance companies, real estate |
| Energy | `sector_energy` | Oil, gas, coal, utilities, renewable energy |
| Tech | `sector_tech` | Software, hardware, telecommunications, internet platforms |
| Foreign Policy | `sector_foreign_policy` | Foreign-affiliated advocacy, international business councils |
| Labor | `sector_labor` | Trade unions, labor federations, workers' associations |
| Uncategorized | `sector_uncategorized` | Committees not yet classified into a named sector |

Sector totals sum to `direct_contributions_total`. They do not overlap.

---

## Transaction Types Included and Excluded

**Included in `direct_contributions_total`:**
- `24K` — Contribution to candidate
- `24Z` — In-kind contribution to candidate

**Excluded from `direct_contributions_total` (reported separately):**
- `24E` — Independent expenditure in support of candidate (see `ie_support_total`)
- `24A` — Independent expenditure against candidate (see `ie_oppose_total`)
- `24C` — Coordinated expenditure (not in this dataset)
- All party committee transfers

---

## Key Limitations

See `KNOWN_LIMITATIONS.md` for a full discussion. Summary:
- 2023–2024 cycle only; no historical comparison.
- ~56% of direct dollars are from Uncategorized committees.
- 433 of 517 members match FEC summary totals within 10%; see `RECONCILIATION_AUDIT.md` for documented variances.
- Independent expenditure totals reflect expenditures *about* the member, not contributions *to* the member. They must not be compared or summed.

---

*Generated by Donor Class Team. Data sourced from FEC bulk files. See `SOURCES.json` for file hashes and download URLs.*
