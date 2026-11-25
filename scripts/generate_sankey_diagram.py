#!/usr/bin/env python3
"""
Generate publication-quality Sankey flow diagrams for Reddit (r/dataisbeautiful)
and media desks, visualizing how PAC capital flows from economic sectors
through legal committees into congressional delegations.

Strict compliance:
- 100% primary FEC bulk data from data/donor-dataset.csv
- Nonpartisan framing, zero state seals, zero emojis
"""

import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_florida_sankey():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'donor-dataset.csv')
    fl_members = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r['state'] == 'FL':
                fl_members.append(r)
    
    # Sector totals
    sectors = {
        'Wall Street & Finance': sum(float(m['sector_finance']) for m in fl_members),
        'Big Pharma & Health': sum(float(m['sector_pharma']) for m in fl_members),
        'Labor Unions': sum(float(m['sector_labor']) for m in fl_members),
        'Fossil Fuels & Energy': sum(float(m['sector_energy']) for m in fl_members),
        'Defense & Aerospace': sum(float(m['sector_defense']) for m in fl_members),
        'Big Tech & Telecom': sum(float(m['sector_tech']) for m in fl_members),
        'Pro-Israel & FP PACs': sum(float(m['sector_foreign_policy']) for m in fl_members),
        'Uncategorized PACs': sum(float(m['sector_uncategorized']) for m in fl_members),
    }
    
    total_direct = sum(float(m['direct_contributions_total']) for m in fl_members)
    total_ie_sup = sum(float(m['ie_support_total']) for m in fl_members)
    total_ie_opp = sum(float(m['ie_oppose_total']) for m in fl_members)
    
    rep_direct = sum(float(m['direct_contributions_total']) for m in fl_members if m['party'] == 'Republican')
    dem_direct = sum(float(m['direct_contributions_total']) for m in fl_members if m['party'] == 'Democrat')
    
    # Canvas dimensions for Reddit 16:9 high-res
    width, height = 1920, 1080
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.axis('off')
    
    # Custom ribbon flow rendering for a stunning infographic
    # Column X coordinates
    x_sec = 0.05
    x_hub = 0.50
    x_dest = 0.95
    
    # Colors
    sec_colors = {
        'Wall Street & Finance': '#10b981',
        'Big Pharma & Health': '#ef4444',
        'Labor Unions': '#f59e0b',
        'Fossil Fuels & Energy': '#8b5cf6',
        'Defense & Aerospace': '#3b82f6',
        'Big Tech & Telecom': '#06b6d4',
        'Pro-Israel & FP PACs': '#ec4899',
        'Uncategorized PACs': '#64748b'
    }
    
    # Title & Header
    plt.text(0.5, 0.94, "WHERE DOES FLORIDA'S PAC MONEY FLOW?", 
             color='#f8fafc', fontsize=26, fontweight='bold', ha='center', va='center',
             fontfamily='sans-serif')
    plt.text(0.5, 0.90, "Tracking $18.28M in Direct Multi-Candidate PAC Contributions Across 29 Members of Congress", 
             color='#94a3b8', fontsize=14, ha='center', va='center')
    plt.text(0.5, 0.87, "Built directly from official FEC bulk files (2024 cycle through Dec 31, 2024) • donorclass.info", 
             color='#e2b340', fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Left Column: Sectors
    y_start = 0.80
    y_spacing = 0.082
    sector_boxes = []
    
    sorted_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)
    for i, (name, val) in enumerate(sorted_sectors):
        y = y_start - (i * y_spacing)
        color = sec_colors[name]
        pct = (val / total_direct) * 100
        
        # Sector label box
        ax.plot([x_sec, x_sec + 0.18], [y, y], color=color, lw=24, solid_capstyle='round', alpha=0.9)
        ax.text(x_sec + 0.01, y, f"{name}", color='#ffffff', fontsize=11, fontweight='bold', va='center')
        ax.text(x_sec + 0.17, y, f"${val/1e6:.2f}M ({pct:.1f}%)" if val >= 1e6 else f"${val/1e3:.0f}K ({pct:.1f}%)", 
                color='#f1f5f9', fontsize=10, ha='right', va='center', fontweight='bold')
        sector_boxes.append((x_sec + 0.18, y, val, color))
    
    # Middle Column: Central Campaign PAC Hub
    y_hub = 0.51
    ax.plot([x_hub - 0.08, x_hub + 0.08], [y_hub, y_hub], color='#e2b340', lw=50, solid_capstyle='round', alpha=0.95)
    ax.text(x_hub, y_hub + 0.012, "DIRECT CAMPAIGN PACs", color='#0b0f19', fontsize=13, fontweight='black', ha='center', va='center')
    ax.text(x_hub, y_hub - 0.012, f"${total_direct/1e6:.2f}M (52 U.S.C. § 30116 Capped)", color='#0b0f19', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Connect Left to Middle via bezier curves
    for (sx, sy, sval, scolor) in sector_boxes:
        width_norm = max(1.5, (sval / total_direct) * 28)
        # Bezier curve
        t = np.linspace(0, 1, 100)
        x_curve = (1-t)**3 * sx + 3*(1-t)**2*t * (sx + 0.12) + 3*(1-t)*t**2 * (x_hub - 0.20) + t**3 * (x_hub - 0.08)
        y_curve = (1-t)**3 * sy + 3*(1-t)**2*t * sy + 3*(1-t)*t**2 * y_hub + t**3 * y_hub
        ax.plot(x_curve, y_curve, color=scolor, lw=width_norm, alpha=0.45)
    
    # Right Column: Distribution by Party & Chamber
    # Republicans
    y_rep = 0.64
    ax.plot([x_dest - 0.22, x_dest], [y_rep, y_rep], color='#ef4444', lw=36, solid_capstyle='round', alpha=0.9)
    ax.text(x_dest - 0.21, y_rep + 0.008, "Florida Republicans (20 Members)", color='#ffffff', fontsize=12, fontweight='bold', va='center')
    ax.text(x_dest - 0.01, y_rep + 0.008, f"${rep_direct/1e6:.2f}M", color='#ffffff', fontsize=13, fontweight='bold', ha='right', va='center')
    ax.text(x_dest - 0.21, y_rep - 0.010, "Top: Scott ($1.39M), Buchanan ($1.24M), Diaz-Balart ($1.07M)", color='#fca5a5', fontsize=9, va='center')
    
    # Democrats
    y_dem = 0.38
    ax.plot([x_dest - 0.22, x_dest], [y_dem, y_dem], color='#3b82f6', lw=32, solid_capstyle='round', alpha=0.9)
    ax.text(x_dest - 0.21, y_dem + 0.008, "Florida Democrats (9 Members)", color='#ffffff', fontsize=12, fontweight='bold', va='center')
    ax.text(x_dest - 0.01, y_dem + 0.008, f"${dem_direct/1e6:.2f}M", color='#ffffff', fontsize=13, fontweight='bold', ha='right', va='center')
    ax.text(x_dest - 0.21, y_dem - 0.010, "Top: Soto ($1.40M), Wasserman Schultz ($824K), Frankel ($808K)", color='#93c5fd', fontsize=9, va='center')
    
    # Connect Middle to Right via curves
    # To Reps
    t = np.linspace(0, 1, 100)
    w_rep = (rep_direct / total_direct) * 28
    xr = (1-t)**3 * (x_hub + 0.08) + 3*(1-t)**2*t * (x_hub + 0.18) + 3*(1-t)*t**2 * (x_dest - 0.32) + t**3 * (x_dest - 0.22)
    yr = (1-t)**3 * y_hub + 3*(1-t)**2*t * y_hub + 3*(1-t)*t**2 * y_rep + t**3 * y_rep
    ax.plot(xr, yr, color='#ef4444', lw=w_rep, alpha=0.45)
    
    # To Dems
    w_dem = (dem_direct / total_direct) * 28
    xd = (1-t)**3 * (x_hub + 0.08) + 3*(1-t)**2*t * (x_hub + 0.18) + 3*(1-t)*t**2 * (x_dest - 0.32) + t**3 * (x_dest - 0.22)
    yd = (1-t)**3 * y_hub + 3*(1-t)**2*t * y_hub + 3*(1-t)*t**2 * y_dem + t**3 * y_dem
    ax.plot(xd, yd, color='#3b82f6', lw=w_dem, alpha=0.45)
    
    # Independent Outside Spending Callout Box (Lower Center)
    ax.plot([0.35, 0.65], [0.18, 0.18], color='#1e293b', lw=36, solid_capstyle='round')
    ax.text(0.50, 0.19, "LEGAL SEPARATION: INDEPENDENT OUTSIDE SPENDING", color='#94a3b8', fontsize=9, fontweight='bold', ha='center', va='center')
    ax.text(0.50, 0.17, f"Outside Support: ${total_ie_sup/1e6:.2f}M  •  Outside Opposition: ${total_ie_opp/1e3:.0f}K (Independent Ad Spending)", 
            color='#38bdf8', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Footer Notes
    plt.text(0.5, 0.06, "Data Source: Federal Election Commission Bulk Disclosures (itpas2.txt, weball24.txt). 433 of 517 members nationwide match FEC summaries within 10% with all variances documented.",
             color='#64748b', fontsize=10, ha='center', va='center')
    plt.text(0.5, 0.03, "Nonpartisan Civic Intelligence • Free Public Inspection • donorclass.info/?state=FL",
             color='#94a3b8', fontsize=11, fontweight='bold', ha='center', va='center')
    
    # Save output
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'infographics')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'fl-sankey-flow.png')
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated Florida Sankey diagram at: {out_path}")

if __name__ == '__main__':
    generate_florida_sankey()
