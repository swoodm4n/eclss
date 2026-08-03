"""Regression tests against docs/derivation.md §3.5 (stagnant/dormancy limit)."""

import pytest

from eclss_gravity import constants, dormancy, particles

MU = constants.water_viscosity()


@pytest.mark.parametrize(
    "g,expected_hours",
    [
        (constants.G_EARTH, 26.2),
        (constants.G_MARS, 69.2),
        (constants.G_MOON, 158.0),
    ],
)
def test_t_settle_cell_line(g, expected_hours):
    t = dormancy.time_to_settle(particles.P1_CELL.a, particles.P1_CELL.delta_rho, g, H=6.35e-3, mu=MU)
    assert t / 3600.0 == pytest.approx(expected_hours, rel=0.03)


@pytest.mark.parametrize(
    "g,expected_days",
    [
        (constants.G_EARTH, 51.5),
        (constants.G_MARS, 136.0),
        (constants.G_MOON, 312.0),
    ],
)
def test_t_settle_cell_tank(g, expected_days):
    t = dormancy.time_to_settle(particles.P1_CELL.a, particles.P1_CELL.delta_rho, g, H=0.30, mu=MU)
    assert t / 86400.0 == pytest.approx(expected_days, rel=0.03)


def test_settling_rate_constant_matches_pure_settling_limit():
    """When D_v -> 0 (no diffusion/convection), k = v_s/H exactly (1/t_settle)."""
    v_s, _, _ = particles.settling_velocity(particles.P1_CELL.a, particles.P1_CELL.delta_rho, constants.G_EARTH, mu=MU)
    H = 6.35e-3
    k = dormancy.settling_rate_constant(v_s, H, D_v=1e-30)
    assert k == pytest.approx(abs(v_s) / H, rel=1e-6)


def test_dormancy_simulation_runs_and_deposits_over_a_year():
    from eclss_gravity import kinetics as kin

    classes = [particles.P1_CELL, particles.P3_MEDIAN_FLOC]
    C0 = {particles.P1_CELL.label: 1e-6, particles.P3_MEDIAN_FLOC.label: 1e-7}
    result = dormancy.simulate_dormancy(
        classes, C0, S0=2000.0, H=0.30, g=constants.G_EARTH, duration_s=3.156e7,
        kinetic_params=kin.KineticParams(), n_eval=50,
    )
    assert result.X[-1] > result.X[0]
    assert result.X[-1] > 0
    # floc (faster settling) should deposit more mass than the cell fraction contributes proportionally
    assert result.C[particles.P3_MEDIAN_FLOC.label][-1] < C0[particles.P3_MEDIAN_FLOC.label]
