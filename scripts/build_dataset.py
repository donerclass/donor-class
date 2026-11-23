#!/usr/bin/env python3
"""
scripts/build_dataset.py

Rebuilds the DONOR CLASS Congressional dataset using 100% official Federal
Election Commission (FEC) bulk data per docs/OPENFEC_REBUILD_SPEC.md.

Hard rule: Zero generated, estimated, or randomized numbers.
Every dollar traces directly to official FEC transaction records.
"""

import os
import sys
import csv
import json
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_EXTRACTED = os.path.join(DATA_DIR, "fec_raw", "extracted")
ROSTER_JSON = os.path.join(DATA_DIR, "fec_raw", "legislators-current.json")
SECTOR_MAP_CSV = os.path.join(DATA_DIR, "sector_map.csv")
SOURCES_JSON = os.path.join(DATA_DIR, "SOURCES.json")

# Verified Sector Definitions per Section 4 of Spec
SECTORS = {
    "defense": {"name": "Defense & Aerospace", "color": "#0ea5e9"},
    "pharma": {"name": "Big Pharma & Health", "color": "#10b981"},
    "finance": {"name": "Wall St & Finance", "color": "#f59e0b"},
    "energy": {"name": "Fossil Fuels & Energy", "color": "#ef4444"},
    "tech": {"name": "Big Tech & Telecom", "color": "#8b5cf6"},
    "foreign_policy": {"name": "Pro-Israel and Foreign Policy PACs", "color": "#f43f5e"},
    "labor": {"name": "Labor Unions", "color": "#3b82f6"},
    "uncategorized": {"name": "Uncategorized Committees", "color": "#64748b"}
}

SECTOR_NAME_TO_KEY = {
    "Defense & Aerospace": "defense",
    "Big Pharma & Health": "pharma",
    "Wall St & Finance": "finance",
    "Fossil Fuels & Energy": "energy",
    "Big Tech & Telecom": "tech",
    "Pro-Israel and Foreign Policy PACs": "foreign_policy",
    "Labor Unions": "labor",
    "Uncategorized Committees": "uncategorized"
}

def load_sector_map():
    mapping = {}
    if os.path.exists(SECTOR_MAP_CSV):
        with open(SECTOR_MAP_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cmte_id = row["cmte_id"].strip().upper()
                sector_raw = row["sector"].strip()
                sector_key = SECTOR_NAME_TO_KEY.get(sector_raw, "uncategorized")
                mapping[cmte_id] = {
                    "sector_key": sector_key,
                    "sector_name": sector_raw,
                    "cmte_name": row["cmte_name"].strip(),
                    "basis": row.get("basis", "")
                }
    return mapping

def load_committee_master():
    cm_path = os.path.join(RAW_EXTRACTED, "cm.txt")
    committees = {}
    if not os.path.exists(cm_path):
        print(f"Warning: {cm_path} not found.")
        return committees

    print("Loading Committee Master (cm.txt)...")
    with open(cm_path, "r", encoding="latin1") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 6:
                cmte_id = parts[0].strip().upper()
                cmte_nm = parts[1].strip()
                cmte_tp = parts[2].strip()
                cmte_dsgn = parts[3].strip()
                connected_org = parts[5].strip() if len(parts) > 5 else ""
                committees[cmte_id] = {
                    "name": cmte_nm,
                    "type": cmte_tp,
                    "designation": cmte_dsgn,
                    "connected_org": connected_org
                }
    print(f"  Loaded {len(committees):,} committees from cm.txt")
    return committees

def load_sitting_members():
    if not os.path.exists(ROSTER_JSON):
        raise FileNotFoundError(f"Roster not found: {ROSTER_JSON}")

    with open(ROSTER_JSON, "r", encoding="utf-8") as f:
        roster = json.load(f)

    members = {}
    fec_to_bioguide = {}

    for leg in roster:
        bg = leg["bioguide"]
        name = leg["name"]
        state = leg["state"]
        district = leg["district"]
        chamber = leg["chamber"]
        party = leg["party"]
        fec_ids = [fid.strip().upper() for fid in leg.get("fec", [])]

        members[bg] = {
            "id": bg,
            "name": name,
            "displayName": name,
            "state": state,
            "district": district,
            "chamber": chamber,
            "party": party,
            "status": "Incumbent",
            "fec_ids": fec_ids,
            "fecCandidateId": fec_ids[0] if fec_ids else "",
            "direct_contributions_total": 0.0,
            "ie_support_total": 0.0,
            "ie_oppose_total": 0.0,
            "sector_totals": {k: 0.0 for k in SECTORS},
            "pacs": {},
            "transaction_count": 0,
            "latest_transaction_date": ""
        }

        for fid in fec_ids:
            fec_to_bioguide[fid] = bg

    print(f"Loaded {len(members)} sitting members across {len(fec_to_bioguide)} FEC candidate IDs")
    return members, fec_to_bioguide

def parse_date(dt_str):
    if len(dt_str) == 8 and dt_str.isdigit():
        return f"{dt_str[4:]}-{dt_str[:2]}-{dt_str[2:4]}"
    return dt_str

def main():
    print("=" * 70)
    print("DONOR CLASS: Rebuilding Dataset from Official FEC Bulk Records")
    print("=" * 70)

    sector_map = load_sector_map()
    cm_data = load_committee_master()
    members, fec_to_bioguide = load_sitting_members()

    pas2_path = os.path.join(RAW_EXTRACTED, "itpas2.txt")
    if not os.path.exists(pas2_path):
        raise FileNotFoundError(f"Missing {pas2_path}. Run scripts/fetch_fec_bulk.py first.")

    print(f"Scanning itemized transactions from {pas2_path}...")

    # Deduplication map on (CMTE_ID, TRAN_ID) keeping highest FILE_NUM
    # Structure: (cmte_id, tran_id) -> (file_num, row_data)
    dedup_map = {}
    total_raw_rows = 0
    candidate_matched_rows = 0
    memo_skipped = 0

    with open(pas2_path, "r", encoding="latin1") as f:
        for line in f:
            total_raw_rows += 1
            if total_raw_rows % 200000 == 0:
                sys.stdout.write(f"\r  Processed {total_raw_rows:,} raw rows...")
                sys.stdout.flush()

            parts = line.strip().split("|")
            if len(parts) < 18:
                continue

            cmte_id = parts[0].strip().upper()
            transaction_tp = parts[5].strip().upper()
            tran_amt_str = parts[14].strip()
            cand_id = parts[16].strip().upper()
            other_id = parts[15].strip().upper()
            tran_id = parts[17].strip()
            file_num_str = parts[18].strip() if len(parts) > 18 else "0"
            memo_cd = parts[19].strip().upper() if len(parts) > 19 else ""
            img_num = parts[4].strip()
            tran_dt = parts[13].strip()

            # Rule: Skip memo items (MEMO_CD == 'X') to prevent double counting parent conduits
            if memo_cd == "X":
                memo_skipped += 1
                continue

            # Check if transaction targets one of our 539 sitting members
            target_cand = cand_id if cand_id in fec_to_bioguide else (other_id if other_id in fec_to_bioguide else None)
            if not target_cand:
                continue

            try:
                amt = float(tran_amt_str)
            except ValueError:
                continue

            try:
                file_num = int(file_num_str) if file_num_str.isdigit() else 0
            except ValueError:
                file_num = 0

            candidate_matched_rows += 1
            dedup_key = (cmte_id, tran_id)

            if dedup_key in dedup_map:
                if file_num > dedup_map[dedup_key]["file_num"]:
                    dedup_map[dedup_key] = {
                        "file_num": file_num,
                        "cmte_id": cmte_id,
                        "cand_id": target_cand,
                        "transaction_tp": transaction_tp,
                        "amount": amt,
                        "image_num": img_num,
                        "date": tran_dt
                    }
            else:
                dedup_map[dedup_key] = {
                    "file_num": file_num,
                    "cmte_id": cmte_id,
                    "cand_id": target_cand,
                    "transaction_tp": transaction_tp,
                    "amount": amt,
                    "image_num": img_num,
                    "date": tran_dt
                }

    print(f"\nCompleted pass: {total_raw_rows:,} total rows scanned.")
    print(f"Matched {candidate_matched_rows:,} candidate rows. Retained {len(dedup_map):,} deduplicated transactions (skipped {memo_skipped:,} memo items).")

    # Aggregate deduplicated transactions into member records
    overall_latest_date = ""

    for item in dedup_map.values():
        cmte_id = item["cmte_id"]
        cand_fec = item["cand_id"]
        tp = item["transaction_tp"]
        amt = item["amount"]
        img_num = item["image_num"]
        raw_dt = item["date"]
        parsed_dt = parse_date(raw_dt)

        if parsed_dt > overall_latest_date:
            overall_latest_date = parsed_dt

        bg = fec_to_bioguide[cand_fec]
        m = members[bg]
        m["transaction_count"] += 1
        if parsed_dt > m["latest_transaction_date"]:
            m["latest_transaction_date"] = parsed_dt

        # Resolve PAC Sector
        if cmte_id in sector_map:
            sec_key = sector_map[cmte_id]["sector_key"]
            cmte_name = sector_map[cmte_id]["cmte_name"]
        elif cmte_id in cm_data:
            sec_key = "uncategorized"
            cmte_name = cm_data[cmte_id]["name"]
        else:
            sec_key = "uncategorized"
            cmte_name = cmte_id

        # Classify Transaction Types per Section 3
        # Direct PAC contributions: 24K (contribution), 24Z (in-kind)
        # Outside spending support: 24E
        # Outside spending oppose: 24A
        is_direct = tp in ("24K", "24Z")
        is_ie_sup = (tp == "24E")
        is_ie_opp = (tp == "24A")

        if is_direct:
            m["direct_contributions_total"] += amt
            m["sector_totals"][sec_key] += amt
        elif is_ie_sup:
            m["ie_support_total"] += amt
        elif is_ie_opp:
            m["ie_oppose_total"] += amt

        # Track committee-level aggregation for top_pacs
        if cmte_id not in m["pacs"]:
            m["pacs"][cmte_id] = {
                "cmte_id": cmte_id,
                "name": cmte_name,
                "sector": sec_key,
                "sector_name": SECTORS[sec_key]["name"],
                "direct_amount": 0.0,
                "ie_support_amount": 0.0,
                "ie_oppose_amount": 0.0,
                "sample_image_num": img_num,
                "proof_link": f"https://docquery.fec.gov/cgi-bin/fecimg/?{img_num}" if img_num else ""
            }

        p = m["pacs"][cmte_id]
        if is_direct:
            p["direct_amount"] += amt
        elif is_ie_sup:
            p["ie_support_amount"] += amt
        elif is_ie_opp:
            p["ie_oppose_amount"] += amt

    # Convert member pac dictionaries to sorted lists and round numbers
    for m in members.values():
        pac_list = list(m["pacs"].values())
        for p in pac_list:
            p["total_activity"] = round(p["direct_amount"] + p["ie_support_amount"] + p["ie_oppose_amount"], 2)
            p["direct_amount"] = round(p["direct_amount"], 2)
            p["ie_support_amount"] = round(p["ie_support_amount"], 2)
            p["ie_oppose_amount"] = round(p["ie_oppose_amount"], 2)

        pac_list.sort(key=lambda x: abs(x["total_activity"]), reverse=True)
        m["top_pacs"] = pac_list[:15]
        m["totalPacAmount"] = m["direct_contributions_total"]
        m["directPacAmount"] = m["direct_contributions_total"]
        m["outsideSpendingAmount"] = m["ie_support_total"]
        m["conduitAmount"] = 0.0

        # Build sectorTopPacs dictionary for frontend modal views
        m["sectorTopPacs"] = {k: [] for k in SECTORS}
        for p in pac_list:
            sec_k = p["sector"]
            if sec_k in m["sectorTopPacs"]:
                m["sectorTopPacs"][sec_k].append({
                    "name": p["name"],
                    "cmte_id": p["cmte_id"],
                    "amount": p["direct_amount"] if p["direct_amount"] > 0 else p["total_activity"],
                    "type": f"FEC ID: {p['cmte_id']}",
                    "note": f"Direct: ${p['direct_amount']:,.0f}" if p["direct_amount"] > 0 else f"Outside IE: ${p['ie_support_amount']:,.0f}",
                    "proof_link": p["proof_link"]
                })
        del m["pacs"]

        m["direct_contributions_total"] = round(m["direct_contributions_total"], 2)
        m["ie_support_total"] = round(m["ie_support_total"], 2)
        m["ie_oppose_total"] = round(m["ie_oppose_total"], 2)
        for k in m["sector_totals"]:
            m["sector_totals"][k] = round(m["sector_totals"][k], 2)

    # 5. Build Auditable CSV: data/donor-dataset.csv
    csv_out = os.path.join(DATA_DIR, "donor-dataset.csv")
    csv_headers = [
        "bioguide_id", "fec_candidate_id", "name", "state", "district", "chamber", "party",
        "direct_contributions_total", "ie_support_total", "ie_oppose_total",
        "sector_defense", "sector_pharma", "sector_finance", "sector_energy",
        "sector_tech", "sector_foreign_policy", "sector_labor", "sector_uncategorized",
        "transaction_count", "data_through"
    ]

    with open(csv_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for m in sorted(members.values(), key=lambda x: (x["state"], x["chamber"], str(x["district"]))):
            writer.writerow([
                m["id"],
                m["fecCandidateId"],
                m["name"],
                m["state"],
                m["district"] if m["district"] is not None else "",
                m["chamber"],
                m["party"],
                m["direct_contributions_total"],
                m["ie_support_total"],
                m["ie_oppose_total"],
                m["sector_totals"]["defense"],
                m["sector_totals"]["pharma"],
                m["sector_totals"]["finance"],
                m["sector_totals"]["energy"],
                m["sector_totals"]["tech"],
                m["sector_totals"]["foreign_policy"],
                m["sector_totals"]["labor"],
                m["sector_totals"]["uncategorized"],
                m["transaction_count"],
                m["latest_transaction_date"]
            ])

    print(f"[OK] Auditable CSV saved to {csv_out}")

    # 6. Build Client Bundle: data/donor-dataset.js
    # Read existing SVG map paths from current bundle if available
    old_bundle_path = os.path.join(DATA_DIR, "donor-dataset.js")
    svg_paths = {}
    if os.path.exists(old_bundle_path):
        try:
            with open(old_bundle_path, "r", encoding="utf-8") as f:
                content = f.read()
                prefix = "window.DONOR_BUNDLE = "
                idx = content.find(prefix)
                if idx != -1:
                    raw_json = content[idx + len(prefix):].rstrip(";\n ")
                    old_obj = json.loads(raw_json)
                    svg_paths = old_obj.get("states", {})
        except Exception as e:
            print(f"Note: Could not extract old SVG map paths: {e}")

    # Build State-level rollups
    state_rollups = {}
    for m in members.values():
        st = m["state"]
        if st not in state_rollups:
            state_rollups[st] = {
                "state": st,
                "candidateCount": 0,
                "direct_contributions_total": 0.0,
                "ie_support_total": 0.0,
                "ie_oppose_total": 0.0,
                "sectorTotals": {k: 0.0 for k in SECTORS},
                "svgPath": svg_paths.get(st, {}).get("svgPath", "")
            }

        s_obj = state_rollups[st]
        s_obj["candidateCount"] += 1
        s_obj["direct_contributions_total"] = round(s_obj["direct_contributions_total"] + m["direct_contributions_total"], 2)
        s_obj["ie_support_total"] = round(s_obj["ie_support_total"] + m["ie_support_total"], 2)
        s_obj["ie_oppose_total"] = round(s_obj["ie_oppose_total"] + m["ie_oppose_total"], 2)
        for k, v in m["sector_totals"].items():
            s_obj["sectorTotals"][k] = round(s_obj["sectorTotals"][k] + v, 2)

    # Wrap client bundle
    client_bundle = {
        "meta": {
            "cycle": "2024",
            "cycle_description": "2023-2024 Federal Election Commission General Election Cycle",
            "data_source": "Official FEC Bulk Data (itpas2.txt, cm.txt, cn.txt, ccl.txt)",
            "downloaded_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "data_through": overall_latest_date,
            "total_incumbents": len(members),
            "disclaimer": "Figures represent line-item disbursements filed with the Federal Election Commission. Outside spending is reported separately and is not added to direct campaign contributions."
        },
        "sectors": SECTORS,
        "states": state_rollups,
        "candidates": list(members.values())
    }

    js_out = os.path.join(DATA_DIR, "donor-dataset.js")
    with open(js_out, "w", encoding="utf-8") as f:
        f.write("// DONOR CLASS Official Dataset (Rebuilt from Primary Source FEC Filings)\n")
        f.write("// Generated per docs/OPENFEC_REBUILD_SPEC.md. Zero modeled or estimated numbers.\n")
        f.write("window.DONOR_BUNDLE = ")
        json.dump(client_bundle, f, indent=2)
        f.write(";\n")

    print(f"[OK] Client-side bundle saved to {js_out}")
    print(f"[DONE] Successfully processed all {len(members)} sitting members.")
    print(f"Data through date: {overall_latest_date}")

if __name__ == "__main__":
    main()
