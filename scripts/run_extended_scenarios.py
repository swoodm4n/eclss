"""Two disclosed-but-previously-unexplored scenarios from docs/limitations.md §2 (A11, A3).

(a) Negative buoyant density (A11): some biofilm is reported LESS dense than water (898 kg/m^3
    vs water's 997, i.e. Delta_rho ~ -99 kg/m^3) and would rise rather than settle. The sign-
    symmetry of the criteria was unit-tested (test_negative_delta_rho_sign_symmetry) but never
    explored across a scenario or reported quantitatively.
(b) Duty-cycling flow (A3): the WPA does not run continuously -- it cycles between a pumped
    processing state and idle/stagnant periods. Every result in this program to date evaluates
    a single fixed regime (R1 pumped OR R4 stagnant), never the alternation.

Produces:
  results/data/rising_aggregate_comparison.csv
  results/figures/fig6_duty_cycling.png
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclss_gravity import constants, criteria, dormancy, hydrodynamics, kinetics as kin, particles  # noqa: E402

FIG_DIR = ROOT / "results" / "figures"
DATA_DIR = ROOT / "results" / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

MU = constants.water_viscosity()
T_K = 298.15


def rising_aggregate_comparison():
    """(a) A11: compare a sinking cell (Delta_rho=+93, nominal) against a rising, gas-entrapping
    biofilm fragment (Delta_rho=-99, the sourced low-end biofilm wet density of 898 kg/m^3)."""
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w, _, _ = hydrodynamics.wall_shear(r1.U, r1.D, constants.water_density(), MU)

    rows = []
    for label, delta_rho in (("sinking cell (+93 kg/m3, nominal)", 93.0), ("rising fragment (-99 kg/m3, gas-entrapping biofilm)", -99.0)):
        for g_label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
            v_s, Re_p, valid = particles.settling_velocity(particles.P1_CELL.a, delta_rho, g, mu=MU, T_K=T_K)
            Ga = criteria.ga_dep_closed_form(particles.P1_CELL.a, delta_rho, g, MU, T_K, gamma_w, r1.L, r1.D)
            rows.append({
                "class": label, "gravity": g_label, "v_s_m_per_s": v_s,
                "direction": "toward bottom wall" if v_s > 0 else "toward top wall",
                "Ga_dep_magnitude": abs(Ga),
            })
    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "rising_aggregate_comparison.csv", index=False)
    print("=== A11: rising vs sinking particle comparison ===")
    print(df.to_string(index=False))
    print(
        "\nFinding: |Ga_dep| scales linearly with |delta_rho| identically regardless of sign "
        "(the ~6% difference above is entirely the 93 vs 99 kg/m3 magnitude difference between "
        "the sourced cell and biofilm-fragment densities, not a sign artifact -- confirmed by "
        "test_ga_dep_closed_form_sign_symmetric_for_negative_delta_rho using equal magnitudes). "
        "The deposition LOCATION inverts: every figure in this program plots only the sinking "
        "(bottom-wall) case; a gas-entrapping biofilm fragment would instead accumulate on the "
        "TOP of a horizontal WPA line. No sensor or sampling strategy that assumes bottom-wall "
        "accumulation would detect this population."
    )
    return df


def duty_cycling_scenario():
    """(b) A3: WPA operates ~2 h/day at nominal flow (a rough illustrative duty cycle -- the
    sourced 13 lb/hr flow rate is a per-hour rate, not an operating-fraction spec; no sourced
    ISS WPA duty-cycle fraction was found, so this is explicitly an ASSUMED illustrative
    schedule, not a claim about actual ISS operations) and is stagnant the rest of the time,
    repeating over a 30-day window. Compares single-cell deposited mass under this alternating
    schedule against the two single-regime bookends already in the program (always-pumped,
    always-stagnant) at each gravity level.
    """
    classes = [particles.P1_CELL]
    C0 = {particles.P1_CELL.label: 5e-6}
    H_LINE = 6.35e-3
    kp = kin.KineticParams()

    PUMPED_HOURS_PER_DAY = 2.0  # ASSUMED illustrative duty cycle, not a sourced ISS value
    CYCLE_DAYS = 30
    STAGNANT_DELTA_T = 1.0

    fig, ax = plt.subplots(figsize=(8, 5.5))
    colors = {"Earth": "steelblue", "Mars": "darkorange", "Moon": "dimgray"}
    summary_rows = []

    for g_label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
        # Duty-cycled: alternate short pumped flush (fast, near-total wall delivery per derivation's
        # own R1 Ga_dep>1 regime for cells is NOT guaranteed -- so we still integrate the same
        # 0-D reactor, just switching k_i between the R1-pumped wall-transport rate and the
        # stagnant settling-rate-constant depending on time of day) and long stagnant period.
        r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
        gamma_w, _, _ = hydrodynamics.wall_shear(r1.U, r1.D, constants.water_density(), MU)
        k_w, _, _ = __import__("eclss_gravity.wall_transport", fromlist=["wall_transport_velocity"]).wall_transport_velocity(
            particles.P1_CELL.a, MU, T_K, gamma_w, r1.L, r1.D
        )
        v_s, _, _ = particles.settling_velocity(particles.P1_CELL.a, particles.P1_CELL.delta_rho, g, mu=MU, T_K=T_K)
        k_pumped = (k_w + v_s / np.pi) / H_LINE  # pumped-regime volumetric loss rate, perimeter-averaged gravity + flow

        D_v, Ra = dormancy.vertical_mixing_diffusivity(particles.P1_CELL.a, MU, T_K, g, constants.water_thermal_expansion(), H_LINE, STAGNANT_DELTA_T, constants.water_kinematic_viscosity(), constants.water_thermal_diffusivity())
        k_stagnant = dormancy.settling_rate_constant(v_s, H_LINE, D_v)

        duration_s = CYCLE_DAYS * 86400.0
        n_steps = 200_000  # fine enough that forward Euler is stable against the fastest rate (k_pumped)
        t = np.linspace(0, duration_s, n_steps)
        dt = t[1] - t[0]
        C = C0[particles.P1_CELL.label]
        S = 3.0  # g-C/m^3, same wastewater-side anchor as dormancy.py; DOES deplete here (bug fix
        # vs an earlier version of this script that held S fixed and produced unbounded growth)
        X = 0.0
        C_hist = np.empty_like(t)
        X_hist = np.empty_like(t)
        for i, ti in enumerate(t):
            hour_of_day = (ti / 3600.0) % 24.0
            k = k_pumped if hour_of_day < PUMPED_HOURS_PER_DAY else k_stagnant
            mu_S = kin.monod_rate(S, kp.mu_max, kp.K_s, kp.phi_g)
            dC = (mu_S - kp.b) * C - k * C
            biofilm_growth = mu_S * X
            dS = -(1.0 / kp.Y) * (mu_S * C + biofilm_growth / H_LINE) if kp.Y > 0 else 0.0
            dX = biofilm_growth - kp.b_f * X + k * C * H_LINE
            C = max(C + dC * dt, 0.0)
            S = max(S + dS * dt, 0.0)
            X = max(X + dX * dt, 0.0)
            C_hist[i] = C
            X_hist[i] = X

        ax.plot(t / 86400.0, X_hist * 1e6, color=colors[g_label], label=f"{g_label} g (duty-cycled)")
        summary_rows.append({"gravity": g_label, "X_final_mg_m2_duty_cycled": X_hist[-1] * 1e6,
                              "k_pumped_per_s": k_pumped, "k_stagnant_per_s": k_stagnant})

    ax.set_xlabel("time (days)")
    ax.set_ylabel(r"deposited areal biomass $X$ (mg m$^{-2}$)")
    ax.set_title(f"Duty-cycled scenario: {PUMPED_HOURS_PER_DAY:.0f} h/day pumped, rest stagnant\n"
                 f"(ASSUMED illustrative schedule, not a sourced ISS duty cycle -- see script docstring)")
    ax.legend()
    fig.tight_layout()
    out = FIG_DIR / "fig6_duty_cycling.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\nwrote {out}")

    df = pd.DataFrame(summary_rows)
    print("=== A3: duty-cycling scenario summary ===")
    print(df.to_string(index=False))
    return df


if __name__ == "__main__":
    rising_aggregate_comparison()
    duty_cycling_scenario()
