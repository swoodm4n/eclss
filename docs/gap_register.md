# ECLSS Gap Register

Consolidated from 8 independent subsystem literature surveys (`/lit/notes/*.md`), each conducted by a separate Haiku subagent using real searches against NASA NTRS, ICES/TTU proceedings, arXiv, and NASA technical standards. 44 candidate gaps were identified in total. This document scores and ranks them, and flags a cross-cutting pattern that emerged independently across surveys.

Scoring: each subsystem agent scored its own gaps 1-10 on Novelty, Tractability, Relevance, using its own judgment — scores are **not** independently calibrated across agents, so they are directional within a subsystem, not strictly comparable across subsystems. Overall column is the agent's own average unless noted.

## Cross-cutting observation (not visible to any single subsystem agent)

Four of eight subsystem surveys — run independently, in parallel, with no visibility into each other's output — converged on **microbial/biofilm dynamics under partial gravity or mission-variable conditions** as a top-scoring gap:

| Subsystem | Gap | Score |
|---|---|---|
| Water recovery | Gap 1: Biofilm prediction & adaptive control under mission-variable conditions | 8/10 |
| Water recovery | Gap 6: In-situ optical biomarkers for real-time biomass quantification | 8/10 |
| Waste management | Gap 1: Quantitative microbial dynamics modeling for waste decomposition in variable gravity | N8/T7/R9 |
| System integration | Gap 3: Autonomy & fault tolerance in water recovery during biofilm transients | N8/T8/R9 |
| Monitoring/fault detection | Gap 1: Real-time autonomous biofilm detection without Earth-return analysis | N7/T6/R9 |

This convergence is itself evidence worth weighing two ways: (a) it signals a real, recognized, high-relevance problem — not an artifact of one agent's narrow reading; (b) it's also a space NASA is *actively* publishing in as of 2025 (e.g. "A Modeling Study on Microbial Growth for the ISS Wastewater Process System: An Update," ICES-2025-406; "Correlation Between the Historical ISS WRS Microbial Data and the Corresponding Water Chemical Analysis Data," ICES-2025), which raises the novelty bar — a submission here must clearly differentiate from that active line of work. The one dimension every survey flagged as *actually* open, consistently, is that all existing models are calibrated to ISS conditions (microgravity or historical 1g ground testing) — none address **partial-gravity (lunar 1/6 g, Mars 0.38 g) microbial kinetics**, which is where the gap concentrates. Noted here as weak-but-consistent evidence per integrity rule §1.3 — absence of hits across 4 independent searches is suggestive, not proof.

## Full gap table (all 8 subsystems)

| # | Subsystem | Gap | Novelty | Tractability | Relevance | Overall |
|---|---|---|---|---|---|---|
| 1 | Atmosphere revitalization | Gas-liquid phase separation for liquid-amine CO2 removal under microgravity/partial-g | 8 | 6 | 9 | 7.7 |
| 2 | Atmosphere revitalization | Sorbent cyclic regeneration under competitive water-CO2 adsorption | 6 | 8 | 7 | 7.0 |
| 3 | Atmosphere revitalization | Humidity-CO2 coupled single-unit sorbent materials | 7 | 7 | 7 | 7.0 |
| 4 | Atmosphere revitalization | OGA partial-gravity electrolysis (bubble dynamics) | 6 | 5 | 7 | 6.0 |
| 5 | Atmosphere revitalization | TCC adaptation to partial-gravity off-gassing profiles | 6 | 6 | 6 | 6.0 |
| 6 | Atmosphere revitalization | Sabatier/Bosch thermal control under transient crew load | 6 | 7 | 6 | 6.3 |
| 7 | Water recovery | Biofilm prediction & adaptive control under mission-variable conditions | 7 | 8 | 9 | 8.0 |
| 8 | Water recovery | Real-time multi-parameter feedback control (biocide/pH) | 8 | 7 | 9 | 8.0 |
| 9 | Water recovery | Unified thermal-hydraulic VCD modeling, transient + partial-g | 8 | 6 | 8 | 7.0 |
| 10 | Water recovery | Integrated multi-stream recovery (urine+fecal+greywater) w/ on-demand polishing | 9 | 7 | 9 | 8.0 |
| 11 | Water recovery | Mineral scale/precipitation prediction (Mars regolith water chemistry) | 7 | 8 | 7 | 7.0 |
| 12 | Water recovery | In-situ optical biomarkers for real-time biomass quantification | 8 | 9 | 8 | 8.0 |
| 13 | Waste management | Microbial dynamics modeling for decomposition in variable gravity | 8 | 7 | 9 | 8.0 |
| 14 | Waste management | Odor breakthrough prediction vs. compaction state | 7 | 8 | 8 | 7.7 |
| 15 | Waste management | Particle settling/segregation under partial gravity during compaction | 8 | 7 | 9 | 8.0 |
| 16 | Waste management | Real-time brine residual moisture sensing/control | 7 | 7 | 7 | 7.0 |
| 17 | Waste management | Multi-stream synergistic resource recovery optimization | 8 | 6 | 8 | 7.3 |
| 18 | Waste management | Halophilic microbial conversion of brine residual | 9 | 6 | 7 | 7.3 |
| 19 | Thermal control | Gravity-dependent two-phase heat transfer correlations | 7 | 6 | 8 | 7.0 |
| 20 | Thermal control | Passive regolith+PCM TES for lunar night — validation/scale-up | 8 | 7 | 8 | 7.7 |
| 21 | Thermal control | MPTL startup/transient anomaly suppression | 6 | 6 | 7 | 6.3 |
| 22 | Thermal control | Integrated thermal-structural radiator topology optimization | 7 | 8 | 6 | 7.0 |
| 23 | Thermal control | Adaptive radiative cooling surface materials | 8 | 6 | 6 | 6.7 |
| 24 | Thermal control | Lunar-night hybrid active-passive TES + heater control strategy | 7 | 8 | 8 | 7.7 |
| 25 | Food/bioregenerative | Crop physiology under combined lunar gravity (1/6g) + reduced pressure | 9 | 7 | 9 | 8.3 |
| 26 | Food/bioregenerative | Real-time nutrient-drift detection/control under altered gravity | 8 | 8 | 8 | 8.0 |
| 27 | Food/bioregenerative | Seed production & multigenerational viability under reduced gravity | 9 | 6 | 9 | 8.0 |
| 28 | Food/bioregenerative | Mars-gravity (0.38g) crop physiology & yield projections | 9 | 7 | 8 | 8.0 |
| 29 | Food/bioregenerative | Integrated plant+algae+microbial system model under variable gravity | 7 | 8 | 8 | 7.7 |
| 30 | Food/bioregenerative | LED spectrum optimization for RUE/nutrition under power constraints | 6 | 9 | 7 | 7.3 |
| 31 | Fire safety | Material flammability envelope under combined O2/pressure/gravity | 8 | 7 | 9 | 8.0 |
| 32 | Fire safety | Partial-gravity flame spread prediction | 8 | 6 | 9 | 7.7 |
| 33 | Fire safety | Cool-flame detection & characterization | 9 | 5 | 8 | 7.3 |
| 34 | Fire safety | Multi-contaminant post-fire atmosphere recovery | 7 | 7 | 8 | 7.3 |
| 35 | Fire safety | Smoke/particulate 3D distribution mapping in variable gravity | 7 | 6 | 7 | 6.7 |
| 36 | Fire safety | Suppression agent efficacy across gravity regimes | 8 | 4 | 8 | 6.7 |
| 37 | Monitoring/fault detection | Real-time autonomous biofilm detection w/o Earth-return | 7 | 6 | 9 | ~7.3 |
| 38 | Monitoring/fault detection | Long-duration sensor degradation & adaptive drift compensation (partial-g) | 8 | 8 | 8 | 8.0 |
| 39 | Monitoring/fault detection | Hybrid physics-ML fault diagnosis for CO2 removal under radiation-corrupted sensors | 7 | 7 | 8 | 7.3 |
| 40 | Monitoring/fault detection | Digital twin fidelity assessment/validation framework for ECLSS | 8 | 6 | 9 | 7.7 |
| 41 | Monitoring/fault detection | Unsupervised anomaly detection for off-nominal regimes, no ground truth | 7 | 7 | 8 | 7.3 |
| 42 | Monitoring/fault detection | Radiation-hardened fault detection architecture | 9 | 5 | 9 | 7.7 |
| 43 | System integration | Cross-subsystem interaction modeling for autonomous ECLSS | 8 | 7 | 9 | 8.0 |
| 44 | System integration | Lunar dust ingestion: system-level characterization & mitigation | 9 | 6 | 9 | 8.0 |
| 45 | System integration | Autonomy/fault tolerance in water recovery during biofilm transients | 8 | 8 | 9 | 8.3 |
| 46 | System integration | Integrated thermal-atmospheric coupling in partial-gravity architectures | 7 | 7 | 8 | 7.3 |
| 47 | System integration | Optimal redundancy architecture / fault-tolerance trade study | 6 | 8 | 8 | 7.3 |
| 48 | System integration | System-level validation of autonomous ECLSS in integrated analog | 5 | 6 | 10 | 7.0 |

## Top candidates carried to Phase 2 novelty adjudication

Selected for diversity of domain (not just top score) and for genuinely open novelty per the evidence in `/lit/notes/`, plus fit to "modeling contribution, with at most a modest bench test" per program scoping (§5):

1. **Partial-gravity microbial/biofilm kinetics for ECLSS water & waste systems** (synthesizes rows 7, 12, 13, 15, 37, 45) — highest cross-survey convergence; real open gap is specifically the gravity-dependence of kinetics, since existing 2025 NASA models are calibrated to ISS-only conditions. Modeling approach: population-dynamics ODEs with gravity-scaled sedimentation/mass-transfer terms, validated at 1g on a bench culture (hobbyist-tractable), extrapolated to partial-g via first-principles scaling with uncertainty bounds — partial-g bench validation flagged as optional future work requiring centrifuge access.

2. **Combined-stressor material flammability envelope for exploration habitats** (row 31, score 8.0, single highest individual score in the register) — existing NASA/NIST data is single-factor (O2 only, or pressure only); no combined-factor predictive model exists for the actual planned habitat envelope (Lunar Gateway 26.5% O2/73.5 kPa; lunar surface up to 34% O2/56.5 kPa). Modeling approach: regression/semi-empirical combination model fit to existing published single-factor data sets, cross-validated against sparse combined-condition data where it exists in the literature.

3. **Fractional-gravity two-phase heat/mass-transfer scaling correlations** (synthesizes rows 1, 19, 24) — spans thermal control and atmosphere revitalization; both ultimately reduce to the same open physics problem (two-phase flow behavior between the well-characterized 1g and 0g limits, with no validated fractional-g correlation). ISS's FBCE experiment is actively generating 0g data but explicitly has not yet produced "gravity-independent design criteria." Modeling approach: CFD/analytical scaling law bridging published 1g and 0g correlations via a Bond/Froude-number interpolation, checked against any available parabolic-flight fractional-g data points in the literature.

Runners-up not advanced (for the record): integrated multi-stream water recovery (row 10, high score but primarily a systems-engineering integration exercise rather than a research question with a falsifiable model); crop physiology under lunar gravity+pressure (row 25, highest single score at 8.3, but requires a centrifuge+pressure-chamber facility that is less certain to be modeling-first-tractable than the three selected); lunar dust ingestion (row 44, high score, but scope is closer to a systems trade study than a bounded single-paper contribution).
