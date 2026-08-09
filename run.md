# Reproducing this repository

One documented command sequence, from a clean checkout, on Linux/macOS with Python 3.11:

```bash
git clone <this repo> eclss && cd eclss
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m pytest src/eclss_gravity/tests/ -v   # 50 regression tests, pinned to docs/derivation.md (as corrected -- see below)
python3 scripts/generate_all_figures.py                        # regenerates everything in results/
```

That single `generate_all_figures.py` call reproduces every figure in `/results/figures` and every
data table in `/results/data` from the equations in `/src/eclss_gravity`, which are themselves
pinned by regression test to the numeric values stated in `/docs/derivation.md` **as corrected by
the Phase 4 red-team** (`docs/redteam_report.md`, `docs/limitations.md` §2) — several of
`derivation.md`'s original headline numbers (the dormancy result, the `Λ_g` depth convention, the
`g*` orientation convention) were found to be wrong or overclaimed and are superseded by the code
and by `limitations.md`, not by the original prose. Read `limitations.md` §2 before trusting any
specific number quoted from `derivation.md` directly.

**Scope note:** this reproduces the closed-form analytic criteria (`derivation.md` §2-3) and the
0-D stagnant/dormancy reduction (§5.7, `dormancy.py`) in full. The general spatial 1-D
advection-diffusion-reaction PDE specified in §5.1-5.2 and §9.7 (Danckwerts boundary conditions,
recycle-loop closure, grid-convergence checks) was **not** implemented — a deliberate scope
decision, since §5.9 states the PDE is needed only to show the *consequence* of crossing the
regime boundary, not to *locate* it, and the closed-form criteria already do that. See
`limitations.md` §4.

## What each script does

- `scripts/run_regime_sweep.py` — the deterministic gravity-relevance regime map (headline figure:
  `Ga_dep`/`Lambda_g` contours vs. particle size and gravity level), the tube-diameter sensitivity
  sweep, and the headline numeric table (`derivation.md` §8.6, regenerated not copy-pasted).
- `scripts/run_dormancy_sim.py` — the 0-D stagnant-reactor dormancy simulation (`derivation.md` §5.7)
  showing accumulated deposit over a 1-year dormancy period at Earth/Mars/Moon gravity, and the
  Rayleigh-number convection-onset comparison across geometries and gravity levels.
- `scripts/run_monte_carlo.py` — 10,000-sample Monte Carlo propagation of the dominant parameter
  uncertainties (bimodal particle-size distribution, buoyant density, tube diameter, temperature)
  onto the crossover gravity level `g*` and `P(Ga_dep > 1 | gravity level)`, reported per
  particle-size branch. Fixed seed (`eclss_gravity.uncertainty.RNG_SEED = 20260803`) for exact
  reproducibility.
- `scripts/run_sensitivity_checks.py` — the four one-at-a-time structural checks `derivation.md`
  §7.3(c) calls mandatory (orientation factor, detachment exponent, `Ra_c` ×0.5/×2, growth
  modulation `φ(g)`). Two of its results are consequential enough that they are quoted in
  `docs/limitations.md` §4 and the manuscript rather than left in the CSV.
- `scripts/run_extended_scenarios.py` — the two scenarios that were disclosed-but-unexplored
  through Phase 6: negative buoyant density (rising aggregates, assumption A11) and a
  duty-cycled pumped/stagnant schedule (assumption A3).

## Analysing bench-validation data (only if someone runs the physical test)

Not part of the figure pipeline. `src/eclss_gravity/validation_compare.py` ingests the CSV
described in `validation/README.md` §A.7 and reports whether an observed convection onset is
consistent with the model's `Ra_c = 1708`:

```bash
PYTHONPATH=src python3 -m eclss_gravity.validation_compare your_data.csv
PYTHONPATH=src python3 -m eclss_gravity.validation_compare --self-test   # synthetic-data check
```

## Reproducibility guarantees

- All dependencies pinned in `requirements.txt` (numpy 1.26.4, scipy 1.13.1, matplotlib 3.8.4,
  pandas 2.2.2, pytest 8.2.0).
- All randomness seeded (`RNG_SEED` in `uncertainty.py`).
- All 50 tests in `src/eclss_gravity/tests/` regress against numeric values documented in
  `docs/derivation.md` and corrected in `docs/limitations.md` §2. The headline result is no longer a
  single point estimate (the original `g* = 0.238 g_Earth` claim was found over-precise by ~50x and
  convention-dependent — see `docs/redteam_report.md` Finding 4.8); it is now reported as a
  distribution: single-cell wall delivery is comparable to within an order of magnitude across the
  Earth-to-Moon gravity range (`P(Ga_dep>1)` = 0.61/0.30/0.12 at Earth/Mars/Moon), while floc/
  aggregate (>7 um) delivery is gravity-dominated by 2-3 orders of magnitude at every gravity level
  tested.
- No network access is required to run any of this — everything here is self-contained modeling
  code. (Network access *was* required, and was partially blocked, for the literature research that
  grounds the parameter values — see `docs/decision_log.md` and `docs/derivation.md` §0.2 for that
  constraint, which is a data-provenance issue, not a reproducibility issue for the code itself.)

## Repository layout

See the top-level `README`-equivalent in `docs/ices_target.md` (target venue/track) and
`docs/problem_statement.md` (the research question), or start at `docs/decision_log.md` for the
full audit trail of how this program arrived at this problem and this model.
