"""Growth kinetics and detachment. derivation.md §5.4-5.5, §8.5. All ASSUMED (not sourced)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KineticParams:
    """derivation.md §8.5 - every value here is an explicitly-flagged placeholder."""

    mu_max: float = 0.1 / 3600.0  # 1/s, ASSUMED range 0.02-0.3 /h
    K_s: float = 1.0  # g-C/m^3, ASSUMED range 0.1-10
    Y: float = 0.4  # kg-dry / kg-C, ASSUMED range 0.2-0.6
    b: float = 0.002 / 3600.0  # 1/s, planktonic decay, ASSUMED
    b_f: float = 0.001 / 3600.0  # 1/s, biofilm decay, ASSUMED
    rho_X: float = 30.0  # kg-dry/m^3, ASSUMED
    alpha: float = 0.3  # attachment efficiency, ASSUMED, midpoint of sourced 0.36-0.78 band
    k_det0: float = 1e-5  # 1/s, ASSUMED, tuned to ~20 day timescale at R1 shear
    n_det: float = 1.0  # detachment shear exponent, ASSUMED (A27: sources disagree linear vs exponential)
    tau_ref: float = 1.0  # Pa, normalisation only
    phi_g: float = 1.0  # gravity growth-modulation factor, MUST stay 1.0 in the published baseline (eq 4.1, S4.2)


def monod_rate(S: float, mu_max: float, K_s: float, phi_g: float = 1.0) -> float:
    """Eq. (5.10) with the eq. (4.1) gravity hook: mu(S,g) = mu_max * phi(g) * S/(K_s+S).

    phi_g defaults to 1 (gravity-independent kinetics) per the deliberate modelling
    decision in derivation.md §4.2 -- this must remain the published baseline.
    """
    if S <= 0:
        return 0.0
    return mu_max * phi_g * S / (K_s + S)


def detachment_rate(tau_w: float, k_det0: float, tau_ref: float, n: float) -> float:
    """Eq. (5.9): k_det = k_det0 * (tau_w/tau_ref)^n."""
    return k_det0 * (tau_w / tau_ref) ** n
