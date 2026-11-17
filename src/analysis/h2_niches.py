"""H2 — Defensible niches. Output 5 (cross-border) + credit test.

Charts: 07_outbound_cross_border.png, 08_inbound_vs_outbound.png, 09_credit_share.png
"""
from __future__ import annotations

import numpy as np
from matplotlib.patches import Patch

from src.analysis.common import (ACCENT, DARK, GREY, LATEST, LIGHT, RED, Metrics, finish, full_year, nbk, new_fig, pct, pd,
                                 src_nbk, t1, ytd)

M = Metrics("h2_niches")
d = nbk()
E25, E26 = pd.Timestamp("2025-09-30"), pd.Timestamp("2026-09-30")
S_T7 = src_nbk("Table 7 (KZ-issued cards used outside KZ, by environment; YTD, mln KZT)", "FY2024, FY2025, Jan–Sep 2025/2026")
S_X = src_nbk("Tables 4, 6, 7 (YTD, mln KZT)", "FY2024, FY2025, Jan–Sep 2025/2026",
              "Domestic use of KZ cards = T4 − T7; foreign cards in KZ = T6 − (T4 − T7) [calc].")


def periods(s: pd.Series) -> dict:
    return {"FY2024": full_year(s, 2024), "FY2025": full_year(s, 2025), "YTD Sep 2025": s.get(E25), "YTD Sep 2026": s.get(E26)}


# ---------------- outbound by channel ----------------
chans = ["POS terminal", "Internet & mobile", "Other", "ATM"]
ob = {ch: periods(ytd(d, "T7", "txn_value", "cashless", channel=ch)) for ch in chans + ["TOTAL"]}
obc = {ch: periods(ytd(d, "T7", "txn_count", "cashless", channel=ch)) for ch in ["POS terminal", "Internet & mobile", "TOTAL"]}
ob_cash = periods(ytd(d, "T7", "txn_value", "cash_withdrawal", channel="TOTAL"))
t4 = periods(ytd(d, "T4", "txn_value", "cashless", scheme="total"))
t6 = periods(ytd(d, "T6", "txn_value", "cashless", channel="TOTAL"))
t4c = periods(ytd(d, "T4", "txn_count", "cashless", scheme="total"))
t6c = periods(ytd(d, "T6", "txn_count", "cashless", channel="TOTAL"))
t7c = periods(ytd(d, "T7", "txn_count", "cashless", channel="TOTAL"))
dom = {k: t4[k] - ob["TOTAL"][k] for k in t4}
inb = {k: t6[k] - dom[k] for k in t4}
inbc = {k: t6c[k] - (t4c[k] - t7c[k]) for k in t4}

g = lambda x, a, b: pct(x[b], x[a]) - 100  # noqa: E731
for k in ["FY2024", "FY2025", "YTD Sep 2025", "YTD Sep 2026"]:
    M.add(f"outbound_cashless_{k.replace(' ', '')}", ob["TOTAL"][k] / 1e6, "KZT trn", "data", S_T7)
    M.add(f"outbound_cnp_{k.replace(' ', '')}", ob["Internet & mobile"][k] / 1e6, "KZT trn", "data", S_T7)
    M.add(f"inbound_foreign_cards_{k.replace(' ', '')}", inb[k] / 1e6, "KZT trn", "calc", S_X)
    M.add(f"domestic_cashless_KZcards_{k.replace(' ', '')}", dom[k] / 1e6, "KZT trn", "calc", S_X)
grow = {}
for lab, a, b in [("FY2025", "FY2024", "FY2025"), ("YTD2026", "YTD Sep 2025", "YTD Sep 2026")]:
    grow[lab] = dict(outbound=g(ob["TOTAL"], a, b), cnp=g(ob["Internet & mobile"], a, b), pos=g(ob["POS terminal"], a, b),
                     domestic=g(dom, a, b), inbound=g(inb, a, b))
    for k, v in grow[lab].items():
        M.add(f"growth_{k}_{lab}", v, "% YoY", "calc", S_X if k in ("domestic", "inbound") else S_T7)
    M.add(f"outbound_vs_domestic_growth_multiple_{lab}", grow[lab]["outbound"] / grow[lab]["domestic"], "x", "calc", S_X)
M.add("cnp_share_of_outbound_YTDSep2026", pct(ob["Internet & mobile"]["YTD Sep 2026"], ob["TOTAL"]["YTD Sep 2026"]),
      "% of outbound cashless value", "calc", S_T7)
M.add("outbound_share_of_KZcard_cashless_YTDSep2026", pct(ob["TOTAL"]["YTD Sep 2026"], t4["YTD Sep 2026"]), "%", "calc", S_X)
M.add("outbound_cnp_avg_ticket_YTDSep2026",
      ob["Internet & mobile"]["YTD Sep 2026"] * 1e6 / (obc["Internet & mobile"]["YTD Sep 2026"] * 1e3), "KZT/txn", "calc", S_T7)
M.add("outbound_pos_avg_ticket_YTDSep2026",
      ob["POS terminal"]["YTD Sep 2026"] * 1e6 / (obc["POS terminal"]["YTD Sep 2026"] * 1e3), "KZT/txn", "calc", S_T7)
M.add("inbound_txn_count_FY2025", inbc["FY2025"] / 1e3, "mln transactions", "calc", S_X)
M.add("outbound_cash_withdrawal_FY2025", ob_cash["FY2025"] / 1e6, "KZT trn", "data", S_T7)
# Intl-rail dependency: outbound cashless as share of international-scheme cashless (assumes all outbound is on intl rails)
intl = periods(ytd(d, "T4", "txn_value", "cashless", scheme="international"))
M.add("outbound_share_of_intl_cashless_YTDSep2026", pct(ob["TOTAL"]["YTD Sep 2026"], intl["YTD Sep 2026"]), "%", "estimate",
      S_X, "assumes KZ cards used abroad run on international schemes (local-system cards assumed not usable abroad)")

fig, ax = new_fig(10.5, 5.6)
cols = ["FY2024", "FY2025", "YTD Sep 2025", "YTD Sep 2026"]
x = np.arange(len(cols))
bottom = np.zeros(len(cols))
for ch, col in [("Internet & mobile", ACCENT), ("POS terminal", "#7FA3D9"), ("Other", LIGHT), ("ATM", GREY)]:
    v = np.array([ob[ch][c] / 1e6 for c in cols])
    ax.bar(x, v, bottom=bottom, color=col, width=0.6, label="Internet & mobile (card-not-present)" if ch.startswith("Int") else ch)
    for xi, (vi, b) in enumerate(zip(v, bottom)):
        if vi > 0.35:
            ax.text(xi, b + vi / 2, f"{vi:.2f}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    bottom += v
for xi, c in enumerate(cols):
    ax.text(xi, bottom[xi] + 0.06, f"₸{bottom[xi]:.2f}trn", ha="center", fontsize=9.5, fontweight="bold")
ax.set_xticks(x, cols)
ax.axvline(1.5, color=GREY, lw=0.8, ls=":")
ax.set_ylabel("KZT trillion")
ax.set_ylim(0, bottom.max() * 1.25)
txt = (f"Growth, FY2025:  CNP abroad {grow['FY2025']['cnp']:+.0f}%  |  POS abroad {grow['FY2025']['pos']:+.0f}%  |  "
       f"domestic {grow['FY2025']['domestic']:+.0f}%\n"
       f"Growth, Jan–Sep 2026:  CNP abroad {grow['YTD2026']['cnp']:+.0f}%  |  POS abroad {grow['YTD2026']['pos']:+.0f}%  |  "
       f"domestic {grow['YTD2026']['domestic']:+.0f}%")
ax.text(0.01, 0.97, txt, transform=ax.transAxes, va="top", fontsize=8.8, color=DARK,
        bbox=dict(boxstyle="round,pad=0.4", fc="#F3F5F8", ec="none"))
hl = ax.get_legend_handles_labels()
finish(fig, ax, f"Cross-border CNP grows {grow['YTD2026']['cnp']:.0f}% a year, ~{grow['YTD2026']['cnp'] / grow['YTD2026']['domestic']:.0f}x "
       f"domestic; POS abroad has stalled",
       S_T7 + " Domestic growth = T4 − T7 [calc]. Growth rates [calc].", "07_outbound_cross_border.png",
       subtitle="Cashless value of KZ-issued cards used outside Kazakhstan, by environment (KZT trillion)",
       fig_legend=dict(handles=hl[0], labels=hl[1], ncol=4))

# ---------------- inbound vs outbound ----------------
fig, ax = new_fig(10.5, 5.4)
x = np.arange(len(cols))
ob_v = [ob["TOTAL"][c] / 1e6 for c in cols]
ib_v = [inb[c] / 1e6 for c in cols]
ax.bar(x - 0.2, ob_v, 0.38, color=ACCENT, label="Outbound: KZ cards used abroad (T7)")
ax.bar(x + 0.2, ib_v, 0.38, color="#7FA3D9", label="Inbound: foreign cards used in KZ [calc]")
for xi, (a, b) in enumerate(zip(ob_v, ib_v)):
    ax.text(xi - 0.2, a + 0.05, f"{a:.2f}", ha="center", fontsize=9, fontweight="bold")
    ax.text(xi + 0.2, b + 0.05, f"{b:.2f}", ha="center", fontsize=9)
ax.set_xticks(x, cols)
ax.axvline(1.5, color=GREY, lw=0.8, ls=":")
ax.set_ylabel("Cashless value, KZT trillion")
ax.set_ylim(0, max(ob_v) * 1.3)
ax.legend(loc="upper left", fontsize=8.5)
ax.text(0.99, 0.97, f"Inbound growth: FY2025 {grow['FY2025']['inbound']:+.0f}%, Jan–Sep 2026 {grow['YTD2026']['inbound']:+.0f}%\n"
        "Kaspi QR now accepts AliPay+ wallets (Kaspi 20-F FY2025 p53)", transform=ax.transAxes, ha="right", va="top",
        fontsize=8.8, bbox=dict(boxstyle="round,pad=0.4", fc="#F3F5F8", ec="none"))
finish(fig, ax, f"Inbound card spend is flat at ₸{inb['FY2025'] / 1e6:.1f}trn while Kaspi QR courts tourists via AliPay+",
       S_X + " Inbound is a residual of three tables (±0.1% revisions ≈ ±₸0.2trn); treat as indicative. "
       "AliPay+: Kaspi.kz Form 20-F FY2025 p53, https://ir.kaspi.kz/media/Form_20-F_2025.pdf",
       "08_inbound_vs_outbound.png", subtitle="Cross-border card value, outbound vs inbound (KZT trillion)")

# ---------------- credit ----------------
S_C = src_nbk("Tables 1 & 2 (thousand cards)", "2024-10-01 and 2026-10-01",
              "Local-system credit = T2 credit total − (Visa + MC + UnionPay credit, T1) [calc]; T1 does not split local cards by type.")
cr = []
for dt in [pd.Timestamp("2024-10-01"), LATEST]:
    for metric in ["cards_in_circulation", "cards_used"]:
        tot = d[(d.table == "T2") & (d.region == "TOTAL") & (d.metric == metric) & (d.card_type == "credit") &
                (d.as_of_date == dt)].value.iloc[0]
        parts = {s: t1(d, metric, s, "credit").get(dt, 0.0) for s in ["visa", "mastercard", "unionpay"]}
        intl_cr = sum(v for v in parts.values() if pd.notna(v))
        cr.append(dict(date=dt, metric=metric, total=tot, intl=intl_cr, local=tot - intl_cr, **parts))
cr = pd.DataFrame(cr)
for r in cr.itertuples():
    tag = f"{r.metric}_{r.date:%Y-%m}"
    M.add(f"credit_total_{tag}", r.total, "thousand cards", "data", S_C)
    M.add(f"credit_intl_share_{tag}", pct(r.intl, r.total), "% of credit cards", "calc", S_C)
    M.add(f"credit_local_{tag}", r.local, "thousand cards", "calc", S_C)

fig, ax = new_fig(10.5, 5.2)
lab = [f"In circulation\n{r.date:%b %Y}" if r.metric == "cards_in_circulation" else f"Used\n{r.date:%b %Y}" for r in cr.itertuples()]
order = [0, 2, 1, 3]
cr2, lab2 = cr.iloc[order].reset_index(drop=True), [lab[i] for i in order]
x = np.arange(len(cr2))
ax.bar(x, cr2.local / 1e3, color=RED, width=0.6, label="Local system (Kaspi.kz) [calc]")
ax.bar(x, cr2.visa / 1e3, bottom=cr2.local / 1e3, color=ACCENT, width=0.6, label="Visa")
ax.bar(x, cr2.mastercard / 1e3, bottom=(cr2.local + cr2.visa) / 1e3, color="#7FA3D9", width=0.6, label="Mastercard")
for xi, r in enumerate(cr2.itertuples()):
    ax.text(xi, r.total / 1e3 + 0.2, f"{r.total / 1e3:.1f}m\nintl {100 * r.intl / r.total:.0f}%", ha="center", fontsize=9,
            fontweight="bold")
ax.set_xticks(x, lab2)
ax.set_ylabel("Credit cards, million")
ax.set_ylim(0, cr2.total.max() / 1e3 * 1.25)
ax.legend(loc="upper right", fontsize=8.5)
last = cr[(cr.date == LATEST) & (cr.metric == "cards_in_circulation")].iloc[0]
finish(fig, ax, f"Credit is not a network stronghold: only {100 * last.intl / last.total:.0f}% of "
       f"{last.total / 1e3:.0f}m credit cards run on Visa or Mastercard",
       S_C, "09_credit_share.png", subtitle="Credit cards by payment system (million)")
M.save()
