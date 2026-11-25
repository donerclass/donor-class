# SKILL: Accuracy Language (all agents)

| Never say | Say instead | Why |
|---|---|---|
| verified, verified filings | "Built directly from official FEC bulk files, with links to the source filings." | Overclaim; Rule 2 |
| Official FEC record / FEC data (as a brand) | "Built from FEC public records" | Implies FEC endorsement |
| capped, § 30116 capped total | "direct PAC and committee contributions" | Limit is per PAC per election, not per member total |
| multi-candidate PAC receipts | "PAC and committee contributions" | Dataset includes party and other committees (24K/24Z) |
| received / funded by (for 24E/24A) | "independent spending supporting / opposing" | Outside spending is not money the member received |
| Foreign PACs / Foreign | "Pro-Israel & Foreign Policy PACs" | These are U.S. committees |
| bought, owned, paid off, in the pocket of, corrupt, shill, puppet | describe the amount and the source | Implies wrongdoing; defamation risk |
| all N members (when some have no records) | "X of [State]'s Y members with 2024-cycle FEC records" | Rule 3 |
| 2024-2026 cycle | "2023-2024 cycle, data through Dec 31, 2024" | Until 2026 cycle is ingested |
| Any number without a link | add the FEC committee or filing link | Every number is checkable |

Outliers: any member in `data/documented_variances.json` must show the caveat wherever their number appears, or be left out of rankings.
