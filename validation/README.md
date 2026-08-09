# Validation Handoff

**Read this first: the core contribution does not require physical validation to stand as an ICES modeling paper.** Every headline number in `paper/manuscript.md` is validated computationally — independently re-derived by an adversarial reviewer to ≤0.3% (`docs/redteam_report.md`), cross-checked against published secondary data (Groningen sedimentation-dominance result, `docs/derivation.md` §10), and reproducible from a documented single command (`run.md`). That is sufficient grounding for the paper's claims as scoped (Discussion §4, `paper/manuscript.md`).

What follows is an **optional** validation plan for someone who wants to go further and generate primary experimental data, split into two parts by cost and by what physics each part actually tests. Neither part requires an institutional budget, a centrifuge, or parabolic-flight access — consistent with this program's individual-spare-money-fundability constraint (`docs/decision_log.md`, 2026-07-31 entry).

---

## Part A: Rayleigh–Bénard convection-onset test (recommended first step)

### A.1 What this test proves

`docs/derivation.md` §2.2(b) predicts a sharp onset of buoyant convection in stagnant water once the Rayleigh number `Ra = gβΔT H³/(να)` exceeds a critical value taken as `Ra_c = 1708`. This threshold is the mechanism behind Figure 4 and the dormancy deposition-rate result in Figure 3.

**The specific open question this test answers.** `Ra_c = 1708` is the classical value for a *rigid–rigid infinite plane layer*. An ECLSS water line is a **tube**, which is not an infinite plane layer. `derivation.md` assumption A18 concedes an unquantified "O(1) geometric factor" for this mismatch, and `docs/limitations.md` §4 shows that a factor of **2** in `Ra_c` is enough to collapse Figure 4's three-way Earth/Mars/Moon gravity separation into a two-way split — because Mars sits only 10% above the nominal threshold. **Measuring the real `Ra_c` for tube geometry is therefore the single highest-value contribution a cheap bench test can make to this model**, and it needs no reduced gravity to do it.

**Why this works at Earth gravity.** `Ra_c` is a dimensionless threshold; it does not depend on `g`. Since `Ra ∝ g·β·ΔT·H³`, the same Rayleigh number reached by a lunar-gravity line can be reached at Earth gravity by adjusting `ΔT` and `H`. The test measures the *threshold*, which then applies at every gravity level.

**Critical design constraint (get this right or the experiment is impossible).** Because `Ra ∝ H³`, the controllable quantity `ΔT_c` is violently sensitive to depth:

| layer depth / tube bore | predicted `ΔT_c` at Earth `g` | measurable? |
|---|---|---|
| 250 mm (a tall cylinder) | ~0.00001 K | **no — hopeless** |
| 25 mm | 0.006 K | no |
| 6.35 mm (the actual WPA line bore) | 0.34 K | marginal; needs differential thermometry |
| **3.0 mm** | **3.3 K** | **yes — easy** |
| **2.5 mm** | **5.7 K** | **yes — easy** |
| 2.0 mm | 11.0 K | yes |

Use `python3 -c "import sys; sys.path.insert(0,'src'); from eclss_gravity.validation_compare import plan_geometry; print(plan_geometry(TARGET_DELTA_T_K))"` to pick your geometry. **A 2–3 mm layer/bore is the sweet spot**: it puts the threshold at 3–11 K, which a $25 thermocouple pair resolves trivially.

### A.2 Design: a control and a measurement

Run **both**, in this order. This is what makes the result trustworthy rather than a single ambiguous number:

- **A-control — shallow plane layer.** A 2–3 mm deep horizontal layer of water in a flat dish, heated uniformly from below. This is *exactly* the geometry `Ra_c = 1708` is derived for, so the classical value should hold. **Purpose: validate your apparatus and technique against textbook physics before trusting it on the open question.** If your control does not reproduce `Ra_c ≈ 1708`, your thermometry or heating uniformity is wrong, and the tube result would be meaningless.
- **A-measurement — horizontal tube.** A 2–3 mm bore clear tube, water-filled, sealed, horizontal, heated uniformly from below along its length. Same `ΔT` sweep. **Purpose: measure the tube-geometry correction factor** — the ratio of the observed onset `Ra` to 1708. This number is the actual deliverable.

**Pass/fail criterion, stated as a number before testing:** the control must bracket `Ra_c = 1708` (i.e. the highest no-convection trial and the lowest convection trial must straddle 1708) — if it does not, stop and fix the apparatus. For the tube, report the bracket and the correction ratio. A ratio within `[0.7, 1.4]` means the classical value transfers adequately and the model's Figure 4 conclusion stands as published; a ratio outside `[0.5, 2.0]` means Figure 4's gravity separation must be re-derived with the measured value, per `limitations.md` §4.

### A.3 Bill of materials

See `validation/bom.csv`. Total for Part A: **approximately $150** (must-buy items only), entirely consumer/hobbyist-grade, no vendor account or long lead time required.

### A.4 Assembly

1. **Heat source.** Any flat, uniformly-heated surface: a cheap electric hot plate, or (better for low `ΔT` control) a metal plate on top of a water bath fed by an aquarium heater or sous-vide circulator. Uniformity matters more than precision — a hot spot creates a *horizontal* gradient, which convects at any `ΔT` and destroys the measurement (see §A.6).
2. **A-control cell.** A flat-bottomed dish (a glass petri dish or a small baking dish) on the heated plate. Fill to a measured 2–3 mm depth — measure with calipers or a depth gauge against the dry dish, and record it precisely; it enters as `H³`.
3. **A-measurement cell.** A 2–3 mm bore clear tube (rigid acrylic/glass preferred over soft silicone, which sags), 100–200 mm long, filled with water, sealed at both ends with no air bubble, laid horizontally in direct contact with the heated plate along its full length.
4. **Thermometry.** One thermocouple in contact with the heated surface, one in the water near the free/top surface. For the control, a thin thermocouple laid just under the water's top surface works; for the tube, tape one to the top outer wall. You are measuring the *difference*, so identical probes on the same meter cancel most absolute error.
5. **Tracer.** Fine mica powder, aluminum "glitter" flake, or thymol-blue/food dye. Mica or aluminum flake is strongly preferred: suspended flakes align with shear and make Rayleigh–Bénard convection cells **directly visible** as a characteristic polygonal/roll pattern — an unambiguous, photographable onset signal, far better than watching dye diffuse.

### A.5 Procedure

1. Compute your predicted `ΔT_c` for your measured `H` (see §A.1's helper command).
2. Equilibrate: heater off, both thermocouples within 0.1 K, tracer evenly dispersed by gentle stirring, then left to still.
3. Set the heater to a target `ΔT`, wait for both thermocouples to be steady for 2 minutes.
4. Observe and record (phone video or timestamped photos) for 30 minutes. Score each trial as **convecting** (visible cell/roll pattern or systematic tracer circulation) or **not convecting** (tracer stays put, only slow diffusive blur).
5. Sweep `ΔT` at 0.3×, 0.6×, 1×, 1.5×, 2.5×, and 4× your predicted `ΔT_c`. **Minimum 3 repetitions per level** — onset near threshold is genuinely stochastic.
6. Re-stir and re-equilibrate fully between every trial; residual motion from a previous run is the most common way to get a false positive.
7. Run the full sweep for the control cell first, confirm it brackets 1708, then repeat for the tube.

### A.6 Safety

- Keep water below ~45 °C: well under any scald risk, and it keeps `β`/`ν`/`α` within ~10% of the 25 °C values the model uses (`docs/derivation.md` §6.6). Low `ΔT` is the regime of interest anyway — you do not need hot water for this.
- GFCI-protected outlet for any mains heater near water; no energized heater left unattended; keep connections out of splash range.
- Mica/aluminum flake and food dye are non-toxic in these quantities; avoid inhaling dry powder — wear a dust mask when dispensing, and dispose of rinse water down a normal drain.
- Glass dishes/tubes: handle cold, inspect for cracks before heating, do not thermally shock (no cold water into a hot dish).

### A.7 Data handling

Record one row per trial: `trial, delta_T_K, H_m, mixing_onset_s, notes`, where `mixing_onset_s` is the time to visible convection or **left empty if no convection was observed**. Keep the control and tube datasets in separate CSVs.

Then run the analysis script (written, tested, and ready — no code needed from you):

```bash
python3 -m eclss_gravity.validation_compare your_control_data.csv
python3 -m eclss_gravity.validation_compare your_tube_data.csv
python3 -m eclss_gravity.validation_compare --self-test   # verifies the script itself on synthetic data
```

It computes `Ra` for every trial, brackets the empirical threshold between the highest non-convecting and lowest convecting trial, and returns a verdict (`CONSISTENT` / `INCONSISTENT` / `SCATTERED` / `INCONCLUSIVE`) against `Ra_c = 1708`, with guidance for each. `eclss_gravity.validation_compare.tube_geometry_correction(observed_delta_T_c, H)` returns the correction ratio directly.

### A.8 Expected result and interpretation

**Control:** should bracket 1708. If it does not, the apparatus is at fault (most likely a horizontal temperature gradient from non-uniform heating, or residual motion between trials) — fix it before proceeding, because the same fault would silently corrupt the tube measurement.

**Tube:** the honest expected outcome is a correction factor somewhat *above* 1.0 — confinement by the tube walls generally stabilizes against convection, raising the effective `Ra_c` — but the derivation does not predict a specific value, which is exactly why it is worth measuring. Any of these is a real, reportable result:

- **Ratio ≈ 1:** the classical value transfers; `derivation.md` A18's O(1) concern is resolved benignly and Figure 4 stands as published.
- **Ratio ≳ 2:** Figure 4's three-way gravity separation is not supported; per `limitations.md` §4 the Mars case falls below onset and the result becomes a two-way Earth-vs-rest split. **This would be a genuine correction to a published figure and the most valuable possible outcome of the test.**
- **`SCATTERED` verdict:** onset is not cleanly threshold-like in a tube, which would itself be worth reporting — it would mean the sharp-switch framing in `derivation.md` §3.5 is the wrong model for tube geometry regardless of where the threshold sits.

A null or inconvenient result here should be reported, not adjusted away; the model's own limitations file already stakes out that a factor-2 discrepancy overturns a figure, so there is no face to lose in finding one.

## Part B (optional, higher cost/complexity): inclined-clinostat fractional-gravity analog

### B.1 What this adds

Part A validates the convection mechanism but not the gravity-scaling itself. `docs/redteam_report.md` Finding 4.5 identifies the precedent for this: SAE 2009-01-2359 (39th ICES, 2009) used an inclined clinostat (~10° tilt from horizontal, slowly rotating) as a ground-based fractional-gravity analog for particle-transport testing in a lunar water-filtration concept. The same approach could test this program's `Λ_g` size-selective floc carry-through prediction (the "sharpest, most design-relevant prediction" per `paper/manuscript.md` §4): does a ~100–183 µm bead/floc surrogate settle out of a flow tube at simulated Earth-equivalent conditions but carry through at a clinostat-simulated lower effective gravity?

### B.2 Bill of materials (additional, beyond Part A)

See `validation/bom.csv`, Part B rows. Total additional cost: **approximately $128** (must-buy items; see `bom.csv`) for a basic DIY clinostat (small geared motor, mounting hardware, tilt fixture) — well documented in the amateur/citizen-science plant-biology clinostat literature, which this design borrows from directly.

### B.3 Why this is Part B, not Part A

A clinostat is a genuine fractional-gravity *analog*, not a source of real reduced gravity (it averages the gravity vector's effect over a rotation, which is a different physical situation from a sustained lower-magnitude gravity field). It is the right tool for a qualitative, order-of-magnitude check of the size-selective transition, not a precise quantitative test of the specific `g*` thresholds this work reports (which, per `docs/limitations.md`, are themselves reported as ranges/probabilities rather than precise points, for exactly this kind of reason). Treat Part B results as directional corroboration, not a precision check.

### B.4 Fallback

If Part B's cost or complexity is not justified, Part A alone is a legitimate, complete, cheap validation of the model's most important disclosed-as-uncertain mechanism (the convection onset), and the size-selective floc prediction can be left as a stated, falsifiable hypothesis for future work rather than tested in this cycle. This costs nothing beyond Part A and loses only the (already explicitly caveated as analog-only) Part B corroboration.

---

## Summary

| | Tests | Cost | Confidence gained |
|---|---|---|---|
| **Computational (already done)** | Internal consistency, independent re-derivation, secondary-data comparison | $0 | High confidence in the algebra and closed-form results |
| **Part A** | The `Ra_c` convection-onset mechanism (Figures 3–4's basis) | ~$85–140 | Direct, quantitative, real (not analog) physical test |
| **Part B (optional)** | Size-selective floc carry-through, qualitatively, via gravity analog | +~$120–220 | Directional corroboration only |

No part of this plan requires institutional funding, a centrifuge, parabolic flight, or a vendor account beyond an ordinary consumer purchase.
