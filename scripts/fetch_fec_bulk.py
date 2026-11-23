#!/usr/bin/env python3
"""
scripts/fetch_fec_bulk.py

Downloads official Federal Election Commission (FEC) bulk data files and
current Congressional roster per docs/OPENFEC_REBUILD_SPEC.md.

Records download timestamps, source URLs, and SHA-256 checksums in data/SOURCES.json.
"""

import os
import sys
import json
import hashlib
import urllib.request
import zipfile
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "fec_raw")
CYCLE = "2024"

# Official FEC Bulk Data Endpoints (Cycle 2024: 2023-2024 general election cycle)
FEC_FILES = {
    "pas2": {
        "url": f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/pas2{CYCLE[-2:]}.zip",
        "description": "Contributions from committees to candidates and independent expenditures (itemized)",
        "expected_txt": "itpas2.txt"
    },
    "cm": {
        "url": f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/cm{CYCLE[-2:]}.zip",
        "description": "Committee Master: ID, Name, Type, Designation, Connected Org",
        "expected_txt": "cm.txt"
    },
    "cn": {
        "url": f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/cn{CYCLE[-2:]}.zip",
        "description": "Candidate Master: Candidate ID, Name, Party, Office, State, District",
        "expected_txt": "cn.txt"
    },
    "ccl": {
        "url": f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/ccl{CYCLE[-2:]}.zip",
        "description": "Candidate-Committee Linkage",
        "expected_txt": "ccl.txt"
    },
    "weball": {
        "url": f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/weball{CYCLE[-2:]}.zip",
        "description": "All Candidates Summary: total contributions from other political committees",
        "expected_txt": f"weball{CYCLE[-2:]}.txt"
    }
}

ROSTER_YAML_URL = "https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-current.yaml"

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def download_file(url, dest_path):
    print(f"Fetching: {url}")
    headers = {"User-Agent": "DonorClassCivicIntelligence/2.0 (contact@donorclass.info)"}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as response, open(dest_path, "wb") as out_file:
        total_size = int(response.info().get("Content-Length", 0))
        downloaded = 0
        block_size = 65536
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            downloaded += len(buffer)
            out_file.write(buffer)
            if total_size > 0:
                percent = downloaded * 100 / total_size
                sys.stdout.write(f"\r  Downloaded {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB ({percent:.1f}%)")
                sys.stdout.flush()
    print()

def parse_legislators_yaml_light(yaml_path):
    """
    Lightweight zero-dependency parser for congress-legislators yaml format.
    Extracts bioguide, fec IDs, official name, state, district, chamber, party.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    legislators = []
    current = None
    in_fec = False
    in_terms = False
    current_term = None

    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if line.startswith("- id:"):
            if current:
                legislators.append(current)
            current = {
                "bioguide": "",
                "fec": [],
                "name": "",
                "party": "",
                "state": "",
                "district": None,
                "chamber": "",
                "terms": []
            }
            in_fec = False
            in_terms = False
            continue

        if not current:
            continue

        if stripped.startswith("bioguide:"):
            current["bioguide"] = stripped.split(":", 1)[1].strip()
        elif stripped == "fec:":
            in_fec = True
            in_terms = False
            continue
        elif in_fec:
            if stripped.startswith("- "):
                val = stripped[2:].strip().strip("'").strip('"')
                current["fec"].append(val)
                continue
            elif indent <= 4:
                in_fec = False

        if stripped.startswith("official_full:"):
            current["name"] = stripped.split(":", 1)[1].strip().strip("'").strip('"')
        elif stripped.startswith("last:") and not current["name"]:
            current["name"] = stripped.split(":", 1)[1].strip().strip("'").strip('"')

        if stripped == "terms:":
            in_terms = True
            in_fec = False
            continue
        elif in_terms:
            if stripped.startswith("- type:"):
                t_val = stripped.split(":", 1)[1].strip()
                current_term = {"type": t_val}
                current["terms"].append(current_term)
                continue
            elif current_term and stripped.startswith("state:"):
                current_term["state"] = stripped.split(":", 1)[1].strip()
            elif current_term and stripped.startswith("party:"):
                current_term["party"] = stripped.split(":", 1)[1].strip()
            elif current_term and stripped.startswith("district:"):
                try:
                    current_term["district"] = int(stripped.split(":", 1)[1].strip())
                except ValueError:
                    current_term["district"] = None

    if current:
        legislators.append(current)

    # Populate top-level fields from most recent term
    for leg in legislators:
        if leg["terms"]:
            latest = leg["terms"][-1]
            leg["chamber"] = "Senate" if latest.get("type") == "sen" else "House"
            leg["state"] = latest.get("state", "")
            leg["party"] = latest.get("party", "")
            leg["district"] = latest.get("district", None)

    return legislators

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    extract_dir = os.path.join(RAW_DIR, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    sources = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "cycle": CYCLE,
        "files": {}
    }

    # 1. Download FEC Bulk ZIPs and extract (skip download if already extracted)
    for key, meta in FEC_FILES.items():
        zip_filename = f"{key}{CYCLE[-2:]}.zip"
        zip_path = os.path.join(RAW_DIR, zip_filename)
        extracted_txt = os.path.join(extract_dir, meta["expected_txt"])

        if not os.path.exists(extracted_txt):
            download_file(meta["url"], zip_path)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

        zip_hash = sha256_file(zip_path) if os.path.exists(zip_path) else None
        zip_size = os.path.getsize(zip_path) if os.path.exists(zip_path) else 0
        txt_hash = sha256_file(extracted_txt) if os.path.exists(extracted_txt) else None

        sources["files"][key] = {
            "url": meta["url"],
            "description": meta["description"],
            "zip_filename": zip_filename,
            "zip_size_bytes": zip_size,
            "zip_sha256": zip_hash,
            "extracted_file": meta["expected_txt"],
            "extracted_sha256": txt_hash
        }
        print(f"  [OK] Verified {meta['expected_txt']} (SHA256: {txt_hash[:12]}...)")

    # 2. Download Congress Legislators YAML Roster & convert to JSON
    roster_yaml_path = os.path.join(RAW_DIR, "legislators-current.yaml")
    if not os.path.exists(roster_yaml_path):
        download_file(ROSTER_YAML_URL, roster_yaml_path)
    
    yaml_hash = sha256_file(roster_yaml_path)
    legislators = parse_legislators_yaml_light(roster_yaml_path)
    
    roster_json_path = os.path.join(RAW_DIR, "legislators-current.json")
    with open(roster_json_path, "w", encoding="utf-8") as f:
        json.dump(legislators, f, indent=2)

    sources["roster"] = {
        "url": ROSTER_YAML_URL,
        "description": "unitedstates/congress-legislators sitting members roster with FEC candidate IDs",
        "member_count": len(legislators),
        "yaml_sha256": yaml_hash,
        "json_file": "legislators-current.json"
    }
    print(f"  [OK] Current members roster: {len(legislators)} sitting members loaded and saved to {roster_json_path}")

    # 3. Save SOURCES.json
    sources_file = os.path.join(DATA_DIR, "SOURCES.json")
    with open(sources_file, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2)
    print(f"\n[DONE] Manifest saved to {sources_file}")

if __name__ == "__main__":
    main()
