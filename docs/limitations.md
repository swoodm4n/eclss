# Known Limitations

This file is the authoritative, current account of this program's limitations. It supersedes its
own pre-Phase-4 version (see `decision_log.md` for the superseded text if needed). Section-by-section
physics assumptions and their validity ranges are documented exhaustively in `derivation.md` §6
(27 numbered items, A1-A27) — not duplicated here except where Phase 4 changed a grade.

## 1. Standing, unresolved: no scholarly full text has been read in this entire program

Every citation in every document (`gap_register.md`, `novelty_adjudication.md`, `problem_statement.md`,
`derivation.md`, `redteam_report.md`) was found via `WebSearch`. This sandbox's network policy blocks
`WebFetch` to every scholarly host tested across three independent attempts (Phase 2, Phase 3, Phase 4):
`ntrs.nasa.gov`, `ttu-ir.tdl.org`, `biorxiv.org`, `arxiv.org`, `ices.space`, `sciencedirect.com`,
`nature.com`, `mdpi.com`, `ncbi.nlm.nih.gov`, `engineering.purdue.edu`, `frontiersin.org`,
`biocolloid.mcgill.ca`, `esurf.copernicus.org` — all return HTTP 403 at the proxy (policy denial, not
a site-side block). **No full text has been read in producing this program.** Every content claim
about a cited paper is `[snippet-level]`, not read-the-PDF fidelity. This is raised repeatedly (three
separate phases independently hit and reported it) because it is the single highest-value action
available before submission: clearing it would let this program verify, rather than merely cite,
its own most load-bearing sources — starting with Li/Busscher/van der Mei (2011) on sedimentation
vs. convective-diffusion dominance (the strongest defense of `Ga_dep >> 1`) and the four colloid-
filtration papers in §3 below (which determine how the novelty claim must be worded).

## 2. Phase 4 red-team findings: what was fixed, what remains open

Full detail in `redteam_report.md` (independent adversarial review: re-derived 14 headline numbers
from scratch, reproduced 2 figures independently, ran 8 further literature searches). Summary of
disposition below; "Fixed" means the code/docs were changed and re-verified, not just acknowledged.

| # | Finding | Class | Disposition |
|---|---|---|---|
| Dormancy growth term omitted (eq 5.3) | The headline "~2.2×10⁵× lunar/Earth deposit" claim was a substrate-conversion artifact | BLOCKING | **Fixed.** `dormancy.py` now implements eq (5.3) fully. Corrected finding: deposition RATE differs ~1700× by gravity (real); long-time OUTCOME converges to ~unity ratio because g-independent growth kinetics dominate once any deposit seeds. `fig3` and its narrative rebuilt around the corrected finding. |
| `Ra_c=1708` requires a vertical destabilizing gradient | A real spacecraft line's thermal gradient is not generically vertical-from-below; a horizontal component removes the threshold entirely | BLOCKING for §3.5's "strongest result" framing | **Disclosed, not fixed.** No code change — the Rayleigh-Bénard formula itself is correct for the case it models; what's wrong is treating that case as generic. `derivation.md` A18 should be read as ❌ (upgraded from ⚠️), not ✅. The dormancy rework above already stopped relying on this as the headline, which substantially de-risks it, but the `fig4` "convection switch" figure still implicitly assumes a vertical gradient and should be captioned as conditional on that geometry, not general. |
| `Λ_g` factor-2 depth convention (R=D/2 vs. Hazen's full depth) | Flips the "100 µm floc settles at Earth, carried through at Mars/Moon" claim | SERIOUS | **Fixed.** `criteria.lambda_g` now uses full depth D. 183 µm floc used as the headline size-selective example instead (survives both conventions). Regression tests updated. |
| `Re_p` Stokes-validity unenforced in closed-form criteria | Eq (3.3)'s "radius cancels exactly" result has an unstated upper size bound (~184-335 µm depending on gravity) | SERIOUS | **Fixed.** Every closed-form function in `criteria.py` now checks `Re_p` and warns (`UserWarning`) when Stokes' law is applied outside its validity range, rather than silently returning a biased value. `fig1`/Monte Carlo now print how many grid points/samples are affected (~13%). |
| `cos θ = 1` vs. perimeter-averaged `f_θ = 1/π` give different `g*` | 0.238 `g_E` (local bound) vs. 0.749 `g_E` (physically-correct average) — the original headline used the less-defensible convention | SERIOUS | **Fixed.** `orientation_factor` is now an explicit, named parameter on every `Ga_dep`-family function; default changed to the perimeter-averaged value `derivation.md` §5.3 itself derives as correct. Both conventions are tested explicitly (`test_g_star_single_cell_wpa_is_convention_and_uncertainty_sensitive`) rather than one being silently chosen. |
| `g* = 0.238 g_E` reported as a precise point estimate | Over-precise by ~50× across the program's own assumed-parameter ranges (0.062-3.04 `g_E`); `derivation.md` §7.3(b) itself said not to do this | BLOCKING | **Fixed via reframing.** No single point value is the headline anymore. The defensible claim (adopted from `redteam_report.md`'s recommended reframe, §7 of `problem_statement.md`): single-cell wall delivery is ambiguous — comparable to within an order of magnitude — across the whole Earth-to-Moon gravity range; `P(Ga_dep>1)` = 0.61/0.30/0.12 at Earth/Mars/Moon (Monte Carlo, single-cell branch only). |
| Monte Carlo mixed two branches into one misleading statistic | Combined median/interval landed in the empty valley of a bimodal distribution where no sample sits | SERIOUS | **Fixed.** `run_monte_carlo.py` now reports per-branch (cell/diffusion vs. floc/interception) statistics and figures. |
| Regression tests were transcription checks, not physics checks | §9.6's required closed-form-vs-direct-velocity-ratio cross-check was absent; several §9 deliverables were unused ("dead") code | SERIOUS | **Fixed.** Added cross-check tests (`ga_dep_closed_form` vs. `ga_dep_direct`, `Ga_dep=min(Ga_dif,Ga_int)`, `a_c` closed-form vs. numerical root-find). Wired previously-dead functions (`ga_mot`, `entrance_length`, `stokes_validity_diameter`, `crossover_radius`) into tests. |
| Novelty framing anchored to the wrong field (two-phase flow boiling) | Colloid-filtration theory (Yao/Habibian/O'Melia 1971; Tufenkji/Elimelech 2004; Pich 1972; Belfort/Davis/Zydney 1994) already owns this decomposition and an ICES paper (SAE 2009-01-2359) already did partial-gravity particle transport in water hardware | BLOCKING for framing | **Fixed.** `problem_statement.md` §7 restates the contribution as adding a gravity axis to an established 1971-2004 transport-regime decomposition, not deriving a new criterion. New citations added to `lit/sources.bib`. |
| §5's general 1-D PDE (Danckwerts BCs, recycle closure, grid-convergence) was never implemented | `run.md`/derivation §9.7 implied it existed | SERIOUS | **Disclosed, not built.** Only the closed-form analytic criteria (§3, the actual headline deliverable — `derivation.md` §5.9 itself says the PDE isn't needed to *locate* the regime boundary, only to show consequences) and the 0-D stagnant reduction (§5.7, `dormancy.py`) were implemented. `run.md` no longer overclaims; see §4 below. |
| `A3` steady-flow assumption; `A11` `Δρ<0` (rising aggregates) never sampled | The WPA duty-cycles (not analyzed as a time-varying hybrid regime); some biofilm is reported less dense than water and would deposit on the *top* wall, inverting every deposition-location conclusion | SERIOUS | **Now explored** (`scripts/run_extended_scenarios.py`, post-Phase-4). A11: confirmed `|Ga_dep|` is sign-symmetric (fixing a real bug this exploration found — see below) and quantified that a gas-entrapping biofilm fragment (898 kg/m³, `Δρ≈-99`) would accumulate on the *top* of a horizontal line at essentially the same relative magnitude as the sinking case — no bottom-wall-only sampling strategy would detect it. A3: an illustrative (not sourced) 2h/day-pumped duty cycle shows the same growth-kinetics-dominated convergence as the pure dormancy scenario — Earth and Mars track almost identically, Moon slightly lower — consistent with, and a useful cross-check on, the Figure 3 finding. Neither exploration changes any headline claim; both are additional evidence for the "growth kinetics dominate the long-time outcome" conclusion. |
| **NEW (found via the A11 exploration): `ga_dep_closed_form` was not sign-symmetric for `Δρ<0`** | `min(Ga_dif, Ga_int)` is only the correct branch selection for `Δρ>0`; for negative buoyant density the correct selection is `max`, not `min` (both branches carry the sign of `v_s`, and dividing a negative number by a larger denominator gives a *less* negative result). The bug reported a rising-fragment magnitude ~880× too large. | BLOCKING (for any `Δρ<0` use) | **Fixed.** `criteria.ga_dep_closed_form` now selects the branch by `abs()` comparison and restores the sign; regression test added (`test_ga_dep_closed_form_sign_symmetric_for_negative_delta_rho`). This had no effect on any figure or Monte Carlo result in the manuscript, since none of them used `Δρ<0` before this exploration — caught before it reached a published claim, not after. |
| `A12` non-motile-cells assumption under-drawn | The actual ISS isolates motivating this work (*P. aeruginosa*, *Burkholderia*, *Stenotrophomonas*) are flagellated; `Ga_dep` for a motile single cell overstates gravity's role by ~500× | SERIOUS | **Partially fixed.** `criteria.ga_mot` is now tested and available for reporting; the manuscript must state prominently (not in a limitations footnote) that the single-cell `Ga_dep` result applies to non-motile/motility-repressed cells, and that motile planktonic cells are dominated by self-propulsion, not gravity, at every gravity level considered. |
| fig1 non-physical kink at `d=7 µm`; fig3 mislabelled "tank floor" | Cosmetic/labeling | MINOR | **Both fixed.** |

## 3. Standing methodology lesson (recorded once, applies going forward)

Both the Phase 2 adjudication (candidates A/B/C) and the Phase 4 red-team (this problem's own novelty
claim) found the same failure mode: absence-of-hits in a search scoped to the obviously-relevant field
(ECLSS/NTRS/spaceflight biology, then heat-transfer journals) was mistaken for absence of prior art,
when the actual disqualifying or contextualizing literature sat in an adjacent field the search never
reached (astrobiology/bioRxiv for A; colloid filtration/membrane engineering for this problem). Any
future novelty or completeness claim in this program should default to searching at least one field
laterally adjacent to the obvious one before treating a clean search as evidence.

## 4. Sensitivity checks (derivation.md §7.3(c), closed post-Phase-4)

`redteam_report.md` Finding 1.4 noted that the derivation's own "mandatory" one-at-a-time
structural checks were never implemented. `scripts/run_sensitivity_checks.py` now runs all four
(`results/data/sensitivity_checks.csv`); two produced results important enough to state here
rather than leave in a CSV:

- **Detachment exponent `n` (A27, unresolved in the literature — linear vs. exponential shear
  dependence) changes the biofilm loss timescale at the WPA nominal line by ~300×: 20 days at
  `n=1` vs. ~16 years at `n=3`.** This is a far larger sensitivity than any other parameter in
  the retention/detachment side of the model and should be read as a genuinely open question,
  not a rounding uncertainty — any claim about how long a deposit persists once formed is not
  currently defensible to better than two orders of magnitude.
- **The Figure 4 three-way gravity separation (Earth/Mars convecting, Moon not) is not robust
  to the O(1) geometric uncertainty on `Ra_c` that assumption A18 already conceded.** At
  `Ra_c × 0.5`, the same three-way split holds. At `Ra_c × 2` (still within the stated
  uncertainty for a tube rather than an infinite plane layer), Mars *also* stops convecting —
  the result degrades to a two-way split (Earth vs. Mars-and-Moon), not three-way. This
  quantifies, rather than just names, `redteam_report.md` Finding 2.5's concern that Mars sits
  only 10% above the nominal `Ra_c`.
- Two other checks were reassuring: the orientation-factor sensitivity is exactly the expected
  factor of `π` (already documented in §2's table), and the growth-modulation factor `φ(g)`
  shifts final dormancy mass by a modest, roughly proportional amount without changing the
  qualitative Earth/Mars/Moon convergence story from Figure 3.

## 5. `run.md` accuracy note

`run.md` previously stated that figure generation reproduces results "from the equations in
`/src/eclss_gravity`" without qualification. That is accurate for the closed-form criteria (§2-3) and
the 0-D dormancy reduction (§5.7) — both fully implemented and tested — but not for the general 1-D
PDE (§5.1-5.2, §9.7), which was never built (see table above). This is a deliberate scope decision
consistent with `derivation.md` §5.9 (the PDE is not needed to *locate* the regime boundary), not an
unfinished implementation, but `run.md` should be read with that scope in mind.
