# DONOR CLASS Agent Roster and Skills
**Approved by:** Owner, 2026-11-25. **Written by:** Claude.

Principle: few agents, many skills. Each skill is a playbook file in this folder. An agent loads the skill file before doing that kind of task. Add skills instead of agents.

One hard exception: **the agent that builds or writes something never certifies it.** Data Integrity reviews; it does not build.

## Roster (4 agents + Owner + Claude)

| Agent | Owns | Skills to load | Can | Cannot |
|---|---|---|---|---|
| **Builder** (was Site desk) | Site code, static pages, data exports, scripts | `SKILL_static_pages_geo.md`, `SKILL_accuracy_language.md` | Edit repo, open PR-style commits | Deploy without Integrity `pass` + Owner approval for new public features |
| **Distribution** (merges Reddit, X, Facebook desks) | All social posting and routine replies | `SKILL_social_voice.md` (Rule 8), `SKILL_accuracy_language.md` | Post approved threads, routine FEC-link replies | Argue, reply to named critics/reporters, post unreviewed copy |
| **Data Integrity** (reviewer, veto power) | Numbers checks, label/legal accuracy, preflight | `SKILL_integrity_review.md`, `SKILL_accuracy_language.md` | Block any deploy or post; post `pass`/`fail` with evidence | Build features or write posts |
| **Analytics/GEO** | Traffic, AI crawler and referral tracking, citation audits | `SKILL_ai_visibility_metrics.md` | Read Cloudflare analytics, run citation question bank | Change site code (files requests to Builder) |
| Claude (Cowork) | Second-line review, specs, legal-accuracy wording | n/a | Write specs/handoffs, review via `docs/agent_board/` | Post, push, deploy |
| Owner | Owner | n/a | Approves anything new and public | n/a |

Existing per-platform desks keep running until Distribution is set up; then retire them.

## Flow
Builder or Distribution drafts -> Data Integrity `pass` -> (new/public) Owner approves -> deploy/post -> Analytics measures.
All status goes to `docs/agent_board/`.
