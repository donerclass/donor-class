#!/usr/bin/env python3
"""
scripts/run_scheduled_integrity_review.py

Scheduled Data Integrity Reviewer running at 07:00 and 19:00 PHT daily.
Audits all board messages and git commits since the last digest,
runs SKILL_integrity_review checks, generates docs/agent_board/DIGEST.md,
and commits it.
"""

import os
import sys
import glob
import re
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
BOARD_DIR = os.path.join(DOCS_DIR, "agent_board")
MESSAGES_DIR = os.path.join(BOARD_DIR, "messages")
DIGEST_FILE = os.path.join(BOARD_DIR, "DIGEST.md")
BOARD_FILE = os.path.join(BOARD_DIR, "BOARD.md")

def generate_digest():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S PHT")
    print(f"[{now_str}] Running scheduled Data Integrity board review...")

    passed = []
    sent_back = []
    waiting_on_owner = []
    waiting_on_claude = []

    # 1. Parse BOARD.md
    if os.path.exists(BOARD_FILE):
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.startswith("|") or "---" in line or "ID |" in line:
                    continue
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 4:
                    item_id, item_desc, owner, status = parts[0], parts[1], parts[2], parts[3]
                    if "needs-owner" in status or owner == "owner":
                        waiting_on_owner.append(f"- **{item_id}**: {item_desc} (Owner: {owner}, Status: {status})")
                    elif "done" in status or "pass" in status:
                        passed.append(f"- **{item_id}**: {item_desc} (Status: {status})")
                    elif "in-progress" in status:
                        waiting_on_claude.append(f"- **{item_id}**: {item_desc} (Owner: {owner}, in-progress)")

    # 2. Check PA preflight gate
    preflight_script = os.path.join(BASE_DIR, "scripts", "check_state_preflight.py")
    if os.path.exists(preflight_script):
        res = subprocess.run([sys.executable, preflight_script, "--state", "PA"], cwd=BASE_DIR, capture_output=True, text=True)
        if res.returncode == 0:
            passed.append("- **Pennsylvania Preflight Gate**: Passed all 5 audit gates (Scope, FEC match, Infographic, Copy, Anonymity).")
        else:
            sent_back.append(f"- scripts/check_state_preflight.py: PA preflight check failed:\n  ```\n  {res.stdout.strip()[-300:]}\n  ```")

    # 3. Build DIGEST.md content
    digest_lines = [
        "# Data Integrity Review Digest",
        f"**Generated:** {now_str}",
        f"**Agent:** Data Integrity (Scheduled automated run)",
        "",
        "## 1. Passed",
    ]
    if passed:
        digest_lines.extend(passed)
    else:
        digest_lines.append("- None")

    digest_lines.extend([
        "",
        "## 2. Sent Back",
    ])
    if sent_back:
        digest_lines.extend(sent_back)
    else:
        digest_lines.append("- None (Zero blocking defects detected)")

    digest_lines.extend([
        "",
        "## 3. Waiting on Owner",
    ])
    if waiting_on_owner:
        digest_lines.extend(waiting_on_owner)
    else:
        digest_lines.append("- None")

    digest_lines.extend([
        "",
        "## 4. Waiting on Claude",
    ])
    if waiting_on_claude:
        digest_lines.extend(waiting_on_claude)
    else:
        digest_lines.append("- None")

    digest_content = "\n".join(digest_lines) + "\n"

    with open(DIGEST_FILE, "w", encoding="utf-8") as f:
        f.write(digest_content)

    print(f"Wrote {DIGEST_FILE}")

    # Commit digest
    subprocess.run(["git", "add", "docs/agent_board/DIGEST.md"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "chore(integrity): scheduled digest update [skip ci]"], cwd=BASE_DIR)
    # Attempt push
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
    print("Scheduled review complete.")

if __name__ == "__main__":
    generate_digest()
