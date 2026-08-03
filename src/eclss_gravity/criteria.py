"""The gravity-relevance dimensionless criteria. derivation.md §3, §9.6.

Ga_dep : gravitational vs hydrodynamic wall delivery      (eq 3.1-3.5)
Lambda_g : is there enough channel length to settle out    (eq 3.6, Hazen number)
Sigma_g : gravity in the near-wall retention force balance (eq 3.7)
Pe_g   : gravitational Peclet number, stagnant limit        (eq 3.8)
Ga_mot : settling vs self-motility (planktonic cells only)  (§4.3)
"""

import math
from dataclasses import dataclass
from enum import Enum

from .constants import K_B
from .particles import brownian_diffusivity, settling_velocity
from .wall_transport import wall_transport_velocity

_GA_DIF_PREFACTOR = 2.925  # derivation.md eq (3.2), derived in the document from first principles


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


def ga_dep_direct(a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float, cos_theta: float = 1.0) -> float:
    """Eq. (3.1): Ga_dep = v_s * cos(theta) / k_w, computed from the underlying velocities."""
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu, T_K=T_K)
    k_w, _, _ = wall_transport_velocity(a, mu, T_K, gamma_w, x, D)
    return v_s * cos_theta / k_w


def ga_dif_closed_form(a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (3.2): closed form on the diffusion branch, Ga_dif = v_s / k_lev in closed form.

    Ga_dif = 2.925 * delta_rho * g * a^(8/3) / (mu^(1/3) * (k_B T)^(2/3)) * (x/gamma_w)^(1/3)
    """
    x_reg = max(x, D)
    return (
        _GA_DIF_PREFACTOR
        * delta_rho
        * g
        * a ** (8.0 / 3.0)
        / (mu ** (1.0 / 3.0) * (K_B * T_K) ** (2.0 / 3.0))
        * (x_reg / gamma_w) ** (1.0 / 3.0)
    )


def ga_int_closed_form(delta_rho: float, g: float, mu: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (3.3): Ga_int = (4/9) * delta_rho * g * x / (mu * gamma_w). Particle-radius-independent."""
    x_reg = max(x, D)
    return (4.0 / 9.0) * delta_rho * g * x_reg / (mu * gamma_w)


def ga_dep_closed_form(a: float, delta_rho: float, g: float, mu: float, T_K: float, gamma_w: float, x: float, D: float) -> float:
    """Ga_dep = max branch selection between the diffusion and interception closed forms.

    Since Ga_dep = v_s / max(k_lev, k_int) = min(v_s/k_lev, v_s/k_int) = min(Ga_dif, Ga_int).
    """
    return min(
        ga_dif_closed_form(a, delta_rho, g, mu, T_K, gamma_w, x, D),
        ga_int_closed_form(delta_rho, g, mu, gamma_w, x, D),
    )


def g_star_dif(a: float, delta_rho: float, mu: float, T_K: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (3.4): gravity level at which Ga_dif = 1, on the diffusion branch."""
    x_reg = max(x, D)
    return (
        mu ** (1.0 / 3.0)
        * (K_B * T_K) ** (2.0 / 3.0)
        / (_GA_DIF_PREFACTOR * delta_rho * a ** (8.0 / 3.0))
        * (gamma_w / x_reg) ** (1.0 / 3.0)
    )


def g_star_int(delta_rho: float, mu: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (3.5): gravity level at which Ga_int = 1, on the interception branch."""
    x_reg = max(x, D)
    return 9.0 * mu * gamma_w / (4.0 * delta_rho * x_reg)


def lambda_g(a: float, delta_rho: float, g: float, mu: float, L: float, U: float, D: float) -> float:
    """Eq. (3.6): Lambda_g = v_s * L / (U * R), R = D/2. Hazen/overflow number."""
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu)
    R = D / 2.0
    return v_s * L / (U * R)


def sigma_g(a: float, delta_rho: float, g: float, mu: float, gamma_w: float) -> float:
    """Eq. (3.7): Sigma_g = 2 * delta_rho * g * a / (15.31 * mu * gamma_w)."""
    return 2.0 * delta_rho * g * a / (15.31 * mu * gamma_w)


def pe_g(a: float, delta_rho: float, g: float, mu: float, T_K: float, H: float) -> float:
    """Eq. (3.8): Pe_g = v_s * H / D_B, gravitational Peclet number for the stagnant limit."""
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu, T_K=T_K)
    D_B = brownian_diffusivity(a, mu, T_K)
    return abs(v_s) * H / D_B


def ga_mot(a: float, delta_rho: float, g: float, mu: float, v_swim: float) -> float:
    """Section 4.3: Ga_mot = v_s / v_swim, for planktonic (motile) single cells only."""
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
    branch: str  # "diffusion" or "interception"

    def regime_summary(self) -> str:
        vals = {"Ga_dep": self.Ga_dep, "Lambda_g": self.Lambda_g, "Sigma_g": self.Sigma_g}
        classes = {k: classify(v).value for k, v in vals.items()}
        return ", ".join(f"{k}={v:.3g} ({classes[k]})" for k, v in vals.items())
