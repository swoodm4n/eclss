"""Particle classes and settling kinematics. derivation.md §1.4, §2.1, §8.3."""

from dataclasses import dataclass

from . import constants


@dataclass(frozen=True)
class ParticleClass:
    """A biological particle class (single cell, aggregate, or floc).

    d: equivalent-sphere diameter (m)
    delta_rho: excess (buoyant) density rho_p - rho_f, nominal value (kg/m^3)
    delta_rho_range: (low, high) sourced/derived range, for uncertainty propagation
    label: human-readable name
    """

    label: str
    d: float
    delta_rho: float
    delta_rho_range: tuple[float, float]

    @property
    def a(self) -> float:
        """Equivalent-sphere radius (m)."""
        return self.d / 2.0


# derivation.md §1.4 table. P1 uses the E. coli buoyant-density proxy (A25),
# P2-P5 use the activated-sludge floc density range (A26) -- both flagged
# as cross-species/cross-system substitutions in the derivation's assumptions table.
P1_CELL = ParticleClass("P1 single cell", d=1.088e-6, delta_rho=93.0, delta_rho_range=(83.0, 103.0))
P2_SMALL_AGGREGATE = ParticleClass("P2 small aggregate (7 um)", d=7e-6, delta_rho=50.0, delta_rho_range=(38.0, 68.0))
P3_MEDIAN_FLOC = ParticleClass("P3 median floc (100 um)", d=100e-6, delta_rho=50.0, delta_rho_range=(38.0, 68.0))
P4_LARGE_FLOC = ParticleClass("P4 large floc (183 um)", d=183e-6, delta_rho=50.0, delta_rho_range=(38.0, 68.0))
P5_SLOUGHED = ParticleClass("P5 sloughed piece (500 um)", d=500e-6, delta_rho=50.0, delta_rho_range=(38.0, 68.0))

ALL_CLASSES = (P1_CELL, P2_SMALL_AGGREGATE, P3_MEDIAN_FLOC, P4_LARGE_FLOC, P5_SLOUGHED)

V_SWIM_P_PUTIDA = 32.1e-6  # m/s, derivation.md §2.5, [snippet-level]

# Schiller-Naumann Reynolds number below which Stokes' law (eq 2.1) is used
# directly; above it, the implicit correction (eq 2.2) is applied.
# derivation.md §2.1 / §6.2 A6: Re_p < 0.34 for < 5% Stokes error.
RE_P_STOKES_LIMIT = 0.34


def stokes_settling_velocity(a: float, delta_rho: float, g: float, mu: float) -> float:
    """Eq. (2.1): v_s = (2/9) * delta_rho * g * a^2 / mu. Signed: negative delta_rho -> rises."""
    return (2.0 / 9.0) * delta_rho * g * a**2 / mu


def particle_reynolds(v_s: float, d: float, mu: float, rho_f: float) -> float:
    return rho_f * abs(v_s) * d / mu


def settling_velocity(
    a: float,
    delta_rho: float,
    g: float,
    mu: float = None,
    rho_f: float = None,
    T_K: float = 298.15,
    max_iter: int = 100,
    tol: float = 1e-10,
) -> tuple[float, float, bool]:
    """Settling velocity with Schiller-Naumann correction (eq 2.2) when Re_p exceeds validity.

    Returns (v_s, Re_p, stokes_regime_valid).

    Fixed-point iteration on the implicit Schiller-Naumann drag law:
        v_s = v_stokes / (1 + 0.15 * Re_p^0.687)
    with Re_p evaluated at the current v_s estimate (derivation.md eq 2.2).
    """
    if mu is None:
        mu = constants.water_viscosity(T_K)
    if rho_f is None:
        rho_f = constants.water_density(T_K)

    v_stokes = stokes_settling_velocity(a, delta_rho, g, mu)
    if v_stokes == 0.0:
        return 0.0, 0.0, True

    sign = 1.0 if v_stokes >= 0 else -1.0
    v_mag = abs(v_stokes)
    d = 2.0 * a

    for _ in range(max_iter):
        Re_p = particle_reynolds(v_mag, d, mu, rho_f)
        if Re_p < RE_P_STOKES_LIMIT:
            return sign * v_mag, Re_p, True
        drag_factor = 1.0 + 0.15 * Re_p**0.687
        v_new = abs(v_stokes) / drag_factor
        if abs(v_new - v_mag) < tol * max(v_mag, 1e-30):
            v_mag = v_new
            break
        v_mag = v_new

    Re_p = particle_reynolds(v_mag, d, mu, rho_f)
    return sign * v_mag, Re_p, False


def brownian_diffusivity(a: float, mu: float, T_K: float = 298.15) -> float:
    """Eq. (2.11): Stokes-Einstein D_B = k_B T / (6 pi mu a)."""
    return constants.K_B * T_K / (6.0 * 3.141592653589793 * mu * a)


def stokes_validity_diameter(delta_rho: float, mu: float, rho_f: float, g: float, re_p_target: float = RE_P_STOKES_LIMIT) -> float:
    """Eq. (2.3): largest diameter for which Stokes' law holds to ~5% (Re_p = 0.34).

    Solved numerically since v_s and Re_p are coupled through d.
    """
    from scipy.optimize import brentq

    def f(d):
        a = d / 2.0
        v_stokes = stokes_settling_velocity(a, delta_rho, g, mu)
        Re_p = particle_reynolds(v_stokes, d, mu, rho_f)
        return Re_p - re_p_target

    # bracket search
    lo, hi = 1e-8, 1e-2
    if f(lo) > 0:
        return lo
    while f(hi) < 0 and hi < 1.0:
        hi *= 2
    return brentq(f, lo, hi)
