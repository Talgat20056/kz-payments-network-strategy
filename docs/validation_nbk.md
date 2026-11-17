# NBK data validation

Tolerance: |diff| <= 0.1% of the parent total (values are rounded to 0.1 thousand / 0.1 mln KZT).
Checks run on every release (all vintages). `FLAG` = outside tolerance.

Checks run: 1832. Flags: 198 ({'ERROR': 16, 'INFO-residual': 143, 'INFO-scope': 39}).

* **ERROR** = source table internally inconsistent -> excluded or quality-flagged (see `EXCLUDE` / `QUALITY` in `src/acquire/nbk_parse.py`).
* **INFO-residual** = international total exceeds Visa + MasterCard + UnionPay by 0.1-0.3%. Systematic in every release since UnionPay was broken out (v266); interpreted as other international schemes not itemised by NBK. Kept as `other_international` [calc].
* **INFO-scope** = Table 5 (by region) and Table 6 (by channel) have the same stated scope but totals differ by up to ~0.3%. NBK does not explain the gap; we use T6 for channel mix and T5 for regional mix and never mix them in one ratio.

| category | release as-of | check | parent | sum of parts | diff | rel diff |
|---|---|---|---|---|---|---|
| ERROR | 2024-07-01 | T4 txn_value cash_withdrawal 2023-06-30: total = local + international | 8,688,689.3 | 10,667,236.1 | -1,978,546.8 | 22.77% |
| ERROR | 2024-07-01 | T4 txn_value cashless 2023-06-30: total = local + international | 50,887,004.4 | 62,769,284.0 | -11,882,279.7 | 23.35% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2024-08-01: mastercard = debit + credit + limit/prepaid | 3,107.9 | 24,274.1 | -21,166.2 | 681.05% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2024-08-01: total = local + international | 78,063.0 | 104,456.0 | -26,393.0 | 33.81% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2024-08-01: visa = debit + credit + limit/prepaid | 52,606.6 | 74,953.6 | -22,347.0 | 42.48% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2025-08-01: mastercard = debit + credit + limit/prepaid | 2,367.0 | 29,646.9 | -27,279.9 | 1152.51% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2025-08-01: total = local + international | 81,721.1 | 109,374.7 | -27,653.6 | 33.84% |
| ERROR | 2025-08-01 | T1 cards_in_circulation 2025-08-01: visa = debit + credit + limit/prepaid | 54,482.3 | 74,374.6 | -19,892.3 | 36.51% |
| ERROR | 2025-08-01 | T1 cards_used 2024-08-01: mastercard = debit + credit + limit/prepaid | 423.7 | 6,478.7 | -6,055.0 | 1429.08% |
| ERROR | 2025-08-01 | T1 cards_used 2024-08-01: total = local + international | 179.7 | 55,542.4 | -55,362.7 | 30808.40% |
| ERROR | 2025-08-01 | T1 cards_used 2024-08-01: visa = debit + credit + limit/prepaid | 22,987.7 | 38,107.7 | -15,120.0 | 65.77% |
| ERROR | 2025-08-01 | T1 cards_used 2025-08-01: mastercard = debit + credit + limit/prepaid | 315.1 | 6,102.3 | -5,787.2 | 1836.62% |
| ERROR | 2025-08-01 | T1 cards_used 2025-08-01: total = local + international | 576.1 | 57,337.8 | -56,761.7 | 9852.75% |
| ERROR | 2025-08-01 | T1 cards_used 2025-08-01: visa = debit + credit + limit/prepaid | 23,479.3 | 39,624.2 | -16,144.9 | 68.76% |
| ERROR | 2025-08-01 | T2 vs T1 cards_in_circulation: T1 total = T2 TOTAL (debit+credit+other) | 81,721.1 | 81,928.4 | -207.3 | 0.25% |
| ERROR | 2025-08-01 | T2 vs T1 cards_used: T1 total = T2 TOTAL (debit+credit+other) | 576.1 | 40,408.5 | -39,832.4 | 6914.15% |
| INFO-residual | 2025-11-01 | T1 cards_in_circulation 2024-11-01: international = Visa + MC + UnionPay | 54,170.7 | 54,061.3 | 109.4 | 0.20% |
| INFO-residual | 2025-11-01 | T1 cards_in_circulation 2025-11-01: international = Visa + MC + UnionPay | 56,363.4 | 56,213.0 | 150.4 | 0.27% |
| INFO-residual | 2025-11-01 | T1 cards_used 2024-11-01: international = Visa + MC + UnionPay | 23,771.9 | 23,726.9 | 45.0 | 0.19% |
| INFO-residual | 2025-11-01 | T1 cards_used 2025-11-01: international = Visa + MC + UnionPay | 24,569.0 | 24,520.2 | 48.8 | 0.20% |
| INFO-residual | 2025-11-01 | T4 txn_count cash_withdrawal 2024-10-31: international = Visa + MC + UnionPay | 140,118.9 | 139,884.0 | 234.9 | 0.17% |
| INFO-residual | 2025-11-01 | T4 txn_count cash_withdrawal 2025-10-31: international = Visa + MC + UnionPay | 127,243.2 | 127,095.4 | 147.8 | 0.12% |
| INFO-residual | 2025-11-01 | T4 txn_count cashless 2024-10-31: international = Visa + MC + UnionPay | 1,708,271.7 | 1,706,490.8 | 1,780.9 | 0.10% |
| INFO-residual | 2025-11-01 | T4 txn_count cashless 2025-10-31: international = Visa + MC + UnionPay | 1,930,944.3 | 1,928,001.1 | 2,943.2 | 0.15% |
| INFO-residual | 2025-11-01 | T4 txn_value cash_withdrawal 2024-10-31: international = Visa + MC + UnionPay | 15,904,645.1 | 15,881,715.8 | 22,929.3 | 0.14% |
| INFO-residual | 2025-11-01 | T4 txn_value cash_withdrawal 2025-10-31: international = Visa + MC + UnionPay | 16,478,380.5 | 16,459,611.6 | 18,768.9 | 0.11% |
| INFO-residual | 2025-11-01 | T4 txn_value cashless 2024-10-31: international = Visa + MC + UnionPay | 29,545,808.3 | 29,492,493.7 | 53,314.6 | 0.18% |
| INFO-residual | 2025-11-01 | T4 txn_value cashless 2025-10-31: international = Visa + MC + UnionPay | 36,917,186.1 | 36,838,186.2 | 78,999.9 | 0.21% |
| INFO-residual | 2025-12-01 | T1 cards_in_circulation 2024-12-01: international = Visa + MC + UnionPay | 53,832.3 | 53,717.7 | 114.6 | 0.21% |
| INFO-residual | 2025-12-01 | T1 cards_in_circulation 2025-12-01: international = Visa + MC + UnionPay | 56,457.6 | 56,308.3 | 149.3 | 0.26% |
| INFO-residual | 2025-12-01 | T1 cards_used 2024-12-01: international = Visa + MC + UnionPay | 23,731.3 | 23,686.8 | 44.5 | 0.19% |
| INFO-residual | 2025-12-01 | T1 cards_used 2025-12-01: international = Visa + MC + UnionPay | 24,170.8 | 24,123.2 | 47.6 | 0.20% |
| INFO-residual | 2025-12-01 | T4 txn_count cash_withdrawal 2024-11-30: international = Visa + MC + UnionPay | 153,126.7 | 152,874.9 | 251.8 | 0.16% |
| INFO-residual | 2025-12-01 | T4 txn_count cash_withdrawal 2025-11-30: international = Visa + MC + UnionPay | 138,892.7 | 138,728.0 | 164.7 | 0.12% |
| INFO-residual | 2025-12-01 | T4 txn_count cashless 2024-11-30: international = Visa + MC + UnionPay | 1,885,518.2 | 1,883,512.8 | 2,005.4 | 0.11% |
| INFO-residual | 2025-12-01 | T4 txn_count cashless 2025-11-30: international = Visa + MC + UnionPay | 2,131,013.2 | 2,127,763.3 | 3,249.9 | 0.15% |
| INFO-residual | 2025-12-01 | T4 txn_value cash_withdrawal 2024-11-30: international = Visa + MC + UnionPay | 17,578,380.1 | 17,553,565.8 | 24,814.3 | 0.14% |
| INFO-residual | 2025-12-01 | T4 txn_value cash_withdrawal 2025-11-30: international = Visa + MC + UnionPay | 18,005,718.2 | 17,984,590.5 | 21,127.7 | 0.12% |
| INFO-residual | 2025-12-01 | T4 txn_value cashless 2024-11-30: international = Visa + MC + UnionPay | 32,865,664.0 | 32,805,345.1 | 60,318.9 | 0.18% |
| INFO-residual | 2025-12-01 | T4 txn_value cashless 2025-11-30: international = Visa + MC + UnionPay | 40,764,543.2 | 40,677,418.4 | 87,124.8 | 0.21% |
| INFO-residual | 2026-01-01 | T1 cards_in_circulation 2025-01-01: international = Visa + MC + UnionPay | 54,625.5 | 54,504.7 | 120.8 | 0.22% |
| INFO-residual | 2026-01-01 | T1 cards_in_circulation 2026-01-01: international = Visa + MC + UnionPay | 56,547.2 | 56,400.0 | 147.2 | 0.26% |
| INFO-residual | 2026-01-01 | T1 cards_used 2025-01-01: international = Visa + MC + UnionPay | 24,161.8 | 24,115.1 | 46.7 | 0.19% |
| INFO-residual | 2026-01-01 | T1 cards_used 2026-01-01: international = Visa + MC + UnionPay | 25,127.2 | 25,079.2 | 48.0 | 0.19% |
| INFO-residual | 2026-01-01 | T4 txn_count cash_withdrawal 2024-12-31: international = Visa + MC + UnionPay | 167,454.7 | 167,185.5 | 269.2 | 0.16% |
| INFO-residual | 2026-01-01 | T4 txn_count cash_withdrawal 2025-12-31: international = Visa + MC + UnionPay | 151,913.7 | 151,731.8 | 181.9 | 0.12% |
| INFO-residual | 2026-01-01 | T4 txn_count cashless 2024-12-31: international = Visa + MC + UnionPay | 2,082,919.5 | 2,080,669.7 | 2,249.8 | 0.11% |
| INFO-residual | 2026-01-01 | T4 txn_count cashless 2025-12-31: international = Visa + MC + UnionPay | 2,346,217.1 | 2,342,662.6 | 3,554.5 | 0.15% |
| INFO-residual | 2026-01-01 | T4 txn_value cash_withdrawal 2024-12-31: international = Visa + MC + UnionPay | 19,502,438.7 | 19,475,546.9 | 26,891.8 | 0.14% |
| INFO-residual | 2026-01-01 | T4 txn_value cash_withdrawal 2025-12-31: international = Visa + MC + UnionPay | 19,882,652.7 | 19,859,095.1 | 23,557.6 | 0.12% |
| INFO-residual | 2026-01-01 | T4 txn_value cashless 2024-12-31: international = Visa + MC + UnionPay | 36,842,820.9 | 36,773,745.5 | 69,075.4 | 0.19% |
| INFO-residual | 2026-01-01 | T4 txn_value cashless 2025-12-31: international = Visa + MC + UnionPay | 45,406,215.3 | 45,309,724.3 | 96,491.0 | 0.21% |
| INFO-residual | 2026-02-01 | T1 cards_in_circulation 2025-02-01: international = Visa + MC + UnionPay | 56,745.0 | 56,619.9 | 125.1 | 0.22% |
| INFO-residual | 2026-02-01 | T1 cards_in_circulation 2026-02-01: international = Visa + MC + UnionPay | 56,930.6 | 56,783.7 | 146.9 | 0.26% |
| INFO-residual | 2026-02-01 | T1 cards_used 2025-02-01: international = Visa + MC + UnionPay | 24,776.9 | 24,732.8 | 44.1 | 0.18% |
| INFO-residual | 2026-02-01 | T1 cards_used 2026-02-01: international = Visa + MC + UnionPay | 24,113.6 | 24,069.0 | 44.6 | 0.18% |
| INFO-residual | 2026-02-01 | T4 txn_count cash_withdrawal 2025-01-31: international = Visa + MC + UnionPay | 11,577.0 | 11,564.7 | 12.3 | 0.11% |
| INFO-residual | 2026-02-01 | T4 txn_count cash_withdrawal 2026-01-31: international = Visa + MC + UnionPay | 10,421.7 | 10,407.4 | 14.3 | 0.14% |
| INFO-residual | 2026-02-01 | T4 txn_count cashless 2025-01-31: international = Visa + MC + UnionPay | 168,697.9 | 168,452.8 | 245.1 | 0.15% |
| INFO-residual | 2026-02-01 | T4 txn_count cashless 2026-01-31: international = Visa + MC + UnionPay | 188,200.5 | 187,946.1 | 254.4 | 0.14% |
| INFO-residual | 2026-02-01 | T4 txn_value cash_withdrawal 2025-01-31: international = Visa + MC + UnionPay | 1,419,080.9 | 1,417,637.3 | 1,443.6 | 0.10% |
| INFO-residual | 2026-02-01 | T4 txn_value cash_withdrawal 2026-01-31: international = Visa + MC + UnionPay | 1,304,162.3 | 1,302,328.4 | 1,833.9 | 0.14% |
| INFO-residual | 2026-02-01 | T4 txn_value cashless 2025-01-31: international = Visa + MC + UnionPay | 3,115,395.0 | 3,108,202.7 | 7,192.3 | 0.23% |
| INFO-residual | 2026-02-01 | T4 txn_value cashless 2026-01-31: international = Visa + MC + UnionPay | 3,524,033.3 | 3,517,107.0 | 6,926.3 | 0.20% |
| INFO-residual | 2026-03-01 | T1 cards_in_circulation 2025-03-01: international = Visa + MC + UnionPay | 54,109.9 | 53,986.8 | 123.1 | 0.23% |
| INFO-residual | 2026-03-01 | T1 cards_in_circulation 2026-03-01: international = Visa + MC + UnionPay | 56,847.7 | 56,703.2 | 144.5 | 0.25% |
| INFO-residual | 2026-03-01 | T1 cards_used 2025-03-01: international = Visa + MC + UnionPay | 25,112.7 | 25,069.9 | 42.8 | 0.17% |
| INFO-residual | 2026-03-01 | T1 cards_used 2026-03-01: international = Visa + MC + UnionPay | 24,280.8 | 24,236.5 | 44.3 | 0.18% |
| INFO-residual | 2026-03-01 | T4 txn_count cash_withdrawal 2025-02-28: international = Visa + MC + UnionPay | 23,603.5 | 23,578.8 | 24.7 | 0.10% |
| INFO-residual | 2026-03-01 | T4 txn_count cash_withdrawal 2026-02-28: international = Visa + MC + UnionPay | 21,186.0 | 21,156.4 | 29.6 | 0.14% |
| INFO-residual | 2026-03-01 | T4 txn_count cashless 2025-02-28: international = Visa + MC + UnionPay | 341,377.3 | 340,876.0 | 501.3 | 0.15% |
| INFO-residual | 2026-03-01 | T4 txn_count cashless 2026-02-28: international = Visa + MC + UnionPay | 374,552.3 | 374,051.4 | 500.9 | 0.13% |
| INFO-residual | 2026-03-01 | T4 txn_value cash_withdrawal 2025-02-28: international = Visa + MC + UnionPay | 2,908,801.0 | 2,905,846.6 | 2,954.4 | 0.10% |
| INFO-residual | 2026-03-01 | T4 txn_value cash_withdrawal 2026-02-28: international = Visa + MC + UnionPay | 2,671,796.9 | 2,667,751.4 | 4,045.5 | 0.15% |
| INFO-residual | 2026-03-01 | T4 txn_value cashless 2025-02-28: international = Visa + MC + UnionPay | 7,041,011.9 | 7,026,750.1 | 14,261.8 | 0.20% |
| INFO-residual | 2026-03-01 | T4 txn_value cashless 2026-02-28: international = Visa + MC + UnionPay | 7,139,530.6 | 7,124,941.2 | 14,589.4 | 0.20% |
| INFO-residual | 2026-04-01 | T1 cards_in_circulation 2025-04-01: international = Visa + MC + UnionPay | 54,767.2 | 54,641.1 | 126.1 | 0.23% |
| INFO-residual | 2026-04-01 | T1 cards_in_circulation 2026-04-01: international = Visa + MC + UnionPay | 56,854.4 | 56,710.4 | 144.0 | 0.25% |
| INFO-residual | 2026-04-01 | T1 cards_used 2025-04-01: international = Visa + MC + UnionPay | 25,697.6 | 25,653.3 | 44.3 | 0.17% |
| INFO-residual | 2026-04-01 | T1 cards_used 2026-04-01: international = Visa + MC + UnionPay | 24,829.7 | 24,784.9 | 44.8 | 0.18% |
| INFO-residual | 2026-04-01 | T4 txn_count cash_withdrawal 2025-03-31: international = Visa + MC + UnionPay | 36,585.3 | 36,546.2 | 39.1 | 0.11% |
| INFO-residual | 2026-04-01 | T4 txn_count cash_withdrawal 2026-03-31: international = Visa + MC + UnionPay | 32,846.4 | 32,800.3 | 46.1 | 0.14% |
| INFO-residual | 2026-04-01 | T4 txn_count cashless 2025-03-31: international = Visa + MC + UnionPay | 534,067.5 | 533,297.1 | 770.4 | 0.14% |
| INFO-residual | 2026-04-01 | T4 txn_count cashless 2026-03-31: international = Visa + MC + UnionPay | 578,543.9 | 577,759.9 | 784.0 | 0.14% |
| INFO-residual | 2026-04-01 | T4 txn_value cash_withdrawal 2025-03-31: international = Visa + MC + UnionPay | 4,451,042.2 | 4,446,208.9 | 4,833.3 | 0.11% |
| INFO-residual | 2026-04-01 | T4 txn_value cash_withdrawal 2026-03-31: international = Visa + MC + UnionPay | 4,105,728.6 | 4,099,504.6 | 6,224.0 | 0.15% |
| INFO-residual | 2026-04-01 | T4 txn_value cashless 2025-03-31: international = Visa + MC + UnionPay | 10,610,795.1 | 10,589,024.0 | 21,771.1 | 0.21% |
| INFO-residual | 2026-04-01 | T4 txn_value cashless 2026-03-31: international = Visa + MC + UnionPay | 11,033,229.8 | 11,010,839.6 | 22,390.2 | 0.20% |
| INFO-residual | 2026-05-01 | T1 cards_in_circulation 2025-05-01: international = Visa + MC + UnionPay | 54,004.4 | 53,874.3 | 130.1 | 0.24% |
| INFO-residual | 2026-05-01 | T1 cards_in_circulation 2026-05-01: international = Visa + MC + UnionPay | 56,628.2 | 56,486.1 | 142.1 | 0.25% |
| INFO-residual | 2026-05-01 | T1 cards_used 2025-05-01: international = Visa + MC + UnionPay | 24,567.4 | 24,522.3 | 45.1 | 0.18% |
| INFO-residual | 2026-05-01 | T1 cards_used 2026-05-01: international = Visa + MC + UnionPay | 24,750.2 | 24,706.1 | 44.1 | 0.18% |
| INFO-residual | 2026-05-01 | T4 txn_count cash_withdrawal 2025-04-30: international = Visa + MC + UnionPay | 49,685.6 | 49,632.6 | 53.0 | 0.11% |
| INFO-residual | 2026-05-01 | T4 txn_count cash_withdrawal 2026-04-30: international = Visa + MC + UnionPay | 44,409.8 | 44,346.8 | 63.0 | 0.14% |
| INFO-residual | 2026-05-01 | T4 txn_count cashless 2025-04-30: international = Visa + MC + UnionPay | 727,229.9 | 726,178.6 | 1,051.3 | 0.14% |
| INFO-residual | 2026-05-01 | T4 txn_count cashless 2026-04-30: international = Visa + MC + UnionPay | 778,947.3 | 777,889.5 | 1,057.8 | 0.14% |
| INFO-residual | 2026-05-01 | T4 txn_value cash_withdrawal 2025-04-30: international = Visa + MC + UnionPay | 6,128,182.5 | 6,121,556.5 | 6,626.0 | 0.11% |
| INFO-residual | 2026-05-01 | T4 txn_value cash_withdrawal 2026-04-30: international = Visa + MC + UnionPay | 5,622,906.9 | 5,614,132.7 | 8,774.2 | 0.16% |
| INFO-residual | 2026-05-01 | T4 txn_value cashless 2025-04-30: international = Visa + MC + UnionPay | 14,164,647.0 | 14,135,227.1 | 29,419.9 | 0.21% |
| INFO-residual | 2026-05-01 | T4 txn_value cashless 2026-04-30: international = Visa + MC + UnionPay | 14,942,366.2 | 14,912,623.5 | 29,742.7 | 0.20% |
| INFO-residual | 2026-06-01 | T1 cards_in_circulation 2025-06-01: international = Visa + MC + UnionPay | 53,968.7 | 53,834.5 | 134.2 | 0.25% |
| INFO-residual | 2026-06-01 | T1 cards_in_circulation 2026-06-01: international = Visa + MC + UnionPay | 55,637.1 | 55,496.3 | 140.8 | 0.25% |
| INFO-residual | 2026-06-01 | T1 cards_used 2025-06-01: international = Visa + MC + UnionPay | 24,298.7 | 24,253.1 | 45.6 | 0.19% |
| INFO-residual | 2026-06-01 | T1 cards_used 2026-06-01: international = Visa + MC + UnionPay | 24,830.1 | 24,786.9 | 43.2 | 0.17% |
| INFO-residual | 2026-06-01 | T4 txn_count cash_withdrawal 2025-05-31: international = Visa + MC + UnionPay | 63,120.0 | 63,052.9 | 67.1 | 0.11% |
| INFO-residual | 2026-06-01 | T4 txn_count cash_withdrawal 2026-05-31: international = Visa + MC + UnionPay | 56,030.9 | 55,952.5 | 78.5 | 0.14% |
| INFO-residual | 2026-06-01 | T4 txn_count cashless 2025-05-31: international = Visa + MC + UnionPay | 928,642.6 | 927,295.8 | 1,346.8 | 0.15% |
| INFO-residual | 2026-06-01 | T4 txn_count cashless 2026-05-31: international = Visa + MC + UnionPay | 985,079.8 | 983,748.0 | 1,331.9 | 0.14% |
| INFO-residual | 2026-06-01 | T4 txn_value cash_withdrawal 2025-05-31: international = Visa + MC + UnionPay | 7,823,268.5 | 7,814,969.8 | 8,298.7 | 0.11% |
| INFO-residual | 2026-06-01 | T4 txn_value cash_withdrawal 2026-05-31: international = Visa + MC + UnionPay | 7,103,442.9 | 7,092,470.1 | 10,972.8 | 0.15% |
| INFO-residual | 2026-06-01 | T4 txn_value cashless 2025-05-31: international = Visa + MC + UnionPay | 17,801,358.9 | 17,764,243.4 | 37,115.5 | 0.21% |
| INFO-residual | 2026-06-01 | T4 txn_value cashless 2026-05-31: international = Visa + MC + UnionPay | 18,926,524.3 | 18,889,540.1 | 36,984.2 | 0.20% |
| INFO-residual | 2026-07-01 | T1 cards_in_circulation 2025-07-01: international = Visa + MC + UnionPay | 54,367.7 | 54,228.1 | 139.6 | 0.26% |
| INFO-residual | 2026-07-01 | T1 cards_in_circulation 2026-07-01: international = Visa + MC + UnionPay | 55,321.5 | 55,181.3 | 140.2 | 0.25% |
| INFO-residual | 2026-07-01 | T1 cards_used 2025-07-01: international = Visa + MC + UnionPay | 24,270.0 | 24,222.4 | 47.6 | 0.20% |
| INFO-residual | 2026-07-01 | T1 cards_used 2026-07-01: international = Visa + MC + UnionPay | 24,437.9 | 24,395.1 | 42.8 | 0.18% |
| INFO-residual | 2026-07-01 | T4 txn_count cash_withdrawal 2025-06-30: international = Visa + MC + UnionPay | 76,478.5 | 76,397.4 | 81.1 | 0.11% |
| INFO-residual | 2026-07-01 | T4 txn_count cash_withdrawal 2026-06-30: international = Visa + MC + UnionPay | 67,804.2 | 67,710.2 | 94.0 | 0.14% |
| INFO-residual | 2026-07-01 | T4 txn_count cashless 2025-06-30: international = Visa + MC + UnionPay | 1,126,330.6 | 1,124,677.8 | 1,652.8 | 0.15% |
| INFO-residual | 2026-07-01 | T4 txn_count cashless 2026-06-30: international = Visa + MC + UnionPay | 1,191,174.6 | 1,189,576.7 | 1,597.9 | 0.13% |
| INFO-residual | 2026-07-01 | T4 txn_value cash_withdrawal 2025-06-30: international = Visa + MC + UnionPay | 9,592,734.7 | 9,582,608.7 | 10,126.0 | 0.11% |
| INFO-residual | 2026-07-01 | T4 txn_value cash_withdrawal 2026-06-30: international = Visa + MC + UnionPay | 8,744,220.1 | 8,730,975.2 | 13,244.9 | 0.15% |
| INFO-residual | 2026-07-01 | T4 txn_value cashless 2025-06-30: international = Visa + MC + UnionPay | 21,534,922.1 | 21,489,712.6 | 45,209.5 | 0.21% |
| INFO-residual | 2026-07-01 | T4 txn_value cashless 2026-06-30: international = Visa + MC + UnionPay | 23,239,426.1 | 23,195,076.0 | 44,350.1 | 0.19% |
| INFO-residual | 2026-08-01 | T1 cards_in_circulation 2025-08-01: international = Visa + MC + UnionPay | 54,482.3 | 54,335.9 | 146.4 | 0.27% |
| INFO-residual | 2026-08-01 | T1 cards_in_circulation 2026-08-01: international = Visa + MC + UnionPay | 55,623.5 | 55,482.7 | 140.8 | 0.25% |
| INFO-residual | 2026-08-01 | T1 cards_used 2025-08-01: international = Visa + MC + UnionPay | 23,479.3 | 23,429.0 | 50.3 | 0.21% |
| INFO-residual | 2026-08-01 | T1 cards_used 2026-08-01: international = Visa + MC + UnionPay | 23,259.4 | 23,217.8 | 41.6 | 0.18% |
| INFO-residual | 2026-08-01 | T4 txn_count cash_withdrawal 2025-07-31: international = Visa + MC + UnionPay | 89,465.9 | 89,369.2 | 96.7 | 0.11% |
| INFO-residual | 2026-08-01 | T4 txn_count cash_withdrawal 2026-07-31: international = Visa + MC + UnionPay | 79,165.4 | 79,056.6 | 108.8 | 0.14% |
| INFO-residual | 2026-08-01 | T4 txn_count cashless 2025-07-31: international = Visa + MC + UnionPay | 1,326,781.6 | 1,324,809.6 | 1,972.0 | 0.15% |
| INFO-residual | 2026-08-01 | T4 txn_count cashless 2026-07-31: international = Visa + MC + UnionPay | 1,424,860.3 | 1,423,000.3 | 1,860.1 | 0.13% |
| INFO-residual | 2026-08-01 | T4 txn_value cash_withdrawal 2025-07-31: international = Visa + MC + UnionPay | 11,383,828.0 | 11,371,612.0 | 12,216.0 | 0.11% |
| INFO-residual | 2026-08-01 | T4 txn_value cash_withdrawal 2026-07-31: international = Visa + MC + UnionPay | 10,312,367.8 | 10,296,885.8 | 15,482.0 | 0.15% |
| INFO-residual | 2026-08-01 | T4 txn_value cashless 2025-07-31: international = Visa + MC + UnionPay | 25,348,652.2 | 25,294,922.8 | 53,729.4 | 0.21% |
| INFO-residual | 2026-08-01 | T4 txn_value cashless 2026-07-31: international = Visa + MC + UnionPay | 27,614,727.9 | 27,563,314.6 | 51,413.3 | 0.19% |
| INFO-residual | 2026-09-01 | T1 cards_in_circulation 2026-09-01: international = Visa + MC + UnionPay | 55,889.5 | 55,820.5 | 69.0 | 0.12% |
| INFO-residual | 2026-09-01 | T1 cards_used 2025-09-01: international = Visa + MC + UnionPay | 24,156.7 | 24,104.9 | 51.8 | 0.21% |
| INFO-residual | 2026-09-01 | T1 cards_used 2026-09-01: international = Visa + MC + UnionPay | 24,335.9 | 24,291.2 | 44.7 | 0.18% |
| INFO-residual | 2026-09-01 | T4 txn_count cash_withdrawal 2025-08-31: international = Visa + MC + UnionPay | 102,483.1 | 102,369.5 | 113.6 | 0.11% |
| INFO-residual | 2026-09-01 | T4 txn_count cash_withdrawal 2026-08-31: international = Visa + MC + UnionPay | 90,176.9 | 90,052.7 | 124.2 | 0.14% |
| INFO-residual | 2026-09-01 | T4 txn_count cashless 2025-08-31: international = Visa + MC + UnionPay | 1,527,449.0 | 1,525,149.7 | 2,299.3 | 0.15% |
| INFO-residual | 2026-09-01 | T4 txn_count cashless 2026-08-31: international = Visa + MC + UnionPay | 1,660,845.4 | 1,658,718.1 | 2,127.3 | 0.13% |
| INFO-residual | 2026-09-01 | T4 txn_value cash_withdrawal 2025-08-31: international = Visa + MC + UnionPay | 13,174,412.4 | 13,160,094.6 | 14,317.8 | 0.11% |
| INFO-residual | 2026-09-01 | T4 txn_value cash_withdrawal 2026-08-31: international = Visa + MC + UnionPay | 11,836,013.9 | 11,818,191.9 | 17,822.0 | 0.15% |
| INFO-residual | 2026-09-01 | T4 txn_value cashless 2025-08-31: international = Visa + MC + UnionPay | 28,546,949.7 | 28,484,753.0 | 62,196.7 | 0.22% |
| INFO-residual | 2026-09-01 | T4 txn_value cashless 2026-08-31: international = Visa + MC + UnionPay | 31,888,173.4 | 31,828,570.4 | 59,603.0 | 0.19% |
| INFO-residual | 2026-10-01 | T1 cards_in_circulation 2025-10-01: international = Visa + MC + UnionPay | 55,291.5 | 55,140.4 | 151.1 | 0.27% |
| INFO-residual | 2026-10-01 | T1 cards_in_circulation 2026-10-01: international = Visa + MC + UnionPay | 56,919.9 | 56,770.1 | 149.8 | 0.26% |
| INFO-residual | 2026-10-01 | T1 cards_used 2025-10-01: international = Visa + MC + UnionPay | 24,258.6 | 24,207.0 | 51.6 | 0.21% |
| INFO-residual | 2026-10-01 | T1 cards_used 2026-10-01: international = Visa + MC + UnionPay | 24,590.7 | 24,544.2 | 46.5 | 0.19% |
| INFO-residual | 2026-10-01 | T4 txn_count cash_withdrawal 2025-09-30: international = Visa + MC + UnionPay | 114,428.4 | 114,297.7 | 130.7 | 0.11% |
| INFO-residual | 2026-10-01 | T4 txn_count cash_withdrawal 2026-09-30: international = Visa + MC + UnionPay | 100,451.6 | 100,312.3 | 139.3 | 0.14% |
| INFO-residual | 2026-10-01 | T4 txn_count cashless 2025-09-30: international = Visa + MC + UnionPay | 1,721,979.5 | 1,719,357.8 | 2,621.7 | 0.15% |
| INFO-residual | 2026-10-01 | T4 txn_count cashless 2026-09-30: international = Visa + MC + UnionPay | 1,937,190.9 | 1,934,790.6 | 2,400.3 | 0.12% |
| INFO-residual | 2026-10-01 | T4 txn_value cash_withdrawal 2025-09-30: international = Visa + MC + UnionPay | 14,808,090.2 | 14,791,596.3 | 16,493.9 | 0.11% |
| INFO-residual | 2026-10-01 | T4 txn_value cash_withdrawal 2026-09-30: international = Visa + MC + UnionPay | 13,296,433.5 | 13,276,301.5 | 20,132.0 | 0.15% |
| INFO-residual | 2026-10-01 | T4 txn_value cashless 2025-09-30: international = Visa + MC + UnionPay | 32,245,868.9 | 32,175,355.6 | 70,513.3 | 0.22% |
| INFO-residual | 2026-10-01 | T4 txn_value cashless 2026-09-30: international = Visa + MC + UnionPay | 36,281,785.6 | 36,214,071.8 | 67,713.8 | 0.19% |
| INFO-scope | 2025-11-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 22,488,562.2 | 22,460,968.0 | 27,594.2 | 0.12% |
| INFO-scope | 2025-12-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 24,647,435.5 | 24,618,716.7 | 28,718.8 | 0.12% |
| INFO-scope | 2026-01-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 232,527.0 | 233,922.6 | -1,395.6 | 0.60% |
| INFO-scope | 2026-01-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 27,239,535.5 | 27,290,291.0 | -50,755.5 | 0.19% |
| INFO-scope | 2026-02-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 16,543.5 | 17,561.1 | -1,017.6 | 6.15% |
| INFO-scope | 2026-02-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 1,847,191.2 | 1,892,236.9 | -45,045.7 | 2.44% |
| INFO-scope | 2026-02-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 13,433,410.9 | 13,388,378.8 | 45,032.1 | 0.34% |
| INFO-scope | 2026-03-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 33,435.1 | 35,553.2 | -2,118.1 | 6.33% |
| INFO-scope | 2026-03-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 2,055,507.2 | 2,053,389.3 | 2,117.9 | 0.10% |
| INFO-scope | 2026-03-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 3,765,089.3 | 3,860,897.7 | -95,808.4 | 2.54% |
| INFO-scope | 2026-03-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 27,102,094.7 | 27,006,311.6 | 95,783.1 | 0.35% |
| INFO-scope | 2026-04-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 52,223.8 | 55,636.6 | -3,412.8 | 6.53% |
| INFO-scope | 2026-04-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 3,216,591.4 | 3,213,178.7 | 3,412.7 | 0.11% |
| INFO-scope | 2026-04-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 5,826,823.2 | 5,973,937.0 | -147,113.8 | 2.52% |
| INFO-scope | 2026-04-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 42,351,866.0 | 42,204,777.5 | 147,088.5 | 0.35% |
| INFO-scope | 2026-05-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 71,164.2 | 75,820.9 | -4,656.7 | 6.54% |
| INFO-scope | 2026-05-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 4,435,733.0 | 4,416,588.3 | 19,144.7 | 0.43% |
| INFO-scope | 2026-05-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 8,011,418.2 | 8,195,127.2 | -183,709.0 | 2.29% |
| INFO-scope | 2026-05-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 57,842,483.3 | 57,477,255.5 | 365,227.8 | 0.63% |
| INFO-scope | 2026-06-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 90,412.6 | 96,359.0 | -5,946.4 | 6.58% |
| INFO-scope | 2026-06-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 5,708,041.7 | 5,687,607.3 | 20,434.4 | 0.36% |
| INFO-scope | 2026-06-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 10,178,393.7 | 10,413,161.3 | -234,767.6 | 2.31% |
| INFO-scope | 2026-06-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 73,933,578.3 | 73,517,291.8 | 416,286.5 | 0.56% |
| INFO-scope | 2026-07-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 109,882.3 | 117,157.2 | -7,274.9 | 6.62% |
| INFO-scope | 2026-07-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 6,974,010.1 | 6,952,247.2 | 21,762.9 | 0.31% |
| INFO-scope | 2026-07-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 12,559,497.6 | 12,850,307.6 | -290,810.0 | 2.32% |
| INFO-scope | 2026-07-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 91,238,400.6 | 90,766,071.7 | 472,328.9 | 0.52% |
| INFO-scope | 2026-08-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 128,791.1 | 137,370.8 | -8,579.7 | 6.66% |
| INFO-scope | 2026-08-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 8,247,106.8 | 8,224,039.0 | 23,067.8 | 0.28% |
| INFO-scope | 2026-08-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 14,858,786.3 | 15,199,943.1 | -341,156.8 | 2.30% |
| INFO-scope | 2026-08-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 108,618,526.5 | 108,095,850.8 | 522,675.7 | 0.48% |
| INFO-scope | 2026-09-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 147,595.0 | 156,174.5 | -8,579.5 | 5.81% |
| INFO-scope | 2026-09-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 9,538,682.4 | 9,515,614.8 | 23,067.6 | 0.24% |
| INFO-scope | 2026-09-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 17,131,382.9 | 17,469,342.1 | -337,959.2 | 1.97% |
| INFO-scope | 2026-09-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 126,266,263.5 | 125,746,785.4 | 519,478.1 | 0.41% |
| INFO-scope | 2026-10-01 | T5 vs T6 txn_count cash_withdrawal: same scope (in KZ, all issuers) | 165,039.9 | 173,619.1 | -8,579.2 | 5.20% |
| INFO-scope | 2026-10-01 | T5 vs T6 txn_count cashless: same scope (in KZ, all issuers) | 10,812,263.3 | 10,789,558.6 | 22,704.7 | 0.21% |
| INFO-scope | 2026-10-01 | T5 vs T6 txn_value cash_withdrawal: same scope (in KZ, all issuers) | 19,296,449.6 | 19,633,788.5 | -337,338.9 | 1.75% |
| INFO-scope | 2026-10-01 | T5 vs T6 txn_value cashless: same scope (in KZ, all issuers) | 142,914,695.2 | 142,405,352.9 | 509,342.3 | 0.36% |

## Known header issues (handled by taking as-of date from narrative text)

* Release v269 (as of 2026-02-01): Table 1 header reads 01.01.2025 / 01.01.2026.
* Release v277 (as of 2026-10-01): Table 2 header reads 'As of 01.10.2025' but totals match Table 1's 2026 column.
* Releases before v266 (as of 2025-11-01) do not break out UnionPay; `other_international` = international - Visa - MasterCard is derived [calc] in analysis.