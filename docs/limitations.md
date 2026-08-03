# Known Limitations

This file collects limitations at the program level. Section-by-section physics/model assumptions
and their validity ranges are documented exhaustively in `derivation.md` §6 (fluid mechanics,
particle mechanics, transport modelling, biology/kinetics, and an explicit "not modelled" list) —
that is the authoritative source and is not duplicated here. This file adds (a) a pointer to the
single highest-priority open item, (b) one implementation-level finding from Phase 3 not yet in the
derivation document, and (c) a running list to be extended by the Phase 4 red-team.

## 1. Highest-priority open item: citation fidelity

Every citation in this program (`gap_register.md`, `novelty_adjudication.md`, `problem_statement.md`,
`derivation.md`) was found via `WebSearch`. This sandbox's network policy blocks `WebFetch` to every
scholarly host tested (`ntrs.nasa.gov`, `ttu-ir.tdl.org`, `biorxiv.org`, `arxiv.org`, `ices.space`,
`sciencedirect.com`, `nature.com`, `mdpi.com`, `ncbi.nlm.nih.gov`, `engineering.purdue.edu`,
`frontiersin.org` — all return HTTP 403 at the proxy). **No full text has been read in producing this
program.** Every content claim about a cited paper is `[snippet-level]`, not read-the-PDF fidelity.
`derivation.md` §10 names this as the single most load-bearing unverified point: the claim that
sedimentation dominates convective diffusion in a parallel-plate geometry (the strongest available
defence of the `Ga_dep >> 1` results) rests on a paper (Li/Busscher/van der Mei, *Colloids Surf. B*
2011) that has not been read in full. Clearing this network restriction is the single highest-value
action available to this program, named repeatedly across `novelty_adjudication.md`, `derivation.md`,
and this file, and still outstanding.

## 2. Implementation-level finding (Phase 3): the well-mixed limit of the eq. (5.7)/(5.8) reduction

`derivation.md` §5.3(B) specifies `D_v = D_B + D_conv` for the stagnant vertical-mixing term, fed
into the eq. (5.8) wall-flux formula `k_tot = v_s/(1-exp(-H/h_s))`. Implementing this literally
(`src/eclss_gravity/dormancy.py`) produces a well-mixed-limit behaviour (`h_s >> H`) of
`k_tot -> D_v/H`, i.e. a deposition rate that **increases**, not decreases, with stronger convective
mixing. This is mathematically correct for a perfect-sink wall (with enough time, turbulent transport
delivers everything to an absorbing boundary just as certainly as settling does), but it sits in
tension with the more intuitive statement in `derivation.md` §2.2(b)/§3.5 that convection "keeps
cells suspended" — that statement is about the *instantaneous* flux competition (`Omega = v_s/u_conv`),
not the *long-time asymptotic fate* against an absorbing boundary. Both are correct within their own
scope, but a reader could reasonably interpret the derivation's prose as claiming the opposite of what
the equations, applied literally over a full year, actually produce.

**Consequence found and worked around, not hidden:** simulating the 0.30 m tank scenario at any
realistic `ΔT` gives `Ra >> Ra_c` at all three gravity levels (as `derivation.md` §2.2(b) itself
already showed via the `ΔT_c` table — tank convection is "unconditionally present"), which drives the
well-mixed limit and produces near-total, gravity-*insensitive* depletion within hours regardless of
`g`. The headline dormancy figure (`fig3`) was therefore built on the 6.35 mm line geometry at
`ΔT` = 1 K instead, where `Ra` straddles `Ra_c` across the three gravity levels and the intended
"lowering gravity suppresses convection, unopposed settling wins" effect is actually visible (a
~10^5-10^6× difference in final deposited mass between lunar and Earth/Mars gravity). The tank result
is still real and is itself informative (gravity is irrelevant to a strongly-convecting tank's fate,
which is a legitimate finding) — but it should not be the paper's headline dormancy figure, since it
doesn't test the gravity-dependence claim the program is making.

**This is flagged explicitly for the Phase 4 red-team**: is the eq. (5.7)/(5.8) reduction the right
one for the well-mixed regime, or does it need an explicit two-branch treatment (settling-flux vs.
Rouse-profile-equilibrium vs. mixing-limited-delivery-to-a-perfect-sink) rather than one formula
applied uniformly? The current code implements the derivation as specified; whether the derivation's
own specification is the physically correct reduction in the well-mixed limit is exactly the kind of
question an adversarial check should resolve, not something to quietly patch around.

## 3. Everything else

See `derivation.md` §6 for the full assumption table (27 numbered items, A1-A27) and §7 for the
uncertainty ranking. The single most consequential ASSUMED (not sourced) values are the WPA/UPA
process-line internal diameter (6.35 mm, swept 3.18-12.7 mm in `fig2`) and the bimodal particle-size
distribution parameters (§7.3(b), used in the Monte Carlo). Both are swept, not fixed, in the code.
