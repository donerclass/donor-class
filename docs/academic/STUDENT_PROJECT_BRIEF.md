# Student Project Brief

## Classifying Uncategorized PAC Committees in the DONOR CLASS Dataset

**Dataset:** DONOR CLASS — Committee-to-Candidate Contributions, 119th Congress (2023-2024)  
**Version:** 1.0.0-data-2024  
**URL:** https://donorclass.info  
**Contact:** contact@donorclass.info

---

## Background

The DONOR CLASS dataset documents itemized political action committee (PAC) contributions to all 539 members of the 119th U.S. Congress, reconstructed from Federal Election Commission (FEC) bulk data for the 2023–2024 election cycle. Each contributing committee is classified into one of eight industry sectors: Defense, Pharma/Health, Finance, Energy, Tech, Foreign Policy, Labor, and Uncategorized.

As of the current release, approximately **56% of total direct PAC dollars** — across roughly **3,600 unique committees** — remain in the Uncategorized sector. This limits the dataset's analytical utility for industry-level analysis. Classifying even the top 500 committees by dollar volume would substantially reduce this gap.

---

## Project Task

**Classify the top 500 uncategorized PAC committees** by total contribution volume into the eight sectors defined in the dataset's sector classification scheme.

The starting list is provided in `uncategorized_top500.csv` with columns: `cmte_id`, `cmte_name`, `total_amount`.

For each committee, coders will:

1. Look up the committee name in the FEC Committee Master (`cm24.txt`, freely downloadable from fec.gov).
2. Use the committee's connected organization name and stated purpose to assign it to one of the eight sectors, or flag it as `Other/Multi` if it does not fit.
3. Document the basis for the classification in a one-line memo field.

The FEC Committee Master is a public file; no data access agreements or institutional review is required for the publicly available FEC data.

---

## Deliverables

A completed project should produce:

1. **Classified CSV** — the `uncategorized_top500.csv` with two new columns: `assigned_sector` and `classification_basis`.
2. **Methods memo** — a one-to-two page document describing the classification criteria, any judgment calls made for borderline cases, and any sectors where the classification scheme needed interpretation.
3. **Inter-coder reliability statistic** — at minimum, a Cohen's kappa or percent agreement on the 10% double-coded subsample (described below).

---

## Quality Control

To assess reliability, coders should double-code a **10% random sample** (50 committees) independently before comparing results. Disagreements should be adjudicated and documented.

A project achieving kappa ≥ 0.70 on the double-coded subsample is considered publication-quality for a replication study; kappa ≥ 0.80 is suitable for primary research.

---

## Credit and Attribution

Completed classifications submitted to the project (via GitHub pull request or by contacting the team) will be incorporated into the next dataset release. Contributors will be named in the dataset's contributor list (with their consent) and will be listed in `CITATION.cff` by name or institutional affiliation as preferred.

The dataset carries a Zenodo DOI (pending issuance), making it citable in academic work. Student contributions to the classification effort will be credited in a versioned dataset release with its own DOI.

---

## Course Fit

This project is well suited to:

- **Data analytics capstone** — data cleaning, manual classification, reliability assessment, and documentation.
- **Political science research methods** — operationalizing a contested variable (PAC industry affiliation) with inter-coder reliability.
- **Data journalism lab** — real, public, policy-relevant data; publishable findings from completing the top-500 classification.
- **Library research data services** — dataset curation, annotation, and documentation workflows.

The dataset is open-access, fully documented, and reproducible from public FEC source files. No subscription, licensing fee, or institutional data agreement is required.

---

## Resources

- Dataset documentation: https://donorclass.info/data/
- Sector definitions: `release/DATA_DICTIONARY.md`
- FEC Committee Master: https://www.fec.gov/data/bulk-downloads/2024/cm24.zip
- FEC data documentation: https://www.fec.gov/campaign-finance-data/all-candidates-file-description/

---

*Donor Class Team — donorclass.info — 2026*
