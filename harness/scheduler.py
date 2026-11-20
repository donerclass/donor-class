"""
DONOR CLASS // Event Chronometer & Scheduler
Synchronizes operations across Philippine Time (PHT, UTC+8) and US East Coast (EST, UTC-5).
"""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from .config import TIMEZONE_PRIMARY, TIMEZONE_SECONDARY, SCHEDULE_MORNING_BRIEF, SCHEDULE_PRIME_DROP

class OperationalScheduler:
    def __init__(self):
        self.tz_pht = ZoneInfo(TIMEZONE_PRIMARY)
        self.tz_est = ZoneInfo(TIMEZONE_SECONDARY)

    def get_clocks(self) -> dict:
        now_pht = datetime.now(self.tz_pht)
        now_est = datetime.now(self.tz_est)
        return {
            "pht_time": now_pht.strftime("%H:%M:%S"),
            "pht_date": now_pht.strftime("%Y-%m-%d"),
            "est_time": now_est.strftime("%H:%M:%S"),
            "est_date": now_est.strftime("%Y-%m-%d"),
            "pht_iso": now_pht.isoformat(),
            "est_iso": now_est.isoformat()
        }

    def get_next_milestone(self) -> dict:
        now_pht = datetime.now(self.tz_pht)
        today = now_pht.date()

        brief_h, brief_m = map(int, SCHEDULE_MORNING_BRIEF.split(":"))
        drop_h, drop_m = map(int, SCHEDULE_PRIME_DROP.split(":"))

        brief_dt = datetime.combine(today, time(brief_h, brief_m), tzinfo=self.tz_pht)
        drop_dt = datetime.combine(today, time(drop_h, drop_m), tzinfo=self.tz_pht)

        events = []
        if now_pht < brief_dt:
            events.append(("Morning Executive Briefing", brief_dt))
        else:
            events.append(("Morning Executive Briefing", brief_dt + timedelta(days=1)))

        if now_pht < drop_dt:
            events.append(("50-State Prime Campaign Drop", drop_dt))
        else:
            events.append(("50-State Prime Campaign Drop", drop_dt + timedelta(days=1)))

        # Sort by earliest upcoming
        events.sort(key=lambda x: x[1])
        next_event, next_time = events[0]
        delta = next_time - now_pht
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)

        return {
            "event_name": next_event,
            "target_time_pht": next_time.strftime("%Y-%m-%d %H:%M:%S PHT"),
            "target_time_est": next_time.astimezone(self.tz_est).strftime("%Y-%m-%d %H:%M:%S EST"),
            "countdown_str": f"{hours}h {minutes}m remaining"
        }
