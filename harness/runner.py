"""
DONOR CLASS // Unified Harness Command-Line Controller
Entrypoint for inspecting status, running preflight linters, and managing the campaign.
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to sys.path if run directly
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from harness.config import BASE_URL, STATE_SCHEDULE, DATA_FILE
from harness.state_manager import StateManager
from harness.preflight_linter import PreflightLinter
from harness.scheduler import OperationalScheduler

def cmd_status(args):
    sm = StateManager()
    sched = OperationalScheduler()
    clocks = sched.get_clocks()
    milestone = sched.get_next_milestone()
    progress = sm.get_campaign_progress()
    snipes = sm.state.get("tactical_snipes", [])

    print("=" * 70)
    print("  DONOR CLASS // AUTONOMOUS OPERATIONAL HARNESS")
    print("=" * 70)
    print(f"  Live Clocks:     Manila: {clocks['pht_time']} PHT  |  Washington: {clocks['est_time']} EST")
    print(f"  Next Milestone:  {milestone['event_name']} in {milestone['countdown_str']}")
    print(f"                   Target: {milestone['target_time_pht']}")
    print("-" * 70)
    print(f"  50-State Cycle:  Day {progress['current_day']} of 50 ({progress['completion_percentage']}% Complete)")
    print(f"  Completed (1):   {sm.state.get('states_completed', [])}")
    print(f"  Active State:    {progress['active_state']} (Scheduled tonight 22:30 PHT)")
    print(f"  Staged State:    {progress['staged_state']} (Pre-staged for tomorrow)")
    print("-" * 70)
    print(f"  Tactical Snipes: {len(snipes)} of 5 Daily Limit")
    for s in snipes:
        print(f"    • Snipe #{s['id']}: {s['target_topic']} -> {s['reply_tweet_url']}")
    print("=" * 70)

def cmd_lint(args):
    text = args.text
    is_tweet = not args.not_tweet
    print(f"Linting input text ({len(text)} chars)...")
    passed, violations = PreflightLinter.lint_post(text, is_tweet=is_tweet)
    if passed:
        print("PASS: Text complies with all safety rules (zero emojis, URL unfurl parameters, character limits).")
        sys.exit(0)
    else:
        print("FAIL: Preflight violations detected:")
        for v in violations:
            print(f"  • {v}")
        sys.exit(1)

def cmd_verify_dataset(args):
    if not DATA_FILE.exists():
        print(f"ERROR: Dataset not found at {DATA_FILE}")
        sys.exit(1)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    prefix = "window.DONOR_BUNDLE = "
    if content.startswith(prefix):
        content = content[len(prefix):].rstrip(";\n ")
    
    try:
        data = json.loads(content)
        candidates = data.get("candidates", [])
        sectors = data.get("sectors", {})
        print(f"PASS: Dataset parsed successfully.")
        print(f"  • Version: {data.get('version')} (Cycle: {data.get('fecCycle')})")
        print(f"  • Candidates Tracked: {len(candidates)} members")
        print(f"  • Sectors Defined: {len(sectors)} sectors ({list(sectors.keys())})")
    except Exception as e:
        print(f"FAIL: JSON parsing error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="DONOR CLASS Operational Harness")
    subparsers = parser.add_subparsers(dest="command", help="Harness command")

    # Status
    subparsers.add_parser("status", help="Print operational dashboard and milestone clocks")

    # Lint
    p_lint = subparsers.add_parser("lint", help="Lint text against zero-emoji, character count, and URL safety")
    p_lint.add_argument("text", help="Text string to evaluate")
    p_lint.add_argument("--not-tweet", action="store_true", help="Disable 280-character limit check")

    # Verify Dataset
    subparsers.add_parser("verify-dataset", help="Verify FEC dataset integrity")

    args = parser.parse_args()
    if not args.command or args.command == "status":
        cmd_status(args)
    elif args.command == "lint":
        cmd_lint(args)
    elif args.command == "verify-dataset":
        cmd_verify_dataset(args)

if __name__ == "__main__":
    main()
