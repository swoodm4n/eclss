"""Uncertainty propagation. derivation.md §7.3.

(a) Deterministic sweep -- for the regime boundaries (headline figure, no MC needed
    since the criteria are closed-form/analytic).
(b) Monte Carlo -- for the uncertainty band on the crossover gravity level g*.
"""

import warnings
from dataclasses import dataclass

import numpy as np

from . import constants, criteria
from .hydrodynamics import STANDARD_TUBE_DIAMETERS_M, bulk_velocity, reynolds_number, wall_shear

RNG_SEED = 20260803  # fixed seed for reproducibility (run.md)


def sample_bimodal_diameter(rng: np.random.Generator, n: int, p_small: float = 0.8) -> tuple[np.ndarray, np.ndarray]:
    """derivation.md §7.3(b): bimodal particle-size distribution.

    Small mode (single cells / small aggregates): lognormal, geometric mean 1.1 um, geometric sd 1.5
    Large mode (flocs): lognormal, geometric mean 110 um, geometric sd 2.0
    Sourced qualitatively: ">80% of detached clusters <= 7 um by number" and "volume-dominant
    band 68-183 um" -- the literature describes a genuinely bimodal by-number/by-volume distribution.

    Returns (d_meters, is_large_mode_bool_array).
    """
    is_large = rng.random(n) >= p_small
    d = np.empty(n)
    n_small = int((~is_large).sum())
    n_large = int(is_large.sum())
    if n_small:
        d[~is_large] = rng.lognormal(mean=np.log(1.1e-6), sigma=np.log(1.5), size=n_small)
    if n_large:
        d[is_large] = rng.lognormal(mean=np.log(110e-6), sigma=np.log(2.0), size=n_large)
    return d, is_large


def sample_delta_rho(rng: np.random.Generator, is_large_mode: np.ndarray) -> np.ndarray:
    """Cell range (83-103 kg/m^3) for the small mode, floc range (38-68) for the large mode."""
    n = len(is_large_mode)
    out = np.empty(n)
    out[~is_large_mode] = rng.uniform(83.0, 103.0, size=(~is_large_mode).sum())
    out[is_large_mode] = rng.uniform(38.0, 68.0, size=is_large_mode.sum())
    return out


def sample_tube_diameter(rng: np.random.Generator, n: int) -> np.ndarray:
    return rng.choice(np.array(STANDARD_TUBE_DIAMETERS_M), size=n)


def sample_temperature_K(rng: np.random.Generator, n: int) -> np.ndarray:
    return rng.uniform(288.0, 318.0, size=n)


@dataclass
class MonteCarloResult:
    d: np.ndarray
    delta_rho: np.ndarray
    D_tube: np.ndarray
    T_K: np.ndarray
    is_large_mode: np.ndarray  # True = floc/interception branch, False = cell/diffusion branch
    g_star: np.ndarray  # crossover gravity level (m/s^2) for Ga_dep = 1
    Ga_dep_at_mars: np.ndarray
    Ga_dep_at_moon: np.ndarray
    Ga_dep_at_earth: np.ndarray


def monte_carlo_g_star(Q_flow: float, L: float, n_samples: int = 10_000, seed: int = RNG_SEED) -> MonteCarloResult:
    """derivation.md §7.3(b): propagate parameter uncertainty onto g* and P(Ga_dep>1 | g).

    Q_flow: volumetric flow rate (m^3/s) at the sourced nominal operating point (e.g. WPA R1).
    """
    rng = np.random.default_rng(seed)
    d, is_large = sample_bimodal_diameter(rng, n_samples)
    delta_rho = sample_delta_rho(rng, is_large)
    D_tube = sample_tube_diameter(rng, n_samples)
    T_K = sample_temperature_K(rng, n_samples)

    g_star = np.empty(n_samples)
    Ga_earth = np.empty(n_samples)
    Ga_mars = np.empty(n_samples)
    Ga_moon = np.empty(n_samples)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for i in range(n_samples):
            mu = constants.water_viscosity(T_K[i])
            rho_f = constants.water_density(T_K[i])
            U = bulk_velocity(Q_flow, D_tube[i])
            gamma_w, tau_w, _ = wall_shear(U, D_tube[i], rho_f, mu)
            a = d[i] / 2.0

            g_star_dif = criteria.g_star_dif(a, delta_rho[i], mu, T_K[i], gamma_w, L, D_tube[i])
            g_star_int = criteria.g_star_int(delta_rho[i], mu, gamma_w, L, D_tube[i])
            # Ga_dep is the min of the two branches (2.13: k_w = max(k_lev,k_int) -> Ga = min(Ga_dif,Ga_int)),
            # so the controlling (larger, i.e. later-crossing) threshold is the max of the two g*'s
            # on the branch that is actually active. We report the diffusion-branch g* when a < a_c
            # (small mode) and the interception-branch g* otherwise, since that is the branch that
            # governs at that particle size (derivation.md §3.2).
            g_star[i] = g_star_dif if not is_large[i] else g_star_int

            Ga_earth[i] = criteria.ga_dep_closed_form(a, delta_rho[i], constants.G_EARTH, mu, T_K[i], gamma_w, L, D_tube[i])
            Ga_mars[i] = criteria.ga_dep_closed_form(a, delta_rho[i], constants.G_MARS, mu, T_K[i], gamma_w, L, D_tube[i])
            Ga_moon[i] = criteria.ga_dep_closed_form(a, delta_rho[i], constants.G_MOON, mu, T_K[i], gamma_w, L, D_tube[i])
    n_outside_validity = len(caught)
    if n_outside_validity:
        print(f"monte_carlo_g_star: {n_outside_validity} of {2 * n_samples} closed-form calls "
              f"outside Stokes validity (Re_p > 0.34) -- biased high, mostly large-floc samples.")

    return MonteCarloResult(
        d=d, delta_rho=delta_rho, D_tube=D_tube, T_K=T_K, is_large_mode=is_large, g_star=g_star,
        Ga_dep_at_earth=Ga_earth, Ga_dep_at_mars=Ga_mars, Ga_dep_at_moon=Ga_moon,
    )
