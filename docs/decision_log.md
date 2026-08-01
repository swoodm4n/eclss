# Decision Log

Append-only. Each entry: date, phase, decision, alternatives considered, rationale, confidence.

---

## 2026-07-31 — Phase 0 — Run mode: Kickoff Mode selected for this first run

**Decision:** Execute Phases 0–2 only (setup, landscape survey, problem selection), then stop and present a checkpoint to the human before spending Phase 3+ compute on modeling/writing.

**Alternatives considered:** Full autonomous run through Phase 6 with no checkpoint, as the base prompt's default instructs.

**Rationale:** This is the first run against a completely empty repository. The base prompt itself defines "Kickoff Mode" (Appendix A) as the recommended pattern for exactly this situation — front-loading the cheap, decision-heavy phases and getting one sanity check before Opus-heavy derivation, code-building, red-teaming, and manuscript drafting are committed to a specific problem. This is not the human overriding the "near-zero involvement" mandate; it is following the run mode the prompt's own author designed for a first pass. No further checkpoints will be requested after this one (per Appendix A: "subsequent work proceeds under the full prompt with no further interruptions until the validation handoff").

**Confidence:** High that this is the correct interpretation of an ambiguous instruction (prompt offers no explicit kickoff-mode flag from the human, but is a brand-new repo starting cold).

---

## 2026-07-31 — Phase 0 — ICES target cycle and track

**Decision:** Target the ECLSS Technical Track. Use the 55th cycle (2026, now closed) as the best-available proxy for format/word-limit/template conventions, since the 56th cycle (~2027) has no published CFP yet.

**Alternatives considered:** None on track selection — ECLSS is explicitly named as a track and is the program's entire mandate, so no other track was seriously in contention.

**Rationale / limitation:** Direct WebFetch access to ices.space is blocked at the network-policy level in this sandbox (proxy returns 403 on CONNECT to ices.space:443 — confirmed via proxy status endpoint, not a site-side rejection). All facts in `/docs/ices_target.md` are reconstructed from WebSearch snippets of third-party pages that mirror ices.space content, cross-checked across 3+ independent sources (SICSA/UH, PNNL Tethys, Puerto Rico Space Foundation). No page content was hallucinated; anything not corroborated is explicitly marked unverified/TBD in that file. This is a genuine environment limitation, not a judgment call — flagging per integrity rule §1.4 (uncertainty tracked, not hidden).

**Confidence:** High on track/venue identity and the closed 55th-cycle facts (well corroborated). Low on exact 56th-cycle deadlines (not yet published anywhere) — treated as a placeholder, explicitly not to be relied on for an actual submission without re-verification.

---

## 2026-07-31 — Phase 1 — Gap register: cross-cutting convergence noted, methodology risk flagged

**Decision:** Consolidate 48 candidate gaps from 8 independent Haiku subsystem surveys into `gap_register.md`; carry 3 diverse finalists to Phase 2 Opus adjudication rather than the single top-scored row, to avoid over-indexing on one subsystem agent's self-calibrated scoring.

**Notable finding:** 4 of 8 independently-run surveys (water recovery, waste management, system integration, monitoring) converged unprompted on partial-gravity biofilm/microbial dynamics as a top gap. Logged as a two-edged signal at the time: real relevance vs. a well-populated field the searches might not be seeing all of. This caveat turned out to be correct and under-weighted — see the next entry.

**Confidence:** Medium — flagged explicitly that the survey methodology (search scoped to NTRS/ICES/arXiv) could not rule out prior art the searches didn't reach.

---

## 2026-07-31 — Phase 2 — All 3 finalists rejected by adversarial novelty adjudication; problem reselected via reframe

**Decision:** Reject Candidates A (partial-gravity microbial/biofilm kinetics), B (combined-stressor material flammability), and C (fractional-gravity two-phase heat transfer) as originally framed. Select an inverted reframe of Candidate A — a dimensionless criterion for *when* gravity-driven transport is negligible vs. first-order for microbial/biofilm processes in pumped ECLSS water loops — as the provisional problem. Full reasoning in `problem_statement.md` and `novelty_adjudication.md`.

**Alternatives considered:** All 48 rows of `gap_register.md` were in scope; the adjudicator additionally proposed gap-register row 11 (Mars ISRU-water mineral-scale prediction) as an explicitly-unvetted fallback if the reframe fails its own trivial-result risk (see below).

**Rationale:** An Opus subagent ran ~33 adversarial searches specifically trying to disprove each finalist's novelty and found real, disqualifying prior art for all three — not absence-of-evidence, but positive findings: NASA WSTF combined O2×pressure flammability data since 2007 (kills B), a 2004 Froude-number scaling law for two-phase flow at Mars/Moon gravity plus an active 20-year subfield (kills C), and three independent NASA Ames modeling efforts plus a May 2026 bioRxiv preprint plus an ESA flight experiment showing a null gravity effect (kills A as originally framed). All three failures trace to the same cause: Phase 1's searches were scoped to NTRS/ICES/arXiv, and the disqualifying prior art sat in ASME/Elsevier journals, WSTF reports, and bioRxiv — outside that scope. **Methodology lesson logged for Phase 3 onward: do not trust a clean NTRS/ICES-only search as evidence of novelty for any future claim in this program.**

The inverted framing of A survives because it treats the prior art as input/validation data rather than a competing result, borrows a contribution *form* (Konishi/Mudawar/Hasan's "criteria for negating gravity's influence," 2013) that is precedented in the adjacent two-phase-flow field but not yet made on the microbial/biofilm side, and requires no new facilities.

**Confidence:** Medium (adjudicator's explicit assessment, adopted). Named risk: the criterion may resolve to a trivially wide margin everywhere and read as confirming the obvious — mitigated by scoping to stagnant/dormancy regimes where the margin is genuinely narrow, with an explicit fallback (unvetted) to gap-register row 11 if that risk materializes.

**Outstanding blocker, logged rather than silently worked around:** the adjudicator's top-priority next action — read the full text of the Latham/Skountzos/Lawson bioRxiv preprint before fully committing — cannot be executed in this sandbox. Confirmed directly: `WebFetch` returns HTTP 403 (proxy policy denial, not a site-side block) for `biorxiv.org`, `ntrs.nasa.gov`, `ices.space`, and `arxiv.org` alike. `WebSearch` still functions and is how every citation in this program has been sourced, but no scholarly primary source is currently readable in full — every content claim in this program to date is search-snippet fidelity, not read-the-source fidelity. This is raised at the Kickoff Mode checkpoint as a question for the human rather than proceeding past it silently, per the program's integrity rules on uncertainty and per the general principle that an infrastructure limitation blocking further verification is exactly the kind of thing worth a human's attention before committing further compute.

---

## 2026-07-31 — Standing constraint added (human, mid-checkpoint) — individual spare-money fundability

**New durable rule, effective immediately and retroactively applied to problem selection:** any physical validation the chosen problem eventually needs must be fundable out of an individual engineer's personal spare money — not dependent on a well-funded institution's budget or facilities (combustion labs, centrifuges, parabolic-flight campaigns, cleanrooms, radiation-test beamtime, etc.). This refines rather than replaces §7 of the base prompt: the validator is still assumed competent with lab technique, but the *cost* of whatever they'd need to buy or access must clear a personal-spending bar, not an institutional-grant bar. Cheap workarounds to an otherwise-expensive investigation are explicitly allowed (e.g., a DIY rotating rig standing in for a real centrifuge) — this doesn't blanket-exclude any physical phenomenon, only investigations with no affordable path to evidence.

**Re-check against the currently selected problem:** Passes. The core contribution (dimensional analysis + 1-D transport model, Python, validated against already-published secondary data) has zero marginal cost. The optional sanity-check bench culture (jars, common bacterial strains, basic optical/turbidity measurement) is a few-hundred-dollar personal expense, and is explicitly optional/non-load-bearing for the core claim.

**Retroactive re-check on the two rejected finalists:** both would have failed this bar independently of their novelty problems. Candidate B (combined-stressor flammability) needs a controlled elevated-O2/reduced-pressure ignition chamber — real fire-safety infrastructure, institutional-only, and not something to recommend a hobbyist attempt regardless of budget. Candidate C (fractional-gravity two-phase heat transfer) needs parabolic-flight or centrifuge access. Both the adversarial-novelty elimination and this new budget lens converge on the same rejections — treated as a useful cross-check, not a coincidence to be suspicious of.

**Fallback re-check (gap-register row 11, Mars ISRU-water mineral scaling):** Passes. PHREEQC is free/open-source; optional wet-chemistry validation uses synthetic regolith-water recipes at bench scale, affordable out of pocket.

**Confidence:** High that the currently selected problem satisfies this constraint as scoped. This constraint will be re-applied at Phase 6 when the actual `/validation/README.md` and `bom.csv` are drafted, since that is where a violation would concretely surface.

---

## 2026-07-31 — HARD STOP — account monthly spend limit reached

**Event:** The Phase 3 first-principles derivation subagent (Opus, tasked with deriving the gravity-relevance dimensionless criterion and the ADR transport model) failed mid-run with: "Agent terminated early due to an API error: You've hit your monthly spend limit." This is a billing/quota condition on the account, not a defect in the task or the agent's approach — the agent had reportedly finished parameter research and was about to compute criterion values when it was killed.

**Action taken:** Stopped rather than retrying. Per program rule §8, a step that would spend real money — or in this case, one the account's spend cap says has already spent too much — is an explicit hard-stop condition requiring the human, not a decision to make autonomously. Did not attempt further Agent spawns (Opus or otherwise) to avoid running against a cap that is already exceeded.

**State at stop:** Phases 0–2 complete and pushed (target track/facts, gap register, adversarial novelty adjudication, provisional problem statement, individual-fundability check). Phase 3 (first-principles derivation + code) has not produced any output yet — no derivation document exists, no model code has been written. Python environment is scaffolded and ready (`requirements.txt` pinned, installed in `.venv`, `.gitignore` in place) so implementation can start immediately once derivation work resumes.

**Open question for the human:** raise the spend limit (claude.ai/settings/usage) to continue, or hold here until it resets.

---
