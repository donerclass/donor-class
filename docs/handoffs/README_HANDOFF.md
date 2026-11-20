# Antigravity Launch Handoff: Video, Privacy & Day-1 Distribution

**Project:** DONOR CLASS (`https://donorclass.info`)  
**Priority:** **URGENT — Launch & distribute to as many people as possible TODAY**  
**Related Audit:** See [`handoff.md`](./handoff.md) (5/5 pre-launch audit checks passed; 1 minor `"Other Foreign Policy Advocacy PACs"` categorization note to review).

---

## 1. Launch Video Asset (Ready)

* **File:** `donor-class-launch.mp4` (`./donor-class-launch.mp4`)
* **Specs:** 40.0 seconds, 1920×1080 (16:9), 30 fps H.264 + 48 kHz stereo AAC ambient score, 8.0 MB.
* **Content:** Built directly from live 2024–2026 FEC totals in `data/donor-dataset.js` (539 sitting members, $277.0M tracked across 50 states and 7 sectors, FECA-capped vs. Super PAC vs. Conduit disaggregation) and closes with **"a quiet revolution has begun"** fading to black.
* **Before Uploading Anywhere:**
  1. Strip container metadata: `ffmpeg -i donor-class-launch.mp4 -map_metadata -1 -c copy donor-class-launch-clean.mp4`
  2. Create a **9:16 vertical cut (1080×1920)** for TikTok, Instagram Reels, and YouTube Shorts so mobile feeds display full-screen without letterboxing.

---

## 2. Anonymity & Contact Funnel (Critical Pre-Deploy Check)

The operator wants to stay **as anonymous as possible** while still letting journalists, researchers, and users reach out—and choosing who to reply to.

* **Email (`contact@donorclass.info`):**
  * Currently configured via **Cloudflare Email Routing** forwarding to the operator's personal email.
  * **Important:** Receiving is anonymous, **but replying from a personal inbox leaks the personal email address and display name.**
  * **Fix:** Point Cloudflare Email Routing to a brand-new, isolated **Proton Mail** (or **Zoho Mail**) inbox for `donorclass.info` before launch—or strictly treat the personal forward as read-only and never hit Reply from it. Also ensure vacation/auto-replies are disabled on any forwarded inbox.
* **Repo & Site Scrub:**
  * Audit `index.html`, `app.js`, and `git log` / `git config` for any personal names, personal emails, or local paths before pushing to GitHub / Cloudflare Pages / Netlify.
  * Verify WHOIS privacy redaction is active on `donorclass.info`.
* **Social Accounts:**
  * Turn **off** open DMs on X and Reddit. Direct all inquiries to `contact@donorclass.info` (or an anonymous web form) in the bio and site footer.

---

## 3. Day-1 Distribution Plan (Maximum Reach Today)

Pair **Reddit** (fastest traffic from zero followers) with **X (Twitter)** (fastest pickup by political reporters and Substack writers), plus **TikTok / YouTube Shorts** for algorithmic reach.

| Platform | Asset | Framing & Execution |
| :--- | :--- | :--- |
| **Reddit** | 16:9 video or live link + screenshot | Post to `r/dataisbeautiful`, `r/CivicTech`, `r/SideProject`, and state subreddits (MI, SC, CA, TX). Lead with neutral methodology, FECA statutory compliance, and 1-click CSV export. |
| **X (Twitter)** | Native 16:9 `donor-class-launch.mp4` | Hook: *"We mapped $277M in FEC PAC & Super PAC money across all 539 sitting members of Congress."* Upload native MP4 in the main post; put `https://donorclass.info` in the **first reply** (so links aren't throttled). |
| **TikTok / Reels / Shorts** | 9:16 vertical cut (1080×1920) | Lead with the opening question immediately. Pin a comment asking viewers to drop their state so the account can reply with their delegation's numbers. |
| **Hacker News (`Show HN`)** | Live site URL | *"Show HN: Donor Class – 100% client-side, zero-build FEC PAC tracker across 539 sitting members."* Emphasize zero dependencies, statutory disaggregation, and CSV export. |
| **Journalists / Substack** | Short pitch + video + CSV export | Reach out to campaign-finance reporters and local political newsletters highlighting the pre-audited 2024–2026 dataset. |

---

## 4. Account Setup & Agent Automation Split

* **Manual (15 minutes, do NOT automate):** Sign up for X, Reddit, TikTok, YouTube, and Bluesky manually. Automated sign-ups trigger SMS checks, CAPTCHAs, and device-fingerprinting bans on new accounts.
* **Agent-Automated (Post-Setup):**
  1. **Brand Profile Kit:** Generate consistent pseudonymous bios, handles, banners, and avatar crops.
  2. **Automated Video Factory:** Render the 9:16 vertical cut plus daily 15-second **state-spotlight** clips directly from `data/donor-dataset.js`.
  3. **API Publishing:** Automate native video posts to X, Bluesky, and YouTube (or via a unified scheduler API like Postiz, Ayrshare, or Buffer).
  4. **Human-in-the-Loop:** Have agents draft Reddit posts, `Show HN`, and journalist outreach emails for quick human review and submission.

---

## 5. Immediate Next Actions for Antigravity

1. **Deploy `donorclass.info`** (Cloudflare Pages / Netlify) after scrubbing any personal git/code metadata and reviewing the minor `handoff.md` edge case.
2. **Generate the metadata-stripped 16:9 and 9:16 video cuts** from `donor-class-launch.mp4`.
3. **Prepare Day-1 launch copy** (X thread, Reddit posts, `Show HN`, TikTok/Shorts captions) so posts can go live immediately once the operator finishes manual account creation.
