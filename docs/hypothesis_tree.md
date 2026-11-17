# Hypothesis tree

**Governing question.** Where should an international card network (Visa / Mastercard) invest in Kazakhstan in 2027–2029 to grow, given Kaspi.kz's closed-loop dominance?

**Day-1 answer (to be proven or killed).** Networks should put money where the closed loop is structurally weak — **cross-border (outbound card-not-present and inbound acceptance)** and **turning the large, cash-heavy, under-used international card base into everyday spend** with non-Kaspi issuers — and should *not* fund a head-on fight for domestic QR / P2P, where Kaspi's share is very large but (to be tested) no longer expanding.

> Integrity note: thresholds below were fixed after a profiling pass of the cleaned data (structure, coverage, a handful of headline totals) and before any Phase 3 analysis or chart. They are conventional cut-offs, stated so a reviewer can disagree with them explicitly. Where the profiling pass already contradicted a starting hypothesis, the hypothesis was refined and the original wording kept for transparency.

```
Governing question
├── H1  Activation & usage: the installed international card base is under-used
│       (dormant + cash-only), and fixing usage is the biggest near-term lever
├── H2  Defensible niches: networks' structural advantage is in cross-border and
│       card-not-present, where closed-loop QR is weakest (credit tested separately)
└── H3  Domestic erosion: Kaspi's closed loop captures a large AND growing share of
        domestic cashless value that bypasses international rails
```

MECE logic: H1 = *existing* cardholders' behaviour (supply already in market); H2 = *use cases* the closed loop cannot reach; H3 = *the contested core* (domestic purchases and transfers). Together they cover where network volume can come from: more use of existing cards, new use cases, or share in the core.

---

## H1 — Activation & usage
*Starting wording:* "A large dormant card pool exists; activating it is the biggest near-term lever for networks/issuers."
*Refined wording:* "A large dormant international card pool exists **and active international cards are disproportionately used for cash**; activation + cash-to-cashless conversion is the biggest near-term lever." (Refined because profiling showed international cards carry most cash withdrawals.)

| # | Test (metric) | Source | Confirm if | Kill if |
|---|---|---|---|---|
| H1a | Dormant international cards = international in circulation − international used | NBK T1 | ≥ 40% of international cards dormant at 2026-10-01 | < 25% |
| H1b | Trend of activation ratio (used ÷ in circulation), international, 24 months | NBK T1 | flat or falling (≤ +1pp over 24m) → gap not self-correcting | rising ≥ 3pp |
| H1c | Activation gap: local vs international | NBK T1 | local − international ≥ 10pp | gap < 5pp |
| H1d | Cash-withdrawal share of card value: international vs local cards | NBK T4 | international ≥ 2× local | ratio < 1.3× |
| H1e | Sizing [estimate]: cashless value from lifting dormant/cash usage vs other levers | NBK T1, T4 | ≥ 10% uplift to international cashless value under base assumptions | < 5% |

## H2 — Defensible niches
*Starting wording:* "Networks' structural advantage is in cross-border, e-commerce/card-not-present, and credit — where closed-loop QR is weakest."

| # | Test (metric) | Source | Confirm if | Kill if |
|---|---|---|---|---|
| H2a | Outbound: KZ-issued card cashless value **outside** KZ, growth vs domestic cashless growth | NBK T7, T4 | outbound growth ≥ 1.5× domestic growth (FY2025 and YTD 2026) | ≤ 1.0× |
| H2b | Outbound CNP: internet & mobile channel abroad, growth and share of outbound | NBK T7 | CNP is the largest and fastest-growing outbound channel | POS abroad growing faster |
| H2c | Inbound: foreign-issued card value in KZ = T6 total − (T4 total − T7 total) [calc] | NBK T4, T6, T7 | positive and growing; documented closed-loop competition (Alipay+ via Kaspi QR) noted | n/a (sizing) |
| H2d | Credit: international schemes' share of credit cards in circulation | NBK T1, T2 | ≥ 25% (a real foothold to defend) | < 10% (Kaspi/local owns credit) |
| H2e | Domestic e-commerce (CNP) separable from P2P in NBK data? | NBK T6 | separable → size it | not separable → logged as data gap, no claim |

## H3 — Domestic erosion by the closed loop
*Starting wording:* "Kaspi's closed loop captures a growing share of domestic cashless value that bypasses international rails."

| # | Test (metric) | Source | Confirm if | Kill if |
|---|---|---|---|---|
| H3a | Level: local-system share of KZ-issued **domestic** cashless value = (T4 local) ÷ (T4 total − T7 total) [calc; assumes local cards are not used abroad] | NBK T4, T7 | ≥ 60% | < 40% |
| H3b | Trend: change in that share, same YTD period YoY and FY2024→FY2025 | NBK T4, T7 | rising ≥ 1pp/yr | flat (±1pp) or falling |
| H3c | In-store: QR share of (POS + QR) value in KZ, trend | NBK T6 | rising ≥ 1pp/yr | flat or falling |
| H3d | Kaspi scale vs market: Kaspi TPV ÷ NBK cashless card value; Kaspi QR+card TPV [calc] ÷ NBK (POS + QR) | Kaspi 20-F p92; NBK T4, T6 | consistent with H3a level | contradicts it |
| H3e | In-store bypass share [estimate] = (QR × q + POS × s) ÷ (POS + QR) with low/base/high on s, q | NBK T6 + assumptions | base ≥ 60% | base < 40% |
| H3f | Kaspi's stated intent to move volume off networks | Kaspi 20-F FY2023–25 (p109/p105/p105) | explicit statement exists | absent |

---

## What would change the answer
* If H3 is confirmed on **trend** (closed loop still gaining), networks should treat domestic volume as a melting asset and shift budget even harder into H2.
* If H1 is killed (activation already rising), the near-term lever is acceptance/use-case expansion rather than issuer incentives.
* If H2d is confirmed (networks hold credit), a credit/BNPL-on-card play would rank above activation.
