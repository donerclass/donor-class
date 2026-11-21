import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
img = Image.new("RGBA", (W, H), "#0b0f19")
draw = ImageDraw.Draw(img)

font_path_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
font_path_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"

font_header = ImageFont.truetype(font_path_bold, 13)
font_title = ImageFont.truetype(font_path_bold, 28)
font_sub = ImageFont.truetype(font_path_reg, 14)
font_col_header = ImageFont.truetype(font_path_bold, 16)
font_col_sub = ImageFont.truetype(font_path_reg, 11)
font_section = ImageFont.truetype(font_path_bold, 13)
font_name = ImageFont.truetype(font_path_bold, 14)
font_meta = ImageFont.truetype(font_path_reg, 12)
font_amt = ImageFont.truetype(font_path_bold, 14)
font_pill = ImageFont.truetype(font_path_bold, 11)
font_box_title = ImageFont.truetype(font_path_bold, 13)
font_box_body = ImageFont.truetype(font_path_reg, 12)
font_footer = ImageFont.truetype(font_path_reg, 11)

# Header Area
draw.rectangle([(0, 0), (W, 105)], fill="#0f172a")
draw.line([(0, 105), (W, 105)], fill="#1e293b", width=2)

# California State Silhouette Drawing (Top Right, next to logo)
ca_poly_base = [
    (0, 0),      # NW corner
    (65, 0),     # NE corner
    (65, 80),    # Nevada angle point
    (110, 160),  # SE angle point
    (110, 190),  # SE corner
    (80, 190),   # San Diego / Tijuana border
    (55, 155),   # LA / Orange County coast
    (35, 125),   # Point Conception
    (20, 85),    # Big Sur coast
    (15, 65),    # SF Bay Area coast
    (5, 30),     # Mendocino / Humboldt coast
    (0, 0)
]

ca_offset_x = W - 185
ca_offset_y = 12
ca_scale = 0.42
ca_poly = [(ca_offset_x + x * ca_scale, ca_offset_y + y * ca_scale) for x, y in ca_poly_base]
draw.polygon(ca_poly, fill="#1e293b", outline="#38bdf8")

# Paste logo in top right if available
logo_path = "./logo-master.png"
if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((65, 65), Image.Resampling.LANCZOS)
        img.paste(logo, (W - 90, 20), logo)
    except Exception:
        pass

# Header text
draw.text((40, 18), "DONOR CLASS  |  50 STATES IN 50 DAYS", font=font_header, fill="#10b981")
draw.text((40, 36), "DAY 2: CALIFORNIA CONGRESSIONAL DELEGATION", font=font_title, fill="#ffffff")
draw.text((40, 74), "Tracking $25,571,776 across 54 Members | Bipartisan Capital & Sector Penetration | 2024-2026 FEC Disclosures", font=font_sub, fill="#94a3b8")

# ==============================================================================
# LEFT COLUMN: BIPARTISAN TOP RECIPIENTS (CAPITAL VOLUME)
# ==============================================================================
col1_x = 40
col1_w = 540

draw.text((col1_x, 120), "BIPARTISAN TOP RECIPIENTS", font=font_col_header, fill="#f8fafc")
draw.text((col1_x + 280, 123), "BAR LENGTH = CAPITAL VOLUME ($)", font=font_col_sub, fill="#38bdf8")
draw.line([(col1_x, 142), (col1_x + col1_w, 142)], fill="#334155", width=1)

# Group 1: Top Democrats
draw.text((col1_x, 150), "DEMOCRATIC DELEGATION LEADERS", font=font_section, fill="#60a5fa")

top_democrats = [
    ("1. Jimmy Gomez", "D-CA-34", "$2,587,656", 1.0),
    ("2. Pete Aguilar", "D-CA-33", "$1,697,465", 0.656),
    ("3. Mike Thompson", "D-CA-04", "$1,482,740", 0.573),
]

y_dem = 172
max_amt_val = 2587656
for name, dist, amt, scale in top_democrats:
    draw.rounded_rectangle([(col1_x, y_dem), (col1_x + 18, y_dem + 16)], radius=3, fill="#2563eb")
    draw.text((col1_x + 5, y_dem + 1), "D", font=font_meta, fill="#ffffff")
    draw.text((col1_x + 26, y_dem), name, font=font_name, fill="#f1f5f9")
    draw.text((col1_x + 210, y_dem + 2), dist, font=font_meta, fill="#94a3b8")
    draw.text((col1_x + 430, y_dem), amt, font=font_amt, fill="#38bdf8")
    
    bar_y = y_dem + 20
    draw.rounded_rectangle([(col1_x, bar_y), (col1_x + col1_w, bar_y + 5)], radius=2, fill="#1e293b")
    draw.rounded_rectangle([(col1_x, bar_y), (col1_x + int(col1_w * scale), bar_y + 5)], radius=2, fill="#3b82f6")
    y_dem += 38

# Group 2: Top Republicans
draw.text((col1_x, y_dem + 8), "REPUBLICAN DELEGATION LEADERS", font=font_section, fill="#f87171")

top_republicans = [
    ("1. Ken Calvert", "R-CA-41", "$1,331,406", 0.515),
    ("2. Young Kim", "R-CA-40", "$707,679", 0.274),
    ("3. David Valadao", "R-CA-22", "$503,665", 0.195),
]

y_rep = y_dem + 30
for name, dist, amt, scale in top_republicans:
    draw.rounded_rectangle([(col1_x, y_rep), (col1_x + 18, y_rep + 16)], radius=3, fill="#dc2626")
    draw.text((col1_x + 5, y_rep + 1), "R", font=font_meta, fill="#ffffff")
    draw.text((col1_x + 26, y_rep), name, font=font_name, fill="#f1f5f9")
    draw.text((col1_x + 210, y_rep + 2), dist, font=font_meta, fill="#94a3b8")
    draw.text((col1_x + 430, y_rep), amt, font=font_amt, fill="#f87171")
    
    bar_y = y_rep + 20
    draw.rounded_rectangle([(col1_x, bar_y), (col1_x + col1_w, bar_y + 5)], radius=2, fill="#1e293b")
    draw.rounded_rectangle([(col1_x, bar_y), (col1_x + int(col1_w * scale), bar_y + 5)], radius=2, fill="#ef4444")
    y_rep += 38

# ==============================================================================
# RIGHT COLUMN: ECONOMIC SECTOR VOLUME & PENETRATION
# ==============================================================================
col2_x = 620
col2_w = 540

draw.text((col2_x, 120), "SECTOR CAPITAL & PENETRATION", font=font_col_header, fill="#f8fafc")
draw.text((col2_x + 260, 123), "BAR = CAPITAL ($) | PILL = REACH (%)", font=font_col_sub, fill="#10b981")
draw.line([(col2_x, 142), (col2_x + col2_w, 142)], fill="#334155", width=1)

sectors = [
    ("Foreign Policy Advocacy", "$16,847,276", "52/54 (96%)", 1.0, "#ec4899"),
    ("Big Tech & Telecom", "$1,867,500", "49/54 (91%)", 0.111, "#3b82f6"),
    ("Labor Unions", "$1,673,000", "47/54 (87%)", 0.099, "#eab308"),
    ("Big Pharma & Health", "$1,597,500", "51/54 (94%)", 0.095, "#10b981"),
    ("Wall St & Big Finance", "$1,540,000", "51/54 (94%)", 0.091, "#8b5cf6"),
    ("Defense & Aerospace", "$1,425,000", "50/54 (93%)", 0.085, "#06b6d4"),
    ("Fossil Fuels & Energy", "$621,500", "52/54 (96%)", 0.037, "#f97316"),
]

y_sec = 154
for sec_name, sec_amt, sec_pill, bar_scale, sec_color in sectors:
    # Sector name
    draw.text((col2_x, y_sec), sec_name, font=font_name, fill="#f1f5f9")
    
    # Penetration Pill Badge (Separate distinct visual from dollar bar)
    pill_w = 95
    pill_x = col2_x + 290
    draw.rounded_rectangle([(pill_x, y_sec - 1), (pill_x + pill_w, y_sec + 17)], radius=4, fill="#1e293b", outline="#334155")
    draw.text((pill_x + 8, y_sec + 1), sec_pill, font=font_pill, fill="#e2e8f0")
    
    # Amount text
    draw.text((col2_x + 430, y_sec), sec_amt, font=font_amt, fill="#22c55e")
    
    # Proportional Dollar Bar
    bar_y = y_sec + 20
    draw.rounded_rectangle([(col2_x, bar_y), (col2_x + col2_w, bar_y + 5)], radius=2, fill="#1e293b")
    # minimum visible bar of 6px so smaller sectors remain visible
    actual_bar_w = max(int(col2_w * bar_scale), 6)
    draw.rounded_rectangle([(col2_x, bar_y), (col2_x + actual_bar_w, bar_y + 5)], radius=2, fill=sec_color)
    
    y_sec += 34

# ==============================================================================
# BOTTOM CALLOUT BOX: BIPARTISAN & SCALE INSIGHTS
# ==============================================================================
box_y = 445
box_h = 160
draw.rounded_rectangle([(40, box_y), (W - 40, box_y + box_h)], radius=8, fill="#131c31", outline="#1e293b", width=1)

# Left sub-box: Capital Distribution
draw.text((60, box_y + 15), "CAPITAL CONCENTRATION & TECH ALLOCATIONS", font=font_box_title, fill="#38bdf8")
draw.text((60, box_y + 36), "Foreign policy advocacy PACs contributed 66% ($16.85M) of all CA PAC funds,\nreaching 52 of 54 members (96% delegation penetration).\nSilicon Valley tech PACs poured $1.87M across 49 lawmakers (91% penetration).\nJimmy Gomez (D-CA-34) ranks #1 overall with $2.59M in total PAC support.", font=font_box_body, fill="#cbd5e1")

draw.line([(580, box_y + 15), (580, box_y + box_h - 15)], fill="#334155", width=1)

# Right sub-box: Bipartisan Balance
draw.text((610, box_y + 15), "BIPARTISAN REACH & COMMITTEE JURISDICTION", font=font_box_title, fill="#10b981")
draw.text((610, box_y + 36), "PAC capital follows committee jurisdiction and seniority across party lines:\n94% of CA members take Big Pharma money; 93% take Defense contractor cash.\nTop recipients span both parties: Ken Calvert (R-CA-41) received $1.33M,\nwhile Pete Aguilar (D-CA-33) and Mike Thompson (D-CA-04) received $1.7M and $1.48M.", font=font_box_body, fill="#cbd5e1")

# Footer
draw.line([(40, 620), (W - 40, 620)], fill="#1e293b", width=1)
draw.text((40, 635), "DONOR CLASS  |  OFFICIAL 2024-2026 FEC FILINGS  |  100% NONPARTISAN CLIENT-SIDE CIVIC ENGINE", font=font_footer, fill="#64748b")
draw.text((W - 250, 635), "EXPLORE LIVE: donorclass.info/?state=CA", font=font_footer, fill="#10b981")

out_dir = "~/.gemini/antigravity/brain/a9dd7135-f05e-45c6-b160-b7d791ff4202"
out_path = os.path.join(out_dir, "california-infographic.png")
img.save(out_path, "PNG")

# Also copy to repo assets
repo_assets = "./assets/infographics"
if os.path.exists(repo_assets):
    repo_out = os.path.join(repo_assets, "california-infographic.png")
    img.save(repo_out, "PNG")
    print("Saved to repo assets:", repo_out)

print("Saved California graphic v2 to:", out_path)
