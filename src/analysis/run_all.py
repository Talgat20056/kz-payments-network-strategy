"""Re-run every analysis module in order (charts -> outputs/charts, numbers -> outputs/metrics.csv)."""
import importlib
import runpy

for mod in ["market_structure", "h1_activation", "h2_niches", "h3_closed_loop"]:
    print(f"== {mod}")
    runpy.run_module(f"src.analysis.{mod}", run_name="__main__")
