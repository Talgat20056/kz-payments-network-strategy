"""Build outputs/kz_payments_strategy.pptx from outputs/storyline.md (single source of truth for slide text).

Layout: 16:9, white background, one accent colour, action title top-left, source footnote bottom-left, page number
bottom-right. Charts come from outputs/charts/deck/ (variants without embedded title/footnote).
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / "outputs" / "storyline.md"
CH = ROOT / "outputs" / "charts" / "deck"
OUT = ROOT / "outputs" / "kz_payments_strategy.pptx"

ACCENT = RGBColor(0x1F, 0x4E, 0x9E)
DARK = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x66, 0x66, 0x66)
LIGHTBG = RGBColor(0xF3, 0xF5, 0xF8)
FONT = "Arial"
W, H = Inches(13.333), Inches(7.5)
MX = Inches(0.5)


# ---------------- parse storyline ----------------
def parse(md: str):
    slides = []
    for block in md.split("### Slide ")[1:]:
        head, *rest = block.split("\n")
        num, _, section = head.partition(" — ")
        body = "\n".join(rest)
        title = re.search(r"\*\*Title:\*\*\s*(.+)", body).group(1).strip()
        chart = re.search(r"\*\*Chart:\*\*\s*(.+)", body).group(1).strip()
        source = re.search(r"\*\*Source:\*\*\s*(.+)", body).group(1).strip()
        m = re.search(r"`outputs/charts/([^`]+)`", chart)
        bullets = [l[2:].strip() for l in body.split("### Backup")[0].split("\n") if l.startswith("- ")]
        table = [l for l in body.split("\n") if l.startswith("|")]
        slides.append(dict(num=int(num), section=section.strip(), title=title, chart=m.group(1) if m else None,
                           source=source, bullets=bullets, table=table))
    backups = []
    if "### Backup slides" in md:
        for l in md.split("### Backup slides")[1].split("\n"):
            if l.startswith("- B"):
                bid, title, chart, src = [x.strip() for x in l[2:].split(" | ")]
                backups.append(dict(section=f"Backup {bid}", title=title, chart=chart.strip("`"), source=src, bullets=[],
                                    table=[]))
    return slides, backups


# ---------------- text helpers ----------------
def add_runs(par, text, size, color=DARK, bold_all=False):
    """Render **bold** markdown segments as bold runs; strip backticks."""
    text = re.sub(r"(?<!\*)\*(?!\*)", "", text.replace("`", ""))
    for i, seg in enumerate(re.split(r"\*\*", text)):
        if not seg:
            continue
        r = par.add_run()
        r.text = seg
        r.font.size = Pt(size)
        r.font.name = FONT
        r.font.bold = bold_all or (i % 2 == 1)
        r.font.color.rgb = color


def est_height_in(paras: list[str], width_in: float, size: float, space_after_pt: float = 6) -> float:
    """Conservative text height estimate (Arial avg glyph width ≈ 0.52 em)."""
    cpl = max(1, int(width_in * 72 / (size * 0.52)))
    lines = sum(max(1, math.ceil(len(re.sub(r"\*\*|`", "", p)) / cpl)) for p in paras)
    return lines * size * 1.2 / 72 + len(paras) * space_after_pt / 72


def fit_size(paras, width_in, height_in, start=13, floor=9):
    s = start
    while s > floor and est_height_in(paras, width_in, s) > height_in:
        s -= 0.5
    return s


def textbox(slide, x, y, w, h, paras, size, color=DARK, bullet=True, space_after=6, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    for i, p in enumerate(paras):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.space_after = Pt(space_after)
        add_runs(par, ("▪  " if bullet else "") + p, size, color)
    return tb


# ---------------- slide furniture ----------------
def furniture(prs, slide, title, source, page, total, section):
    # accent marker + title
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, MX, Inches(0.42), Inches(0.08), Inches(0.62))
    bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT; bar.line.fill.background()
    tsize = 24 if len(title) <= 70 else 21
    textbox(slide, MX + Inches(0.2), Inches(0.3), W - 2 * MX - Inches(0.2), Inches(0.9), [title], tsize, bullet=False,
            anchor=MSO_ANCHOR.MIDDLE).text_frame.paragraphs[0].runs[0].font.bold = True
    for r in slide.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.bold = True
    textbox(slide, MX + Inches(0.2), Inches(0.08), Inches(6), Inches(0.25), [section.upper()], 9, color=ACCENT, bullet=False)
    line = slide.shapes.add_connector(1, MX, Inches(1.28), W - MX, Inches(1.28))
    line.line.color.rgb = RGBColor(0xC9, 0xCE, 0xD6); line.line.width = Pt(0.75)
    # footnote + page number
    fsize = 8 if len(source) < 330 else 7
    textbox(slide, MX, Inches(6.78), Inches(11.4), Inches(0.62), ["Source: " + source], fsize, color=GREY, bullet=False,
            space_after=0, anchor=MSO_ANCHOR.BOTTOM)
    textbox(slide, W - MX - Inches(0.8), Inches(7.05), Inches(0.8), Inches(0.3), [f"{page} / {total}"], 9, color=GREY,
            bullet=False).text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


def chart_slide(prs, s, page, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    furniture(prs, slide, s["title"], s["source"], page, total, s["section"])
    img = CH / s["chart"]
    with Image.open(img) as im:
        ar = im.height / im.width
    top, max_h = Inches(1.45), Inches(5.25)
    if s["bullets"]:
        cw = Inches(8.1)
        ch = Emu(int(cw * ar))
        if ch > max_h:
            ch = max_h; cw = Emu(int(ch / ar))
        slide.shapes.add_picture(str(img), MX, top, cw, ch)
        bx = MX + cw + Inches(0.3)
        bw_in = (W - MX - bx) / 914400
        box_h = max(ch, Inches(3.6))
        size = fit_size(s["bullets"], bw_in - 0.3, box_h / 914400 - 0.3, start=14)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, top, W - MX - bx, box_h)
        box.fill.solid(); box.fill.fore_color.rgb = LIGHTBG; box.line.fill.background()
        textbox(slide, bx + Inches(0.12), top + Inches(0.12), W - MX - bx - Inches(0.24), box_h - Inches(0.24),
                s["bullets"], size)
    else:
        ch = max_h
        cw = Emu(int(ch / ar))
        slide.shapes.add_picture(str(img), int((W - cw) / 2), top, cw, ch)
    return slide


def exec_slide(prs, s, page, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    furniture(prs, slide, s["title"], s["source"], page, total, s["section"])
    y = Inches(1.55)
    rowh = Inches(1.6)
    for i, b in enumerate(s["bullets"]):
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", b)
        lead, rest = (m.group(1), m.group(2)) if m else (b, "")
        num = slide.shapes.add_shape(MSO_SHAPE.OVAL, MX, y + Inches(0.2), Inches(0.55), Inches(0.55))
        num.fill.solid(); num.fill.fore_color.rgb = ACCENT; num.line.fill.background()
        tf = num.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        add_runs(tf.paragraphs[0], str(i + 1), 16, RGBColor(255, 255, 255), bold_all=True)
        textbox(slide, MX + Inches(0.8), y + Inches(0.12), Inches(3.6), rowh - Inches(0.2), [lead], 17, color=ACCENT,
                bullet=False)
        for r in slide.shapes[-1].text_frame.paragraphs[0].runs:
            r.font.bold = True
        size = fit_size([rest], 7.7, 1.35, start=14)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, MX + Inches(4.55), y, W - 2 * MX - Inches(4.55), rowh - Inches(0.15))
        box.fill.solid(); box.fill.fore_color.rgb = LIGHTBG; box.line.fill.background()
        textbox(slide, MX + Inches(4.7), y + Inches(0.08), W - 2 * MX - Inches(4.85), rowh - Inches(0.3), [rest], size,
                bullet=False, anchor=MSO_ANCHOR.MIDDLE)
        y += rowh + Inches(0.05)
    return slide


def rec_slide(prs, s, page, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    furniture(prs, slide, s["title"], s["source"], page, total, s["section"])
    rows = [[c.strip() for c in r.strip("|").split("|")] for r in s["table"] if not re.match(r"^\|[-\s|]+\|$", r)]
    nr, nc = len(rows), len(rows[0])
    widths = [0.35, 4.6, 2.55, 1.85, 2.98]
    tbl = slide.shapes.add_table(nr, nc, MX, Inches(1.45), Inches(sum(widths)), Inches(4.3)).table
    for j, wdt in enumerate(widths):
        tbl.columns[j].width = Inches(wdt)
    tbl.rows[0].height = Inches(0.42)
    for i in range(1, nr):
        tbl.rows[i].height = Inches(1.15)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            tf = cell.text_frame; tf.word_wrap = True
            tf.paragraphs[0].text = ""
            if i == 0:
                add_runs(tf.paragraphs[0], val, 11, RGBColor(255, 255, 255), bold_all=True)
                cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT
            else:
                add_runs(tf.paragraphs[0], val, 10.5 if j in (1, 4) else 10.5)
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHTBG if i % 2 else RGBColor(255, 255, 255)
    notes = [b for b in s["bullets"]]
    textbox(slide, MX, Inches(5.95), W - 2 * MX, Inches(0.8), notes, 11)
    return slide


def main():
    slides, backups = parse(STORY.read_text(encoding="utf-8"))
    assert 8 <= len(slides) <= 10, len(slides)
    for s in slides:
        assert len(s["title"].split()) <= 15, (s["num"], s["title"])
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    total = len(slides) + len(backups)
    for i, s in enumerate(slides, start=1):
        if s["table"]:
            rec_slide(prs, s, i, total)
        elif s["chart"] is None:
            exec_slide(prs, s, i, total)
        else:
            chart_slide(prs, s, i, total)
    for j, b in enumerate(backups, start=len(slides) + 1):
        chart_slide(prs, b, j, total)
    prs.save(OUT)
    print(f"saved {OUT} ({total} slides)")


if __name__ == "__main__":
    main()
