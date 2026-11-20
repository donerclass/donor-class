# DONOR CLASS // AUTONOMOUS OPERATIONAL HARNESS

**Architecture:** Deterministic Scheduling & Safety Controller for Campaign Distribution  
**Primary Timezone:** Asia/Manila (PHT, UTC+8)  
**Target Market Timezone:** America/New_York (EST, UTC-5)  
**Security Policy:** Strict Team Anonymity (`Donor Class Team <contact@donorclass.info>`)  
**Hard Constraint:** Zero-Emoji Policy across all automated communications, posts, and code.

---

## 1. Overview

The `harness` directory provides the orchestration, state management, scheduling, and safety circuit breakers that govern DONOR CLASS. It transforms manual prompt-driven operations into an automated, verifiable civic intelligence engine.

---

## 2. Directory Structure

```
harness/
├── config.py           # Master constants, schedule definitions, and channel parameters
├── state.json          # Persistent state ledger (50-state calendar, verified post IDs, live snipes)
├── state_manager.py    # State CRUD operations and audit trail logging
├── preflight_linter.py # Pre-flight validation (zero-emoji, character limits, URL unfurl parameters)
├── scheduler.py        # Event chronometer synchronized to Manila PHT and Washington EST
├── runner.py           # CLI entrypoint for operational commands and status inspection
└── README.md           # This architecture guide
```

---

## 3. Operational CLI Usage

Run commands from the repository root:

```bash
# 1. Print full operational dashboard, live clocks, and milestone countdown
python3 -m harness.runner status

# 2. Lint draft post against zero-emoji, URL unfurl, and character limits
python3 -m harness.runner lint "Here are the receipts: https://donorclass.info/?ref=x"

# 3. Verify FEC dataset bundle integrity (539 members, 7 sectors)
python3 -m harness.runner verify-dataset
```

---

## 4. Operational Schedule & Event Loop (PHT)

| Time (PHT) | Time (EST) | Event Type | Description |
| :--- | :--- | :--- | :--- |
| **04:30 AM** | 03:30 PM (Prev) | Pre-Brief Audit | Scrapes Cloudflare request logs, X engagement metrics, and Reddit thread activity. |
| **05:30 AM** | 04:30 PM (Prev) | Morning Briefing | Updates and deploys the master executive briefing dashboard for your wake-up review. |
| **10:30 PM** | 09:30 AM | Prime Campaign Drop | Publishes the daily 50-State thread on X and cross-posts to target state subreddits. |
| **Continuous**| Continuous | Tactical News Sniper | Scans verified newsroom clips (`@BreakingPointsx`, `@LeverNews`) and replies with verified receipts (max 5/day). |

---

## 5. Safety Circuit Breakers

1. **Zero-Emoji Enforcer:** All outgoing posts are passed through `preflight_linter.py`. Any emoji sequence causes an immediate pre-flight abortion.
2. **URL Cache-Busting:** Any link to `donorclass.info` must contain a query parameter (`?ref=...` or `?state=...&ref=...`) to avoid stale crawler card rendering bugs.
3. **Daily Snipe Cap:** Maximum of 5 tactical news replies per 24 hours to maintain 100% verified account reputation and prevent algorithmic throttling.
