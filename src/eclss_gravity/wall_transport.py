"""Hydrodynamic wall-transport velocities: Leveque diffusion and interception. derivation.md §2.4."""

import math

from .particles import brownian_diffusivity

_LEVEQUE_PREFACTOR = 0.538  # derivation.md eq (2.10): 1/(9^(1/3) * Gamma(4/3))


def leveque_deposition_velocity(D_B: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (2.10): k_lev = 0.538 * D_B^(2/3) * (gamma_w / x)^(1/3).

    x is regularised to max(x, D) per derivation.md §5.3 (the Leveque solution
    is singular at x=0).
    """
    x_reg = max(x, D)
    return _LEVEQUE_PREFACTOR * D_B ** (2.0 / 3.0) * (gamma_w / x_reg) ** (1.0 / 3.0)


def interception_deposition_velocity(gamma_w: float, a: float, x: float, D: float) -> float:
    """Eq. (2.12): k_int = gamma_w * a^2 / (2x)."""
    x_reg = max(x, D)
    return gamma_w * a**2 / (2.0 * x_reg)


def wall_transport_velocity(
    a: float, mu: float, T_K: float, gamma_w: float, x: float, D: float
) -> tuple[float, float, float]:
    """Eq. (2.13): k_w = max(k_lev, k_int). Returns (k_w, k_lev, k_int)."""
    D_B = brownian_diffusivity(a, mu, T_K)
    k_lev = leveque_deposition_velocity(D_B, gamma_w, x, D)
    k_int = interception_deposition_velocity(gamma_w, a, x, D)
    return max(k_lev, k_int), k_lev, k_int


def crossover_radius(mu: float, T_K: float, gamma_w: float, x: float, D: float) -> float:
    """Eq. (2.14): radius a_c where k_lev = k_int (diffusion <-> interception branch).

    a_c = 1.076^(3/8) * (k_B T / (6 pi mu))^(1/4) * (x/gamma_w)^(1/4)
    """
    from .constants import K_B

    x_reg = max(x, D)
    return (
        1.076 ** (3.0 / 8.0)
        * (K_B * T_K / (6.0 * math.pi * mu)) ** 0.25
        * (x_reg / gamma_w) ** 0.25
    )
