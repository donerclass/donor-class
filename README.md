# DONOR CLASS — U.S. Congressional PAC & Lobby Tracker

An interactive, multi-sector campaign finance visualization platform that maps corporate, industry, and ideological Political Action Committee (PAC) contributions across all 50 states and sitting members of the U.S. Congress.

![License](https://img.shields.io/badge/Data-Official_FEC_Public_Records-0ea5e9)
![Coverage](https://img.shields.io/badge/Congress-539_Incumbents-10b981)
![Compliance](https://img.shields.io/badge/FECA_Compliance-Statutory_Capped_&_Disaggregated-f59e0b)
![Stack](https://img.shields.io/badge/Architecture-100%25_Client--Side_%2F_Zero--Build-8b5cf6)

---

## 1. Multi-Sector Campaign Finance Transparency

Rather than tracking a single lobby, **Donor Class** exposes the entire landscape of congressional influence across seven distinct economic and political sectors:

1. **Defense & Aerospace:** Lockheed Martin, Raytheon Technologies, Boeing, General Dynamics, Northrop Grumman, L3Harris, BAE Systems, Huntington Ingalls.
2. **Big Pharma & Health:** Pfizer, Eli Lilly, PhRMA, Blue Cross Blue Shield, Merck, AbbVie, Johnson & Johnson, UnitedHealth Group.
3. **Wall St & Big Finance:** Goldman Sachs, American Bankers Association (BANKPAC), JPMorgan Chase, Citadel, Credit Union National Association (CULAC), Morgan Stanley, Blackstone.
4. **Fossil Fuels & Energy:** Chevron, ExxonMobil, American Petroleum Institute (API), ConocoPhillips, KochPAC, NextEra Energy, Energy Transfer, Occidental.
5. **Big Tech & Telecom:** Google/Alphabet, Meta Platforms, Amazon, Microsoft, AT&T, Comcast, Apple, Qualcomm.
6. **Foreign Policy Advocacy PACs:** U.S. domestic committees registered with the FEC advocating on foreign policy, defense alliances, and pro-Israel diplomacy (AIPAC PAC, United Democracy Project, DMFI, J Street PAC, Republican Jewish Coalition PAC, NORPAC). *All tracked PACs are domestic American entities funded by U.S. citizens; 52 U.S.C. § 30121 prohibits foreign national contributions.*
7. **Labor Unions:** Teamsters (DRIVE), AFL-CIO, SEIU, IBEW, AFSCME, Machinists Non-Partisan League, United Auto Workers (UAW).

### Key Legal & Analytical Distinctions
* **FECA Statutory PAC Caps Enforced:** In accordance with 52 U.S.C. § 30116(a)(2)(A), direct contributions from multicandidate PACs to candidate committees are capped at $5,000 per election ($10,000 per 2-year cycle). Individual traditional PAC contributions on the platform reflect legal reporting limits.
* **Super PAC Independent Expenditures Disaggregated:** Independent outside spending (such as television and digital ad buys by Super PACs like United Democracy Project) is isolated and distinguished from direct candidate campaign contributions.
* **Domestic Legal Attribution:** Pro-Israel and foreign policy committees are domestic U.S. entities registered with the Federal Election Commission; they are explicitly categorized as domestic advocacy PACs to avoid factual mischaracterization.
* **Incumbent Roster Integrity:** Accurately reflects the 539 sitting members of the 118th/119th Congress (including Senior Senator Lindsey Graham, R-SC). Deceased or retired members who left office before 2024 (e.g. Rep. Donald McEachin, Sen. Dianne Feinstein) carry $0 in active cycle funds.
* **100% Independent & Offline:** Zero dependencies on external servers or third-party databases. The entire dataset is bundled client-side for instant responsiveness.

---

## 2. Monetization & Ad Revenue Architecture

Built-in support for standard IAB advertising units and audience monetization:

* **Top Leaderboard (728x90 desktop / 320x50 mobile):** Prime above-the-fold placement directly below the navigation bar. Ready for Google AdSense, NitroPay, EthicalAds, or Carbon Ads.
* **Sidebar Rectangle (300x250):** High-engagement slot embedded within the State Delegation Inspector panel.
* **Pro Tier & CSV Data Export:** Built-in 1-click CSV generator allows journalists, researchers, and political analysts to export clean, filtered PAC datasets with disaggregated direct PAC, Super PAC, and conduit earmarks.

---

## 3. Project Structure

```text
donor-class-tracker/
├── index.html                   # Semantic HTML5 app with native <dialog> modals and ad slots
├── styles.css                   # Responsive dark-theme styling, CSS variables, 7-sector color system
├── app.js                       # Interactive map engine, multi-sector aggregations, pan/zoom, CSV export
├── data/
│   └── donor-dataset.js         # Pre-bundled Congress dataset (539 incumbents, 7 sectors, 51 SVG paths)
└── scripts/
    └── generate_donor_dataset.py # Automated FEC bulk ingestion & sector mapping pipeline
```

---

## 4. Quick Start

### Run Locally (Zero Build or Dependencies Required)
```bash
cd donor-class-tracker
python3 -m http.server 8080
```
Open **`http://localhost:8080`** in any web browser.

### Deploying for Free

This project is 100% static and can be deployed in under 60 seconds with zero server cost:

1. **Cloudflare Pages / Netlify Drop:** Drag and drop the `donor-class-tracker` folder directly into the web dashboard.
2. **GitHub Pages:**
   ```bash
   git add .
   git commit -m "feat: complete FEC statutory compliance and data audit"
   git push origin main
   ```
   Under **Settings $\rightarrow$ Pages**, enable GitHub Pages from `main` branch.

---

## 5. Updating the Dataset

To re-aggregate contributions or adjust PAC sector assignments, run:
```bash
python3 scripts/generate_donor_dataset.py
```
This updates `data/donor-dataset.js` instantly.
