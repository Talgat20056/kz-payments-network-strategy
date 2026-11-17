# Data gaps & source issues

Logged as encountered. Each item: what is missing / wrong -> how it is handled -> what would close it.

## Source A — NBK payment-card releases
1. **Release v263 (as of 2025-08-01), Table 1 is row-shifted in the source HTML** (e.g. the 'local systems' row holds the grand total 81,928.5). -> Table 1 of that release excluded (`EXCLUDE` in `src/acquire/nbk_parse.py`). Both dates it covers (2024-08-01, 2025-08-01) are available from other releases (v251 current column, v275 comparison column). Close: none needed.
2. **Release v250 (as of 2024-07-01), Table 4, 2023 H1 txn value block is internally inconsistent** (local + international exceeds total by 23%). -> rows kept with `quality_flag`; 2023 flows are outside the analysis window. Close: Russian-language release or NBK statistical bulletin for 2023.
3. **Header date typos** (v269 Table 1 says 01.01 for a 01.02 release; v277 Table 2 says 2025 for 2026 data). -> as-of date taken from the release narrative, cross-checked against Table 1 totals.
4. **UnionPay not broken out before v266 (as of 2025-11-01)**; and international > Visa + MC + UnionPay by 0.1-0.3% in every later release. -> residual reported as `other_international` [calc]; never attributed to a named scheme.
5. **Local system not named per row.** NBK narrative states the local system is Kaspi.kz ("payment cards of the local system Kaspi.kz"), but tables say only "local systems". -> We label it "local systems (Kaspi.kz per NBK narrative)" and do NOT claim 100% of it is Kaspi.
6. **No scheme split for POS / QR / e-commerce channels** (Table 6 is by channel, Table 4 by scheme; no cross-tab). -> scheme share *by channel* is not observable; the H3 bypass share is therefore an [estimate] with a stated formula and low/base/high range. Close: NBK payment-system statistics (ru `/ru/page/payment-systems`) or a Visa/MC internal BIN-level dataset.
7. **Internet & mobile channel mixes purchases and P2P transfers.** -> e-commerce (card-not-present purchase) value is not separable; we do not report an "e-commerce market size". Close: NBK e-commerce statistics, or Kaspi marketplace GMV as a partial proxy.
8. **Foreign cards used in Kazakhstan are not reported directly or by scheme.** -> derived as Table 6 total − (Table 4 total − Table 7 total) [calc]; no scheme split possible. Close: Visa/MC inbound cross-border data; tourism arrivals (stat.gov.kz).
9. **Table 5 (by region) vs Table 6 (by channel) totals differ by up to ~0.3%** despite the same stated scope. -> never mixed in one ratio.
10. **Small revisions between vintages** (e.g. Jan–Sep 2025 cashless value 136,518,314 mln KZT in v265 vs 136,640,440 in v277, +0.09%). -> latest vintage used by default; all vintages kept in `nbk_cards_long_allvintages.csv`.
11. **"Used cards" definition is not given in the release** (presumably ≥1 transaction in the reporting month). -> activation ratio is reported as NBK-defined "used ÷ in circulation"; interview defence notes the definitional risk.
12. Russian-language index has the same releases (~28 pages); **no xlsx/downloadable files were found** on the release pages — HTML tables are the only machine-readable format.

## Source B — Kaspi.kz Form 20-F
13. **TPV definition is ambiguous**: "excluding free P2P and QR payments" (FY2025 20-F, p8) while 69% of TPV is "payments through Kaspi QR and card transactions" (p92). -> we read the exclusion as applying to *free* P2P only and flag this; Kaspi QR+card TPV = 69% × TPV is labelled [calc] with ±0.5pp rounding band.
14. **No split of Kaspi QR vs Kaspi Gold card**, and no split of on-us vs off-us (Visa/MC) card transactions. -> cannot say what share of Kaspi TPV touches international rails; the 20-F only says other cards' volumes in Kaspi POS are "significantly lower" (p91). Close: Kaspi investor-day materials / management Q&A.
15. Kaspi TPV is *annual, by fiscal year*; NBK is monthly YTD. -> comparisons are made on full calendar years 2024 and 2025 only.
16. FY2023 20-F printed page numbers not detected by the text extractor; PDF page index is authoritative for all rows.

## Source C — Population (stat.gov.kz)
17. **Unit not stated in `Population by region.xlsx`**; inferred as thousand persons from magnitude (total 20,633.5 → 20.6 mln [calc]).
18. Population is as of 2026-10-01 only; per-capita metrics for earlier periods use this single denominator ([estimate]: population change < 2%/yr assumed immaterial).

## Not attempted / out of scope
* Visa / Mastercard issuer-level data, interchange rate tables, acquirer MDR — not public at the needed granularity.
* Tourism inbound statistics (would size inbound cross-border opportunity).
