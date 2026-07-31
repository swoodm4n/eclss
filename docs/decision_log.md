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
