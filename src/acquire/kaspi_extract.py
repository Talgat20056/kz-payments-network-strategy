"""Kaspi.kz Form 20-F Payments Platform KPIs -> data/clean/kaspi_kpis.csv

Each record carries a verbatim quote. The script FAILS if the quote is not found on the stated PDF page,
so every number in kaspi_kpis.csv is mechanically traceable to (file, PDF page, printed page, quote).
pdf_page = 1-based page index in the PDF; printed_page = page number printed in the document footer.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "kaspi"
URL = "https://ir.kaspi.kz/media/Form_20-F_{y}.pdf"

# (filing FY, metric, period FY, value, unit, pdf_page, quote)
R = [
    # ---- FY2025 20-F, Item 5 Payments key operating metrics table (p92) ----
    (2025, "tpv", 2023, 28406, "KZT bn", 92, "TPV(1) ........................................................ 28,406 37,229 44,219"),
    (2025, "tpv", 2024, 37229, "KZT bn", 92, "TPV(1) ........................................................ 28,406 37,229 44,219"),
    (2025, "tpv", 2025, 44219, "KZT bn", 92, "TPV(1) ........................................................ 28,406 37,229 44,219"),
    (2025, "tpv_incl_hepsiburada", 2025, 46350, "KZT bn", 92, "TPV including Hepsiburada(1) ................... 28,406 37,229 46,350"),
    (2025, "payments_active_consumers", 2023, 12.9, "mln", 92, "Payments Active Consumers, millions(2) ... 12.9 13.6 14.6"),
    (2025, "payments_active_consumers", 2024, 13.6, "mln", 92, "Payments Active Consumers, millions(2) ... 12.9 13.6 14.6"),
    (2025, "payments_active_consumers", 2025, 14.6, "mln", 92, "Payments Active Consumers, millions(2) ... 12.9 13.6 14.6"),
    (2025, "tpv_transactions", 2023, 4219, "mln", 92, "TPV Payments Transactions, millions(3) .... 4,219 5,890 6,724"),
    (2025, "tpv_transactions", 2024, 5890, "mln", 92, "TPV Payments Transactions, millions(3) .... 4,219 5,890 6,724"),
    (2025, "tpv_transactions", 2025, 6724, "mln", 92, "TPV Payments Transactions, millions(3) .... 4,219 5,890 6,724"),
    (2025, "payments_take_rate", 2023, 1.23, "%", 92, "Payments Take Rate(4) .............................. 1.23 % 1.18 % 1.10%"),
    (2025, "payments_take_rate", 2024, 1.18, "%", 92, "Payments Take Rate(4) .............................. 1.23 % 1.18 % 1.10%"),
    (2025, "payments_take_rate", 2025, 1.10, "%", 92, "Payments Take Rate(4) .............................. 1.23 % 1.18 % 1.10%"),
    (2025, "avg_current_account_balances", 2025, 981, "KZT bn", 92, "Average Balances on Current Accounts(5) . 769 938 981"),
    (2025, "tpv_mix_p2p", 2025, 8, "% of TPV", 92, "P2P transactions accounted for 8% of our TPV"),
    (2025, "tpv_mix_household_bills", 2025, 16, "% of TPV", 92, "accounted for 16%, 69% and 7% of TPV"),
    (2025, "tpv_mix_qr_and_card", 2025, 69, "% of TPV", 92, "accounted for 16%, 69% and 7% of TPV"),
    (2025, "tpv_mix_b2b", 2025, 7, "% of TPV", 92, "accounted for 16%, 69% and 7% of TPV"),
    (2025, "b2b_tpv", 2025, 2833, "KZT bn", 92, "Payments’ TPV was ₸2,833 billion for the year ended December 31, 2025"),
    (2025, "b2b_transactions", 2025, 79.7, "mln", 92, "number of Kaspi B2B Payments’ transactions was 79.7 million"),
    (2025, "average_mau", 2025, 15.7, "mln", 51, "the Kaspi.kz Super App in Kazakhstan had approximately 15.7 million Average MAU"),
    (2025, "active_merchants", 2025, 764, "thousand", 51, "Kaspi Pay Super App had approximately 764,000 Active Merchants"),
    (2025, "payments_segment_revenue", 2025, 658726, "KZT mln", 104, "Total segment revenue of Payments increased by 12% to ₸658,726 million"),
    (2025, "payments_segment_revenue", 2024, 587097, "KZT mln", 104, "from ₸587,097 million for the year ended December 31, 2024"),
    (2025, "payments_fee_revenue", 2025, 510763, "KZT mln", 104, "to ₸510,763 million for the"),
    (2025, "payments_fee_revenue", 2024, 458953, "KZT mln", 104, "from ₸458,953 million for the year ended December 31, 2024"),
    (2025, "incr_revenue_qr_and_card", 2025, 35038, "KZT mln (YoY increase)", 104, "mainly attributable to a ₸35,038 million increase in revenue from Kaspi QR and card transactions"),
    (2025, "payments_net_income", 2025, 433001, "KZT mln", 105, "Net income of Payments increased by 13% to ₸433,001 million"),
    (2025, "receivables_from_visa_mastercard", 2025, 7674, "KZT mln", 202, "Receivables from VISA and Master Card 2,782 7,674"),
    (2025, "receivables_from_visa_mastercard", 2024, 2782, "KZT mln", 202, "Receivables from VISA and Master Card 2,782 7,674"),
    (2025, "kzt_per_usd_convenience_rate", 2025, 505.53, "KZT per USD (31 Dec 2025)", 8, "₸505.53 per $1 as of"),
    (2025, "kaspi_qr_partner_banks_local", 2025, 7, "banks", 58, "we have integrated Kaspi Pay QR with 7 local banks"),
    # ---- FY2024 20-F ----
    (2024, "tpv_mix_p2p", 2024, 7, "% of TPV", 92, "P2P transactions accounted for 7% of our TPV"),
    (2024, "tpv_mix_household_bills", 2024, 17, "% of TPV", 92, "accounted for 17%, 71% and"),
    (2024, "tpv_mix_qr_and_card", 2024, 71, "% of TPV", 92, "accounted for 17%, 71% and"),
    (2024, "tpv_mix_b2b", 2024, 5, "% of TPV", 92, "5% of TPV, respectively"),
    (2024, "b2b_tpv", 2024, 1951, "KZT bn", 92, "Our Kaspi B2B Payments’ TPV was ₸1,951 billion"),
    (2024, "average_mau", 2024, 14.7, "mln", 56, "the Kaspi.kz Super App had approximately 14.7 million Average MAU"),
    (2024, "active_merchants", 2024, 737, "thousand", 56, "Pay Super App had approximately 737,000 Active Merchants"),
    (2024, "payments_fee_revenue", 2023, 368925, "KZT mln", 105, "from ₸368,925 million for the year ended December 31, 2023"),
    (2024, "incr_revenue_qr_and_card", 2024, 63820, "KZT mln (YoY increase)", 105, "a ₸63,820 million increase in revenue from Kaspi QR and card"),
    # ---- FY2023 20-F ----
    (2023, "tpv", 2021, 12935, "KZT bn", 96, "TPV(1) ............................................................. 12,935 19,913 28,406"),
    (2023, "tpv", 2022, 19913, "KZT bn", 96, "TPV(1) ............................................................. 12,935 19,913 28,406"),
    (2023, "payments_active_consumers", 2021, 9.7, "mln", 96, "Payments Active Consumers, millions(2) ............ 9.7 11.3 12.9"),
    (2023, "payments_active_consumers", 2022, 11.3, "mln", 96, "Payments Active Consumers, millions(2) ............ 9.7 11.3 12.9"),
    (2023, "tpv_transactions", 2021, 1990, "mln", 96, "TPV Payments Transactions, millions(3) ............. 1,990 3,060 4,219"),
    (2023, "tpv_transactions", 2022, 3060, "mln", 96, "TPV Payments Transactions, millions(3) ............. 1,990 3,060 4,219"),
    (2023, "tpv_mix_p2p", 2023, 7, "% of TPV", 96, "P2P transactions accounted for 7% of our TPV"),
    (2023, "tpv_mix_household_bills", 2023, 18, "% of TPV", 96, "accounted for 18%, 71% and 4% of TPV"),
    (2023, "tpv_mix_qr_and_card", 2023, 71, "% of TPV", 96, "accounted for 18%, 71% and 4% of TPV"),
    (2023, "tpv_mix_b2b", 2023, 4, "% of TPV", 96, "accounted for 18%, 71% and 4% of TPV"),
    (2023, "b2b_tpv", 2023, 1081, "KZT bn", 96, "Payments’ TPV was ₸1,081 billion for the year ended December 31, 2023"),
    (2023, "average_mau", 2023, 14.0, "mln", 52, "the Kaspi.kz Super App had approximately 14.0 million Average MAU"),
    (2023, "active_merchants", 2023, 581, "thousand", 52, "Super App had approximately 581,000 Active Merchants"),
    (2023, "incr_revenue_qr_and_card", 2023, 71430, "KZT mln (YoY increase)", 108, "a ₸71,430 million increase in revenue from Kaspi QR and card"),
]

# Qualitative disclosures used as evidence (no numbers derived from them)
Q = [
    (2025, "qr_eliminates_interchange", 105, "continuing adoption of proprietary QR transactions, which eliminates interchange fees paid to"),
    (2024, "qr_eliminates_interchange", 105, "continuing adoption of proprietary QR transactions, which eliminates"),
    (2023, "qr_eliminates_interchange", 109, "continuing adoption of proprietary QR transactions, which eliminates interchange fees paid to"),
    (2025, "alipay_plus_integration", 53, "In Kazakhstan Kaspi QR is directly integrated with other local banks and internationally with AliPay+"),
    (2025, "other_cards_low_volume", 91, "we also accept other cards besides Kaspi Gold in our POS; however, such transaction volumes are significantly lower than"),
    (2025, "visa_mc_agent_net_revenue", 181, "When using third-party payments platforms or networks (e.g., Visa/Mastercard), the Group is an agent"),
    (2025, "tpv_definition", 8, "by Active Consumers within our Payments Platform, excluding free P2P and QR payments;"),
    (2025, "alaqan_palm_launch", 53, "In December 2025 we launched Kaspi Alaqan, a pay-by-palm service."),
    (2025, "significant_psp_register", 66, "Kaspi Bank was included in the Register of Significant Payment Services Providers as of May 1, 2018"),
    (2025, "significant_psp_25pct_threshold", 66, "processes transactions using payment cards in the amount of at least 25% of the total volume of"),
]
Q = [q for q in Q if q[2] > 0]


def pages(fy: int) -> dict[int, str]:
    txt = (RAW / f"Form_20-F_{fy}.pages.txt").read_text(encoding="utf-8")
    out = {}
    for chunk in txt.split("\n=====PAGE ")[1:]:
        head, _, body = chunk.partition("=====\n")
        out[int(head)] = body
    return out


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def printed_page(body: str) -> str:
    lines = [l.strip() for l in body.strip().split("\n") if l.strip()]
    return lines[-1] if lines and re.fullmatch(r"(F-)?\d+", lines[-1]) else ""


def main():
    cache = {fy: pages(fy) for fy in (2023, 2024, 2025)}
    rows, errors = [], []
    for fy, metric, period, value, unit, pg, quote in R:
        body = cache[fy].get(pg, "")
        if squash(quote) not in squash(body):
            errors.append(f"NOT FOUND: FY{fy} p{pg} {metric}: {quote}")
            continue
        rows.append(dict(metric=metric, period=f"FY{period}", value=value, unit=unit, source_doc=f"Kaspi.kz Form 20-F FY{fy}",
                         source_url=URL.format(y=fy), pdf_page=pg, printed_page=printed_page(body),
                         as_of_date=f"{period}-12-31", quote=quote, label="data"))
    for fy, metric, pg, quote in Q:
        body = cache[fy].get(pg, "")
        if squash(quote) not in squash(body):
            errors.append(f"NOT FOUND: FY{fy} p{pg} {metric}: {quote}")
            continue
        rows.append(dict(metric=metric, period=f"FY{fy}", value="", unit="qualitative", source_doc=f"Kaspi.kz Form 20-F FY{fy}",
                         source_url=URL.format(y=fy), pdf_page=pg, printed_page=printed_page(body),
                         as_of_date=f"{fy}-12-31", quote=quote, label="qualitative"))
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    df = pd.DataFrame(rows).astype(object)
    # [calc] derived rows: QR+card TPV = mix share x TPV (mix is rounded to whole %, so +/-0.5pp band)
    tpv = df[df.metric == "tpv"].set_index("period").value.astype(float)
    mix = df[df.metric == "tpv_mix_qr_and_card"].set_index("period").value.astype(float)
    for p in mix.index:
        if p in tpv.index:
            for tag, adj in [("", 0), ("_low", -0.5), ("_high", 0.5)]:
                df.loc[len(df)] = dict(metric=f"tpv_qr_and_card{tag}", period=p, value=round(tpv[p] * (mix[p] + adj) / 100),
                                       unit="KZT bn", source_doc="[calc] tpv x tpv_mix_qr_and_card", source_url="",
                                       pdf_page="", printed_page="", as_of_date=p[2:] + "-12-31",
                                       quote=f"[calc] {tpv[p]:,.0f} x ({mix[p]:.0f}{adj:+.1f})% ; mix rounded to whole % in source",
                                       label="calc")
    out = ROOT / "data" / "clean" / "kaspi_kpis.csv"
    df.to_csv(out, index=False)
    print(f"{len(df)} rows -> {out}")


if __name__ == "__main__":
    main()
