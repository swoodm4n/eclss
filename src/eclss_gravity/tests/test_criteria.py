"""Regression tests against docs/derivation.md §9.6, CORRECTED per docs/redteam_report.md.

Where a red-team finding changed a formula or default (Lambda_g depth convention, Finding 2.1;
orientation_factor default, Finding 2.3), the test checks the corrected behavior AND retains a
check of the original derivation.md number under the ORIGINAL convention, so both the algebra
(still correct) and the fix (now applied by default) are pinned. See criteria.py's module
docstring for the full account.
"""

import math

import pytest

from eclss_gravity import constants, criteria, hydrodynamics, particles, wall_transport

T_K = 298.15
MU = constants.water_viscosity(T_K)
RHO_F = constants.water_density(T_K)
G_E = constants.G_EARTH


def _gamma_w(regime):
    gamma_w, tau_w, u_star = hydrodynamics.wall_shear(regime.U, regime.D, RHO_F, MU)
    return gamma_w


def test_r1_reynolds_and_shear_match_derivation_table():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    Re = hydrodynamics.reynolds_number(r1.U, r1.D, RHO_F, MU)
    gamma_w = _gamma_w(r1)
    # derivation.md §1.3 table: Re=368, gamma_w=65.2 /s (rounding of sourced 13 lb/hr;
    # redteam_report.md Finding 1.2 notes a 0.3% units-slip offset in the document's own table)
    assert Re == pytest.approx(368, rel=0.02)
    assert gamma_w == pytest.approx(65.2, rel=0.02)


def test_ga_dif_p1_r1_earth_original_convention():
    """Original derivation.md value under cos(theta)=1 (the document's stated convention there)."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.ga_dif_closed_form(
        particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D,
        orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL,
    )
    # derivation.md §9.6 regression: 4.2035
    assert val == pytest.approx(4.2035, rel=0.02)


def test_ga_dif_p1_r1_earth_default_orientation():
    """redteam_report.md Finding 2.3: the perimeter-averaged default gives a different Ga_dep."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.ga_dif_closed_form(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    assert val == pytest.approx(4.2035 / math.pi, rel=0.02)  # ~1.34, matches redteam_report.md §2.3


def test_ga_int_r1_earth_is_particle_independent_within_stokes_validity():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.ga_int_closed_form(
        particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, gamma_w, r1.L, r1.D,
        orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL,
    )
    # derivation.md §9.6 regression: 1878
    assert val == pytest.approx(1878, rel=0.02)
    # radius-independence within Stokes validity: same delta_rho, different (but still-valid) radius
    val_p4 = criteria.ga_int_closed_form(
        particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, G_E, MU, gamma_w, r1.L, r1.D,
        orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL,
    )
    assert val == pytest.approx(val_p4, rel=1e-9)


def test_ga_int_size_independence_breaks_down_above_stokes_validity():
    """redteam_report.md Finding 2.2: the 'radius cancels' result has an unstated upper bound.

    P5 (500 um, Re_p=4.29 at Earth) is outside Stokes validity; a warning must fire, and the
    TRUE (drag-corrected) Ga is measurably below the naive closed-form value that ignores it.
    """
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    with pytest.warns(UserWarning, match="Re_p"):
        ga_int_naive = criteria.ga_int_closed_form(
            particles.P5_SLOUGHED.a, particles.P5_SLOUGHED.delta_rho, G_E, MU, gamma_w, r1.L, r1.D,
            orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL,
        )
    # ga_int_closed_form is radius-independent BY FORM even when the warning fires (it does not
    # itself apply the correction) -- the warning is the documented signal that the caller must.
    v_s_corrected, Re_p, valid = particles.settling_velocity(particles.P5_SLOUGHED.a, particles.P5_SLOUGHED.delta_rho, G_E, mu=MU, T_K=T_K)
    assert not valid
    assert Re_p > particles.RE_P_STOKES_LIMIT


def test_g_star_int_r1_original_convention():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    gstar = criteria.g_star_int(particles.P3_MEDIAN_FLOC.delta_rho, MU, gamma_w, r1.L, r1.D, orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL)
    # derivation.md §9.6 regression: 5.32e-4 g_E
    assert gstar / G_E == pytest.approx(5.32e-4, rel=0.02)


def test_lambda_g_p3_r1_earth_corrected_depth_convention():
    """CORRECTED (Finding 2.1): full-depth R=D, not the original half-depth D/2.

    The original derivation.md value (0.932) used R=D/2; the Hazen-consistent value is exactly
    half of that. This is why the manuscript uses the 183 um floc, not the 100 um floc, as its
    headline size-selective example (see criteria.lambda_g docstring and limitations.md).
    """
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    val = criteria.lambda_g(particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, r1.L, r1.U, r1.D)
    assert val == pytest.approx(0.932 / 2.0, rel=0.03)


def test_lambda_g_p4_183um_still_exceeds_one_at_earth_only():
    """The 183 um floc survives the depth-convention correction as the headline example:
    Lambda_g > 1 at Earth, < 1 at Mars and Moon, under the corrected full-depth convention."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    lam_earth = criteria.lambda_g(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, constants.G_EARTH, MU, r1.L, r1.U, r1.D)
    lam_mars = criteria.lambda_g(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, constants.G_MARS, MU, r1.L, r1.U, r1.D)
    lam_moon = criteria.lambda_g(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, constants.G_MOON, MU, r1.L, r1.U, r1.D)
    assert lam_earth > 1.0
    assert lam_mars < 1.0
    assert lam_moon < 1.0
    assert lam_earth > lam_mars > lam_moon


def test_sigma_g_p4_r1_earth():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.sigma_g(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, G_E, MU, gamma_w)
    # derivation.md §9.6 regression: 0.101 (Sigma_g is unaffected by both corrections above)
    assert val == pytest.approx(0.101, rel=0.03)


def test_pe_g_p1_stagnant_earth():
    val = criteria.pe_g(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, H=6.35e-3)
    # derivation.md §9.6 regression: 950
    assert val == pytest.approx(950, rel=0.03)


def test_g_star_single_cell_wpa_is_convention_and_uncertainty_sensitive():
    """CORRECTED (Finding 2.3, Finding 4.8): replaces the retracted
    'g* = 0.238 g_E, between lunar and Mars gravity' headline-claim test.

    That single point estimate is not defensible: it is convention-dependent (0.238 g_E under
    the local bottom-of-tube bound vs 0.749 g_E under the perimeter-averaged default) and
    over-precise by ~50x across the derivation's own assumed-parameter ranges
    (redteam_report.md Finding 4.8). This test instead pins the DIRECTION and MAGNITUDE of that
    sensitivity, which is the actually-defensible, reportable finding.
    """
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    gstar_local = criteria.g_star_dif(particles.P1_CELL.a, particles.P1_CELL.delta_rho, MU, T_K, gamma_w, r1.L, r1.D, orientation_factor=criteria.ORIENTATION_BOTTOM_LOCAL)
    gstar_averaged = criteria.g_star_dif(particles.P1_CELL.a, particles.P1_CELL.delta_rho, MU, T_K, gamma_w, r1.L, r1.D, orientation_factor=criteria.ORIENTATION_PERIMETER_AVERAGED)
    assert gstar_local / G_E == pytest.approx(0.238, rel=0.05)
    assert gstar_averaged / G_E == pytest.approx(0.749, rel=0.05)
    # both are within roughly an order of magnitude of the Earth-Moon gravity range itself --
    # that comparability, not a precise crossover point, is the defensible claim (see
    # limitations.md and redteam_report.md's "Recommended reframe").
    assert 0.05 * G_E < gstar_local < 5 * G_E
    assert 0.05 * G_E < gstar_averaged < 5 * G_E


def test_ga_dep_closed_form_agrees_with_direct_velocity_ratio():
    """redteam_report.md Finding 1.3: §9.6 requires this cross-check and it was absent.

    ~0.02% residual is expected and harmless: the closed form's 2.925 prefactor is the exact
    algebraic constant, while ga_dep_direct routes through wall_transport's rounded 0.538
    Leveque prefactor -- both internally self-consistent, differing only in that rounding.
    """
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    closed = criteria.ga_dep_closed_form(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    direct = criteria.ga_dep_direct(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    assert closed == pytest.approx(direct, rel=1e-3)


def test_ga_dep_closed_form_equals_min_of_branches():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    ga_dep = criteria.ga_dep_closed_form(particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    ga_dif = criteria.ga_dif_closed_form(particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    ga_int = criteria.ga_int_closed_form(particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, gamma_w, r1.L, r1.D)
    assert ga_dep == pytest.approx(min(ga_dif, ga_int), rel=1e-9)


def test_crossover_radius_closed_form_matches_root_find():
    """redteam_report.md Finding 1.3: a_c closed form vs. direct root-find of k_lev=k_int."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    a_c = wall_transport.crossover_radius(MU, T_K, gamma_w, r1.L, r1.D)

    from scipy.optimize import brentq

    def f(a):
        k_lev = wall_transport.leveque_deposition_velocity(particles.brownian_diffusivity(a, MU, T_K), gamma_w, r1.L, r1.D)
        k_int = wall_transport.interception_deposition_velocity(gamma_w, a, r1.L, r1.D)
        return k_lev - k_int

    a_c_rootfind = brentq(f, 1e-9, 1e-3)
    assert a_c == pytest.approx(a_c_rootfind, rel=1e-4)
    # derivation.md §9.10: a_c ~ 6.8 um for R1 (this report's independent check got 6.765/6.766 um)
    assert a_c * 1e6 == pytest.approx(6.77, rel=0.02)


def test_ga_mot_shows_motile_cells_are_dominated_by_swimming_not_settling():
    """derivation.md §4.3 / §6 A12; redteam_report.md: motile ISS isolates are the LEAST
    representative case for Ga_dep, which is why Ga_mot must be reported alongside it."""
    ga_mot = criteria.ga_mot(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, particles.V_SWIM_P_PUTIDA)
    assert ga_mot < 0.01  # settling is negligible vs swimming, by ~500x per derivation.md §2.5


def test_regime_classifier_boundaries():
    assert criteria.classify(0.05) == criteria.Regime.NEGLIGIBLE
    assert criteria.classify(1.0) == criteria.Regime.AMBIGUOUS
    assert criteria.classify(100.0) == criteria.Regime.DOMINANT


def test_stokes_schiller_naumann_agree_at_low_reynolds():
    """P1-P4 should stay in the Stokes-valid regime (derivation.md §2.1 A6)."""
    v_s, Re_p, valid = particles.settling_velocity(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, G_E, mu=MU, T_K=T_K)
    assert valid
    assert Re_p < particles.RE_P_STOKES_LIMIT


def test_schiller_naumann_engages_for_p5():
    """P5 (500 um) should trigger the Schiller-Naumann correction (derivation.md §2.1)."""
    v_s_stokes = particles.stokes_settling_velocity(particles.P5_SLOUGHED.a, particles.P5_SLOUGHED.delta_rho, G_E, MU)
    v_s_corrected, Re_p, valid = particles.settling_velocity(particles.P5_SLOUGHED.a, particles.P5_SLOUGHED.delta_rho, G_E, mu=MU, T_K=T_K)
    assert not valid
    assert v_s_corrected < v_s_stokes  # drag correction always reduces v_s
    # derivation.md §2.1: Stokes overestimates by ~33% at Earth g for P5
    assert (v_s_stokes - v_s_corrected) / v_s_corrected == pytest.approx(0.334, rel=0.1)


def test_stokes_validity_diameter_at_the_codebase_re_p_gate():
    """Checks stokes_validity_diameter against the RE_P_STOKES_LIMIT=0.34 gate actually used
    everywhere else in this codebase (particles.settling_velocity, criteria.py's warnings).

    NOTE on a minor documented inconsistency (not a code bug): derivation.md's prose states
    "Re_p ~= 0.34" is the boundary for "5% Stokes error" and quotes d_max=184/254/335 um at
    Earth/Mars/Moon, but its own worked example (P4, 183 um, Re_p=0.200) shows +5.0% error at
    Re_p=0.200, not 0.34. Solving the Schiller-Naumann correction factor for exactly 5% error
    gives Re_p ~= 0.20, not 0.34 -- Re_p=0.34 actually corresponds to ~7% error. This test
    therefore checks the diameter at the CODE's actual, consistently-applied Re_p=0.34 gate
    (~215 um at Earth), not the derivation prose's 184 um figure, and records the discrepancy
    here rather than silently using whichever number makes the test pass.
    """
    d_max_earth = particles.stokes_validity_diameter(50.0, MU, RHO_F, constants.G_EARTH)
    d_max_moon = particles.stokes_validity_diameter(50.0, MU, RHO_F, constants.G_MOON)
    assert d_max_earth < d_max_moon  # validity range widens as gravity falls (derivation.md §2.1)
    assert 150 < d_max_earth * 1e6 < 260  # ~215 um at the code's Re_p=0.34 gate


def test_entrance_length_flags_r1_as_not_fully_developed():
    """derivation.md A2: ~23% of the R1 0.5 m segment is not fully developed laminar flow."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    Re = hydrodynamics.reynolds_number(r1.U, r1.D, RHO_F, MU)
    L_e = hydrodynamics.entrance_length(Re, r1.D)
    assert L_e / r1.L == pytest.approx(0.234, rel=0.05)


def test_ga_dep_closed_form_sign_symmetric_for_negative_delta_rho():
    """Regression for a real bug found post-Phase-4 (A11 exploration): a naive
    min(Ga_dif, Ga_int) is only correct for delta_rho > 0. See criteria.ga_dep_closed_form
    docstring for the full explanation. |Ga_dep| must be IDENTICAL for +/-delta_rho of the
    same magnitude (only the sign, representing deposition-wall direction, should flip)."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    ga_sinking = criteria.ga_dep_closed_form(particles.P1_CELL.a, 93.0, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    ga_rising = criteria.ga_dep_closed_form(particles.P1_CELL.a, -93.0, G_E, MU, T_K, gamma_w, r1.L, r1.D)
    assert ga_sinking > 0
    assert ga_rising < 0
    assert abs(ga_sinking) == pytest.approx(abs(ga_rising), rel=1e-9)


def test_negative_delta_rho_sign_symmetry():
    """derivation.md A11: some biofilm is reported less dense than water (Delta_rho ~ -99
    kg/m^3), i.e. it would rise rather than settle. Criteria must not crash and the settling
    velocity must flip sign (deposits on top wall, not bottom) rather than silently going
    to the wrong magnitude."""
    v_s_pos, _, _ = particles.settling_velocity(particles.P1_CELL.a, 93.0, G_E, mu=MU, T_K=T_K)
    v_s_neg, _, _ = particles.settling_velocity(particles.P1_CELL.a, -99.0, G_E, mu=MU, T_K=T_K)
    assert v_s_pos > 0
    assert v_s_neg < 0
    assert abs(v_s_neg) == pytest.approx(abs(v_s_pos) * 99.0 / 93.0, rel=1e-6)
