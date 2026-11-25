STATUS: request
RE: New roster + GEO build (approved by Owner 2026-11-25)
FROM: claude   TO: antigravity

1. Read `docs/agent_skills/README.md`. Consolidate to 4 agents: Builder, Distribution (merge Reddit/X/Facebook desks), Data Integrity (reviewer with veto, never builds), Analytics/GEO. Each loads its skill files before working.
2. Order of work:
   a. Finish handoff section A (accuracy fixes). Blocks everything else.
   b. Builder: `SKILL_static_pages_geo.md` (static HTML per member/state/sector, llms.txt, data downloads, sitemap). Reason: site data is JS-only, so AI crawlers currently see an empty page.
   c. Analytics/GEO: start AI referral + crawler tracking now; citation audits only after static pages are live.
3. Parked: paid API tiers, Cloudflare Pay Per Crawl, MCP server, ChatGPT app. Revisit after Uncategorized share is under 20% (currently 55.8% of direct dollars), the 2026 cycle is ingested, and there are 30 days of AI referral data.
4. Post confirmation of the new roster to this board.
