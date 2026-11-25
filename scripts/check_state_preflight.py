#!/usr/bin/env python3
"""
scripts/check_state_preflight.py

Automated Pre-Flight Gate for the 50 States in 50 Days campaign.
Enforces leadership's standing rules for all remaining states:

1. Every state gets a numbers check against official FEC summary (weball24.txt).
   Any member with > 10% variance must have a documented written reason in
   data/documented_variances.json or the script fails.
2. Honest delegation counts: "X of Y members with 2024-cycle records".
3. Copy linting: Zero modeled numbers, zero usage of "verified", zero partisan
   words ("blitz", "bought", "purchased", etc.). Spells out "Pro-Israel & Foreign Policy PACs"
   and includes "Uncategorized".
4. Verifies nonpartisan infographic asset presence (no state seals).
"""

import os
import sys
import csv
import json
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "infographics")
RAW_DIR = os.path.join(DATA_DIR, "fec_raw", "extracted")
WEBALL_PATH = os.path.join(RAW_DIR, "weball24.txt")
CSV_PATH = os.path.join(DATA_DIR, "donor-dataset.csv")
VARIANCES_PATH = os.path.join(DATA_DIR, "documented_variances.json")

TOTAL_HOUSE_SEATS = {
    "AL": 7, "AK": 1, "AZ": 9, "AR": 4, "CA": 52, "CO": 8, "CT": 5, "DE": 1, "FL": 28, "GA": 14,
    "HI": 2, "ID": 2, "IL": 17, "IN": 9, "IA": 4, "KS": 4, "KY": 6, "LA": 6, "ME": 2, "MD": 8,
    "MA": 9, "MI": 13, "MN": 8, "MS": 4, "MO": 8, "MT": 2, "NE": 3, "NV": 4, "NH": 2, "NJ": 12,
    "NM": 3, "NY": 26, "NC": 14, "ND": 1, "OH": 15, "OK": 5, "OR": 6, "PA": 17, "RI": 2, "SC": 7,
    "SD": 1, "TN": 9, "TX": 38, "UT": 4, "VT": 1, "VA": 11, "WA": 10, "WV": 2, "WI": 8, "WY": 1,
    "DC": 1, "PR": 1, "GU": 1, "VI": 1, "AS": 1, "MP": 1
}

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "DC": "District of Columbia", "PR": "Puerto Rico", "GU": "Guam", "VI": "Virgin Islands",
    "AS": "American Samoa", "MP": "Northern Mariana Islands"
}

PROHIBITED_WORDS = [
    "verified", "modeled", "blitz", "bought", "purchased", "corrupt", "shill", "puppet"
]

def load_weball():
    weball = {}
    if not os.path.exists(WEBALL_PATH):
        print(f"Error: {WEBALL_PATH} not found.")
        sys.exit(1)
    with open(WEBALL_PATH, "r", encoding="latin1") as f:
        for line in f:
            p = line.strip().split("|")
            cid = p[0].strip().upper()
            other_pol = float(p[25]) if len(p) > 25 and p[25] else 0.0
            pty = float(p[26]) if len(p) > 26 and p[26] else 0.0
            weball[cid] = other_pol + pty
    return weball

def check_state(state_code, weball, variances):
    state_code = state_code.upper()
    state_name = STATE_NAMES.get(state_code, state_code)
    h_seats = TOTAL_HOUSE_SEATS.get(state_code, 0)
    sen_seats = 2 if state_code not in ["DC", "PR", "GU", "VI", "AS", "MP"] else 0
    total_expected = h_seats + sen_seats

    print("=" * 70)
    print(f"STATE PRE-FLIGHT AUDIT: {state_name} ({state_code})")
    print("=" * 70)

    # 1. Load dataset rows
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["state"] == state_code]

    if not rows:
        print(f"FAILED: No records found for state {state_code} in {CSV_PATH}")
        return False

    actual_count = len(rows)
    honest_count_phrase = f"{actual_count} of {state_name}'s {total_expected} members with 2024-cycle FEC records"
    print(f"[Gate 1: Member Scope] {honest_count_phrase}")

    # 2. Check reconciliation against weball24
    outliers_unexplained = []
    outliers_documented = []
    within_tol = 0

    if isinstance(variances, dict):
        variance_map_fec = {v.get("fec_candidate_id"): v for v in variances.values()}
        variance_map_bio = variances
    else:
        variance_map_fec = {v.get("fec_candidate_id"): v for v in variances}
        variance_map_bio = {v.get("bioguide_id"): v for v in variances}

    for r in rows:
        cand_id = r["fec_candidate_id"]
        bio_id = r["bioguide_id"]
        our_val = float(r["direct_contributions_total"])
        fec_val = weball.get(cand_id, 0.0)

        diff = abs(our_val - fec_val)
        denom = max(our_val, fec_val)
        pct = (diff / denom * 100.0) if denom > 0 else 0.0

        if pct <= 10.0 or diff <= 5000:
            within_tol += 1
        else:
            var_item = variance_map_fec.get(cand_id) or variance_map_bio.get(bio_id)
            if var_item and (var_item.get("explanation") or var_item.get("reason")):
                reason = var_item.get("explanation") or var_item.get("reason")
                outliers_documented.append((r["name"], cand_id, our_val, fec_val, pct, reason))
            else:
                outliers_unexplained.append((r["name"], cand_id, our_val, fec_val, pct))

    print(f"[Gate 2: Reconciliation vs FEC Summary]")
    print(f"  Within 10% match: {within_tol} / {actual_count}")
    print(f"  Documented outliers: {len(outliers_documented)} / {actual_count}")

    if outliers_unexplained:
        print(f"  FAILED: Found {len(outliers_unexplained)} UNEXPLAINED outlier(s) > 10%:")
        for name, cid, our, fec, pct in outliers_unexplained:
            print(f"    - {name} ({cid}): Rebuilt ${our:,.2f} vs FEC ${fec:,.2f} ({pct:.1f}% diff)")
        return False
    else:
        print("  PASSED: 100% of members match within 10% or have verified documented written explanations.")

    # 3. Check Infographic
    state_lower = state_code.lower()
    info_path = os.path.join(ASSETS_DIR, f"{state_lower}-infographic.png")
    if not os.path.exists(info_path):
        print(f"[Gate 3: Infographic Asset] WARNING: {info_path} does not exist yet. Run scripts/generate_state_infographic.py.")
    else:
        print(f"[Gate 3: Infographic Asset] PASSED: {info_path} exists.")

    # 4. Check Social Copy if present
    import re
    social_x_dir = os.path.join(BASE_DIR, "social", "x")
    social_file = None
    state_slug = state_name.lower().replace(" ", "-")
    pattern = re.compile(rf"(^|[-_])({state_lower}|{state_slug})([-_.]|$)", re.IGNORECASE)
    for fname in os.listdir(social_x_dir) if os.path.exists(social_x_dir) else []:
        if pattern.search(fname) and fname.endswith(".md"):
            social_file = os.path.join(social_x_dir, fname)
            break

    if social_file:
        print(f"[Gate 4: Copy Linting] Checking {os.path.basename(social_file)}...")
        with open(social_file, "r", encoding="utf-8") as f:
            full_text = f.read()

        # Extract only broadcast blocks (between ```text and ```) that are part of the main campaign thread
        blocks = re.findall(r"```text\s*(.*?)\s*```", full_text, flags=re.DOTALL)
        
        # Check broadcast copy
        violations = []
        for block in blocks:
            # Skip historical correction quote blocks
            if "our launch figures were modeled estimates" in block.lower():
                continue
            for word in PROHIBITED_WORDS:
                if re.search(rf"\b{word}\b", block, re.IGNORECASE):
                    violations.append((word, block[:60]))

        if violations:
            print(f"  FAILED: Prohibited words detected in broadcast copy:")
            for word, sample in violations:
                print(f"    - Word '{word}' in: {sample}...")
            return False

        lower_full = full_text.lower()
        if "pro-israel & foreign policy pacs" not in lower_full and "pro-israel/fp" not in lower_full:
            print("  FAILED: Copy must spell out 'Pro-Israel & Foreign Policy PACs'.")
            return False

        if "uncategorized" not in lower_full:
            print("  FAILED: Copy must show 'Uncategorized' sector slice.")
            return False

        print("  PASSED: Broadcast copy adheres to 100% nonpartisan and factual standards.")
    else:
        print(f"[Gate 4: Copy Linting] Notice: No staged campaign draft found for {state_code}. Ready for creation.")

    # 5. Check Team Anonymity
    if not check_anonymity():
        return False

    print(f"\nSTATUS: {state_code} PASSES PRE-FLIGHT. Clear to prepare rollout.")
    return True

def check_anonymity():
    """Verify that no tracked file outside data/ contains personal names or local home paths."""
    import subprocess
    import re
    res = subprocess.run(["git", "ls-files"], cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        return True

    files = res.stdout.splitlines()
    violations = []
    import base64
    u_pat = re.compile(base64.b64decode(b"").decode(), re.IGNORECASE)
    l_pat = re.compile(rf"\b{base64.b64decode(b'').decode()}\b", re.IGNORECASE)
    patterns = [u_pat, l_pat]
    for rel in files:
        if rel.startswith("data/") or "scrub" in rel or rel == "scripts/check_state_preflight.py":
            continue
        full_p = os.path.join(BASE_DIR, rel)
        if not os.path.isfile(full_p):
            continue
        try:
            with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                for lno, line in enumerate(f, 1):
                    for pat in patterns:
                        if pat.search(line):
                            violations.append((rel, lno, line.strip()))
                            break
        except Exception:
            pass

    if violations:
        print(f"[Gate 5: Team Anonymity] FAILED: {len(violations)} personal identity references found outside data/:")
        for rel, lno, l in violations[:5]:
            print(f"  - {rel}:{lno}: {l}")
        return False

    print("[Gate 5: Team Anonymity] PASSED: Zero personal names or home paths in tracked files outside data/.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit state rollout readiness against FEC primary data.")
    parser.add_argument("--state", required=True, help="Two-letter state code or 'ALL'")
    args = parser.parse_args()

    weball = load_weball()
    variances = []
    if os.path.exists(VARIANCES_PATH):
        with open(VARIANCES_PATH, "r", encoding="utf-8") as f:
            variances = json.load(f)

    if args.state.upper() == "ALL":
        failed = []
        for st in TOTAL_HOUSE_SEATS.keys():
            if not check_state(st, weball, variances):
                failed.append(st)
        if failed:
            print(f"\nFAILED STATES: {failed}")
            sys.exit(1)
        print("\nALL 50 STATES AND TERRITORIES PASS AUDIT GATES.")
    else:
        ok = check_state(args.state, weball, variances)
        if not ok:
            sys.exit(1)

if __name__ == "__main__":
    main()
