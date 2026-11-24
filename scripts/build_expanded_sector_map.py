#!/usr/bin/env python3
"""
scripts/build_expanded_sector_map.py

Generates an expanded, fully auditable sector_map.csv mapping PACs
to the 7 official sectors based on FEC Committee Master (cm.txt)
connected organizations and verified industry classifications.
"""

import os
import csv
import re
from collections import Counter
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CM_TXT = os.path.join(DATA_DIR, "fec_raw", "extracted", "cm.txt")
PAS2_TXT = os.path.join(DATA_DIR, "fec_raw", "extracted", "itpas2.txt")
ROSTER_JSON = os.path.join(DATA_DIR, "fec_raw", "legislators-current.json")
OUTPUT_CSV = os.path.join(DATA_DIR, "sector_map.csv")

# 1. Load sitting member candidate IDs
with open(ROSTER_JSON, "r", encoding="utf-8") as f:
    roster = json.load(f)

fec_cands = set()
for m in roster:
    for fid in m.get("fec", []):
        fec_cands.add(fid.strip().upper())

# 2. Load cm.txt
cmtes = {}
with open(CM_TXT, "r", encoding="latin1") as f:
    for line in f:
        p = line.strip().split("|")
        if len(p) >= 14:
            cmtes[p[0].strip().upper()] = {
                "name": p[1].strip(),
                "dsgn": p[8].strip(),
                "type": p[9].strip(),
                "org_tp": p[12].strip(),
                "connected_org": p[13].strip()
            }

# 3. Sum dollars per committee in pas2
CONDUITS = {"C00694323", "C00401224"}
cmte_dollars = Counter()

with open(PAS2_TXT, "r", encoding="latin1") as f:
    for line in f:
        p = line.strip().split("|")
        if len(p) > 18:
            cid = p[16].strip().upper()
            if cid in fec_cands and p[5] in ("24K", "24Z"):
                memo = p[19].strip() if len(p) > 19 else ""
                if memo == "X":
                    continue
                cmte_id = p[0].strip().upper()
                if cmte_id in CONDUITS:
                    continue
                amt = float(p[14]) if p[14] else 0.0
                cmte_dollars[cmte_id] += amt

# Seed with verified manual PACs
EXISTING_SECTOR_MAP = os.path.join(DATA_DIR, "sector_map.csv")
manual_map = {}
if os.path.exists(EXISTING_SECTOR_MAP):
    with open(EXISTING_SECTOR_MAP, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            manual_map[r["cmte_id"].strip().upper()] = {
                "cmte_id": r["cmte_id"].strip().upper(),
                "cmte_name": r["cmte_name"].strip(),
                "sector": r["sector"].strip(),
                "basis": r["basis"].strip()
            }

# Regex patterns for classification
SECTOR_RULES = [
    # Pro-Israel and Foreign Policy PACs
    ("Pro-Israel and Foreign Policy PACs", [
        r"\bAIPAC\b", r"\bAMERICAN ISRAEL PUBLIC AFFAIRS\b", r"\bDEMOCRATIC MAJORITY FOR ISRAEL\b",
        r"\bDMFI\b", r"\bREPUBLICAN JEWISH COALITION\b", r"\bRJC\b", r"\bJ STREET\b",
        r"\bUNITED DEMOCRACY PROJECT\b", r"\bPRO-ISRAEL\b", r"\bNORPAC\b", r"\bTO SUNPAC\b",
        r"\bCITYPAC\b", r"\bFLORIDIANS FOR A STRONG MIDDLE EAST\b", r"\bMARYLAND ASSOCIATION FOR CONCERNED CITIZENS\b",
        r"\bFOREIGN POLICY\b", r"\bISRAEL\b"
    ]),
    # Labor Unions
    ("Labor Unions", [
        r"\bUNION\b", r"\bBROTHERHOOD\b", r"\bLABORERS\b", r"\bMACHINISTS\b", r"\bAFL-CIO\b",
        r"\bTEAMSTERS\b", r"\bWORKERS\b", r"\bSEIU\b", r"\bAFSCME\b", r"\bFLIGHT ATTENDANTS\b",
        r"\bAIR LINE PILOTS\b", r"\bFIRE FIGHTERS\b", r"\bPOSTAL WORKERS\b", r"\bLETTER CARRIERS\b",
        r"\bBOILERMAKERS\b", r"\bBRICKLAYERS\b", r"\bPLUMBERS\b", r"\bPIPEFITTERS\b", r"\bIRONWORKERS\b",
        r"\bELECTRICAL WORKERS\b", r"\bSTEELWORKERS\b", r"\bCOMMUNICATIONS WORKERS\b", r"\bMINE WORKERS\b",
        r"\bAUTO WORKERS\b", r"\bUAW\b", r"\bTEACHERS\b", r"\bEDUCATION ASSOCIATION\b",
        r"\bAMALGAMATED TRANSIT\b", r"\bPOLICE\b", r"\bLAW ENFORCEMENT\b", r"\bAIR TRAFFIC CONTROLLERS\b",
        r"\bOPERATING ENGINEERS\b", r"\bSHEET METAL\b", r"\bCARPENTERS\b", r"\bLONGSHOREMEN\b",
        r"\bFOOD AND COMMERCIAL WORKERS\b", r"\bUFCW\b", r"\bBAKERY, CONFECTIONERY\b"
    ]),
    # Defense & Aerospace
    ("Defense & Aerospace", [
        r"\bLOCKHEED\b", r"\bBOEING\b", r"\bRAYTHEON\b", r"\bRTX\b", r"\bNORTHROP\b",
        r"\bGENERAL DYNAMICS\b", r"\bL3HARRIS\b", r"\bBAE SYSTEMS\b", r"\bHUNTINGTON INGALLS\b",
        r"\bLEIDOS\b", r"\bTEXTRON\b", r"\bHONEYWELL\b", r"\bDEFENSE\b", r"\bAEROSPACE\b",
        r"\bSPACE EXPLORATION\b", r"\bSPACEX\b", r"\bGENERAL ATOMICS\b", r"\bSAIC\b",
        r"\bBOOZ ALLEN\b", r"\bCACI\b", r"\bAMPHENOL\b", r"\bPARKER-HANNIFIN\b", r"\bAEROJET\b",
        r"\bCURTISS-WRIGHT\b", r"\bTELEDYNE\b", r"\bELBIT\b", r"\bHEICO\b", r"\bBWX TECHNOLOGIES\b"
    ]),
    # Big Pharma & Health
    ("Big Pharma & Health", [
        r"\bPHARMACEUTICAL\b", r"\bPHARMA\b", r"\bBIOTECH\b", r"\bPFIZER\b", r"\bMODERNA\b",
        r"\bJOHNSON & JOHNSON\b", r"\bMERCK\b", r"\bELI LILLY\b", r"\bLILLY\b", r"\bBRISTOL MYERS\b",
        r"\bABBVIE\b", r"\bAMGEN\b", r"\bGILEAD\b", r"\bREGENERON\b", r"\bASTRAZENECA\b",
        r"\bNOVARTIS\b", r"\bSANOFI\b", r"\bGLAXOSMITHKLINE\b", r"\bGSK\b", r"\bHOSPITAL\b",
        r"\bHEALTHCARE\b", r"\bHEALTH CARE\b", r"\bHEALTH\b", r"\bMEDICAL\b", r"\bPHYSICIANS\b",
        r"\bDOCTORS\b", r"\bSURGEONS\b", r"\bNURSES\b", r"\bELEVANCE\b", r"\bUNITEDHEALTH\b",
        r"\bCIGNA\b", r"\bHUMANA\b", r"\bCENTENE\b", r"\bCVS HEALTH\b", r"\bWALGREENS\b",
        r"\bABBOTT\b", r"\bMEDTRONIC\b", r"\bBOSTON SCIENTIFIC\b", r"\bSTRYKER\b",
        r"\bAMERICAN HOSPITAL ASSOCIATION\b", r"\bAMERICAN MEDICAL ASSOCIATION\b", r"\bBLUE CROSS\b",
        r"\bBLUE SHIELD\b", r"\bHEALTHCARE DISTRIBUTION\b", r"\bBIOTECHNOLOGY INNOVATION\b",
        r"\bPHRMA\b", r"\bDERMATOLOGY\b", r"\bANESTHESIOLOGISTS\b", r"\bOPTOMETRIC\b",
        r"\bDENTAL\b", r"\bRADIOLOGY\b", r"\bPSYCHIATRIC\b", r"\bOPHTHALMOLOGY\b",
        r"\bORTHOPAEDIC\b", r"\bCARDIOVASCULAR\b", r"\bKIDNEY CARE\b", r"\bDIALYSIS\b",
        r"\bDAVITA\b", r"\bFRESENIUS\b", r"\bCARDINAL HEALTH\b", r"\bMCKESSON\b", r"\bAMERISOURCEBERGEN\b",
        r"\bCENCORA\b"
    ]),
    # Wall St & Finance
    ("Wall St & Finance", [
        r"\bBANK\b", r"\bBANKERS\b", r"\bFINANCIAL\b", r"\bFINANCE\b", r"\bCREDIT UNION\b",
        r"\bINVESTMENT\b", r"\bSECURITIES\b", r"\bCAPITAL\b", r"\bINSURANCE\b", r"\bINSURERS\b",
        r"\bGOLDMAN SACHS\b", r"\bMORGAN STANLEY\b", r"\bJPMORGAN\b", r"\bCITIGROUP\b",
        r"\bWELLS FARGO\b", r"\bBANK OF AMERICA\b", r"\bBLACKROCK\b", r"\bBLACKSTONE\b",
        r"\bFIDELITY\b", r"\bSCHWAB\b", r"\bPRUDENTIAL\b", r"\bMETLIFE\b", r"\bNEW YORK LIFE\b",
        r"\bMASSMUTUAL\b", r"\bNORTHWESTERN MUTUAL\b", r"\bTRAVELERS\b", r"\bALLSTATE\b",
        r"\bSTATE FARM\b", r"\bAFLAC\b", r"\bVISA\b", r"\bMASTERCARD\b", r"\bAMERICAN EXPRESS\b",
        r"\bDISCOVER FINANCIAL\b", r"\bCAPITAL ONE\b", r"\bINTERCONTINENTAL EXCHANGE\b",
        r"\bCME GROUP\b", r"\bNASDAQ\b", r"\bCBOE\b", r"\bREALTORS\b", r"\bREAL ESTATE\b",
        r"\bMORTGAGE\b", r"\bHOUSING COUNCIL\b", r"\bHOME BUILDERS\b", r"\bACCOUNTANTS\b",
        r"\bAICPA\b", r"\bMANAGED FUNDS\b", r"\bINVESTMENT COMPANY INSTITUTE\b",
        r"\bSECURITIES INDUSTRY\b", r"\bSIFMA\b", r"\bDELOITTE\b", r"\bERNST & YOUNG\b",
        r"\bPRICEWATERHOUSECOOPERS\b", r"\bPWC\b", r"\bKPMG\b", r"\bFARM CREDIT\b",
        r"\bFINANCIAL SERVICES\b", r"\bMUTUAL INSURANCE\b", r"\bTITLE INSURANCE\b"
    ]),
    # Fossil Fuels & Energy
    ("Fossil Fuels & Energy", [
        r"\bENERGY\b", r"\bOIL\b", r"\bGAS\b", r"\bPETROLEUM\b", r"\bEXXON\b", r"\bCHEVRON\b",
        r"\bCONOCOPHILLIPS\b", r"\bPHILLIPS 66\b", r"\bOCCIDENTAL\b", r"\bVALERO\b", r"\bMARATHON\b",
        r"\bKINDER MORGAN\b", r"\bWILLIAMS COMPANIES\b", r"\bENTERPRISE PRODUCTS\b", r"\bENERGY TRANSFER\b",
        r"\bELECTRIC\b", r"\bUTILITIES\b", r"\bUTILITY\b", r"\bSOUTHERN COMPANY\b", r"\bDUKE ENERGY\b",
        r"\bNEXTERA\b", r"\bDOMINION\b", r"\bEXELON\b", r"\bENTERGY\b", r"\bAMERICAN ELECTRIC POWER\b",
        r"\bEDISON\b", r"\bPUBLIC SERVICE ENTERPRISE\b", r"\bCOAL\b", r"\bMINING\b",
        r"\bAMERICAN PETROLEUM INSTITUTE\b", r"\bINTERSTATE NATURAL GAS\b", r"\bAMERICAN GAS ASSOCIATION\b",
        r"\bNUCLEAR ENERGY INSTITUTE\b", r"\bCLEARPATH\b", r"\bSOLAR ENERGY\b", r"\bCLEAN ENERGY\b",
        r"\bELECTRIC COOPERATIVE\b", r"\bNATIONAL RURAL ELECTRIC\b", r"\bPG&E\b", r"\bSEMPRA\b",
        r"\bTC ENERGY\b", r"\bENBRIDGE\b", r"\bHALLIBURTON\b", r"\bSCHLUMBERGER\b", r"\bSLB\b",
        r"\bBAKER HUGHES\b", r"\bDEVON ENERGY\b", r"\bEOG RESOURCES\b", r"\bCHESAPEAKE ENERGY\b",
        r"\bEQT CORPORATION\b", r"\bDIAMONDBACK\b", r"\bTARGA RESOURCES\b"
    ]),
    # Big Tech & Telecom
    ("Big Tech & Telecom", [
        r"\bTECH\b", r"\bTECHNOLOGY\b", r"\bTELECOM\b", r"\bTELECOMMUNICATIONS\b", r"\bSOFTWARE\b",
        r"\bCOMPUTER\b", r"\bINTERNET\b", r"\bGOOGLE\b", r"\bALPHABET\b", r"\bMICROSOFT\b",
        r"\bAMAZON\b", r"\bAPPLE\b", r"\bMETA\b", r"\bFACEBOOK\b", r"\bORACLE\b", r"\bINTEL\b",
        r"\bCISCO\b", r"\bQUALCOMM\b", r"\bNVIDIA\b", r"\bBROADCOM\b", r"\bIBM\b", r"\bDELL\b",
        r"\bHP\b", r"\bSALESFORCE\b", r"\bADOBE\b", r"\bNETFLIX\b", r"\bUBER\b", r"\bLYFT\b",
        r"\bDOORDASH\b", r"\bAIRBNB\b", r"\bAT&T\b", r"\bVERIZON\b", r"\bT-MOBILE\b", r"\bCOMCAST\b",
        r"\bCHARTER COMMUNICATIONS\b", r"\bNCTA\b", r"\bCTIA\b", r"\bINFORMATION TECHNOLOGY INDUSTRY\b",
        r"\bSEMICONDUCTOR\b", r"\bINTERNET ASSOCIATION\b", r"\bCOX ENTERPRISES\b", r"\bMOTOROLA\b",
        r"\bMICRON\b", r"\bAPPLIED MATERIALS\b", r"\bLAM RESEARCH\b", r"\bTEXAS INSTRUMENTS\b",
        r"\bINTUIT\b", r"\bSERVICENOW\b", r"\bSYNOPSYS\b", r"\bCADENCE\b", r"\bPALANTIR\b"
    ])
]

combined_map = dict(manual_map)

# Classify top 1,000 PACs by volume
top_pacs = cmte_dollars.most_common(1000)

for cid, amt in top_pacs:
    if cid in combined_map:
        continue
    
    ci = cmtes.get(cid, {})
    name = ci.get("name", "")
    conn = ci.get("connected_org", "")
    org_tp = ci.get("org_tp", "")
    
    # Auto-classify labor by organization type
    if org_tp == "L":
        combined_map[cid] = {
            "cmte_id": cid,
            "cmte_name": name,
            "sector": "Labor Unions",
            "basis": conn if conn else "Labor organization charter"
        }
        continue
        
    search_text = f"{name} {conn}".upper()
    matched_sector = None
    
    for sector_name, patterns in SECTOR_RULES:
        for pat in patterns:
            if re.search(pat, search_text, re.IGNORECASE):
                matched_sector = sector_name
                break
        if matched_sector:
            break
            
    if matched_sector:
        combined_map[cid] = {
            "cmte_id": cid,
            "cmte_name": name,
            "sector": matched_sector,
            "basis": conn if conn else name
        }

# Write out sector_map.csv sorted by sector and committee name
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["cmte_id", "cmte_name", "sector", "basis"])
    writer.writeheader()
    for cid in sorted(combined_map.keys(), key=lambda x: (combined_map[x]["sector"], combined_map[x]["cmte_name"])):
        writer.writerow(combined_map[cid])

print(f"Successfully generated {OUTPUT_CSV} with {len(combined_map)} mapped PACs.")

# Check metrics
total_direct = sum(cmte_dollars.values())
mapped_dollars = sum(cmte_dollars[cid] for cid in combined_map)
uncat_dollars = total_direct - mapped_dollars

print(f"Total direct PAC dollars to sitting members: ${total_direct:,.2f}")
print(f"Covered PAC dollars in 7 sectors:         ${mapped_dollars:,.2f} ({mapped_dollars/total_direct*100:.1f}%)")
print(f"Uncategorized PAC dollars:                 ${uncat_dollars:,.2f} ({uncat_dollars/total_direct*100:.1f}%)")
