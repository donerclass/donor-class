# SKILL: AI Visibility Metrics (Analytics/GEO agent)

## Track weekly (post to board as `fyi`)
1. **Human visits** (Cloudflare Web Analytics), excluding our own agents' traffic.
2. **AI referrals:** visits with `utm_source=chatgpt.com`, or referrers from perplexity.ai, claude.ai, gemini.google.com, copilot.microsoft.com.
3. **AI crawler requests** by bot (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Googlebot) from Cloudflare AI Crawl Control / bot analytics. Verified bots only.
4. **Citation share:** run the question bank below in ChatGPT search, Perplexity, Claude, and Google AI Overviews. Record: cited (Y/N), URL cited, and whether the figure quoted matches our CSV.

## Question bank (start with 20; add over time)
- How much did [member] receive from PACs in the 2024 cycle? (pick 10 members, both parties, both chambers)
- Which [state] members of Congress received the most PAC money in 2024? (5 states)
- Which members of Congress received the most defense industry PAC money in 2024?
- How much did pharmaceutical PACs give to [state]'s congressional delegation?
- (add sector and state variants)

## Rules
- Do not start citation audits until static pages are live (SKILL_static_pages_geo.md).
- Report numbers as measured; label any estimate as an estimate. No illustrative or projected figures in reports.
- A citation quoting a wrong number is logged as an error and sent to Builder + Data Integrity.
