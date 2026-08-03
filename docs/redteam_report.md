# Phase 4 — Adversarial Red-Team Report

**Reviewer:** independent adversarial pass (no authorship stake in `derivation.md` or `src/eclss_gravity/`)
**Date:** 2026-08-03
**Inputs read in full:** `problem_statement.md`, `novelty_adjudication.md`, `derivation.md` (1652 lines),
`limitations.md`, `decision_log.md`, all 10 modules in `src/eclss_gravity/`, all 3 test files, all 4
scripts, all 5 PNG figures, all 5 CSV outputs.
**Work done:** ran the test suite; re-derived 14 headline numbers from scratch in a standalone script
with no import from the package; re-derived the `Ga_dif` prefactor, the `a_c` exponent algebra and the
`Σ_g` constant symbolically; ran controlled ablations of the dormancy model; reproduced figure 2
end-to-end from raw physics; ran 8 adversarial literature searches.

**Citation-fidelity convention inherited from `novelty_adjudication.md` §0.2.** `WebFetch` was tested
against `biocolloid.mcgill.ca`, `esurf.copernicus.org` and `calliope.dem.uniud.it` — **all returned HTTP
403 at the proxy**, in addition to the hosts already known to be blocked. **No full text was read for
this report either.** Every content claim about a cited paper below is `[snippet-level]`; existence and
venue are `[verified-existence]` where corroborated across independent result sets.

**Classification key:** **BLOCKING** = invalidates a stated core result, must be fixed before the
manuscript. **SERIOUS** = real limitation, must be disclosed prominently (abstract/limitations, not a
footnote). **MINOR** = worth noting, does not change a conclusion.

---

## 1. Verification of the "ready for implementation" chain

### 1.1 Test suite

`PYTHONPATH=src python3 -m pytest src/eclss_gravity/tests/ -v` → **28 passed in 0.38 s.** Confirmed
directly, not taken on trust.

### 1.2 Independent re-derivation (no package imports)

I rebuilt the physics from the equations in a standalone script (`scratchpad/indep.py`), starting from
`k_B`, `T`, `μ`, `ρ_f` and the sourced 13 lb/hr flow rate, and computed the Lévêque prefactor as
`1/(9^{1/3}Γ(4/3))` rather than accepting `0.538`.

| Quantity | `derivation.md` | Independent | Δ | Verdict |
|---|---|---|---|---|
| Lévêque prefactor | 0.538 | **0.538366** | 0.07 % | ✅ correct |
| `Ga_dif` prefactor | 2.925 | **2.92355** (exact); 2.92554 using the doc's rounded 0.538 | 0.07 % | ✅ correct, self-consistent |
| `Ga_dif` P1/R1/Earth | 4.2035 | **4.1943** (velocity ratio) / 4.1964 (closed form) | 0.2 % | ✅ |
| `g*_dif` P1/R1 | 2.334 m s⁻² = 0.238 `g_E` | **2.3389 m s⁻² = 0.23842 `g_E`** | 0.2 % | ✅ |
| `Ga_int` R1/Earth | 1878 | **1872.9** | 0.3 % | ✅ |
| `g*_int` R1 | 5.32 × 10⁻⁴ `g_E` | **5.3395 × 10⁻⁴** | 0.4 % | ✅ |
| `a_c` R1 | 6.8 µm | **6.765 µm** (closed form) = **6.766 µm** (direct root-find of `k_lev = k_int`) | — | ✅ eq. (2.14) algebra correct |
| `Λ_g` P3/R1/Earth | 0.932 | **0.9289** | 0.3 % | ✅ (but see F2.2) |
| `Σ_g` P4/R1/Earth | 0.101 | **0.1007** | 0.3 % | ✅ |
| `Pe_g` P1/6.35 mm/Earth | 950 | **949.1** | 0.1 % | ✅ |
| `t_settle` cell, line / tank (Earth) | 26.2 h / 51.5 d | **26.17 h / 51.51 d** | — | ✅ |
| `ΔT_c` line E/M/L | 0.345 / 0.912 / 2.088 K | **0.3448 / 0.9118 / 2.0882** | — | ✅ |
| `Ra` line ΔT=1 K, E/M/L | 4953 / 1873 / 818 | **4953.1 / 1873.2 / 817.9** | — | ✅ |
| Schiller–Naumann P5 Earth error | +33.4 % | **+33.4 %** (`Re_p` = 3.21) | — | ✅ |
| `D_ax` Taylor–Aris P1/R1 | ≈ 1250 m² s⁻¹ | **1249.5** | — | ✅ |

**Finding 1.1 — [PASS].** The core arithmetic of §§2–3 is correct and independently reproducible. The
tests are not self-consistently wrong: I got the same answers without using the code or the document's
intermediate values. **This is the strongest thing in the program.**

**Finding 1.2 — [MINOR] A 0.3 % systematic offset from a units slip.** Every discrepancy above has the
same sign and size. Its source: §1.2 converts "13 lb/hr = 5.90 kg/hr ≈ 5.90 L/hr = 1.639 × 10⁻⁶ m³ s⁻¹",
which uses ρ = 1000 kg m⁻³, while `ρ_f = 997.0` is used everywhere else (including in `hydrodynamics.py`,
which computes `Q = 5.90/997/3600 = 1.6438 × 10⁻⁶`). Consequently the document's table says `U` = 5.175 ×
10⁻², `Re` = 368, `γ_w` = 65.2 while the code (and I) get 5.191 × 10⁻², 369.2, 65.39. Harmless
numerically; fix the document so the two agree.

**Finding 1.3 — [SERIOUS] The regression tests are self-referential and do not test the one thing §9.6
asked them to.** Every test in `test_criteria.py` pins the code to a number copied from `derivation.md`
with `rel` tolerances of 0.02–0.05 — wide enough to absorb the 0.3 % offset above and any error up to
5 %. The suite verifies *transcription*, not *physics*. Specifically, §9.6 instructs: "verify it
reproduces (3.1) on the diffusion branch". **No test compares `ga_dif_closed_form` against
`ga_dep_direct`.** I did that check by hand (both give 4.1943 — it passes), but the suite does not, and
`ga_dep_direct` is never called anywhere in the repository. Add at least: closed-form vs.
velocity-ratio agreement; `Ga_dep = min(Ga_dif, Ga_int)` vs. `v_s/max(k_lev, k_int)`; `a_c` closed form
vs. root-find; `Λ_g` vs. an explicit ballistic-trajectory integration.

**Finding 1.4 — [SERIOUS] §5 — the entire 1-D advection–diffusion–reaction PDE — is not implemented.**
There is no `pde_model.py`. Equations (5.1), (5.2), (5.3), (5.11), (5.12), the method-of-lines scheme of
§5.8, the grid-convergence check, the Danckwerts BCs and the recycle closure — the whole of §9.7 — do
not exist in the repository. `dormancy.py`'s own docstring refers to "the general 1-D PDE
(`pde_model.py`)", a file that has never existed in the git history. `run.md` states that
`generate_all_figures.py` "reproduces every figure … from the equations in `/src/eclss_gravity`, which
are themselves pinned by regression test to the exact numeric values stated in `/docs/derivation.md`" —
true for §§2–3, false for §5.

Related dead code, all listed as deliverables in §9 and never called by any test, script or module:
`hydrodynamics.entrance_length` (§9.3 entrance-length warning — A2 says 23 % of the R1 segment is not
fully developed, and nothing checks it), `particles.stokes_validity_diameter` (§9.2),
`wall_transport.crossover_radius` (§9.4), `buoyancy.suspension_settling_ratio` (Ω, §9.5),
`criteria.ga_mot` (§9.6, §4.3), `criteria.ga_dep_direct`, `kinetics.detachment_rate` (§5.4),
`criteria.CriteriaResult`. §7.3(c)'s **mandatory** one-at-a-time structural checks (`f_θ` 1/π vs 1,
`n` 1 vs 3, `Ra_c` ×0.5/×2, `φ(g)` ±20 %) are implemented nowhere.

---

## 2. Equation-by-equation audit

Everything in §§2.1–2.14 and §§3.1–3.8 is dimensionally consistent; I checked each group's units
individually. The algebra I re-derived symbolically and confirmed: eq. (2.1) force balance; eq. (2.10)
Lévêque prefactor from `Γ(4/3)`; eq. (2.14)'s `1.076^{3/8}` and `1/4` exponents (verified against a
numerical root-find of `k_lev = k_int`); eq. (3.2)'s `2/(9·0.538)·(6π)^{2/3}`; eq. (3.3)'s exact `a`
cancellation; eqs. (3.4)/(3.5) as correct inversions; eq. (3.7)'s `2/15.31` from O'Neill's 1.7009 ×
6π; eq. (5.8) as the exact steady solution of `J = v_s C + D_v ∂C/∂y` with `C(0) = 0`. **No sign errors
found.** The problems are not algebraic; they are in scope, convention and enforcement.

**Finding 2.1 — [SERIOUS] `Λ_g` carries a factor-2 convention error that flips its headline claim.**
Eq. (3.6) and `criteria.lambda_g` use `R = D/2` as the distance a particle must fall. In the same
paragraph the derivation identifies `Λ_g` with the Hazen surface-overflow number, `Λ_g = v_s (LW)/Q`.
That identification requires the **full** channel depth, not the half-depth: for a rectangular duct of
height `h`, `v_s L W/Q = v_s L/(U h)`. The two conventions differ by exactly 2.

Consequence, computed independently:

| P3 (100 µm) in R1 | `R = D/2` (as coded) | `R = D` (Hazen-consistent) |
|---|---|---|
| Earth | **0.929** | **0.464** |
| Mars | 0.351 | 0.176 |
| Moon | 0.153 | 0.077 |

§3.3's stated result — "the 100 µm floc … settles out at Earth gravity but is *carried through* at Mars
and lunar gravity" — is a threshold statement (`Λ_g ≷ 1`) and it **reverses** under the Hazen-consistent
convention: 0.46 < 1 means the 100 µm floc is carried through at Earth too. The 183 µm case survives
(1.56 / 0.59 / 0.26, still Earth-only), so the *phenomenon* is real, but the specific size window quoted
in the abstract-level claim is a convention artifact. Either justify `R = D/2` as a mean-fall-distance
convention and stop calling `Λ_g = 1` a settle/no-settle threshold, or use the full depth and re-quote
the sizes. **Related:** see Finding 4.3 — Pich (1972) gives the *exact* deposition efficiency for this
exact problem, which removes the ambiguity entirely.

**Finding 2.2 — [SERIOUS] The Stokes validity range is stated but never enforced in the criteria path.**
`settling_velocity()` applies Schiller–Naumann correctly. But `ga_dif_closed_form`, `ga_int_closed_form`,
`g_star_dif`, `g_star_int` and `sigma_g` all use the pure-Stokes closed forms with **no `Re_p` check, no
correction and no warning**. Consequences:

- Every P5 (500 µm) entry in the document is computed with a `v_s` that §2.1 and A6 say is 33 % too
  high: `Ga_dep` = 1878 (§3.2), `Ω` = 8.8 (§2.2), `Λ_g` = 23.3 (§3.3), `Σ_g` = 0.276 (§3.4).
- Structurally worse: **the celebrated "particle radius cancels exactly" result (3.3) is an artifact of
  `v_s ∝ a²` and holds only while `Re_p < 0.34`,** i.e. `d < 184 / 254 / 335 µm` at Earth / Mars / Moon
  — the derivation's own eq. (2.3). Above that, `v_s` grows more slowly than `a²` while `k_int ∝ a²`
  exactly, so `Ga_int` becomes size-*dependent* (decreasing) again. §7.2's "genuinely reassuring
  structural result — above `a_c` the size uncertainty is irrelevant to the regime conclusion" therefore
  has an unstated upper bound that lies **inside** the sourced particle range (P5 = 500 µm, sourced as
  the upper bound of observed detachment).
- Quantified impact on the Monte Carlo: the large mode is lognormal (GM 110 µm, GSD 2.0), so
  `P(d > 184 µm) = 0.23` of that mode ≈ **4.5 % of all 10 000 samples are outside Stokes validity** and
  are propagated with a 5–35 % biased `v_s`.

Fix: route the closed forms through `settling_velocity()` (or gate them on `Re_p`), and state the upper
validity bound wherever eq. (3.3) is described as size-independent.

**Finding 2.3 — [SERIOUS] `cos θ = 1` vs. `f_θ = 1/π`: the headline `g*` depends on which one you use,
and the two halves of the document use different ones.** §3.2 takes `cos θ = 1` "for the bounding case";
§5.3 *derives* `f_θ = 1/π = 0.318` as the correct perimeter-averaged gravitational deposition velocity
for a horizontal tube. The criteria code uses `cos_theta = 1.0`; `dormancy.py` uses neither. Computed:

| Convention | `Ga_dep` P1/R1/Earth | `g*` |
|---|---|---|
| `cos θ = 1` (bottom of tube, local) | 4.20 | **0.238 `g_E`** — between Moon and Mars |
| `f_θ = 1/π` (tube perimeter average) | 1.34 | **0.749 `g_E`** — *above* Mars |

Both are defensible answers to different questions, but the paper's single most quoted sentence — "the
crossover from gravity-dominated to flow-dominated wall delivery falls *inside* the lunar-to-Mars
gravity window" — is **true only for the bottom-of-tube local comparison and false for the
tube-averaged one.** Under the perimeter average, gravity is sub-dominant for single-cell wall delivery
at *both* Mars and lunar gravity. This is currently buried in §7.3(c) as an optional sensitivity check
that was never run. It belongs in the abstract.

**Finding 2.4 — [BLOCKING for §3.5] `Ra_c = 1708` assumes the temperature gradient is vertical and
destabilising. For any other orientation there is no threshold at all, and the "strongest single result
in this derivation" disappears.** Rayleigh–Bénard's critical Rayleigh number exists only for a
horizontal layer heated exactly from below. A cavity with any *horizontal* component of temperature
gradient convects at arbitrarily small `ΔT`: "horizontal convection can be set to motion by any small
temperature gradient, unlike … Rayleigh–Bénard convection" `[snippet-level]`. A spacecraft water line's
thermal environment is set by whatever is adjacent to it — cabin air on one side, structure on the
other, a heater downstream — and the resulting gradient is generically *not* vertical-from-below.

If the gradient has any horizontal component, `u_conv > 0` at every gravity level, there is no switch,
and §3.5's claim — "at lunar gravity a 6.35 mm line with a 1 K gradient has `Ra = 818 < Ra_c`, so
convection is *off* and settling is unopposed … **Lowering gravity can therefore increase net cell
deposition in narrow stagnant lines** … this is the strongest single result in this derivation" —
evaporates. Assumption A18 concedes only an "O(1) factor" from tube-vs-plane geometry; **the gradient-
orientation assumption is not in the assumption table at all.** Upgrade A18 from ⚠️ to ❌ and add a new
assumption row.

**Finding 2.5 — [SERIOUS] Even granting a purely vertical destabilising gradient, the convection switch
is not robust.** In the 6.35 mm line, `Ra > Ra_c` requires `ΔT > 0.345 / 0.912 / 2.088 K` at Earth /
Mars / Moon. The three-way ordering shown in fig4 therefore exists only for **0.345 K < ΔT < 2.088 K** —
less than one decade of a parameter the derivation itself labels ASSUMED and sweeps over 0.01–5 K (2.7
decades). Below 0.345 K no gravity level convects; above 2.09 K all three do. And Mars sits at
`Ra = 1873`, only **10 % above `Ra_c`** — comfortably inside the O(1) uncertainty A18 already concedes.
The figure's clean Earth/Mars-on, Moon-off separation is a knife-edge in an assumed parameter.

**Finding 2.6 — [MINOR] `u_conv` near-onset velocity scale is off by `Pr`.** Eq. (2.6a) uses `ν/H` as
the velocity scale; the conventional weakly-nonlinear Rayleigh–Bénard amplitude uses the thermal scale
`α_th/H`. These differ by `Pr = ν/α_th = 6.1` for water at 25 °C. All near-onset `u_conv` values, all `Ω`
values derived from them, and `D_conv` in the near-onset branch carry that factor. Order-unity, but it
should be stated rather than silently chosen.

**Finding 2.7 — [MINOR] Arithmetic slip in §5.6.** The text states Taylor–Aris requires
`t ≫ D²/D_B = 4.5 × 10⁷ s`. With the document's own `D_B(P1) = 4.51 × 10⁻¹³ m² s⁻¹` and `D = 6.35 mm`,
`D²/D_B = 8.9 × 10⁷ s`. The conclusion (don't use Taylor–Aris) is unaffected — `t_res` = 9.7 s either
way — and `D_ax = 1250 m² s⁻¹` reproduces exactly.

**Finding 2.8 — [MINOR] fig1 contains a non-physical discontinuity.** `run_regime_sweep.py` sets
`delta_rho = 93 if d <= 7e-6 else 50`, a hard step. Both panels of fig1 show a visible jog in the
contours at `d = 7 µm`, and the `Ga_dep = 1` contour has a spurious kink there. The regime map is
therefore not a single physical surface. Either plot the cell family and the floc family as separate
overlaid surfaces, or interpolate `Δρ`, and say which was done.

**Finding 2.9 — [MINOR] `a_c` is a radius but is repeatedly compared against diameters.** Eq. (2.14)
solves for a radius (6.765 µm for R1, so `d_c` = 13.5 µm), yet §3.2 immediately writes "(d ≲ 6–60 µm)"
using the *radii* 3.1 and 32 µm from R2 and R4. The numbers happen to work out because 2×3.1 ≈ 6 and
2×32 ≈ 64, but the sentence as written conflates the two. Tighten the notation; a reviewer who checks
this will not be charitable.

**Finding 2.10 — [MINOR] Monte Carlo branch selection is by sampling mode, not by `a` vs `a_c`.**
`uncertainty.py` lines 93–98 contain a comment correctly stating that the controlling threshold is
`max(g*_dif, g*_int)`, then selects by which lognormal mode the sample came from. I checked 2000
samples: **2 disagree** (0.1 %). Harmless in practice, but the code should do what its own comment says.

---

## 3. Adjudication of the open question in `limitations.md` §2

**The question.** Does eq. (5.7)/(5.8), which in the well-mixed limit gives `k_tot → D_v/H` (deposition
*increasing* with mixing), contradict the §2.2(b)/§3.5 narrative that convection "keeps cells
suspended"?

### 3.1 Verdict

**It is neither a pure algebra error nor merely "two different questions that happen to look
contradictory." It is a boundary-condition inconsistency: the derivation applies a perfect-sink wall to
convective delivery, where the perfect-sink assumption is doing all the work and is not physically
warranted, while implicitly treating gravitational deposition as capture-independent.** The
implementer's mathematics is right; the reduction is the wrong physical model for the stagnant case;
and the §3.5 narrative is not recoverable from it. Classification: **SERIOUS, escalating to BLOCKING
for the specific claim in §3.5 and for fig3.**

### 3.2 Reasoning

**(a) The formula itself is correct.** I re-derived it: for steady 1-D vertical transport
`J = v_s C + D_v ∂C/∂y` with an absorbing bottom (`C(0) = 0`) and `C(H) = C_H`, the solution is
`C(y) = (J/v_s)(1 − e^{−y/h_s})`, `h_s = D_v/v_s`, giving `J = v_s C_H/(1 − e^{−H/h_s})` — exactly eq.
(5.8). Both limits are right: `k_tot → v_s` for `h_s ≪ H`, `k_tot → D_v/H` for `h_s ≫ H`. And in both
limits `C_H ≈ C̄`, so the 0-D closure `k = k_tot/H` is self-consistent. The implementer's diagnosis is
correct as far as it goes.

**(b) But "instantaneous flux vs. long-time fate" is the wrong reconciliation.** Both `Ω = v_s/u_conv`
and eq. (5.8) are answering the *same* question in the dormancy context — how much biomass ends up on
the wall after a year — and they give opposite answers. What actually differs is the wall boundary
condition, and the two mechanisms are not physically entitled to the same one:

- **Gravitational deposition onto a horizontal floor is capture-independent.** A cell that settles onto
  the bottom of a stagnant line is at the bottom of the line whether or not it chemically attaches.
  Absent flow, nothing brings it back up.
- **Convective delivery is capture-*dependent*.** A cell swept to the wall by an eddy and not captured
  is swept away again by the same eddy. The net deposition rate saturates at the attachment-limited
  rate, not the transport-limited rate.

Eq. (5.8) applies `C_wall = 0` (α → 1) to both. That single choice is what converts convection from a
*suspension* mechanism into a *deposition* mechanism 1700× faster than settling. And the derivation's
own nominal attachment efficiency is **α = 0.3, swept over 0.01–1** (§5.3(A), §8.5) — i.e. the program
does not believe the wall is a perfect sink anywhere else in the document.

**(c) The numbers, from controlled ablations I ran.** In the fig3 scenario (6.35 mm line, ΔT = 1 K):

| | `Ra` | `D_v` (m² s⁻¹) | `h_s/H` | `k` (s⁻¹) | deposition timescale |
|---|---|---|---|---|---|
| Earth, P1 cell | 4953 | 1.23 × 10⁻⁷ | 287 (well-mixed) | 3.06 × 10⁻³ | **5.5 min** |
| Mars, P1 cell | 1873 | 2.78 × 10⁻⁸ | 172 (well-mixed) | 6.91 × 10⁻⁴ | 24 min |
| Moon, P1 cell | 818 | 4.51 × 10⁻¹³ | 0.0064 (settling) | 1.75 × 10⁻⁶ | **158 h** |

So **in the code, Earth gravity deposits single cells 1700× faster than lunar gravity** — the exact
opposite of "convection keeps cells suspended." §3.5's prose and §5.3(B)'s equations state contradictory
physics.

**(d) The consequence for the headline is worse than `limitations.md` §2 realises.** I ran the fig3
scenario with the growth and decay terms switched off:

| Configuration | Earth `X_final` | Mars | Moon | Moon/Earth |
|---|---|---|---|---|
| As shipped | 5.48 × 10⁻¹² | 5.60 × 10⁻¹² | 1.22 × 10⁻⁶ kg m⁻² | **2.2 × 10⁵** |
| Growth off (`μ_max = 0`) | 5.44 × 10⁻¹² | 5.44 × 10⁻¹² | 4.77 × 10⁻¹² | **0.88** |
| Growth **and** decay off | 3.493 × 10⁻⁸ | 3.493 × 10⁻⁸ | 3.493 × 10⁻⁸ | **1.000** |

`3.493 × 10⁻⁸ kg m⁻² = C₀·H` exactly. **With growth and decay removed, the transport model deposits
100 % of the initial inventory at every gravity level. The transport physics alone produces exactly
zero gravity dependence in the dormancy scenario** — because a perfect sink plus a year is enough time
at any `g`. With decay on and growth off, lunar deposits *less*, not more.

The entire 2.2 × 10⁵ ratio in fig3 comes from the growth term: at lunar gravity the cell removal
timescale (158 h) is long enough for suspended cells to convert the whole substrate inventory
(`Y·S₀·H = 7.62 × 10⁻³ kg m⁻²` ceiling) into biomass *before* depositing, while at Earth/Mars they are
removed in 5–24 minutes, before any growth. fig3's left panel confirms this: the lunar curve rises to
~4300 mg m⁻² by day 20 (substrate exhaustion) and then decays back to ~1.2 mg m⁻² (the `b_f` term over
a year). **It is a substrate-conversion result, not a transport result.**

**(e) And it is an implementation bug, not just a modelling subtlety.** `dormancy.py` computes
`dX = deposit_flux − b_f·X`. Derivation eq. (5.3) is `∂X/∂t = [μ(S_w) − b_f]·X + Σ_i j_dep,i − j_det` —
**the biofilm growth term `μ(S_w)·X` is omitted**, and eq. (5.2)'s wall-biomass substrate sink
`−(σ/Y)·μ(S_w)·X` is omitted with it. I re-ran the fig3 scenario with both terms restored exactly as
the derivation specifies:

| | Earth | Mars | Moon | Moon/Earth |
|---|---|---|---|---|
| As implemented (no biofilm growth) | 5.48 × 10⁻¹² | 5.60 × 10⁻¹² | 1.22 × 10⁻⁶ | 2.2 × 10⁵ |
| **With eq. (5.3) as written** | **1.388 × 10⁻⁶** | **1.388 × 10⁻⁶** | **1.329 × 10⁻⁶** | **0.958** |

**Restoring the term the derivation itself specifies collapses the headline dormancy result from
2.2 × 10⁵ to 0.96.** Physically obvious in hindsight: with wall growth enabled, the early-deposited
Earth-gravity biofilm consumes the same substrate at the wall and reaches the same `Y·S₀` ceiling. The
gravity dependence was an artifact of denying the deposited biomass the ability to grow.

### 3.3 What must change

1. **`dormancy.py`: add the `μ(S_w)·X` biofilm growth term and its substrate sink** (eqs. 5.3, 5.2).
   Non-optional — the model currently does not implement its own governing equations.
2. **Retract or completely rebuild fig3 and the "~10⁵–10⁶× difference in final deposited mass" claim in
   `limitations.md` §2.** It does not survive either fix.
3. **Replace eq. (5.7)/(5.8) with an explicit branch structure**, not one formula applied uniformly. The
   minimum defensible version:
   - a **capture-independent** gravitational term `f_θ·v_s` that is *not* multiplied by `α`;
   - a **capture-dependent** convective/diffusive term limited by the slower of transport and
     attachment, e.g. `k_conv = [1/(D_v/H) + 1/(α·u_conv)]⁻¹`;
   - and an explicit statement of which branch is being reported.
   With any `α < 1` the convective branch stops dominating and the `Ω`-based narrative is recoverable —
   but the *sign* of the convective term's net effect then depends on `α`, for which the program has no
   ECLSS-specific value.
4. **Demote §3.5's "strongest single result" claim.** Between Finding 2.4 (no `Ra_c` for a non-vertical
   gradient), Finding 2.5 (the switch lives in a sub-decade `ΔT` window with Mars 10 % from the
   threshold), and this section (the wall BC decides the sign, and the demonstration figure is broken),
   the "lowering gravity increases net deposition in narrow stagnant lines" prediction is currently
   unsupported by the program's own model. Either rebuild it properly or present it as a hypothesis with
   its conditions stated, not as a result.
5. Also note: eq. (5.8) is a *steady* flux law with a *maintained* top concentration, applied to a
   closed, depleting inventory. In the well-mixed branch the profile relaxation time and the depletion
   time are the same order, so the quasi-steady closure is marginal exactly where it is being relied on.

---

## 4. Hidden invalidating assumptions and cheaper prior solutions

### 4.1 Prior art the program missed

The Phase 2 adjudication searched the ECLSS/spaceflight/microbiology literature. It did not search the
**colloid-filtration, aerosol-deposition or membrane-fouling** literatures, which is precisely where a
"gravity vs. other particle transport mechanisms" criterion has lived for fifty-five years. This is a
recurrence of the exact methodology failure the adjudicator diagnosed for candidates A/B/C.

**Finding 4.1 — [BLOCKING for the novelty framing, not for the physics] The three-mechanism
decomposition and a gravity number already exist: Yao, Habibian & O'Melia (1971).** Classical colloid
filtration theory decomposes the single-collector efficiency into exactly **diffusion + interception +
gravitational sedimentation**, with `η_G` "described by Yao et al. (1971) as the ratio of settling
velocity (as determined by Stokes' Law) to the hydraulic loading rate" `[snippet-level, corroborated
across several independent secondary sources]` `[verified-existence: Yao, Habibian & O'Melia, "Water and
waste water filtration: concepts and applications," Environ. Sci. Technol. 5:1105–1112, 1971]`. That is
a gravity-relevance number for particle transport in an engineered flow system. The derivation's
`Ga_dep = v_s/max(k_lev, k_int)` is the same three-mechanism competition, restructured as a ratio rather
than a sum, and with `g` promoted from a constant to the swept variable.

**Finding 4.2 — [SERIOUS] `N_G` is a named, regressed dimensionless group in the standard correlation.**
Tufenkji & Elimelech, "Correlation equation for predicting single-collector efficiency in
physicochemical filtration in saturated porous media," *Environ. Sci. Technol.* 38:529–536 (2004)
`[verified-existence]` regresses `η₀` against dimensionless groups including a gravity number `N_G`,
with the total efficiency assembled from Brownian diffusion, interception and gravitational
sedimentation contributions `[snippet-level]`. I could not read the paper (proxy 403 on the McGill
PDF), so the exact `N_G` definition is unverified — **but the manuscript must cite this and state
explicitly how `Ga_dep` differs from `N_G`.** A referee from the water-treatment side will know this
correlation by heart.

**Finding 4.3 — [SERIOUS] There is a cheaper and *stronger* prior solution for Criterion 2.**
Pich, "Theory of gravitational deposition of particles from laminar flows in channels," *J. Aerosol
Sci.* 3:351–361 (1972) `[verified-existence]` gives a **closed-form deposition efficiency** for a
horizontal cylindrical tube in laminar flow, parameterised by a settling parameter proportional to
`v_s L/(U D)` — i.e. `Λ_g` up to a constant `[snippet-level]`. Pich returns *the fraction of entering
particles deposited*; `Λ_g` returns only a ≷ 1 threshold. **A referee can reasonably ask why the paper
proposes a threshold criterion when an exact efficiency for the same geometry has existed since 1972.**
Using Pich's `η(κ)` directly would also resolve Finding 2.1's factor-2 convention problem, since the
constant is then fixed by the exact solution rather than chosen. Related, and relevant to A16:
"Aerosol deposition in circular tubes with simultaneous consideration of diffusion and sedimentation,"
*J. Aerosol Sci.* (2021), and "Analytical solutions for particle transport through an inclined channel
with gravitational effect," *J. Aerosol Sci.* (2018) `[verified-existence; content snippet-level]` —
**the coupled diffusion + sedimentation channel problem has published analytical solutions.** A16's
linear superposition of `v_s cos θ` and `k_lev` is therefore a *choice*, not a necessity, and grading it
"genuinely approximate" understates the position.

**Finding 4.4 — [SERIOUS] The contribution *form* — a transport-mechanism-vs-particle-size regime map —
is standard in membrane engineering.** Belfort, Davis & Zydney, "The behavior of suspensions and
macromolecular solutions in crossflow microfiltration," *J. Membrane Sci.* 96:1–58 (1994)
`[verified-existence]` is the canonical treatment of competing back-transport mechanisms (Brownian
diffusion, shear-induced diffusion, inertial lift, gravitational sedimentation) selected by particle
size, including the well-known back-transport minimum for particles in the **0.1–1 µm** range
`[snippet-level]`. The program's fig1 is structurally the same object with `g` added as the second axis.
This does *not* kill the contribution — adding the `g` axis is genuinely new — but the paper must
present itself as "we add the gravity axis to a known regime decomposition," not as "we derive a new
criterion." The Konishi/Mudawar/Hasan analogy in §3.6 is a good rhetorical anchor but it is the *wrong
field's* anchor; the correct one is colloid filtration / membrane back-transport.

**Finding 4.5 — [SERIOUS] Prior partial-gravity particle-transport work exists in the target venue and
was missed.** SAE 2009-01-2359, "A Novel Testing Protocol for Evaluating Particle Behavior in Fluid Flow
Under Simulated Reduced Gravity Conditions," 39th ICES, Savannah, July 2009 `[verified-existence]`:
tracer-particle flow behaviour through a glass-bead media filter for a proposed lunar regolith-based
water filtration design, flown on NASA's reduced-gravity aircraft at microgravity **and lunar gravity**,
with an inclined-clinostat (≈10° tilt) ground analogue calibrated to the 1/6 `g` axial vector; Phase I
covered large-particle fluidization and sedimentation, Phase II tracer settling `[snippet-level]`. This
is partial-gravity particle sedimentation in water-recovery hardware, at ICES, seventeen years ago, and
neither the Phase 1 surveys nor the Phase 2 adjudication found it. It does **not** pre-empt the
criterion — it is a test protocol, not a dimensionless analysis — but omitting it from an ICES
submission on partial-gravity particle transport in water systems would be a visible gap. **It also
supplies exactly the cheap validation route the program's spare-money constraint needs:** an inclined
clinostat as a fractional-gravity analogue, buildable for tens of dollars, rather than a centrifuge.

**Finding 4.6 — [MINOR, favourable] The one load-bearing citation in §10 corroborates independently.**
An independent search reproduced the Groningen result: for *S. aureus* ATCC 12600 in a parallel-plate
flow chamber, "sedimentation appeared as the predominant contribution to mass transport"; deposition
efficiencies were 4–5× above unity relative to the Smoluchowski–Levich convective-diffusion solution
but **below** unity relative to sedimentation `[snippet-level, two independent result sets]`. This
strengthens §10's defence of the `Ga_dep ≫ 1` results. It also means "sedimentation beats convective
diffusion for bacteria in a laminar flow chamber" is an already-published 1-`g` result, and the paper's
novel content is strictly the `g`-parameterisation, not the finding.

**Finding 4.7 — [MINOR, favourable] A partial-gravity settling dataset exists and is uncited.**
"Computational sedimentation modelling calibration: a tool to measure the settling velocity under
different gravity conditions," *Earth Surface Dynamics* 13:549 (2025) `[verified-existence]`: particle
settling trajectories in water recorded under **reduced Martian and lunar gravity in parabolic flight**
`[snippet-level]`. That is direct empirical validation for eq. (2.1)'s `v_s ∝ g` scaling — the single
most load-bearing physical assumption in the whole criterion — and it is free. Add it to §9.10.

### 4.2 Robustness of `g* ≈ 0.24 g_E`

**Finding 4.8 — [BLOCKING as currently reported] The headline number is over-precise by roughly a
factor of 50, and the derivation's own §7.3(b) already says so.**

Sweeping only the parameters the derivation itself flags as ASSUMED or ranged — `D` ∈ {3.18, 12.7} mm,
`x` ∈ {0.1, 2} m, `T` ∈ {288, 318} K, `Δρ_cell` ∈ {83, 103}, `f_θ` ∈ {1, 1/π} — I get

```
    g*/g_E  ranges from 0.062 to 3.04       (baseline 0.238)
```

a factor of **49**, with the upper end above Earth gravity. The program's own Monte Carlo agrees once
you separate the two size modes (the mixture statistics in fig5 are not meaningful — see below): for
the single-cell mode alone,

```
    g*  5th/50th/95th percentile  =  0.029 / 0.224 / 1.65  g_E
    P(Ga_dep > 1 | Earth) = 0.89 ,  | Mars = 0.67 ,  | Moon = 0.40
```

So the defensible statement is: *for single planktonic cells in a nominal WPA line, gravitational and
diffusive wall-delivery fluxes are within an order of magnitude of each other across the entire
Earth-to-Moon range; the crossover cannot be located more precisely than "between ~0.03 and ~1.6 `g_E`",
and gravity dominates with probability 0.40 at lunar gravity and 0.67 at Mars gravity.* That is still a
publishable, useful, non-trivial result — arguably a **better** one, because it is honest. What is not
defensible is "`g*` = 0.238 `g_E`, between lunar and Mars gravity", which is currently the headline in
§3.2, §8.6, §10, `run.md`, `fig2`, and a test function name
(`test_g_star_headline_single_cell_wpa_between_mars_and_moon`, which asserts
`G_MOON < gstar < G_MARS` at `rel=0.05` — a test that pins an over-claim).

§7.3(b) says this in as many words: "A criterion reported as `g* = 0.24 g_E` is indefensible given §6."
**The document does not follow its own instruction.** Fix the headline, not the advice.

**Finding 4.9 — [SERIOUS] fig5's summary statistics mix two physically distinct branches.** The reported
"median 0.154 `g_E`, 90 % interval [1.19 × 10⁻⁴, 1.44] `g_E`" is the median and interval of a bimodal
mixture: 80 % single-cell samples on the diffusion branch (median 0.224 `g_E`) and 20 % floc samples on
the interception branch (median 4.6 × 10⁻⁴ `g_E`). The mixture median lands in the empty valley between
the two modes, where no sample actually sits — visible as a dip in the left panel of fig5 at
log₁₀ ≈ −2. Similarly, `P(Ga_dep > 1 | Moon) = 0.52` is `0.2 × 1.00 + 0.8 × 0.40`: the 0.52 is an
artifact of the assumed 80/20 mode weighting, which §7.3(b) itself derives from a by-number/by-volume
mix-up in two different sources. **Report per-branch.**

### 4.3 Assumption table (§6, A1–A27) — items worse than graded

| Item | Current grade | Red-team grade | Why |
|---|---|---|---|
| **A18** `Ra_c = 1708` | ⚠️ "O(1) geometry factor" | **❌ BLOCKING for §3.5** | Threshold exists only for a vertical destabilising gradient; any horizontal component removes it entirely (Finding 2.4). The orientation assumption is not stated anywhere. |
| **A16** linear superposition | ⚠️ "genuinely approximate" | **SERIOUS** | Published analytical coupled diffusion+sedimentation channel solutions exist (Finding 4.3). It is an avoidable choice, not a necessary approximation. |
| **A14** perfect-sink wall | ⚠️ "conservative" | **Correct for §3, wrong for §5** | The grading reasoning ("makes `Ga_dep` underestimated → conservative") applies only to the criterion. The same assumption in eq. (5.8) is what produces the wrong-signed convection behaviour (§3 of this report). |
| **A6** Stokes drag | ✅ P1–P4 / ❌ P5 | **SERIOUS — unenforced** | Correct as written but not implemented in the criteria path, and eq. (3.3)'s size-independence silently inherits the same bound (Finding 2.2). |
| **A12** non-motile cells | ❌, §7 rank 2 | **SERIOUS — under-drawn** | The ISS isolates the paper cites as its motivation (*P. aeruginosa*, *Burkholderia*, *Stenotrophomonas*) are flagellated. The headline single-cell case is therefore the *least* representative case for the very organisms motivating the work. This belongs in the abstract, not §6. |
| **A11** `Δρ > 0` | ⚠️ | **SERIOUS** | The sourced 898 kg m⁻³ biofilm density gives `Δρ ≈ −99` — larger in magnitude than the cell's `+93`. Rising aggregates deposit on the *top* wall: every deposition-*location* conclusion inverts. Neither the Monte Carlo nor any figure ever samples `Δρ < 0`. |
| **A3** steady flow | ⚠️ | **SERIOUS** | The WPA duty-cycles. A cycling line is a time-alternating R1/R4 hybrid, and the whole thesis is about the pumped/stagnant contrast — yet every criterion is evaluated at a fixed `U`. The most operationally realistic case is the one not analysed. |
| **A8** dilute / no hindered settling | ✅ | **MINOR caveat** | Correct in the bulk, but the *deposit* is a bed, and the deposit is the model's output quantity. Bed compaction and re-entrainment are outside scope; say so. |
| A2 entrance length | ⚠️ 23 % not developed | **MINOR — unenforced** | `entrance_length()` exists and is never called (Finding 1.4). |

---

## 5. Independent figure reproduction

**Chosen: fig2 (`g*` vs. assumed tube diameter)** — produced by `scripts/run_regime_sweep.py ::
fig2_g_star_vs_diameter()`, backed by `results/data/g_star_vs_diameter.csv`.

I rebuilt it from raw physics in a standalone script: `Q` from the sourced 13 lb/hr, `U = Q/(πD²/4)`,
`γ_w = 8U/D`, `D_B = k_BT/(6πμa)`, `k_lev = [1/(9^{1/3}Γ(4/3))]·D_B^{2/3}(γ_w/L)^{1/3}`,
`v_s = 2Δρ g a²/(9μ)`, `g* = g_E/(v_s/k_lev)` — i.e. via the *velocity ratio*, never touching the
`2.925` closed form the code uses.

| `D` (mm) | `U` (m s⁻¹) | `γ_w` (s⁻¹) | `k_lev` (m s⁻¹) | `Ga_dif` | `g*/g_E` **independent** | `g*/g_E` **repo CSV** | Δ |
|---|---|---|---|---|---|---|---|
| 3.18 | 0.20697 | 520.7 | 3.210 × 10⁻⁸ | 2.1005 | **0.47608** | 0.47585 | 0.05 % |
| 4.57 | 0.10021 | 175.4 | 2.233 × 10⁻⁸ | 3.0186 | **0.33128** | 0.33112 | 0.05 % |
| 6.35 | 0.05191 | 65.39 | 1.607 × 10⁻⁸ | 4.1943 | **0.23842** | 0.23830 | 0.05 % |
| 9.53 | 0.02305 | 19.35 | 1.071 × 10⁻⁸ | 6.2948 | **0.15886** | 0.15878 | 0.05 % |
| 12.7 | 0.01298 | 8.17 | 8.036 × 10⁻⁹ | 8.3887 | **0.11921** | 0.11915 | 0.05 % |

**fig2 reproduces from scratch to 0.05 %.** The residual is the closed form's rounded `2.925` vs. the
exact `2.9236`. `derivation.md` §3.2's table (0.475 / 0.331 / 0.238 / 0.159 / 0.119) matches.

I also independently confirmed fig1's `Ga_dep = 1` contour anchors (0.238 `g_E` at `d` ≈ 1 µm; the kink
at `d = 2a_c` = 13.5 µm; the flat 5.3 × 10⁻⁴ `g_E` interception plateau above it) and every `Ra` bar in
fig4 (4953 / 1873 / 818; 3.2 × 10⁵ / 1.2 × 10⁵ / 5.3 × 10⁴; 5.2 × 10⁸ / 2.0 × 10⁸ / 8.6 × 10⁷). fig3 is
diagnosed in §3 above and does not survive.

**Finding 5.1 — [MINOR] fig3 is mislabelled.** Its left panel is titled "Accumulated deposit on tank
floor" and its summary CSV column is `Ra_tank`, but the geometry simulated is the 6.35 mm *line*
(`H_LINE = 6.35e-3`). The `run_dormancy_sim.py` docstring explains the switch correctly; the figure and
CSV were not updated.

---

## 6. Overall verdict

**Is this derivation and its code sound enough to write a paper around? — Yes, with substantial
rework of the framing and the retraction of one headline result.**

What is genuinely solid, and I tried hard to break it:

- The algebra of §§2–3 is **correct**. I re-derived the Lévêque prefactor, the `2.925` group, the `a_c`
  exponents (against a numerical root-find) and the `2/15.31` O'Neill constant independently; all check.
- Fourteen headline numbers reproduce from scratch to ≤ 0.3 %, and fig2 reproduces to 0.05 %.
- The three-criterion structure is well-motivated. §3.1's insistence that `v_s/U` is the *wrong*
  comparison, and the orthogonality argument behind it, is correct and is a real contribution to how
  this question gets framed in the ECLSS community.
- §4's decoupling of the transport question from the growth question — and its use of the BioRock null
  as *support* rather than refutation — is logically sound and is the strongest defensive argument in
  the program.
- The document's own honesty is above average: §7.3(b) correctly forbids the headline that §8.6 then
  publishes, and §10 correctly names the load-bearing weak joint. The problem is that these warnings
  were written and then not obeyed.

**Three BLOCKING items must be cleared before the manuscript:**

1. **The dormancy result (§3.5, fig3, `limitations.md` §2).** `dormancy.py` omits the `μ(S_w)·X` biofilm
   growth term that eq. (5.3) specifies; restoring it collapses the claimed 2.2 × 10⁵ lunar/Earth ratio
   to 0.96. With growth and decay both off, the transport model gives *exactly zero* gravity dependence
   in the dormancy scenario. Separately, `Ra_c = 1708` requires a vertical destabilising gradient that a
   real spacecraft line will not generically have. The "strongest single result in this derivation" is
   currently the weakest thing in it and must be rebuilt or retracted.
2. **The headline `g*`.** "0.238 `g_E`, between lunar and Mars gravity" is over-precise by ~50× across
   the program's own assumed-parameter box (0.062–3.04 `g_E`) and is convention-dependent (0.749 `g_E`
   under the perimeter-averaged `f_θ = 1/π` that §5.3 itself derives). Replace with the interval and the
   per-branch probabilities.
3. **Novelty framing vs. colloid-filtration prior art.** The diffusion/interception/sedimentation
   decomposition and a gravity number date to Yao, Habibian & O'Melia (1971); `N_G` is a named group in
   the standard Tufenkji–Elimelech (2004) correlation; Pich (1972) already gives a *closed-form*
   deposition efficiency for the exact geometry Criterion 2 addresses; and Belfort/Davis/Zydney (1994)
   established the mechanism-vs-size regime-map form. None of these appear anywhere in the program. The
   contribution is real but must be restated as **"we parameterise an established transport-regime
   decomposition in `g` and apply it to ECLSS water hardware"** — not as deriving a new criterion. This
   is the same searched-the-wrong-literature failure the Phase 2 adjudication identified for candidates
   A, B and C, recurring one phase later.

**Recommended reframe.** The defensible paper is narrower and, I think, better than the one currently
scoped:

> For non-motile cells and aggregates in ECLSS water loops, gravitational wall delivery exceeds
> Brownian/interceptive delivery by 2–3 orders of magnitude for every aggregate above ~7 µm at every
> gravity level down to milli-`g`; for single planktonic cells the two are comparable to within an order
> of magnitude across the entire Earth-to-Moon range, so a 1-`g` qualification test is not a valid
> surrogate and the gravity term must be retained. The size-selective floc carry-through transition
> (`Λ_g`) falls in the 100–200 µm band across the lunar-to-Mars window and is the sharpest testable
> prediction. Retention (`Σ_g`) is shear-controlled and `g`-independent in every pumped regime.

That claim survives every attack in this report. Everything about the stagnant/convection branch does
not, yet.

**Confidence in the criterion framework (§§2–3): HIGH.** **Confidence in the stagnant/dormancy branch
(§§3.5, 5.3(B), fig3): LOW — do not publish as-is.** **Confidence that the novelty claim survives
contact with a water-treatment or aerosol-science referee, as currently framed: LOW; as reframed above:
MEDIUM.**

---

## Appendix — findings index

| # | Finding | Class |
|---|---|---|
| 1.1 | 14 headline numbers reproduce independently to ≤ 0.3 %; 28/28 tests pass | PASS |
| 1.2 | 0.3 % offset from a ρ = 1000 vs. 997 units slip in §1.2 | MINOR |
| 1.3 | Regression tests are transcription checks; §9.6's closed-form-vs-direct check absent | SERIOUS |
| 1.4 | §5 PDE (all of §9.7) unimplemented; 8 §9 deliverables are dead code; §7.3(c) checks absent | SERIOUS |
| 2.1 | `Λ_g` factor-2 convention (`R = D/2` vs. Hazen full depth) flips the 100 µm claim | SERIOUS |
| 2.2 | Stokes `Re_p < 0.34` bound unenforced in closed forms; eq. (3.3) size-independence has an unstated `d < 184 µm` ceiling | SERIOUS |
| 2.3 | `cos θ = 1` vs. `f_θ = 1/π`: `g*` = 0.238 vs. 0.749 `g_E`; criteria and PDE disagree | SERIOUS |
| 2.4 | `Ra_c = 1708` requires a vertical destabilising gradient; otherwise no threshold exists | BLOCKING (§3.5) |
| 2.5 | Convection switch lives in a sub-decade `ΔT` window; Mars is 10 % from `Ra_c` | SERIOUS |
| 2.6 | Near-onset `u_conv` velocity scale off by `Pr` = 6.1 | MINOR |
| 2.7 | §5.6 states `D²/D_B` = 4.5 × 10⁷ s; should be 8.9 × 10⁷ s | MINOR |
| 2.8 | fig1 discontinuity at `d` = 7 µm from a hard `Δρ` step | MINOR |
| 2.9 | `a_c` (a radius) compared against diameters in §3.2 prose | MINOR |
| 2.10 | MC branch selection by sampling mode, not `a` vs `a_c` (2/2000 disagree) | MINOR |
| 3 | eq. (5.7)/(5.8): boundary-condition inconsistency, not a scope confusion; `μ(S_w)X` omitted from `dormancy.py`; fig3 result is a substrate-conversion artifact | BLOCKING |
| 4.1 | Yao/Habibian/O'Melia (1971) already decompose diffusion+interception+sedimentation with a gravity number | BLOCKING (framing) |
| 4.2 | `N_G` is a named group in Tufenkji–Elimelech (2004) | SERIOUS |
| 4.3 | Pich (1972) gives a closed-form efficiency for Criterion 2's exact problem; coupled analytic solutions exist (A16 avoidable) | SERIOUS |
| 4.4 | Belfort/Davis/Zydney (1994) established the mechanism-vs-size regime-map form | SERIOUS |
| 4.5 | SAE/ICES 2009-01-2359: lunar-gravity particle transport in water filtration, at ICES, missed | SERIOUS |
| 4.6 | Groningen sedimentation-dominance result corroborates independently | MINOR (favourable) |
| 4.7 | ESurf 13:549 (2025) parabolic-flight settling at Mars/lunar `g` — free validation data, uncited | MINOR (favourable) |
| 4.8 | `g*` = 0.238 `g_E` over-precise by ~50×; contradicts the derivation's own §7.3(b) | BLOCKING |
| 4.9 | fig5 median/interval are bimodal-mixture artifacts | SERIOUS |
| 4.10 | A18 → ❌; A16, A14, A6, A12, A11, A3 all under-graded | SERIOUS |
| 5.1 | fig3 mislabelled "tank floor"; simulates the 6.35 mm line | MINOR |
