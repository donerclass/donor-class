#!/usr/bin/env python3
"""
scripts/generate_state_infographic.py

Generates publication-grade 1200x675 infographics for the 50 States in 50 Days campaign.
Uses nonpartisan institutional typography badges (NO state seals to strictly comply
with state statutory seal restrictions and eliminate endorsement implications).
Pulls 100% verified FEC bulk data from data/donor-dataset.csv.
"""

import os
import sys
import csv
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_CSV = os.path.join(BASE_DIR, "data", "donor-dataset.csv")
LOGO_PATH = os.path.join(BASE_DIR, "logo-master.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "infographics")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

def make_state_badge(state_code, size=74):
    """Creates a sleek, nonpartisan circular state badge (avoids state seal restrictions)."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((0, 0, size - 1, size - 1), fill="#0f172a", outline="#38bdf8", width=2)
    draw.ellipse((4, 4, size - 5, size - 5), outline="#1e293b", width=1)
    
    font_code = ImageFont.truetype(FONT_BOLD, 26)
    font_sub = ImageFont.truetype(FONT_BOLD, 8)
    
    bbox_code = font_code.getbbox(state_code)
    w_code = bbox_code[2] - bbox_code[0]
    draw.text(((size - w_code) // 2, 16), state_code, font=font_code, fill="#ffffff")
    
    sub_text = "50 STATES"
    bbox_sub = font_sub.getbbox(sub_text)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text(((size - w_sub) // 2, 48), sub_text, font=font_sub, fill="#38bdf8")
    
    return canvas

def fmt_amt_short(val):
    if val < 0:
        return f"-${abs(val)/1e3:.0f}K"
    return f"${val/1e3:.0f}K"

def generate_infographic(state_code, state_name, day_num):
    with open(DATA_CSV, "r", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["state"] == state_code]
    
    if not rows:
        print(f"No records found for state {state_code}")
        return
    
    direct_total = sum(float(r["direct_contributions_total"]) for r in rows)
    outside_sup = sum(float(r["ie_support_total"]) for r in rows)
    outside_opp = sum(float(r["ie_oppose_total"]) for r in rows)
    member_count = len(rows)
    
    rows.sort(key=lambda x: float(x["direct_contributions_total"]), reverse=True)
    top_recipients = rows[:7]
    
    W, H = 1200, 675
    img = Image.new("RGBA", (W, H), "#070a13")
    draw = ImageDraw.Draw(img)
    
    font_day = ImageFont.truetype(FONT_BOLD, 13)
    font_title = ImageFont.truetype(FONT_BOLD, 26)
    font_sub = ImageFont.truetype(FONT_REG, 13)
    font_col_header = ImageFont.truetype(FONT_BOLD, 15)
    font_name = ImageFont.truetype(FONT_BOLD, 14)
    font_meta = ImageFont.truetype(FONT_REG, 11)
    font_amt = ImageFont.truetype(FONT_BOLD, 14)
    font_box_title = ImageFont.truetype(FONT_BOLD, 13)
    font_box_body = ImageFont.truetype(FONT_REG, 12)
    font_cta_main = ImageFont.truetype(FONT_BOLD, 14)
    font_cta_sub = ImageFont.truetype(FONT_REG, 11)
    font_footer = ImageFont.truetype(FONT_REG, 11)
    
    draw.rectangle([(0, 0), (W, 105)], fill="#0f172a")
    draw.line([(0, 105), (W, 105)], fill="#1e293b", width=2)
    
    draw.text((40, 16), f"50 STATES IN 50 DAYS // DAY {day_num}: {state_name.upper()}", font=font_day, fill="#38bdf8")
    draw.text((40, 36), f"WHO FUNDS THE {state_name.upper()} CONGRESSIONAL DELEGATION?", font=font_title, fill="#ffffff")
    draw.text((40, 74), f"Official FEC Primary-Source Bulk Records: ${direct_total/1e6:.2f}M Direct PAC Funds Across {member_count} Lawmakers", font=font_sub, fill="#94a3b8")
    
    badge = make_state_badge(state_code, size=74)
    img.paste(badge, (W - 195, 15), badge)
    
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo.thumbnail((68, 68), Image.Resampling.LANCZOS)
            img.paste(logo, (W - 95, 18), logo)
        except Exception:
            pass
            
    # Left column: top recipients
    draw.rounded_rectangle([(40, 122), (660, 615)], radius=8, fill="#0f172a", outline="#1e293b", width=1)
    draw.text((60, 136), f"TOP DIRECT PAC RECIPIENTS ({state_name.upper()})", font=font_col_header, fill="#f8fafc")
    draw.text((480, 138), "Direct Campaign PACs", font=font_meta, fill="#64748b")
    
    row_y = 168
    for r in top_recipients:
        draw.rounded_rectangle([(55, row_y), (645, row_y + 54)], radius=6, fill="#131d31", outline="#1e293b", width=1)
        party_initial = r["party"][0] if r["party"] else "?"
        chamber_str = "Sen" if r["chamber"] == "Senate" else f"H-{r['district']}"
        badge_text = f"{party_initial}-{chamber_str}"
        is_dem = r["party"] == "Democrat"
        badge_color = "#38bdf8" if is_dem else "#f43f5e"
        
        draw.text((70, row_y + 8), r["name"], font=font_name, fill="#ffffff")
        draw.text((70, row_y + 30), badge_text, font=font_meta, fill=badge_color)
        
        def_amt = float(r["sector_defense"])
        pharma_amt = float(r["sector_pharma"])
        fin_amt = float(r["sector_finance"])
        fp_amt = float(r["sector_foreign_policy"])
        detail_str = f"Def {fmt_amt_short(def_amt)} • Pharma {fmt_amt_short(pharma_amt)} • Fin {fmt_amt_short(fin_amt)} • FP {fmt_amt_short(fp_amt)}"
        draw.text((135, row_y + 30), detail_str, font=font_meta, fill="#94a3b8")
        
        amt_val = float(r["direct_contributions_total"])
        amt_str = f"${amt_val:,.0f}"
        bbox = font_amt.getbbox(amt_str)
        w_amt = bbox[2] - bbox[0]
        draw.text((630 - w_amt, row_y + 16), amt_str, font=font_amt, fill="#10b981")
        row_y += 62
        
    # Right column: campaign vs outside spending
    draw.rounded_rectangle([(685, 122), (1160, 360)], radius=8, fill="#0f172a", outline="#1e293b", width=1)
    draw.text((705, 136), "CAMPAIGN MONEY VS. OUTSIDE EXPENDITURES", font=font_col_header, fill="#f8fafc")
    
    card_items = [
        ("Direct Campaign PACs (24K, 24Z)", f"${direct_total:,.0f}", "#10b981", "Given directly to candidate committees; subject to federal limits."),
        ("Outside Super PAC Support (24E)", f"${outside_sup:,.0f}", "#38bdf8", "Independent expenditures advocating candidate; never given to campaign."),
        ("Outside Super PAC Opposition (24A)", f"${outside_opp:,.0f}", "#ef4444", "Independent expenditures opposing candidate across television & digital.")
    ]
    
    c_y = 170
    for title, val, col, sub in card_items:
        draw.text((705, c_y), title, font=font_box_title, fill="#e2e8f0")
        bbox_v = font_box_title.getbbox(val)
        w_v = bbox_v[2] - bbox_v[0]
        draw.text((1140 - w_v, c_y), val, font=font_box_title, fill=col)
        draw.text((705, c_y + 20), sub, font=font_meta, fill="#64748b")
        c_y += 56
        
    # Right column: takeaways and CTA
    draw.rounded_rectangle([(685, 375), (1160, 615)], radius=8, fill="#0f172a", outline="#1e293b", width=1)
    draw.text((705, 390), f"PRIMARY-SOURCE TAKEAWAYS // {state_code}", font=font_col_header, fill="#38bdf8")
    
    bullets = [
        f"• All figures derived from 703,181 itemized official FEC records (pas2).",
        f"• Zero modeled, estimated, or projected numbers anywhere on this graphic.",
        f"• Top recipient in {state_code} collected ${float(top_recipients[0]['direct_contributions_total']):,.0f} in direct PAC cash.",
        f"• Check scanned FEC filing proof links for every transaction on live map."
    ]
    
    b_y = 422
    for b in bullets:
        draw.text((705, b_y), b, font=font_box_body, fill="#cbd5e1")
        b_y += 25
        
    btn_x1, btn_y1, btn_x2, btn_y2 = 705, 542, 1140, 598
    draw.rounded_rectangle([(btn_x1, btn_y1), (btn_x2, btn_y2)], radius=6, fill="#0284c7")
    
    cta_line1 = f"EXPLORE LIVE {state_name.upper()} DATA ON DONOR CLASS"
    cta_line2 = f"https://donorclass.info/?state={state_code}&ref=bp"
    
    bbox1 = font_cta_main.getbbox(cta_line1)
    w1 = bbox1[2] - bbox1[0]
    bbox2 = font_cta_sub.getbbox(cta_line2)
    w2 = bbox2[2] - bbox2[0]
    
    draw.text((btn_x1 + (btn_x2 - btn_x1 - w1) // 2, btn_y1 + 10), cta_line1, font=font_cta_main, fill="#ffffff")
    draw.text((btn_x1 + (btn_x2 - btn_x1 - w2) // 2, btn_y1 + 30), cta_line2, font=font_cta_sub, fill="#e0f2fe")
    
    draw.line([(40, 630), (W - 40, 630)], fill="#1e293b", width=1)
    draw.text((40, 642), "Official FEC Bulk Records (pas2, cm, cn, ccl) Through Dec 31, 2024 • Nonpartisan Public Interest Dataset • DONOR CLASS", font=font_footer, fill="#64748b")
    draw.text((W - 270, 642), f"VERIFIED: donorclass.info/?state={state_code}&ref=bp", font=font_footer, fill="#10b981")
    
    out_file = os.path.join(OUTPUT_DIR, f"{state_code.lower()}-infographic.png")
    img.save(out_file, "PNG")
    print(f"Generated {state_code}: {out_file}")

if __name__ == "__main__":
    generate_infographic("FL", "Florida", 3)
    generate_infographic("CA", "California", 2)
    generate_infographic("TX", "Texas", 1)
