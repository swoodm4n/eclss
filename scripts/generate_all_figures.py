"""Single entry point: regenerates every figure and data table in /results from a clean checkout.

Run via: python3 scripts/generate_all_figures.py  (from repo root, with .venv activated)
Or via the one-liner in run.md.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ["run_regime_sweep.py", "run_dormancy_sim.py", "run_monte_carlo.py"]


def main():
    for name in SCRIPTS:
        print(f"\n=== running scripts/{name} ===")
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT)
        if result.returncode != 0:
            print(f"FAILED: {name}", file=sys.stderr)
            sys.exit(result.returncode)
    print("\nAll figures and data tables regenerated in results/figures and results/data.")


if __name__ == "__main__":
    main()
