# Progress log (append-only; ≤5 lines per phase)

## Phase 1 — Data acquisition (done 2026-11-18)
- NBK: 30 monthly releases (v248–v277, as of 2024-05-01 → 2026-10-01) scraped to `data/raw/nbk/`, parsed to `data/clean/nbk_cards_long.csv` (12.3k rows, latest vintage) + all-vintage file.
- Validation: 1,832 checks, 16 ERROR (two NBK source errors: v263 T1 row-shift → excluded; v250 2023 T4 → flagged), 182 INFO (UnionPay residual, T5/T6 scope) → `docs/validation_nbk.md`.
- Kaspi 20-F FY2023/24/25: 72 rows incl. quote-verified page refs → `data/clean/kaspi_kpis.csv`. Key: TPV FY25 ₸44,219bn, take rate 1.10%, QR "eliminates interchange" (p105).
- Population by region (stat.gov.kz, 2026-10-01) → `data/clean/population_by_region.csv`. Gaps → `docs/data_gaps.md`.

## Phase 2 — Hypothesis tree (done 2026-11-18)
- `docs/hypothesis_tree.md`: governing Q → day-1 answer → H1 (activation **+ cash usage**, refined), H2 (cross-border/CNP; credit tested separately), H3 (closed-loop level **and trend**).
- 16 tests with confirm/kill thresholds; integrity note: thresholds fixed after profiling, before analysis/charts.
- Profiling signals: international share of KZ-issued cashless value rising; ~92% of credit cards on local system [calc]; intl cards carry ~68% of cash-withdrawal value.

## Phase 3 — Analysis (done 2026-11-18)
- Modules: `src/analysis/{market_structure,h1_activation,h2_niches,h3_closed_loop}.py`, run all via `python -m src.analysis.run_all`; 12 charts in `outputs/charts/`, 200 labelled metrics in `outputs/metrics.csv`.
- Verdicts: H1 Partially (32.3m dormant intl cards, intl = 68% of cash withdrawals; uplift +6.6% base [est]); H2 Partially (outbound CNP +25.6% vs domestic +5.8%; credit killed: intl 7.8%); H3 Killed as stated (local share 77% but −1.4pp YoY; QR in-store flat ~52%).
- `outputs/findings.md` written with source keys (release URL + table + as-of) for every number.

## Phase 4 — Storyline & defence (done 2026-11-18)
- `outputs/storyline.md`: 10-slide pyramid (answer → A closed loop stalled / B idle wallets / C cross-border niche → 3 recs with Impact×Effort + NBK KPIs) + 4 backup charts.
- `outputs/interview_defense.md`: 10 hardest Qs (Kaspi attribution, 'used' definition, short trend, causality, Kaspi counter-moves, regulator, revenue, bypass assumption, inbound residual, credit) + "must not say" list.

## Phase 5 — Deck (done 2026-11-18)
- `src/deck/build_deck.py` parses `outputs/storyline.md` → `outputs/kz_payments_strategy.pptx` (10 body + 4 backup slides, 16:9, accent #1F4E9E, title top-left, source bottom-left, page numbers).
- Rendered via Keynote AppleScript (bundle id com.apple.Keynote) to `outputs/render/render.0NN.png`; checked all 14: fixed table row heights, bullet-box sizing, stray markdown asterisks. No overflow/overlap remaining.

## Phase 6 — Repo (done 2026-11-18)
- `git init` (branch main, repo-local author config), `.gitignore`, consulting-structure `README.md`, `requirements.txt`; single commit `feat: KZ payments network strategy analysis`. Not pushed.
- Resume: all phases complete. To refresh with a new NBK release: rerun the 'How to reproduce' block in README.
