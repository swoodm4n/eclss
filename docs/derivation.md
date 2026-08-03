# A Dimensionless Criterion for Gravity-Driven Microbial Transport in ECLSS Water Loops

**Phase 3 — first-principles derivation**
**Date:** 2026-08-03
**Status:** Derivation complete; ready for implementation. All numerical values below are reproducible from the equations and the parameter table in §8.

> **ERRATUM (Phase 4, added after an independent adversarial red-team review — see
> `redteam_report.md` and `limitations.md` §2 for the full account).** The physics and algebra
> below (§§0-8) were independently re-derived and checked and are correct. However, several
> headline **conclusions** drawn from that correct algebra are wrong or overclaimed as
> originally stated here, and were corrected in the code (`src/eclss_gravity`) and in
> `limitations.md`, not in this file's prose:
> - **§3.5's "strongest single result"** (lowering gravity suppresses convection and increases
>   net dormancy deposition, illustrated ~10⁵-10⁶× in the original fig3) is **retracted as
>   stated**. The implementation had omitted the eq. (5.3) biofilm growth term; with it
>   restored, the long-time dormancy outcome is nearly gravity-independent (growth kinetics
>   dominate once any deposit seeds), though the deposition *rate* still differs by ~1700x.
>   Separately, `Ra_c=1708` (§2.2b) requires a vertical destabilizing thermal gradient that a
>   real spacecraft line will not generically have — this was not stated as an assumption below
>   and should be read as a significant, not minor, caveat on all of §3.5/§2.2(b).
> - **§3.2's headline `g* = 0.238 g_E`** is over-precise by roughly 50x across this
>   document's own assumed-parameter ranges, and is sensitive to a convention choice
>   (`cos θ=1` vs. the perimeter-averaged `f_θ=1/π` this document itself derives in §5.3 as
>   correct) that §3.2 did not carry through consistently with §5.3. See `limitations.md` for
>   the corrected, uncertainty-quantified statement.
> - **§3.3's `Λ_g` used a channel half-depth (`R=D/2`)** while identifying itself with the
>   classical Hazen surface-overflow number, which requires the full depth. This changes the
>   quoted 100 µm floc example (see `limitations.md`; the 183 µm example survives).
> - **§3.6's novelty anchor (Konishi/Mudawar/Hasan, two-phase flow boiling) is the wrong
>   field.** The closer, and older, prior art is colloid-filtration theory (Yao/Habibian/
>   O'Melia 1971; Tufenkji/Elimelech 2004; Pich 1972) — see `problem_statement.md` §7 for the
>   corrected novelty framing.
>
> Treat the equations and parameter values in this document as reliable (they were
> independently reproduced to within 0.3%); treat any specific headline claim or conclusion
> sentence as superseded by `limitations.md` and the current code/tests unless you have checked
> it was not on the list above.

---

## 0. Scope, conventions, and an honest statement of source fidelity

### 0.1 What this document is

This is the core physics derivation for the problem committed to in `docs/problem_statement.md`: a
Konishi/Mudawar/Hasan-style **"when does gravity matter"** criterion, transferred from two-phase
flow boiling to **microbial and biofilm transport** in pumped and stagnant ECLSS water loops
(WPA, UPA, MABR).

It delivers:

- a precise physical system definition with real, sourced operating parameters (§1);
- transport velocities derived from first principles, with validity checks (§2);
- **three** dimensionless criteria, derived (not asserted), plus their closed-form gravity thresholds `g*` (§3);
- an explicit reconciliation with the growth-rate literature the adjudicator flagged as the hidden
  invalidating assumption for the original Candidate A (§4);
- a fully specified 1-D advection–diffusion–reaction PDE model ready for Python implementation (§5);
- every assumption with its validity range (§6);
- an uncertainty ranking and a recommended propagation strategy (§7);
- a parameter table (§8) and an implementation checklist (§9).

### 0.2 Citation-fidelity convention (inherited from `novelty_adjudication.md` §0)

- **[verified-existence]** — the source demonstrably exists with the stated title/authors/venue,
  corroborated across independent search result sets.
- **[snippet-level]** — the *content* assertion comes from search-result summarisation, **not** from
  reading the full text. Must be re-checked against the PDF before submission.
- **ASSUMED (not sourced)** — a value I could not find. Every such value is labelled inline with the
  value, the reason it is a defensible placeholder, and the sensitivity of the result to it.

**Network constraint, re-confirmed for this session.** `WebFetch` was tested directly against
`ntrs.nasa.gov`, `ttu-ir.tdl.org` (the Texas Tech repository that hosts ICES proceedings),
`engineering.purdue.edu`, `frontiersin.org` and `ncbi.nlm.nih.gov`. **All returned HTTP 403 at the
proxy.** `WebSearch` works and is how every citation below was found. Therefore **no full text was
read in producing this document**, and every content claim about a cited paper is `[snippet-level]`
by construction. This is the same constraint recorded in `problem_statement.md` §4 and it has not
lifted.

### 0.3 Notation

| Symbol | Meaning | SI units |
|---|---|---|
| `g` | gravitational acceleration | m s⁻² |
| `a` | particle (cell/floc) equivalent-sphere radius | m |
| `d = 2a` | particle equivalent-sphere diameter | m |
| `ρ_p, ρ_f` | particle and fluid density | kg m⁻³ |
| `Δρ = ρ_p − ρ_f` | excess (buoyant) density | kg m⁻³ |
| `μ, ν` | fluid dynamic / kinematic viscosity | Pa s, m² s⁻¹ |
| `D` | channel hydraulic diameter | m |
| `R = D/2` | channel half-height / tube radius | m |
| `L`, `x` | segment length / streamwise coordinate | m |
| `U` | cross-section-mean (bulk) velocity | m s⁻¹ |
| `γ_w` | wall shear rate | s⁻¹ |
| `τ_w = μ γ_w` | wall shear stress | Pa |
| `u* = √(τ_w/ρ_f)` | friction velocity | m s⁻¹ |
| `v_s` | Stokes settling velocity | m s⁻¹ |
| `D_B` | particle Brownian diffusivity | m² s⁻¹ |
| `k_w` | hydrodynamic wall-transport (deposition) velocity | m s⁻¹ |
| `k_B, T` | Boltzmann constant, absolute temperature | J K⁻¹, K |
| `θ` | angle between **g** and the inward wall normal | rad |

Gravity levels used throughout, per `problem_statement.md` §1:
**Earth 9.81, Mars 3.71, Moon 1.62 m s⁻²** (these are exactly the values used in the reduced-gravity
two-phase literature, e.g. the flow-regime-transition computations at 0.196 / 1.62 / 3.71 / 9.81
m s⁻² noted in `novelty_adjudication.md` C-3 `[snippet-level]`), plus the near-zero/stagnant limit.

---

## 1. Physical system definition

### 1.1 The canonical geometry

The system is a **single wetted channel segment** of an ECLSS water loop:

```
                        z = 0                                          z = L
                          |                                              |
   inlet  C_in, S_in  --> |==============================================| --> outlet
                          |  bulk liquid: planktonic cells C, substrate S |
                          |----------------------------------------------|
   wall (biofilm layer X, areal density kg m⁻²)      ^ deposition   v detachment
                          |----------------------------------------------|
                                        g  (angle θ to wall normal)
```

- **Bulk phase**: water carrying planktonic cells and multicellular flocs/aggregates at low volume
  fraction, plus a growth-limiting dissolved substrate (measured operationally as TOC).
- **Wall phase**: an attached biofilm of areal dry-biomass density `X`.
- **Gravity** enters through (i) the wall-normal settling flux, (ii) the onset and strength of
  buoyancy-driven convection in stagnant segments, and (iii) the orientation factor `cos θ`.

Four regimes are evaluated, spanning the operating envelope named in `problem_statement.md` §1:

| Regime | Physical instance | Character |
|---|---|---|
| **R1** Pumped nominal | WPA process line during a processing cycle | laminar forced flow |
| **R2** Post-restart transient | flush after dormancy | transitional/turbulent |
| **R3** Low-flow | UPA feed line, MABR shell side, filter housing | creeping flow |
| **R4** Stagnant | dormancy (≤ 1 yr), tank ullage, dead legs | `U → 0` |

### 1.2 Real operating parameters

**Water Processor Assembly (WPA).**
- Wastewater tank volume **68 L**; wastewater initially collected in a bellows tank of ~150 lb
  capacity; pumped through a **0.5 µm** depth filter to protect the multifiltration beds
  `[snippet-level]`. Source: Carter et al., *Performance Qualification Test of the ISS Water
  Processor Assembly (WPA) Expendables*, SAE 2005-01-2837 / NTRS 20050207388 `[verified-existence]`.
- **Process flow rate: 13 lb/hr = 5.90 kg/hr ≈ 5.90 L/hr = 1.639 × 10⁻⁶ m³ s⁻¹** ("the flight design
  flow rate of 13 lb/hr") `[snippet-level]`, same source.
- Pretreated urine feed to the WPA wastewater tank at **300 cm³/min (18 L/hr)** `[snippet-level]`.
- WPA wastewater **TOC commonly exceeds 2000 mg/L** `[snippet-level]`; ISS potable-water
  specification is **≤ 3 mg/L TOC** and **≤ 50 CFU/mL** `[snippet-level]`. Sources: *Status of ISS
  Water Management and Recovery*, ICES-2023-097 / NTRS 20230006217 `[verified-existence]`;
  Yamaguchi et al., *Bacterial bioburden and community structure of potable water used in the
  International Space Station*, **Sci. Rep. 12 (2022)**, DOI 10.1038/s41598-022-19320-3
  `[verified-existence]` — reports that typical in-flight levels are "a few CFU per mL", with
  documented excursions above the limit `[snippet-level]`.
- The VRA catalytic oxidation reactor operates at **265 °F ≈ 129 °C** `[snippet-level]` (NTRS
  20070021782) — relevant only as an upper bound; it is downstream of, and thermally isolated from,
  the biofilm-bearing wastewater side.

**Urine Processor Assembly (UPA).**
- Designed for a nominal load of **9 kg/day** of urine + flush water (6-crew ISS load); recovery
  85 % nominal, reduced to 75 % (US) / 70 % (RS) after the 2009 urine-quality issue `[snippet-level]`.
- Recycle loop: pretreated urine recirculates through the Distillation Assembly (DA), the Advanced
  Recycle Filter Tank Assembly (ARFTA), a brine filter, and back to the DA; DA throughput
  **1.76–1.93 kg/hr** during test campaigns `[snippet-level]`. Sources: *Upgrades to the ISS Urine
  Processor Assembly*, ICES-2021-083 / NTRS 20210015781 `[verified-existence]`; NASA/TM-1998-208539
  `[verified-existence]`.
- **Biofilm has been directly recovered from UPA flex lines**: Zea et al. / O'Rourke et al.,
  *Microbial isolation and characterization from two flex lines from the urine processor assembly
  onboard the International Space Station*, **Biofilm 5 (2023)**, DOI 10.1016/j.bioflm.2023.100115
  `[verified-existence]` — "first evidence of biofilm formation within flex lines from the UPA
  onboard the ISS"; fungal biofilm networks apparent in both lines; *Burkholderia*,
  *Paraburkholderia*, *Leifsonia*, *Fusarium*, *Lecythophora* recovered `[snippet-level]`.

**Membrane Aerated Biofilm Reactor (MABR).**
- Lab-scale space-wastewater MABR: **void volume 1.35 L**, vertically and centrally mounted fibre
  module of **1140 microporous polypropylene hollow fibres of 280 µm diameter**; **recirculation
  150 mL/min** promoting complete mixing and controlling biomass accumulation on the filaments
  `[snippet-level]`.
- PVDF hollow fibres with 0.1 µm pore size, 50 µm wall thickness, 50 % porosity; **HRT 2.0–10.7 h**
  `[snippet-level]`. Source cluster: Jackson et al., *Performance of a lab-scale membrane aerated
  biofilm reactor treating nitrogen dominant space-based wastewater through simultaneous
  nitrification–denitrification*, **J. Environ. Chem. Eng.** (2020/21) `[verified-existence]`;
  Christenson et al., *Integration of Full-Size Graywater Membrane-Aerated Biological Reactor with
  Reverse Osmosis System for Space-Based Wastewater Treatment*, **Membranes 14(6):127 (2024)**,
  DOI 10.3390/membranes14060127 `[verified-existence]`.
- **Exploration-class / partial-gravity design point**: Hooshyari & Jackson, *Partial gravity
  habitation water recovery using hybrid life support systems: Membrane aerated biological reactor
  integrated with a distillation system for urine recycling*, **J. Water Process Eng.** (2025),
  also SSRN 5156296 and ICES-2025 `[verified-existence]` — MABR pretreating urine + flush water
  coupled to static distillation, >2300 L treated, >90 % DOC removal `[snippet-level]`. This is the
  single closest published **partial-gravity** water-recovery hardware description found and is the
  natural target system for the criterion.

**Dormancy.** "Biofilm control is expected to be a challenge for long-term missions with a dormancy
period of **up to a year**, as stagnant water systems are highly susceptible to biofilm growth"
`[snippet-level]` — Li, Callahan et al., *A Preliminary Modeling Study of Biofilm Accumulation in the
Water Recovery System*, **ICES-2020-42** / NTRS 20205004391 `[verified-existence]`. Corroborated by
*Potential biofilm control strategies for extended spaceflight missions*, **Biofilm 2 (2020)**
`[verified-existence]`.

### 1.3 Derived geometric/flow operating points

The one parameter I could **not** source is the internal diameter of WPA/UPA process tubing. Repeated
searches for ISS water-line tubing dimensions returned only generic industrial guidance.

> **ASSUMED (not sourced): WPA/UPA process line internal diameter `D = 6.35 mm` (0.25 in).**
> Defensible because (a) 1/4-inch is the standard tube size for aerospace fluid lines at these flow
> rates; (b) at the sourced 13 lb/hr it yields `Re = 368`, comfortably laminar and physically
> sensible for a spacecraft water line; (c) §7 shows the headline result is only weakly sensitive to
> it — sweeping `D` over 3.18–12.7 mm (1/8″–1/2″) at fixed sourced flow rate moves the single-cell
> gravity threshold `g*` only from 0.48 to 0.12 `g_E`, i.e. it stays inside the partial-gravity
> range for every plausible diameter. **The code must expose `D` as a swept parameter, not a
> constant.**

> **ASSUMED (not sourced): analysis segment length `L = 0.5 m`** (0.30 m for the MABR module).
> This is a modelling choice, not a hardware claim: it sets the streamwise coordinate `x` in the
> Lévêque solution. `Ga_dif ∝ x^{1/3}` and `Ga_int ∝ x`, so it is reported explicitly everywhere.

> **ASSUMED (not sourced): MABR module length 0.30 m**, used with the sourced 1.35 L void volume to
> get a shell free-flow area of `1.35 L / 0.30 m = 4.50 × 10⁻³ m²`, minus fibre cross-section
> `1140 × (π/4)(280 µm)² = 7.02 × 10⁻⁵ m²`, giving `A ≈ 4.43 × 10⁻³ m²`. Wetted (fibre) area
> `1140 × π × 280 µm × 0.30 m = 0.301 m²`, hence hydraulic diameter
> `d_h = 4V/A_wet = 4(1.35×10⁻³)/0.301 = 17.95 mm`.

> **ASSUMED (not sourced): dead-leg / creep-flow velocity `U = 10⁻⁴ m s⁻¹`.** Chosen as a
> representative non-zero residual (thermal-expansion-driven, valve-leakage-driven) flow, one order
> below the slowest sourced operating point. Reported as a regime, not a measurement.

Computed operating points (water at 25 °C, §8):

| Regime | `D` (mm) | `U` (m s⁻¹) | `Re` | `γ_w` (s⁻¹) | `τ_w` (Pa) | `t_res` (s) |
|---|---|---|---|---|---|---|
| **R1** WPA line, nominal (13 lb/hr) | 6.35 | 5.175 × 10⁻² | 368 | 65.2 | 0.0580 | 9.7 |
| **R2** WPA line, restart flush (10×) | 6.35 | 5.175 × 10⁻¹ | 3681 | 1521 | 1.354 | 1.0 |
| **R3a** UPA feed line (9 kg/day) | 6.35 | 3.289 × 10⁻³ | 23.4 | 4.14 | 0.00369 | 152 |
| **R3b** MABR shell side (150 mL/min) | 17.95 | 5.643 × 10⁻⁴ | 11.3 | 0.252 | 0.000224 | 532 |
| **R4** Dead leg / creep | 6.35 | 1.0 × 10⁻⁴ | 0.7 | 0.126 | 0.000112 | 5000 |

`γ_w = 8U/D` for laminar duct flow; for R2 (`Re > 2300`) the Blasius correlation
`f = 0.316 Re^{−1/4}`, `τ_w = (f/8)ρ_f U²` is used instead.

### 1.4 Biological particle classes

The organisms repeatedly documented in ISS water systems are *Burkholderia* (incl. *B. contaminans*,
*B. multivorans*), *Ralstonia insidiosa*, *Cupriavidus metallidurans*, *Methylobacterium* spp.,
*Sphingomonas*, *Stenotrophomonas maltophilia* and *Pseudomonas aeruginosa* `[snippet-level]`
(Sci. Rep. 12 (2022) 19320 `[verified-existence]`; *Genome Sequences of Bacteria Isolated from the
ISS Water Systems*, **Microbiol. Resour. Announc.** (2023), DOI 10.1128/mra.00158-23
`[verified-existence]`; O'Rourke et al., *Biofilm formation is correlated with low nutrient and
simulated microgravity conditions in a Burkholderia isolate from the ISS water processor assembly*,
**Biofilm 5 (2023)** `[verified-existence]`).

All are Gram-negative rods of similar size. I use *P. aeruginosa* dimensions as the representative
single-cell geometry because they are the best-quantified:

- **Cell dimensions: 0.5–0.8 µm width × 1.5–3.0 µm length**, with an SEM-measured mean diameter of
  **0.65 µm** `[snippet-level]`. Taking `d_c = 0.65 µm`, `L_c = 2.25 µm` (midpoint) and modelling
  the rod as a cylinder with hemispherical caps:

  `V_cell = (π/4)d_c²(L_c − d_c) + (π/6)d_c³ = 0.675 µm³`
  `a_cell = (3V/4π)^{1/3} = 0.544 µm`, i.e. **equivalent-sphere diameter 1.088 µm**.

- **Cell density**: *E. coli* banded in Percoll at **1.080–1.100 g mL⁻¹** depending on growth rate
  and centrifugation temperature; 1.091 g mL⁻¹ at 150 mOsM and 1.101 g mL⁻¹ at 500 mOsM
  `[snippet-level]`. Sources: Martínez-Salas, Martín & Vicente, *Relationship of Escherichia coli
  density to growth rate and cell age*, and Baldwin & Kubitschek, *Buoyant density variation during
  the cell cycle of Escherichia coli* / *Variation in Escherichia coli buoyant density measured in
  Percoll gradients*, **J. Bacteriol. 148(1):58–63 (1981)** `[verified-existence]`.
  ⇒ **`Δρ_cell = 83–103 kg m⁻³`, nominal 93.**
  *Caveat: this is measured for E. coli, not for the ISS isolates.* No buoyant-density measurement
  for *Burkholderia*/*Ralstonia* was found; substituting the *E. coli* value is a cross-species
  transfer and is flagged as such in §6 and §7.

- **Aggregates/flocs.** Two independent size scales are documented:
  - Activated-sludge floc: *most particles < 5 µm by number, but the majority of the volume is in
    flocs of* **68–183 µm** `[snippet-level]` — Jenné/Van Impe et al. via *Characterization of
    activated sludge flocs by confocal laser scanning microscopy and image analysis*, **Water Res.**
    `[verified-existence]`.
  - Biofilm detachment: *"detaching biomass ranges from single cells to an aggregate with a diameter
    of approximately* **500 µm**"; and *"more than 80 % of clusters detached … are* **≤ 7 µm** *in
    diameter"* `[snippet-level]` — from the detachment/sloughing literature
    (*Detachment characteristics of a mixed culture biofilm using particle size analysis*,
    **Chem. Eng. J.** (2013) `[verified-existence]`; *Growth and Detachment of Cell Clusters from
    Mature Mixed-Species Biofilms*, **Appl. Environ. Microbiol. 67(12):5608 (2001)**
    `[verified-existence]`).
  - **Floc density**: activated-sludge aggregate densities **1.038 g mL⁻¹** (slow-settling) to
    **1.065 g mL⁻¹** (fast-settling) `[snippet-level]` — *Density and Activity Characterization of
    Activated Sludge Flocs* / *On the free-settling test for estimating activated sludge floc
    density*, **Water Res.** (1995) `[verified-existence]`.
    ⇒ **`Δρ_floc = 38–68 kg m⁻³`, nominal 50.**
  - Biofilm wet density measured at **1011–1029 kg m⁻³** (colonised vs non-colonised carriers) and
    as low as 898 kg m⁻³ `[snippet-level]` (*Calculation, Measurement and Validation for Estimating
    the Biomass of the Biofilm on Microcarriers*, **ChemEngineering 10(2):23** `[verified-existence]`)
    — consistent with, and at the low end of, the floc range. **Note the 898 kg m⁻³ value is
    *negatively* buoyant-density (`Δρ < 0`, i.e. it would rise); this is a real physical possibility
    for gas-entrapping biofilm and is flagged in §7 as a sign-uncertainty.**

Working particle classes used throughout:

| Class | `d` | `Δρ` (nominal) | Rationale |
|---|---|---|---|
| P1 single cell | 1.088 µm | 93 | *P. aeruginosa* equivalent sphere |
| P2 small aggregate | 7 µm | 50 | >80 % of detached clusters are ≤ this |
| P3 median floc | 100 µm | 50 | inside the 68–183 µm volume-dominant band |
| P4 large floc | 183 µm | 50 | upper end of the volume-dominant band |
| P5 sloughed piece | 500 µm | 50 | upper bound of observed detachment |

---

## 2. Transport velocities from first principles

### 2.1 Gravity-driven: Stokes settling

For a rigid sphere of radius `a` in creeping flow, force balance between buoyant weight and Stokes
drag (`F_D = 6πμ a v`):

```
(4/3)π a³ Δρ g  =  6 π μ a v_s
```

giving the **Stokes settling velocity**

```
                2  Δρ g a²
    v_s   =    ───────────                                              (2.1)
                9     μ
```

Direct proportionality to `g` is the entire basis of the criterion: `v_s(g) = v_s(g_E)·(g/g_E)`.

**Validity.** Eq. (2.1) requires particle Reynolds number `Re_p = ρ_f v_s d / μ ≪ 1`. Computed at
25 °C:

| Class | `v_s` Earth (m s⁻¹) | `v_s` Mars | `v_s` Moon | `Re_p` (Earth) | Schiller–Naumann factor |
|---|---|---|---|---|---|
| P1 cell (1.088 µm) | 6.744 × 10⁻⁸ | 2.550 × 10⁻⁸ | 1.114 × 10⁻⁸ | 8.2 × 10⁻⁸ | 1.000 |
| P2 agg (7 µm) | 1.500 × 10⁻⁶ | 5.674 × 10⁻⁷ | 2.478 × 10⁻⁷ | 1.2 × 10⁻⁵ | 1.000 |
| P3 floc (100 µm) | 3.062 × 10⁻⁴ | 1.158 × 10⁻⁴ | 5.056 × 10⁻⁵ | 3.4 × 10⁻² | 1.015 |
| P4 floc (183 µm) | 1.025 × 10⁻³ | 3.878 × 10⁻⁴ | 1.693 × 10⁻⁴ | 2.1 × 10⁻¹ | 1.051 |
| P5 sloughed (500 µm) | 7.654 × 10⁻³ | 2.895 × 10⁻³ | 1.264 × 10⁻³ | **4.29** | **1.408** |

**Stokes' law is valid for P1–P4 and fails for P5.** The correction is the Schiller–Naumann drag
correlation, `C_D = (24/Re_p)(1 + 0.15 Re_p^{0.687})`, which turns (2.1) into the implicit relation

```
                2  Δρ g a²          1
    v_s   =    ───────────  ·  ─────────────────                        (2.2)
                9     μ         1 + 0.15 Re_p^{0.687}
```

solved by fixed-point iteration (`Re_p` evaluated at the current `v_s`). Solving (2.2):

| Class | `g` | Stokes `v_s` | Schiller–Naumann `v_s` | `Re_p` | Stokes error |
|---|---|---|---|---|---|
| P4 183 µm | Earth | 1.025 × 10⁻³ | 9.768 × 10⁻⁴ | 0.200 | **+5.0 %** |
| P5 500 µm | Earth | 7.654 × 10⁻³ | 5.736 × 10⁻³ | 3.21 | **+33.4 %** |
| P5 500 µm | Mars | 2.895 × 10⁻³ | 2.441 × 10⁻³ | 1.37 | +18.6 % |
| P5 500 µm | Moon | 1.264 × 10⁻³ | 1.139 × 10⁻³ | 0.64 | +11.0 % |
| 1000 µm | Earth | 3.062 × 10⁻² | 1.500 × 10⁻² | 16.8 | +104 % |

Solving for the diameter at which the Stokes error reaches 5 % (`Re_p ≈ 0.34`) at `Δρ = 50`:

```
    d_max(Earth) = 184 µm      d_max(Mars) = 254 µm      d_max(Moon) = 335 µm     (2.3)
```

**This is itself a gravity-dependent result worth stating in the paper:** the Stokes regime extends
to larger aggregates as gravity falls, so a partial-gravity model may legitimately use the simpler
law over a wider size range than a 1-g model. The code must nonetheless implement (2.2) and fall
back to (2.1) only when `Re_p < 0.34`.

### 2.2 Gravity-driven: buoyancy convection — is it real here?

The task asks for an honest assessment rather than a forced symmetry with the two-phase analogy.
There are three candidate buoyancy mechanisms; they do **not** all survive.

**(a) Cell-scale solutal convection from metabolism — negligible.** The Klaus/Gesztesi line of work
models the density perturbation a single cell creates in its own neighbourhood by consuming
substrate and excreting waste. The reported finding is that *"fluid density changes surrounding
individual bacteria were found to be too small to measure directly"* `[snippet-level]`
(Benoit & Klaus, *Responses, applications, and analysis of microgravity effects on bacteria*, PhD
2005, and the *Microgravity Effect on Bacterial Growth: A Literature Review*, ICES-2022-269 /
ICES-2024-44 `[verified-existence]`). Gesztesi et al., *The chemical neighborhood of cells in a
diffusion-limited system*, **Front. Microbiol. 14:1155726 (2023)** `[verified-existence]`, quantify
the *diffusive* depletion zone (10 % substrate reduction at **5.04 mm** radius for a single *E. coli*
cell `[snippet-level]`) precisely because they have removed sedimentation and density-driven
convection. **I therefore drop this term** and state so explicitly: at ECLSS bulk cell densities the
per-cell density perturbation is orders below the bulk perturbations in (b)/(c), and including it
would be false precision.

**(b) Bulk thermal convection in stagnant segments — real, and it is the dominant buoyancy term.**
A stagnant water line or tank subject to a vertical temperature difference `ΔT` across depth `H` has
Rayleigh number

```
              g β ΔT H³
    Ra   =   ───────────                                                (2.4)
                ν α_th
```

Convection sets in above `Ra_c ≈ 1708` (Rayleigh–Bénard, rigid–rigid). Inverting for the
**critical temperature difference**:

```
                1708 · ν α_th
    ΔT_c   =   ───────────────      ⇒     ΔT_c ∝ 1/g  and  ∝ 1/H³        (2.5)
                  g β H³
```

Evaluated with water at 25 °C (`β = 2.57 × 10⁻⁴ K⁻¹`, `α_th = 1.46 × 10⁻⁷ m² s⁻¹`,
`ν = 8.93 × 10⁻⁷ m² s⁻¹`):

| `H` | `ΔT_c` Earth (K) | `ΔT_c` Mars (K) | `ΔT_c` Moon (K) |
|---|---|---|---|
| 1 mm | 88.3 | 233 | 535 |
| **6.35 mm (line)** | **0.345** | **0.912** | **2.088** |
| 25.4 mm (filter housing) | 5.39 × 10⁻³ | 1.43 × 10⁻² | 3.26 × 10⁻² |
| 100 mm | 8.83 × 10⁻⁵ | 2.34 × 10⁻⁴ | 5.35 × 10⁻⁴ |
| **300 mm (tank)** | **3.27 × 10⁻⁶** | 8.65 × 10⁻⁶ | 1.98 × 10⁻⁵ |

This is a **sharp, gravity-controlled switch and one of the more actionable results in the
derivation**: a stagnant 6.35 mm ISS water line convects if the vertical `ΔT` across it exceeds
~0.35 K at Earth gravity, but needs ~0.91 K at Mars gravity and ~2.09 K at lunar gravity. Cabin-to-
line temperature gradients of a few tenths of a kelvin are entirely ordinary, so **reducing gravity
can switch bulk convection off in narrow lines**. In tanks (`H ~ 0.3 m`) `ΔT_c ~ 10⁻⁶ K` and
convection is unconditionally present at all three gravity levels.

Characteristic convective velocity, near onset and far above it:

```
    u_conv  ≈  (ν/H) √(Ra/Ra_c − 1)          (near onset)               (2.6a)
    u_conv  ≈  0.1 √(g β ΔT H)               (Ra ≫ Ra_c)                (2.6b)
```

| Case | `Ra` | `u_conv` (m s⁻¹) |
|---|---|---|
| Line `H`=6.35 mm, `ΔT`=1 K, Earth | 4953 | 1.94 × 10⁻⁴ (2.6a) |
| Line `H`=6.35 mm, `ΔT`=1 K, Mars | 1873 | 4.37 × 10⁻⁵ (2.6a) |
| Line `H`=6.35 mm, `ΔT`=1 K, Moon | **818 < Ra_c** | **0 — no convection** |
| Tank `H`=0.30 m, `ΔT`=0.1 K, Earth | 5.2 × 10⁷ | 8.70 × 10⁻⁴ (2.6b) |
| Tank `H`=0.30 m, `ΔT`=0.1 K, Mars | 2.0 × 10⁷ | 5.35 × 10⁻⁴ (2.6b) |
| Tank `H`=0.30 m, `ΔT`=0.1 K, Moon | 8.6 × 10⁶ | 3.53 × 10⁻⁴ (2.6b) |

**Both gravity-driven velocities scale with `g`** (`v_s ∝ g`; `u_conv ∝ g^{1/2}` well above onset,
and `∝ g` near onset) — so the criterion's `g`-dependence is structurally robust. But they **oppose
each other**: sedimentation carries cells *to* the wall, convection keeps them *suspended*. This is
the transport-side analogue of the two-opposing-mechanisms decomposition reported by Latham,
Skountzos & Lawson (§4), and it is why a single scalar "gravity effect" is the wrong object.

Define the **suspension–settling competition number**

```
              v_s
    Ω    =   ───────                                                    (2.7)
             u_conv
```

For a 0.30 m tank at `ΔT = 0.1 K`: `Ω(cell) = 7.8 × 10⁻⁵` (Earth) → **convection completely
overwhelms single-cell settling in a convecting tank**; `Ω(100 µm floc) = 0.35`; `Ω(183 µm) = 1.18`;
`Ω(500 µm) = 8.8`. So in a convecting tank only flocs ≳ 150 µm actually reach the floor; cells stay
suspended. In a *non*-convecting narrow line (`Ra < Ra_c`), `Ω → ∞` and settling is unopposed.

**(c) Solutal convection from bulk composition gradients — real in the UPA only.** The UPA
concentrates urine to 70–85 % water recovery, producing strong brine density stratification in the
ARFTA. This is a genuine buoyancy source but it is a *stratifying* (stabilising) gradient that
**suppresses** vertical mixing rather than driving it. I note it as a bounding effect and do not
model it: it can only make the settling-dominated conclusion stronger. Flagged in §6.

### 2.3 Forced advection

From the sourced volumetric flow rate `Q` and cross-sectional area `A`:

```
    U = Q / A                                                           (2.8)
```

Values in §1.3. Note `U` is **axial** — parallel to the wall — whereas `v_s` (for a horizontal
channel) is **wall-normal**. §3.1 explains why comparing them directly is the central error to avoid.

### 2.4 Wall shear and the hydrodynamic wall-transport velocity

For fully developed laminar flow in a circular duct the wall shear rate and stress are

```
    γ_w = 8U/D  ,   τ_w = μ γ_w  ,   u* = √(τ_w/ρ_f)                    (2.9)
```

(For `Re > 2300`, `τ_w = (f/8)ρ_f U²` with Blasius `f = 0.316 Re^{−1/4}`, and `γ_w ≡ τ_w/μ` is the
equivalent viscous-sublayer shear rate.)

Forced flow delivers particles to the wall by **two** mechanisms, and the correct competitor for
gravity is whichever is larger.

**(i) Convective diffusion (Lévêque / Smoluchowski–Levich).** In the near-wall region the velocity
profile is linear, `u = γ_w y`. The steady convection–diffusion equation for a perfect-sink wall is

```
    γ_w y ∂C/∂x  =  D_B ∂²C/∂y²  ,   C(y=0)=0 ,  C(y→∞)=C_∞
```

With the similarity variable `η = y (γ_w /(9 D_B x))^{1/3}` the solution is
`C/C_∞ = Γ(4/3)^{-1} ∫₀^η e^{−s³} ds`, and the wall flux is

```
    J = D_B (∂C/∂y)|₀ = C_∞ D_B^{2/3}(γ_w/x)^{1/3} / (9^{1/3} Γ(4/3))
```

Since `9^{1/3} Γ(4/3) = 2.0801 × 0.89298 = 1.8575`, the deposition velocity is

```
    k_lev  =  0.538 · D_B^{2/3} (γ_w / x)^{1/3}                         (2.10)
```

with the particle Brownian diffusivity from Stokes–Einstein

```
    D_B  =  k_B T / (6 π μ a)                                           (2.11)
```

The 0.538 prefactor is exactly the coefficient used in the bacterial-adhesion flow-chamber
literature, which is the correct provenance for this application (see §3.4).

**(ii) Interception.** Diffusion is hopeless for large flocs (`D_B(183 µm) = 2.7 × 10⁻¹⁵ m² s⁻¹`).
The physically honest competitor there is *interception*: a particle whose centre passes within one
radius of the wall touches it. The flux of centres through the near-wall layer of thickness `a`,
per unit wall area over a streamwise distance `x`, is `C ∫₀^a γ_w y dy / x`, giving an equivalent
deposition velocity

```
    k_int  =  γ_w a² / (2 x)                                            (2.12)
```

The hydrodynamic wall-transport velocity is therefore

```
    k_w  =  max( k_lev , k_int )                                        (2.13)
```

The two branches cross where `k_lev = k_int`. Setting (2.10) = (2.12) and using (2.11):

```
    a_c  =  1.076^{3/8} · ( k_B T / (6πμ) )^{1/4} · ( x / γ_w )^{1/4}   (2.14)
```

Evaluated: `a_c = 6.8 µm` for R1 (WPA line), 3.1 µm for R2 (flush), 32 µm for R4 (dead leg).
So **Brownian diffusion is the relevant competitor only for single cells and the smallest
aggregates (d ≲ 6–60 µm); interception governs everything larger.** Because `a_c ∝ (x/γ_w)^{1/4}`,
this boundary is extremely insensitive to operating conditions — a useful robustness property.

### 2.5 Motility — the competing self-propulsion velocity

Motile cells swim, and swimming is not a function of `g`. Measured mean swimming speed for
*Pseudomonas putida* wild-type is **32.1 ± 0.3 µm s⁻¹** `[snippet-level]` (biorxiv
2022.08.03.502738, *Role of the two flagellar stators in swimming motility of Pseudomonas putida*
`[verified-existence]`; comparable methodology in Toutain et al., *Evidence for two flagellar
stators and their role in the motility of Pseudomonas aeruginosa*, **J. Bacteriol. (2005)**, PMID
15629949 `[verified-existence]`).

Ratio `v_s / v_swim`:

| Class | Earth | Mars | Moon |
|---|---|---|---|
| P1 single cell | 2.1 × 10⁻³ | 7.9 × 10⁻⁴ | 3.5 × 10⁻⁴ |
| P2 7 µm aggregate | 4.7 × 10⁻² | 1.8 × 10⁻² | 7.7 × 10⁻³ |
| P3 100 µm floc | 9.5 | 3.6 | 1.6 |

**For a motile single cell, self-propulsion exceeds gravitational settling by ~500× at Earth
gravity and ~3000× at lunar gravity.** This is directly corroborated experimentally: Korber,
Lawrence, Zhang & Caldwell, *Effect of gravity on bacterial deposition and orientation in laminar
flow environments*, **Biofouling 2:335–350 (1990)** `[verified-existence]` found that **wild-type
organisms deposited on upper and lower surfaces independent of gravity, whereas flagellar mutants
deposited on lower surfaces at 10–40× the rate of deposition to upper surfaces** `[snippet-level]`.

This is a **first-order caveat on the whole criterion**, not a footnote: the criterion applies to
*non-motile or motility-repressed* cells and to all aggregates (flocs are far too large to be
propelled by their constituent flagella). §6 states the validity boundary; §7 ranks it as the
second-largest uncertainty. It also happens to be the same restriction the Klaus/Gesztesi
depletion-zone mechanism carries ("non-motile cells in quiescent suspension") — so the criterion
inherits, rather than escapes, that scope limit, and the paper must say so.

---

## 3. The dimensionless criteria

### 3.1 Why the obvious criterion is the wrong one

The intuitive move — and the one implicit in `novelty_adjudication.md` §1 ("Forced advection and
wall shear exceed cell-scale sedimentation velocity (∝ g) … by orders of magnitude") — is to compare
`v_s` with `U`:

| Regime | `v_s/U`, single cell | `v_s/U`, 100 µm floc |
|---|---|---|
| R1 WPA line | 1.3 × 10⁻⁶ | 5.9 × 10⁻³ |
| R3a UPA feed | 2.1 × 10⁻⁵ | 9.3 × 10⁻² |
| R3b MABR | 1.2 × 10⁻⁴ | 5.4 × 10⁻¹ |
| R4 dead leg | 6.7 × 10⁻⁴ | 3.1 |

Read naively this says "gravity is negligible by six orders of magnitude in the WPA," which is the
trivial-result failure mode the problem statement names as its single biggest risk.

**It is the wrong comparison, and identifying why is a substantive part of the contribution.**
In a horizontal channel `U` is *parallel* to the wall and `v_s` is *perpendicular* to it. They are
orthogonal components and their ratio is not a competition — a fast axial flow does not prevent a
particle from falling; it only shortens the time available. The physically meaningful competitions
are three, and they map cleanly (and non-arbitrarily) onto the three-criterion structure of
Konishi, Mudawar & Hasan (§3.4):

1. **Does gravity dominate the delivery of cells to the wall?** → compare `v_s` with `k_w`, the
   *wall-normal* hydrodynamic transport velocity. → `Ga_dep`
2. **Is there enough channel length for gravity to act before the particle exits?** → compare the
   settling time across the channel with the residence time. → `Λ_g`
3. **Once at the wall, does gravity matter for whether the particle stays?** → compare submerged
   weight with hydrodynamic removal force. → `Σ_g`

Gravity is negligible for biofilm accumulation **only if all three are ≪ 1 simultaneously**.

### 3.2 Criterion 1 — `Ga_dep`: gravitational vs hydrodynamic wall delivery

**Derivation.** Both mechanisms are expressed as a flux of particles onto unit wall area, `J = k C`,
with `k` an effective deposition velocity. Gravity contributes `J_g = v_s cos θ · C`. Forced flow
contributes `J_h = k_w C` with `k_w` from (2.13). Their ratio is dimensionless by construction:

```
                 J_g        v_s cos θ
    Ga_dep  =   ─────  =   ───────────                                  (3.1)
                 J_h           k_w
```

Take `cos θ = 1` (horizontal channel, lower wall) for the bounding case.

**Closed form, diffusion branch (`a < a_c`).** Substituting (2.1), (2.10), (2.11):

```
                    2 Δρ g a²/(9μ)
    Ga_dif  =  ───────────────────────────
                0.538 · (k_BT/6πμa)^{2/3} (γ_w/x)^{1/3}

                 2 (6π)^{2/3}       Δρ g a^{8/3}      ⎛  x  ⎞^{1/3}
            =   ──────────────  ·  ───────────────  · ⎜─────⎟
                  9 × 0.538          μ^{1/3}(k_BT)^{2/3}  ⎝ γ_w ⎠
```

```
                          Δρ · g · a^{8/3}        ⎛  x  ⎞^{1/3}
    Ga_dif  =  2.925 · ────────────────────────·  ⎜─────⎟            (3.2)
                        μ^{1/3} (k_B T)^{2/3}     ⎝ γ_w ⎠
```

**This is the central analytic result.** Note the exponent: **`Ga_dif ∝ a^{8/3}`**, not `a²`. The
`a²` comes from Stokes settling and a further `a^{2/3}` from the Stokes–Einstein diffusivity in the
denominator. Between a single cell (`a` = 0.54 µm) and a 100 µm floc (`a` = 50 µm) this is an
amplification of `(50/0.54)^{8/3} = 1.76 × 10⁵`. **Particle/floc size is by a wide margin the
dominant parameter**, which is why §7 makes floc-size distribution the priority for uncertainty
propagation. Dependence on temperature (`T^{−2/3}`), viscosity (`μ^{−1/3}`), shear (`γ_w^{−1/3}`)
and length (`x^{1/3}`) is weak — all cube-root-ish. Only `g`, `Δρ` and `a` matter strongly.

**Closed form, interception branch (`a > a_c`).** Substituting (2.1) and (2.12):

```
                 2 Δρ g a²/(9μ)         4  Δρ g x
    Ga_int  =  ──────────────────  =   ─── ─────────                    (3.3)
                 γ_w a² /(2x)           9   μ γ_w
```

**The particle radius cancels exactly.** Above the crossover size the criterion is
**size-independent** — it depends only on `Δρ g x /(μ γ_w)`. This is a clean and, I think,
genuinely interesting structural result: floc-size uncertainty, which dominates everything below
~7 µm, *stops mattering at all* above it. Physically: both settling and interception scale as the
particle's cross-section, so they scale together.

**Gravity thresholds.** Setting `Ga = 1` and solving for `g`:

```
                 μ^{1/3} (k_B T)^{2/3}   ⎛ γ_w ⎞^{1/3}
    g*_dif  =  ──────────────────────── ⎜─────⎟                        (3.4)
                  2.925 · Δρ · a^{8/3}   ⎝  x  ⎠

                 9 μ γ_w
    g*_int  =  ───────────                                              (3.5)
                 4 Δρ x
```

**Computed values.**

`Ga_dep` for the WPA nominal line (R1: `γ_w` = 65.2 s⁻¹, `x` = 0.5 m):

| Class | `k_lev` | `k_int` | `k_w` | **Ga Earth** | **Ga Mars** | **Ga Moon** |
|---|---|---|---|---|---|---|
| P1 cell | 1.60 × 10⁻⁸ | 1.93 × 10⁻¹¹ | 1.60 × 10⁻⁸ | **4.20** | **1.59** | **0.694** |
| P2 7 µm | 4.64 × 10⁻⁹ | 7.99 × 10⁻¹⁰ | 4.64 × 10⁻⁹ | 323 | 122 | 53.4 |
| P3 100 µm | 7.88 × 10⁻¹⁰ | 1.63 × 10⁻⁷ | 1.63 × 10⁻⁷ | 1878 | 710 | 310 |
| P4 183 µm | 5.27 × 10⁻¹⁰ | 5.46 × 10⁻⁷ | 5.46 × 10⁻⁷ | 1878 | 710 | 310 |
| P5 500 µm | 2.69 × 10⁻¹⁰ | 4.08 × 10⁻⁶ | 4.08 × 10⁻⁶ | 1878 | 710 | 310 |

(P3–P5 identical, as (3.3) requires.)

**The headline number:** for a **single planktonic cell in the nominal WPA process line**,

```
    Ga_dep = 4.20 (Earth) ,  1.59 (Mars) ,  0.694 (Moon)
    g*_dif = 2.334 m s⁻²  =  0.238 g_E
```

**The crossover from gravity-dominated to flow-dominated wall delivery falls *inside* the
lunar-to-Mars gravity window.** This is precisely the non-trivial outcome the problem statement was
scoped to find, and it is not the trivially-wide-margin failure mode.

Sensitivity to the one ASSUMED geometric parameter, at fixed sourced flow rate:

| `D` (mm) | `U` (m s⁻¹) | `Re` | `γ_w` (s⁻¹) | `Ga_dif` cell, Earth | `g*` (`g_E`) |
|---|---|---|---|---|---|
| 3.18 (1/8″) | 0.2064 | 735 | 519 | 2.11 | 0.475 |
| 4.57 | 0.0999 | 512 | 175 | 3.03 | 0.331 |
| **6.35 (1/4″)** | **0.0518** | **368** | **65.2** | **4.20** | **0.238** |
| 9.53 (3/8″) | 0.0230 | 245 | 19.3 | 6.31 | 0.159 |
| 12.7 (1/2″) | 0.0129 | 184 | 8.15 | 8.41 | 0.119 |

`g*` stays in the range **0.12–0.48 `g_E`** across the entire plausible tube-size range — i.e.
**bracketing lunar gravity (0.165 `g_E`) and Mars gravity (0.378 `g_E`) for every diameter tested.**
The qualitative conclusion is robust to the assumption; the precise threshold is not.

For all other regimes and all aggregate classes, `Ga_dep ≫ 1` at every gravity level:

| Regime | `g*_int` (from 3.5) |
|---|---|
| R1 WPA line | 5.32 × 10⁻⁴ `g_E` |
| R2 restart flush | 1.24 × 10⁻² `g_E` |
| R3a UPA feed | 3.38 × 10⁻⁵ `g_E` |
| R3b MABR | 3.42 × 10⁻⁶ `g_E` |
| R4 dead leg | 1.03 × 10⁻⁶ `g_E` |

**Interpretation: for any aggregate larger than ~7 µm, gravity dominates wall delivery not only at
lunar and Mars gravity but down into the milli-`g` and micro-`g` range.** Gravity-driven deposition
of flocs is essentially never negligible in these systems.

### 3.3 Criterion 2 — `Λ_g`: is there enough length for gravity to act?

`Ga_dep ≫ 1` says gravity *wins* the delivery competition, but not that delivery actually *happens*
within the segment. A particle starting at the channel centreline must fall a distance `R` before
touching the wall, taking `t_fall = R/v_s`; it is in the segment for `t_res = L/U`. Requiring
`t_fall ≤ t_res`:

```
                t_res        v_s L
    Λ_g   =   ─────────  =  ───────                                     (3.6)
                t_fall        U R
```

For a rectangular channel of width `W` this is `Λ_g = v_s (L W)/Q` — **exactly the classical
surface-overflow-rate (Hazen) number** used to size gravity clarifiers. Re-purposing that criterion
is legitimate and citable rather than novel-for-novelty's-sake, and it gives the paper an
established engineering anchor.

**Computed:**

| Class | R1 WPA line | R2 flush | R3a UPA | R3b MABR | R4 dead leg |
|---|---|---|---|---|---|
| | E / M / L | E | E / M / L | E / M / L | E / M / L |
| P1 cell | 2.1e−4 / 7.8e−5 / 3.4e−5 | 2.1e−5 | 3.2e−3 / 1.2e−3 / 5.3e−4 | 4.0e−3 / 1.5e−3 / 6.6e−4 | 0.106 / 0.040 / 0.018 |
| P2 7 µm | 4.6e−3 / 1.7e−3 / 7.5e−4 | 4.6e−4 | 7.2e−2 / 2.7e−2 / 1.2e−2 | 8.9e−2 / 3.4e−2 / 1.5e−2 | 2.36 / 0.89 / 0.39 |
| **P3 100 µm** | **0.932 / 0.352 / 0.154** | 9.3e−2 | 14.7 / 5.5 / 2.4 | 18.1 / 6.9 / 3.0 | 482 / 182 / 80 |
| **P4 183 µm** | **3.12 / 1.18 / 0.515** | 0.312 | 49.1 / 18.6 / 8.1 | 60.7 / 23.0 / 10.0 | 1615 / 611 / 267 |
| P5 500 µm | 23.3 / 8.8 / 3.8 | 2.33 | 367 / 139 / 61 | 453 / 172 / 75 | 12050 / 4559 / 1991 |

**This is where partial gravity bites.** In the nominal WPA line over a 0.5 m segment:
- the **100 µm floc** has `Λ_g` = 0.93 at Earth, 0.35 at Mars, 0.15 at Moon — it settles out at
  Earth gravity but is *carried through* at Mars and lunar gravity;
- the **183 µm floc** has `Λ_g` = 3.12 / 1.18 / 0.52 — it settles out at Earth and Mars, and the
  transition to carry-through occurs between Mars and lunar gravity.

So the criterion predicts a **size-selective, gravity-dependent partitioning**: reducing gravity from
Earth to lunar shifts the smallest floc that deposits within a given line length upward by roughly
`(g_E/g_L)^{1/2} = 2.5×` in diameter (since `Λ_g ∝ g a²`). A lunar-surface WPA would transport
flocs of 100–180 µm to downstream components that would have dropped out in a 1-g ground test rig.
**That is a concrete, falsifiable, design-relevant prediction, and it is exactly the kind of finding
that would be invisible in a 1-g qualification campaign.**

Conversely `Λ_g ≪ 1` for single cells everywhere except the dead leg — single cells do not settle
out of a pumped line regardless of gravity, even though `Ga_dep` says gravity dominates *their*
wall delivery too. **The two criteria are genuinely independent and both are needed.**

### 3.4 Criterion 3 — `Σ_g`: gravity in the near-wall retention balance

Once a particle contacts the wall, does gravity influence whether it stays? Compare the submerged
weight with the hydrodynamic drag on a sphere resting against a plane wall in shear flow. O'Neill's
result for a sphere touching a wall gives `F_D = 1.7009 × 6πμ a² γ_w`. Hence

```
                W'          (4/3)π a³ Δρ g            2 Δρ g a
    Σ_g   =   ──────  =  ────────────────────────  = ───────────        (3.7)
                F_D       1.7009 · 6πμ a² γ_w        15.31 μ γ_w
```

Again linear in `g`, and linear in `a`.

| Class | R1 WPA line `Σ_g` (E / Moon) | R3b MABR (E / Moon) | R4 dead leg (E / Moon) |
|---|---|---|---|
| P1 cell | 1.1e−3 / 1.8e−4 | 0.290 / 0.048 | 0.578 / 0.096 |
| P2 7 µm | 3.9e−3 / 6.4e−4 | 1.00 / 0.166 | 2.00 / 0.330 |
| P3 100 µm | 5.5e−2 / 9.1e−3 | 14.3 / 2.36 | 28.6 / 4.72 |
| P4 183 µm | 0.101 / 0.017 | 26.2 / 4.33 | 52.3 / 8.64 |
| P5 500 µm | 0.276 / 0.046 | 71.6 / 11.8 | 143 / 23.6 |

**Interpretation.** In pumped lines `Σ_g ≪ 1` for everything — **hydrodynamic drag dominates
retention and gravity is irrelevant to whether a particle stays attached.** In the MABR shell and in
dead legs `Σ_g ≳ 1` for aggregates, so gravity does hold flocs against the wall there.

**Important honesty check:** for single cells, both forces are minute (`W' ≈ 6 × 10⁻¹⁶ N`,
`F_D ≈ 5.5 × 10⁻¹³ N` in R1) and both are dwarfed by specific adhesion forces, which for bacteria
are typically 0.1–10 nN. `Σ_g` therefore correctly reports "gravity does not control retention," but
it should **not** be read as a complete adhesion model. §6 records this.

### 3.5 The stagnant limit (R4, `U → 0`) — where the criterion does its real work

As `U → 0`, `γ_w → 0`, so `k_w → 0` and `Ga_dep → ∞`, `Λ_g → ∞`, `Σ_g → ∞`. The criteria as written
degenerate. The correct competitor for gravity in a genuinely stagnant segment is **Brownian
diffusion** (and, if `Ra > Ra_c`, buoyant convection from §2.2). Define the **gravitational Péclet
number** over the channel dimension `H`:

```
               v_s H         2 Δρ g a² H         4π Δρ g a⁴
    Pe_g  =   ────────  =  ───────────────  =  ─────────────  (with H→ using D_B) (3.8)
                D_B          9 μ D_B              3 k_B T
```

(the last form uses `D_B = k_BT/6πμa` and `H = ` the settling distance; the `a⁴` dependence makes
this the steepest size-scaling in the whole derivation.)

| Class | `Pe_g` Earth (6.35 mm) | `Pe_g` Moon | `t_settle` Earth | `t_settle` Mars | `t_settle` Moon |
|---|---|---|---|---|---|
| P1 cell | 9.50 × 10² | 1.57 × 10² | 26.2 h | 69.2 h | 158 h (6.6 d) |
| P2 7 µm | 1.36 × 10⁵ | 2.24 × 10⁴ | 1.18 h | 3.11 h | 7.12 h |
| P3 100 µm | 3.96 × 10⁸ | 6.54 × 10⁷ | 21 s | 55 s | 127 s |

Over a 0.30 m tank dimension: single cell settles in **51.5 d (Earth) / 136 d (Mars) / 312 d (Moon)**;
a 7 µm aggregate in 2.3 / 6.1 / 14.0 d.

**Conclusion for the dormancy regime, which is the centre of gravity of the whole problem:**

> Against a dormancy period of up to one year, **every** particle class fully settles out at **every**
> gravity level considered, in a 6.35 mm line within hours-to-days and in a 0.30 m tank within days-
> to-months. `Pe_g ≥ 157` even for a single cell at lunar gravity — gravity beats Brownian diffusion
> by more than two orders of magnitude in the worst case. **In stagnant ECLSS water, gravity-driven
> transport is first-order at Earth, Mars *and* lunar gravity without exception.**

But this must be immediately qualified by the convection result of §2.2(b): in a *convecting* volume
(tank, or a line with `ΔT > ΔT_c`) the suspension number `Ω` (2.7) says single cells are held in
suspension and never reach the floor. **The two gravity mechanisms give opposite answers, and which
one wins is set by `Ra` vs `Ra_c` — which is itself gravity-dependent.** The practically important
case is the narrow line: at lunar gravity a 6.35 mm line with a 1 K gradient has `Ra = 818 < Ra_c`,
so convection is *off* and settling is unopposed; the same line at Earth gravity has `Ra = 4953`,
convection is *on*, and cells are partly resuspended. **Lowering gravity can therefore *increase*
net cell deposition in narrow stagnant lines, by switching off the convection that would otherwise
keep cells suspended.** This is a counter-intuitive, testable, and specifically partial-gravity
prediction; it is the strongest single result in this derivation.

### 3.6 Cross-check against the Konishi/Mudawar/Hasan criteria structure

Konishi, Mudawar & Hasan, *Criteria for negating the influence of gravity on flow boiling critical
heat flux with two-phase inlet conditions*, **Int. J. Heat Mass Transfer 65:203–218 (2013)**
`[verified-existence]`, negate gravity's influence by requiring **three criteria simultaneously**:
(i) overcoming gravity **perpendicular** to the heated wall, (ii) overcoming gravity **parallel** to
it, and (iii) **sufficient heated length** to ensure liquid contact `[snippet-level]`. Their
companion literature (Zhang/Mudawar/Hasan; Merte et al.) frames the bounds via a **two-phase
Richardson number, a two-phase Weber number and a Bond number** `[snippet-level]`, with the physical
statement that *"high inertia negates the influence of gravity"* and that gravity dominates
interfacial behaviour at low mass velocities `[snippet-level]`.

The structural mapping is close but **not** copied — each of my criteria is derived from this
system's own physics in §§3.2–3.4, and the dimensionless groups are entirely different (theirs are
inertia/surface-tension groups for a deformable interface; mine are viscous-drag/Brownian/geometric
groups for a rigid colloid):

| Konishi et al. criterion | This work | Shared physical role |
|---|---|---|
| gravity ⊥ heated wall vs inertia | **`Ga_dep`** (3.1) | wall-normal body-force transport vs flow-driven wall transport |
| gravity ∥ heated wall vs inertia | **`Σ_g`** (3.7) | wall-parallel force balance governing retention/removal |
| sufficient heated length for liquid contact | **`Λ_g`** (3.6) | sufficient streamwise length for the wall-normal process to complete |
| — | **`Ω`** (2.7), **`Ra/Ra_c`** (2.4–2.5) | *additional*: buoyancy has no CHF analogue in their inlet-quality framing |

Two honest differences worth stating in the paper:
1. **Their criteria are "negating" criteria** — satisfy all three and gravity's influence vanishes.
   Mine are the same in form, but the *answer* is different: in this system the criteria are
   **not** simultaneously satisfiable in stagnant regimes at any gravity level of interest.
2. **I have a fourth axis they do not** (buoyant convection with a sharp `Ra_c` threshold), because
   a single-phase colloidal suspension has a stability threshold that a boiling two-phase flow,
   already violently mixed, does not.

### 3.7 Summary of the criterion set

```
    ┌──────────────────────────────────────────────────────────────────────┐
    │  Gravity-driven transport is NEGLIGIBLE for biofilm accumulation     │
    │  in a channel segment  ⟺  ALL of the following hold:                 │
    │                                                                       │
    │      Ga_dep ≪ 1     and     Λ_g ≪ 1     and     Σ_g ≪ 1              │
    │                                                                       │
    │  Gravity-driven transport is FIRST-ORDER if ANY exceeds ~1.          │
    │  0.1 ≲ (any) ≲ 10  is the AMBIGUOUS band: gravity is a correction    │
    │  of the same order as the modelling error and must be carried, but   │
    │  no regime conclusion can be drawn.                                  │
    └──────────────────────────────────────────────────────────────────────┘
```

Physical meaning of each limit:

- **`Ga_dep ≫ 1`** — cells/flocs arrive at the wall predominantly *because they fall*, not because
  the flow brings them. Biofilm accrual is anisotropic (bottom-loaded) and scales with `g`.
- **`Ga_dep ≪ 1`** — arrival is flow-controlled; biofilm accrual is circumferentially uniform and
  `g`-independent. Ground testing transfers directly.
- **`Λ_g ≫ 1`** — everything that can settle does settle within the segment; the segment acts as a
  clarifier and accumulates a bottom deposit.
- **`Λ_g ≪ 1`** — particles are flushed through before they can fall; deposition is a small
  perturbation on through-transport.
- **`Σ_g ≫ 1`** — gravity pins particles to the lower wall; shear cannot re-entrain them.
- **`Σ_g ≪ 1`** — shear controls retention; gravity is irrelevant to what stays attached.
- **Ambiguous band (0.1–10)** — this is where the WPA nominal line sits for single cells
  (`Ga_dep` = 4.2 / 1.6 / 0.69) and where 100–183 µm flocs sit for `Λ_g`. The honest statement is
  *not* "gravity matters" or "gravity doesn't"; it is **"the gravity term is the same size as the
  other terms and the model must retain it, and a 1-g qualification test is not a valid surrogate."**

---

## 4. Reconciliation with the growth-rate literature (the flagged invalidating assumption)

`novelty_adjudication.md` §1 identified the hidden invalidating assumption for the *original*
Candidate A: the depletion-zone mechanism is defined for quiescent, diffusion-limited suspension;
gravity's effect on growth was found to be **non-monotonic** (two opposing mechanisms, A-1);
**null in bulk** at Mars gravity (BioRock, A-4); and **strain-dependent** (A-5). Any criterion in
this program must show it is not quietly re-importing that assumption.

### 4.1 Transport and growth are different questions

They are different in **what is being predicted**, in **what would falsify them**, and in **what
data validates them**:

| | Growth-rate question (Candidate A, rejected) | Transport question (this work) |
|---|---|---|
| Predicted quantity | specific growth rate `μ(g)`, final cell concentration | wall-normal particle flux `J(g)`, spatial distribution of accumulated biomass |
| Physical content | how gravity modulates a cell's *access to substrate* and hence its metabolism | how gravity modulates *where cells and flocs end up* |
| Governing physics | reaction kinetics coupled to a local mass-transfer boundary layer | Stokes drag, Brownian motion, wall shear, channel geometry |
| Falsified by | a flight experiment showing equal final cell counts across `g` | a flight experiment showing equal *spatial distribution* of deposit across `g` |
| Status of BioRock null | **fatal** — it directly measures the predicted quantity | **not applicable** — it measured final bulk concentration, not deposit distribution |

**BioRock (Santomartino et al., *Front. Microbiol.* 11 (2020) `[verified-existence]`) measured final
bacterial cell concentrations and found no effect of microgravity or simulated Mars gravity**
`[snippet-level]`. That is a statement about the *integrated production of biomass*. It is
**logically compatible** with a large gravity effect on *where that biomass sits*: the same total
number of cells can be uniformly suspended, or entirely deposited on one wall, without changing the
bulk count. Indeed the corroborating snippet notes the null held *"despite different predicted
sedimentation rates"* — i.e. the authors themselves observed that sedimentation differed while the
bulk outcome did not. **That is precisely the decoupling this work relies on, stated by the very
experiment that killed Candidate A.**

Likewise Latham, Skountzos & Lawson (bioRxiv 2026.05.15.725518 `[verified-existence]`) report that
*lack of gravity-driven flow decreases growth in microgravity while absence of sedimentation
increases growth* `[snippet-level]`. Both of those are **transport** mechanisms feeding a growth
model. This work computes the transport terms directly and does not need their net effect on growth
to be monotonic — the non-monotonicity of the *growth* response is a downstream consequence of two
transport terms of opposite sign, and my §2.2/§3.5 result (settling deposits, convection resuspends,
and the `Ra_c` threshold decides which wins) is the transport-side statement of the same structure.

### 4.2 Where growth-rate effects enter — as a decoupled secondary term

In the model of §5, gravity enters **only** the transport coefficients:

```
    v_s ∝ g            (deposition flux)
    Ra ∝ g             (onset and strength of vertical mixing)
    cos θ              (orientation of g relative to the wall)
```

and the kinetic parameters `μ_max`, `K_s`, `Y`, `b` are held **`g`-independent**. This is a
deliberate modelling decision, and it is the defensible one, because:

1. The best available direct evidence (BioRock at Mars gravity) reports no bulk kinetic effect.
2. The effect that does exist is strain-dependent (Abrevaya et al., *Life* 12(9):1399 (2022)
   `[verified-existence]`, reporting increased growth under simulated micro- and lunar gravity *for
   some strains* `[snippet-level]`), so no single scaling law is defensible.
3. Making the kinetics `g`-dependent would re-import exactly the assumption the adjudicator
   identified as fatal.

If a future user wants to include a growth-rate effect, the correct architecture is a **multiplicative,
separately-parameterised, separately-defensible factor**:

```
    μ_eff(S, g)  =  μ_max · φ(g) · S/(K_s + S)        with  φ(g) ≡ 1  by default   (4.1)
```

with `φ(g)` supplied from an external source and its uncertainty propagated independently.
**`φ(g) ≡ 1` is the baseline and must remain the published baseline.** The criterion's conclusions
must be reported for `φ ≡ 1`, with any `φ ≠ 1` sensitivity shown separately and labelled as
speculative. This keeps the transport claim clean: if a reviewer disputes `φ`, the criterion is
untouched.

### 4.3 The quiescent-suspension scope limit is inherited, not escaped

One thing this work must **not** claim: it does not escape the "non-motile cells" restriction.
§2.5 showed that a motile single cell swims ~500× faster than it settles. The Korber et al. (1990)
result — wild-type deposits gravity-independently, flagellar mutants 10–40× preferentially downward
`[snippet-level]` — is the experimental statement of this. So:

- for **motile planktonic cells**, `Ga_dep` overstates gravity's role and the correct competitor is
  `v_swim`, not `k_w`;
- for **non-motile cells, motility-repressed cells (a documented biofilm phenotype), and all
  aggregates ≳ 5 µm**, the criterion applies as derived.

The criterion should be published with `v_swim` shown alongside, and a fourth optional criterion
`Ga_mot = v_s/v_swim` reported for the planktonic single-cell class. This is a limitation, but it is
a *stated, quantified* limitation, and it is narrower than Candidate A's, which needed quiescence
for the whole mechanism.

---

## 5. The 1-D advection–diffusion–reaction model to implement

### 5.1 State variables

On a 1-D domain `z ∈ [0, L]` (channel axis), for each particle class `i ∈ {P1…P5}`:

| Variable | Meaning | Units |
|---|---|---|
| `C_i(z,t)` | suspended biomass concentration in class `i` | kg-dry m⁻³ |
| `S(z,t)` | growth-limiting substrate (as TOC/DOC carbon) | kg-C m⁻³ |
| `X(z,t)` | **areal** biofilm dry-biomass density on the wall | kg-dry m⁻² |

Optional derived output: biofilm thickness `L_f = X / ρ_X` with `ρ_X` the biofilm dry-density.

### 5.2 Governing equations

Let `σ = P_wet/A_cs` be the wetted perimeter per unit cross-sectional area (`σ = 4/D` for a circular
tube). Then:

**Suspended biomass (one equation per class `i`):**

```
  ∂C_i        ∂C_i         ∂²C_i
  ──── = −U ·──── + D_ax,i·─────  +  [μ(S) − b]·C_i  −  σ·(j_dep,i − j_det,i)    (5.1)
   ∂t         ∂z            ∂z²
```

**Substrate:**

```
  ∂S         ∂S          ∂²S       1                    σ
  ──  = −U ·──  + D_S ·─────  −  ───·μ(S)·Σ_i C_i  −  ───·μ(S_w)·X            (5.2)
  ∂t         ∂z          ∂z²       Y                    Y
```

**Biofilm (ODE at each `z` — no wall-parallel biofilm transport):**

```
  ∂X
  ──  =  [μ(S_w) − b_f]·X  +  Σ_i j_dep,i  −  j_det                            (5.3)
  ∂t
```

### 5.3 Where gravity enters — the three entry points

**(A) Deposition flux — the primary `g` term.**

```
    j_dep,i  =  α_i · k_tot,i · C_i                                            (5.4)

    k_tot,i  =  f_θ · v_s,i(g)  +  k_w,i                                       (5.5)
```

- `v_s,i(g)` from (2.1), or (2.2) when `Re_p > 0.34`. **This is where `g` multiplies in.**
- `k_w,i = max(k_lev, k_int)` from (2.10)/(2.12), with `x` taken as the local streamwise coordinate
  `z` (regularise as `max(z, z_min)` with `z_min = D`, since the Lévêque solution is singular at
  `z = 0`).
- **`f_θ` is the orientation factor and must be derived, not guessed.** For a *horizontal circular
  tube*: particles settle vertically at `v_s`; per unit axial length the swept volumetric rate is
  `v_s × D` (the projected width), so the mass arriving per unit axial length is `v_s D C`.
  Dividing by the perimeter `πD` gives the perimeter-averaged gravitational deposition velocity

  ```
      f_θ = 1/π ≈ 0.3183          (horizontal tube, perimeter-averaged)         (5.6)
      f_θ = 0                     (vertical tube — g is parallel to the wall)
      f_θ = cos θ                 (flat wall at angle θ to g)
  ```

  The vertical-tube case (`f_θ = 0`) is the direct analogue of Konishi's "gravity parallel to the
  heated wall" criterion and gives the model a genuine **orientation** axis, which is a real ECLSS
  design variable and is exactly what Marra/Rizzo/Caserta (*npj Biofilms Microbiomes* 11:122 (2025)
  `[verified-existence]`) and the *Water* 17(15):2277 (2025) inclination study
  `[verified-existence]` measure experimentally — giving the model a validation target.

- `α_i` = attachment (collision/sticking) efficiency, dimensionless, `0 < α ≤ 1`.

  > **ASSUMED (not sourced): `α = 0.3` nominal, range 0.01–1.** Colloid-filtration theory defines
  > `α` as "the probability of attachment given a collision event" `[snippet-level]`, and the
  > flow-chamber literature reports deposition efficiencies *relative to the Smoluchowski–Levich
  > prediction* of "four-to-five fold higher than unity", falling **below unity (0.78 → 0.36 with
  > increasing flow rate) when computed relative to sedimentation instead** `[snippet-level]`
  > (Li, Busscher, van der Mei et al., *Analysis of the contribution of sedimentation to bacterial
  > mass transport in a parallel plate flow chamber*, **Colloids Surf. B** (2011)
  > `[verified-existence]`). **`α = 0.3` is chosen as the midpoint of that sourced 0.36–0.78 band,
  > rounded down**, and is therefore a defensible placeholder rather than an invention. It must be
  > swept.

**(B) Vertical mixing in stagnant segments — the buoyancy `g` term.**
When `U → 0`, replace the wall-normal transport in (5.5) with a settling-vs-mixing balance. Define

```
    D_v  =  D_B  +  D_conv ,      D_conv = 0                if Ra < Ra_c
                                  D_conv ≈ u_conv · H / 10   if Ra ≥ Ra_c        (5.7)
```

with `Ra` from (2.4), `Ra_c = 1708`, `u_conv` from (2.6a)/(2.6b). The vertical steady concentration
profile is then the classical Rouse/sedimentation–diffusion exponential with scale height
`h_s = D_v / v_s`, and the wall-normal deposition velocity in (5.5) becomes

```
    k_tot  =  v_s / [1 − exp(−H/h_s)]  →  v_s  when  h_s ≪ H (settling dominant)  (5.8)
```

> The `/10` in `D_conv` is **ASSUMED (not sourced)**: it is the standard order-unity mixing-length
> reduction converting a convective velocity scale into an eddy diffusivity
> (`D_conv ~ u' ℓ` with `ℓ ~ H/10`). It affects only the stagnant-convecting branch and must be
> swept over 1/3–1/30.

**(C) Orientation.** `f_θ` in (5.6). Gravity's *direction*, not just magnitude, is a model input.

**Gravity does NOT enter** `μ_max`, `K_s`, `Y`, `b`, `b_f`, `k_det` — see §4.2.

### 5.4 Detachment

```
    j_det  =  k_det · X ,       k_det = k_det,0 · (τ_w / τ_ref)^n                (5.9)
```

Rittmann, *The effect of shear stress on biofilm loss rate*, **Biotechnol. Bioeng. 24:501–506
(1982)** `[verified-existence]` is the founding correlation. Note the snippets disagree with each
other on the functional form — one summary reports *"an exponential correlation between the
detachment rate of biofilms and the water shear force"*, another reports *"a linear relationship
between biofilm loss rate and rotational speed"* `[snippet-level]`. **This disagreement cannot be
resolved without the full text and must be reported as an open item.**

> **ASSUMED (not sourced): `n = 1` (linear in `τ_w`), `τ_ref = 1 Pa`, `k_det,0 = 1 × 10⁻⁵ s⁻¹`.**
> `n = 1` is chosen as the lower/more conservative of the two reported forms. `k_det,0` is set so
> that at `τ_w ≈ 0.058 Pa` (R1) `k_det = 5.8 × 10⁻⁷ s⁻¹`, i.e. a biofilm detachment timescale of
> ~20 days — the same order as
> ISS biocide-flush intervals — a defensible engineering placeholder, not a measurement. **Sweep
> `n ∈ [1,3]` and `k_det,0` over two decades.**

Gravity does **not** appear in (5.9): §3.4 showed `Σ_g ≪ 1` in every pumped regime, so
gravity-assisted re-entrainment is negligible where shear exists, and where shear does not exist
(`R4`) there is no detachment to modulate.

### 5.5 Growth kinetics

```
    μ(S)  =  μ_max · S / (K_s + S)                     (Monod)                  (5.10)
```

Monod (not Blackman) is the correct choice and is also the form Latham et al. adopted when improving
the CAMDLES growth functional `[snippet-level]` — using the same form makes cross-comparison
possible.

External mass-transfer resistance at the biofilm surface (optional, recommended on):

```
    J_S = k_S (S − S_w) = (1/Y) μ(S_w) X ,   k_S = 0.538 D_S^{2/3}(γ_w/z)^{1/3}  (5.11)
```

solved for `S_w` at each node by a scalar Newton iteration. Setting `S_w = S` (no external
limitation) is the fast option and is accurate for thin biofilms at high `S`.

**Kinetic parameters — all flagged.**

> **ASSUMED (not sourced): `μ_max = 0.1 h⁻¹` (range 0.02–0.3).** No `μ_max` for the ISS isolates
> under oligotrophic conditions was found. *B. cepacia* "can survive under nutrient-limited
> conditions and metabolize organic matter present in oligotrophic aquatic environments"
> `[snippet-level]` but no rate was reported. 0.1 h⁻¹ (≈7 h doubling) is a standard aerobic
> heterotroph value and defensible as an order-of-magnitude placeholder.

> **ASSUMED (not sourced): `K_s = 1 g-C m⁻³` (= 1 mg/L; range 0.1–10).** The sourced anchor is
> *"typical values for domestic wastewater bacteria `K_s` range from 0.01 to 0.18 kg m⁻³"*
> (10–180 mg/L) `[snippet-level]`, combined with the sourced finding that *"`K_s` values were lower
> for the biofilm oligotrophs than for typical copiotrophs"* `[snippet-level]` — Rittmann, Crawford,
> Tuck & Namkung, *In situ determination of kinetic parameters for biofilms: isolation and
> characterization of oligotrophic biofilms*, **Biotechnol. Bioeng. 28:1753–1760 (1986)**
> `[verified-existence]`. 1 mg/L is one decade below the low end of the copiotroph range, consistent
> with that qualitative finding. **The numeric value is mine, not Rittmann's — I could not read the
> table.**

> **ASSUMED (not sourced): `Y = 0.4 kg-dry per kg-C`, `b = 0.002 h⁻¹`, `b_f = 0.001 h⁻¹`,
> `ρ_X = 30 kg-dry m⁻³`.** Standard aerobic-heterotroph values. `ρ_X` is consistent with the sourced
> biofilm wet densities of 1011–1029 kg m⁻³ `[snippet-level]` at ~97 % water content.

**Substrate levels are, by contrast, well sourced:** WPA wastewater TOC > 2000 g-C m⁻³, potable
spec ≤ 3 g-C m⁻³ `[snippet-level]`. Since `S ≫ K_s` on the wastewater side, growth there is
effectively zero-order at `μ_max` — a useful simplification and a real result: **the WPA wastewater
tank is not substrate-limited, so biofilm accumulation there is transport- and detachment-limited,
which is exactly the regime this criterion addresses.**

### 5.6 Axial dispersion — an important numerical finding

The natural choice is Taylor–Aris dispersion, `D_ax = D_B + U²D²/(192 D_B)`. **Do not use it here.**
For P1 in R1 that formula gives `D_ax ≈ 1250 m² s⁻¹`, which is nonsense: Taylor–Aris requires
`t ≫ D²/D_B = 4.5 × 10⁷ s`, whereas the residence time is 9.7 s. The dispersion is nowhere near
established.

**Use `D_ax,i = D_B,i`** (and `D_S ≈ 5 × 10⁻¹⁰ m² s⁻¹` for dissolved organics). Then the axial
Péclet number is `Pe_ax = UL/D_B ≈ 5.7 × 10¹⁰` for cells and `5.2 × 10⁷` for substrate — **the
system is purely advective in the flowing regimes**, and the diffusion term exists only to keep the
stagnant limit (`U = 0`) well posed. Implement it, but expect it to be numerically irrelevant when
`U > 0`; use an upwind advection scheme so this does not create artificial diffusion.

### 5.7 Boundary and initial conditions

**Inlet (`z = 0`) — Danckwerts:**

```
    U C_in,i  =  U C_i(0,t) − D_ax,i ∂C_i/∂z |₀
    U S_in    =  U S(0,t)   − D_S    ∂S/∂z   |₀                                (5.12)
```

**Outlet (`z = L`) — zero-gradient:** `∂C_i/∂z|_L = 0`, `∂S/∂z|_L = 0`.

**Recycle-loop closure** (for UPA/MABR recirculation, optional):
`C_in,i(t) = C_i(L,t)`, `S_in(t) = S(L,t) + S_makeup(t)`.

**Stagnant (`U = 0`):** set both ends to zero-flux (`∂/∂z = 0`); the segment becomes a set of
independent 0-D reactors with a gravitational wall flux, which is the correct dormancy model.

**Initial conditions:**
- `C_i(z,0) = C_0,i` — anchor the *total* to the sourced ISS potable value of "a few CFU/mL"
  (≈ 5 × 10⁶ cells m⁻³) or the 50 CFU/mL spec limit `[snippet-level]`; convert to mass with the
  cell volume from §1.4 and a dry-mass fraction.
  > **ASSUMED (not sourced): cell dry mass fraction 0.3 of wet mass.** Standard microbiology value.
  > The partition of `C_0` **across** classes P1–P5 is unconstrained by any source and is a primary
  > uncertainty (§7).
- `S(z,0) = S_0` — 2000 g-C m⁻³ (wastewater side) or 3 g-C m⁻³ (potable side), both sourced.
- `X(z,0) = X_0` — small non-zero seed.
  > **ASSUMED (not sourced): `X_0 = 10⁻⁶ kg m⁻²`** (≈ a sparse monolayer). Any small value works;
  > the system is not sensitive to it once growth is established.

### 5.8 Numerical method (method of lines)

1. Discretise `z ∈ [0,L]` into `N` cells (start `N = 200`; verify grid convergence).
2. **Advection:** first-order upwind (or MUSCL with a minmod limiter for sharper fronts).
   Note `U ≥ 0` always, so upwinding is unambiguous.
3. **Diffusion:** standard second-order central differences.
4. **Reaction + wall exchange:** evaluated pointwise; these are the stiff terms.
5. Assemble `dy/dt = F(t, y)` with `y = [C_1…C_5, S, X]` per node → `7N` ODEs for 5 classes.
6. Integrate with `scipy.integrate.solve_ivp`, **method `'BDF'` or `'LSODA'`** — the problem is
   stiff (deposition timescales of seconds against growth timescales of hours against dormancy
   timescales of a year, i.e. ~8 decades of timescale separation). Explicit integrators will fail.
7. Supply the Jacobian sparsity pattern (block-tridiagonal) via `jac_sparsity` — this is worth a
   large speed-up at `N = 200` and 6 species.
8. **Non-negativity:** clip `C_i, S, X ≥ 0` after each step, or integrate `log` variables. Monod
   with negative `S` will produce garbage.
9. **Dormancy runs:** integrate to `t = 3.156 × 10⁷ s` (1 year) with `U = 0`; use `max_step` capped
   so the integrator does not step over the settling transient (which completes in hours).

### 5.9 Model outputs

- `X(z, t; g)` — accumulated areal biofilm density, the primary quantity.
- Total accumulated biomass `∫₀^L σ X dz` vs `g` — the headline gravity-dependence curve.
- `Ga_dep`, `Λ_g`, `Σ_g`, `Ω`, `Ra/Ra_c` evaluated per regime and per class — the criterion map.
- The **regime boundary surface** in `(Q, D, d_particle, g)` space where each criterion = 1. This
  is the deliverable named in `problem_statement.md` §1 and it can be computed *analytically* from
  (3.4), (3.5), (3.6), (3.7) without running the PDE at all — the PDE serves to show the
  *consequence* of crossing the boundary, not to locate it.

---

## 6. Assumptions and their validity ranges

**Program integrity rule: "A model that only works under stated assumptions must state them."**

### 6.1 Fluid mechanics

| # | Assumption | Validity range | Status in this system |
|---|---|---|---|
| A1 | Newtonian, incompressible water | `T` 5–60 °C, dilute | ✅ holds |
| A2 | Fully developed laminar duct flow, `γ_w = 8U/D` | `Re < 2300`, `z > 0.05 Re D` | ✅ R1 (`Re`=368), R3, R4. ❌ R2 (`Re`=3681) → Blasius used. Entrance length for R1 is 0.117 m, i.e. **23 % of the 0.5 m segment is not fully developed** — a real error source, `γ_w` is *higher* there, so `Ga_dep` is *overestimated* near the inlet. |
| A3 | Steady flow | — | ⚠️ WPA cycles on/off; transients not modelled |
| A4 | Rigid, smooth walls; biofilm does not change the flow | `L_f ≪ D` | ✅ while `L_f < 0.1 D` = 635 µm. **Fails for mature biofilm**; §6.5 |
| A5 | Taylor–Aris dispersion **not** applicable | `t_res ≪ D²/D_B` | ✅ verified in §5.6; `D_ax = D_B` used instead |

### 6.2 Particle mechanics

| # | Assumption | Validity range | Status |
|---|---|---|---|
| A6 | Stokes drag, eq. (2.1) | `Re_p < 0.34` for 5 % accuracy | ✅ P1–P4 (`Re_p` ≤ 0.21). ❌ P5 (`Re_p` = 4.29, +33 % error) → Schiller–Naumann (2.2) required. `d_max` = 184 / 254 / 335 µm at Earth / Mars / Moon (2.3) |
| A7 | Spherical particles (equivalent-sphere radius) | aspect ratio ≲ 3 | ⚠️ *P. aeruginosa* rods are ~3.5:1. Prolate spheroid drag is 5–15 % higher than the equal-volume sphere for this aspect ratio → `v_s` **overestimated** by ~10 % for P1 |
| A8 | Dilute suspension — no hindered settling | `φ_vol < 10⁻³` | ✅ At 50 CFU/mL, `φ_vol ≈ 3 × 10⁻¹¹`. **Richardson–Zaki hindering is utterly negligible.** Would only matter in a settled bed |
| A9 | No particle–particle aggregation during transit | — | ⚠️ Not modelled. Flocculation would shift the size distribution upward over time and **increase** the gravity effect (`∝ a^{8/3}`), so neglecting it is conservative *against* the paper's own thesis — acceptable |
| A10 | Rigid, impermeable flocs | — | ❌ Flocs are porous; permeability raises the settling velocity above the impermeable-sphere Stokes value. Sourced note: *"the effective floc density is strongly dependent on the drag coefficient expression employed"* `[snippet-level]`. Another reason `v_s(floc)` is uncertain (§7) |
| A11 | `Δρ > 0` (particles sink) | — | ⚠️ One sourced biofilm density is **898 kg m⁻³** `[snippet-level]`, i.e. `Δρ < 0`. Gas-entrapping aggregates would **rise**. The criteria are sign-symmetric (`|Ga|`) but the *direction* of deposition flips |
| A12 | Non-motile cells | — | ❌ **Fails for motile planktonic cells** — `v_swim/v_s ≈ 500` (Earth) to 3000 (Moon), §2.5. Criterion applies to non-motile/motility-repressed cells and to all aggregates. Corroborated by Korber et al. (1990) `[verified-existence]` |
| A13 | Brownian diffusivity from Stokes–Einstein | rigid sphere, continuum | ✅ |

### 6.3 Transport modelling

| # | Assumption | Validity range | Status |
|---|---|---|---|
| A14 | Lévêque perfect-sink wall (`C_wall = 0`) | `α → 1`, high Pe | ⚠️ Overestimates `k_lev` when `α < 1`; since `k_lev` is the **denominator** of `Ga_dep`, this makes `Ga_dep` **under**estimated → conservative |
| A15 | Interception as `γ_w a²/2x` | `a ≪ D` | ✅ `a/D ≤ 0.04` for P5 |
| A16 | Gravity and flow deposition superpose linearly, (5.5) | both fluxes small perturbations | ⚠️ Genuinely approximate; the true problem is a coupled convection–diffusion–sedimentation boundary-value problem. The Groningen group's finding that **sedimentation, not convective diffusion, is the major mass-transport mechanism** in a parallel-plate chamber `[snippet-level]` supports the *conclusion* but not the *linear superposition* |
| A17 | `f_θ = 1/π` for a horizontal tube | perimeter-averaged | ✅ derived in (5.6). Note this **averages away** the top/bottom asymmetry that Korber et al. and Marra et al. actually measure — a 2-D (angular) model would resolve it |
| A18 | `Ra_c = 1708` | rigid–rigid infinite plane layer | ⚠️ A tube is not an infinite plane layer; the true `Ra_c` for a horizontal cylinder differs by an O(1) factor. **`ΔT_c` values in §2.2 are therefore order-of-magnitude, not precise** |
| A19 | Solutal (brine) buoyancy neglected | — | ⚠️ UPA only; it is *stabilising*, so neglecting it is conservative |
| A20 | Cell-scale metabolic convection neglected | — | ✅ justified in §2.2(a) by a sourced null |

### 6.4 Biology / kinetics

| # | Assumption | Status |
|---|---|---|
| A21 | Monod kinetics (5.10) | ✅ same form as Latham et al. `[snippet-level]` |
| A22 | Kinetic parameters `g`-independent (`φ(g) ≡ 1`) | ✅ **deliberate**, §4.2, defensible via BioRock null |
| A23 | Single lumped substrate (TOC) | ⚠️ Real WPA chemistry is multi-component (DMSD excursions are documented `[snippet-level]`) |
| A24 | Single lumped species | ⚠️ Real ISS consortia are ≥6 species with documented synergy (*Ralstonia insidiosa* + *Chryseobacterium gleum* `[snippet-level]`) |
| A25 | *E. coli* buoyant density used for ISS isolates | ❌ **Cross-species substitution.** No *Burkholderia*/*Ralstonia* value found |
| A26 | Activated-sludge floc density used for ECLSS flocs | ❌ **Cross-system substitution.** ECLSS flocs are oligotrophic and low-inert-content; sludge flocs are not |
| A27 | Detachment linear in `τ_w`, `n = 1` | ❌ **Unresolved** — sources disagree (linear vs exponential) `[snippet-level]` |

### 6.5 Explicitly **not** modelled

- **Biofilm-induced flow blockage.** `D` is constant; `L_f` does not feed back on `U`, `γ_w`, `Re`.
  Valid while `L_f < 0.1 D` (635 µm). Beyond that, `γ_w` rises as `L_f` grows, which *reduces*
  `Ga_dep` — a stabilising feedback the model will miss.
- **Biocide dosing / disinfection kinetics.** No iodine or UV term. Real ISS operations flush with
  biocidal water, so absolute `X(t)` predictions over a year are **not** operationally realistic;
  the *ratio* `X(g₁)/X(g₂)` is the defensible output.
- **EPS production, biofilm mechanics, sloughing events.** Detachment is a smooth first-order sink;
  real sloughing is stochastic and episodic.
- **Temperature dependence of kinetics** (no Arrhenius term).
- **Two-dimensional (angular) structure.** `f_θ = 1/π` averages top vs bottom; the asymmetry is real
  and measurable and would be the natural next model.
- **Non-isothermal operation.** `ΔT` is an input to (2.4), not solved for.

### 6.6 Temperature range

All values are quoted at **25 °C** (`ρ_f` = 997.0 kg m⁻³, `μ` = 8.90 × 10⁻⁴ Pa s). ECLSS water is
plausibly 15–45 °C. Over that range `μ` varies from 1.14 × 10⁻³ to 6.0 × 10⁻⁴ Pa s (≈ ±30 %), so
`v_s ∝ 1/μ` varies by ∓30 %, while `Ga_dif ∝ μ^{−1/3} T^{−2/3}` varies by only ≈ ±10 %.
**The criterion is weakly temperature-sensitive; the settling velocity is not.**

---

## 7. Uncertainty: ranking and propagation

### 7.1 Ranked by contribution to the criterion

| Rank | Parameter | How it enters | Plausible range | Effect on `Ga_dep` | Notes |
|---|---|---|---|---|---|
| **1** | **Floc/aggregate size `a`** | `Ga_dif ∝ a^{8/3}`; `Λ_g ∝ a²`; `Pe_g ∝ a⁴` | 1 µm – 500 µm | **10⁷** across the range (diffusion branch) | **Dominant.** But see §7.2 — it *saturates* |
| **2** | **Motility state** | replaces `k_w` with `v_swim` | on/off | **~500×** for planktonic cells | Binary, not continuous; A12 |
| 3 | Partition of biomass across size classes | selects which `a` applies | unconstrained | up to 10⁷ | **No source found at all.** Arguably rank 1 |
| 4 | `Δρ` of flocs | `Ga ∝ Δρ` | 38–68 (possibly **< 0**) | ~1.8×, plus sign risk | A11, A26 |
| 5 | `α` attachment efficiency | scales `j_dep` | 0.01–1 | 100× on `X`, **0× on the criteria** | Affects the PDE, not the regime boundary |
| 6 | `k_det,0`, `n` | scales `j_det` | 2 decades, `n∈[1,3]` | 0× on criteria | A27 unresolved |
| 7 | Tube diameter `D` | `γ_w ∝ U/D ∝ Q/D³` | 3.18–12.7 mm | `g*` 0.12–0.48 `g_E` | ASSUMED; **quantified in §3.2** |
| 8 | `μ_max`, `K_s`, `Y` | growth only | 1 decade each | 0× on criteria | ASSUMED; affects `X(t)` not regime |
| 9 | `ΔT` in stagnant segments | `Ra ∝ ΔT`; `u_conv ∝ ΔT^{1/2}` | 0.01–5 K | switches convection on/off | **Sharp threshold**, §2.2 |
| 10 | Temperature | `μ^{−1/3}T^{−2/3}` | 15–45 °C | ±10 % | §6.6 |
| 11 | `Δρ` of cells | `Ga ∝ Δρ` | 83–103 | ±11 % | A25 cross-species |
| 12 | Segment length `x` | `Ga_dif ∝ x^{1/3}` | 0.1–2 m | ±2× | ASSUMED |

### 7.2 The most important structural point about the size uncertainty

Naively, `Ga_dif ∝ a^{8/3}` makes floc size catastrophic for the result. **It is not**, because of
(3.3): above the crossover radius `a_c ≈ 3–32 µm`, the criterion switches to the interception branch
where **`a` cancels exactly**. So:

- **Below `a_c`** (single cells, smallest aggregates): `a^{8/3}` sensitivity is real, and this is
  precisely where the criterion sits in its ambiguous band (`Ga_dep` = 0.69–4.2). **Here the size
  uncertainty genuinely matters and must be propagated.**
- **Above `a_c`** (everything from 7 µm up): `Ga_dep` is size-independent and `≫ 1` down to
  10⁻⁶ `g_E`. **Here the size uncertainty is irrelevant to the regime conclusion.** It still matters
  for `Λ_g ∝ a²`, which is where the partial-gravity discrimination actually lives (§3.3).

This is a genuinely reassuring structural result and should be stated prominently: **the conclusion
"gravity dominates floc deposition" is robust to the dominant uncertainty; the conclusion "the
single-cell crossover sits at ~0.24 `g_E`" is not.**

### 7.3 Recommended propagation strategy for the code

**Do both of the following; they answer different questions.**

**(a) Deterministic sensitivity sweep — for the regime boundaries.**
The criteria (3.2)–(3.7) are closed-form and cheap. Sweep the full grid analytically:

```
    g       ∈ {9.81, 3.71, 1.62} ∪ logspace(1e-6, 1e1, 100)   m s⁻²
    d       ∈ logspace(0.5 µm, 1000 µm, 100)
    Q       ∈ logspace(0.1×, 10×) of each sourced nominal
    D       ∈ {3.18, 4.57, 6.35, 9.53, 12.7} mm
```

and emit the **contour surfaces `Ga_dep = 1`, `Λ_g = 1`, `Σ_g = 1`** in `(Q, D, d, g)` space. This
*is* the paper's headline figure and it needs no Monte Carlo — the criteria are analytic, so the
boundary is exact given the inputs.

**(b) Monte Carlo — for the uncertainty band on the boundary.**
Sample `N = 10⁴`–`10⁵` from literature-supported distributions and report the *distribution of
`g*`*, not a point value:

| Parameter | Distribution | Justification |
|---|---|---|
| `d` | **bimodal**: lognormal(μ=1.1 µm, σ_g=1.5) w.p. 0.8 ⊕ lognormal(μ=110 µm, σ_g=2.0) w.p. 0.2 | Sourced: ">80 % of detached clusters ≤ 7 µm" and "volume-dominant band 68–183 µm" `[snippet-level]` — the literature genuinely describes a **bimodal by-number/by-volume** distribution. **Do not use a single lognormal.** |
| `Δρ_cell` | Uniform(83, 103) | Percoll range `[snippet-level]` |
| `Δρ_floc` | Uniform(38, 68) | free-settling range `[snippet-level]` |
| `α` | LogUniform(0.01, 1) | flow-chamber efficiencies `[snippet-level]` |
| `D` | Discrete uniform over standard tube sizes | ASSUMED |
| `T` | Uniform(288, 318) K | ASSUMED operating range |
| `μ_max` | LogUniform(0.02, 0.3) h⁻¹ | ASSUMED |
| `K_s` | LogUniform(0.1, 10) g m⁻³ | anchored to `[snippet-level]` copiotroph range, shifted down |
| `n` (detachment) | Uniform(1, 3) | A27 unresolved |
| `ΔT` | LogUniform(0.01, 5) K | ASSUMED |

**Report `P(Ga_dep > 1 | g = g_Moon)` and `P(Ga_dep > 1 | g = g_Mars)`** as the headline
probabilistic statement, plus the 5th/50th/95th percentiles of `g*`. A criterion reported as
"`g* = 0.24 g_E`" is indefensible given §6; one reported as "`g*` has median 0.24 `g_E` with a 90 %
interval of [0.08, 0.6] `g_E`, so the crossover lies within the exploration gravity range with
probability P" is defensible and is a stronger claim scientifically.

**(c) Mandatory one-at-a-time checks** (cheap, catches structural errors):
`f_θ = 1/π` vs `f_θ = 1` (factor π on the whole gravity term); `n = 1` vs `n = 3`;
`Ra_c = 1708` vs `Ra_c = 1708/2` and `× 2` (A18); `φ(g) ≡ 1` vs a ±20 % `φ` (§4.2).

### 7.4 What would most reduce the uncertainty

In priority order, and all of these are cheap:

1. **Read the full texts.** Rittmann (1986) for real oligotrophic `K_s`/`k`; Rittmann (1982) to
   resolve the linear-vs-exponential detachment contradiction; the Groningen parallel-plate papers
   for the sedimentation/convective-diffusion partition they already measured; Korber et al. (1990)
   for the quantitative motility/gravity split. **Every one of these is currently `[snippet-level]`
   solely because of the proxy block.** This is the single highest-value action and it costs nothing
   but network access.
2. **A particle-size distribution for ECLSS water specifically.** The 0.5 µm WPA depth filter
   `[snippet-level]` implies an upper truncation on what circulates downstream of it — that alone
   would sharply constrain the bimodal distribution in §7.3(b). Worth a dedicated search.
3. **A buoyant density for any of the actual ISS isolates**, removing A25.
4. **The actual WPA/UPA line diameter**, removing the largest ASSUMED geometric input.

---

## 8. Parameter table

**Legend:** `[V]` = verified-existence, `[S]` = snippet-level content, `[A]` = ASSUMED (not sourced),
`[D]` = derived in this document, `[STD]` = standard physical constant / reference-table value.

### 8.1 Physical constants and fluid properties

| Symbol | Value | Units | Source |
|---|---|---|---|
| `k_B` | 1.380649 × 10⁻²³ | J K⁻¹ | `[STD]` SI defined |
| `T` | 298.15 (range 288–318) | K | `[A]` operating range |
| `ρ_f` | 997.0 | kg m⁻³ | `[STD]` water @ 25 °C, IAPWS-95 / CRC |
| `μ` | 8.90 × 10⁻⁴ | Pa s | `[STD]` water @ 25 °C |
| `ν` | 8.926 × 10⁻⁷ | m² s⁻¹ | `[D]` `= μ/ρ_f` |
| `β` | 2.57 × 10⁻⁴ | K⁻¹ | `[STD]` water @ 25 °C thermal expansion |
| `α_th` | 1.46 × 10⁻⁷ | m² s⁻¹ | `[STD]` water @ 25 °C thermal diffusivity |
| `D_S` | 5 × 10⁻¹⁰ | m² s⁻¹ | `[A]` typical small dissolved organic; sweep 2–10 × 10⁻¹⁰ |
| `g_E, g_M, g_L` | 9.81, 3.71, 1.62 | m s⁻² | `[V]` standard; same values as IJMF reduced-g literature `[S]` |
| `Ra_c` | 1708 | — | `[STD]` Rayleigh–Bénard rigid–rigid |

### 8.2 Geometry and flow

| Symbol | Value | Units | Source |
|---|---|---|---|
| WPA process flow | 13 lb/hr = 5.90 | kg hr⁻¹ | `[S]` NTRS 20050207388 / SAE 2005-01-2837 `[V]` |
| WPA wastewater tank | 68 | L | `[S]` same |
| WPA particulate filter | 0.5 | µm | `[S]` same |
| WPA urine feed | 300 | cm³ min⁻¹ | `[S]` same |
| UPA nominal load | 9 | kg day⁻¹ | `[S]` ICES-2021-083 / NTRS 20210015781 `[V]` |
| UPA DA throughput | 1.76–1.93 | kg hr⁻¹ | `[S]` NASA/TM-1998-208539 `[V]` |
| MABR void volume | 1.35 | L | `[S]` J. Environ. Chem. Eng. `[V]` |
| MABR fibres | 1140 × 280 µm dia | — | `[S]` same |
| MABR recirculation | 150 | mL min⁻¹ | `[S]` same |
| MABR HRT | 2.0–10.7 | h | `[S]` same |
| **`D` (WPA/UPA line ID)** | **6.35 (sweep 3.18–12.7)** | **mm** | **`[A]`** — see §1.3; `g*` sensitivity quantified §3.2 |
| **`L` (segment)** | **0.5 (MABR 0.30)** | **m** | **`[A]`** modelling choice |
| **MABR module length** | **0.30** | **m** | **`[A]`** used to derive shell area |
| MABR shell free area | 4.43 × 10⁻³ | m² | `[D]` from above |
| MABR `d_h` | 17.95 | mm | `[D]` `4V/A_wet` |
| **`U` dead leg** | **1 × 10⁻⁴** | **m s⁻¹** | **`[A]`** representative residual flow |
| Dormancy duration | up to 1 | year | `[S]` ICES-2020-42 / NTRS 20205004391 `[V]` |

### 8.3 Particle properties

| Symbol | Value | Units | Source |
|---|---|---|---|
| *P. aeruginosa* cell | 0.5–0.8 × 1.5–3.0 (SEM mean dia 0.65) | µm | `[S]` |
| `a_cell` | 0.544 (`d` = 1.088) | µm | `[D]` cylinder + hemispherical caps |
| `ρ_p` cell | 1080–1100 | kg m⁻³ | `[S]` J. Bacteriol. 148(1):58–63 (1981) `[V]` — **E. coli**, A25 |
| `Δρ_cell` | 83–103 (nom. 93) | kg m⁻³ | `[D]` from above |
| Floc volume-dominant band | 68–183 | µm | `[S]` Water Res. `[V]` |
| Detached cluster size | single cell – 500 (>80 % ≤ 7) | µm | `[S]` Chem. Eng. J. (2013) `[V]`; AEM 67:5608 (2001) `[V]` |
| `ρ_p` floc | 1038–1065 | kg m⁻³ | `[S]` Water Res. (1995) `[V]` |
| `Δρ_floc` | 38–68 (nom. 50) | kg m⁻³ | `[D]` from above |
| Biofilm wet density | 1011–1029 (also 898 reported) | kg m⁻³ | `[S]` ChemEngineering 10(2):23 `[V]` — A11 |
| `v_swim` | 32.1 ± 0.3 | µm s⁻¹ | `[S]` *P. putida* WT, bioRxiv 2022.08.03.502738 `[V]` |
| `D_B(a)` | `k_BT/6πμa` | m² s⁻¹ | `[D]` Stokes–Einstein |

### 8.4 Water chemistry and bioburden

| Symbol | Value | Units | Source |
|---|---|---|---|
| WPA wastewater TOC | > 2000 | mg L⁻¹ | `[S]` |
| ISS potable TOC spec | ≤ 3 | mg L⁻¹ | `[S]` Sci. Rep. 12 (2022) 19320 `[V]` |
| ISS potable bacteria spec | ≤ 50 | CFU mL⁻¹ | `[S]` same |
| Typical in-flight level | "a few" | CFU mL⁻¹ | `[S]` same |
| Dominant genera | *Burkholderia, Ralstonia, Cupriavidus, Methylobacterium, Sphingomonas, Stenotrophomonas, Pseudomonas* | — | `[S]` MRA (2023) DOI 10.1128/mra.00158-23 `[V]`; Biofilm 5 (2023) `[V]` |

### 8.5 Kinetic and wall-exchange parameters — **all ASSUMED**

| Symbol | Value | Range to sweep | Units | Status |
|---|---|---|---|---|
| `μ_max` | 0.1 | 0.02–0.3 | h⁻¹ | **`[A]`** no oligotrophic rate found |
| `K_s` | 1.0 | 0.1–10 | g-C m⁻³ | **`[A]`** anchored to `[S]` copiotroph 10–180 mg/L, shifted per Rittmann 1986 `[V]` qualitative finding |
| `Y` | 0.4 | 0.2–0.6 | kg-dry (kg-C)⁻¹ | **`[A]`** standard heterotroph |
| `b` | 0.002 | 0.0005–0.01 | h⁻¹ | **`[A]`** |
| `b_f` | 0.001 | 0.0002–0.005 | h⁻¹ | **`[A]`** |
| `ρ_X` | 30 | 10–80 | kg-dry m⁻³ | **`[A]`** consistent with `[S]` wet densities @ 97 % water |
| `α` | 0.3 | 0.01–1 | — | **`[A]`** midpoint of `[S]` 0.36–0.78 band, rounded down |
| `k_det,0` | 1 × 10⁻⁵ | 10⁻⁶–10⁻⁴ | s⁻¹ | **`[A]`** set to give ~20 d timescale at R1 shear |
| `n` | 1 | 1–3 | — | **`[A]`** sources contradict (linear vs exponential) `[S]` |
| `τ_ref` | 1.0 | — | Pa | **`[A]`** normalisation only |
| `X_0` | 1 × 10⁻⁶ | — | kg m⁻² | **`[A]`** sparse seed |
| cell dry fraction | 0.3 | 0.2–0.4 | — | **`[A]`** standard |
| `ΔT` (stagnant) | 0.5 | 0.01–5 | K | **`[A]`** |
| `D_conv` mixing-length factor | 1/10 | 1/3–1/30 | — | **`[A]`** |

### 8.6 Derived criterion values (headline)

| Quantity | Earth | Mars | Moon | Source |
|---|---|---|---|---|
| `Ga_dep`, single cell, WPA nominal line | **4.20** | **1.59** | **0.694** | `[D]` (3.2) |
| `g*_dif`, single cell, WPA line | **0.238 `g_E`** (range 0.12–0.48 over `D`) | — | — | `[D]` (3.4) |
| `Ga_dep`, any floc ≥ 7 µm, WPA line | 1878 | 710 | 310 | `[D]` (3.3) |
| `g*_int`, WPA line | 5.32 × 10⁻⁴ `g_E` | — | — | `[D]` (3.5) |
| `Λ_g`, 100 µm floc, WPA line | 0.932 | 0.352 | 0.154 | `[D]` (3.6) |
| `Λ_g`, 183 µm floc, WPA line | 3.12 | 1.18 | 0.515 | `[D]` (3.6) |
| `Σ_g`, 183 µm floc, WPA line | 0.101 | — | 0.017 | `[D]` (3.7) |
| `Σ_g`, 183 µm floc, dead leg | 52.3 | — | 8.64 | `[D]` (3.7) |
| `Pe_g`, single cell, 6.35 mm, stagnant | 950 | — | 157 | `[D]` (3.8) |
| `t_settle`, cell, 6.35 mm line | 26.2 h | 69.2 h | 158 h | `[D]` |
| `t_settle`, cell, 0.30 m tank | 51.5 d | 136 d | 312 d | `[D]` |
| `ΔT_c`, 6.35 mm line | 0.345 K | 0.912 K | 2.088 K | `[D]` (2.5) |
| `ΔT_c`, 0.30 m tank | 3.27 × 10⁻⁶ K | 8.65 × 10⁻⁶ K | 1.98 × 10⁻⁵ K | `[D]` (2.5) |
| `d_max` for 5 % Stokes accuracy | 184 µm | 254 µm | 335 µm | `[D]` (2.3) |
| `a_c` (diffusion↔interception) | 6.8 µm (WPA line) | — | — | `[D]` (2.14) |

---

## 9. "Ready for implementation" checklist

Everything the Python model needs, in dependency order. Equation numbers refer to this document.

### 9.1 Constants and properties module
- [ ] `k_B`, `T`, `ρ_f(T)`, `μ(T)`, `ν`, `β`, `α_th`, `D_S` — §8.1
- [ ] `g` as a **free parameter**, defaulting to {9.81, 3.71, 1.62, 0} — §8.1
- [ ] `Ra_c = 1708` — §8.1

### 9.2 Particle kinematics
- [ ] **(2.1)** `v_s = (2/9)Δρ g a²/μ` — Stokes
- [ ] **(2.2)** Schiller–Naumann iterative correction; auto-engage when `Re_p > 0.34`
- [ ] `Re_p = ρ_f v_s (2a)/μ` with an assertion/warning when Stokes is used out of range
- [ ] **(2.11)** `D_B = k_B T/(6πμa)` — Stokes–Einstein
- [ ] **(2.3)** report `d_max(g)` for the Stokes-validity boundary

### 9.3 Hydrodynamics
- [ ] `U = Q/A`; `Re = ρ_f U D/μ`
- [ ] **(2.9)** `γ_w = 8U/D`, `τ_w = μγ_w`, `u* = √(τ_w/ρ_f)` for `Re < 2300`
- [ ] Blasius branch `f = 0.316 Re^{−1/4}`, `τ_w = (f/8)ρ_f U²` for `Re ≥ 2300`
- [ ] Entrance-length check `L_e = 0.05 Re D`; warn when `L_e > 0.1 L` (A2)

### 9.4 Wall-transport velocities
- [ ] **(2.10)** `k_lev = 0.538 D_B^{2/3}(γ_w/x)^{1/3}`, with `x → max(x, D)` regularisation
- [ ] **(2.12)** `k_int = γ_w a²/(2x)`
- [ ] **(2.13)** `k_w = max(k_lev, k_int)`
- [ ] **(2.14)** report the crossover radius `a_c`

### 9.5 Buoyancy
- [ ] **(2.4)** `Ra = gβΔT H³/(ν α_th)`
- [ ] **(2.5)** `ΔT_c = 1708 ν α_th/(gβH³)`
- [ ] **(2.6a/b)** `u_conv`, with the `Ra < Ra_c ⇒ u_conv = 0` switch
- [ ] **(2.7)** `Ω = v_s/u_conv`

### 9.6 The four criteria (analytic — no PDE needed)
- [ ] **(3.1)** `Ga_dep = v_s cosθ / k_w`
- [ ] **(3.2)** `Ga_dif = 2.925 Δρ g a^{8/3} μ^{−1/3}(k_BT)^{−2/3}(x/γ_w)^{1/3}` — verify it
      reproduces (3.1) on the diffusion branch (regression test: **4.2035** for P1/R1/Earth)
- [ ] **(3.3)** `Ga_int = (4/9)Δρ g x/(μ γ_w)` — verify size-independence (regression test:
      **1878** for R1/Earth)
- [ ] **(3.4)** `g*_dif`; **(3.5)** `g*_int = 9μγ_w/(4Δρ x)` (regression: **5.32 × 10⁻⁴ g_E**, R1)
- [ ] **(3.6)** `Λ_g = v_s L/(U R)` (regression: **0.932** for P3/R1/Earth)
- [ ] **(3.7)** `Σ_g = 2Δρ g a/(15.31 μ γ_w)` (regression: **0.101** for P4/R1/Earth)
- [ ] **(3.8)** `Pe_g = v_s H/D_B` (regression: **950** for P1/6.35 mm/Earth)
- [ ] `Ga_mot = v_s/v_swim` for the planktonic single-cell class (§4.3)
- [ ] Regime classifier: `≪1` (<0.1), **ambiguous** (0.1–10), `≫1` (>10)

### 9.7 PDE model
- [ ] State vector `y = [C_1…C_5, S, X]` on `N` nodes (start `N = 200`)
- [ ] **(5.1)** suspended biomass; **(5.2)** substrate; **(5.3)** biofilm
- [ ] **(5.4)/(5.5)** `j_dep = α k_tot C`, `k_tot = f_θ v_s(g) + k_w`
- [ ] **(5.6)** `f_θ = 1/π` horizontal tube / `0` vertical / `cos θ` flat wall
- [ ] **(5.7)/(5.8)** stagnant-branch `D_v`, `h_s`, and the `k_tot` replacement
- [ ] **(5.9)** `j_det = k_det,0 (τ_w/τ_ref)^n X`
- [ ] **(5.10)** Monod `μ(S)`; **(4.1)** `φ(g) ≡ 1` hook, default identity, **must stay identity in
      the published baseline**
- [ ] **(5.11)** optional external mass-transfer `S_w` Newton solve
- [ ] **(5.12)** Danckwerts inlet, zero-gradient outlet, recycle-closure option, zero-flux stagnant
- [ ] `D_ax = D_B` — **do not use Taylor–Aris** (§5.6); assert `t_res ≪ D²/D_B`
- [ ] Upwind advection; central diffusion; `solve_ivp(method='BDF'|'LSODA')` with `jac_sparsity`
- [ ] Non-negativity clipping; grid-convergence check at `N` = 100/200/400

### 9.8 Parameters
- [ ] All of §8, with every `[A]` value carrying a machine-readable `assumed=True` flag so the
      limitations section can be auto-generated
- [ ] Sourced values (`[V]`/`[S]`) carry their citation string

### 9.9 Uncertainty
- [ ] §7.3(a) deterministic sweep → the `Ga_dep = 1`, `Λ_g = 1`, `Σ_g = 1` contour surfaces in
      `(Q, D, d, g)` — **the paper's headline figure**
- [ ] §7.3(b) Monte Carlo (`N ≥ 10⁴`) with the **bimodal** size distribution — report the `g*`
      distribution and `P(Ga_dep > 1 | g)` at Mars and lunar gravity
- [ ] §7.3(c) one-at-a-time structural checks: `f_θ` (1/π vs 1), `n` (1 vs 3), `Ra_c` (×0.5, ×2),
      `φ(g)` (1 vs ±20 %)

### 9.10 Validation targets (all published, all `[snippet-level]` until full texts are readable)
- [ ] **Korber et al., Biofouling 2:335–350 (1990)** — flagellar mutants deposit 10–40× more on
      lower than upper surfaces; wild-type gravity-independent. The model with `f_θ = ±1` (upper vs
      lower flat wall) and motility off/on must reproduce that ratio.
- [ ] **Li/Busscher/van der Mei, Colloids Surf. B (2011)** — sedimentation, not convective
      diffusion, is the dominant mass-transport mechanism in a parallel-plate chamber; deposition
      efficiency relative to sedimentation falls 0.78 → 0.36 as flow rate rises. The model's
      `Ga_dep ≫ 1` in low-shear parallel-plate geometry must be consistent with this.
- [ ] **Santomartino et al. (BioRock), Front. Microbiol. 11 (2020)** — no effect of µg or simulated
      Mars gravity on *final bulk cell concentration*. The model must reproduce a **null in bulk
      concentration** while predicting a **non-null in spatial distribution** (§4.1). This is the
      single most important consistency check in the whole program.
- [ ] **Chen, Hong & Walker, Langmuir 26(1):314–319 (2010)** — top vs bottom deposition of 0.5/1.1/
      1.8 µm spheres and *Burkholderia cepacia* G4g at 0.06 and 3 mL/min. Direct quantitative target
      for `Ga_dep` in the sub-`a_c` branch.
- [ ] **Marra, Rizzo & Caserta, npj Biofilms Microbiomes 11:122 (2025)** and **Water 17(15):2277
      (2025)** — gravity × shear on biofilm in laminar microchannels; surface-inclination series at
      0/45/90/180°. Direct target for the `f_θ = cos θ` orientation factor.

---

## 10. Bottom line, and the honest caveat

**The criterion is:**

```
    Ga_dep = v_s cosθ / max(k_lev, k_int)      (wall-normal delivery)
    Λ_g    = v_s L / (U R)                     (sufficient length — Hazen number)
    Σ_g    = 2Δρ g a / (15.31 μ γ_w)           (retention force balance)
    [+ Ra/Ra_c and Ω = v_s/u_conv in stagnant segments]
```

all four linear (or `g^{1/2}`) in `g`, with the closed forms (3.2)–(3.7) and the explicit thresholds
(3.4)–(3.5).

**It does not resolve to a trivially wide margin** — the failure mode `problem_statement.md` §4
named as the single biggest risk. Three of the results sit squarely in the interesting range:
the single-cell deposition crossover at `g* ≈ 0.24 g_E` (between Mars and lunar gravity); the
size-selective floc carry-through transition at 100–183 µm across the same window; and the
convection-onset switch (`ΔT_c` = 0.35 / 0.91 / 2.09 K) that can make lunar gravity *increase*
net deposition in narrow stagnant lines.

**Biggest concern — stated plainly.** The `Ga_dep ≫ 1` results rest on comparing a body-force
transport velocity against a **perfect-sink Lévêque** wall-transport velocity, and the enormous
margins (10²–10⁶) arise mostly because Brownian diffusion of micron-scale particles is
extraordinarily weak, not because gravity is strong. A referee who believes the real competitor is
hydrodynamic dispersion, secondary flows, wall roughness, or bulk turbulence — none of which this
1-D treatment carries — could argue `k_w` is understated by orders of magnitude, which would move
`g*` proportionally. The counter-argument is that the Groningen parallel-plate measurements
independently found sedimentation dominant over convective diffusion in exactly this geometry
`[snippet-level]` — **but I could not read that paper, so the strongest available defence of the
central result is currently a search snippet.** Clearing the proxy block (§7.4 item 1) is the
highest-value next action for the program, and until it is cleared this derivation should be treated
as structurally sound but evidentially thin at its single most load-bearing joint.
