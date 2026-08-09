"""Tests for the bench-data comparison script (validation/README.md Part A).

This module analyses experimental data that does not exist yet, so its correctness cannot be
established by running it on real results. These tests pin it against synthetic datasets with a
KNOWN true onset, so it is trustworthy the first time a real experimenter uses it.
"""

import pytest

from eclss_gravity import buoyancy, constants, validation_compare


def _rows_for(ra_outcomes, H=2.5e-3):
    """Build trial rows at Earth g whose Ra values are exactly `ra_outcomes` keys."""
    beta = constants.water_thermal_expansion()
    nu = constants.water_kinematic_viscosity()
    alpha_th = constants.water_thermal_diffusivity()
    rows = []
    for ra, mixed in ra_outcomes:
        delta_T = ra * nu * alpha_th / (constants.G_EARTH * beta * H**3)
        rows.append({"trial": len(rows), "delta_T_K": delta_T, "H_m": H,
                     "mixing_onset_s": 120 if mixed else ""})
    return rows


def test_self_test_passes():
    assert validation_compare._self_test() == 0


def test_consistent_verdict_when_bracket_contains_ra_c():
    rows = _rows_for([(900, False), (1400, False), (2500, True), (5000, True)])
    result = validation_compare.compare_onset(rows)
    assert result.verdict.startswith("CONSISTENT")
    assert result.bracket_consistent
    assert result.ra_highest_not_mixed < constants.RA_C < result.ra_lowest_mixed


def test_inconsistent_verdict_when_true_onset_is_higher():
    """The scientifically interesting outcome: tube geometry raises the effective Ra_c."""
    rows = _rows_for([(2000, False), (3000, False), (5000, True), (7000, True)])
    result = validation_compare.compare_onset(rows)
    assert result.verdict.startswith("INCONSISTENT")


def test_scattered_verdict_when_outcomes_overlap():
    rows = _rows_for([(3000, False), (1000, True)])
    result = validation_compare.compare_onset(rows)
    assert result.verdict.startswith("SCATTERED")
    assert not result.bracket_consistent


@pytest.mark.parametrize("ra,mixed", [(500, False), (9000, True)])
def test_inconclusive_verdict_for_one_sided_data(ra, mixed):
    rows = _rows_for([(ra, mixed)] * 3)
    result = validation_compare.compare_onset(rows)
    assert result.verdict.startswith("INCONCLUSIVE")


def test_blank_and_nan_onset_both_count_as_no_mixing():
    """Experimenters will record 'no mixing' inconsistently; both forms must parse the same."""
    H = 2.5e-3
    beta = constants.water_thermal_expansion()
    nu = constants.water_kinematic_viscosity()
    alpha_th = constants.water_thermal_diffusivity()
    delta_T = 800 * nu * alpha_th / (constants.G_EARTH * beta * H**3)
    for blank in ("", "  ", "nan", "-1"):
        rows = [{"trial": 0, "delta_T_K": delta_T, "H_m": H, "mixing_onset_s": blank}]
        result = validation_compare.compare_onset(rows)
        assert result.n_not_mixed == 1, f"{blank!r} should count as no-mixing"
        assert result.n_mixed == 0


def test_plan_geometry_inverts_critical_delta_T():
    """The design helper must round-trip exactly against the model it plans for."""
    for target_dT in (0.5, 1.0, 5.0, 11.0):
        H = validation_compare.plan_geometry(target_dT)
        dT = buoyancy.critical_delta_T(
            constants.G_EARTH, constants.water_thermal_expansion(), H,
            constants.water_kinematic_viscosity(), constants.water_thermal_diffusivity(),
        )
        assert dT == pytest.approx(target_dT, rel=1e-9)


def test_plan_geometry_reproduces_the_readme_design_table():
    """validation/README.md §A.1 quotes these depths; keep the doc and code in agreement."""
    assert validation_compare.plan_geometry(3.3) * 1000 == pytest.approx(3.0, abs=0.1)
    assert validation_compare.plan_geometry(5.7) * 1000 == pytest.approx(2.5, abs=0.1)
    assert validation_compare.plan_geometry(11.0) * 1000 == pytest.approx(2.0, abs=0.1)


def test_tube_geometry_correction_is_unity_for_on_prediction_onset():
    H = validation_compare.plan_geometry(5.0)
    assert validation_compare.tube_geometry_correction(5.0, H) == pytest.approx(1.0, rel=1e-9)


def test_tube_geometry_correction_scales_linearly_with_observed_onset():
    """A tube that only convects at 2x the predicted delta_T has an effective Ra_c 2x higher --
    which docs/limitations.md §4 says is enough to overturn the Figure 4 conclusion."""
    H = validation_compare.plan_geometry(5.0)
    assert validation_compare.tube_geometry_correction(10.0, H) == pytest.approx(2.0, rel=1e-9)
