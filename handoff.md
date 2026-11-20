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

---

## 4. Launch Media, Anonymity & Day-1 Distribution Handoff

### Ready Media Assets
* **Launch Video:** `./donor-class-launch.mp4` (40s, 1920×1080 H.264 + 48kHz stereo AAC, closing with *"a quiet revolution has begun"* fade to black).
  * **Pre-upload:** Strip container metadata (`ffmpeg -i donor-class-launch.mp4 -map_metadata -1 -c copy donor-class-launch-clean.mp4`) and render a **9:16 vertical cut (1080×1920)** for TikTok, Instagram Reels, and YouTube Shorts.
* **Brand Graphics (Generated in Chat):** Avatar (**D** with canted top hat) + two X header banners (branded U.S. map banner and upside-down U.S. distress flag banner).

### Anonymity & Contact Funnel (`contact@donorclass.info`)
* **Email Routing Trap:** `contact@donorclass.info` uses Cloudflare Email Routing to forward to a personal inbox. **Receiving is anonymous, but replying from a personal inbox leaks the personal address and display name.**
* **Fix:** Point Cloudflare Email Routing to a brand-new, isolated **Proton Mail** (or **Zoho Mail**) inbox before launch (or treat the personal forward as strictly read-only), and disable auto-replies.
* **Repo & Domain Scrub:** Audit `index.html`, `app.js`, and `git log` / `git config` for personal names or emails before pushing live; confirm WHOIS privacy is active on `donorclass.info`; keep open DMs turned **off** on X and Reddit.

### X (Twitter) Growth & Agent Automation
* **Viral Playbook:** Upload `donor-class-launch.mp4` natively in the main tweet and put `https://donorclass.info` in the **first reply** (links in main posts get throttled). Quote-tweet breaking legislative/lobbying news with state/committee screenshots and run a *"50 States in 50 Days"* thread series.
* **X API Automation:** X retired its free API tier in Feb 2026 and uses pay-per-use credits ($0.015/post, $0.20/post with a link, $0.005/read; up to $70 starter credits with a card). A lightweight monitoring + link-free media posting agent costs ~$6–$10/mo. Keep replies human-in-the-loop to avoid spam flags, and do **not** automate initial account sign-ups (create accounts manually in ~15 min).

### Paid Ads (Facebook & YouTube) — Cost & Anonymity Warning
* **No free ad tier** (organic YouTube Shorts, Reels, and FB video are free).
* **Identity Disclosure Risk:** Both Meta and Google classify congressional/campaign-finance content under **Political / Social Issues / Election Ads** policies, requiring government photo ID, address/EIN verification, and a public **"Paid for by [Legal Name/Organization]"** disclaimer (archived 7 years in Meta Ad Library and Google's Transparency Report).
* **Recommendation:** **Skip paid political ads** unless running under a registered LLC/nonprofit entity; rely on free organic distribution (Reddit `r/dataisbeautiful` & `r/CivicTech`, X, TikTok, YouTube Shorts, `Show HN`, and journalist/Substack outreach).

### SEO & Google Search Ranking (AdSense vs. Search)
* **Note:** The existing Google AdSense tag (`ca-pub-6657813406289371` in `index.html`) monetizes traffic only—it does **not** boost search rankings.
* **Immediate SEO Priorities:**
  1. Add `robots.txt`, `sitemap.xml`, and `<link rel="canonical">` to `donorclass.info`, then submit the sitemap in **Google Search Console** (`google-site-verification` is already present in `index.html`).
  2. Pre-render **static state and member landing pages** (e.g., `/states/texas.html`, `/members/haley-stevens.html` with unique `<title>` and `<h1>` tags) so Google indexes all 50 states and 539 members instead of only the SPA shell.
  3. Embed `WebApplication` and `Dataset` **JSON-LD structured data** in `index.html`.

