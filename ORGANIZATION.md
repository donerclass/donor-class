# DONOR CLASS // REPOSITORY DIRECTORY & ACCOUNTABILITY INDEX

**Classification:** Nonpartisan Campaign Finance Intelligence & Viral Distribution Platform  
**Production Site:** [https://donorclass.info](https://donorclass.info)  
**Hosting Architecture:** Cloudflare Pages (100% Static Client-Side Edge Distribution)  
**Security Policy:** Strict Team Anonymity (`Donor Class Team <contact@donorclass.info>`)  
**Visual Constraint:** Strict Zero-Emoji Policy across all source code, assets, and metadata.

---

## 1. Directory Tree & Responsibility Matrix

```
./
├── index.html                   # Cloudflare Pages Web Root: Main Interactive Dashboard & Map
├── app.js                       # Client-Side Application Engine (Sectors, Filters, URL Deep-Linking)
├── styles.css                   # Custom Theme Tokens & Visual Styling
├── privacy.html                 # Nonpartisan Privacy Policy & Terms
├── robots.txt                   # Web Crawler Directives
├── sitemap.xml                  # Search Engine Sitemap Index
├── logo-master.png              # Master High-Resolution Top-Hat "D" Branding
├── favicon.ico                  # Root Multi-Resolution Browser Favicon
├── favicon.png                  # Standard 32x32 Favicon
├── favicon-16x16.png            # 16x16 Favicon
├── favicon-32x32.png            # 32x32 Favicon
├── apple-touch-icon.png         # iOS Mobile App Icon
├── og-image.jpg                 # OpenGraph Social Card (1200x630)
├── og-image-square.jpg          # Square OpenGraph Thumbnail (800x800)
├── README.md                    # Core System Documentation
├── ORGANIZATION.md              # This Master Architecture & Accountability Index
├── .gitignore                   # Git Ignore Rules (Protects Credentials & Video Blobs)
│
├── assets/                      # All Static Media, Visuals & Infographics
│   ├── infographics/            # Generated 50-State Infographics (1200x675)
│   │   ├── texas-infographic.png        # Day 1: Texas Delegation Breakdown ($14.15M)
│   │   ├── california-infographic.png   # Day 2: California Delegation Breakdown ($31.8M)
│   │   └── florida-infographic.png      # Day 3: Florida Delegation Breakdown ($16.8M)
│   ├── videos/                  # Launch & Vertical Video Formats
│   │   ├── donor-class-launch.mp4               # Horizontal 16:9 Launch Video
│   │   ├── donor-class-launch-clean.mp4         # Textless Clean Cut
│   │   ├── donor-class-launch-vertical-9x16.mp4 # TikTok/Reels/Shorts 9:16 Cut
│   │   └── donor-class-truth-vertical.mp4       # Campaign Narrative Vertical Cut
│   └── screenshots/             # Staged Reference Images & Timeline Verifications
│       ├── image.jpeg
│       ├── image1.jpeg
│       ├── image2.jpeg
│       ├── image3.jpeg
│       ├── image4.jpeg
│       └── image5.jpeg
│
├── data/                        # FEC Primary Data Bundles
│   └── donor-dataset.js         # Window Bundle with 539 Reps & 2,900+ PAC Contribution Nodes
│
├── docs/                        # Project Documentation, Records & Security
│   ├── handoffs/                # Session Handoff Summaries & Analytical Audits
│   │   ├── GEMINI_FACT_CHECK_HANDOFF.md
│   │   ├── README_HANDOFF.md
│   │   └── handoff.md
│   └── security/                # Critical Credentials & Private Key Storage (.gitignored)
│       └── proton-recovery-phrase.pdf
│
├── scripts/                     # Data Pipelines & Dataset Compilers
│   └── generate_donor_dataset.py # Automated FEC Bulk Exporter & Parser
│
└── harness/                     # The Autonomous Operations Harness Engine
    ├── config.py                # Operational Constants, Schedules & Channel Definitions
    ├── state.json               # 50-State Campaign Calendar & Live Sniper Ledger
    ├── state_manager.py         # State Ledger CRUD & Audit Trail
    ├── preflight_linter.py      # Hard Zero-Emoji & FEC Dataset Verification Linter
    ├── scheduler.py             # Event Chronometer Aligned to Manila PHT / Washington EST
    ├── runner.py                # Command-Line Harness Controller
    └── README.md                # Harness Usage & Architecture Guide
```

---

## 2. Accountability & Folder Purposes

| Directory | Primary Purpose | Security / Access Controls | Git Status |
| :--- | :--- | :--- | :--- |
| **Root (`/`)** | Web deployment root for Cloudflare Pages. Must only contain assets needed for the public web app. | Public CDN (read-only edge) | Tracked |
| `assets/infographics/` | Storage for 1200x675 state delegation infographics used in daily social campaigns. | Public Social Assets | Tracked |
| `assets/videos/` | High-definition promotional and vertical short-form video files. | Internal Media Archive | Ignored by Git (Prevents Repo Bloat) |
| `assets/screenshots/` | Internal verification evidence and screenshot captures. | Internal Reference | Ignored by Git |
| `data/` | FEC verified dataset bundle loaded directly into client browser memory. | Public Data Asset | Tracked |
| `docs/handoffs/` | Historical logs, multi-agent context handoffs, and fact-check audits. | Engineering Internal | Tracked |
| `docs/security/` | Cold storage for recovery keys, passwords, and verification secrets. | Strictly Private / Zero Web Exposure | Strictly Ignored by Git |
| `scripts/` | Data ETL and JSON dataset generation scripts. | Developer Tooling | Tracked |
| `harness/` | Autonomous operations harness, scheduling state, and pre-flight validation. | Operations Engine | Tracked |
