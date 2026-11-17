"""H3 — Domestic erosion by the closed loop. Output 6 (Kaspi vs networks, bypass estimate with sensitivity).

Charts: 10_closed_loop_share.png, 11_qr_vs_pos.png, 12_bypass_estimate.png
"""
from __future__ import annotations

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.common import (ACCENT, DARK, GREY, LIGHT, RED, ROOT, Metrics, finish, full_year, kaspi, monthly_from_ytd,
                                 nbk, new_fig, pct, pd, src_kaspi, src_nbk, to_month_start, ytd)

M = Metrics("h3_closed_loop")
d = nbk()
k = kaspi()
E25, E26 = pd.Timestamp("2025-09-30"), pd.Timestamp("2026-09-30")
S_47 = src_nbk("Tables 4 & 7 (YTD, mln KZT)", "Jan 2024 – Sep 2026",
               "Domestic = T4 − T7; local share = T4 local ÷ (T4 total − T7 total) [calc]; assumes local-system cards are not used abroad.")
S_6 = src_nbk("Table 6 (cards of KZ and foreign banks used in KZ, by environment; YTD, mln KZT)", "Jan 2024 – Sep 2026")


def periods(s):
    return {"FY2024": full_year(s, 2024), "FY2025": full_year(s, 2025), "YTD Sep 2025": s.get(E25), "YTD Sep 2026": s.get(E26)}


# ---------------- H3a/b: local-system share of domestic cashless value ----------------
loc = ytd(d, "T4", "txn_value", "cashless", scheme="local")
tot = ytd(d, "T4", "txn_value", "cashless", scheme="total")
ab = ytd(d, "T7", "txn_value", "cashless", channel="TOTAL")
P = {n: periods(s) for n, s in [("loc", loc), ("tot", tot), ("ab", ab)]}
share = {p: pct(P["loc"][p], P["tot"][p] - P["ab"][p]) for p in P["loc"]}
for p, v in share.items():
    M.add(f"local_share_domestic_{p.replace(' ', '')}", v, "% of KZ-card domestic cashless value", "calc", S_47)
M.add("local_share_change_FY24_FY25_pp", share["FY2025"] - share["FY2024"], "pp", "calc", S_47)
M.add("local_share_change_YTD_pp", share["YTD Sep 2026"] - share["YTD Sep 2025"], "pp", "calc", S_47)
growth_loc = pct(P["loc"]["YTD Sep 2026"], P["loc"]["YTD Sep 2025"]) - 100
growth_intl_dom = pct(P["tot"]["YTD Sep 2026"] - P["ab"]["YTD Sep 2026"] - P["loc"]["YTD Sep 2026"],
                      P["tot"]["YTD Sep 2025"] - P["ab"]["YTD Sep 2025"] - P["loc"]["YTD Sep 2025"]) - 100
M.add("growth_local_cashless_YTD2026", growth_loc, "% YoY", "calc", S_47)
M.add("growth_intl_domestic_cashless_YTD2026", growth_intl_dom, "% YoY", "calc", S_47)

ml, mt_, ma = monthly_from_ytd(loc), monthly_from_ytd(tot), monthly_from_ytd(ab)
ms = (100 * ml / (mt_ - ma)).dropna()
ms = ms[(ms.index >= "2024-10-31") & (ms.index <= "2026-09-30")]
assert len(ms) == 24, len(ms)
roll = (ml.rolling(3).sum() / (mt_ - ma).rolling(3).sum() * 100).reindex(ms.index)
ms, roll = to_month_start(ms), to_month_start(roll)
fig, ax = new_fig(10.5, 5.4)
ax.plot(ms.index, ms, color=LIGHT, lw=1.5, marker="o", ms=3, label="Monthly")
ax.plot(roll.index, roll, color=RED, lw=2.4, label="3-month rolling")
for lab, p, x in [("FY2024", "FY2024", pd.Timestamp("2024-11-15")), ("FY2025", "FY2025", pd.Timestamp("2025-07-01"))]:
    pass
ax.set_ylim(60, 90)
ax.set_ylabel("Local-system share of domestic cashless value, %")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%y"))
ax.text(0.99, 0.97, f"FY2024 {share['FY2024']:.1f}%  →  FY2025 {share['FY2025']:.1f}%\n"
        f"Jan–Sep 2025 {share['YTD Sep 2025']:.1f}%  →  Jan–Sep 2026 {share['YTD Sep 2026']:.1f}%",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.2, bbox=dict(boxstyle="round,pad=0.4", fc="#F3F5F8", ec="none"))
ax.legend(loc="lower left", fontsize=8.5)
finish(fig, ax, f"Kaspi's local system handles {share['YTD Sep 2026']:.0f}% of domestic card value, but its share is slipping",
       S_47 + " Monthly = YTD differences [calc].", "10_closed_loop_share.png",
       subtitle="Local-system (Kaspi.kz per NBK) share of KZ-issued card cashless value used in Kazakhstan, incl. P2P transfers")

# ---------------- H3c: QR vs POS in store ----------------
qr = ytd(d, "T6", "txn_value", "cashless", channel="QR code")
pos = ytd(d, "T6", "txn_value", "cashless", channel="POS terminal")
qrc = ytd(d, "T6", "txn_count", "cashless", channel="QR code")
posc = ytd(d, "T6", "txn_count", "cashless", channel="POS terminal")
im = ytd(d, "T6", "txn_value", "cashless", channel="Internet & mobile")
t6 = ytd(d, "T6", "txn_value", "cashless", channel="TOTAL")
PQ, PP = periods(qr), periods(pos)
qs = {p: pct(PQ[p], PQ[p] + PP[p]) for p in PQ}
for p, v in qs.items():
    M.add(f"qr_share_instore_{p.replace(' ', '')}", v, "% of POS+QR value", "calc", S_6)
    M.add(f"qr_value_{p.replace(' ', '')}", PQ[p] / 1e6, "KZT trn", "data", S_6)
    M.add(f"pos_value_{p.replace(' ', '')}", PP[p] / 1e6, "KZT trn", "data", S_6)
for lab, a, b in [("FY2025", "FY2024", "FY2025"), ("YTD2026", "YTD Sep 2025", "YTD Sep 2026")]:
    M.add(f"growth_qr_{lab}", pct(PQ[b], PQ[a]) - 100, "% YoY", "calc", S_6)
    M.add(f"growth_pos_{lab}", pct(PP[b], PP[a]) - 100, "% YoY", "calc", S_6)
M.add("internet_mobile_share_T6_YTDSep2026", pct(periods(im)["YTD Sep 2026"], periods(t6)["YTD Sep 2026"]), "% of in-KZ cashless value",
      "calc", S_6)
M.add("avg_ticket_qr_FY2025", full_year(qr, 2025) * 1e6 / (full_year(qrc, 2025) * 1e3), "KZT/txn", "calc", S_6)
M.add("avg_ticket_pos_FY2025", full_year(pos, 2025) * 1e6 / (full_year(posc, 2025) * 1e3), "KZT/txn", "calc", S_6)

mq, mp = monthly_from_ytd(qr), monthly_from_ytd(pos)
win = (mq.index >= "2024-10-31") & (mq.index <= "2026-09-30")
mq, mp = to_month_start(mq[win]), to_month_start(mp[win])
assert len(mq) == 24
fig, ax = new_fig(10.5, 5.4)
w = 12
ax.bar(mq.index - pd.Timedelta(days=6), mq / 1e6, width=w, color=RED, label="QR code")
ax.bar(mp.index + pd.Timedelta(days=6), mp / 1e6, width=w, color=ACCENT, label="POS terminal")
ax.set_ylabel("KZT trillion per month")
ax2 = ax.twinx()
qsm = 100 * mq / (mq + mp)
ax2.plot(qsm.index, qsm, color=DARK, lw=2, label="QR share of POS+QR (rhs)")
ax2.set_ylim(30, 60)
ax2.spines["right"].set_visible(True)
ax2.set_ylabel("QR share, %")
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5, ncol=3)
ax.set_ylim(0, max(mq.max(), mp.max()) / 1e6 * 1.35)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%y"))
finish(fig, ax, f"QR overtook POS in-store, but its share has plateaued near {qs['YTD Sep 2026']:.0f}% since 2025",
       S_6 + f" QR share = QR ÷ (QR + POS) [calc]: FY2024 {qs['FY2024']:.1f}%, FY2025 {qs['FY2025']:.1f}%, "
       f"Jan–Sep 2025 {qs['YTD Sep 2025']:.1f}%, Jan–Sep 2026 {qs['YTD Sep 2026']:.1f}%.",
       "11_qr_vs_pos.png", subtitle="Monthly in-store card value in Kazakhstan by environment (all issuers)")

# ---------------- H3d/e: Kaspi vs NBK and bypass estimate ----------------
kv = lambda m, p: float(k[(k.metric == m) & (k.period == p)].value.iloc[0])  # noqa: E731
S_K = src_kaspi(2025, "Item 5 Payments key operating metrics, PDF p92 (TPV) and mix shares p92; FY2024 mix: FY2024 20-F p92")
comp = []
for fy in (2024, 2025):
    tpv = kv("tpv", f"FY{fy}")
    qc = kv("tpv_qr_and_card", f"FY{fy}")
    nbk_cashless = full_year(tot, fy) / 1e3        # KZT bn
    nbk_instore = (full_year(qr, fy) + full_year(pos, fy)) / 1e3
    comp.append(dict(fy=fy, tpv=tpv, qr_card=qc, nbk_cashless=nbk_cashless, nbk_instore=nbk_instore,
                     r_tpv=pct(tpv, nbk_cashless), r_qc=pct(qc, nbk_instore)))
    M.add(f"kaspi_tpv_to_nbk_cashless_FY{fy}", pct(tpv, nbk_cashless), "%", "calc", S_K + " ; " + S_47,
          "scope mismatch: Kaspi TPV excl. free P2P, incl. B2B & bills; NBK incl. P2P card transfers")
    M.add(f"kaspi_qrcard_to_nbk_instore_FY{fy}", pct(qc, nbk_instore), "%", "calc", S_K + " ; " + S_6,
          "Kaspi QR+card TPV = mix% x TPV [calc]; includes Kaspi online card payments, NBK side is POS+QR only")
    M.add(f"kaspi_qrcard_tpv_FY{fy}", qc / 1e3, "KZT trn", "calc", S_K)
M.add("growth_kaspi_qrcard_FY2025", pct(comp[1]["qr_card"], comp[0]["qr_card"]) - 100, "% YoY", "calc", S_K)
M.add("growth_nbk_instore_FY2025", pct(comp[1]["nbk_instore"], comp[0]["nbk_instore"]) - 100, "% YoY", "calc", S_6)
M.add("growth_kaspi_tpv_FY2025", pct(kv("tpv", "FY2025"), kv("tpv", "FY2024")) - 100, "% YoY", "calc", S_K)
M.add("growth_nbk_cashless_FY2025", pct(full_year(tot, 2025), full_year(tot, 2024)) - 100, "% YoY", "calc", S_47)

# Bypass estimate [estimate]:  B = (q * QR + s * POS) / (QR + POS)
#   q = share of QR value NOT on international rails; s = share of POS value on local-system (Kaspi.kz) cards.
SCEN = {"low": dict(q=0.85, s=0.10), "base": dict(q=1.00, s=0.30), "high": dict(q=1.00, s=0.50)}
rows = []
for per in ["FY2024", "FY2025", "YTD Sep 2025", "YTD Sep 2026"]:
    for case, a in SCEN.items():
        b = 100 * (a["q"] * PQ[per] + a["s"] * PP[per]) / (PQ[per] + PP[per])
        rows.append(dict(period=per, case=case, q=a["q"], s=a["s"], qr_trn=PQ[per] / 1e6, pos_trn=PP[per] / 1e6, bypass_pct=b))
byp = pd.DataFrame(rows)
byp.round(3).to_csv(ROOT / "outputs" / "h3_bypass_sensitivity.csv", index=False)
ASSUME = ("q = share of QR value not on intl rails (low 0.85 / base 1.0 / high 1.0; Kaspi: proprietary QR 'eliminates interchange', "
          "20-F FY2025 p105); s = share of POS value on local-system cards (0.10 / 0.30 / 0.50; anchors: local = 42% of used cards, "
          "NBK T1; Kaspi says other cards' POS volumes are 'significantly lower' than Kaspi QR + Kaspi Gold, 20-F FY2025 p91)")
for r in byp.itertuples():
    M.add(f"bypass_instore_{r.case}_{r.period.replace(' ', '')}", r.bypass_pct, "% of POS+QR value", "estimate", S_6, ASSUME)
print(byp.pivot(index="period", columns="case", values="bypass_pct").round(1))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 5.6), gridspec_kw=dict(width_ratios=[1.15, 1]))
f25 = byp[byp.period == "FY2025"].set_index("case")
cases = ["low", "base", "high"]
a1.bar(cases, f25.loc[cases, "bypass_pct"], color=[LIGHT, RED, LIGHT], width=0.55)
for i, c in enumerate(cases):
    a1.text(i, f25.loc[c, "bypass_pct"] + 1.5, f"{f25.loc[c, 'bypass_pct']:.0f}%", ha="center", fontweight="bold")
    a1.text(i, 4, f"q={SCEN[c]['q']:.2f}\ns={SCEN[c]['s']:.2f}", ha="center", fontsize=8.5, color=DARK)
a1.set_ylim(0, 100)
a1.set_ylabel("Share of in-store value bypassing intl rails, %")
a1.set_title("[estimate] In-store bypass share, FY2025\nB = (q·QR + s·POS) ÷ (QR + POS)", loc="left", fontsize=10, fontweight="bold")
base_tr = byp[byp.case == "base"].set_index("period").bypass_pct
a1.text(0.02, 0.97, f"Base case over time:\nFY2024 {base_tr['FY2024']:.1f}% → FY2025 {base_tr['FY2025']:.1f}%\n"
        f"9M25 {base_tr['YTD Sep 2025']:.1f}% → 9M26 {base_tr['YTD Sep 2026']:.1f}%", transform=a1.transAxes, va="top", fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.35", fc="#F3F5F8", ec="none"))
x = np.arange(2)
cdf = pd.DataFrame(comp)
a2.bar(x - 0.2, cdf.r_tpv, 0.38, color=GREY, label="Kaspi TPV ÷ NBK cashless card value")
a2.bar(x + 0.2, cdf.r_qc, 0.38, color=RED, label="Kaspi QR+card TPV [calc] ÷ NBK POS+QR")
for xi, r in enumerate(cdf.itertuples()):
    a2.text(xi - 0.2, r.r_tpv + 1.5, f"{r.r_tpv:.0f}%", ha="center", fontsize=9)
    a2.text(xi + 0.2, r.r_qc + 1.5, f"{r.r_qc:.0f}%", ha="center", fontsize=9, fontweight="bold")
a2.set_xticks(x, ["FY2024", "FY2025"])
a2.set_ylim(0, 100)
a2.set_title("[calc] Kaspi volume vs NBK market (scope differs)", loc="left", fontsize=10, fontweight="bold")
a2.legend(loc="upper left", fontsize=8, frameon=False)
finish(fig, a1, f"Base case: ~{f25.loc['base', 'bypass_pct']:.0f}% of in-store value bypasses networks — "
       f"range {f25.loc['low', 'bypass_pct']:.0f}–{f25.loc['high', 'bypass_pct']:.0f}%, flat since 2024",
       S_6 + " " + S_K + ". Kaspi QR+card TPV = TPV × QR&card mix (69% FY2025, 71% FY2024; rounded in source) [calc]. "
       "Assumptions: " + ASSUME + ".", "12_bypass_estimate.png")
M.save()
