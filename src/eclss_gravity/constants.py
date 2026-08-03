"""Physical constants and default fluid properties. derivation.md §8.1."""

K_B = 1.380649e-23  # J/K, SI-defined

# Gravity levels (m/s^2), matching the reduced-gravity two-phase-flow literature
# (derivation.md §0.3, novelty_adjudication.md C-3)
G_EARTH = 9.81
G_MARS = 3.71
G_MOON = 1.62
G_STAGNANT = 0.0  # limiting case; treated separately (derivation.md §3.5)

RA_C = 1708.0  # Rayleigh-Benard critical Rayleigh number, rigid-rigid infinite plane (STD)


def water_density(T_K: float = 298.15) -> float:
    """kg/m^3. Constant value at 25 C per derivation.md §8.1 (A1: valid 5-60 C)."""
    return 997.0


def water_viscosity(T_K: float = 298.15) -> float:
    """Pa s, water dynamic viscosity.

    derivation.md §8.1 quotes 8.90e-4 Pa s at 25 C and notes mu varies
    ~1.14e-3 (15 C) to 6.0e-4 (45 C) Pa s over the plausible ECLSS range (§6.6).
    We interpolate log-linearly between those two anchors for T sweeps.
    """
    T_C = T_K - 273.15
    anchors_C = (15.0, 25.0, 45.0)
    anchors_mu = (1.14e-3, 8.90e-4, 6.0e-4)
    if T_C <= anchors_C[0]:
        return anchors_mu[0]
    if T_C >= anchors_C[-1]:
        return anchors_mu[-1]
    import numpy as np

    log_mu = np.interp(T_C, anchors_C, np.log(anchors_mu))
    return float(np.exp(log_mu))


def water_kinematic_viscosity(T_K: float = 298.15) -> float:
    return water_viscosity(T_K) / water_density(T_K)


def water_thermal_expansion(T_K: float = 298.15) -> float:
    """1/K. Constant at 25 C value per derivation.md §8.1 (A1 validity range)."""
    return 2.57e-4


def water_thermal_diffusivity(T_K: float = 298.15) -> float:
    """m^2/s. Constant at 25 C value per derivation.md §8.1."""
    return 1.46e-7


D_S_DEFAULT = 5e-10  # m^2/s, dissolved organic diffusivity, ASSUMED (derivation.md §8.1)
