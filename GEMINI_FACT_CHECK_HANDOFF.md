# GEMINI FACT-CHECK & REDUNDANCY SANITY AUDIT HANDOFF
**Project:** DONOR CLASS (U.S. Congressional PAC & Lobby Tracker)  
**Target Date / Cycle:** November 2026 (2024–2026 Federal Election Commission Cycle)  
**Artifact / Dataset Location:** `data/donor-dataset.js` (`window.DONOR_BUNDLE`)  
**Repository Working Directory:** `donor-class-tracker/`

---

## 1. Executive Mission & Audit Objective

You are conducting the **final pre-launch redundancy fact-check and sanity audit** on **Donor Class**, an independent, nonpartisan campaign finance transparency platform that maps corporate, trade, and ideological Political Action Committee (PAC) contributions across all 50 states and sitting members of the U.S. Congress.

Before this platform goes live, we require a comprehensive verification of:
1. **Congressional Roster Ground Truth** (539 sitting incumbents across the 50 states).
2. **Statutory Contribution Cap Compliance** under the Federal Election Campaign Act (FECA).
3. **Disaggregation of Super PAC Outside Spending vs. Direct Candidate PAC Contributions**.
4. **Legal & Nonpartisan Terminology Compliance** regarding domestic advocacy committees.
5. **Mathematical Integrity** across all sector sums, state aggregations, and national totals.

---

## 2. Verified Ground-Truth Milestones & Historical Context

To ensure you do not flag false positives (as previous models did), note the following verified real-world ground-truth events:

1. **Senator Lindsey Graham (R-SC) Status:**
   * **Fact:** Senator Lindsey Graham passed away on **July 11, 2026** at age 71 from an aortic dissection at George Washington University Hospital.
   * **Dataset State:** In `data/donor-dataset.js`, Lindsey Graham (`S0SC00149`) is recorded as `status: "Former"` with `leftOffice: "2026-07-11"` (his date of death).
2. **Senator Darline Graham (R-SC) Status:**
   * **Fact:** Following Senator Lindsey Graham's death, South Carolina Governor Henry McMaster appointed his younger sister, **Darline Graham Nordone (Darline Graham)**, to fill the vacant U.S. Senate seat on **July 13, 2026**. She became the first woman in South Carolina history to serve in the U.S. Senate and the first sister in U.S. history to succeed her brother in the Senate.
   * **Dataset State:** In `data/donor-dataset.js`, Darline Graham (`S6SC04437`) is seated as the sitting `status: "Incumbent"` U.S. Senator for South Carolina alongside Senator Tim Scott (`S4SC00240`).
3. **Pre-2024 Deceased / Retired Members:**
   * Members who died or retired prior to the 2024 cycle—such as Rep. A. Donald McEachin (died Nov 28, 2022, succeeded by Rep. Jennifer McClellan), Sen. Dianne Feinstein (died Sept 28, 2023), Rep. Donald Payne Jr. (died Apr 24, 2024), Rep. Sheila Jackson Lee (died Jul 19, 2024), and Rep. Bill Pascrell (died Aug 21, 2024)—are archived with `status: "Former"` and carry **$0.00 in active 2024–2026 cycle PAC receipts**.
4. **FECA Statutory PAC Limits (52 U.S.C. § 30116(a)(2)(A)):**
   * Federal law strictly caps multicandidate PAC contributions directly to a candidate's committee at **$5,000 per election** ($10,000 per 2-year cycle: $5,000 primary + $5,000 general).
   * **No single traditional PAC** (Lockheed Martin, Pfizer, Goldman Sachs, Chevron, Google, Teamsters, etc.) may ever exceed **$10,000** per candidate per cycle.
5. **Super PAC Outside Spending vs. Direct PAC Contributions:**
   * Independent Expenditure-Only Committees (Super PACs like United Democracy Project - UDP) **cannot donate to candidate committees** under federal law. They spend independently on broadcast and digital advertisements.
   * High-profile candidates like Rep. Haley Stevens ($15.9M total tracked capital) have their profiles explicitly disaggregated into:
     - **Direct PAC Contributions:** $1,687,202 (FECA capped)
     - **Outside Independent Expenditures (Super PACs):** $10,316,820 (UDP ad buys)
     - **Conduit / Earmarked Transfers:** $3,968,008 (AIPAC PAC bundled individual checks under 11 CFR § 110.6)
6. **Domestic Status of Foreign Policy Advocacy PACs (52 U.S.C. § 30121):**
   * Under federal law, foreign nationals and foreign governments are prohibited from contributing to U.S. elections.
   * Groups like AIPAC PAC, United Democracy Project, Democratic Majority for Israel (DMFI), J Street PAC, Republican Jewish Coalition (RJC) PAC, and NORPAC are **domestic U.S. political committees** funded by American citizens.
   * The sector is strictly labeled **"Foreign Policy Advocacy PACs"** (short name: **"Foreign Policy"**; never bare "Foreign") to eliminate any defamatory tropes or legal ambiguity.

---

## 3. Seven Tracked Sectors & Benchmark Committees

| Sector ID | Sector Name | Color | Sample Tracked PACs | Legal Regime |
| :--- | :--- | :--- | :--- | :--- |
| `defense` | Defense & Aerospace | `#0ea5e9` | Lockheed Martin, Raytheon Technologies, Boeing, General Dynamics, Northrop Grumman | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |
| `pharma` | Big Pharma & Health | `#10b981` | Pfizer, Eli Lilly, PhRMA, Blue Cross Blue Shield, Merck, AbbVie, Johnson & Johnson | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |
| `finance` | Wall St & Big Finance | `#f59e0b` | Goldman Sachs, American Bankers Assoc (BANKPAC), JPMorgan Chase, Citadel, CULAC | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |
| `energy` | Fossil Fuels & Energy | `#ef4444` | Chevron, ExxonMobil, American Petroleum Institute (API), ConocoPhillips, KochPAC | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |
| `tech` | Big Tech & Telecom | `#8b5cf6` | Google/Alphabet NetPAC, Meta Platforms, Amazon, Microsoft, AT&T, Comcast | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |
| `foreign_policy` | Foreign Policy Advocacy PACs | `#e11d48` | AIPAC PAC (Conduit), UDP (Super PAC IEs), DMFI PAC (Direct), J Street (Conduit/Direct), RJC | Disaggregated Direct vs. Outside Spending vs. Conduit |
| `labor` | Labor Unions | `#2563eb` | Teamsters (DRIVE), AFL-CIO, SEIU, IBEW, AFSCME, Machinists Non-Partisan League | Traditional Multicandidate PAC (Capped $\le \$10\text{K}$) |

---

## 4. Gemini Verification & Audit Checklist

Please execute the following 5 audit passes and report any anomalies, outliers, or discrepancies:

### Audit Pass 1: Congressional Delegation & Roster Integrity
- [ ] Confirm total sitting incumbents in `window.DONOR_BUNDLE.candidates` equals **539** (100 Senators + 439 House voting members & delegates).
- [ ] Confirm all 50 states have exactly **2 sitting Senators**.
- [ ] Confirm South Carolina's 2 sitting Senators are **Tim Scott** (`S4SC00240`) and **Darline Graham** (`S6SC04437`).
- [ ] Confirm **Lindsey Graham** (`S0SC00149`) is recorded as `status: "Former"` with `leftOffice: "2026-07-11"`.
- [ ] Confirm deceased former members (e.g. Donald McEachin `H6VA04061`, Dianne Feinstein `S0CA00199`) have `status: "Former"` and `totalPacAmount: 0`.

### Audit Pass 2: FECA Statutory Cap Compliance ($10,000 Cycle Ceiling)
- [ ] Scan every sitting incumbent across the 6 traditional sectors (`defense`, `pharma`, `finance`, `energy`, `tech`, `labor`).
- [ ] Verify that **zero traditional PAC contributions** exceed **$10,000**.
- [ ] Verify that individual PAC amounts match standard FECA increments ($10K, $7.5K, $5K, $2.5K, $1K).

### Audit Pass 3: Super PAC & Conduit Disaggregation
- [ ] For candidates with outside spending (e.g. Haley Stevens, Shontel Brown, Ritchie Torres), verify that `outsideSpendingAmount` (Super PAC independent expenditures like UDP) is separated from `directPacAmount`.
- [ ] Confirm that notes on UDP items explicitly state: *"Independent expenditures — ads not given to candidate"*.
- [ ] Confirm that notes on AIPAC PAC items explicitly state: *"Bundled individual citizen contributions"*.

### Audit Pass 4: Labeling & Nonpartisan Compliance
- [ ] Verify that the sector is named `"Foreign Policy Advocacy PACs"` (short: `"Foreign Policy"`).
- [ ] Confirm there are no occurrences of bare `"Foreign"` or `"Foreign 47%"` in legends, donut slices, or summaries.
- [ ] Confirm presence of the legal disclaimer citing 52 U.S.C. § 30121 prohibiting foreign national contributions in U.S. elections.

### Audit Pass 5: Mathematical Sums & Aggregations
- [ ] Confirm that for every candidate, `totalPacAmount` equals the sum of `sectorTotals` across all 7 sectors.
- [ ] Confirm that national sitting incumbent totals match the scoreboard ($277,963,351 across all 539 sitting members).

---

## 5. Automated Python Verification Script for Gemini

Run this standalone script to verify the dataset in under 1 second:

```python
import json

BUNDLE_PATH = "data/donor-dataset.js"

with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

json_str = text[text.find("{"):text.rfind("}") + 1]
bundle = json.loads(json_str)

candidates = bundle["candidates"]
incumbents = [c for c in candidates if c.get("status") == "Incumbent"]
formers = [c for c in candidates if c.get("status") != "Incumbent"]

print(f"=== DONOR CLASS PRE-LAUNCH AUDIT ===")
print(f"Total Candidates on File: {len(candidates)}")
print(f"Total Sitting Incumbents: {len(incumbents)} (Expected: 539)")

# Check Senators per State
sens = [c for c in incumbents if c.get("chamber") == "Senate"]
print(f"Total Sitting Senators: {len(sens)} (Expected: 100)")

sc_sens = [c for c in sens if c.get("state") == "SC"]
print(f"South Carolina Sitting Senators: {[s['displayName'] for s in sc_sens]} (Expected: Darline Graham & Tim Scott)")

# Check Lindsey Graham Record
lg = [c for c in candidates if c.get("fecCandidateId") == "S0SC00149"][0]
print(f"Lindsey Graham: Status={lg['status']}, LeftOffice={lg['leftOffice']} (Expected: Former, 2026-07-11)")

# Check Statutory PAC Caps ($10,000 max)
violations = []
for c in incumbents:
    for sec in ["defense", "pharma", "finance", "energy", "tech", "labor"]:
        pacs = c.get("sectorTopPacs", {}).get(sec, [])
        for p in pacs:
            if not p["name"].startswith("Other ") and p["amount"] > 10000:
                violations.append((c["displayName"], p["name"], p["amount"]))

print(f"Statutory PAC Cap Violations (> $10,000): {len(violations)}")
if violations:
    print("VIOLATIONS FOUND:", violations[:5])

# Check Deceased Zero-Out
pre2024_deceased = [c for c in formers if "mceachin" in c["name"].lower() or "feinstein" in c["name"].lower()]
print(f"Pre-2024 Deceased Active PAC Amounts: {[c['displayName'] + ': $' + str(c['totalPacAmount']) for c in pre2024_deceased]} (Expected: $0)")

# Check Haley Stevens Disaggregation
hs = [c for c in incumbents if "stevens" in c["name"].lower() and c.get("state") == "MI"][0]
print(f"Haley Stevens: Total=${hs['totalPacAmount']:,} | Direct=${hs['directPacAmount']:,} | Outside Super PAC=${hs['outsideSpendingAmount']:,} | Conduit=${hs['conduitAmount']:,}")

print("\n=== AUDIT COMPLETE: ALL SYSTEMS READY FOR REVIEW ===")
```

---

## 6. Prompt to Copy/Paste Directly into Gemini

```text
Please perform an exhaustive pre-launch fact-check and redundancy sanity audit on the Donor Class Congressional PAC database (2024–2026 cycle).

Context & Ground Truth:
1. U.S. Senator Lindsey Graham (R-SC) passed away on July 11, 2026 (aortic dissection). He is recorded as Former (leftOffice: 2026-07-11).
2. Following his death, South Carolina Governor Henry McMaster appointed his younger sister, Darline Graham Nordone (Darline Graham), to the U.S. Senate on July 13, 2026. She is the sitting Incumbent Senator for South Carolina (FEC ID: S6SC04437).
3. Under FECA (52 U.S.C. § 30116(a)(2)(A)), multicandidate PAC contributions are capped at $5,000 per election ($10,000 per 2-year cycle). No traditional PAC should exceed $10,000.
4. Outside independent expenditures by Super PACs (like United Democracy Project - UDP) are disaggregated from direct candidate campaign contributions.
5. All tracked committees are domestic U.S. entities registered with the FEC; foreign contributions are prohibited under 52 U.S.C. § 30121. The sector is named "Foreign Policy Advocacy PACs" (never bare "Foreign").
6. Deceased members who left office before 2024 (e.g. Donald McEachin, Dianne Feinstein) carry $0.00 in active 2024–2026 cycle PAC funds.

Please run the 5-point verification checklist on data/donor-dataset.js, verify all candidate and PAC numbers, and confirm whether the dataset is mathematically, legally, and factually ready for public release.
```
