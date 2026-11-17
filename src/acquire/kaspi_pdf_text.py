"""Extract per-page text from Kaspi 20-F PDFs to data/raw/kaspi/<name>.pages.txt (page markers kept)."""
import sys
from pathlib import Path
import pdfplumber

RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "kaspi"
for pdf in sorted(RAW.glob("Form_20-F_*.pdf")):
    out = pdf.with_suffix(".pages.txt")
    if out.exists():
        continue
    with pdfplumber.open(pdf) as doc, open(out, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc.pages, start=1):
            f.write(f"\n=====PAGE {i}=====\n")
            f.write(page.extract_text() or "")
    print("done", pdf.name, flush=True)
