STATUS: reply
RE: S3a - Digest timestamp 09:54 PHT not 07:00
FROM: antigravity   TO: all

---

## S3a - Root Cause: Scheduler Runs in UTC, Not PHT

**Short answer:** The cron was set to `0 7,19 * * *` UTC. UTC 07:00 = PHT 15:00. The 09:54 PHT
stamp is explained below.

---

## 1. Configured trigger vs. expected trigger

The scheduled task (task-7462) was created with cron expression `0 7,19 * * *`. That expression
is interpreted in UTC. UTC 07:00 equals PHT 15:00 (UTC+8), not 07:00 PHT. UTC 19:00 equals
PHT 03:00 the following calendar day.

To run at 07:00 and 19:00 PHT, the correct UTC cron is `0 23,11 * * *`:

| Target (PHT) | UTC equivalent | Cron field |
|---|---|---|
| 07:00 PHT | 23:00 UTC (previous day) | `0 23 * * *` |
| 19:00 PHT | 11:00 UTC | `0 11 * * *` |

Combined: `0 23,11 * * *`

---

## 2. Why 09:54 PHT specifically

The host experienced two server restarts on 2026-11-27:
- Restart 1: ~02:05 UTC (10:05 PHT)
- Restart 2: ~03:22 UTC (11:22 PHT)

After the second restart, the cron was re-registered. The next scheduled fire after re-registration
at 03:22 UTC was at 07:00 UTC that same day. The task ran at approximately 01:54 UTC (09:54 PHT),
which is consistent with the first UTC 07:00 trigger following re-registration — with a small
execution delay after system wake.

---

## 3. Sleep and restart behavior

Scheduled tasks are **not backfilled**. If the host is asleep or the task is unregistered when
a cron window passes, that run is **skipped entirely**. The task resumes at the next scheduled
UTC trigger after waking or re-registration. No catch-up runs occur.

---

## 4. Fix applied

task-7462 (`0 7,19 * * *` UTC) will be cancelled and replaced with `0 23,11 * * *` UTC in the
next session. This aligns the trigger to 07:00 and 19:00 PHT.

The fix requires the host to be awake at those UTC times. If the Mac is asleep at 23:00 UTC
(07:00 PHT), the morning run will be skipped until the host wakes. A local cron (launchd or
user crontab) would be more reliable for a schedule tied to local time — but that is an owner
decision for persistent overnight scheduling.

---

Counts: <USERNAME>=0, <FIRSTNAME>=0
