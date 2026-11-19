# Antigravity Handoff: Pre-Launch Fact-Check & Sanity Audit

**Project:** DONOR CLASS (U.S. Congressional PAC & Campaign Finance Tracker)  
**Target Dataset:** `data/donor-dataset.js` (`window.DONOR_BUNDLE`)  
**FEC Cycle:** 2024–2026  
**Audit Date:** 2026-11-19  
**Overall Status:** **PASS** (5/5 core checks passed; 1 minor categorization edge case flagged for review)

## 1. Five-Point Audit Summary

| Check | Status | Verified Result |
| :--- | :--- | :--- |
| **1. Roster Count** | PASS | **539** sitting Incumbents (**100** Senators, exactly 2 per state across all 50 states; **439** House members including all 6 territorial delegates: `AS`, `DC`, `GU`, `MP`, `PR`, `VI`) and **797** Former members (**1,336** total records). |
| **2. South Carolina Senate** | PASS | Sitting SC Senators: **Darline Graham** (`S6SC04437`, Republican, `Incumbent`) and **Tim Scott** (`S4SC00240`, Republican, `Incumbent`). **Lindsey Graham** (`S0SC00149`) is `Former` with `leftOffice: "2026-07-11"`. |
| **3. FECA PAC Caps (> $10,000)** | PASS | **0** violations across all 6 traditional sectors (`defense`, `pharma`, `finance`, `energy`, `tech`, `labor`) for both Incumbents and Formers, and **0** violations among direct-only Foreign Policy Advocacy PACs (DMFI, RJC). |
| **4. Pre-2024 Deceased / Former** | PASS | **Donald McEachin** (`$0`) and **Dianne Feinstein** (`$0`) are zeroed out. All **705** Former records with `leftOffice < 2024-01-01` (and all **797** Former records overall) carry `$0` in active cycle funds. |
| **5. Disaggregation & Labeling** | PASS | **Haley Stevens** (`H8MI11254`) disaggregates `$15,972,030` into `$1,687,202` Direct PAC (`directPacAmount`), `$10,316,820` Super PAC (`outsideSpendingAmount` — United Democracy Project), and `$3,968,008` Conduit (`conduitAmount` — AIPAC PAC). |

## 2. Extended Integrity & Compliance Checks

* **Real-World & Statutory Ground Truth:**
  * Public records confirm [Sen. Lindsey Graham](https://en.wikipedia.org/wiki/Lindsey_Graham) passed away on July 11, 2026, and South Carolina Governor Henry McMaster appointed [Darline Graham](https://governor.sc.gov/news/2026-07/gov-mcmaster-appoints-darline-graham-us-senate) on July 13, 2026, to serve until January 3, 2027.
  * Direct multicandidate PAC caps align with [52 U.S.C. § 30116](https://uscode.house.gov/us/usc/t52/s30116/) ($5,000 per election / $10,000 per 2-year cycle), and foreign-national contribution prohibitions align with [52 U.S.C. § 30121](https://www.fec.gov/help-candidates-and-committees/foreign-nationals/).
* **Arithmetic & Schema Consistency (All 1,336 Records):**
  * `directPacAmount + outsideSpendingAmount + conduitAmount == totalPacAmount`: **0** mismatches (> $1).
  * Negative dollar amounts across all amount fields: **0**.
  * Duplicate `fecCandidateId` values: **0**.
  * Records with `outsideSpendingAmount > 0`: **44**; records with `conduitAmount > 0`: **518**.
* **Foreign Policy Sector PACs Exceeding $10,000:**
  * Only conduit/earmarked committees (`AIPAC PAC`: 409 records; `Pro-Israel America PAC`: 74 records) and Super PAC independent expenditures (`United Democracy Project (UDP)`: 44 records) exceed `$10,000`.
  * Direct-only committees (`Democratic Majority for Israel (DMFI)`, `Republican Jewish Coalition PAC`) have **0** records over `$10,000`.
* **UI & Copy Compliance (`index.html`, `app.js`, `data/donor-dataset.js`):**
  * All sector labels consistently use **Foreign Policy Advocacy** / **Foreign Policy Advocacy PACs** (no bare `"Foreign"` labels).
  * Statutory compliance notices referencing `52 U.S.C. § 30121` and domestic U.S. committee status are present in `data/donor-dataset.js`, `index.html`, and `app.js`.

## 3. Minor Edge Case Flagged for Antigravity Review

* **Issue:** In Haley Stevens's record (`H8MI11254`), the `"Other Foreign Policy Advocacy PACs"` entry (`$1,577,202`, tagged `type: "Conduit / PAC Transfers"`) is aggregated into `directPacAmount` (`$1,687,202`) rather than `conduitAmount` (`$3,968,008`).
* **Why It Matters:** The CSV export in `app.js` (line 789) labels `directPacAmount` as `Direct_PAC_Capped`. If `"Other Foreign Policy Advocacy PACs"` includes earmarked conduit transfers rather than solely direct FECA-capped PAC donations, grouping it under `Direct_PAC_Capped` could be misread by external reviewers.
* **Recommended Action:** Confirm whether the `"Other Foreign Policy Advocacy PACs"` bucket across affected candidates should remain in `directPacAmount` (and optionally clarify the CSV/tooltip label) or be reclassified into `conduitAmount` before public launch.
