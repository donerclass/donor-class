#!/usr/bin/env python3
"""
Generate static HTML pages for members, states, sectors, methodology, and data,
along with llms.txt, donor-dataset.json, and sitemap.xml.
Adheres strictly to SKILL_static_pages_geo.md and all accuracy & anonymity rules.
"""

import os
import json
import csv
import re
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
MEMBERS_DIR = os.path.join(DATA_DIR, "members")

SECTOR_DISPLAY = {
    "defense": "Defense & Aerospace",
    "pharma": "Pharmaceuticals & Health Products",
    "finance": "Finance, Insurance & Real Estate",
    "energy": "Energy & Natural Resources",
    "tech": "Technology & Communications",
    "foreign_policy": "Foreign Policy & Defense Advocates",
    "labor": "Labor Unions & Associations",
    "uncategorized": "Uncategorized"
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
    "DC": "District of Columbia", "AS": "American Samoa", "GU": "Guam", "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico", "VI": "Virgin Islands"
}

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    return re.sub(r'[\s-]+', '-', text)

def fmt_curr(val):
    try:
        val = float(val)
        return f"${val:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def get_base_html(title, description, canonical_url, body_content, json_ld=None):
    schema_script = f'<script type="application/ld+json">{json.dumps(json_ld, indent=2)}</script>' if json_ld else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="author" content="Donor Class Team">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="stylesheet" href="/styles.css">
  {schema_script}
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #0b0f19; color: #f1f5f9; }}
    .container {{ max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem; }}
    header.static-header {{ border-bottom: 1px solid #1e293b; padding-bottom: 1.5rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }}
    header.static-header a.logo {{ font-weight: 800; font-size: 1.25rem; color: #38bdf8; text-decoration: none; letter-spacing: -0.025em; }}
    nav.static-nav a {{ color: #94a3b8; text-decoration: none; margin-left: 1.25rem; font-size: 0.95rem; font-weight: 500; }}
    nav.static-nav a:hover {{ color: #f8fafc; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.5rem; color: #ffffff; letter-spacing: -0.02em; }}
    .meta-tag {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background: #1e293b; color: #94a3b8; font-size: 0.875rem; font-weight: 600; margin-right: 0.5rem; margin-bottom: 1rem; }}
    table.data-table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; background: #0f172a; border-radius: 0.5rem; overflow: hidden; border: 1px solid #1e293b; }}
    table.data-table th, table.data-table td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid #1e293b; font-size: 0.95rem; }}
    table.data-table th {{ background: #1e293b; color: #cbd5e1; font-weight: 600; }}
    table.data-table td.amount {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 500; }}
    table.data-table th.amount {{ text-align: right; }}
    .callout {{ background: #131d31; border-left: 4px solid #38bdf8; padding: 1rem 1.25rem; border-radius: 0.25rem; margin: 1.5rem 0; font-size: 0.95rem; color: #cbd5e1; }}
    .callout.variance {{ border-left-color: #f59e0b; background: #261d11; }}
    footer.static-footer {{ margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #1e293b; font-size: 0.875rem; color: #64748b; text-align: center; }}
    footer.static-footer a {{ color: #94a3b8; text-decoration: none; }}
    footer.static-footer a:hover {{ text-decoration: underline; }}
    a.btn-interactive {{ display: inline-block; margin-top: 1rem; padding: 0.6rem 1.2rem; background: #0284c7; color: #ffffff; font-weight: 600; border-radius: 0.375rem; text-decoration: none; transition: background 0.2s; }}
    a.btn-interactive:hover {{ background: #0369a1; }}
  </style>
</head>
<body>
  <div class="container">
    <header class="static-header">
      <a href="/" class="logo">DONOR CLASS</a>
      <nav class="static-nav">
        <a href="/">Interactive Map</a>
        <a href="/methodology/">Methodology</a>
        <a href="/data/">Data</a>
      </nav>
    </header>
    <main>
      {body_content}
    </main>
    <footer class="static-footer">
      <p>Built from FEC public records. Data through Dec 31, 2024. Independent research and nonpartisan campaign finance transparency.</p>
      <p><a href="/">Home</a> | <a href="/methodology/">Methodology</a> | <a href="/data/">Data Downloads</a> | <a href="/privacy.html">Privacy</a></p>
    </footer>
  </div>
</body>
</html>"""

def build():
    variances = {}
    var_file = os.path.join(DATA_DIR, "documented_variances.json")
    if os.path.exists(var_file):
        with open(var_file, "r") as f:
            v_data = json.load(f)
            variances = {item.get("bioguide_id"): item for item in v_data.get("variances", []) if item.get("bioguide_id")}

    members_list = []
    with open(os.path.join(DATA_DIR, "donor-dataset.csv"), "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            members_list.append(row)

    print(f"Loaded {len(members_list)} members from donor-dataset.csv")

    sitemap_urls = [
        ("https://donorclass.info/", "2026-11-27", "daily", "1.0"),
        ("https://donorclass.info/methodology/", "2026-11-27", "weekly", "0.8"),
        ("https://donorclass.info/data/", "2026-11-27", "weekly", "0.8"),
    ]

    # 1. Member Pages
    for m in members_list:
        bid = m["bioguide_id"]
        name = m["name"]
        slug = f"{bid}-{slugify(name)}"
        state = m["state"]
        dist = m.get("district", "0")
        chamber = m["chamber"]
        party = m["party"]
        direct_total = float(m["direct_contributions_total"] or 0)
        ie_sup = float(m["ie_support_total"] or 0)
        ie_opp = float(m["ie_oppose_total"] or 0)

        # Load detailed pac list from members/
        m_json_path = os.path.join(MEMBERS_DIR, f"{bid}.json")
        pacs = []
        if os.path.exists(m_json_path):
            with open(m_json_path, "r") as jf:
                m_detail = json.load(jf)
                pacs = m_detail.get("pacs", [])

        # Sort PACs by amount desc
        pacs.sort(key=lambda x: abs(float(x.get("amount", 0))), reverse=True)
        top_pacs = pacs[:25]

        # Variance check
        variance_html = ""
        if bid in variances:
            v_info = variances[bid]
            variance_html = f"""
            <div class="callout variance">
              <strong>Reconciliation Note:</strong> FEC Weball Summary shows {fmt_curr(v_info.get('fec_weball_total', 0))}.
              Rebuilt PAC direct contribution total is {fmt_curr(direct_total)} (Variance: {v_info.get('variance_pct', 0)}%).<br>
              <em>Reason:</em> {v_info.get('reason', '')}
            </div>
            """

        # Sector breakdown table
        sector_rows = ""
        for sec_id, sec_title in SECTOR_DISPLAY.items():
            amt = float(m.get(f"sector_{sec_id}", 0) or 0)
            pct = (amt / direct_total * 100) if direct_total > 0 else 0
            sector_rows += f"""
            <tr>
              <td>{sec_title}</td>
              <td class="amount">{fmt_curr(amt)}</td>
              <td class="amount">{pct:.1f}%</td>
            </tr>"""

        # PAC table
        pac_rows = ""
        for p in top_pacs:
            cid = p.get("id", "")
            cname = p.get("name", "Unknown Committee")
            p_amt = float(p.get("amount", 0))
            p_sec = p.get("sector_name") or SECTOR_DISPLAY.get(p.get("sector", "uncategorized"), "Uncategorized")
            fec_link = f"https://www.fec.gov/data/committee/{cid}/" if cid else "#"
            pac_rows += f"""
            <tr>
              <td><a href="{fec_link}" target="_blank" rel="noopener noreferrer" style="color: #38bdf8;">{cname}</a> <span style="font-size:0.8rem; color:#64748b;">({cid})</span></td>
              <td>{p_sec}</td>
              <td class="amount">{fmt_curr(p_amt)}</td>
            </tr>"""

        district_str = f"District {dist}" if chamber.lower() == "house" and dist != "0" else ("At-Large" if chamber.lower() == "house" else "Senate")

        body = f"""
        <h1>{name}</h1>
        <div>
          <span class="meta-tag">{party}</span>
          <span class="meta-tag">{state} - {district_str}</span>
          <span class="meta-tag">{chamber}</span>
        </div>

        <p>FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings.</p>

        {variance_html}

        <h2>PAC & Committee Contributions Summary</h2>
        <table class="data-table">
          <thead>
            <tr><th>Metric</th><th class="amount">Amount</th></tr>
          </thead>
          <tbody>
            <tr><td><strong>Direct PAC Contributions Total</strong></td><td class="amount"><strong>{fmt_curr(direct_total)}</strong></td></tr>
            <tr><td>Outside Independent Spending Supporting</td><td class="amount">{fmt_curr(ie_sup)}</td></tr>
            <tr><td>Outside Independent Spending Opposing</td><td class="amount">{fmt_curr(ie_opp)}</td></tr>
          </tbody>
        </table>
        <p style="font-size: 0.85rem; color: #94a3b8;">*Note: Outside independent spending is reported by third-party PACs/Super PACs advocating for or against the candidate and is kept strictly separate from direct campaign contributions.</p>

        <h2>Direct Contributions by Sector</h2>
        <table class="data-table">
          <thead>
            <tr><th>Sector</th><th class="amount">Total</th><th class="amount">Share</th></tr>
          </thead>
          <tbody>
            {sector_rows}
          </tbody>
        </table>

        <h2>Top Committee Contributors</h2>
        <table class="data-table">
          <thead>
            <tr><th>Committee Name</th><th>Sector</th><th class="amount">Amount</th></tr>
          </thead>
          <tbody>
            {pac_rows if pac_rows else '<tr><td colspan="3">No direct PAC contributions recorded in bulk files.</td></tr>'}
          </tbody>
        </table>

        <div style="margin-top: 2rem;">
          <a href="/?candidate={m.get('fec_candidate_id', '')}" class="btn-interactive">View in Interactive Explorer &rarr;</a>
        </div>
        """

        json_ld = {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": name,
            "jobTitle": f"U.S. {chamber} Member",
            "affiliation": {"@type": "Organization", "name": f"U.S. {chamber}"},
            "description": f"{name} ({party}-{state}) received {fmt_curr(direct_total)} in direct PAC contributions during the 2023-2024 FEC cycle."
        }

        page_title = f"{name} ({party}-{state}) Campaign Finance & PAC Donors | DONOR CLASS"
        page_desc = f"Explore {fmt_curr(direct_total)} in PAC contributions to {name} ({party}-{state}). Detailed breakdown across Defense, Pharma, Finance, Energy, Tech, Foreign Policy, Labor, and Uncategorized."
        canon = f"https://donorclass.info/members/{slug}/"

        out_dir = os.path.join(REPO_ROOT, "members", slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out_f:
            out_f.write(get_base_html(page_title, page_desc, canon, body, json_ld))

        sitemap_urls.append((canon, "2026-11-27", "monthly", "0.6"))

    print(f"Generated {len(members_list)} static member pages.")

    # 2. State Pages
    state_members = {}
    for m in members_list:
        st = m["state"]
        state_members.setdefault(st, []).append(m)

    for st, m_list in state_members.items():
        st_slug = st.lower()
        st_name = STATE_NAMES.get(st, st)
        total_direct = sum(float(x.get("direct_contributions_total", 0) or 0) for x in m_list)
        total_ie_sup = sum(float(x.get("ie_support_total", 0) or 0) for x in m_list)
        total_ie_opp = sum(float(x.get("ie_oppose_total", 0) or 0) for x in m_list)

        # Sector aggregates for state
        st_sec_totals = {sec: sum(float(x.get(f"sector_{sec}", 0) or 0) for x in m_list) for sec in SECTOR_DISPLAY}

        sec_rows = ""
        for sec_id, sec_title in SECTOR_DISPLAY.items():
            amt = st_sec_totals[sec_id]
            pct = (amt / total_direct * 100) if total_direct > 0 else 0
            sec_rows += f"""
            <tr>
              <td><a href="/sectors/{sec_id}/" style="color: #38bdf8;">{sec_title}</a></td>
              <td class="amount">{fmt_curr(amt)}</td>
              <td class="amount">{pct:.1f}%</td>
            </tr>"""

        # Delegation table
        del_rows = ""
        for m in sorted(m_list, key=lambda x: float(x.get("direct_contributions_total", 0) or 0), reverse=True):
            bid = m["bioguide_id"]
            slug = f"{bid}-{slugify(m['name'])}"
            d_total = float(m.get("direct_contributions_total", 0) or 0)
            del_rows += f"""
            <tr>
              <td><a href="/members/{slug}/" style="color: #38bdf8; font-weight: 500;">{m['name']}</a></td>
              <td>{m['chamber']}</td>
              <td>{m['party']}</td>
              <td class="amount">{fmt_curr(d_total)}</td>
            </tr>"""

        body = f"""
        <h1>{st_name} Congressional Delegation Campaign Finance</h1>
        <p>FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings.</p>

        <h2>Delegation PAC Funding Totals</h2>
        <table class="data-table">
          <thead>
            <tr><th>Metric</th><th class="amount">Amount</th></tr>
          </thead>
          <tbody>
            <tr><td><strong>Direct PAC Contributions to Delegation</strong></td><td class="amount"><strong>{fmt_curr(total_direct)}</strong></td></tr>
            <tr><td>Outside Independent Spending Supporting</td><td class="amount">{fmt_curr(total_ie_sup)}</td></tr>
            <tr><td>Outside Independent Spending Opposing</td><td class="amount">{fmt_curr(total_ie_opp)}</td></tr>
          </tbody>
        </table>

        <h2>Sector Breakdown ({st_name})</h2>
        <table class="data-table">
          <thead>
            <tr><th>Sector</th><th class="amount">Total</th><th class="amount">Share</th></tr>
          </thead>
          <tbody>
            {sec_rows}
          </tbody>
        </table>

        <h2>Members of Congress ({st_name})</h2>
        <table class="data-table">
          <thead>
            <tr><th>Member</th><th>Chamber</th><th>Party</th><th class="amount">Direct PAC Total</th></tr>
          </thead>
          <tbody>
            {del_rows}
          </tbody>
        </table>

        <div style="margin-top: 2rem;">
          <a href="/?state={st}" class="btn-interactive">Explore {st_name} Interactively &rarr;</a>
        </div>
        """

        page_title = f"{st_name} Congressional PAC Contributions & Campaign Finance | DONOR CLASS"
        page_desc = f"Track {fmt_curr(total_direct)} in PAC and committee contributions across all {len(m_list)} members of the {st_name} congressional delegation."
        canon = f"https://donorclass.info/states/{st_slug}/"

        out_dir = os.path.join(REPO_ROOT, "states", st_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out_f:
            out_f.write(get_base_html(page_title, page_desc, canon, body))

        sitemap_urls.append((canon, "2026-11-27", "weekly", "0.7"))

    print(f"Generated {len(state_members)} static state pages.")

    # 3. Sector Pages
    grand_total_direct = sum(float(x.get("direct_contributions_total", 0) or 0) for x in members_list)

    for sec_id, sec_title in SECTOR_DISPLAY.items():
        sec_slug = sec_id
        sec_total = sum(float(x.get(f"sector_{sec_id}", 0) or 0) for x in members_list)
        sec_pct = (sec_total / grand_total_direct * 100) if grand_total_direct > 0 else 0

        # Top recipients in this sector
        top_recipients = sorted(members_list, key=lambda x: float(x.get(f"sector_{sec_id}", 0) or 0), reverse=True)[:50]
        rec_rows = ""
        for m in top_recipients:
            amt = float(m.get(f"sector_{sec_id}", 0) or 0)
            if amt <= 0:
                continue
            bid = m["bioguide_id"]
            slug = f"{bid}-{slugify(m['name'])}"
            rec_rows += f"""
            <tr>
              <td><a href="/members/{slug}/" style="color: #38bdf8; font-weight: 500;">{m['name']}</a></td>
              <td>{m['state']}</td>
              <td>{m['chamber']}</td>
              <td>{m['party']}</td>
              <td class="amount">{fmt_curr(amt)}</td>
            </tr>"""

        body = f"""
        <h1>{sec_title} PAC Contributions to Congress</h1>
        <p>FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings.</p>

        <div class="callout">
          <strong>Sector Aggregate:</strong> {fmt_curr(sec_total)} total across all 539 members of the 119th Congress ({sec_pct:.1f}% of all direct committee contributions).
        </div>

        <h2>Top Congressional Recipients ({sec_title})</h2>
        <table class="data-table">
          <thead>
            <tr><th>Member</th><th>State</th><th>Chamber</th><th>Party</th><th class="amount">Contribution Total</th></tr>
          </thead>
          <tbody>
            {rec_rows}
          </tbody>
        </table>

        <div style="margin-top: 2rem;">
          <a href="/" class="btn-interactive">Explore Full Sector Flows on Interactive Map &rarr;</a>
        </div>
        """

        page_title = f"{sec_title} PAC Donations to Congress (2024) | DONOR CLASS"
        page_desc = f"Total {sec_title} contributions to U.S. Congress reached {fmt_curr(sec_total)}. View the top House and Senate recipients based on official FEC filings."
        canon = f"https://donorclass.info/sectors/{sec_slug}/"

        out_dir = os.path.join(REPO_ROOT, "sectors", sec_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out_f:
            out_f.write(get_base_html(page_title, page_desc, canon, body))

        sitemap_urls.append((canon, "2026-11-27", "weekly", "0.7"))

    print("Generated 8 static sector pages.")

    # 4. Methodology Page
    meth_body = """
    <h1>Methodology & Data Sources</h1>
    <p>FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings.</p>

    <h2>Data Pipeline & Verification</h2>
    <p>DONOR CLASS processes official Federal Election Commission bulk data releases covering the complete 2023–2024 federal election cycle. Data files ingested include:</p>
    <ul>
      <li><strong>pas224:</strong> Contributions from committees to candidates and other committees.</li>
      <li><strong>cm24:</strong> Committee master records (committee type, connected organization, designations).</li>
      <li><strong>cn24:</strong> Candidate master records.</li>
      <li><strong>ccl24:</strong> Candidate-to-committee linkage records.</li>
      <li><strong>weball24:</strong> Campaign summary figures reported directly by candidate principal campaign committees.</li>
    </ul>

    <h2>Reconciliation Audit</h2>
    <p>433 of 517 members match the FEC's own summary within 10%; every larger variance is individually documented in our reconciliation audit. Key accounting distinctions include:</p>
    <ul>
      <li><strong>Joint Fundraising Committee (JFC) Transfers:</strong> Bulk committee filings report direct disbursements to campaigns, whereas campaign summaries frequently aggregate these under transfers from authorized committees.</li>
      <li><strong>Chamber Transitions:</strong> Candidates transitioning from House to Senate campaigns account for split filings across committee IDs.</li>
      <li><strong>Independent Spending Separation:</strong> Independent expenditures (24E support, 24A oppose) are kept strictly distinct and are never summed with direct campaign contributions.</li>
    </ul>

    <h2>Classification Framework</h2>
    <p>Committees are assigned to one of eight macro sectors based on their FEC connected organization, economic interest, and primary industry filings. Uncategorized PACs (comprising ~56% of direct committee disbursements) are reported transparently as their own distinct category.</p>
    """
    meth_dir = os.path.join(REPO_ROOT, "methodology")
    os.makedirs(meth_dir, exist_ok=True)
    with open(os.path.join(meth_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(get_base_html("Methodology & FEC Data Pipeline | DONOR CLASS", "Official methodology, reconciliation audit details, and FEC bulk data processing pipeline for DONOR CLASS.", "https://donorclass.info/methodology/", meth_body))

    # 5. Data Index Page
    data_body = """
    <h1>Data Downloads & Open Access</h1>
    <p>FEC 2023-2024 cycle data through Dec 31, 2024. Built directly from official FEC bulk files, with links to the source filings.</p>

    <div class="callout">
      <strong>Open Data Commitment:</strong> All derived datasets are published under Creative Commons Attribution 4.0 International (CC BY 4.0). No individual contributor information is included.
    </div>

    <h2>Direct Dataset Downloads</h2>
    <table class="data-table">
      <thead>
        <tr><th>Dataset / File</th><th>Format</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><a href="/data/donor-dataset.csv" style="color: #38bdf8; font-weight: 600;">donor-dataset.csv</a></td>
          <td>CSV</td>
          <td>Member-level summaries for all 539 members of the 119th Congress, including sector breakdown and outside spending.</td>
        </tr>
        <tr>
          <td><a href="/data/donor-dataset.json" style="color: #38bdf8; font-weight: 600;">donor-dataset.json</a></td>
          <td>JSON</td>
          <td>Clean JSON summary export of all member campaign finance metrics and sector allocations.</td>
        </tr>
        <tr>
          <td><a href="/data/sector_map.csv" style="color: #38bdf8; font-weight: 600;">sector_map.csv</a></td>
          <td>CSV</td>
          <td>Complete committee classification mapping linking FEC Committee IDs to sectors.</td>
        </tr>
        <tr>
          <td><a href="/data/documented_variances.json" style="color: #38bdf8; font-weight: 600;">documented_variances.json</a></td>
          <td>JSON</td>
          <td>Documented variances reconciling rebuilt figures with FEC Weball campaign summaries.</td>
        </tr>
        <tr>
          <td><a href="/data/SOURCES.json" style="color: #38bdf8; font-weight: 600;">SOURCES.json</a></td>
          <td>JSON</td>
          <td>FEC bulk file hashes, timestamps, and download sources.</td>
        </tr>
      </tbody>
    </table>
    """
    data_dir = os.path.join(REPO_ROOT, "data")
    with open(os.path.join(data_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(get_base_html("Data Downloads & Open Dataset Access | DONOR CLASS", "Download complete CSV and JSON datasets of PAC contributions to the 119th Congress. Open access under CC BY 4.0.", "https://donorclass.info/data/", data_body))

    # 6. JSON Export
    with open(os.path.join(DATA_DIR, "donor-dataset.json"), "w", encoding="utf-8") as jf:
        json.dump(members_list, jf, indent=2)
    print("Exported data/donor-dataset.json")

    # 7. llms.txt
    llms_text = """# DONOR CLASS (donorclass.info)
> Nonpartisan campaign finance intelligence tracking committee-to-candidate contributions to the 119th U.S. Congress (2023-2024 election cycle).

## What This Data Is
- Rebuilt from official Federal Election Commission (FEC) bulk data files (pas2, cm, cn, ccl, weball24) through Dec 31, 2024.
- Tracks direct contributions from Political Action Committees (PACs), Super PACs, leadership PACs, and party committees to candidate principal campaign committees.
- Classifies committee contributions across 8 macro sectors: Defense & Aerospace, Pharmaceuticals & Health Products, Finance, Insurance & Real Estate, Energy & Natural Resources, Technology & Communications, Foreign Policy & Defense Advocates, Labor Unions & Associations, and Uncategorized.
- Keeps independent expenditures (outside spending supporting and opposing) strictly separate from direct contributions.

## What This Data Is Not
- Contains zero individual donor records.
- Does not track personal contributions or small-dollar unitemized individual donations.
- Does not make partisan value judgments or endorsements.

## Primary Endpoints and Resources
- Methodology: https://donorclass.info/methodology/
- Data Downloads: https://donorclass.info/data/
- CSV Dataset: https://donorclass.info/data/donor-dataset.csv
- JSON Dataset: https://donorclass.info/data/donor-dataset.json
- Sector Map: https://donorclass.info/data/sector_map.csv
- States Index: https://donorclass.info/states/
- Sectors Index: https://donorclass.info/sectors/
- GitHub: https://github.com/donerclass/donor-class
"""
    with open(os.path.join(REPO_ROOT, "llms.txt"), "w", encoding="utf-8") as lf:
        lf.write(llms_text)
    print("Generated llms.txt")

    # 8. Sitemap.xml
    sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, freq, prio in sitemap_urls:
        sitemap_content.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    sitemap_content.append('</urlset>')
    with open(os.path.join(REPO_ROOT, "sitemap.xml"), "w", encoding="utf-8") as sf:
        sf.write("\n".join(sitemap_content) + "\n")
    print(f"Generated sitemap.xml with {len(sitemap_urls)} URLs.")

if __name__ == "__main__":
    build()
