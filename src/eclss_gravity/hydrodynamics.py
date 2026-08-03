"""Duct hydrodynamics: velocity, Reynolds number, wall shear. derivation.md §2.3-2.4, §9.3."""

import math
from dataclasses import dataclass


def bulk_velocity(Q: float, D: float) -> float:
    """Eq. (2.8): U = Q / A for a circular duct of diameter D."""
    A = math.pi / 4.0 * D**2
    return Q / A


def reynolds_number(U: float, D: float, rho_f: float, mu: float) -> float:
    return rho_f * U * D / mu


def wall_shear(U: float, D: float, rho_f: float, mu: float) -> tuple[float, float, float]:
    """Eq. (2.9) laminar branch, Blasius branch for Re >= 2300.

    Returns (gamma_w, tau_w, u_star).
    """
    Re = reynolds_number(U, D, rho_f, mu)
    if Re < 2300:
        gamma_w = 8.0 * U / D
        tau_w = mu * gamma_w
    else:
        f = 0.316 * Re ** (-0.25)  # Blasius
        tau_w = (f / 8.0) * rho_f * U**2
        gamma_w = tau_w / mu
    u_star = math.sqrt(tau_w / rho_f)
    return gamma_w, tau_w, u_star


def entrance_length(Re: float, D: float) -> float:
    """Laminar hydrodynamic entrance length, L_e = 0.05 Re D (derivation.md A2)."""
    return 0.05 * Re * D


@dataclass(frozen=True)
class Regime:
    """A named ECLSS operating regime. derivation.md §1.1, §1.3 (Table)."""

    label: str
    D: float  # m, hydraulic/tube diameter
    Q: float  # m^3/s, volumetric flow rate
    L: float  # m, analysis segment length
    H: float  # m, vertical extent for stagnant-buoyancy calc (tank height or line diameter)

    @property
    def U(self) -> float:
        return bulk_velocity(self.Q, self.D)


def _Q_from_mass_rate(kg_per_hr: float, rho_f: float = 997.0) -> float:
    return kg_per_hr / rho_f / 3600.0


# derivation.md §1.3 Table (computed operating points) and §1.2 (sourced flow rates).
# D is the ASSUMED 6.35 mm (1/4") line ID unless otherwise noted (§1.3).
REGIME_R1_WPA_NOMINAL = Regime(
    label="R1 WPA line, nominal (13 lb/hr)",
    D=6.35e-3,
    Q=_Q_from_mass_rate(5.90),  # 13 lb/hr = 5.90 kg/hr, NTRS 20050207388
    L=0.5,
    H=6.35e-3,
)

REGIME_R2_WPA_RESTART_FLUSH = Regime(
    label="R2 WPA line, restart flush (10x nominal)",
    D=6.35e-3,
    Q=_Q_from_mass_rate(59.0),
    L=0.5,
    H=6.35e-3,
)

REGIME_R3A_UPA_FEED = Regime(
    label="R3a UPA feed line (9 kg/day)",
    D=6.35e-3,
    Q=9.0 / 997.0 / 86400.0,
    L=0.5,
    H=6.35e-3,
)

# MABR shell side: derivation.md §1.3 - void volume 1.35 L, module length 0.30 m (ASSUMED),
# shell free area 4.43e-3 m^2 (derived), d_h = 17.95 mm (derived).
REGIME_R3B_MABR_SHELL = Regime(
    label="R3b MABR shell side (150 mL/min)",
    D=17.95e-3,
    Q=150e-6 / 60.0,
    L=0.30,
    H=17.95e-3,
)

_DEAD_LEG_U = 1e-4  # m/s, ASSUMED representative residual creep flow (derivation.md §1.3)
_DEAD_LEG_D = 6.35e-3
REGIME_R4_DEAD_LEG = Regime(
    label="R4 dead leg / creep flow",
    D=_DEAD_LEG_D,
    Q=_DEAD_LEG_U * math.pi / 4.0 * _DEAD_LEG_D**2,
    L=0.5,
    H=_DEAD_LEG_D,
)

ALL_REGIMES = (
    REGIME_R1_WPA_NOMINAL,
    REGIME_R2_WPA_RESTART_FLUSH,
    REGIME_R3A_UPA_FEED,
    REGIME_R3B_MABR_SHELL,
    REGIME_R4_DEAD_LEG,
)

# derivation.md §1.3: sweep range for the ASSUMED line diameter (standard tube sizes)
STANDARD_TUBE_DIAMETERS_M = (3.18e-3, 4.57e-3, 6.35e-3, 9.53e-3, 12.7e-3)
