"""
DONOR CLASS // State Manager & Ledger Controller
Manages operational state, campaign progression, and post history.
"""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from .config import STATE_FILE, TIMEZONE_PRIMARY, STATE_SCHEDULE

class StateManager:
    def __init__(self, state_file: Path = STATE_FILE):
        self.state_file = state_file
        self.tz = ZoneInfo(TIMEZONE_PRIMARY)
        self.state = self._load()

    def _load(self) -> dict:
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found at {self.state_file}")
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def now_pht_iso(self) -> str:
        return datetime.now(self.tz).isoformat()

    def log_audit(self, action: str, details: str):
        record = {
            "action": action,
            "actor": "Donor Class Team <contact@donorclass.info>",
            "timestamp_pht": self.now_pht_iso(),
            "details": details
        }
        self.state.setdefault("audit_trail", []).append(record)
        self.state["last_audit_timestamp_pht"] = self.now_pht_iso()
        self.save()

    def get_campaign_progress(self) -> dict:
        total = len(STATE_SCHEDULE)
        completed = len(self.state.get("states_completed", []))
        return {
            "current_day": self.state.get("current_day", 1),
            "completed_count": completed,
            "total_count": total,
            "completion_percentage": round((completed / total) * 100, 1),
            "active_state": self.state.get("active_state", "CA"),
            "staged_state": self.state.get("staged_state", "FL")
        }

    def record_campaign_post(self, state_code: str, post_data: dict):
        self.state.setdefault("live_campaign_posts", {})[state_code] = post_data
        if state_code not in self.state.get("states_completed", []):
            self.state.setdefault("states_completed", []).append(state_code)
            if state_code in self.state.get("states_queued", []):
                self.state["states_queued"].remove(state_code)
        
        # Advance active state
        idx = STATE_SCHEDULE.index(state_code) if state_code in STATE_SCHEDULE else -1
        if idx != -1 and idx + 1 < len(STATE_SCHEDULE):
            self.state["active_state"] = STATE_SCHEDULE[idx + 1]
            if idx + 2 < len(STATE_SCHEDULE):
                self.state["staged_state"] = STATE_SCHEDULE[idx + 2]
            self.state["current_day"] = idx + 2

        self.log_audit("CAMPAIGN_POST_RECORDED", f"Recorded launch of Day {self.state['current_day'] - 1} for state {state_code}")

    def record_tactical_snipe(self, snipe_data: dict):
        snipes = self.state.setdefault("tactical_snipes", [])
        snipe_data["id"] = len(snipes) + 1
        snipe_data["timestamp_pht"] = self.now_pht_iso()
        snipe_data["status"] = "VERIFIED_LIVE"
        snipes.append(snipe_data)
        self.log_audit("SNIPE_RECORDED", f"Recorded snipe #{snipe_data['id']} under {snipe_data.get('target_account')} for topic: {snipe_data.get('target_topic')}")

    def get_snipes_count_24h(self) -> int:
        return len(self.state.get("tactical_snipes", []))
