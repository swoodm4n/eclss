"""Stagnant-segment buoyant convection: Rayleigh number, onset, convective velocity. derivation.md §2.2(b)."""

import math

from .constants import RA_C


def rayleigh_number(g: float, beta: float, delta_T: float, H: float, nu: float, alpha_th: float) -> float:
    """Eq. (2.4): Ra = g * beta * delta_T * H^3 / (nu * alpha_th)."""
    return g * beta * delta_T * H**3 / (nu * alpha_th)


def critical_delta_T(g: float, beta: float, H: float, nu: float, alpha_th: float, Ra_c: float = RA_C) -> float:
    """Eq. (2.5): delta_T_c = Ra_c * nu * alpha_th / (g * beta * H^3)."""
    return Ra_c * nu * alpha_th / (g * beta * H**3)


def convective_velocity(Ra: float, H: float, nu: float, g: float, beta: float, delta_T: float, Ra_c: float = RA_C) -> float:
    """Eq. (2.6a/b): characteristic convective velocity, 0 below onset.

    Near onset (2.6a): u_conv ~ (nu/H) * sqrt(Ra/Ra_c - 1)
    Well above onset (2.6b): u_conv ~ 0.1 * sqrt(g * beta * delta_T * H)

    Uses (2.6b) once Ra exceeds ~5*Ra_c (well above onset), else (2.6a).
    """
    if Ra < Ra_c:
        return 0.0
    if Ra < 5 * Ra_c:
        return (nu / H) * math.sqrt(max(Ra / Ra_c - 1.0, 0.0))
    return 0.1 * math.sqrt(g * beta * delta_T * H)


def suspension_settling_ratio(v_s: float, u_conv: float) -> float:
    """Eq. (2.7): Omega = v_s / u_conv. Returns inf if u_conv == 0 (no convection: unopposed settling)."""
    if u_conv == 0.0:
        return math.inf
    return abs(v_s) / u_conv
