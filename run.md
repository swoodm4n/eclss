# Reproducing this repository

One documented command sequence, from a clean checkout, on Linux/macOS with Python 3.11:

```bash
git clone <this repo> eclss && cd eclss
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m pytest src/eclss_gravity/tests/ -v   # 28 regression tests, all pinned to docs/derivation.md
python3 scripts/generate_all_figures.py                        # regenerates everything in results/
```

That single `generate_all_figures.py` call reproduces every figure in `/results/figures` and every
data table in `/results/data` from the equations in `/src/eclss_gravity`, which are themselves
pinned by regression test to the exact numeric values stated in `/docs/derivation.md`.

## What each script does

- `scripts/run_regime_sweep.py` — the deterministic gravity-relevance regime map (headline figure:
  `Ga_dep`/`Lambda_g` contours vs. particle size and gravity level), the tube-diameter sensitivity
  sweep, and the headline numeric table (`derivation.md` §8.6, regenerated not copy-pasted).
- `scripts/run_dormancy_sim.py` — the 0-D stagnant-reactor dormancy simulation (`derivation.md` §5.7)
  showing accumulated deposit over a 1-year dormancy period at Earth/Mars/Moon gravity, and the
  Rayleigh-number convection-onset comparison across geometries and gravity levels.
- `scripts/run_monte_carlo.py` — 10,000-sample Monte Carlo propagation of the dominant parameter
  uncertainties (bimodal particle-size distribution, buoyant density, tube diameter, temperature)
  onto the crossover gravity level `g*` and `P(Ga_dep > 1 | gravity level)`. Fixed seed
  (`eclss_gravity.uncertainty.RNG_SEED = 20260803`) for exact reproducibility.

## Reproducibility guarantees

- All dependencies pinned in `requirements.txt` (numpy 1.26.4, scipy 1.13.1, matplotlib 3.8.4,
  pandas 2.2.2, pytest 8.2.0).
- All randomness seeded (`RNG_SEED` in `uncertainty.py`).
- All 28 tests in `src/eclss_gravity/tests/` regress against the exact numeric values documented in
  `docs/derivation.md`, including its headline result (the single-cell WPA-line crossover gravity
  `g* ≈ 0.238 g_Earth`, between lunar and Mars gravity).
- No network access is required to run any of this — everything here is self-contained modeling
  code. (Network access *was* required, and was partially blocked, for the literature research that
  grounds the parameter values — see `docs/decision_log.md` and `docs/derivation.md` §0.2 for that
  constraint, which is a data-provenance issue, not a reproducibility issue for the code itself.)

## Repository layout

See the top-level `README`-equivalent in `docs/ices_target.md` (target venue/track) and
`docs/problem_statement.md` (the research question), or start at `docs/decision_log.md` for the
full audit trail of how this program arrived at this problem and this model.
