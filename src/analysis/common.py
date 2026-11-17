"""Shared loaders, derivations and chart styling for the analysis modules.

Every derived number produced here is a [calc] on NBK / Kaspi source data. Helpers return pandas objects;
provenance strings are built with `src_nbk()` / `src_kaspi()` so charts and markdown cite identically.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data" / "clean"
CHARTS = ROOT / "outputs" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

NBK_INDEX = "https://www.nationalbank.kz/en/news/elektronnye-bankovskie-uslugi"
KASPI_20F = "https://ir.kaspi.kz/media/Form_20-F_{y}.pdf"
WINDOW_START = pd.Timestamp("2024-10-01")  # 24-month analysis window for stocks: 2024-10-01 .. 2026-10-01
LATEST = pd.Timestamp("2026-10-01")

# ---------- loading ----------

def nbk() -> pd.DataFrame:
    df = pd.read_csv(CLEAN / "nbk_cards_long.csv", dtype={"release_version": str}, keep_default_na=False,
                     na_values=[""])
    for c in ["scheme", "card_type", "region", "channel", "flow_type", "quality_flag"]:
        df[c] = df[c].fillna("")
    df["as_of_date"] = pd.to_datetime(df["as_of_date"])
    return df


def kaspi() -> pd.DataFrame:
    return pd.read_csv(CLEAN / "kaspi_kpis.csv")


def population() -> pd.DataFrame:
    return pd.read_csv(CLEAN / "population_by_region.csv")


def release_url(df: pd.DataFrame, as_of_release: str) -> str:
    return df.loc[df.release_as_of == as_of_release, "source_url"].iloc[0]


# ---------- stock series (Table 1) ----------

def t1(df: pd.DataFrame, metric: str, scheme: str, card_type: str = "all") -> pd.Series:
    s = df[(df.table == "T1") & (df.metric == metric) & (df.scheme == scheme) & (df.card_type == card_type)]
    return s.set_index("as_of_date").value.sort_index()


def t1_panel(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Cards by scheme (columns) over time; adds other_international [calc] = international - Visa - MC - UnionPay."""
    p = pd.DataFrame({s: t1(df, metric, s) for s in ["total", "local", "international", "visa", "mastercard", "unionpay"]})
    p["other_international"] = p["international"] - p[["visa", "mastercard"]].sum(axis=1) - p["unionpay"].fillna(0)
    return p


# ---------- flows (Tables 4-7 are YTD cumulative) ----------

def ytd(df: pd.DataFrame, table: str, metric: str, flow: str, **filters) -> pd.Series:
    s = df[(df.table == table) & (df.metric == metric) & (df.flow_type == flow)]
    for k, v in filters.items():
        s = s[s[k] == v]
    s = s[s.quality_flag == ""]
    return s.set_index("as_of_date").value.sort_index()


def monthly_from_ytd(s: pd.Series) -> pd.Series:
    """[calc] monthly flow = YTD(m) - YTD(m-1) within a calendar year; January = YTD(Jan).
    Months whose previous YTD point is missing are dropped (never interpolated)."""
    out = {}
    for d, v in s.items():
        if d.month == 1:
            out[d] = v
            continue
        prev = d - pd.offsets.MonthEnd(1)
        if prev in s.index:
            out[d] = v - s[prev]
    return pd.Series(out).sort_index()


def to_month_start(s: pd.Series) -> pd.Series:
    """For plotting: month-end index -> first day of month, so bars sit on their own month label."""
    s = s.copy()
    s.index = s.index.to_period("M").to_timestamp()
    return s


def full_year(s: pd.Series, year: int) -> float | None:
    d = pd.Timestamp(f"{year}-12-31")
    return s.get(d)


# ---------- provenance strings ----------

def src_nbk(tables: str, as_of: str, extra: str = "") -> str:
    return (f"Source: National Bank of Kazakhstan, 'Electronic banking services / payment cards' monthly releases, "
            f"{tables}; as of {as_of}. {NBK_INDEX}" + (f" {extra}" if extra else ""))


def src_kaspi(fy: int, pages: str) -> str:
    return f"Source: Kaspi.kz Form 20-F FY{fy}, {pages}. {KASPI_20F.format(y=fy)}"


# ---------- chart styling ----------
ACCENT = "#1F4E9E"     # single accent (network blue)
GREY = "#8C8C8C"
LIGHT = "#C9CED6"
DARK = "#222222"
RED = "#C0392B"        # used sparingly for the 'threat' series (local / Kaspi)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#888888", "axes.labelcolor": DARK, "xtick.color": DARK, "ytick.color": DARK,
    "axes.titleweight": "bold", "axes.titlesize": 12.5, "axes.titlelocation": "left", "figure.dpi": 150,
    "savefig.dpi": 200, "legend.frameon": False,
})


def new_fig(w=10, h=5.6):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax


def finish(fig, ax, title: str, source: str, fname: str, subtitle: str | None = None, fig_legend: dict | None = None):
    """Action title (insight) top-left, optional unit subtitle, wrapped source footnote bottom-left.
    fig_legend: dict(handles=..., labels=..., ncol=...) drawn centred above the footnote.
    Also saves a 'deck' variant (no title / footnote: the slide carries both) to outputs/charts/deck/."""
    import textwrap
    w_in = fig.get_size_inches()[0]
    st = fig.suptitle(title, x=0.01, y=0.985, ha="left", va="top", fontsize=13.5, fontweight="bold", color=DARK)
    if subtitle:
        ax.set_title(subtitle, loc="left", fontsize=10, fontweight="normal", color="#555555", pad=8)
    foot = "\n".join(textwrap.wrap(source, int(w_in * 17)))
    ft = fig.text(0.01, 0.01, foot, ha="left", va="bottom", fontsize=6.8, color="#555555")
    n = foot.count("\n") + 1
    bottom = 0.03 + 0.024 * n
    leg = None
    if fig_legend:
        leg = fig.legend(fig_legend["handles"], fig_legend["labels"], loc="lower center", ncol=fig_legend.get("ncol", 4),
                         bbox_to_anchor=(0.5, bottom), fontsize=8.5, frameon=False)
        bottom += 0.065
    fig.tight_layout(rect=(0, bottom, 1, 0.945))
    fig.savefig(CHARTS / fname, facecolor="white")
    # deck variant
    st.set_visible(False)
    ft.set_visible(False)
    b2 = 0.0
    if leg is not None:
        leg.set_bbox_to_anchor((0.5, 0.0))
        b2 = 0.07
    fig.tight_layout(rect=(0, b2, 1, 1))
    (CHARTS / "deck").mkdir(exist_ok=True)
    fig.savefig(CHARTS / "deck" / fname, facecolor="white")
    plt.close(fig)
    return CHARTS / fname


# ---------- metric registry (feeds outputs/metrics.csv -> findings / storyline) ----------
import json  # noqa: E402

METRICS_CSV = ROOT / "outputs" / "metrics.csv"


class Metrics:
    """Collects headline numbers with label (data / calc / estimate) and provenance."""

    def __init__(self, module: str):
        self.module, self.rows = module, []

    def add(self, key: str, value: float, unit: str, label: str, source: str, note: str = ""):
        assert label in {"data", "calc", "estimate"}, label
        self.rows.append(dict(module=self.module, key=key, value=value, unit=unit, label=label, source=source,
                              note=note))
        return value

    def save(self):
        old = pd.read_csv(METRICS_CSV) if METRICS_CSV.exists() else pd.DataFrame()
        if len(old):
            old = old[old.module != self.module]
        out = pd.concat([old, pd.DataFrame(self.rows)], ignore_index=True)
        out.to_csv(METRICS_CSV, index=False)
        for r in self.rows:
            v = r["value"]
            vs = f"{v:,.3f}" if isinstance(v, float) and abs(v) < 10 else f"{v:,.1f}"
            print(f"  [{r['label']}] {r['key']}: {vs} {r['unit']}")


def pct(a, b):
    return 100.0 * a / b
