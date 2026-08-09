"""One-at-a-time structural sensitivity checks. derivation.md §7.3(c), flagged as "mandatory"
and never implemented per redteam_report.md Finding 1.4. Closes that gap.

Four checks, each varying exactly one structural choice with everything else held at its
nominal/default value:
  1. orientation_factor: 1/pi (perimeter-averaged, default) vs 1 (local bottom-of-tube bound)
  2. detachment exponent n: 1 (linear, default) vs 3 -- derivation.md A27, sources disagree
  3. Ra_c: 1708 (default, rigid-rigid infinite plane) x0.5 and x2 -- derivation.md A18
  4. phi(g), the gravity growth-modulation factor: 1 (default, deliberate) vs 0.8/1.2 (+/-20%)

Produces results/data/sensitivity_checks.csv
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclss_gravity import buoyancy, constants, criteria, dormancy, hydrodynamics, kinetics as kin, particles  # noqa: E402

DATA_DIR = ROOT / "results" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

MU = constants.water_viscosity()
RHO_F = constants.water_density()
T_K = 298.15


def check_1_orientation_factor():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w, _, _ = hydrodynamics.wall_shear(r1.U, r1.D, RHO_F, MU)
    rows = []
    for label, f_theta in (("perimeter_averaged_1_over_pi (default)", criteria.ORIENTATION_PERIMETER_AVERAGED),
                            ("local_bottom_of_tube_cos1", criteria.ORIENTATION_BOTTOM_LOCAL)):
        for g_label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
            Ga = criteria.ga_dep_closed_form(particles.P1_CELL.a, particles.P1_CELL.delta_rho, g, MU, T_K, gamma_w, r1.L, r1.D, orientation_factor=f_theta)
            rows.append({"check": "1_orientation_factor", "variant": label, "gravity": g_label, "Ga_dep_single_cell": Ga})
    return rows


def check_2_detachment_exponent():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    _, tau_w, _ = hydrodynamics.wall_shear(r1.U, r1.D, RHO_F, MU)
    rows = []
    for n in (1.0, 3.0):
        k_det = kin.detachment_rate(tau_w, kin.KineticParams().k_det0, kin.KineticParams().tau_ref, n)
        rows.append({"check": "2_detachment_exponent", "variant": f"n={n:.0f}", "gravity": "N/A (R1 pumped)",
                     "k_det_per_s": k_det, "biofilm_loss_timescale_days": (1.0 / k_det) / 86400.0 if k_det > 0 else float("inf")})
    return rows


def check_3_rayleigh_critical():
    classes = [particles.P1_CELL]
    C0 = {particles.P1_CELL.label: 5e-6}
    rows = []
    for ra_c_label, ra_c_mult in (("Ra_c_x0.5", 0.5), ("Ra_c_default_x1", 1.0), ("Ra_c_x2", 2.0)):
        ra_c_value = constants.RA_C * ra_c_mult
        for g_label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
            nu = constants.water_kinematic_viscosity()
            alpha_th = constants.water_thermal_diffusivity()
            beta = constants.water_thermal_expansion()
            Ra = buoyancy.rayleigh_number(g, beta, 1.0, 6.35e-3, nu, alpha_th)
            convecting = Ra >= ra_c_value
            rows.append({"check": "3_rayleigh_critical", "variant": ra_c_label, "gravity": g_label,
                         "Ra": Ra, "Ra_c_tested": ra_c_value, "convecting": convecting})
    return rows


def check_4_gravity_growth_modulation():
    classes = [particles.P1_CELL, particles.P3_MEDIAN_FLOC]
    C0 = {particles.P1_CELL.label: 5e-6, particles.P3_MEDIAN_FLOC.label: 5e-7}
    rows = []
    for phi_label, phi in (("phi=0.8 (-20%)", 0.8), ("phi=1.0 (default, deliberate)", 1.0), ("phi=1.2 (+20%)", 1.2)):
        kp = kin.KineticParams(phi_g=phi)
        for g_label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
            result = dormancy.simulate_dormancy(classes, C0, S0=3.0, H=6.35e-3, g=g, duration_s=3.156e7,
                                                 kinetic_params=kp, delta_T=1.0, n_eval=100)
            rows.append({"check": "4_gravity_growth_modulation", "variant": phi_label, "gravity": g_label,
                         "X_final_mg_m2": result.X[-1] * 1e6})
    return rows


def main():
    all_rows = []
    all_rows += check_1_orientation_factor()
    all_rows += check_2_detachment_exponent()
    all_rows += check_3_rayleigh_critical()
    all_rows += check_4_gravity_growth_modulation()
    df = pd.DataFrame(all_rows)
    df.to_csv(DATA_DIR / "sensitivity_checks.csv", index=False)

    print("=== Check 1: orientation_factor (1/pi vs 1) ===")
    print(df[df.check == "1_orientation_factor"][["variant", "gravity", "Ga_dep_single_cell"]].to_string(index=False))
    print("\n=== Check 2: detachment exponent n (1 vs 3), at R1 tau_w ===")
    print(df[df.check == "2_detachment_exponent"][["variant", "k_det_per_s", "biofilm_loss_timescale_days"]].to_string(index=False))
    print("\n=== Check 3: Ra_c x0.5/x1/x2 -- does the convection switch flip? ===")
    print(df[df.check == "3_rayleigh_critical"][["variant", "gravity", "Ra", "Ra_c_tested", "convecting"]].to_string(index=False))
    print("\n=== Check 4: phi(g) growth-modulation +/-20% ===")
    print(df[df.check == "4_gravity_growth_modulation"][["variant", "gravity", "X_final_mg_m2"]].to_string(index=False))
    print(f"\nwrote {DATA_DIR / 'sensitivity_checks.csv'}")


if __name__ == "__main__":
    main()
