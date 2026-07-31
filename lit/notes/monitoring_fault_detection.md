# ECLSS Monitoring, Sensing, and Fault Detection: Literature Survey & Research Gaps

## Sources

1. **Graph-based Real-Time Fault Diagnostics** (NASA NTRS 1989)
   - Citation: 19890006195
   - URL: https://ntrs.nasa.gov/citations/19890006195
   - Summary: Describes graph-based real-time fault detection and diagnosis techniques well-suited for structured knowledge representation and testing/validation in large-scale space systems.

2. **Intelligent Monitoring and Diagnosis Systems for the Space Station** (NASA NTRS 1991)
   - Citation: 19910011370  
   - URL: https://ntrs.nasa.gov/api/citations/19910011370/downloads/19910011370.pdf
   - Summary: Demonstrates ARGES (Atmospheric Revitalization Group Expert System) for real-time fault management of SAWD CO₂ removal assembly; detects gradual degradations and predicts failures.

3. **ECLSS Advanced Automation Preliminary** (UAH Research Report 823, NASA NTRS)
   - Citation: 19910018451
   - Summary: Early work on automation and intelligent monitoring for ECLSS subsystems including potable water, hygiene water, CO₂ reduction processes.

4. **Prognostics for Autonomous Deep-Space Habitat Health Management Under Multiple Unknown Failure Modes** (arXiv 2411.12159, November 2024)
   - URL: https://arxiv.org/pdf/2411.12159
   - Summary: Addresses prognostics framework for deep-space habitats facing unknown failure modes; relevant for Lunar/Mars long-duration missions with limited ground support.

5. **Unraveling Anomalies in Time: Unsupervised Discovery and Isolation of Anomalous Behavior in Bio-regenerative Life Support System Telemetry** (arXiv 2406.09825, June 2024)
   - URL: https://arxiv.org/abs/2406.09825
   - Summary: Demonstrates unsupervised anomaly detection (MDI, DAMP, K-means clustering) applied to EDEN ISS greenhouse telemetry; addresses challenge of detecting anomalies without labeled fault data.

6. **Machine Learning-based vs Deep Learning-based Anomaly Detection in Multivariate Time Series for Spacecraft Attitude Sensors** (arXiv 2409.17841, September 2024)
   - URL: https://arxiv.org/abs/2409.17841
   - Summary: Comparative study of ML vs. DL for FDIR in spacecraft sensor suites; reports on stuck-value detection in attitude sensor multivariate data.

7. **Machine Learning-driven Anomaly Detection and Forecasting for Euclid Space Telescope Operations** (arXiv 2411.05596, November 2024)
   - URL: https://arxiv.org/abs/2411.05596
   - Summary: XGBoost-based anomaly detection and temperature forecasting for spacecraft operations; demonstrates operational spacecraft anomaly detection methods.

8. **Combining Life Support Systems with Digital Twins: A New Potential?** (MDPI Proceedings 2024)
   - URL: https://www.mdpi.com/2673-4591/133/1/94
   - Summary: Reviews digital twin implementation for LSS monitoring and testing; identifies data collection, sensor requirements, and simulation model challenges as key barriers.

9. **A Supervised AI-Based Toolchain for Anomaly Detection, Diagnosis, and Reconfiguration for the Life-Support System of the COLUMBUS Module of the ISS** (ResearchGate, 2024)
   - URL: https://www.researchgate.net/publication/394783272_A_supervised_AI-based_toolchain_for_anomaly_detection_diagnosis_and_reconfiguration_for_the_life-support_system_of_the_COLUMBUS_module_of_the_ISS
   - Summary: Describes supervised AI methods for ISS ECLSS anomaly detection and diagnosis; demonstrates operational toolchain for European module life support.

10. **Development of a High-Resolution Multiplex qPCR Method to Profile Microbial Consortia in Spaceflight Water Recovery Systems** (NIH/PMC 2025)
    - URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12891862/
    - Summary: Reports persistent five-species biofilm (P. aeruginosa, B. contaminans, M. fujisawaense, R. insidiosa, C. metallidurans) in ISS water recovery; detection limit 10⁴–10⁶ CFU, but current ISS methods cannot detect < 10⁴ CFU/L.

11. **Microbial Detection and Quantification of Low-Biomass Water Samples Using an International Space Station Smart Sample Concentrator** (Microorganisms 2023, NIH)
    - URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10537578/
    - Summary: ISS Smart Sample Concentrator (iSSC) achieves < 10⁴ CFU/L detection; current real-time monitoring methods absent—samples sent to Earth for culture-based analysis (months delay).

12. **ICES-2024-141: ECLS Overview of Events 2023** (ICES Proceedings 2024, Texas Tech University Repository)
    - URL: https://ntrs.nasa.gov/api/citations/20240005249/downloads/ICES-2024-141%20ECLS%20Overview%20of%20Events%202023%20Final.pdf
    - Summary: Reports 2023 ISS ECLSS events including Hall Effect sensor damage on CDRA blower during ground test; summarizes on-orbit HEPA and charcoal filter monitoring.

13. **ECLSS - First Space Habitat Architecture** (ICES-2024-193, 2024)
    - URL: https://spacearchitect.org/pubs/ICES-2024-193.pdf
    - Summary: Discusses design requirements for ECLSS to detect and diagnose component/system health in real time for first lunar habitats; outlines sensor architecture needs.

14. **More Than a Decade of International Space Station Microbial Sampling in the Environmental Control and Life Support Systems** (ICES 2024, Abstract)
    - Conference: 53rd ICES (July 2024)
    - Summary: Ten+ years of ISS ECLSS microbial monitoring data covering both US and Russian segments; identifies persistent contamination patterns and biofilm formation.

15. **Long-Term Electronics Reliability in Deep Space: Lessons from 47 Years of Voyager Mission Telemetry Analysis** (ScienceDirect, 2025)
    - URL: https://www.sciencedirect.com/science/article/abs/pii/S0263224126017720
    - Summary: Quantified Voyager sensor degradation: power efficiency −6%, RF power −15%, sensor drift 0.1%/decade. Critical for predicting ECLSS sensor lifetime in deep space.

16. **PHM for Spacecraft Propulsion Systems: Similarity-Based Model and Physics-Inspired Features** (ResearchGate, 2024)
    - URL: https://www.researchgate.net/publication/375231148_PHM_for_Spacecraft_Propulsion_Systems_Similarity-Based_Model_and_Physics-Inspired_Features
    - Summary: Hybrid physics-inspired + data-driven prognostics; winning approach in NASA PHM competition for spacecraft systems diagnosis.

17. **Review: Practical Options for Selecting Data-Driven or Physics-Based Prognostics** (NSF/NASA Review)
    - URL: https://web.mae.ufl.edu/nkim/Papers/paper70.pdf
    - Summary: Comprehensive review of physics-based, data-driven, and hybrid prognostics methods; notes "small data problem" in spacecraft PHM and limited fault occurrence data.

18. **NASA-STD-3001, Volume 2 (ECLSS Technical Requirements)**
    - URL: https://www.nasa.gov/wp-content/uploads/2023/11/nasa-std-3001-vol-2-rev-d-with-signature.pdf
    - Summary: Specifies requirements for atmospheric control, atmospheric data recording/display, atmospheric monitoring/alerting, trace constituent monitoring, combustion monitoring, and celestial dust monitoring.

19. **HERA: Human Exploration Research Analog Facility** (NASA JSC)
    - URL: https://www.nasa.gov/wp-content/uploads/2016/05/2019_hera_facility_capabilities_information.pdf
    - Summary: 650 sq ft analog habitat at JSC with simulated ECLSS for crew isolation/confinement studies; enables testing of ECLSS monitoring procedures and anomaly response under realistic conditions.

20. **3D Interactive Model of HERA to Support ECLSS Anomaly Resolution Using a Virtual Assistant** (IEEE 2021)
    - URL: https://ieeexplore.ieee.org/document/9438341/
    - Summary: Demonstrates virtual assistant (Daphne-AT) for astronaut-AI interaction during ECLSS anomaly diagnosis at HERA; identifies human factors in anomaly diagnosis workflows.

21. **Model-Free Fault Detection Framework for Spacecraft Health Monitoring** (ScienceDirect 2025)
    - URL: https://www.sciencedirect.com/science/article/abs/pii/S1270963825010752
    - Summary: Addresses model-free anomaly detection when physics-based models are unavailable or complex; relevant for novel or untested ECLSS subsystems.

22. **Environmental Control and Life Support Systems (ECLSS) - NASA Reference** (NASA.gov)
    - URL: https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/
    - Summary: Official NASA overview: ECLSS provides/controls atmospheric pressure, fire detection/suppression, O₂ levels, ventilation, waste management, and water supply. Integrates subsystems: atmosphere revitalization, water recovery, waste management, thermal control.

---

## Candidate Research Gaps

### Gap 1: Real-Time Autonomous Microbial Biofilm Detection in Spacecraft Water Recovery Systems Without Earth-Return Analysis

**Closest Prior Work:**
- Multiplex qPCR method (Source 10): detects species-specific biofilms at 10⁴–10⁶ CFU but requires lab benchtop equipment.
- iSSC (Smart Sample Concentrator, Source 11): achieves < 10⁴ CFU/L but no real-time decision capability.
- ISS current practice (Source 11): samples collected, sent to Earth for months-long culture analysis.

**Why It Matters:**
Long-duration Lunar/Mars missions cannot rely on Earth return cycles. Persistent biofilms (five identified species) cause biofouling, corrosion, and water quality degradation (Source 10). Early detection enables targeted biocide application or unit replacement before system failure. Partial-gravity biofilm behavior is unknown—biofilm formation kinetics may differ on Moon/Mars.

**Tractability & Validation:**
Moderate. Bench test could use ISM (International Space Microbiome) bacterial cultures in a miniaturized water circuit with real-time optical/electrochemical sensors (e.g., impedance spectroscopy, fluorescence-based viability staining). Pairing machine learning anomaly detection (Source 5: unsupervised methods) with sensor fusion could enable autonomous thresholds. Challenge: verifying detection limits under variable biofilm morphology; would require 6–12 month ground analog test (HERA or ISM facility).

**Novelty/Tractability/Relevance Scores:**
- Novelty: 7/10 (qPCR miniaturization and real-time optics exist; integration for autonomous LSS use is new)
- Tractability: 6/10 (optical sensors flight-proven; biofilm culturing well-established; autonomous decision logic moderate)
- Relevance: 9/10 (critical blocker for multi-year missions; affects crew health & mission success directly)

---

### Gap 2: Long-Duration ECLSS Sensor Degradation Characterization and Adaptive Drift Compensation for Partial-Gravity Environments

**Closest Prior Work:**
- Voyager 47-year reliability data (Source 15): 0.1%/decade sensor drift; power and RF efficiency decline 6–15% over decades. ISS sensors show cumulative drift but no published characterization under lunar/Martian gravity or radiation.
- NASA-STD-3001 (Source 18): specifies atmospheric and water monitoring but does not address drift compensation or adaptive recalibration.
- Model-free fault detection framework (Source 21): detects anomalies when models unavailable but not designed for gradual sensor degradation.

**Why It Matters:**
ISS operates at 1G with frequent resupply & crew repair. Moon (1/6G) and Mars (0.38G) missions lasting 2–3 years cannot rely on ground calibration cycles. Electrolytic sensors (O₂, CO₂, pH) and conductivity probes drift under thermal, radiation, and gravity stress. Uncompensated drift leads to false alarms (crew action overhead) or missed thresholds (safety risk). Gravity-induced drift (thermal gradients, convection changes) is poorly characterized.

**Tractability & Validation:**
High. Centrifuge test at NASA Glenn or German Aerospace Center (DLR) could expose ECLSS sensors (O₂, CO₂, water quality probes) to lunar/Martian gravity for 6–12 months with accelerated thermal cycling and radiation simulation. Collect hourly telemetry, measure offline calibration drift. Develop Bayesian adaptive filter (physics-inspired, Source 16) to estimate true value from drifting sensor. Validate against reference lab instruments. Bench-level hobbyist test: tabletop long-term sensor logging in thermal chamber with periodic manual calibration checks.

**Novelty/Tractability/Relevance Scores:**
- Novelty: 8/10 (gravity-dependent sensor drift in ECLSS not published; adaptive compensation methods exist but not applied to life support)
- Tractability: 8/10 (hardware/gravity facilities exist; sensor logging straightforward; Bayesian filters well-developed; 12-month timeline reasonable for phased analog test)
- Relevance: 8/10 (directly affects autonomous ECLSS operation fidelity on Moon/Mars; enables longer mission confidence intervals)

---

### Gap 3: Hybrid Physics-Data-Driven Fault Diagnosis for CO₂ Removal Systems Under Radiation-Induced Sensor Corruption

**Closest Prior Work:**
- ARGES (Source 2): rule-based expert system for SAWD CO₂ removal; detects gradual degradation. Does not handle sensor noise/faults.
- Physics-inspired features + similarity-based model (Source 16): winning NASA PHM approach. Not demonstrated on ECLSS CO₂ systems.
- ML anomaly detection for spacecraft telemetry (Sources 6, 7): handles sensor stuck-values but does not isolate fault source (mechanical vs. sensor).
- "Small data problem" in spacecraft PHM (Source 17): limited labeled fault data for deep learning training.

**Why It Matters:**
CDRA/Sabatier CO₂ removal is critical for long-duration missions. Hall Effect sensors on CDRA blower suffer damage during ground test (Source 12) and radiation environment on Moon may degrade semiconductor sensors. Current methods cannot distinguish sensor failure from mechanical degradation under noisy/corrupted data. Radiation-induced sensor drift or bit flips are undercharacterized in ECLSS literature. False diagnosis wastes limited spares and crew time.

**Tractability & Validation:**
Moderate–High. Develop hybrid approach: (1) Physics layer: model CO₂ absorption kinetics, thermal feedback, and blower dynamics; (2) Data layer: train ML model (e.g., Random Forest, Source 16) on synthetic faults + sparse ISS telemetry to predict sensor vs. mechanical faults; (3) Radiation testing: expose Hall Effect sensors to ISS-equivalent radiation dose, log stuck-bit corruption patterns. Integrate with HERA or simulator (Source 20) to validate diagnosis under crew-in-the-loop scenarios. Bench test: tabletop CO₂ absorption column with intentionally corrupted sensor signals.

**Novelty/Tractability/Relevance Scores:**
- Novelty: 7/10 (hybrid physics-ML proven in propulsion; not applied to ECLSS CO₂ removal; radiation sensor corruption in ECLSS not addressed in open literature)
- Tractability: 7/10 (physics model moderate complexity; radiation effects well-characterized; ML frameworks available; requires integration work and ISS data sharing)
- Relevance: 8/10 (CO₂ removal system-critical; affects crew safety and mission flexibility; radiation hardening is gap for Lunar/Mars)

---

### Gap 4: Digital Twin Fidelity Assessment and Validation Framework for ECLSS Multi-Component Systems

**Closest Prior Work:**
- Digital twins for life support overview (Source 8): identifies data collection, sensor requirements, and model calibration challenges but lacks formalized fidelity metrics or validation methodology.
- ECLSS-first habitat architecture (Source 13): states design requirement for real-time diagnostics but does not specify digital twin implementation or validation approach.
- Hybrid physics-data prognostics (Source 16): demonstrates model-driven diagnosis but not full system digital twin.

**Why It Matters:**
NASA and ESA are advocating digital twins for autonomous ECLSS monitoring on Lunar/Mars habitats. No published standard exists for validating digital twin accuracy (fidelity) across normal, off-nominal, and emergency scenarios. Developers cannot compare fidelity across model types (CFD, reduced-order, ML-based) or justify computational cost vs. prediction gain. Without rigorous validation, crews may over-trust or under-trust autonomous diagnostic recommendations, reducing operational efficiency.

**Tractability & Validation:**
Moderate. Define fidelity metrics: (1) prediction error tolerance (e.g., ±5% for O₂/CO₂ partial pressure), (2) false alarm rate, (3) fault isolation latency, (4) computational footprint. Use ISS historical telemetry (10+ years of ECLSS data, Source 14) to train and validate candidate digital twin models (CFD, neural ODE, physics-informed neural networks). Compare against ground-truth ISS events (Source 12: sensor failures, filter clogging). Publish open benchmark dataset and leaderboard (similar to ML challenges). Bench test: tabletop ECLSS loop (water quality, atmosphere) with instrumented faults; compare real vs. model predictions.

**Novelty/Tractability/Relevance Scores:**
- Novelty: 8/10 (no published digital twin fidelity standard for ECLSS; benchmarking approach novel for life support)
- Tractability: 6/10 (ISS data access may be limited; model training straightforward; defining fidelity thresholds requires multi-center consensus)
- Relevance: 9/10 (directly enables autonomous ECLSS for long-duration missions; high-priority gap for NASA/ESA architecture studies)

---

### Gap 5: Unsupervised Anomaly Detection for ECLSS in Off-Nominal Regimes Without Ground Truth (Extended Mission Data Gap)

**Closest Prior Work:**
- Unsupervised anomaly detection in bio-regenerative LSS (Source 5): MDI, DAMP clustering applied to EDEN greenhouse; demonstrates methods without labeled data.
- Small data problem in spacecraft PHM (Source 17): lack of labeled failure samples limits supervised learning; unsupervised methods needed.
- Model-free fault detection (Source 21): generic framework for systems with incomplete physical models.

**Why It Matters:**
During 2–3 year Lunar/Mars transit or habitat occupation, crews may encounter degradation modes not seen in ground testing or ISS data (e.g., interaction of radiation, dust, reduced gravity, unanticipated contaminants). Supervised ML models trained on historical data will not detect novel faults. Unsupervised methods (clustering, density-based anomaly detection) can identify deviations from nominal without labeled data, but performance on ECLSS telemetry (multivariate, noisy, seasonal patterns) is unvalidated. Published work on bio-regenerative LSS (Source 5) shows promise but not on thermal, water, or atmosphere revitalization subsystems.

**Tractability & Validation:**
Moderate–High. Extend Source 5 methodology to ISS ECLSS subsystems: apply MDI, DAMP, LOF (Local Outlier Factor), and isolation forest algorithms to multi-year ISS telemetry (atmosphere, water, thermal). Benchmark against known ISS anomalies (Source 12, 14). Test sensitivity to sensor noise and seasonal patterns. Validate on HERA simulated off-nominal scenarios (depressurization, filter clogging, microbial spike). Bench test: simulate ECLSS degradation in tabletop loop; assess detection latency and false positive rate.

**Novelty/Tractability/Relevance Scores:**
- Novelty: 7/10 (unsupervised methods established; application to full ECLSS subsystem suite novel)
- Tractability: 7/10 (algorithms well-documented; ISS data access variable; validation in analog (HERA) feasible; 18–24 month development)
- Relevance: 8/10 (critical for crew safety on long-duration missions; no mission ground support available; enables autonomous anomaly early warning)

---

### Gap 6: Radiation-Hardened Fault Detection Architecture for Long-Duration Deep-Space ECLSS Sensor Pathways

**Closest Prior Work:**
- ICES-2024 sensor damage report (Source 12): Hall Effect sensor damage on CDRA blower; not from radiation but indicates mechanical sensitivity.
- Voyager radiation effects (Source 15): documented sensor drift and power degradation but not specific to ECLSS sensors.
- NASA-STD-3001 (Source 18): specifies monitoring requirements but does not address radiation hardening of sensor signal chains.

**Why It Matters:**
Lunar South Pole and deep-space missions expose sensors to cumulative solar and galactic cosmic radiation. Analog circuitry (sensor signal conditioning, A/D converters) experiences single-event upsets (SEUs), total ionizing dose (TID) effects, and bit flips. No published study quantifies ECLSS sensor radiation susceptibility or proposes fault-tolerant sensor architectures. Radiation-hardened electronics exist but are expensive and power-hungry; cost-benefit analysis for ECLSS sensor pathways lacking. Undetected sensor corruption during a critical event (e.g., habitat decompression alarm) could endanger crew.

**Tractability & Validation:**
Moderate. Conduct radiation test campaign at heavy-ion facility (e.g., LBNL, TAMU): expose flight-candidate ECLSS sensors (CO₂, O₂, H₂O partial pressure, conductivity probes) and signal conditioning circuits to 1–10 Gy dose under mission-relevant energy spectra. Log upset events, bit-flip patterns, analog offset shifts. Develop fault detection signatures (sensor rate-of-change limits, redundancy voting). Compare unshielded vs. shielded sensor designs. Test recovery/reset protocols. Bench test: table-top circuit with programmed upsets; verify detection and fault isolation logic.

**Novelty/Tractability/Relevance Scores:**
- Novelty: 9/10 (radiation hardening of ECLSS sensor pathways not addressed in open literature; high-impact gap)
- Tractability: 5/10 (radiation testing expensive and access-limited; signal processing straightforward; 24–36 month timeline with test facility access)
- Relevance: 9/10 (essential for Moon/Mars mission risk management; directly affects sensor reliability over mission lifetime; no current mitigation strategy published)

---

## Summary

**Key Challenges Identified:**
1. **Autonomy gap**: Real-time diagnosis without Earth-return analysis (biofilm detection, sensor degradation).
2. **Data scarcity**: Limited labeled ECLSS fault data constrains supervised ML and physics-based hybrid approaches.
3. **Environment validation**: Partial-gravity, radiation, and thermal effects on sensors and diagnostic algorithms poorly characterized.
4. **Standards and benchmarks**: No formalized digital twin fidelity metrics or unsupervised anomaly detection validation frameworks for ECLSS.
5. **Radiation effects**: Sensor hardening and fault detection under space radiation not addressed for life support systems.

**Most Tractable, Highest-Impact Gaps (for near-term research):**
- Gap 2 (sensor degradation): High tractability (gravity chambers exist), directly validates sensor models for 2–3 year missions.
- Gap 5 (unsupervised anomaly detection): Moderate tractability (ISS data + open algorithms), addresses novel fault modes on extended missions.
- Gap 3 (hybrid CO₂ diagnosis under radiation): Moderate tractability (combines established methods), addresses system-critical component with radiation sensitivity.

**Highest Novelty/Highest Risk Gaps (for moonshot research):**
- Gap 4 (digital twin fidelity): Enables autonomous ECLSS; requires multi-center consensus on standards.
- Gap 6 (radiation-hardened sensor architecture): Fundamental enabler for deep-space missions; high cost but mission-critical.

