"""Regression tests against docs/derivation.md §2.2(b) buoyancy table."""

import pytest

from eclss_gravity import buoyancy, constants

NU = constants.water_kinematic_viscosity()
ALPHA_TH = constants.water_thermal_diffusivity()
BETA = constants.water_thermal_expansion()


@pytest.mark.parametrize(
    "g,H,expected_dT_c",
    [
        (constants.G_EARTH, 6.35e-3, 0.345),
        (constants.G_MARS, 6.35e-3, 0.912),
        (constants.G_MOON, 6.35e-3, 2.088),
        (constants.G_EARTH, 0.30, 3.27e-6),
        (constants.G_MARS, 0.30, 8.65e-6),
        (constants.G_MOON, 0.30, 1.98e-5),
    ],
)
def test_critical_delta_T(g, H, expected_dT_c):
    dT_c = buoyancy.critical_delta_T(g, BETA, H, NU, ALPHA_TH)
    assert dT_c == pytest.approx(expected_dT_c, rel=0.03)


def test_rayleigh_number_line_1K_earth():
    Ra = buoyancy.rayleigh_number(constants.G_EARTH, BETA, 1.0, 6.35e-3, NU, ALPHA_TH)
    assert Ra == pytest.approx(4953, rel=0.03)


def test_rayleigh_number_line_1K_moon_below_critical():
    """derivation.md §2.2(b): at lunar g, Ra=818 < Ra_c=1708 -> convection OFF.

    This is the counter-intuitive headline result: lowering gravity can suppress
    the buoyant convection that would otherwise resuspend settled cells.
    """
    Ra = buoyancy.rayleigh_number(constants.G_MOON, BETA, 1.0, 6.35e-3, NU, ALPHA_TH)
    assert Ra == pytest.approx(818, rel=0.03)
    assert Ra < constants.RA_C
    u_conv = buoyancy.convective_velocity(Ra, 6.35e-3, NU, constants.G_MOON, BETA, 1.0)
    assert u_conv == 0.0


def test_convective_velocity_tank_earth():
    Ra = buoyancy.rayleigh_number(constants.G_EARTH, BETA, 0.1, 0.30, NU, ALPHA_TH)
    u_conv = buoyancy.convective_velocity(Ra, 0.30, NU, constants.G_EARTH, BETA, 0.1)
    # derivation.md §2.2(b): u_conv ~= 8.70e-4 m/s
    assert u_conv == pytest.approx(8.70e-4, rel=0.1)
