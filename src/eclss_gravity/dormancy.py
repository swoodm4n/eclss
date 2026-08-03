"""0-D stagnant/dormancy reactor model. derivation.md §3.5, §5.3(B), §5.7.

derivation.md explicitly specifies this reduction: "Stagnant (U=0): ... the segment
becomes a set of independent 0-D reactors with a gravitational wall flux, which is
the correct dormancy model" (§5.7). This module implements exactly that reduction,
rather than degenerating the general 1-D PDE (pde_model.py) at U->0.
"""

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from . import buoyancy, constants, kinetics as kin
from .particles import ParticleClass, brownian_diffusivity, settling_velocity


def vertical_mixing_diffusivity(
    a: float, mu: float, T_K: float, g: float, beta: float, H: float, delta_T: float,
    nu: float, alpha_th: float, mixing_length_factor: float = 1.0 / 10.0,
) -> tuple[float, float]:
    """Eq. (5.7): D_v = D_B + D_conv, D_conv = 0 if Ra < Ra_c else u_conv*H*mixing_length_factor.

    Returns (D_v, Ra) for diagnostics.
    """
    D_B = brownian_diffusivity(a, mu, T_K)
    Ra = buoyancy.rayleigh_number(g, beta, delta_T, H, nu, alpha_th)
    if Ra < constants.RA_C:
        D_conv = 0.0
    else:
        u_conv = buoyancy.convective_velocity(Ra, H, nu, g, beta, delta_T)
        D_conv = u_conv * H * mixing_length_factor
    return D_B + D_conv, Ra


def settling_rate_constant(v_s: float, H: float, D_v: float) -> float:
    """Eq. (5.8) reduced to a 0-D loss rate constant k = k_tot/H.

    k_tot = v_s / (1 - exp(-H/h_s)), h_s = D_v/v_s (scale height).
    When h_s << H (settling dominant, D_v -> 0): k_tot -> v_s, i.e. k -> v_s/H = 1/t_settle,
    which is the closed form used for the t_settle table in derivation.md §3.5.
    """
    v_s_abs = abs(v_s)
    if v_s_abs == 0.0:
        return 0.0
    h_s = D_v / v_s_abs
    if h_s < 1e-6 * H:
        k_tot = v_s_abs
    else:
        exponent = -H / h_s
        # avoid overflow for very small h_s (exponent very negative -> exp ~ 0)
        denom = 1.0 - math.exp(max(exponent, -700.0))
        k_tot = v_s_abs / denom if denom > 1e-300 else v_s_abs
    return k_tot / H


def time_to_settle(a: float, delta_rho: float, g: float, H: float, mu: float, T_K: float = 298.15) -> float:
    """t_settle = H / v_s (pure-settling limit, D_v -> 0). Regression target: derivation.md §3.5, §8.6."""
    v_s, _, _ = settling_velocity(a, delta_rho, g, mu=mu, T_K=T_K)
    return H / abs(v_s)


@dataclass
class DormancySimResult:
    t: np.ndarray  # seconds
    C: dict  # label -> array (N_t,), suspended concentration
    X: np.ndarray  # deposited areal biomass density, kg/m^2
    S: np.ndarray  # substrate
    g: float
    H: float
    Ra: float
    D_v_by_class: dict


def simulate_dormancy(
    particle_classes: list[ParticleClass],
    C0_by_class: dict,
    S0: float,
    H: float,
    g: float,
    duration_s: float,
    kinetic_params: kin.KineticParams = None,
    delta_T: float = 0.5,
    T_K: float = 298.15,
    n_eval: int = 400,
) -> DormancySimResult:
    """Integrate the 0-D dormancy reactor: growth, decay, and gravity-driven wall loss.

    dC_i/dt = (mu(S) - b) * C_i - k_i(g) * C_i
    dS/dt   = -(1/Y) * mu(S) * sum_i C_i           (substrate consumption by suspended biomass)
    dX/dt   = sum_i k_i(g) * C_i * H  - b_f * X     (deposited areal mass gains a volumetric->areal
                                                       conversion: a loss rate k_i [1/s] from a
                                                       reactor of depth H deposits k_i*C_i*H onto
                                                       unit floor area per unit time)
    """
    if kinetic_params is None:
        kinetic_params = kin.KineticParams()
    kp = kinetic_params

    mu_visc = constants.water_viscosity(T_K)
    nu = constants.water_kinematic_viscosity(T_K)
    alpha_th = constants.water_thermal_diffusivity(T_K)
    beta = constants.water_thermal_expansion(T_K)

    v_s_list = []
    k_list = []
    D_v_by_class = {}
    Ra_last = None
    for pc in particle_classes:
        v_s, _, _ = settling_velocity(pc.a, pc.delta_rho, g, mu=mu_visc, T_K=T_K)
        D_v, Ra = vertical_mixing_diffusivity(pc.a, mu_visc, T_K, g, beta, H, delta_T, nu, alpha_th)
        Ra_last = Ra
        k = settling_rate_constant(v_s, H, D_v)
        v_s_list.append(v_s)
        k_list.append(k)
        D_v_by_class[pc.label] = D_v

    n_classes = len(particle_classes)
    C0 = np.array([C0_by_class[pc.label] for pc in particle_classes])
    y0 = np.concatenate([C0, [S0], [0.0]])  # [C_1..C_n, S, X]

    k_arr = np.array(k_list)

    def rhs(t, y):
        # derivation.md §5.8 item 8: clip non-negativity to prevent Monod/rate blowup
        # once a stiff decay term has driven a state to numerical zero.
        C = np.maximum(y[:n_classes], 0.0)
        S = max(y[n_classes], 0.0)
        X = max(y[n_classes + 1], 0.0)
        mu_S = kin.monod_rate(S, kp.mu_max, kp.K_s, kp.phi_g)
        dC = (mu_S - kp.b) * C - k_arr * C
        total_C = C.sum()
        dS = -(1.0 / kp.Y) * mu_S * total_C if kp.Y > 0 else 0.0
        deposit_flux = (k_arr * C).sum() * H  # kg/m^2/s onto unit floor area
        dX = deposit_flux - kp.b_f * X
        return np.concatenate([dC, [dS], [dX]])

    t_eval = np.linspace(0, duration_s, n_eval)
    sol = solve_ivp(rhs, (0, duration_s), y0, method="BDF", t_eval=t_eval, rtol=1e-8, atol=1e-18)
    if not sol.success:
        raise RuntimeError(f"dormancy integration failed: {sol.message}")

    # Clip reported output too: the solver's internal trajectory can carry small
    # negative floating-point excursions once a state has decayed to numerical
    # zero, even though the RHS clips at evaluation time (derivation.md §5.8 item 8).
    C_out = {pc.label: np.maximum(sol.y[i], 0.0) for i, pc in enumerate(particle_classes)}
    S_out = np.maximum(sol.y[n_classes], 0.0)
    X_out = np.maximum(sol.y[n_classes + 1], 0.0)

    return DormancySimResult(t=sol.t, C=C_out, X=X_out, S=S_out, g=g, H=H, Ra=Ra_last, D_v_by_class=D_v_by_class)
