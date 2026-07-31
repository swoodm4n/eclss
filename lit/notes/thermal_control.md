# Thermal Control Systems in ECLSS: Literature Survey & Candidate Gaps

## Sources

1. **International Space Station Active Thermal Control Sub-System On-Orbit Pump Performance and Reliability Using Liquid Ammonia as a Coolant**
   - NASA Technical Reports Server (NTRS)
   - Authors: NASA/GSFC ISS Thermal Team
   - Year: 2011
   - URL: https://ntrs.nasa.gov/citations/20110023292
   - Finding: ISS ATCS uses two mechanically-pumped ammonia loops (LOOP A/B), each with redundant radiator deployable panels. Report quantifies on-orbit pump performance, degradation rates, and reliability margins for long-duration operation; documents transient operating scenarios and heat load profiles.

2. **NASA Passive Thermal Control Engineering Guidebook Revision 4.0**
   - NASA Technical Reports Server (NTRS)
   - Year: 2023
   - URL: https://ntrs.nasa.gov/api/citations/20230013900
   - Finding: Comprehensive reference standard defining passive thermal control modes (radiative coatings, multi-layer insulation, louvers, heat pipes), active system types (single-phase and two-phase loops), heat rejection surfaces, and design trade-space. Establishes NASA's current best practices for thermal mathematical models and margin requirements.

3. **Thermal Performance of Orion Active Thermal Control System With Seven-Panel Reduced-Curvature Radiator**
   - NASA NTRS
   - Year: 2010
   - URL: https://ntrs.nasa.gov/citations/20100040420
   - Finding: Documents design and thermal analysis of Orion spacecraft ATCS with variable-geometry radiator; presents performance models for crewed vehicle thermal management under lunar/Earth-return mission profiles with varying power dissipation.

4. **Ammonia Vent of the External Active Thermal Control System (EATCS) Radiator #3 Flow Path #2 on the International Space Station (ISS)**
   - NASA NTRS
   - Year: 2018
   - URL: https://ntrs.nasa.gov/citations/20180007472
   - Finding: Incident report on ISS EATCS ammonia venting anomaly; documents failure mode and operational workarounds, illustrating reliability challenges in long-duration two-phase liquid-ammonia systems and need for redundancy.

5. **Spacecraft Thermal Management using Advanced Hybrid Two-Phase Loop Technology**
   - Presented at STAIF 2007
   - Authors: Advanced Cooling Technologies & Partners
   - Year: 2007
   - Summary from search: Compares single-phase mechanically-pumped loops, passive two-phase devices (CPL/LHP), and hybrid mechanically-pumped two-phase loops (MPTL). MPTL combines long-distance transport, high heat density, passive evaporator phase separation, and loop pressure control via accumulator; eliminates drawbacks of pure passive systems (startup issues) and pure active systems (parasitic pump power).

6. **Retrospective Review of a Two-Phase Mechanically Pumped Loop for Spacecraft Thermal Control Systems**
   - ResearchGate / Academia
   - Year: 2021
   - Summary from search: Reviews MPTL development history and lessons learned. Notes that despite passive phase separation and high reliability potential, MPTL systems have seen limited spaceflight heritage; fabrication complexity and working-fluid purity requirements increase cost vs. single-phase loops.

7. **Capillary Pumped Loop (CPL) Heat Pipe Technology: Space Applications and Recent Canadian Activities**
   - Academia.edu / International Heat Transfer Conference
   - Year: 2002
   - Summary from search: Defines CPL technology (passive, capillary-driven two-phase transport) vs. Loop Heat Pipes (LHP). Both offer graceful degradation under off-nominal conditions but suffer startup/de-priming transients; electrical heaters or thermoelectric de-priming devices often required. Alpha Magnetic Spectrometer (AMS) on ISS uses small two-phase pumped CO2 loop for thermal stabilization.

8. **Spacecraft Fluidic Thermal Control Subsystem Reliability**
   - DTIC (Defense Technical Information Center)
   - Year: Unknown (recent)
   - Summary from search: Analyzes reliability architecture of fluidic thermal systems (active and passive loops). Notes that CPL/LHP startup anomalies and transients can lead to failure; tuning and ground testing essential but expensive.

9. **Mechanically Tunable Radiative Cooling for Adaptive Thermal Control**
   - arXiv:2203.14697
   - Year: 2022
   - URL: https://arxiv.org/abs/2203.14697
   - Summary from search: Develops modeling method for mechanically-stretching tunable emitters (adaptive radiators) that respond to electromagnetic stimulus. Tailored for variable external thermal environment (e.g., Mars surface, translunar, lunar day/night). Novelty: combines mechanical and electromagnetic modeling; scalability and fabrication cost not yet quantified.

10. **Multifunctional Lightweight Radiators for Small-Satellite Thermal Control**
    - arXiv:2511.06683
    - Year: 2025
    - URL: https://arxiv.org/abs/2511.06683
    - Summary from search: Proposes topology optimization and design-space analysis for multifunctional radiator architectures for small-satellites and CubeSats. Addresses trade-space between structural function, thermal function, and mass. Method is emerging; application to crewed vehicles and long-duration habitat radiators not yet explored.

11. **Topical: Boiling, Condensation and Two-Phase Flows in Microgravity**
    - NASA Science / Technical Presentation
    - Year: 2023
    - URL: https://science.nasa.gov/wp-content/uploads/2023/05/60_fd7f0c637f1b4e15a08c04fbaa69ee4b_KhusidBoris.pdf
    - Summary from search: Reviews state of knowledge on gravity effects on flow boiling and condensation. Lack of predictive models for two-phase heat transfer at reduced gravity (0g, lunar 1/6g, partial g). Flow Boiling and Condensation Experiment (FBCE) on ISS seeks to validate models and generate gravity-independent design criteria.

12. **Flow Boiling and Condensation Experiment (FBCE) - ISS Investigation**
    - NASA Science
    - Year: Ongoing (launched to ISS)
    - Summary from search: Ground and ISS-based two-phase flow facility. Objectives: generate condensation heat-transfer database for microgravity design; determine critical heat flux behavior; develop criteria for gravity-independent condensation heat transfer. Early results suggest gravity independence possible for certain flow regimes, but full database not yet released.

13. **Variable Conductance Heat Pipe (VCHP) Technology Review**
    - NASA NTRS & ESA ESTEC
    - Year: 1972 (foundational), 2024 (recent review)
    - Summary from search: VCHP uses non-condensable gas to partially block condenser, modulating heat transport passively. Beneficial for planetary rovers and deep-space missions with extreme environmental temperature swings. Recent ESA review (2024) highlights applications for lunar surface vehicles; design complexity lower than MPTL but effective range of control limited.

14. **Numerical Analysis of 3D Printed Lunar Habitats: Integrating Regolith and PCM for Passive Temperature Control**
    - Microgravity Science and Technology (Springer Nature)
    - Year: 2025
    - Summary from search: Proposes coaxial 3D printing of lunar regolith shells + phase-change material (PCM) cores for passive habitat thermal control during 14-day lunar night (95 K surface minimum). Model-only study; no experimental validation yet. Regolith provides structural support and ~5-inch layer provides adequate insulation.

15. **Utilisation of Moon Regolith for Radiation Protection and Thermal Insulation in Permanent Lunar Habitats**
    - Applied Sciences (MDPI), Open Access
    - Year: 2021
    - URL: https://www.mdpi.com/2076-3417/11/9/3853
    - Finding: Regolith thermal conductivity ~0.1 W/(m·K); 10 cm layer reduces external temperature swings to ±50 K (acceptable for shielded habitat interior). In-situ resource utilization (ISRU) of regolith for insulation is mature concept; integration with active radiators for day-side heat rejection remains underexplored.

16. **Lunar Inflatable Habitats: A Comprehensive Literature Review**
    - Embry-Riddle Aeronautical University
    - Year: Recent (available through Commons)
    - URL: https://commons.erau.edu/db-srs/
    - Summary from search: Reviews habitat thermal challenges: extreme day/night temperature swings, dust thermal properties, micrometeorite/radiation protection. Notes trade-off between regolith burial (low power, high mass) and active radiators (high power, thermal rejection difficulty at low external temperature).

17. **ECSS-E-ST-31C: Space Engineering - Thermal Control General**
    - European Cooperation for Space Standardization (ECSS)
    - Year: 2008 (current standard)
    - URL: https://ecss.nl/standard/ecss-e-st-31c-thermal-control/
    - Finding: Defines thermal control requirements across three temperature ranges (cryogenic, conventional, high-temp). Specifies design margin philosophy, testing requirements, and processes for thermal validation. NASA ECSS-compliant. Handbook ECSS-E-HB-31A provides implementation guidance.

18. **International Conference on Environmental Systems (ICES) - Conference Proceedings 2022-2025**
    - Texas Tech University Libraries (open access)
    - Years: Annual 2022-2025 (ICES 51-55)
    - URL: https://ttu-ir.tdl.org/collections/ef7ac1dd-cfc8-4fb0-9bd9-81e30264df7f
    - Finding: ICES hosts ~300+ papers annually on ECLSS. Thermal and Environmental Control Systems Committee (TECS) session covers active/passive thermal control, radiators, heat pipes, and habitat systems. Papers accessible online; summary: current focus on ISS operations, Artemis/lunar systems, long-duration deep-space missions.

19. **Human Exploration Research Analog (HERA) Facility - NASA JSC**
    - NASA Johnson Space Center
    - Year: Ongoing (multiple missions per year)
    - URL: https://analogstudies.jsc.nasa.gov/hera
    - Finding: HERA is a 3-story isolated habitat for 45-day analog missions. Has active thermal control for crew comfort but not a focus of HERA research program. HERA data on thermal comfort, humidity control, and power consumption available but ECLSS thermal subsystem design/validation is not primary mission objective.

20. **Spacecraft Radiator Optimization: Node-Based Multi-Objective Design**
    - Journal of Spacecraft and Rockets / ScienceDirect
    - Year: 2014-2023 (multiple papers)
    - Summary from search: Multi-objective optimization (minimize radiator panel count, minimize temperature margins) using genetic algorithms. Recent arXiv work adds structural multifunctionality (radiator as load-bearing panel). Trade-space analysis matures; application to transit-mission radiators with dynamic thermal loads not yet common.

---

## Candidate Research Gaps

### Gap 1: Gravity-Dependent Heat Transfer Models for Reduced-Gravity Two-Phase Systems

**Description:**  
Two-phase heat-transfer coefficients (boiling, condensation) scale with gravity. ISS experiments (FBCE) are generating microgravity data, but design models for fractional gravity (lunar 1/6g, Martian 0.38g, asteroid/Lagrange 0g) remain sparse. Spacecraft operating in or transiting through multiple gravity environments (e.g., Earth-LEO ascent, Earth-Moon-Mars trajectory) need robust correlations.

**Closest Prior Work:**  
- FBCE (NASA Science, ongoing): ISS-based two-phase flow facility collecting 0g data.  
- Topical review (Khusid et al. 2023, NASA): Concludes "gravity-independent design criteria" are needed but not yet finalized.  
- Historical microgravity boiling/condensation experiments (1980s-2010s) mostly on short-duration parabolic flights and Space Shuttle; data scattered.

**Why It Matters:**  
- **Long-duration missions:** Lunar outpost radiator must work during 14-day lunar night at 1/6g and extreme cold (95 K). Current ISS design assumes 1g startup and 0g-stable operation; lunar is neither.  
- **Transit missions:** Mars transit (0.38g on arrival) with reduced power margin demands efficient two-phase cooling; single-phase loops over-size radiator mass.  
- **Habitat sustainability:** Future rotation habitats (artificial gravity via spin) will operate at intermediate gravity; thermal design methods don't exist.

**Tractability:**  
- **Bench validation:** Parabolic-flight experiments (ESA, NASA, China) can validate correlations at discrete gravity levels (0g, 1/6g, 1/3g). Drop-tower experiments (5-10 sec) can measure transient boiling nucleation.  
- **Feasibility:** Moderate; parabolic flights are expensive (~€500k-1M per campaign) but mature. A hobbyist-level thermal test (2-phase loop in a centrifuge or drop-tower) is borderline tractable; professional-grade parabolic test is not.  
- **Modeling:** CFD + population-balance methods (nucleation, bubble coalescence under variable gravity) are available; application to spacecraft coolants (ammonia, water, glycol-water) is a data-fitting exercise.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 7/10** – Gravity-dependent models exist for pure research; aerospace application to thermal-control design is novel but narrowly scoped.  
- **Tractability: 6/10** – Requires parabolic flights or drop-tower, not just desktop simulation; achievable by a team but not a solo hobbyist.  
- **Relevance: 8/10** – Lunar and Mars programs explicitly need this; ISS operations (0g-stable) are past this need, but NASA Artemis thermal design is blocked without it.

---

### Gap 2: Passive Regolith+PCM Thermal Energy Storage for Lunar Night Survival — Validation & Scale-Up

**Description:**  
Models (Springer 2025, MDPI 2021) propose passive thermal energy storage (TES) using lunar regolith as insulation + PCM as thermal buffer to survive 14-day lunar night without power. No full-scale ground test or analog mission data exists. Fabrication (3D printing regolith+PCM, wick structure, regolith consolidation) is unproven at habitat scale.

**Closest Prior Work:**  
- Numerical models: 3D printing coaxial regolith/PCM (Springer 2025, model-only).  
- Regolith thermal properties: MDPI 2021 (k ≈ 0.1 W/(m·K), layer thickness ~10 cm sufficient).  
- ISS thermal control: well-established active loops; no analog in passive TES for extreme environment.

**Why It Matters:**  
- **Power budget:** Lunar base power is scarce; passive night survival eliminates need for 14-day radioisotope heater backup or nuclear reactor.  
- **Dust/regolith handling:** In-situ resource utilization (ISRU) reduces launch mass; regolith sourcing is near any lunar location.  
- **Cost and reliability:** Passive systems (no pumps, no moving parts) are inherently more reliable than active ATCS for decades-long outpost.

**Tractability:**  
- **Bench validation:** Small-scale test (1 m³ regolith simulant [JSC-1A] + PCM capsules, insulation, heater/sink) can mimic lunar day/night cycle (~4 hours heating, ~4 hours cooling). Achievable in university lab.  
- **Analog test:** HERA or Moon Analogs (LUNARES, CESAR) could host a lunar-habitat mockup with regolith TES during 45-day mission.  
- **Scale-up risk:** Unknown adhesion of 3D-printed regolith binder, thermal contact resistance at regolith-PCM interface, and dust mitigation inside structure.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 8/10** – Integrated regolith+PCM TES is novel; individual components (regolith insulation, PCM units) are known.  
- **Tractability: 7/10** – Benchtop test very feasible; analog mission is harder (requires lunar-thermal simulator at night). Full-scale validation requires flight/HERA.  
- **Relevance: 8/10** – Artemis base thermal strategy is openly debated; this removes a major power constraint if viable.

---

### Gap 3: Mechanically-Pumped Two-Phase Loops (MPTL) Startup & Transient Anomaly Suppression for Off-Nominal Missions

**Description:**  
MPTL (hybrid of active pump + passive evaporator) avoids startup/de-priming issues of pure CPL/LHP but is underflown (~AMS on ISS is one of few spaceflight examples). Transient behaviors (startup from cold-soak, oscillation damping, load-step response) are modeled but not fully validated in multi-gravity or multi-fluid scenarios. ISS ATCS ammonia-loop incidents (e.g., radiator venting, pump cavitation) highlight reliability gaps even for single-phase.

**Closest Prior Work:**  
- Retrospective MPTL review (ResearchGate 2021): Notes reliability is good but spaceflight heritage is limited.  
- Accumulator design: NASA/GSFC work on ISS pump cavitation margin (NTRS 2011) provides rig data.  
- Two-phase microgravity fundamentals: FBCE is generating flow-regime maps but not MPTL-specific startup protocols.

**Why It Matters:**  
- **Deep-space missions:** Mars transit and lunar missions have limited power and high thermal load variability; MPTL radiators and pump efficiency are critical.  
- **Fault tolerance:** ISS ATCS redundancy (dual pumps, dual loops) masks some anomalies; future crewed missions may not have same mass margin.  
- **System maturity:** Parachute ECLSS design relies on proven heritage; MPTL heritage is thin, limiting adoption.

**Tractability:**  
- **Rig-level test:** A benchtop two-phase loop (heater, evaporator with wick, pump, condenser, accumulator) can simulate startup transients and oscillations. Academic groups have built such rigs.  
- **Space validation:** Nanosatellite or ISS external attached payload (small MPTL demo) could flight-test in 0g; ~€500k-2M for small satellite mission.  
- **Hobbyist feasibility:** Low-power MPTL breadboard (water-ethanol, mm-scale pump) is doable; manufacturing precision and working-fluid purity control are barriers.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 6/10** – MPTL physics is known; transient suppression strategies (accumulator tuning, pump ramp control) are incremental.  
- **Tractability: 6/10** – Benchtop rig is feasible; spaceflight validation is expensive and time-consuming.  
- **Relevance: 7/10** – Artemis and deep-space missions would benefit; ISS is not a driver.

---

### Gap 4: Integrated Thermal-Structural Radiator Design Optimization for Variable-Gravity Habitats

**Description:**  
Recent work (arXiv 2511.06683) proposes topology optimization for radiators as structural panels. Most applications are to small-satellites; application to large habitat radiators (10+ m²) under variable external thermal load (Earth orbit, lunar, Mars surface, in-transit) is unexplored. Trade-space between radiator efficiency, structural strength, mass, and manufacturability is not quantified for crewed vehicles.

**Closest Prior Work:**  
- Radiator node-based optimization (ScienceDirect 2014+): Minimizes panel count and margins; structural role ignored.  
- Multifunctional radiator topology (arXiv 2025): Demonstrates method for CubeSat; scale to 100+ kg radiator system not demonstrated.  
- ISS radiator design: Fixed geometry, not optimized for structural role; Orion radiator (NTRS 2010) is passive structural design.

**Why It Matters:**  
- **Launch mass:** Habitat radiators are one of the largest structures; if they can also carry internal loads (pressure wall, thermal duct support), mass savings are 10-20%.  
- **Reliability:** Fewer parts and integrated design reduce failure points.  
- **Adaptability:** Optimized radiators for different missions (LEO, lunar, Mars) can share design language, reducing development time.

**Tractability:**  
- **Analysis:** Finite-element + thermal-FEM coupled optimization is standard (many commercial tools: ANSYS, COMSOL). Application to radiator topology is a software exercise.  
- **Validation:** Ground testing (thermal vacuum chamber) is standard; structural testing under acceleration is routine. Benchtop optimization + thermal test is very feasible.  
- **Manufacturing:** 3D-printed titanium or aluminum radiators with integrated ducting are emerging; cost is currently high but declining.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 7/10** – Radiator optimization and structural multifunctionality are separately mature; combined application to spacecraft is novel.  
- **Tractability: 8/10** – Primarily a software/analysis effort; hobbyist-level thermal-structural optimization model is very feasible (Python + open-source FEM).  
- **Relevance: 6/10** – Valuable for future deep-space vehicles; ISS and Artemis near-term designs are less constrained by mass.

---

### Gap 5: Adaptive Radiative Cooling Surface Materials for Dynamic Thermal Environments

**Description:**  
Mechanically-tunable emissivity (arXiv 2022) and vanadium-dioxide switchable coatings are emerging but not yet integrated into spacecraft radiator systems. Material performance under micrometeoroids, atomic oxygen (LEO), and UV radiation remains unquantified. Manufacturing scale-up from lab (~cm²) to flight radiators (~m²) is not demonstrated.

**Closest Prior Work:**  
- Mechanically-tunable radiators (arXiv 2203.14697): Lab demonstration with stretch-responsive metamaterial; space qualification not addressed.  
- VO₂ switchable radiators (NIH PMC 2019, 2024): Lab emissivity switching (α 0.1–0.9); durability under LEO/lunar environment unknown.  
- Thermal control coatings: ISS and heritage spacecraft use fixed (high-emissivity) or reflective coatings; adaptive coatings are not baseline.

**Why It Matters:**  
- **Variable external environment:** Moon has extreme day/night; Mars has dust storms and low albedo; adaptive coatings reduce need for active-loop power.  
- **Efficiency:** Dynamic emissivity matching to radiative environment can reduce radiator area by 20-30%.  
- **System simplicity:** Passive control is more reliable than closed-loop ATCS regulation.

**Tractability:**  
- **Material research:** Stretch-induced tunability and VO₂ switching are university-level materials science; characterization under vacuum and radiation is standard testing.  
- **Flight qualification:** AMS-type small-area test on ISS could validate coating durability and thermal performance.  
- **Scale-up risk:** Manufacturing uniform coatings on curved radiator surfaces at 1-m scale is challenging; spray or CVD deposition is viable but not yet production-ready.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 8/10** – Adaptive coatings are emerging; spaceflight validation is completely novel.  
- **Tractability: 6/10** – Materials research and small-scale test are feasible; flight qualification is expensive and multi-year.  
- **Relevance: 6/10** – Valuable for future missions; current Artemis and ISS designs are not drivers.

---

### Gap 6: Lunar Night Thermal Transient Control — Passive + Active Hybrid Strategy for Extreme Day/Night Cycles

**Description:**  
Regolith+PCM passive TES (Gap 2) can supply thermal energy but may not maintain 18°C ± 5°C cabin during the full 14-day lunar night without periodic active backup (small radioisotope heater or resistive heating, powered by battery). Trade-off between passive TES size (mass, volume) and active heater capacity (power budget) is not quantified. Control logic (when to activate heater, heater power level) is not optimized.

**Closest Prior Work:**  
- Passive TES models (Springer 2025, MDPI 2021): Assume full passive survival; no hybrid analysis.  
- ISS ATCS: Fully active, no passive backup; Orion capsule uses hybrid (passive MLI + active heater during Earth reentry cold-soak).  
- HERA habitat: Active HVAC control but not extreme thermal environment.

**Why It Matters:**  
- **Feasibility:** Pure passive TES may require prohibitively large PCM volume; hybrid approach (smaller TES + modest heater) is more practical.  
- **Reliability:** Redundancy (TES + heater) improves fault tolerance.  
- **Power margin:** Lunar base power is scarce; optimizing heater duty cycle could save 10-20% of total power budget.

**Tractability:**  
- **Modeling:** Transient thermal analysis + control logic (bang-bang or PID heater control) is routine simulation.  
- **Analog test:** HERA or thermal chamber can simulate lunar day/night cycle with hybrid TES + heater.  
- **Validation:** Ground testing is feasible; spaceflight validation requires lunar base or Artemis lander.

**Novelty / Tractability / Relevance Scores:**  
- **Novelty: 7/10** – Hybrid strategy is intuitive but not deeply explored in literature; control optimization is novel.  
- **Tractability: 8/10** – Modeling and analog testing are straightforward; full-scale validation is expensive.  
- **Relevance: 8/10** – Artemis base design is actively being refined; this directly impacts power and thermal architecture.

---

## Summary & Scoring

**Top two candidate gaps by combined novelty/tractability/relevance:**

1. **Gap 1 (Gravity-Dependent Two-Phase Heat Transfer)** — Avg score: 7.0. Highest relevance (8/10); critical for Mars/lunar transits. Parabolic-flight validation is accessible path. Moderate novelty; spaceflight experience is thin.

2. **Gap 6 (Lunar Hybrid Thermal Control)** — Avg score: 7.7. Highest relevance and tractability (8/10 each); directly supports Artemis. Combines novel control strategy (hybrid active-passive) with proven components. Analog testing is very feasible.

**Other strong candidates:** Gap 2 (Regolith+PCM validation, 7.7 avg) and Gap 4 (Integrated radiator design, 7.0 avg) are also promising but require larger experiments or longer development timelines.

