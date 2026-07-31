# Phase 2 Novelty & Tractability Adjudication

**Adjudicator:** Opus (adversarial due diligence pass)
**Date:** 2026-07-31
**Input:** `docs/gap_register.md` + `lit/notes/*.md` (8 Haiku subsystem surveys)
**Mandate:** Try to *disprove* the novelty of each of three finalists before committing months of effort.

---

## 0. Method, and an honest statement of limitations

I ran ~33 targeted adversarial web searches across the three candidates, deliberately structured to find (a) someone already doing exactly the proposed work, including non-NASA sources; (b) a cheaper/simpler prior solution that makes the work unnecessary; (c) a hidden invalidating assumption in the underlying physics or biology.

**Limitation that materially affects confidence — read this before trusting any content claim below.**
The sandbox's outbound HTTPS proxy denied `CONNECT` to nearly every scholarly host I needed: `ntrs.nasa.gov`, `sciencedirect.com`, `nature.com`, `mdpi.com`, `ncbi.nlm.nih.gov`, `pmc.ncbi.nlm.nih.gov`, `biorxiv.org`, `ices.space` all returned HTTP 403 at the proxy (confirmed via `$HTTPS_PROXY/__agentproxy/status`, which logged `connect_rejected` for `ices.space:443` and `ntrs.nasa.gov:443`). **I therefore could not read a single full text.** Every citation below was surfaced by web search and its existence, title, authorship and venue are corroborated across independent search result sets — but all statements about what a paper *contains* are at search-snippet fidelity, not read-the-PDF fidelity.

Consequences, stated plainly:
- Claims marked **[verified-existence]** — the paper demonstrably exists with the stated title/authors/venue.
- Claims marked **[snippet-level]** — the content assertion comes from search-result summarization and should be re-checked against the PDF before it is relied on in a submission.
- Where I say "no prior art found," that is **weak** evidence of novelty, not proof. Absence of hits in a search-only workflow is especially weak here given I could not search full text.

The verdicts below are nonetheless firm, because in all three cases the disqualifying evidence is *positive* (prior art found), not *negative* (prior art absent). Positive findings survive the fetch limitation; a "clean search" would not have.

---

## 1. Candidate A — Partial-gravity microbial/biofilm kinetics for ECLSS water & waste systems

### Claim under test
Existing biofilm/microbial growth models for spacecraft water and waste systems are calibrated only to ISS conditions (microgravity, or historical 1 g ground data); none address lunar (1/6 g) or Mars (0.38 g) partial-gravity kinetics. Proposed: population-dynamics ODEs with gravity-scaled sedimentation/mass-transfer terms, 1 g bench validation, extrapolation to partial g with uncertainty bounds.

### Closest genuine prior art found

**A-1. Latham, A.P., Skountzos, E.N., Lawson, J.W. (NASA Ames Research Center). "Toward resolving gravitational effects on microbial growth with computer simulations." bioRxiv, preprint 2026.05.15.725518, posted May 2026.** [verified-existence]
This is the single most damaging find. It is a NASA Ames computational study that modifies a previously developed model of cell growth in microgravity, improving the growth functional form (Monod replacing Blackman) and code usability, explicitly "to enable further research into how microbial communities are influenced by gravity." Its headline result is a *mechanism decomposition*: **lack of gravity-driven flow decreases cell growth in microgravity, while absence of sedimentation increases cell growth in microgravity** [snippet-level]. That is precisely the "gravity-scaled sedimentation/mass-transfer terms" decomposition Candidate A proposes to build, done by the agency, three months before this adjudication.

**A-2. Bhattacharjee/Lee et al., "CAMDLES: CFD-DEM Simulation of Microbial Communities in Spaceflight and Artificial Microgravity." *Life* (MDPI) 2022, 12(5), 660. PMID 35629329.** [verified-existence]
The parent framework of A-1. CFD-DEM + agent-based modeling of biological flow, growth, and **mass transfer** in microgravity and in ground analog devices (rotating wall vessels). Simulation mass-transfer calculations are correlated with **Monod dynamic parameters to predict relative growth rates between artificial microgravity, spaceflight microgravity, and 1 g** [snippet-level]. Gravity is already a tunable parameter in a published, working, NASA-affiliated code. Extending it to 1/6 g and 0.38 g is a parameter sweep, not a research program.

**A-3. Gesztesi, J., Broddrick, J.T., Lannin, T., Lee, J.A. (NASA Ames / Northeastern). "The chemical neighborhood of cells in a diffusion-limited system." *Frontiers in Microbiology* 14:1155726 (2023). DOI 10.3389/fmicb.2023.1155726. PMID 37143535.** [verified-existence]
Analytical + finite-difference modeling of the substrate depletion zone around a cell when sedimentation and density-driven convection are removed. Reports a quantitative zone-of-depletion radius of **5.04 mm** (10 % substrate reduction) for a single *E. coli* cell under their simulated conditions [snippet-level]. This is the mechanistic core Candidate A would have had to build from scratch — already built, already quantified, already NASA.

**A-4. Santomartino, R., Waajen, A.C., Nicholson, N., et al. (ESA BioRock). "No Effect of Microgravity and Simulated Mars Gravity on Final Bacterial Cell Concentrations on the International Space Station: Applications to Space Bioproduction." *Frontiers in Microbiology* 11 (2020). PMID 33154740.** [verified-existence]
**This is the hidden invalidating assumption.** ESA flew three bacterial species on ISS under microgravity, **simulated Mars gravity** (on-orbit centrifuge) and simulated Earth gravity, with ground controls — and the title states the finding: *no effect* on final cell concentrations. A corroborating snippet notes that despite different predicted sedimentation rates, no significant differences in final cell counts or optical densities were observed across gravity regimes [snippet-level]. Candidate A's premise is that partial-gravity kinetics differ enough to matter; the only flight experiment that has actually tested Mars gravity on bacteria says the bulk outcome does not.

**A-5. Abrevaya et al. (attribution per ADS 2022Life...12.1399A). "Simulated Micro-, Lunar, and Martian Gravities on Earth—Effects on *Escherichia coli* Growth, Phenotype, and Sensitivity to Antibiotics." *Life* 2022, 12(9), 1399. DOI 10.3390/life12091399.** [verified-existence]
Inclined clinostats at optimized 5 rpm, three *E. coli* strains, **simulated micro-, lunar AND Martian gravity**, measuring growth dynamics, phenotype, antibiotic sensitivity. Findings: increased growth under simulated micro- and lunar gravity *for some strains*; higher antibiotic concentrations needed under simulated lunar gravity [snippet-level]. The empirical partial-gravity microbial growth dataset Candidate A proposes to predict already exists — and is strain-dependent, which is fatal for a clean scaling law.

**A-6. Marra, D., Rizzo, M., Caserta, S. "A microfluidic investigation unveils the role of gravity and shear stress on *Pseudomonas fluorescens* motility and biofilm growth." *npj Biofilms and Microbiomes* 11, article 122 (1 July 2025).** [verified-existence]
Quantifies the *combined* effect of gravity and shear on biofilm growth in a laminar-flow microchannel, comparing top vs. bottom surfaces. Finds asymmetric cell distribution and differing surface contamination driven by gravity direction and shear stress [snippet-level]. Directly occupies the "gravity × biofilm in a flowing system" niche.

**A-7. "Contribution of the Gravity Component and Surface Type During the Initial Stages of Biofilm Formation at Solid–Liquid Interfaces." *Water* (MDPI) 2025, 17(15), 2277. DOI 10.3390/w17152277, published 31 July 2025.** [verified-existence]
*P. fluorescens* adhesion on stainless steel and polycarbonate — **explicitly noted as space-relevant water-distribution materials** — at surface inclinations of 0°, 45°, 90°, 180° to isolate the gravity component. Finds material type dominates on PC; SS shows angle-dependent variation implying combined gravitational-convection and surface effects [snippet-level].

**A-8. Supporting occupancy of the ECLSS-specific niche:** Muirhead, D.L., Hicks, P.M., Garcia Fernandez, R., Jackson, W.A., Gelbart, E., Adam, N., Callahan, M.R., "Evaluation of an Aeration Module for Microbial Environmental Control Life Support System (mECLSS) Integration with ECLSS," **ICES-2025-49**, 54th ICES, Prague, July 2025 (NTRS 20250003738) [verified-existence] — biofilm oxygen limitation and shedding in the WPA, with aeration to sustain healthy biofilm. And Carlson, A.L., Lange, K.E., Callahan, M., "Modeling Evolvable Water Recovery Systems for Short and Long-Duration Missions in Partial Gravity," **ICES-2024-323** (NTRS 20240001310 / 20240005573) [verified-existence] — NASA JSC already modeling water recovery *specifically for partial gravity*.

### Verdict

**How the proposed work differs from prior art (one sentence):** It would apply a gravity-parameterized population-dynamics model to ECLSS water/waste hardware specifically, rather than to generic suspension culture or bioreactor analogs — a *domain transfer* of an existing NASA modeling capability (CAMDLES/CAMDLES2), not a new capability.

**Novelty confidence: LOW.** Three independent NASA Ames modeling efforts (A-1, A-2, A-3) already own the mechanism; two independent experimental groups (A-4, A-5) already own the partial-gravity data at lunar and Mars levels; two 2025 papers (A-6, A-7) already own gravity-plus-shear biofilm behavior on space-relevant materials. The cross-survey convergence flagged in `gap_register.md` §"Cross-cutting observation" turns out to be four Haiku agents independently rediscovering a *well-populated* field rather than an empty one — the convergence signalled relevance, and the register correctly warned it "raises the novelty bar," but the bar is higher than the register estimated.

**Hidden invalidating assumption — this is the serious problem.** Candidate A assumes gravity-scaled kinetics are (i) real at 1/6 g and 0.38 g and (ii) monotonic in g, so that a 1 g-calibrated model can be extrapolated downward with uncertainty bounds. Both halves are in doubt:
- A-1 reports **two opposing gravity mechanisms** (loss of gravity-driven flow *decreases* growth; loss of sedimentation *increases* growth). A quantity governed by two competing terms of similar magnitude is not reliably monotonic in g, and an extrapolation built on a single scaled sedimentation term would be wrong in sign over part of the range.
- A-4 is a flight experiment at Mars gravity that found **no** bulk effect.
- A-5 finds the effect is **strain-dependent** — some strains only.
- Most decisively for the ECLSS application: a WPA/UPA/MABR is a *pumped* loop. Forced advection and wall shear exceed cell-scale sedimentation velocity (∝ g) and buoyancy-driven convection (∝ g) by orders of magnitude. The Klaus/Gesztesi diffusion-limited depletion-zone mechanism is defined for **non-motile cells in quiescent suspension**; it is largely irrelevant once the pump is running. Candidate A's central physical premise is therefore weakest exactly where its mission relevance is strongest.

**Tractability: adequate but the result would likely be null and undefendable.** The code is easy (Python ODEs, a week). The problem is that the falsifiable claim — "partial-gravity kinetics differ from ISS-calibrated kinetics by X%" — cannot be defended without partial-gravity validation data the program does not have, and the best available evidence (A-4) points at X ≈ 0. A paper that predicts an effect nobody can measure, against a flight experiment that found none, is not a defensible ICES contribution.

---

## 2. Candidate B — Combined-stressor material flammability envelope for exploration habitats

### Claim under test
NASA/NIST flammability data is single-factor (oxygen concentration **or** pressure tested independently); no validated combined-factor model exists for planned habitat atmospheres (Gateway 26.5 % O₂ / 73.5 kPa; lunar surface up to 34 % O₂ / 56.5 kPa).

### Closest genuine prior art found

**This premise is factually false.** NASA White Sands Test Facility has run combined O₂ × total-pressure flammability matrices for roughly two decades and has published fitted relationships.

**B-1. "Pressure Effects on Oxygen Concentration Flammability Thresholds of Materials for Aerospace Applications." NASA, NTRS 20070005041 (2007).** [verified-existence]
The title alone contradicts the premise: it is a joint pressure × oxygen-concentration study. Reported finding: **oxygen concentration and oxygen partial pressure flammability thresholds depend on total pressure and vary as a near-linear function of total pressure** [snippet-level]. Motivated explicitly by NASA's exploration program anticipating "various habitable environments."

**B-2. Hirsch, D.B., Juarez, A., Peyton, G.J., Harper, S.A., Olson, S.L. "Selected Parametric Effects on Materials Flammability Limits." 41st International Conference on Environmental Systems, Portland, July 2011. NTRS 20110008636.** [verified-existence]
An ICES paper — i.e. the exact venue being targeted — describing NASA-STD-6001B Test 1 evaluation with the "worst case configuration" defined as **a combination of material thickness, test pressure, oxygen concentration, and temperature** [snippet-level]. Combined-factor by construction. Reports a pressure threshold in 99.8 % oxygen of 0.4–0.9 psia for typical spacecraft materials.

**B-3. Harper, S.A., Juarez, A., et al. "Oxygen Partial Pressure and Oxygen Concentration Flammability: Can They Be Correlated?" NASA, NTRS 20160001047 / 20160004937 (2016).** [verified-existence]
**This is the "cheaper/simpler prior solution."** The paper asks Candidate B's question directly and answers it: material flammability depends on both oxygen concentration and pressure, but **oxygen concentration is the primary driver** — which is why all materials are certified at a single bounding 30 % O₂ / 10.2 psia point for Orion rather than across a two-dimensional envelope [snippet-level]. A corroborating snippet from the WSTF line of work states flammability shows strong oxygen-concentration dependence with little relation to total pressure above ~6 psia, increased pressure dependence below 6 psia, and that **power-equation models fit MOC-vs-total-pressure and partial-pressure-vs-total-pressure trends "very precisely" across 0.4–17.3 psia** [snippet-level]. A fitted combined-factor model already exists; NASA's operational answer is that a bounding-point certification is sufficient and cheaper.

**B-4. NESC / HLS / NASA GRC / WSTF team. ICES-2025-392, 54th ICES, Prague, July 2025 (NTRS 20250002114, 20250006779).** [verified-existence]
An active, multi-center NASA program on Candidate B's exact problem *including the gravity dimension the candidate omits*: it addresses uncertainty about **the impact of lunar gravity on material flammability limits at 56.5 kPa**, notes low-gravity data showing enhanced flammability at very low flow rates, and reports upward high-flow oxygen-index testing in a WSTF chamber operating continuously at 57 kPa across five materials (PMMA, P213 tape, cotton, polycarbonate, Nomex Velcro) at multiple flow rates, developing correction factors [snippet-level].

**B-5. NASA "Flammability of Materials on the Moon" (FM2), targeting launch late 2026.** [verified-existence]
Four solid fuel samples burned autonomously in a sealed chamber simulating planned lunar habitat atmospheric conditions, instrumented for flame size, spread rate, O₂, CO₂, flame and fuel temperature. Described as creating "a real database on flammability in partial gravity, something that does not yet exist outside of Earth."

**B-6. NESC Technical Bulletin TB 26-04, "Webbings for Use in Elevated Oxygen Environments."** [verified-existence] A 60 % Kevlar / 40 % PBI webbing passed NASA-STD-6001B Test 1 at **37 % oxygen and 8.2 psia** [snippet-level] — i.e. combined-condition qualification testing at exploration-atmosphere conditions is routine practice, not a gap.

### Verdict

**How the proposed work differs from prior art (one sentence):** It does not meaningfully differ — a regression model fit to published single-factor datasets would reproduce, with strictly less data, relationships NASA WSTF has already fitted from purpose-run combined-condition test matrices.

**Novelty confidence: LOW.** The central factual claim ("single-factor only") is contradicted by at least three NASA publications spanning 2007–2016, one of which is itself an ICES paper. Worse, the program is *active*: ICES-2025-392 was presented eleven months before this adjudication and covers the same envelope plus the gravity axis, and FM2 flies within months. Submitting a regression fit to secondary data into a session where the WSTF/NESC team is presenting primary data at the same conditions is a losing position.

**Hidden invalidating assumption:** Candidate B assumes the two factors are separably informative. B-3 indicates NASA already collapsed them — oxygen concentration dominates, with pressure a secondary correction below ~6 psia — meaning the "envelope" is closer to one-dimensional than two-dimensional over the range of interest, and a bounding-point certification is the operationally correct (and cheaper) answer. The proposed model would add complexity to solve a problem the community has deliberately simplified away.

**Tractability:** High in the trivial sense (curve-fitting is easy), but there is no defensible falsifiable claim left to make.

---

## 3. Candidate C — Fractional-gravity two-phase heat/mass-transfer scaling correlations

### Claim under test
Two-phase flow boiling/condensation is well characterized at 1 g and reasonably at 0 g (FBCE), but **no validated correlation exists for the fractional-gravity regime**. Proposed: a CFD/analytical scaling law interpolating between 1 g and 0 g correlations via Bond/Froude-number analysis, checked against parabolic-flight fractional-g data.

### Closest genuine prior art found

This is the most comprehensively pre-empted of the three. The proposed *method* was published in 2004, under essentially the proposed *title*.

**C-1. Hurlbert, K.M., Witte, L.C., Best, F.R., Kurwitz, C. "Scaling two-phase flows to Mars and Moon gravity conditions." *International Journal of Multiphase Flow* 30 (2004) 351–368.** [verified-existence]
KC-135 parabolic-flight hydrodynamic measurements of two-phase flow at **Mars and Moon gravity**, R-12 in an 11.1 mm tube, ~150 parabolas. Key result: **the Euler number (containing pressure drop) scales with the Froude number in a simple power law** for a given fluid, saturation temperature and flow regime [snippet-level]. That is Candidate C's Froude-number scaling law, for exactly Candidate C's two gravity levels, twenty-two years ago.

**C-2. Raj, R., Kim, J., McQuillen, J. "Gravity Scaling Parameter for Pool Boiling Heat Transfer." *ASME Journal of Heat Transfer* 132(9):091502 (2010).** [verified-existence]
An explicit gravity scaling parameter (the "RKM model") predicting the influence of gravitational acceleration on nucleate boiling across gravity levels, with a buoyancy-dominated regime at large heaters/higher g and a surface-tension-dominated regime at low g/small heaters [snippet-level]. Later refined against 200+ ISS pool-boiling runs with n-perfluorohexane (ASME JHT 134(10):101504, 2012, "Pool Boiling Heat Transfer on the International Space Station"). Search results explicitly frame this line of work as addressing prediction "at various gravity levels such as Earth, Mars, and lunar gravity."

**C-3. "Flow regime transition criteria for two-phase flow at reduced gravity conditions." *International Journal of Multiphase Flow* (2011).** [verified-existence]
Extends normal-gravity flow-regime transition criteria to reduced gravity, with sample computations run at **0.196, 1.62, 3.71 and 9.81 m/s² — i.e. micro-, lunar, Martian and Earth gravity** [snippet-level]. This is Candidate C's interpolation, already computed at Candidate C's target gravity levels.

**C-4. Konishi, C., Mudawar, I., Hasan, M.M. "Criteria for negating the influence of gravity on flow boiling critical heat flux with two-phase inlet conditions." *International Journal of Heat and Mass Transfer* 65 (2013) 203–218.** [verified-existence]
Three dimensionless criteria which, satisfied simultaneously, negate gravity's influence on flow boiling CHF (gravity perpendicular to the heated wall, gravity parallel to it, sufficient heated length for liquid contact) [snippet-level]. Together with Zhang/Mudawar/Hasan's gravity-independence criteria, this is the mature form of the "when does gravity matter" question in this field.

**C-5. "Assessment and development of flow boiling critical heat flux correlations for partially heated rectangular channels in different gravitational environments." *International Journal of Heat and Mass Transfer* (2022).** [verified-existence] — correlations explicitly developed across gravitational environments.

**C-6. "Cryogenic flow boiling in microgravity: Effects of reduced gravity on two-phase fluid physics and heat transfer." *International Journal of Heat and Mass Transfer* (2023).** [verified-existence]
Parabolic-flight LN₂ flow boiling with heat-transfer measurements and high-speed interfacial video **at microgravity, hypergravity, Lunar gravity and Martian gravity**, evaluating seminal HTC correlations and proposing a new one [snippet-level]. This is Candidate C's deliverable — fractional-gravity data plus a new correlation — published three years ago.

**C-7. "Numerical investigation of the gravity effect on two-phase flow and heat transfer of neon condensation inside horizontal tubes." *Applied Thermal Engineering* (2023).** [verified-existence]
Condensation across **zero, Lunar, Martian and Earth gravity**, mass flux 20–187 kg/m²s, finding enhancement, deterioration and gravity-independent regimes selected mainly by mass flux and vapor quality [snippet-level]. Covers the condensation half of Candidate C.

**C-8. Historical fractional-g flow-pattern maps:** Hamm & Best (1997), KC-135 horizontal-pipe flow patterns at **lunar and Martian gravity**; McQuillen, KC-135 flow-pattern maps under lunar gravity for water–glycerin, air–water, and air–water + Zonyl [snippet-level, via IJMF review coverage]. Plus NASA's own "Two Phase Flow Modeling: Summary of Flow Regimes and Pressure Drop Correlations in Reduced and Partial Gravity" (NTRS 20060008906) [verified-existence] — a NASA summary document of partial-gravity correlations, which is close to a direct refutation of the claim that none exist.

**C-9. Active competing effort:** SwRI + Texas A&M parabolic-flight campaigns on boiling at **multiple partial-gravity levels** (SwRI internal R&D 18-R6267, flights April 2023/2024) [verified-existence]; and Purdue/Mudawar's FBCE, whose condensation module completed its ISS campaign July 2025, with Mudawar having published 70+ reduced-gravity papers and contributed to the decadal survey [snippet-level].

### Verdict

**How the proposed work differs from prior art (one sentence):** It differs only in framing — Bond/Froude-number scaling between the 1 g and 0 g limits for lunar and Martian gravity is not an open gap but a 20-year-old, actively-extended subfield with parabolic-flight data, published scaling parameters, gravity-independence criteria, and 2023-vintage fractional-g correlations for both boiling and condensation.

**Novelty confidence: LOW — the lowest of the three.** The Haiku thermal-control survey's framing rested on one 2023 NASA topical whitepaper (Khusid) saying gravity-independent *design criteria* are "needed but not yet finalized." That statement is about the maturity and standardization of design guidance for a specific application, not about the absence of correlations. The survey read a call for consolidation as a research vacuum. The vacuum does not exist.

**Hidden invalidating assumption:** The candidate assumes the fractional-g regime is a smooth interpolation between the 1 g and 0 g limits. C-7 indicates gravity effects on condensation are **non-monotonic in character** — enhancement, deterioration, and gravity-independence appear in different regions of the (mass flux, vapor quality) plane. A single Bond/Froude interpolant is the wrong functional form, and the field already knows this, which is why the mature literature uses regime-selection *criteria* (C-4) rather than a global interpolation.

**Tractability:** The proposed CFD is in fact the *least* tractable of the three for a bounded single-paper effort with no facility access, and it would be judged against groups (Purdue, SwRI/TAMU, NASA GRC) holding primary flight data.

---

## 4. Ranking

| Rank | Candidate | Novelty | Tractable as code? | Defensible falsifiable result? | Verdict |
|---|---|---|---|---|---|
| 1 (least bad) | **A** — partial-g microbial/biofilm | Low | Yes (easy) | No, as framed | **Reject as framed; salvageable via inversion** |
| 2 | **B** — combined-stressor flammability | Low | Yes (trivial) | No — premise false | **Reject** |
| 3 | **C** — fractional-g two-phase | Low | No (needs CFD + data) | No — 2004 prior art | **Reject** |

**None of the three finalists survives scrutiny as framed.** I want to be explicit about that rather than rank-order three rejects and let the top of the list read as an endorsement. All three failed for the same structural reason: the Haiku surveys inferred novelty from *absence of hits in NTRS/ICES-scoped searches*, and in each case the disqualifying prior art sits just outside that scope — in ASME/Elsevier heat-transfer journals (C), in WSTF materials-testing reports and NESC bulletins (B), and in the astrobiology/microbiology literature and bioRxiv (A). This is exactly the failure mode the integrity rule about absence-of-evidence was written to catch, and the register's own §1.3 caveat was correct but under-weighted.

---

## 5. Recommendation

### Primary: **Candidate A, inverted** — "When does gravity actually matter? A dimensionless criterion for microbial and biofilm processes in engineered partial-gravity ECLSS water loops."

Do **not** build a gravity-scaled kinetics model that predicts a partial-gravity effect. Build the model that determines **whether there is one worth designing for**, and publish the criterion.

Why this survives when Candidate A does not:
- **It is enabled by the prior art rather than blocked by it.** Gesztesi's 5.04 mm depletion-zone radius (A-3), Latham's two-opposing-mechanisms decomposition (A-1), the BioRock null result (A-4) and the strain-dependent clinostat data (A-5) become *inputs and validation targets*, not competitors. The contribution is the synthesis nobody has done.
- **The contribution form is well-precedented and respected.** Konishi/Mudawar/Hasan's "criteria for negating the influence of gravity" (C-4) is exactly this move, and it is a landmark in the two-phase field. The identical move has never been made on the microbial/biofilm side of ECLSS. Borrowing a proven contribution *form* across domains is legitimate and is the strongest position available here.
- **The falsifiable claim is sharp and defensible without new facilities.** Concretely: compute, for representative ISS/exploration WPA, UPA and MABR operating points, the ratio of gravity-driven transport (Stokes sedimentation velocity ∝ g; buoyancy-convection velocity ∝ g) to forced-advection and wall-shear transport, expressed as a Péclet/Richardson-type criterion. Predict the g-threshold below which gravity-driven terms are second-order. The falsifiable output is a **quantitative boundary in (flow rate, channel dimension, cell/floc size, g) space** separating "gravity matters" from "gravity is negligible," validated against the published datasets above.
- **It has a real, useful answer either way.** If the criterion says gravity is negligible in pumped loops, that de-risks lunar/Mars WRS qualification and directly serves the Carlson/Lange/Callahan partial-gravity WRS modeling line (ICES-2024-323) and the mECLSS aeration work (ICES-2025-49) — a genuinely welcome result at ICES. If it says gravity matters in specific stagnant regions (dormancy, tank ullage, dead legs, filter housings), that is a *targeted* design finding far more valuable than a global scaling law, and it maps onto NASA's own stated dormancy concern.
- **It is honest about the null.** A null result presented as a criterion is publishable; a null result presented as a failed prediction is not.

**Tractability: high.** Pure Python. Dimensional analysis plus a modest 1-D advection-diffusion-reaction model of a biofilm-lined channel with a gravity-dependent transport term. No centrifuge, no parabolic flight, no bench culture required — though the optional 1 g bench culture from the original scoping still fits as a sanity check. Bounded at a single-paper effort.

**Named risk to novelty, stated up front:** Latham et al. (A-1) is a preprint I could not read. If it already contains a partial-gravity sweep and a regime criterion, the inverted candidate is substantially weakened. **Reading that preprint's full text is the single highest-priority action before committing.** It is a blocking gate, not a nice-to-have.

### Fallback if the inversion is judged too derivative: **gap_register row 11 — mineral scale/precipitation prediction for Mars regolith/ISRU-sourced makeup water** (N7/T8/R7).

Rationale: it is the highest-tractability row whose underlying physics is *not* gravity-dependent in a contested way — it is well-posed aqueous thermodynamics. PHREEQC is free, mature, and scriptable; the falsifiable claim (predicted saturation indices and precipitation onset vs. concentration ratio for regolith-derived feed chemistry) is clean.

**This fallback is UNVETTED.** I ran only one adversarial search on it. That search already found partial occupancy: NASA's "Process Control for Precipitation Prevention in Space Water Recovery Systems" (NTRS 20150000527) [verified-existence], and a five-stage urine/shower-water treatment train for long-duration missions that used a steady-state water balance **complemented with PHREEQC v3 speciation modeling** to control scaling potential (*Desalination*, 2020) [verified-existence, snippet-level content]. The specifically-Martian ISRU-makeup-water variant did not appear pre-empted, but one search is not due diligence. **Row 11 requires its own full adjudication pass before selection.**

---

## 6. Confidence and biggest risk

**Confidence that the recommended problem yields a genuine, single-paper ICES contribution: MEDIUM.**

Justification for not saying high: the recommendation is a reframe I constructed during adjudication rather than a candidate that survived it, so it has not itself been through a full adversarial cycle; and I was unable to read a single full text, including the one preprint (A-1) most likely to pre-empt it. Justification for not saying low: the contribution form is proven in an adjacent field, the tractability is genuinely high with no facility dependency, the validation targets exist and are published, and the result is useful and publishable in both the positive and null branches.

**Single biggest risk:** that the gravity-relevance criterion resolves to a trivially large margin — that forced advection in every realistic ECLSS operating point exceeds gravity-driven transport by three or more orders of magnitude, making the criterion true but uninteresting, and the paper reads as "we confirmed the obvious with dimensional analysis." The mitigation is to scope the work from the outset around the *stagnant* regimes where the margin is genuinely narrow and the answer is genuinely unknown — dormancy periods of up to a year, tank ullage, dead legs, filter housings, and post-shutdown restart transients — since that is where the criterion has to do real work and where NASA has an acknowledged open concern. If early dimensional analysis shows the margin is wide even in stagnant regimes, abandon the inversion and fall back to row 11 rather than writing the trivial paper.

---

## 7. Recommended immediate next actions

1. **Blocking gate:** obtain and read the full text of Latham, Skountzos & Lawson, bioRxiv 2026.05.15.725518. Determine whether it contains a partial-gravity sweep or a regime criterion. This requires network access the current sandbox does not have — the proxy must be allowlisted for `biorxiv.org`, or the PDF supplied out of band.
2. Also read at full text, in priority order: CAMDLES (*Life* 2022, 12:660); Gesztesi et al. (*Front. Microbiol.* 14:1155726); Santomartino et al. BioRock (*Front. Microbiol.* 11, 2020). These four determine whether the inversion is novel.
3. Request proxy allowlisting for `ntrs.nasa.gov`, `sciencedirect.com`, `nature.com`, `mdpi.com`, `pmc.ncbi.nlm.nih.gov`, `biorxiv.org`, `ices.space` before any further novelty work. **The Phase 1 surveys were conducted under this same restriction, which is a plausible contributing cause of all three finalists' novelty failures** — and it means the rest of `gap_register.md` carries the same unquantified risk.
4. Do not write `problem_statement.md` until action 1 clears.
