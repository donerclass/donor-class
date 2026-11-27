# DONOR CLASS — One-Pager for Academic Partners

**donorclass.info** | contact@donorclass.info | github.com/donerclass/donor-class

---

## What It Is

DONOR CLASS is an open dataset of political action committee (PAC) contributions to all 539 members of the 119th U.S. Congress, reconstructed from Federal Election Commission bulk data for the 2023–2024 election cycle. It is freely available, fully documented, and reproducible from public source files.

**Coverage:**
- 539 House and Senate members
- ~3,600 unique contributing committees
- 8 industry sectors (Defense, Pharma/Health, Finance, Energy, Tech, Foreign Policy, Labor, Uncategorized)
- Independent expenditures reported separately — never summed with direct contributions

---

## What Makes It Verifiable

- **Open source code** — full pipeline published on GitHub; anyone can re-run the build from the same FEC source files.
- **SHA-256 checksums** — all source file hashes documented in `SOURCES.json`; anyone can verify provenance.
- **Reconciliation audit** — 433 of 517 members verified within 10% of FEC's own summary; all larger variances documented with reason codes in `RECONCILIATION_AUDIT.md`.
- **DOI (pending)** — Zenodo deposit in progress; will be citable with a persistent identifier once issued.
- **CC BY 4.0 license** — freely reusable with attribution.

---

## The Research Gap

Approximately 56% of direct PAC dollars — across roughly 3,600 committees — remain unclassified by industry sector. The dataset ships with a list of the top 500 unclassified committees by dollar volume (`uncategorized_top500.csv`), suitable for a structured classification project.

---

## The Ask

We are looking for academic partners interested in:

1. **Student classification projects** — using `uncategorized_top500.csv` as a data annotation exercise in a research methods, data analytics, or data journalism course.
2. **Course dataset** — using the full DONOR CLASS dataset in a campaign finance, political economy, or data journalism unit.
3. **Research collaboration** — co-authoring analysis based on the dataset once the Zenodo DOI is issued.

Nothing is required upfront. The data and documentation are publicly available now.

---

*Donor Class Team — donorclass.info — 2026*
