"""Compare bench-test convection-onset data against the model's Ra_c prediction.

This is the analysis script referenced by `validation/README.md` §A.6. It ingests the CSV a
Part-A experimenter produces and answers one question: **is the empirical convection-onset
threshold consistent with the model's assumed `Ra_c = 1708`?**

Why this matters (validation/README.md §A.7, derivation.md A18, redteam_report.md Finding 2.4):
`Ra_c = 1708` is the classical value for a *rigid-rigid infinite plane layer*. A tube is not an
infinite plane layer, and the derivation concedes an unquantified O(1) geometric correction.
`docs/limitations.md` §4 shows the Figure 4 three-way gravity split does NOT survive a 2x error
in `Ra_c`. So pinning down the real `Ra_c` for a tube geometry is the single highest-value thing
a cheap bench test can contribute to this model.

Input CSV format (validation/README.md §A.6):
    trial, delta_T_K, H_m, mixing_onset_s, notes
where `mixing_onset_s` is the observed time to visible mixing, or empty/NaN/negative if no
mixing was observed within the observation window.

Usage:
    python3 -m eclss_gravity.validation_compare path/to/your_data.csv
    python3 -m eclss_gravity.validation_compare --self-test    # verify on synthetic data

Statistical approach: with the small sample sizes a hobbyist bench test realistically produces
(README §A.4 suggests 5 delta_T levels x 3 repetitions = 15 points), a bracketing estimate is
more honest than a fitted curve. We report the interval between the highest no-mixing Ra and
the lowest mixing Ra -- the empirical Ra_c must lie inside it -- rather than a point estimate
with a false-precision confidence interval. If the bracket is inconsistent (overlapping
mixing/no-mixing outcomes), that is reported as such rather than smoothed over.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

from . import constants
from .buoyancy import rayleigh_number


@dataclass
class OnsetComparison:
    n_trials: int
    n_mixed: int
    n_not_mixed: int
    ra_highest_not_mixed: float | None
    ra_lowest_mixed: float | None
    bracket_consistent: bool
    ra_c_model: float
    verdict: str

    def report(self) -> str:
        lines = [
            "=== Convection-onset validation: bench data vs. model Ra_c ===",
            f"trials: {self.n_trials}  (mixed: {self.n_mixed}, no mixing: {self.n_not_mixed})",
            f"model Ra_c (assumed):            {self.ra_c_model:.0f}",
        ]
        if self.ra_highest_not_mixed is not None:
            lines.append(f"highest Ra with NO mixing:       {self.ra_highest_not_mixed:.0f}")
        else:
            lines.append("highest Ra with NO mixing:       (none -- every trial mixed)")
        if self.ra_lowest_mixed is not None:
            lines.append(f"lowest Ra WITH mixing:           {self.ra_lowest_mixed:.0f}")
        else:
            lines.append("lowest Ra WITH mixing:           (none -- no trial mixed)")
        if self.bracket_consistent and self.ra_highest_not_mixed is not None and self.ra_lowest_mixed is not None:
            lines.append(
                f"empirical Ra_c lies in:          [{self.ra_highest_not_mixed:.0f}, {self.ra_lowest_mixed:.0f}]"
            )
        lines.append("")
        lines.append(f"VERDICT: {self.verdict}")
        return "\n".join(lines)


def compare_onset(
    rows: list[dict],
    ra_c_model: float = constants.RA_C,
    T_K: float = 298.15,
) -> OnsetComparison:
    """Compare observed mixing/no-mixing outcomes against the model's Ra_c.

    `rows` entries need `delta_T_K`, `H_m`, and `mixing_onset_s` (None/NaN/negative = no mixing).
    """
    beta = constants.water_thermal_expansion(T_K)
    nu = constants.water_kinematic_viscosity(T_K)
    alpha_th = constants.water_thermal_diffusivity(T_K)

    ra_not_mixed: list[float] = []
    ra_mixed: list[float] = []

    for r in rows:
        delta_T = float(r["delta_T_K"])
        H = float(r["H_m"])
        Ra = rayleigh_number(constants.G_EARTH, beta, delta_T, H, nu, alpha_th)
        onset = r.get("mixing_onset_s")
        mixed = onset is not None and str(onset).strip() != "" and float(onset) > 0 and not math.isnan(float(onset))
        (ra_mixed if mixed else ra_not_mixed).append(Ra)

    highest_not_mixed = max(ra_not_mixed) if ra_not_mixed else None
    lowest_mixed = min(ra_mixed) if ra_mixed else None

    # The bracket is "consistent" if every no-mixing trial sits below every mixing trial --
    # i.e. the outcome is cleanly threshold-like rather than scattered.
    consistent = (
        highest_not_mixed is not None
        and lowest_mixed is not None
        and highest_not_mixed < lowest_mixed
    )

    if highest_not_mixed is None:
        verdict = (
            "INCONCLUSIVE -- every trial mixed. The lowest Ra tested is already above onset; "
            f"re-run with delta_T values below the model's predicted threshold (Ra < {ra_c_model:.0f})."
        )
    elif lowest_mixed is None:
        verdict = (
            "INCONCLUSIVE -- no trial mixed. The highest Ra tested is still below onset; "
            f"re-run with delta_T values above the model's predicted threshold (Ra > {ra_c_model:.0f})."
        )
    elif not consistent:
        verdict = (
            f"SCATTERED -- mixing and no-mixing outcomes overlap in Ra "
            f"(no-mixing seen up to Ra={highest_not_mixed:.0f}, mixing seen down to Ra={lowest_mixed:.0f}). "
            "Onset is not cleanly threshold-like in this dataset. Increase repetitions, tighten "
            "delta_T control, or check for residual stratification between runs (README A.4 step 7)."
        )
    elif highest_not_mixed <= ra_c_model <= lowest_mixed:
        verdict = (
            f"CONSISTENT with the model -- the empirical bracket "
            f"[{highest_not_mixed:.0f}, {lowest_mixed:.0f}] contains Ra_c = {ra_c_model:.0f}. "
            "The classical plane-layer value is adequate for this tube geometry at this precision."
        )
    else:
        factor = (lowest_mixed if ra_c_model < highest_not_mixed else highest_not_mixed) / ra_c_model
        direction = "HIGHER" if ra_c_model < highest_not_mixed else "LOWER"
        verdict = (
            f"INCONSISTENT with the model -- the empirical bracket "
            f"[{highest_not_mixed:.0f}, {lowest_mixed:.0f}] excludes Ra_c = {ra_c_model:.0f}. "
            f"The real onset is {direction} than assumed, by roughly a factor of {abs(factor):.2f}. "
            "This is a genuine, reportable correction to derivation.md assumption A18 -- and per "
            "docs/limitations.md §4, a factor of ~2 in Ra_c is enough to change the Figure 4 "
            "gravity-separation conclusion, so this should be propagated, not noted and ignored."
        )

    return OnsetComparison(
        n_trials=len(rows),
        n_mixed=len(ra_mixed),
        n_not_mixed=len(ra_not_mixed),
        ra_highest_not_mixed=highest_not_mixed,
        ra_lowest_mixed=lowest_mixed,
        bracket_consistent=consistent,
        ra_c_model=ra_c_model,
        verdict=verdict,
    )


def plan_geometry(target_delta_T_c_K: float = 5.0, T_K: float = 298.15, g: float = constants.G_EARTH) -> float:
    """Return the layer depth / tube bore (m) whose predicted onset sits at `target_delta_T_c_K`.

    Design helper for validation/README.md Part A. Because Ra ~ H^3, the controllable quantity
    (delta_T) is extremely sensitive to depth: a 250 mm column reaches onset at ~1e-5 K
    (unmeasurable), while a 2.5 mm layer reaches it at ~5.7 K (trivially measurable with a $25
    thermocouple). Inverting eq. (2.5) for H:

        H = [ Ra_c * nu * alpha_th / (g * beta * delta_T_c) ] ^ (1/3)
    """
    beta = constants.water_thermal_expansion(T_K)
    nu = constants.water_kinematic_viscosity(T_K)
    alpha_th = constants.water_thermal_diffusivity(T_K)
    return (constants.RA_C * nu * alpha_th / (g * beta * target_delta_T_c_K)) ** (1.0 / 3.0)


def tube_geometry_correction(observed_delta_T_c_K: float, H_m: float, T_K: float = 298.15) -> float:
    """Return the empirical Ra_c / 1708 ratio implied by an observed onset in a tube.

    This is the quantity Part A actually exists to measure (validation/README.md §A.1):
    derivation.md A18 concedes an unquantified O(1) correction for tube-vs-plane-layer geometry,
    and docs/limitations.md §4 shows a factor of 2 here changes a headline conclusion. A ratio
    of 1.0 means the classical plane-layer value transfers to tube geometry unchanged.
    """
    beta = constants.water_thermal_expansion(T_K)
    nu = constants.water_kinematic_viscosity(T_K)
    alpha_th = constants.water_thermal_diffusivity(T_K)
    ra_observed = rayleigh_number(constants.G_EARTH, beta, observed_delta_T_c_K, H_m, nu, alpha_th)
    return ra_observed / constants.RA_C


def load_csv(path: str) -> list[dict]:
    import csv

    with open(path, newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def _self_test() -> int:
    """Verify the comparison logic on synthetic data, since no real bench data exists yet.

    Constructs three datasets with a KNOWN true onset and checks the verdict is right in each
    case. This exists so the script is trustworthy the first time a real experimenter runs it,
    rather than being debugged against their one-and-only dataset.
    """
    beta = constants.water_thermal_expansion()
    nu = constants.water_kinematic_viscosity()
    alpha_th = constants.water_thermal_diffusivity()
    H = 0.25  # 250 mm water column, per the BOM's graduated-cylinder option

    def delta_T_for_ra(target_ra: float) -> float:
        return target_ra * nu * alpha_th / (constants.G_EARTH * beta * H**3)

    failures = 0

    # Case 1: true onset at the model's Ra_c -> should report CONSISTENT
    rows = []
    for ra, mixed in ((800, False), (1200, False), (1500, False), (2200, True), (4000, True)):
        for trial in range(3):
            rows.append({"trial": trial, "delta_T_K": delta_T_for_ra(ra), "H_m": H,
                         "mixing_onset_s": 120 if mixed else ""})
    result = compare_onset(rows)
    if not result.verdict.startswith("CONSISTENT"):
        print(f"SELF-TEST FAIL (case 1, expected CONSISTENT):\n{result.report()}")
        failures += 1

    # Case 2: true onset well above the model's Ra_c (a tube-geometry correction) -> INCONSISTENT
    rows = []
    for ra, mixed in ((1000, False), (2000, False), (3000, False), (5000, True), (8000, True)):
        for trial in range(3):
            rows.append({"trial": trial, "delta_T_K": delta_T_for_ra(ra), "H_m": H,
                         "mixing_onset_s": 120 if mixed else ""})
    result = compare_onset(rows)
    if not result.verdict.startswith("INCONSISTENT"):
        print(f"SELF-TEST FAIL (case 2, expected INCONSISTENT):\n{result.report()}")
        failures += 1

    # Case 3: scattered outcomes -> SCATTERED
    rows = [
        {"trial": 0, "delta_T_K": delta_T_for_ra(1000), "H_m": H, "mixing_onset_s": 120},
        {"trial": 1, "delta_T_K": delta_T_for_ra(3000), "H_m": H, "mixing_onset_s": ""},
        {"trial": 2, "delta_T_K": delta_T_for_ra(2000), "H_m": H, "mixing_onset_s": 90},
    ]
    result = compare_onset(rows)
    if not result.verdict.startswith("SCATTERED"):
        print(f"SELF-TEST FAIL (case 3, expected SCATTERED):\n{result.report()}")
        failures += 1

    # Case 4/5: one-sided datasets -> INCONCLUSIVE
    for ra_all, mixed_all, label in ((500, False, "all below onset"), (9000, True, "all above onset")):
        rows = [{"trial": i, "delta_T_K": delta_T_for_ra(ra_all), "H_m": H,
                 "mixing_onset_s": 120 if mixed_all else ""} for i in range(3)]
        result = compare_onset(rows)
        if not result.verdict.startswith("INCONCLUSIVE"):
            print(f"SELF-TEST FAIL (case '{label}', expected INCONCLUSIVE):\n{result.report()}")
            failures += 1

    # Design-helper checks: plan_geometry must invert critical_delta_T exactly.
    from .buoyancy import critical_delta_T

    for target_dT in (1.0, 5.0, 11.0):
        H_planned = plan_geometry(target_dT)
        dT_check = critical_delta_T(
            constants.G_EARTH, constants.water_thermal_expansion(),
            H_planned, constants.water_kinematic_viscosity(), constants.water_thermal_diffusivity(),
        )
        if abs(dT_check - target_dT) / target_dT > 1e-9:
            print(f"SELF-TEST FAIL (plan_geometry round-trip at {target_dT} K -> {dT_check} K)")
            failures += 1

    # A tube whose onset matches the plane-layer prediction must give a correction ratio of 1.0.
    H_5K = plan_geometry(5.0)
    ratio = tube_geometry_correction(5.0, H_5K)
    if abs(ratio - 1.0) > 1e-9:
        print(f"SELF-TEST FAIL (tube_geometry_correction should be 1.0 for an on-prediction onset, got {ratio})")
        failures += 1

    if failures == 0:
        print("validation_compare self-test: all synthetic verdict cases and design-helper "
              "round-trips passed.")
        print("\nDesign reference (why validation/README.md Part A uses a SHALLOW layer):")
        for target in (1.0, 3.0, 5.0, 11.0):
            print(f"  to put onset at delta_T_c = {target:5.1f} K, use depth/bore = "
                  f"{plan_geometry(target)*1000:.2f} mm")
        print("  (a 250 mm column would reach onset at ~1e-5 K -- unmeasurable, which is why the "
              "original tall-cylinder design was replaced)")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[1] == "--self-test":
        return _self_test()
    rows = load_csv(argv[1])
    if not rows:
        print(f"No rows read from {argv[1]}.")
        return 1
    print(compare_onset(rows).report())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
