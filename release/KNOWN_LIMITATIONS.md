# Known Limitations

## DONOR CLASS: 2023-2024 FEC Cycle Dataset

**Version:** 1.0.0-data-2024  
**Released:** 2026-11-27

---

## 1. Cycle Coverage

This dataset covers the **2023–2024 FEC election cycle only** (calendar years January 1, 2023 through December 31, 2024). It does not include earlier cycles. No historical trend analysis is possible from this dataset alone.

---

## 2. Uncategorized Committees (~56% of Direct Dollars)

Approximately **56% of total direct PAC contribution dollars** in this dataset come from committees not yet classified into a named sector. These committees appear in the `sector_uncategorized` column and are listed in `docs/academic/uncategorized_top500.csv` (top 500 by dollar volume).

The sector classification is a manual, ongoing effort. Users who classify additional committees and share results (with attribution) will be credited in future releases.

---

## 3. FEC Summary Reconciliation

**433 of 517 members** (members with non-trivial direct PAC contribution data) match the FEC's own Candidate Summary totals within 10%. The remaining 84 members have documented variances. Full documentation is in `RECONCILIATION_AUDIT.md`.

Main causes of variance:
- **Off-cycle senators** (Class 2 and 3, not on the 2024 ballot): The FEC Candidate Summary (`weball24.txt`) reflects only filings that reference the 2024 cycle, while `pas2` captures all itemized PAC disbursements during calendar years 2023–2024 regardless of which cycle the committee reports it under.
- **Joint fundraising committee routing**: PAC money may be disbursed to a joint fundraising committee (JFC) rather than directly to the candidate committee. The `pas2` file records the destination as the JFC; the candidate's FEC Summary may show it as a transfer, causing apparent over- or under-counts at the individual candidate level.
- **Multi-office transitions**: Members who moved from one office to another during the cycle (e.g., House to Senate) may have two separate FEC Candidate IDs. A single-ID FEC Summary misses one office's receipts. We aggregate across both IDs; the notes column documents these cases.

---

## 4. Independent Expenditures Are Reported Separately

`ie_support_total` and `ie_oppose_total` are independent expenditure totals — money spent *about* a candidate by outside committees, not money *given* to the candidate. They are not contributions and **must not be added to or compared with `direct_contributions_total`** without clear methodological justification. This dataset keeps them entirely separate. Research using all three columns must clearly label each one.

---

## 5. No Individual Contributor Data

This dataset does not contain individual donor records. All records represent registered federal PACs and committees. Individual contributions, bundled contributions, and small-dollar donations are not reflected here.

---

## 6. No Intraparty or Party Committee Data

Contributions from party committees (DCCC, NRCC, DSCC, NRSC, DNC, RNC, etc.) and from candidates to other candidates are not included. Only PAC-to-candidate contributions are in scope.

---

## 7. FEC Data Quality

The FEC bulk files themselves contain known data quality issues: late amendments, committee name changes, and occasional misfiled records. We filter to accepted amendments (`amndt_ind = 'N'` or the latest amendment per transaction) but cannot resolve all discrepancies without manual review. The reconciliation audit documents the most significant ones.

---

## 8. Territorial Delegates

Non-voting House delegates (DC, PR, VI, GU, AS, MP) are included in the dataset if they appear in FEC records with direct PAC contributions. Their inclusion or exclusion for any analysis is at the researcher's discretion.

---

*Donor Class Team — donorclass.info — 2026*
