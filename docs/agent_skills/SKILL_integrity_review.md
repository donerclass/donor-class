# SKILL: Integrity Review (Data Integrity agent only)

You did not build it, so you can check it. Your output is `pass` or `fail` with evidence, posted to `docs/agent_board/messages/`.

## Every review
1. **Numbers:** re-run `python3 scripts/check_state_preflight.py --state XX` (or the re-check script in `docs/REBUILD_REVIEW_2026-11-24.md`). Paste the command and output.
2. **Traceability:** pick 5 numbers from the draft; find each in `data/donor-dataset.csv`; open 2 FEC committee links and confirm they resolve.
3. **Language:** grep the draft/HTML against every "Never say" item in `SKILL_accuracy_language.md`. Paste the grep.
4. **Separation:** contributions and independent spending are never summed or merged in one figure.
5. **Uncategorized** appears in every sector chart/table.
6. **Outliers:** every documented-variance member that appears carries the caveat.
7. **Voice (posts only):** Rule 8 checks: no wrongdoing words, snark aimed at the system, both parties treated evenly across the week, no snark on caveated numbers.
8. **Anonymity:** no personal names, emails, or local file paths.

Any single failure = `fail`. Do not fix it yourself; send it back to the author with the line and the reason.
