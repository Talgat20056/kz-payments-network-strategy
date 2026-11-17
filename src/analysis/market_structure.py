"""Output 1 (market structure) and Output 3 (usage mix: cashless vs cash, average ticket).

Charts: 01_market_structure.png, 02_usage_mix.png
"""
from __future__ import annotations

import matplotlib.ticker as mt

from src.analysis.common import (to_month_start, ACCENT, DARK, GREY, LATEST, LIGHT, RED, WINDOW_START, Metrics, finish, monthly_from_ytd,
                                 nbk, new_fig, pct, src_nbk, t1_panel, ytd, full_year, pd)

M = Metrics("market_structure")
d = nbk()
A0, A1 = WINDOW_START, LATEST
S_T1 = src_nbk("Table 1 (cards in circulation / used, thousand)", "2024-10-01 to 2026-10-01")

# ---------------- 1. Market structure ----------------
pc = t1_panel(d, "cards_in_circulation")
pu = t1_panel(d, "cards_used")
w = pc.loc[A0:A1]
for s in ["total", "local", "visa", "mastercard", "unionpay", "other_international"]:
    if pd.notna(w[s].iloc[-1]):
        M.add(f"circ_{s}_2026-10", w[s].iloc[-1], "thousand cards", "data" if s != "other_international" else "calc", S_T1)
for s in ["total", "local", "international", "visa", "mastercard"]:
    M.add(f"used_{s}_2026-10", pu.loc[A1, s], "thousand cards", "data", S_T1)
    M.add(f"circ_share_{s}_2026-10", pct(pc.loc[A1, s], pc.loc[A1, "total"]), "% of cards in circulation", "calc", S_T1)
    M.add(f"used_share_{s}_2026-10", pct(pu.loc[A1, s], pu.loc[A1, "total"]), "% of used cards", "calc", S_T1)
    M.add(f"circ_growth_{s}_24m", pct(pc.loc[A1, s], pc.loc[A0, s]) - 100, "% change 2024-10 -> 2026-10", "calc", S_T1)
    M.add(f"used_growth_{s}_24m", pct(pu.loc[A1, s], pu.loc[A0, s]) - 100, "% change 2024-10 -> 2026-10", "calc", S_T1)

import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.6))
cols = [("local", "Local system (Kaspi.kz per NBK)", RED), ("visa", "Visa", ACCENT), ("mastercard", "Mastercard", "#7FA3D9"),
        ("other", "UnionPay & other intl [calc]", LIGHT)]
for ax, panel, lab in [(ax1, pc, "Cards in circulation"), (ax2, pu, "Cards used")]:
    p = panel.loc[A0:A1].copy()
    p["other"] = p["international"] - p["visa"] - p["mastercard"]
    bottom = 0
    dates = [A0, pd.Timestamp("2025-10-01"), A1]
    x = range(len(dates))
    bottoms = [0] * len(dates)
    for key, name, color in cols:
        vals = [p.loc[dt, key] / 1000 for dt in dates]
        ax.bar(x, vals, bottom=bottoms, color=color, width=0.62, label=name)
        for i, v in enumerate(vals):
            share = 100 * v * 1000 / p.loc[dates[i], "total"]
            if share > 6:
                ax.text(i, bottoms[i] + v / 2, f"{share:.0f}%", ha="center", va="center", color="white", fontsize=8.5,
                        fontweight="bold")
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, dt in enumerate(dates):
        ax.text(i, bottoms[i] + 0.8, f"{p.loc[dt, 'total'] / 1000:.1f}m", ha="center", va="bottom", fontsize=9,
                fontweight="bold", color=DARK)
    ax.set_xticks(list(x), [dt.strftime("%b %Y") for dt in dates])
    ax.set_title(lab + " (million)", loc="left", fontsize=10.5, fontweight="bold")
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.set_ylim(0, max(bottoms) * 1.12)
hl = ax1.get_legend_handles_labels()
vis_c = pct(pc.loc[A1, "visa"], pc.loc[A1, "total"])
loc_u = pct(pu.loc[A1, "local"], pu.loc[A1, "total"])
loc_c = pct(pc.loc[A1, "local"], pc.loc[A1, "total"])
mc_c = pct(pc.loc[A1, "mastercard"], pc.loc[A1, "total"])
mc_u = pct(pu.loc[A1, "mastercard"], pu.loc[A1, "total"])
finish(fig, ax1,
       f"Local cards are {loc_c:.0f}% of the stock but {loc_u:.0f}% of active cards; Mastercard {mc_c:.0f}% vs {mc_u:.0f}%",
       S_T1 + " 'Other intl' = international − Visa − Mastercard [calc]. Percent labels = share of total [calc].",
       "01_market_structure.png", fig_legend=dict(handles=hl[0], labels=hl[1], ncol=4))

# ---------------- 3. Usage mix: cashless vs cash ----------------
S_T4 = src_nbk("Table 4 (use of KZ-issued cards in and outside KZ; YTD cumulative)", "Jan 2024 – Sep 2026",
               "Monthly = YTD(m) − YTD(m−1) [calc].")
cv = monthly_from_ytd(ytd(d, "T4", "txn_value", "cashless", scheme="total"))
wv = monthly_from_ytd(ytd(d, "T4", "txn_value", "cash_withdrawal", scheme="total"))
cc = monthly_from_ytd(ytd(d, "T4", "txn_count", "cashless", scheme="total"))
wc = monthly_from_ytd(ytd(d, "T4", "txn_count", "cash_withdrawal", scheme="total"))
win = (cv.index >= "2024-10-31") & (cv.index <= "2026-09-30")
cv, wv, cc, wc = cv[win], wv[win], cc[win], wc[win]
assert len(cv) == 24, len(cv)
cash_share = 100 * wv / (cv + wv)
tick_cashless = cv * 1e6 / (cc * 1e3)   # KZT per transaction
tick_cash = wv * 1e6 / (wc * 1e3)

for y in (2024, 2025):
    tv = full_year(ytd(d, "T4", "txn_value", "cashless", scheme="total"), y)
    tw = full_year(ytd(d, "T4", "txn_value", "cash_withdrawal", scheme="total"), y)
    M.add(f"cashless_value_FY{y}", tv / 1e6, "KZT trn", "data", S_T4)
    M.add(f"cash_value_FY{y}", tw / 1e6, "KZT trn", "data", S_T4)
    M.add(f"cash_share_value_FY{y}", pct(tw, tv + tw), "% of card value", "calc", S_T4)
for y in (2025, 2026):
    e = pd.Timestamp(f"{y}-09-30")
    tv = ytd(d, "T4", "txn_value", "cashless", scheme="total")[e]
    tw = ytd(d, "T4", "txn_value", "cash_withdrawal", scheme="total")[e]
    M.add(f"cashless_value_YTDSep{y}", tv / 1e6, "KZT trn", "data", S_T4)
    M.add(f"cash_value_YTDSep{y}", tw / 1e6, "KZT trn", "data", S_T4)
M.add("cash_share_value_12m_to_Sep2026", 100 * wv[-12:].sum() / (cv[-12:].sum() + wv[-12:].sum()), "% of card value",
      "calc", S_T4)
M.add("cash_share_value_12m_to_Sep2025", 100 * wv[:12].sum() / (cv[:12].sum() + wv[:12].sum()), "% of card value",
      "calc", S_T4)
M.add("avg_ticket_cashless_12m_to_Sep2026", cv[-12:].sum() * 1e6 / (cc[-12:].sum() * 1e3), "KZT/txn", "calc", S_T4)
M.add("avg_ticket_cashless_12m_to_Sep2025", cv[:12].sum() * 1e6 / (cc[:12].sum() * 1e3), "KZT/txn", "calc", S_T4)
M.add("avg_ticket_cash_12m_to_Sep2026", wv[-12:].sum() * 1e6 / (wc[-12:].sum() * 1e3), "KZT/txn", "calc", S_T4)

cv, wv, cash_share = to_month_start(cv), to_month_start(wv), to_month_start(cash_share)
fig, ax = new_fig(10.5, 5.6)
ax.bar(cv.index, cv / 1e6, width=22, color=ACCENT, label="Cashless value")
ax.bar(wv.index, wv / 1e6, bottom=cv / 1e6, width=22, color=LIGHT, label="Cash-withdrawal value")
ax.set_ylabel("KZT trillion per month")
ax2 = ax.twinx()
ax2.plot(cash_share.index, cash_share, color=DARK, lw=2, marker="o", ms=3, label="Cash share of value (rhs)")
ax2.set_ylabel("Cash share of card value, %")
ax2.set_ylim(0, max(cash_share) * 1.6)
ax2.spines["right"].set_visible(True)
for i in [0, len(cash_share) - 1]:
    ax2.annotate(f"{cash_share.iloc[i]:.1f}%", (cash_share.index[i], cash_share.iloc[i]), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=9, fontweight="bold")
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5)
ax.xaxis.set_major_formatter(__import__("matplotlib.dates", fromlist=["DateFormatter"]).DateFormatter("%b\n%y"))
finish(fig, ax,
       f"Cash withdrawals are down to {cash_share.iloc[-1]:.0f}% of card value, falling about 1pp a year",
       S_T4, "02_usage_mix.png",
       subtitle="Monthly value of KZ-issued card transactions, Oct 2024 – Sep 2026")
M.save()
