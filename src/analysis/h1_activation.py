"""H1 — Activation & usage. Outputs 2 (activation gap), 3b (cash dependence by scheme), 4 (regional).

Charts: 03_activation_gap.png, 04_dormant_pool.png, 05_cash_dependence.png, 06_regional.png
"""
from __future__ import annotations

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.common import (ACCENT, DARK, GREY, LATEST, LIGHT, RED, WINDOW_START, Metrics, finish, full_year, nbk,
                                 new_fig, pct, population, pd, src_nbk, t1, t1_panel, ytd)

M = Metrics("h1_activation")
d = nbk()
A0, A1 = WINDOW_START, LATEST
S_T1 = src_nbk("Table 1 (cards in circulation / used, thousand)", "2024-10-01 and 2026-10-01")

# ---------------- activation by scheme x type ----------------
rows = [("Local system (Kaspi.kz)", "local", "all"), ("Visa debit", "visa", "debit"), ("Visa credit", "visa", "credit"),
        ("Visa debit w/ limit & prepaid", "visa", "debit_with_limit_prepaid"), ("Mastercard debit", "mastercard", "debit"),
        ("Mastercard credit", "mastercard", "credit"),
        ("Mastercard debit w/ limit & prepaid", "mastercard", "debit_with_limit_prepaid"),
        ("All international", "international", "all"), ("All cards", "total", "all")]
act = []
for name, s, ct in rows:
    c, u = t1(d, "cards_in_circulation", s, ct), t1(d, "cards_used", s, ct)
    a0, a1 = pct(u[A0], c[A0]), pct(u[A1], c[A1])
    act.append(dict(name=name, scheme=s, ct=ct, act0=a0, act1=a1, circ1=c[A1], used1=u[A1], dormant1=c[A1] - u[A1]))
    M.add(f"activation_{s}_{ct}_2026-10", a1, "% used / in circulation", "calc", S_T1)
    M.add(f"activation_{s}_{ct}_2024-10", a0, "% used / in circulation", "calc", S_T1)
act = pd.DataFrame(act)
intl = act[act.scheme.eq("international")].iloc[0]
loc = act[act.scheme.eq("local")].iloc[0]
M.add("dormant_international_2026-10", intl.dormant1, "thousand cards", "calc", S_T1, "international in circulation − used")
M.add("dormant_international_share_2026-10", 100 - intl.act1, "% of international cards", "calc", S_T1)
M.add("activation_gap_local_minus_intl_pp", loc.act1 - intl.act1, "pp", "calc", S_T1)
M.add("activation_change_intl_24m_pp", intl.act1 - intl.act0, "pp", "calc", S_T1)
tot = act[act.scheme.eq("total")].iloc[0]
M.add("dormant_total_2026-10", tot.dormant1, "thousand cards", "calc", S_T1)

plot = act[~act.scheme.isin(["total"])].iloc[::-1]
fig, ax = new_fig(10.5, 5.8)
y = np.arange(len(plot))
ax.barh(y + 0.19, plot.act0, height=0.36, color=LIGHT, label="Oct 2024")
colors = [RED if s == "local" else (DARK if s == "international" else ACCENT) for s in plot.scheme]
ax.barh(y - 0.19, plot.act1, height=0.36, color=colors, label="Oct 2026")
for i, r in enumerate(plot.itertuples()):
    ax.text(r.act1 + 0.8, i - 0.19, f"{r.act1:.0f}%", va="center", fontsize=8.5, fontweight="bold")
    lab = f"{r.circ1 / 1000:,.1f}m" if r.circ1 >= 100 else f"{r.circ1:,.0f}k"
    ax.text(101, i, lab, va="center", ha="left", fontsize=8.5, color=GREY)
ax.text(101, len(plot) - 0.35, "Cards in\ncirculation", fontsize=8, color=GREY, va="bottom")
ax.set_yticks(y, plot.name)
ax.set_xlim(0, 100)
ax.set_xlabel("Activation ratio = used ÷ in circulation, %")
ax.axvline(loc.act1, color=RED, lw=0.8, ls=":")
ax.legend(loc="lower right", fontsize=8.5)
finish(fig, ax, f"Only {intl.act1:.0f}% of international cards are used vs {loc.act1:.0f}% of local; Mastercard debit just "
       f"{act[(act.scheme == 'mastercard') & (act.ct == 'debit')].act1.iloc[0]:.0f}%",
       S_T1 + " Activation ratio [calc]. NBK does not publish its definition of a 'used' card.",
       "03_activation_gap.png", subtitle="Share of cards in circulation that were used, by payment system and card type")

# ---------------- dormant pool trend ----------------
pc, pu = t1_panel(d, "cards_in_circulation"), t1_panel(d, "cards_used")
dorm = (pc - pu).loc[A0:A1]
assert len(dorm.dropna(subset=["total"])) == 25, len(dorm)
dorm["other"] = dorm["international"] - dorm["visa"] - dorm["mastercard"]
fig, ax = new_fig(10.5, 5.6)
stack = [("local", "Local system (Kaspi.kz)", RED), ("visa", "Visa", ACCENT), ("mastercard", "Mastercard", "#7FA3D9"),
         ("other", "UnionPay & other intl [calc]", LIGHT)]
ax.stackplot(dorm.index, *[dorm[k] / 1000 for k, _, _ in stack], labels=[n for _, n, _ in stack],
             colors=[c for _, _, c in stack], alpha=0.95)
for dt in [A0, A1]:
    ax.annotate(f"{dorm.loc[dt, 'total'] / 1000:.1f}m", (dt, dorm.loc[dt, "total"] / 1000), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=9.5, fontweight="bold")
ax.set_ylabel("Dormant cards (in circulation − used), million")
ax.set_ylim(0, dorm.total.max() / 1000 * 1.18)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%y"))
hl = ax.get_legend_handles_labels()
M.add("dormant_total_2024-10", dorm.loc[A0, "total"], "thousand cards", "calc", S_T1)
M.add("dormant_mastercard_2026-10", dorm.loc[A1, "mastercard"], "thousand cards", "calc", S_T1)
M.add("dormant_mastercard_2024-10", dorm.loc[A0, "mastercard"], "thousand cards", "calc", S_T1)
M.add("dormant_visa_2026-10", dorm.loc[A1, "visa"], "thousand cards", "calc", S_T1)
M.add("dormant_local_2026-10", dorm.loc[A1, "local"], "thousand cards", "calc", S_T1)
intl_d0 = dorm.loc[A0, "international"]
intl_d1 = dorm.loc[A1, "international"]
M.add("dormant_international_2024-10", intl_d0, "thousand cards", "calc", S_T1)
finish(fig, ax, f"The dormant pool grew to {dorm.loc[A1, 'total'] / 1e3:.1f}m cards; "
       f"{100 * intl_d1 / dorm.loc[A1, 'total']:.0f}% of it sits on Visa and Mastercard",
       src_nbk("Table 1 (thousand cards)", "monthly, 2024-10-01 to 2026-10-01",
               "Dormant = in circulation − used [calc]. Release v263 Table 1 excluded (source row-shift); 2025-08-01 taken from v275."),
       "04_dormant_pool.png", subtitle="Cards in circulation that were not used, by payment system (million)",
       fig_legend=dict(handles=hl[0], labels=hl[1], ncol=4))

# ---------------- cash dependence by scheme ----------------
S_T4 = src_nbk("Table 4 (KZ-issued cards in and outside KZ, YTD; mln KZT)", "FY2025 and Jan–Sep 2026")
cd = []
for s, name in [("local", "Local system (Kaspi.kz)"), ("visa", "Visa"), ("mastercard", "Mastercard"),
                ("unionpay", "UnionPay"), ("international", "All international"), ("total", "All cards")]:
    for per, getter in [("FY2025", lambda x: full_year(x, 2025)), ("Jan–Sep 2026", lambda x: x.get(pd.Timestamp("2026-09-30")))]:
        cv = getter(ytd(d, "T4", "txn_value", "cashless", scheme=s))
        wv = getter(ytd(d, "T4", "txn_value", "cash_withdrawal", scheme=s))
        cd.append(dict(scheme=s, name=name, period=per, cashless=cv, cash=wv, cash_share=pct(wv, cv + wv)))
cd = pd.DataFrame(cd)
for r in cd.itertuples():
    M.add(f"cash_share_{r.scheme}_{r.period.replace(' ', '').replace('–', '-')}", r.cash_share, "% of card value",
          "calc", S_T4)
c26 = cd[cd.period == "Jan–Sep 2026"].set_index("scheme")
M.add("intl_share_of_cash_withdrawals_YTDSep2026", pct(c26.loc["international", "cash"], c26.loc["total", "cash"]),
      "% of cash-withdrawal value", "calc", S_T4)
M.add("intl_share_of_cashless_YTDSep2026", pct(c26.loc["international", "cashless"], c26.loc["total", "cashless"]),
      "% of cashless value", "calc", S_T4)
M.add("cash_ratio_intl_vs_local_YTDSep2026", c26.loc["international", "cash_share"] / c26.loc["local", "cash_share"], "x",
      "calc", S_T4)

fig, ax = new_fig(10.5, 5.4)
names = ["Local system (Kaspi.kz)", "Visa", "Mastercard", "UnionPay", "All cards"]
sub = cd[cd.name.isin(names)]
x = np.arange(len(names))
for j, (per, col) in enumerate([("FY2025", LIGHT), ("Jan–Sep 2026", ACCENT)]):
    vals = [sub[(sub.name == n) & (sub.period == per)].cash_share.iloc[0] for n in names]
    bars = ax.bar(x + (j - 0.5) * 0.38, vals, width=0.36, color=[RED if (n.startswith("Local") and j) else col for n in names],
                  label=per)
    for xi, v in zip(x, vals):
        ax.text(xi + (j - 0.5) * 0.38, v + 0.8, f"{v:.0f}%", ha="center", fontsize=8.5, fontweight="bold" if j else None)
ax.set_xticks(x, names)
ax.set_ylabel("Cash withdrawals as % of card value (cash + cashless)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=LIGHT, label="FY2025"), Patch(color=ACCENT, label="Jan–Sep 2026 (local in red)")], fontsize=8.5)
ax.set_ylim(0, sub.cash_share.max() * 1.18)
finish(fig, ax, f"International cards carry {c26.loc['international', 'cash'] / c26.loc['total', 'cash'] * 100:.0f}% of cash "
       f"withdrawals; Visa cards are {c26.loc['visa', 'cash_share'] / c26.loc['local', 'cash_share']:.0f}x as cash-heavy as local",
       S_T4 + " Cash share = cash withdrawal ÷ (cash withdrawal + cashless) [calc].", "05_cash_dependence.png",
       subtitle="Share of each payment system's card value that is cash withdrawal")

# ---------------- regional ----------------
S_T5 = src_nbk("Table 5 (cards of KZ and foreign banks used in KZ, by region; YTD)", "Jan–Sep 2026")
pop = population().set_index("region")
r5 = d[(d.table == "T5") & (d.as_of_date == "2026-09-30") & (d.region != "TOTAL")]
reg = r5.pivot_table(index="region", columns=["metric", "flow_type"], values="value", aggfunc="first")
reg.columns = [f"{a}_{b}" for a, b in reg.columns]
reg["cash_share"] = 100 * reg.txn_value_cash_withdrawal / (reg.txn_value_cash_withdrawal + reg.txn_value_cashless)
reg["pop"] = pop.population
assert reg["pop"].notna().all(), reg[reg["pop"].isna()]
reg["cashless_txn_per_capita"] = reg.txn_count_cashless * 1e3 / (reg["pop"] * 1e3)   # transactions per person, 9 months
r2 = d[(d.table == "T2") & (d.as_of_date == "2026-10-01") & (d.region != "TOTAL")]
c2 = r2[r2.metric == "cards_in_circulation"].groupby("region").value.sum()
u2 = r2[r2.metric == "cards_used"].groupby("region").value.sum()
reg["activation"] = 100 * u2 / c2
reg = reg.sort_values("cashless_txn_per_capita")
reg.round(2).to_csv(__import__("src.analysis.common", fromlist=["ROOT"]).ROOT / "outputs" / "regional_table.csv")
for k in ["Almaty city", "Astana city"]:
    M.add(f"cashless_txn_per_capita_{k}", reg.loc[k, "cashless_txn_per_capita"], "txns per person, Jan–Sep 2026", "calc",
          S_T5 + " Population: stat.gov.kz 2026-10-01.")
lo = reg.iloc[0]
hi_cash = reg.cash_share.idxmax()
M.add("cashless_txn_per_capita_min_region", lo.cashless_txn_per_capita, f"txns per person ({lo.name})", "calc", S_T5)
M.add("cash_share_max_region", reg.cash_share.max(), f"% of value ({hi_cash})", "calc", S_T5)
M.add("cash_share_almaty_city", reg.loc["Almaty city", "cash_share"], "% of value", "calc", S_T5)
M.add("ratio_top_bottom_txn_per_capita", reg.cashless_txn_per_capita.max() / reg.cashless_txn_per_capita.min(), "x", "calc", S_T5)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 6.2), sharey=True)
yy = np.arange(len(reg))
cities = reg.index.str.endswith("city")
a1.barh(yy, reg.cashless_txn_per_capita, color=[ACCENT if c else LIGHT for c in cities])
for i, v in enumerate(reg.cashless_txn_per_capita):
    a1.text(v + 3, i, f"{v:.0f}", va="center", fontsize=8)
a1.set_yticks(yy, reg.index)
a1.set_title("Cashless card transactions per person, Jan–Sep 2026", loc="left", fontsize=10, fontweight="bold")
a2.barh(yy, reg.cash_share, color=[RED if v >= reg.cash_share.quantile(0.75) else LIGHT for v in reg.cash_share])
for i, v in enumerate(reg.cash_share):
    a2.text(v + 0.3, i, f"{v:.0f}%", va="center", fontsize=8)
a2.set_title("Cash withdrawal share of card value", loc="left", fontsize=10, fontweight="bold")
a2.set_xlim(0, reg.cash_share.max() * 1.15)
red = reg[reg.cash_share >= reg.cash_share.quantile(0.75)]
M.add("cash_share_top_quartile_min", red.cash_share.min(), "% of value", "calc", S_T5, ", ".join(red.index))
finish(fig, a1, f"North and east still take {red.cash_share.min():.0f}–{red.cash_share.max():.0f}% of card value in cash "
       f"vs {reg.loc['Almaty city', 'cash_share']:.0f}% in Almaty city",
       S_T5 + " Per capita uses stat.gov.kz 'Population by region.xlsx' as of 2026-10-01 (thousand persons, unit inferred) "
       "[calc]. Cities highlighted. Almaty city (and to a lesser extent Astana) counts are inflated by HQ-registered online / P2P flows; compare regions, not cities.",
       "06_regional.png")

# ---------------- H1e sizing [estimate] ----------------
# 12 months to Sep 2026 = FY2025 − Jan–Sep 2025 + Jan–Sep 2026  [calc]
def last12(scheme, flow):
    s = ytd(d, "T4", "txn_value", flow, scheme=scheme)
    return full_year(s, 2025) - s[pd.Timestamp("2025-09-30")] + s[pd.Timestamp("2026-09-30")]

intl_cashless_12m = last12("international", "cashless")
intl_cash_12m = last12("international", "cash_withdrawal")
used_intl = intl.used1
val_per_used = intl_cashless_12m / used_intl          # mln KZT per used card per year
M.add("intl_cashless_value_12m_to_Sep2026", intl_cashless_12m / 1e6, "KZT trn", "calc", S_T4)
M.add("intl_cash_value_12m_to_Sep2026", intl_cash_12m / 1e6, "KZT trn", "calc", S_T4)
M.add("intl_cashless_value_per_used_card_12m", val_per_used, "thousand KZT per used card per year", "calc", S_T4)
scen = {"low": dict(dpp=2, alpha=0.15, conv=0.05), "base": dict(dpp=5, alpha=0.25, conv=0.10),
        "high": dict(dpp=10, alpha=0.40, conv=0.20)}
sz = []
for k, p in scen.items():
    new_active = intl.circ1 * p["dpp"] / 100
    act_val = new_active * val_per_used * p["alpha"]
    conv_val = intl_cash_12m * p["conv"]
    sz.append(dict(case=k, **p, new_active_k=new_active, activation_value_trn=act_val / 1e6, conversion_value_trn=conv_val / 1e6,
                   uplift_pct=pct(act_val + conv_val, intl_cashless_12m)))
    M.add(f"h1_uplift_{k}", pct(act_val + conv_val, intl_cashless_12m), "% of intl cashless value (12m)", "estimate",
          S_T1 + " " + S_T4,
          f"+{p['dpp']}pp activation on {intl.circ1 / 1e3:.1f}m intl cards x {p['alpha']:.0%} of avg value per used card; "
          f"+ {p['conv']:.0%} of intl cash withdrawals converted to cashless")
pd.DataFrame(sz).round(3).to_csv(__import__("src.analysis.common", fromlist=["ROOT"]).ROOT / "outputs" / "h1_sizing.csv", index=False)
print(pd.DataFrame(sz).round(2).to_string())
M.save()
