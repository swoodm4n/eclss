# Problem Statement (Provisional — see caveat)

**Status: PROVISIONAL, pending one blocking verification step this sandbox cannot currently clear (see §4).** Presented at the Kickoff Mode checkpoint for a human go/no-go rather than committed to silently, specifically because of that gap.

## 1. Chosen problem

**"When does gravity actually matter? A dimensionless criterion for microbial and biofilm transport in engineered partial-gravity ECLSS water loops."**

Not a model that *predicts* a partial-gravity biofilm/microbial effect — a model that determines **whether one is worth designing for**, and where. Concretely: for representative ISS/exploration Water Processor Assembly (WPA), Urine Processor Assembly (UPA), and Membrane Aerated Biofilm Reactor (MABR) operating points, compute the ratio of gravity-driven transport (Stokes sedimentation velocity, buoyancy-driven convection — both ∝ g) to forced-advection and wall-shear transport, as a Péclet/Richardson-type dimensionless criterion. Output: a quantitative boundary in (flow rate, channel dimension, cell/floc size, g) space separating "gravity-driven transport is negligible" from "gravity-driven transport is first-order," evaluated at Earth-1g, Mars (0.38g), and lunar (1/6g) gravity, with explicit attention to stagnant/low-flow regimes (mission dormancy periods up to ~1 year, tank ullage, dead legs, filter housings, post-restart transients) where the margin between the two transport modes is narrowest and least characterized.

## 2. How this problem was reached

This is the second iteration, not the first pick. Phase 1's 8-subsystem survey produced 48 candidate gaps (`gap_register.md`). Three were carried to Phase 2 novelty adjudication:
- **A** — partial-gravity microbial/biofilm kinetics modeling (predict how growth rates change with g)
- **B** — combined-stressor material flammability envelope
- **C** — fractional-gravity two-phase heat/mass-transfer scaling correlations

An adversarial Opus pass (`novelty_adjudication.md`) did real additional literature search specifically trying to disprove each one's novelty, and **rejected all three as framed**:
- **B** was killed by a factually false premise: NASA WSTF has run combined O2×pressure flammability matrices since 2007 (NTRS 20070005041), directly answered "can concentration and partial pressure be correlated?" (NTRS 20160001047), and an active multi-center NASA program (ICES-2025-392, presented 11 months before this adjudication) already covers the same envelope plus the gravity axis Candidate B omitted.
- **C** was killed most decisively: the proposed Froude-number scaling law for two-phase flow at Mars/Moon gravity was published in 2004 (Hurlbert, Witte, Best & Kurwitz, *Int. J. Multiphase Flow* 30:351–368) using the same method, at the same two gravity levels, from parabolic-flight data — with an active subfield since (gravity-scaling parameters, gravity-independence criteria, 2023 fractional-g correlations for both boiling and condensation).
- **A** was killed on both novelty (three independent NASA Ames modeling efforts already own the mechanism, including a May 2026 bioRxiv preprint explicitly decomposing gravity's effect on microbial growth into two opposing terms) and on its underlying physical premise (ESA's BioRock flight experiment at simulated Mars gravity found **no** effect on final bacterial cell concentrations; the effect that does exist is strain-dependent; and the depletion-zone mechanism the field uses is defined for quiescent suspension, which is not what a pumped ECLSS loop is).

All three failures shared one structural cause: the Phase 1 surveys searched NTRS/ICES/arXiv but the disqualifying prior art sat in ASME/Elsevier heat-transfer journals, WSTF materials reports, and the astrobiology/bioRxiv literature — outside that scope. This is logged as a methodology finding, not just a result (see `decision_log.md`).

## 3. Why the inverted framing survives where Candidate A did not

- **The prior art becomes an input, not competition.** The bioRxiv preprint's two-opposing-mechanisms decomposition, the published depletion-zone radius, the BioRock null result, and the strain-dependent clinostat data all become validation targets and parameters for a transport-regime criterion, rather than results this program would be trying to reproduce or contradict.
- **The contribution *form* is precedented and respected in an adjacent field.** Konishi, Mudawar & Hasan's "criteria for negating the influence of gravity on flow boiling critical heat flux" (*Int. J. Heat Mass Transfer* 65:203–218, 2013) is exactly this move — a "when does gravity matter" criterion rather than a global scaling law — and it is a well-regarded contribution in the two-phase-flow literature. The identical move has not been made, as far as this program's search has found, on the microbial/biofilm side of ECLSS.
- **Falsifiable and useful in both branches.** If the criterion shows gravity-driven transport is negligible across realistic ECLSS operating points, that is a genuinely useful de-risking result for lunar/Mars water-recovery-system qualification (directly relevant to NASA's own partial-gravity WRS modeling line, ICES-2024-323). If it shows gravity matters specifically in stagnant regimes, that is a targeted, actionable design finding that maps onto NASA's own stated dormancy-period concern.
- **Tractable without new facilities.** Pure dimensional analysis plus a 1-D advection-diffusion-reaction model of a biofilm-lined channel with a gravity-dependent transport term. No centrifuge, no parabolic flight required for the core contribution; an optional 1g bench culture (achievable by a hobbyist) remains available as a sanity check on the reaction-kinetics parameters, not as the load-bearing validation.

## 4. Open blocking item — why this is PROVISIONAL

The adjudicator's single highest-priority action was: read the full text of Latham, Skountzos & Lawson (bioRxiv 2026.05.15.725518) before committing, because if that preprint already contains a partial-gravity transport-regime sweep, this reframe is substantially weakened.

**This sandbox's network policy blocks that read.** Confirmed directly (not just via subagent report): `WebFetch` on `biorxiv.org`, `ntrs.nasa.gov`, `ices.space`, and even `arxiv.org` all return HTTP 403 at the proxy layer (`connect_rejected` / policy denial, verified via `$HTTPS_PROXY/__agentproxy/status`). `WebSearch` still works and is how every citation in this program's literature review was found, but no scholarly host's full text is currently readable — search-snippet fidelity only, exactly as the adjudicator flagged. This is a program-wide constraint, not specific to this one preprint: it will recur throughout Phase 3 (deriving from first principles), Phase 4 (red-team verification), and Phase 5 (citing sources in the manuscript), everywhere a claim needs to be checked against a primary source rather than a search snippet.

**Confidence this problem yields a genuine, single-paper ICES contribution: MEDIUM** (adjudicator's assessment, adopted here). Reasons to not go higher: the recommendation is a reframe constructed during adjudication, not a candidate that itself survived a full adversarial cycle, and the one preprint most likely to pre-empt it is unread. Reasons to not go lower: the contribution form is proven in an adjacent field, tractability has no facility dependency, and the result is useful in both the positive and null branches.

**Single biggest risk:** the criterion resolves to a trivially wide margin everywhere, including in stagnant regimes, making the result true but uninteresting ("we confirmed the obvious with dimensional analysis"). Mitigation if this happens: abandon the inversion and fall back to gap-register row 11 (Mars ISRU-water mineral-scale prediction via PHREEQC — high tractability, well-posed non-gravity-dependent aqueous thermodynamics) rather than publish a trivial result. That fallback is itself explicitly **unvetted** — the adjudicator ran only one confirmatory search on it — and would need its own adjudication pass before selection.

## 5. Individual spare-money fundability check

Standing constraint added mid-checkpoint: any physical validation must be affordable out of an individual engineer's personal spare money, not dependent on institutional facilities or budget (cheap workarounds to an otherwise-expensive investigation remain fair game — this doesn't blanket-exclude a phenomenon, only investigations with no affordable path to evidence). Full reasoning in `decision_log.md`. This problem passes: the core contribution is pure dimensional analysis and a 1-D transport model validated against already-published secondary data (zero marginal cost); the optional sanity-check bench culture is a few-hundred-dollar personal expense and is explicitly non-load-bearing. Both rejected finalists (B: needs a controlled elevated-O2 ignition chamber; C: needs parabolic-flight or centrifuge access) would have failed this bar independently of their novelty problems — a useful cross-check that the adjudication and this constraint converge rather than conflict.

## 6. Runners-up and why they lost

Full detail in `novelty_adjudication.md`. In brief: Candidate B (flammability) and Candidate C (two-phase heat transfer) are rejected outright, not merely ranked below the winner — both have real, disqualifying, actively-published prior art at essentially the exact scope proposed. They are not held as fallbacks.
