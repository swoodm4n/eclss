"""Regression tests against the exact numeric values stated in docs/derivation.md §9.6.

These pin the implementation to the derivation document. If a value here needs to
change, derivation.md must be updated first and the reason recorded in decision_log.md.
"""

import math

import pytest

from eclss_gravity import constants, criteria, hydrodynamics, particles

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
    # derivation.md §1.3 table: Re=368, gamma_w=65.2 /s (rounding of sourced 13 lb/hr)
    assert Re == pytest.approx(368, rel=0.02)
    assert gamma_w == pytest.approx(65.2, rel=0.02)


def test_ga_dif_p1_r1_earth():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.ga_dif_closed_form(
        particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, gamma_w, r1.L, r1.D
    )
    # derivation.md §9.6 regression: 4.2035
    assert val == pytest.approx(4.2035, rel=0.02)


def test_ga_int_r1_earth_is_particle_independent():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.ga_int_closed_form(particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, gamma_w, r1.L, r1.D)
    # derivation.md §9.6 regression: 1878
    assert val == pytest.approx(1878, rel=0.02)
    # radius-independence: same delta_rho, different radius -> identical result
    val_p4 = criteria.ga_int_closed_form(particles.P4_LARGE_FLOC.delta_rho, G_E, MU, gamma_w, r1.L, r1.D)
    assert val == pytest.approx(val_p4, rel=1e-9)


def test_g_star_int_r1():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    gstar = criteria.g_star_int(particles.P3_MEDIAN_FLOC.delta_rho, MU, gamma_w, r1.L, r1.D)
    # derivation.md §9.6 regression: 5.32e-4 g_E
    assert gstar / G_E == pytest.approx(5.32e-4, rel=0.02)


def test_lambda_g_p3_r1_earth():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    val = criteria.lambda_g(particles.P3_MEDIAN_FLOC.a, particles.P3_MEDIAN_FLOC.delta_rho, G_E, MU, r1.L, r1.U, r1.D)
    # derivation.md §9.6 regression: 0.932
    assert val == pytest.approx(0.932, rel=0.03)


def test_sigma_g_p4_r1_earth():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    val = criteria.sigma_g(particles.P4_LARGE_FLOC.a, particles.P4_LARGE_FLOC.delta_rho, G_E, MU, gamma_w)
    # derivation.md §9.6 regression: 0.101
    assert val == pytest.approx(0.101, rel=0.03)


def test_pe_g_p1_stagnant_earth():
    val = criteria.pe_g(particles.P1_CELL.a, particles.P1_CELL.delta_rho, G_E, MU, T_K, H=6.35e-3)
    # derivation.md §9.6 regression: 950
    assert val == pytest.approx(950, rel=0.03)


def test_g_star_headline_single_cell_wpa_between_mars_and_moon():
    """The paper's central result: g* for single-cell deposition sits between lunar and Mars g."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w = _gamma_w(r1)
    gstar = criteria.g_star_dif(particles.P1_CELL.a, particles.P1_CELL.delta_rho, MU, T_K, gamma_w, r1.L, r1.D)
    # derivation.md §3.2/§8.6: g*_dif = 0.238 g_E, between Moon (0.165 g_E) and Mars (0.378 g_E)
    assert gstar / G_E == pytest.approx(0.238, rel=0.05)
    assert constants.G_MOON < gstar < constants.G_MARS


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
