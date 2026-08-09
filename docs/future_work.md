# Future Work

Consolidated register of everything this program deliberately deferred, why, and what it would
take to close. Items are scattered in context across `limitations.md`, `redteam_report.md`, and
`decision_log.md`; this file is the single place to see what is *open* as opposed to what is
*wrong* (the latter is `limitations.md`).

Ordered by value-per-effort, highest first.

---

## 1. Read the primary sources (BLOCKED — needs external permission)

**Status: blocked, not deferred by choice.** This environment's network policy denies every
scholarly host attempted, across four independent attempts in four phases: `ntrs.nasa.gov`,
`arxiv.org`, `biorxiv.org`, `ices.space`, `sciencedirect.com`, `nature.com`, `mdpi.com`,
`ncbi.nlm.nih.gov`, `frontiersin.org`, `ttu-ir.tdl.org`, `esurf.copernicus.org`,
`biocolloid.mcgill.ca`. All return HTTP 403 at the proxy — an organization egress-policy denial,
which the proxy's own documentation says to report rather than route around.

**Consequence:** all 41 references were located and corroborated by search, but **none was read
in full**. Every content claim is at search-snippet fidelity.

**Highest-value reads, in order:**
1. Latham, Skountzos & Lawson (bioRxiv 2026.05.15.725518) — determines whether the reframed
   contribution is pre-empted; flagged as a blocking gate since Phase 2 and never cleared.
2. Li, Busscher & van der Mei (*Colloids Surf. B*, 2011) — the strongest available defense of
   the central `Ga_dep ≫ 1` result rests on this paper's snippet.
3. Yao/Habibian/O'Melia (1971), Tufenkji & Elimelech (2004), Pich (1972) — determine exactly how
   the novelty claim must be worded relative to colloid-filtration prior art.
4. Rittmann (1982) — would resolve the linear-vs-exponential detachment disagreement that
   currently makes deposit-persistence claims uncertain by ~300× (`limitations.md` §4).

**To close:** widen the environment's egress allowlist (see `code.claude.com/docs/en/claude-code-on-the-web`),
or supply the PDFs out of band.

---

## 2. Build the general 1-D advection–diffusion–reaction PDE (`derivation.md` §5.1–5.2, §9.7)

**Status: deliberately deferred, human-confirmed as future work.**

Only the closed-form analytic criteria (§2–3) and the 0-D stagnant reduction (§5.7,
`dormancy.py`) were implemented. The spatial PDE — Danckwerts inlet boundary conditions,
zero-gradient outlet, recycle-loop closure, method-of-lines discretization, grid-convergence
verification — does not exist.

**Why deferring is defensible:** `derivation.md` §5.9 states the PDE is needed only to show the
*consequence* of crossing a regime boundary, not to *locate* it, and every headline claim in the
manuscript rests on the closed-form criteria that were built. `run.md` and `limitations.md` §5
both scope this honestly rather than implying it exists.

**What it would add:** spatial resolution of where along a segment deposition concentrates,
recycle-loop behavior for UPA/MABR architectures, and the ability to model a biofilm-thickness
feedback on flow (currently excluded by assumption A4). Estimated effort: multi-hour, moderate
risk of stiffness/convergence issues given ~8 decades of timescale separation.

---

## 3. Run the Part A bench validation (needs a human with $150 and a weekend)

**Status: fully specified, never executed.** `validation/README.md` Part A, `validation/bom.csv`,
and the analysis script `eclss_gravity.validation_compare` are complete and tested; nobody has
run the physical experiment.

**Why it matters more than a typical "would be nice to validate":** it measures the critical
Rayleigh number for *tube* geometry. The model assumes the classical plane-layer `Ra_c = 1708`;
assumption A18 concedes an unquantified O(1) correction; and `limitations.md` §4 shows a factor
of 2 there collapses Figure 4's three-way gravity separation into a two-way split. **A cheap
Earth-gravity bench test can overturn a published figure**, which is an unusually high
information-per-dollar ratio.

---

## 4. Model duty-cycled operation properly (assumption A3)

**Status: partially explored, not properly modeled.** `scripts/run_extended_scenarios.py` runs an
*illustrative* 2 h/day pumped schedule with a hand-rolled forward-Euler loop, and finds the same
growth-kinetics-dominated convergence as the pure dormancy case.

**What is missing:** the duty-cycle fraction itself is ASSUMED — no sourced ISS WPA operating
schedule was found. And the criteria (`Ga_dep`, `Λ_g`, `Σ_g`) are still each evaluated at a fixed
`U`; a genuinely time-varying treatment would ask whether repeated pumped/stagnant transitions
produce behavior neither bookend predicts (e.g. resuspension on each restart transient). Finding
a sourced duty cycle is a search problem gated on item 1.

---

## 5. Extend the Monte Carlo to negative buoyant density (assumption A11)

**Status: explored deterministically, absent from the uncertainty propagation.**
`run_extended_scenarios.py` quantifies the rising-aggregate case and a sign-symmetry bug found
there has been fixed and regression-tested. But `uncertainty.py`'s sampler still draws only
positive `Δρ`, so `P(Ga_dep > 1)` in Figure 5 implicitly conditions on "the particle sinks."

**To close:** sample `Δρ` across the full sourced biofilm density range (which straddles zero:
898–1029 kg m⁻³ against water's 997) and report deposition-location probabilities (top wall vs.
bottom wall) alongside magnitude. Small, self-contained code change.

---

## 6. Resolve the two documented internal inconsistencies in `derivation.md`

Neither affects a headline result; both would be caught by a careful referee.

- **Stokes-validity threshold.** The prose states `Re_p ≈ 0.34` corresponds to 5% error, but its
  own worked example shows 5% error at `Re_p = 0.200`; solving Schiller–Naumann for exactly 5%
  gives ≈ 0.20. The code consistently uses 0.34 (≈7% error). Documented in
  `test_stokes_validity_diameter_at_the_codebase_re_p_gate`. Pick one and make prose, code, and
  the quoted `d_max` table (184/254/335 µm) agree.
- **A 0.3% units slip.** §1.2 converts the sourced 13 lb/hr using ρ = 1000 kg m⁻³ while
  everything else uses 997, so the document's `Re`/`γ_w`/`U` table differs from the code's by
  0.3% (`redteam_report.md` Finding 1.2).

---

## 7. Two-dimensional (angular) wall-deposition structure

`f_θ = 1/π` perimeter-averages away the top/bottom asymmetry of deposition in a horizontal tube.
That asymmetry is exactly what the available experimental validation targets measure (Korber et
al. 1990's 10–40× top/bottom ratio for non-motile mutants; the 2025 surface-inclination series),
so a 2-D angular model would connect the criteria to published data far more directly than the
current averaged treatment can. Natural successor once item 2 exists.

---

## 8. Verify the ICES target-cycle facts (BLOCKED with item 1)

`docs/ices_target.md` reconstructs deadlines, word limits, template requirements, and the
technical-track list from third-party pages that mirror ices.space, because ices.space itself is
proxy-blocked. The 56th cycle's call for papers had not been published as of the last check.
**Nothing in this repository should be treated as submission-ready scheduling information** until
re-verified directly.
