"""Parse NBK payment-card releases (Tables 1-7) into tidy long-format CSVs.

Outputs
-------
data/clean/nbk_cards_long_allvintages.csv  every value from every release (keeps revisions)
data/clean/nbk_cards_long.csv              one value per key, taken from the most recent release (latest vintage)
docs/validation_nbk.md                     subtotal / cross-table checks, with every flagged month

Conventions
-----------
* Release as-of date is read from the narrative paragraph ("As of October 01, 2026 ..."),
  NOT from table headers, because headers contain typos (e.g. release 269 says 01.01 instead of 01.02;
  release 277 Table 2 says 01.10.2025 for 2026 data).
* Stocks (Tables 1-3): as_of_date = stock date.  Flows (Tables 4-7) are year-to-date cumulative:
  period_start = Jan 1, period_end = last day of month before the release as-of date; as_of_date = period_end.
* Units are recorded explicitly per row (thousand cards, units, thousand transactions, mln KZT).
"""
from __future__ import annotations

import calendar
import csv
import re
from datetime import date
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "nbk"
CLEAN = ROOT / "data" / "clean"
DOCS = ROOT / "docs"

MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
TITLES = {
    "T1": "Table 1: Cards in circulation and used, by payment system and card type; payment infrastructure",
    "T2": "Table 2: Cards in circulation and used, by region and card type",
    "T3": "Table 3: Payment infrastructure by region",
    "T4": "Table 4: Use of payment cards issued by banks of Kazakhstan, in and outside the country (by payment system)",
    "T5": "Table 5: Use of cards issued by Kazakhstan and foreign banks on the territory of Kazakhstan, by region",
    "T6": "Table 6: Use of cards issued by Kazakhstan and foreign banks on the territory of Kazakhstan, by operation environment",
    "T7": "Table 7: Use of cards issued by Kazakhstan banks outside Kazakhstan, by operation environment",
}

REGION_MAP = {
    "akmola": "Akmola", "aktobe": "Aktobe", "almaty region": "Almaty region", "atyrau": "Atyrau",
    "east kazakhstan": "East Kazakhstan", "jambul": "Jambyl", "zhambyl": "Jambyl",
    "west kazakhstan": "West Kazakhstan", "karaganda": "Karaganda", "kostanai": "Kostanay",
    "kostanay": "Kostanay", "kyzylorda": "Kyzylorda", "mangistau": "Mangystau", "mangystau": "Mangystau",
    "pavlodar": "Pavlodar", "north kazakhstan": "North Kazakhstan", "turkestan": "Turkestan",
    "almaty city": "Almaty city", "shymkent": "Shymkent city", "shimkent": "Shymkent city",
    "astana": "Astana city", "jetysu": "Zhetysu", "zhetysu": "Zhetysu", "abay": "Abai", "abai": "Abai",
    "ulytau": "Ulytau", "total": "TOTAL",
}

CHANNEL_MAP = {
    "pos": "POS terminal", "atm": "ATM", "internet": "Internet & mobile", "payment terminal": "Payment terminals",
    "qr": "QR code", "others": "Other", "other": "Other", "total": "TOTAL",
}


def num(s: str) -> float | None:
    s = s.replace("\xa0", "").replace(" ", "").replace(" ", "").strip()
    if s in {"", "-", "–", "—"}:
        return None
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def cells(tr) -> list[str]:
    return [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def region_of(label: str) -> str | None:
    l = norm(label).replace(" .", ".")
    if l.startswith("total"):
        return "TOTAL"
    for k, v in REGION_MAP.items():
        if k == "almaty region" and l.startswith("almaty reg"):
            return v
        if k == "almaty city" and l.startswith("almaty city"):
            return v
        if k in ("almaty region", "almaty city"):
            continue
        if l.startswith(k):
            return v
    return None


def channel_of(label: str) -> str | None:
    l = norm(label)
    if l.startswith("total"):
        return "TOTAL"
    for k, v in CHANNEL_MAP.items():
        if l.startswith(k):
            return v
    return None


def release_asof(soup) -> date:
    for p in soup.find_all("p"):
        t = re.sub(r"\s+", "", p.get_text(" ", strip=True))
        m = re.match(r"Asof([A-Za-z]+)(\d{2}),(\d{4})", t)
        if m:
            return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    raise ValueError("as-of date not found")


def prev_year(d: date) -> date:
    return date(d.year - 1, d.month, d.day)


def ytd_period(asof: date, year: int) -> tuple[date, date]:
    end_month = 12 if asof.month == 1 else asof.month - 1
    return date(year, 1, 1), date(year, end_month, calendar.monthrange(year, end_month)[1])


class Collector:
    def __init__(self, url: str, asof: date, version: str):
        self.url, self.asof, self.version, self.rows = url, asof, version, []

    def add(self, table, metric, value, unit, *, as_of_date, scheme="", card_type="", region="",
            channel="", flow_type="", period_start="", period_end="", period_type="stock", raw_label=""):
        if value is None:
            return
        self.rows.append(dict(
            as_of_date=as_of_date.isoformat(), table=table, metric=metric, scheme=scheme, card_type=card_type,
            region=region, value=value, unit=unit, source_url=self.url, channel=channel, flow_type=flow_type,
            period_type=period_type, period_start=str(period_start), period_end=str(period_end),
            release_as_of=self.asof.isoformat(), release_version=self.version, table_title=TITLES[table],
            raw_label=raw_label,
        ))


def parse_t1(t, c: Collector):
    dates = [prev_year(c.asof), c.asof]
    section, scheme = "circulation", "total"
    infra = {
        "number of pos": ("pos_terminals", "units", "total"), "commercial": ("pos_terminals", "units", "merchants"),
        "banks": ("pos_terminals", "units", "banks"), "number of atm": ("atms", "units", "total"),
        "with cash distribution": ("atms", "units", "cash_out_only"),
        "with cash reception": ("atms", "units", "cash_in_out"),
        "number of commercial enterprises": ("merchants_with_acquiring", "units", ""),
        "number of users of online": ("online_banking_users", "thousand users", ""),
    }
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if len(cs) < 3:
            continue
        label = norm(cs[0]).lstrip("a") if norm(cs[0]).startswith("adebit") else norm(cs[0])
        vals = [num(x) for x in cs[-2:]]
        if label.startswith("specifications"):
            continue
        if label.startswith("quarterly"):
            section = "infra"
            qd = [re.sub(r"\s", "", x) for x in cs[-2:]]
            try:
                dates = [date(int(x[6:10]), int(x[3:5]), int(x[0:2])) for x in qd]
            except ValueError:
                print("  T1 quarterly header unparsable, using release dates:", qd)
            continue
        if label.startswith("total number of cards"):
            section, scheme, ct = "circulation", "total", "all"
        elif label.startswith("number of used cards"):
            section, scheme, ct = "used", "total", "all"
        elif section == "infra":
            key = next((k for k in infra if label.startswith(k)), None)
            if key is None:
                print("  T1 unknown infra label:", label)
                continue
            metric, unit, sub = infra[key]
            for d, v in zip(dates, vals):
                c.add("T1", metric, v, unit, as_of_date=d, card_type=sub, raw_label=cs[0])
            continue
        elif label.startswith("local"):
            scheme, ct = "local", "all"
        elif label.startswith("international"):
            scheme, ct = "international", "all"
        elif label.startswith("visa"):
            scheme, ct = "visa", "all"
        elif label.startswith("mastercard"):
            scheme, ct = "mastercard", "all"
        elif label.startswith("unionpay"):
            scheme, ct = "unionpay", "all"
        elif "credit limit" in label:
            ct = "debit_with_limit_prepaid"
        elif label == "debit":
            ct = "debit"
        elif label == "credit":
            ct = "credit"
        else:
            print("  T1 unknown label:", label)
            continue
        metric = "cards_in_circulation" if section == "circulation" else "cards_used"
        for d, v in zip(dates, vals):
            c.add("T1", metric, v, "thousand cards", as_of_date=d, scheme=scheme, card_type=ct, raw_label=cs[0])


def parse_t2(t, c: Collector):
    cols = [("cards_in_circulation", "debit"), ("cards_in_circulation", "credit"),
            ("cards_in_circulation", "debit_with_limit_prepaid"), ("cards_used", "debit"),
            ("cards_used", "credit"), ("cards_used", "debit_with_limit_prepaid")]
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if len(cs) != 7:
            continue
        reg = region_of(cs[0])
        if not reg:
            continue
        for (metric, ct), v in zip(cols, cs[1:]):
            c.add("T2", metric, num(v), "thousand cards", as_of_date=c.asof, scheme="total", card_type=ct,
                  region=reg, raw_label=cs[0])


def parse_t3(t, c: Collector):
    cols = [("pos_terminals", "units"), ("atms", "units"), ("merchants_with_acquiring", "units"),
            ("merchant_outlets", "units")]
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if len(cs) != 5:
            continue
        reg = region_of(cs[0])
        if not reg:
            continue
        for (metric, unit), v in zip(cols, cs[1:]):
            c.add("T3", metric, num(v), unit, as_of_date=c.asof, region=reg, raw_label=cs[0])


def year_label(s: str) -> int | None:
    s = re.sub(r"\s", "", s)
    return int(s) if re.fullmatch(r"20\d\d", s) else None


def parse_t4(t, c: Collector):
    year, metric, unit = None, None, None
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if len(cs) == 1 and year_label(cs[0]):
            year = year_label(cs[0])
            continue
        if len(cs) != 3 or year is None:
            continue
        label = norm(cs[0])
        if label.startswith("number of transactions"):
            metric, unit, scheme = "txn_count", "thousand transactions", "total"
        elif label.startswith("volume"):
            metric, unit, scheme = "txn_value", "mln KZT", "total"
        elif label.startswith("local"):
            scheme = "local"
        elif label.startswith("international"):
            scheme = "international"
        elif label.startswith("visa"):
            scheme = "visa"
        elif label.startswith("mastercard"):
            scheme = "mastercard"
        elif label.startswith("unionpay"):
            scheme = "unionpay"
        else:
            print("  T4 unknown label:", label)
            continue
        ps, pe = ytd_period(c.asof, year)
        for flow, v in zip(["cashless", "cash_withdrawal"], cs[1:]):
            c.add("T4", metric, num(v), unit, as_of_date=pe, scheme=scheme, region="KZ-issued, in+outside KZ",
                  flow_type=flow, period_start=ps, period_end=pe, period_type="ytd", raw_label=cs[0])


FLOW_COLS = [("txn_count", "thousand transactions", "cashless"), ("txn_value", "mln KZT", "cashless"),
             ("txn_count", "thousand transactions", "cash_withdrawal"), ("txn_value", "mln KZT", "cash_withdrawal")]


def parse_t5(t, c: Collector):
    year = (c.asof.replace(day=1) - pd.Timedelta(days=1)).year
    ps, pe = ytd_period(c.asof, year)
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if len(cs) != 5:
            continue
        reg = region_of(cs[0])
        if not reg:
            continue
        for (metric, unit, flow), v in zip(FLOW_COLS, cs[1:]):
            c.add("T5", metric, num(v), unit, as_of_date=pe, region=reg, flow_type=flow, period_start=ps,
                  period_end=pe, period_type="ytd", raw_label=cs[0])


def parse_channel_table(t, c: Collector, table: str, region_label: str, has_years: bool):
    year = None if has_years else (c.asof.replace(day=1) - pd.Timedelta(days=1)).year
    for tr in t.find_all("tr"):
        cs = cells(tr)
        if has_years and len(cs) == 1 and year_label(cs[0]):
            year = year_label(cs[0])
            continue
        if len(cs) != 5 or year is None:
            continue
        ch = channel_of(cs[0])
        if not ch:
            continue
        ps, pe = ytd_period(c.asof, year)
        for (metric, unit, flow), v in zip(FLOW_COLS, cs[1:]):
            c.add(table, metric, num(v), unit, as_of_date=pe, region=region_label, channel=ch, flow_type=flow,
                  period_start=ps, period_end=pe, period_type="ytd", raw_label=cs[0])


def parse_release(path: Path, url: str, version: str) -> list[dict]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    asof = release_asof(soup)
    c = Collector(url, asof, version)
    ts = soup.find_all("table")
    assert len(ts) == 7, f"{path.name}: expected 7 tables, got {len(ts)}"
    parse_t1(ts[0], c)
    parse_t2(ts[1], c)
    parse_t3(ts[2], c)
    parse_t4(ts[3], c)
    parse_t5(ts[4], c)
    parse_channel_table(ts[5], c, "T6", "in KZ (KZ + foreign-issued)", has_years=False)
    parse_channel_table(ts[6], c, "T7", "outside KZ (KZ-issued)", has_years=True)
    return c.rows


# Known NBK publishing errors found by validate(); documented in docs/validation_nbk.md and docs/data_gaps.md
EXCLUDE = {  # (release_version, table): reason  -> rows dropped from clean output
    ("263", "T1"): "Table 1 values shifted by one row in source HTML (e.g. 'local systems' row holds the total)",
}
QUALITY = {  # (release_version, table, period_end year): reason -> rows kept but flagged
    ("250", "T4", 2023): "2023 H1 txn_value: local + international exceeds total by 23% in source; count block consistent",
}

KEY = ["as_of_date", "table", "metric", "scheme", "card_type", "region", "channel", "flow_type", "period_type"]


def validate(df: pd.DataFrame) -> str:
    """Subtotal checks on the latest-vintage table AND on every release (to flag specific months)."""
    out = ["# NBK data validation", "",
           "Tolerance: |diff| <= 0.1% of the parent total (values are rounded to 0.1 thousand / 0.1 mln KZT).",
           "Checks run on every release (all vintages). `FLAG` = outside tolerance.", ""]
    flags = []

    def chk(name, release, parent, parts):
        if parent is None or pd.isna(parent):
            return
        s = sum(p for p in parts if p is not None and not pd.isna(p))
        diff = parent - s
        rel = abs(diff) / parent if parent else 0
        status = "ok" if rel <= 0.001 else "FLAG"
        if status == "FLAG":
            if "Visa + MC + UnionPay" in name:
                cat = "INFO-residual"
            elif "T5 vs T6" in name:
                cat = "INFO-scope"
            else:
                cat = "ERROR"
            flags.append((cat, f"| {cat} | {release} | {name} | {parent:,.1f} | {s:,.1f} | {diff:,.1f} | {rel:.2%} |"))
        return status

    n_checks = 0
    for rel_asof, g in df.groupby("release_as_of"):
        def v(**kw):
            m = g
            for k, val in kw.items():
                m = m[m[k] == val]
            return m["value"].iloc[0] if len(m) else None

        t1 = g[g.table == "T1"]
        for d in t1.as_of_date.unique():
            for metric in ["cards_in_circulation", "cards_used"]:
                tot = v(table="T1", as_of_date=d, metric=metric, scheme="total", card_type="all")
                loc = v(table="T1", as_of_date=d, metric=metric, scheme="local", card_type="all")
                intl = v(table="T1", as_of_date=d, metric=metric, scheme="international", card_type="all")
                chk(f"T1 {metric} {d}: total = local + international", rel_asof, tot, [loc, intl]); n_checks += 1
                for sch in ["visa", "mastercard", "unionpay"]:
                    st = v(table="T1", as_of_date=d, metric=metric, scheme=sch, card_type="all")
                    parts = [v(table="T1", as_of_date=d, metric=metric, scheme=sch, card_type=ct)
                             for ct in ["debit", "credit", "debit_with_limit_prepaid"]]
                    if st is not None:
                        chk(f"T1 {metric} {d}: {sch} = debit + credit + limit/prepaid", rel_asof, st, parts); n_checks += 1
                vis = v(table="T1", as_of_date=d, metric=metric, scheme="visa", card_type="all")
                mc = v(table="T1", as_of_date=d, metric=metric, scheme="mastercard", card_type="all")
                up = v(table="T1", as_of_date=d, metric=metric, scheme="unionpay", card_type="all")
                if up is not None:
                    chk(f"T1 {metric} {d}: international = Visa + MC + UnionPay", rel_asof, intl, [vis, mc, up]); n_checks += 1
        # T2 regions
        for metric in ["cards_in_circulation", "cards_used"]:
            for ct in ["debit", "credit", "debit_with_limit_prepaid"]:
                s = g[(g.table == "T2") & (g.metric == metric) & (g.card_type == ct)]
                tot = s[s.region == "TOTAL"].value.sum()
                chk(f"T2 {metric} {ct}: TOTAL = sum of regions", rel_asof, tot, list(s[s.region != "TOTAL"].value)); n_checks += 1
            t2tot = g[(g.table == "T2") & (g.metric == metric) & (g.region == "TOTAL")].value.sum()
            t1tot = v(table="T1", as_of_date=rel_asof, metric=metric, scheme="total", card_type="all")
            chk(f"T2 vs T1 {metric}: T1 total = T2 TOTAL (debit+credit+other)", rel_asof, t1tot, [t2tot]); n_checks += 1
        # T3
        for metric in ["pos_terminals", "atms", "merchants_with_acquiring", "merchant_outlets"]:
            s = g[(g.table == "T3") & (g.metric == metric)]
            tot = s[s.region == "TOTAL"].value.sum()
            chk(f"T3 {metric}: TOTAL = sum of regions", rel_asof, tot, list(s[s.region != "TOTAL"].value)); n_checks += 1
        # T4
        for pe in g[g.table == "T4"].as_of_date.unique():
            for metric in ["txn_count", "txn_value"]:
                for flow in ["cashless", "cash_withdrawal"]:
                    kw = dict(table="T4", as_of_date=pe, metric=metric, flow_type=flow)
                    tot, loc, intl = (v(**kw, scheme=s) for s in ["total", "local", "international"])
                    chk(f"T4 {metric} {flow} {pe}: total = local + international", rel_asof, tot, [loc, intl]); n_checks += 1
                    up = v(**kw, scheme="unionpay")
                    if up is not None:
                        chk(f"T4 {metric} {flow} {pe}: international = Visa + MC + UnionPay", rel_asof, intl,
                            [v(**kw, scheme="visa"), v(**kw, scheme="mastercard"), up]); n_checks += 1
        # T5, T6, T7 sums
        for table, dim in [("T5", "region"), ("T6", "channel"), ("T7", "channel")]:
            s = g[g.table == table]
            for (pe, metric, flow), h in s.groupby(["as_of_date", "metric", "flow_type"]):
                tot = h[h[dim] == "TOTAL"].value.sum()
                chk(f"{table} {metric} {flow} {pe}: TOTAL = sum of {dim}s", rel_asof, tot,
                    list(h[h[dim] != "TOTAL"].value)); n_checks += 1
        # cross-table: T5 vs T6 (same scope: in KZ, KZ + foreign cards)
        for metric in ["txn_count", "txn_value"]:
            for flow in ["cashless", "cash_withdrawal"]:
                a = g[(g.table == "T5") & (g.region == "TOTAL") & (g.metric == metric) & (g.flow_type == flow)].value.sum()
                b = g[(g.table == "T6") & (g.channel == "TOTAL") & (g.metric == metric) & (g.flow_type == flow)].value.sum()
                chk(f"T5 vs T6 {metric} {flow}: same scope (in KZ, all issuers)", rel_asof, b, [a]); n_checks += 1

    from collections import Counter
    cnt = Counter(c for c, _ in flags)
    out.append(f"Checks run: {n_checks}. Flags: {len(flags)} ({dict(cnt)}).")
    out += ["",
            "* **ERROR** = source table internally inconsistent -> excluded or quality-flagged (see `EXCLUDE` / `QUALITY` in `src/acquire/nbk_parse.py`).",
            "* **INFO-residual** = international total exceeds Visa + MasterCard + UnionPay by 0.1-0.3%. Systematic in every release since UnionPay was broken out (v266); interpreted as other international schemes not itemised by NBK. Kept as `other_international` [calc].",
            "* **INFO-scope** = Table 5 (by region) and Table 6 (by channel) have the same stated scope but totals differ by up to ~0.3%. NBK does not explain the gap; we use T6 for channel mix and T5 for regional mix and never mix them in one ratio.",
            ""]
    if flags:
        out += ["| category | release as-of | check | parent | sum of parts | diff | rel diff |", "|---|---|---|---|---|---|---|"]
        out += [f for c, f in sorted(flags, key=lambda x: (x[0] != "ERROR", x[1]))]
    out += ["", "## Known header issues (handled by taking as-of date from narrative text)", "",
            "* Release v269 (as of 2026-02-01): Table 1 header reads 01.01.2025 / 01.01.2026.",
            "* Release v277 (as of 2026-10-01): Table 2 header reads 'As of 01.10.2025' but totals match Table 1's 2026 column.",
            "* Releases before v266 (as of 2025-11-01) do not break out UnionPay; `other_international` = international - Visa - MasterCard is derived [calc] in analysis.",
            ]
    return "\n".join(out)


def main():
    idx = list(csv.DictReader(open(RAW / "_index.csv", encoding="utf-8")))
    rows = []
    for r in idx:
        p = RAW / f"release_{r['release_id']}.html"
        rr = parse_release(p, r["url"], r["version"])
        print(r["version"], rr[0]["release_as_of"], len(rr), "rows")
        rows += rr
    df = pd.DataFrame(rows)
    (DOCS / "validation_nbk.md").write_text(validate(df), encoding="utf-8")  # validate raw, before exclusions
    drop = df.apply(lambda r: (r.release_version, r.table) in EXCLUDE, axis=1)
    print("excluded rows:", int(drop.sum()))
    df = df[~drop].copy()
    df["quality_flag"] = df.apply(
        lambda r: QUALITY.get((r.release_version, r.table, int(r.as_of_date[:4])), ""), axis=1)
    CLEAN.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN / "nbk_cards_long_allvintages.csv", index=False)
    latest = (df.sort_values("release_as_of").groupby(KEY, as_index=False, dropna=False).last())
    latest = latest[df.columns]
    latest.to_csv(CLEAN / "nbk_cards_long.csv", index=False)
    print("all vintages:", len(df), "latest:", len(latest))


if __name__ == "__main__":
    main()
