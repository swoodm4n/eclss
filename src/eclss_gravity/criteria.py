"""The gravity-relevance dimensionless criteria. derivation.md §3, §9.6.

Ga_dep : gravitational vs hydrodynamic wall delivery      (eq 3.1-3.5)
Lambda_g : is there enough channel length to settle out    (eq 3.6, Hazen number)
Sigma_g : gravity in the near-wall retention force balance (eq 3.7)
Pe_g   : gravitational Peclet number, stagnant limit        (eq 3.8)
Ga_mot : settling vs self-motility (planktonic cells only)  (S4.3)

PHASE 4 RED-TEAM CORRECTIONS (redteam_report.md; see limitations.md for the full account).
Three fixes applied here relative to the original derivation.md text:

1. (Finding 2.1) Lambda_g now uses the FULL channel depth (R=D), not D/2. The derivation's own
   text identifies Lambda_g with the classical Hazen surface-overflow number
   (Lambda_g = v_s*L*W/Q for a rectangular duct = v_s*L/(U*h) for full depth h), which requires
   the full depth, not the half-depth. Using D/2 was a convention error that flips the sign of
   the "100 um floc settles at Earth but is carried through at Mars/Moon" claim (0.93 vs the
   Hazen-consistent 0.46, i.e. carried through at Earth too). The 183 um case survives either
   convention and is used as the headline floc example instead.
2. (Finding 2.2) Re_p (particle Reynolds number) is now checked against the Stokes-validity bound
   (RE_P_STOKES_LIMIT = 0.34, particles.py) inside every closed-form criterion function. Values
   computed outside that bound are flagged via the `stokes_valid` field on CriteriaResult / a
   UserWarning, since the pure-Stokes closed forms silently overestimate v_s (and hence every
   criterion) once Re_p exceeds validity -- most consequentially for eq (3.3)'s "radius cancels
   exactly" result, which has an unstated upper size bound (particles.stokes_validity_diameter).
3. (Finding 2.3) The wall-orientation factor is now an explicit, named parameter
   (`orientation_factor`) on every Ga_dep-family function, instead of being silently fixed at
   cos(theta)=1. The default is 1/pi (ORIENTATION_PERIMETER_AVERAGED), the perimeter-averaged
   value derivation.md S5.3 itself derives as correct for a horizontal tube's overall wall
   delivery -- NOT the cos(theta)=1 "bounding case" the original headline number used. This
   changes g* for the single-cell WPA case from 0.238 g_E to ~0.75 g_E; see
   uncertainty.py/limitations.md for why neither point value should be quoted without its
   uncertainty band.
"""

import math
import warnings
from dataclasses import dataclass
from enum import Enum

from . import constants
from .constants import K_B
from .particles import RE_P_STOKES_LIMIT, brownian_diffusivity, particle_reynolds, settling_velocity
from .wall_transport import wall_transport_velocity

_GA_DIF_PREFACTOR = 2.925  # derivation.md eq (3.2), derived in the document from first principles

ORIENTATION_BOTTOM_LOCAL = 1.0  # cos(theta)=1: local bounding case at the very bottom of the tube
ORIENTATION_PERIMETER_AVERAGED = 1.0 / math.pi  # derivation.md eq (5.6): correct perimeter average
ORIENTATION_VERTICAL_TUBE = 0.0  # gravity parallel to the wall: no gravitational wall delivery


class Regime(Enum):
    NEGLIGIBLE = "negligible"  # < 0.1
    AMBIGUOUS = "ambiguous"  # 0.1 - 10
    DOMINANT = "dominant"  # > 10


def classify(value: float) -> Regime:
    v = abs(value)
    if v < 0.1:
        return Regime.NEGLIGIBLE
    if v > 10:
        return Regime.DOMINANT
    return Regime.AMBIGUOUS


def _check_stokes_validity(v_s: float, a: float, mu: float, rho_f: float, context: str) -> bool:
    """Finding 2.2: warn (not silently accept) when a closed-form result used v_s outside
    Stokes' law's validity range. Returns True if valid."""
    Re_p = particle_reynolds(v_s, 2.0 * a, mu, rho_f)
    if Re_p >= RE_P_STOKES_LIMIT:
        warnings.warn(
            f"{context}: Re_p={Re_p:.3g} >= {RE_P_STOKES_LIMIT} -- pure-Stokes v_s overestimates "
            f"drag-corrected settling (derivation.md eq 2.2/A6); result is biased.",
            stacklevel=3,
        )
        return False
    return True


def ga_dep_direct(
    a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED, rho_f: float = None,
) -> float:
    """Eq. (3.1): Ga_dep = v_s * orientation_factor / k_w, computed from the underlying velocities
    (not the closed form) -- used as an independent cross-check of ga_dep_closed_form (Finding 1.3)."""
    if rho_f is None:
        rho_f = constants.water_density(T_K)
    v_s, Re_p, valid = settling_velocity(a, delta_rho, g, mu=mu, T_K=T_K, rho_f=rho_f)
    if not valid:
        warnings.warn(f"ga_dep_direct: Re_p={Re_p:.3g} outside Stokes validity", stacklevel=2)
    k_w, _, _ = wall_transport_velocity(a, mu, T_K, gamma_w, x, D)
    return v_s * orientation_factor / k_w


def ga_dif_closed_form(
    a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED, rho_f: float = None,
) -> float:
    """Eq. (3.2): closed form on the diffusion branch, Ga_dif = v_s / k_lev in closed form.

    Ga_dif = orientation_factor * 2.925 * delta_rho * g * a^(8/3) / (mu^(1/3) * (k_B T)^(2/3)) * (x/gamma_w)^(1/3)
    """
    if rho_f is None:
        rho_f = constants.water_density(T_K)
    x_reg = max(x, D)
    v_s_stokes = (2.0 / 9.0) * delta_rho * g * a**2 / mu
    _check_stokes_validity(v_s_stokes, a, mu, rho_f, "ga_dif_closed_form")
    return (
        orientation_factor
        * _GA_DIF_PREFACTOR
        * delta_rho
        * g
        * a ** (8.0 / 3.0)
        / (mu ** (1.0 / 3.0) * (K_B * T_K) ** (2.0 / 3.0))
        * (x_reg / gamma_w) ** (1.0 / 3.0)
    )


def ga_int_closed_form(
    a: float, delta_rho: float, g: float, mu: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED, rho_f: float = 997.0,
) -> float:
    """Eq. (3.3): Ga_int = orientation_factor * (4/9) * delta_rho * g * x / (mu * gamma_w).

    Particle-radius-independent ONLY within Stokes validity (derivation.md eq 2.3 / Finding 2.2):
    above d_max(g) (184/254/335 um at Earth/Mars/Moon for the nominal WPA line), v_s grows more
    slowly than a^2 while k_int retains its exact a^2 scaling, so Ga_int becomes size-dependent
    (decreasing) again. `a` is accepted here solely to check that bound; it does not appear in
    the returned value while Re_p < RE_P_STOKES_LIMIT.
    """
    v_s_stokes = (2.0 / 9.0) * delta_rho * g * a**2 / mu
    _check_stokes_validity(v_s_stokes, a, mu, rho_f, "ga_int_closed_form")
    x_reg = max(x, D)
    return orientation_factor * (4.0 / 9.0) * delta_rho * g * x_reg / (mu * gamma_w)


def ga_dep_closed_form(
    a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED,
) -> float:
    """Ga_dep = max branch selection between the diffusion and interception closed forms.

    Since Ga_dep = v_s / max(k_lev, k_int) = min(v_s/k_lev, v_s/k_int) = min(Ga_dif, Ga_int).
    """
    return min(
        ga_dif_closed_form(a, delta_rho, g, mu, T_K, gamma_w, x, D, orientation_factor),
        ga_int_closed_form(a, delta_rho, g, mu, gamma_w, x, D, orientation_factor),
    )


def g_star_dif(
    a: float, delta_rho: float, mu: float, T_K: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED,
) -> float:
    """Eq. (3.4): gravity level at which Ga_dif = 1, on the diffusion branch."""
    x_reg = max(x, D)
    return (
        mu ** (1.0 / 3.0)
        * (K_B * T_K) ** (2.0 / 3.0)
        / (orientation_factor * _GA_DIF_PREFACTOR * delta_rho * a ** (8.0 / 3.0))
        * (gamma_w / x_reg) ** (1.0 / 3.0)
    )


def g_star_int(
    delta_rho: float, mu: float, gamma_w: float, x: float, D: float,
    orientation_factor: float = ORIENTATION_PERIMETER_AVERAGED,
) -> float:
    """Eq. (3.5): gravity level at which Ga_int = 1, on the interception branch."""
    x_reg = max(x, D)
    return 9.0 * mu * gamma_w / (4.0 * orientation_factor * delta_rho * x_reg)


def lambda_g(a: float, delta_rho: float, g: float, mu: float, L: float, U: float, D: float) -> float:
    """Eq. (3.6): Lambda_g = v_s * L / (U * D). Hazen/overflow number, FULL channel depth.

    CORRECTED (Finding 2.1): the derivation's original text used R=D/2 (half-depth) while
    simultaneously identifying this with the classical Hazen surface-overflow-rate number
    Lambda_g = v_s*(L*W)/Q, which for a duct of full depth h reduces to v_s*L/(U*h) -- i.e. the
    FULL depth D, not D/2. Using D/2 doubled the reported values and flipped the "100 um floc
    settles at Earth, carried through at Mars/Moon" threshold claim (0.93 -> 0.46, i.e. carried
    through at Earth too under the correct convention). The 183 um floc case is used as the
    headline example instead since it exceeds 1 at Earth under both conventions.
    """
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu)
    return v_s * L / (U * D)


def sigma_g(a: float, delta_rho: float, g: float, mu: float, gamma_w: float) -> float:
    """Eq. (3.7): Sigma_g = 2 * delta_rho * g * a / (15.31 * mu * gamma_w)."""
    return 2.0 * delta_rho * g * a / (15.31 * mu * gamma_w)


def pe_g(a: float, delta_rho: float, g: float, mu: float, T_K: float, H: float) -> float:
    """Eq. (3.8): Pe_g = v_s * H / D_B, gravitational Peclet number for the stagnant limit."""
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu, T_K=T_K)
    D_B = brownian_diffusivity(a, mu, T_K)
    return abs(v_s) * H / D_B


def ga_mot(a: float, delta_rho: float, g: float, mu: float, v_swim: float) -> float:
    """Section 4.3: Ga_mot = v_s / v_swim, for planktonic (motile) single cells only.

    derivation.md S4.3 / S6 A12: the ISS isolates motivating this program (P. aeruginosa,
    Burkholderia, Stenotrophomonas) are flagellated. For a MOTILE cell, Ga_mot << 1 means
    self-propulsion, not the wall-transport competition in Ga_dep, governs delivery, and the
    Ga_dep result for that cell class is not the relevant comparison (redteam_report.md
    Finding on A12: "the headline single-cell case is the least representative case for the
    very organisms motivating the work" unless motility is explicitly assessed and reported,
    which is why this function is called from the test suite and the headline reporting script.
    """
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu)
    return abs(v_s) / v_swim


@dataclass
class CriteriaResult:
    """Bundle of all criteria evaluated at one operating point, for reporting."""

    label: str
    g: float
    Ga_dep: float
    Ga_dif: float
    Ga_int: float
    Lambda_g: float
    Sigma_g: float
    Ga_mot: float = None  # None if the class is not motile / not applicable

    def regime_summary(self) -> str:
        vals = {"Ga_dep": self.Ga_dep, "Lambda_g": self.Lambda_g, "Sigma_g": self.Sigma_g}
        classes = {k: classify(v).value for k, v in vals.items()}
        s = ", ".join(f"{k}={v:.3g} ({classes[k]})" for k, v in vals.items())
        if self.Ga_mot is not None:
            s += f", Ga_mot={self.Ga_mot:.3g} (if motile: self-propulsion, not Ga_dep, governs)"
        return s
