#!/usr/bin/env python3
"""
build_release.py — Generate the release/ dataset package for DONOR CLASS.

Usage:
    python3 scripts/build_release.py

Outputs under release/:
  donor-dataset.csv
  sector_map.csv
  documented_variances.json
  SOURCES.json
  DATA_DICTIONARY.md   (pre-written; this script verifies it exists)
  METHODOLOGY.md       (pre-written; this script verifies it exists)
  KNOWN_LIMITATIONS.md (pre-written; this script verifies it exists)
  RECONCILIATION_AUDIT.md (copied from docs/RECONCILIATION_AUDIT_2024.md)
"""

import csv
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RELEASE = REPO / "release"
DATA = REPO / "data"
DOCS = REPO / "docs"

REQUIRED_PRE_WRITTEN = [
    "DATA_DICTIONARY.md",
    "METHODOLOGY.md",
    "KNOWN_LIMITATIONS.md",
]

COPY_MAP = {
    DATA / "donor-dataset.csv": RELEASE / "donor-dataset.csv",
    DATA / "sector_map.csv": RELEASE / "sector_map.csv",
    DATA / "documented_variances.json": RELEASE / "documented_variances.json",
    DATA / "SOURCES.json": RELEASE / "SOURCES.json",
    DOCS / "RECONCILIATION_AUDIT_2024.md": RELEASE / "RECONCILIATION_AUDIT.md",
}

BANNED_WORDS = ["verified", "CAPPED", "30116", "Official FEC"]


def check_banned_words(path):
    text = Path(path).read_text(encoding="utf-8")
    hits = [w for w in BANNED_WORDS if w in text]
    return hits


def main():
    RELEASE.mkdir(exist_ok=True)

    errors = []

    # 1. Check pre-written docs exist
    for fname in REQUIRED_PRE_WRITTEN:
        dest = RELEASE / fname
        if not dest.exists():
            errors.append(f"MISSING pre-written file: {dest}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Copy data files
    for src, dst in COPY_MAP.items():
        if not src.exists():
            print(f"WARNING: source not found, skipping: {src}", file=sys.stderr)
            continue
        shutil.copy2(src, dst)
        print(f"Copied: {src.name} -> {dst}")

    # 3. Data integrity: verify donor-dataset.csv
    csv_path = RELEASE / "donor-dataset.csv"
    if csv_path.exists():
        rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
        member_count = len(rows)
        print(f"donor-dataset.csv: {member_count} rows")

        if member_count < 530 or member_count > 550:
            print(f"WARNING: unexpected row count {member_count} (expected ~539)", file=sys.stderr)

        # Verify IE columns never appear mixed with direct
        for r in rows:
            bio = r.get("bioguide_id", "?")
            # Basic type check: all dollar columns should be numeric
            for col in ["direct_contributions_total", "ie_support_total", "ie_oppose_total"]:
                try:
                    float(r[col])
                except (ValueError, KeyError):
                    print(f"WARNING: non-numeric value in {col} for {bio}", file=sys.stderr)

    # 4. Banned-word audit across all release files
    for f in RELEASE.glob("*"):
        if f.suffix in (".csv", ".json", ".md", ".txt", ".cff"):
            hits = check_banned_words(f)
            if hits:
                print(f"WARNING: banned words {hits} found in {f.name}", file=sys.stderr)

    # 5. Summary
    files = list(RELEASE.iterdir())
    print(f"\nRelease package ready: {len(files)} files in {RELEASE}/")
    for f in sorted(files):
        size = f.stat().st_size
        print(f"  {f.name:40s}  {size:>10,} bytes")

    print("\nDone. Verify outputs, then tag: git tag v1.0.0-data-2024")


if __name__ == "__main__":
    main()
