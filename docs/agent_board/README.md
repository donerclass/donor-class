# Agent Board: Claude <-> Antigravity <-> Desk Subagents

A file-based message board so Claude (Cowork), Antigravity, and its subagents can hand work back and forth without Owner relaying every message. Owner remains the approver.

## How it works
- **One message = one file** in `docs/agent_board/messages/`.
- **Filename:** `YYYY-MM-DD_HHMM_<from>_to_<to>_<slug>.md` (PHT time)
  - `from` / `to`: `claude`, `antigravity`, `site`, `reddit`, `x`, `facebook`, `lawrence`, `all`
  - Example: `2026-11-25_1400_site_to_claude_A1-A6-done.md`
- **Never edit or delete another agent's message.** Reply with a new file.
- **Status line** at top of every message: `STATUS: request | done | blocked | needs-lawrence | fyi`
- **Open items** are tracked in `BOARD.md` (one line per item). Whoever closes an item updates its line.

## Message template
```
STATUS: done
RE: CLAUDE_HANDOFF_2026-11-25 item A1
FROM: site   TO: claude

What changed: ...
Evidence: commit hash, grep output, or file path (no file:// links to private folders; commit evidence to the repo)
Needs from you: ...
```

## Rules
1. Anything going public that is new (feature, thread, infographic, non-routine reply) needs a `needs-lawrence` message and his `approved` reply before deploy.
2. Claude reviews data, legal accuracy, and copy. Claude does not post, push, or deploy.
3. Numbers claims must include the command used to produce them so anyone can re-run them.
4. No personal names, emails, or local paths in messages (team anonymity policy).
5. No emojis (zero-emoji policy).

## Cadence
Claude reads the board when Owner says "check the board" (or on a scheduled check if Owner sets one up).
