# Validation Handoff

**Read this first: the core contribution does not require physical validation to stand as an ICES modeling paper.** Every headline number in `paper/manuscript.md` is validated computationally — independently re-derived by an adversarial reviewer to ≤0.3% (`docs/redteam_report.md`), cross-checked against published secondary data (Groningen sedimentation-dominance result, `docs/derivation.md` §10), and reproducible from a documented single command (`run.md`). That is sufficient grounding for the paper's claims as scoped (Discussion §4, `paper/manuscript.md`).

What follows is an **optional** validation plan for someone who wants to go further and generate primary experimental data, split into two parts by cost and by what physics each part actually tests. Neither part requires an institutional budget, a centrifuge, or parabolic-flight access — consistent with this program's individual-spare-money-fundability constraint (`docs/decision_log.md`, 2026-07-31 entry).

---

## Part A: Rayleigh–Bénard convection-onset test (recommended first step)

### A.1 What this test proves

`docs/derivation.md` §2.2(b) predicts a sharp onset of buoyant convection in a stagnant, vertically-heated water-filled tube once the Rayleigh number `Ra = gβΔT H³/(να)` exceeds the critical value `Ra_c = 1708`. This is the mechanism behind Figure 4 and the dormancy-rate result in Figure 3.

**The key insight that makes this testable on Earth without a centrifuge:** `Ra_c = 1708` is a universal, gravity-independent threshold. Since `Ra ∝ g·ΔT`, an equivalent Rayleigh number to what a 6.35 mm line would reach at *lunar* gravity with a 2 K gradient can be reached at *Earth* gravity with a proportionally smaller `ΔT` (specifically, `ΔT_Earth = ΔT_target × (g_Moon/g_Earth) = ΔT_target × 0.165`). **This test validates the fluid-mechanics model itself — the existence and location of the `Ra_c` threshold — using only Earth gravity and a controlled temperature difference.** It does not directly validate the gravity-scaling itself (that would need reduced gravity — see Part B) but it validates the single most consequential, and currently least-verified, mechanism in the derivation: whether convection really turns on/off where the model says it does, and whether it really suppresses/enables net particle deposition the way `derivation.md` §3.5 and this program's corrected Figure 3 claim.

**Pass/fail criterion, stated before testing:** below the predicted `ΔT_c` (computed from your actual tube geometry — see §A.4), dye or tracer particles introduced at the top of a vertical tube should remain visibly stratified (minimal lateral/vertical mixing) for at least 30 minutes. Above `1.5×ΔT_c`, visible convective mixing (dye spreading, tracer redistribution) should occur within 5 minutes. A null result — no qualitative difference in mixing behavior across this `ΔT` range — falsifies the convection-onset mechanism as modeled and should be reported as such, not adjusted away.

### A.2 Bill of materials

See `validation/bom.csv`. Total for Part A: **approximately $140** (must-buy items only; a lab stand/clamp is often already on hand and is excluded from that figure — see `bom.csv`), entirely consumer/hobbyist-grade, no vendor account or long lead time required. Everything is either already in a typical home/garage or available same-week from a hardware store or Amazon.

### A.3 Assembly

1. Mount the clear acrylic/glass tube vertically in a stand or clamp, sealed at the bottom, open (or loosely capped) at the top.
2. Wrap the lower third of the tube with the resistive heating tape (or submerge the bottom in a small heated water bath — a sous-vide immersion circulator works well and gives precise, stable `ΔT` control if you have one; if not, the heating tape + a simple PID temperature controller is the budget option in the BOM).
3. Insert one thermocouple near the top of the water column and one near the bottom, both away from the tube wall (mid-radius), connected to a dual-channel or two single-channel digital thermometers.
4. Fill the tube with room-temperature distilled or filtered water (chlorine-free — tap water dechlorinated 24h in an open container is fine) to a fixed height `H` (record this precisely; it enters the Rayleigh number as `H³`, the most sensitive parameter).
5. Prepare a small syringe of food-coloring dye (or, for a more quantitative test, 1–5 µm polystyrene microspheres — cheap, available from science-hobbyist suppliers — imaged with a phone camera and simple image-processing script for a semi-quantitative mixing measure).

### A.4 Procedure

1. **Compute your target `ΔT_c`** for your actual tube diameter `H` (use it as the height in the vertical convection cell, not the WPA line diameter — this test uses a taller water column for practical bench access, so recompute `Ra_c` via `scripts/run_regime_sweep.py`-style code with your `H`, or ask: `python3 -c "from eclss_gravity import buoyancy, constants; print(buoyancy.critical_delta_T(constants.G_EARTH, constants.water_thermal_expansion(), YOUR_H_METERS, constants.water_kinematic_viscosity(), constants.water_thermal_diffusivity()))"` from the repo's `.venv`).
2. Let the water column equilibrate to a uniform temperature (both thermocouples within 0.05 K of each other) before each run.
3. Set the bottom heater to establish a target `ΔT` (bottom warmer than top — this is the destabilizing, convection-favorable orientation the model requires; see the important caveat in §A.5).
4. Once `ΔT` is stable (both thermocouples steady for 2 minutes), introduce the dye/tracer at the top of the column via the syringe, released gently to minimize injection-induced mixing.
5. Record (video, or timestamped photos) the tracer's spread for 30 minutes.
6. Repeat at `ΔT` = 0.5×, 1×, 1.5×, 2×, and 4× your computed `ΔT_c`. **Minimum 3 repetitions per `ΔT` level** for statistical validity (mixing onset can be somewhat stochastic near the threshold).
7. Reset to a uniform-temperature baseline between every run (drain and refill, or actively mix and re-equilibrate) to avoid residual stratification carrying over.

### A.5 Safety

- Heating tape/immersion circulator: follow the manufacturer's max-temperature rating; do not exceed ~40°C water temperature (well below any scalding risk, and keeps `β`/`ν`/`α` close to the 25°C values used in the model — see `docs/derivation.md` §6.6 for the ±10% sensitivity over 15–45°C).
- Standard electrical safety for any heating element near water: use a GFCI-protected outlet, keep all electrical connections away from splash zones, never leave an energized heater unattended.
- No hazardous chemicals; food-coloring dye and (if used) polystyrene microspheres are non-toxic at these quantities. If you use microspheres, avoid inhaling the dry powder before suspension — wear a basic dust mask when opening the vial.
- Glass/acrylic tube: handle empty tube carefully (edges), and do not use a tube rated below the small hydrostatic pressure of your column (trivial for any of the tube options in the BOM at these heights).

### A.6 Data handling

Record: `ΔT` (K), `H` (m), qualitative mixing onset time (or "no mixing observed in 30 min"), and if using microspheres, image timestamps for a simple pixel-intensity-spread analysis. Save as a CSV with columns `trial, delta_T_K, H_m, mixing_onset_s, notes`. A short analysis script comparing your empirical mixing-onset `ΔT` against the model's `Ra_c=1708` prediction would live at `src/eclss_gravity/validation_compare.py` (not yet written — this is a natural next step for whoever runs this test, using `buoyancy.rayleigh_number` and `buoyancy.critical_delta_T` from the existing package as the comparison target).

### A.7 Expected result and interpretation

If the model is right: no visible mixing below `ΔT_c`, clear mixing above it, with the transition sharpening as trial count increases. If mixing occurs well below the predicted `ΔT_c`, or fails to occur well above it, that specifically implicates the `Ra_c=1708`-for-an-infinite-plane-layer assumption (`docs/derivation.md` assumption A18, and `docs/redteam_report.md` Finding 2.4's point that a *tube* is not an infinite plane layer — the true critical Rayleigh number for a horizontal-gradient-free vertical cylinder may differ by an O(1) factor). That would be a genuine, reportable, quantitative correction to the model, not just a validation failure.

---

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
