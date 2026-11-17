"""Population by region (Bureau of National Statistics, stat.gov.kz) -> data/clean/population_by_region.csv

Source page: https://stat.gov.kz/en/industries/social-statistics/demography/publications/520987/
 ('Population of the Republic of Kazakhstan by gender and type of locality (as of October 1, 2026)', file 'Population by region.xlsx').
Unit is NOT stated in the file; values are thousand persons, inferred from magnitude (Almaty city 2,392 -> ~2.4 mln).
Total population = sum of urban + rural over regions [calc].
"""
from pathlib import Path
import unicodedata
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "raw" / "stat" / "population_by_region_2026-10-01.xlsx"
PAGE = "https://stat.gov.kz/en/industries/social-statistics/demography/publications/520987/"
CYR = str.maketrans({"А": "A", "К": "K", "М": "M", "О": "O", "е": "e", "Е": "E", "о": "o", "а": "a", "к": "k"})
MAP = {"Abay": "Abai", "Akmola": "Akmola", "Aktobe": "Aktobe", "Almaty": "Almaty region", "Atyrau": "Atyrau",
       "Batys Kazakhstan": "West Kazakhstan", "Zhambyl": "Jambyl", "Zhetisu": "Zhetysu", "Karagandy": "Karaganda",
       "Kostanay": "Kostanay", "Kyzylorda": "Kyzylorda", "Mangystau": "Mangystau", "Pavlodar": "Pavlodar",
       "Soltustik Kazakhstan": "North Kazakhstan", "Turkistan": "Turkestan", "Ulytau": "Ulytau",
       "Shygys Kazakhstan": "East Kazakhstan", "Astana city": "Astana city", "Almaty city": "Almaty city",
       "Shymkent city": "Shymkent city"}

raw = pd.read_excel(SRC, header=None).iloc[2:]
rows = []
for _, r in raw.iterrows():
    name = str(r[0]).translate(CYR).strip()
    reg = MAP[name]
    urban, rural = float(r[1]), (0.0 if pd.isna(r[2]) else float(r[2]))
    rows.append(dict(as_of_date="2026-10-01", region=reg, source_region_name=str(r[0]).strip(), urban=urban, rural=rural,
                     population=urban + rural, unit="thousand persons (inferred)", source_url=PAGE,
                     table="Population by region.xlsx (Лист1)", note="population = urban + rural [calc]"))
df = pd.DataFrame(rows)
df.to_csv(ROOT / "data" / "clean" / "population_by_region.csv", index=False)
print(df[["region", "population"]].to_string(), "\nTOTAL [calc]", round(df.population.sum(), 1))
