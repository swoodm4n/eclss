"""Dormancy (stagnant, U=0) simulation: the consequence of crossing the regime boundary.

derivation.md §3.5, §5.7. Produces:
  results/figures/fig3_dormancy_biofilm_accumulation.png
  results/figures/fig4_convection_switch_narrow_line.png  -- the lunar-suppresses-convection result
  results/data/dormancy_sim_summary.csv
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

from eclss_gravity import buoyancy, constants, dormancy, kinetics as kin, particles  # noqa: E402

FIG_DIR = ROOT / "results" / "figures"
DATA_DIR = ROOT / "results" / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

ONE_YEAR_S = 3.156e7
GRAVITIES = (("Earth", constants.G_EARTH, "steelblue"), ("Mars", constants.G_MARS, "darkorange"), ("Moon", constants.G_MOON, "dimgray"))


def fig3_dormancy_accumulation():
    """Biofilm accumulation over a 1-year dormancy period, cell vs floc class, per gravity level.

    Uses the 6.35 mm LINE geometry at dT=1 K, not the 0.30 m tank: derivation.md §2.2(b)
    shows a tank's Ra >> Ra_c at every gravity level considered (dT_c ~ 1e-6 to 1e-5 K, so
    any realistic gradient convects unconditionally) -- confirmed numerically below, where the
    tank case fully depletes within hours at all three gravities and the gravity signal is
    washed out. The line at dT=1 K is where Ra straddles Ra_c across the three gravity levels
    (Earth 4953 > Ra_c, Mars 1873 > Ra_c, Moon 818 < Ra_c -- convection OFF at Moon gravity),
    which is where the derivation's counter-intuitive "lower gravity can increase net
    deposition by switching off convection" result (§3.5) actually shows up in a simulation.
    """
    classes = [particles.P1_CELL, particles.P3_MEDIAN_FLOC]
    C0 = {particles.P1_CELL.label: 5e-6, particles.P3_MEDIAN_FLOC.label: 5e-7}  # kg-dry/m^3, rough anchor to ISS potable spec
    H_LINE = 6.35e-3
    DELTA_T_LINE = 1.0

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharex=True)

    summary_rows = []
    for label, g, color in GRAVITIES:
        result = dormancy.simulate_dormancy(
            classes, C0, S0=3.0, H=H_LINE, g=g, duration_s=ONE_YEAR_S,
            kinetic_params=kin.KineticParams(), delta_T=DELTA_T_LINE, n_eval=400,
        )
        t_days = result.t / 86400.0
        axes[0].plot(t_days, result.X * 1e6, color=color, label=f"{label} g")  # mg/m^2
        for pc in classes:
            ls = "-" if pc is particles.P1_CELL else "--"
            axes[1].plot(t_days, result.C[pc.label] / (C0[pc.label] or 1), color=color, ls=ls,
                         label=f"{label} g, {pc.label.split(' (')[0]}")
        summary_rows.append({
            "gravity": label, "g_m_s2": g, "Ra_tank": result.Ra,
            "X_final_mg_m2": result.X[-1] * 1e6,
            "C_cell_frac_remaining": result.C[particles.P1_CELL.label][-1] / C0[particles.P1_CELL.label],
            "C_floc_frac_remaining": result.C[particles.P3_MEDIAN_FLOC.label][-1] / C0[particles.P3_MEDIAN_FLOC.label],
        })

    axes[0].set_xlabel("dormancy duration (days)")
    axes[0].set_ylabel(r"deposited areal biomass $X$ (mg m$^{-2}$)")
    axes[0].set_title("Accumulated deposit on tank floor")
    axes[0].legend(fontsize=8)

    axes[1].set_xlabel("dormancy duration (days)")
    axes[1].set_ylabel("suspended fraction remaining, $C(t)/C_0$")
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-12, 2.0)  # floor out floating-point noise well below any physically meaningful level
    axes[1].set_title("Suspended biomass depletion (solid=cell, dashed=100 $\\mu$m floc)")
    axes[1].legend(fontsize=7, ncol=2)

    fig.suptitle("Dormancy simulation (6.35 mm line, 1 year, $\\Delta T$=1 K): consequence of crossing the regime boundary\n"
                 "(Ra > Ra_c at Earth/Mars but NOT at Moon g -- convection suppressed at lunar gravity)")
    fig.tight_layout()
    out = FIG_DIR / "fig3_dormancy_biofilm_accumulation.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")

    df = pd.DataFrame(summary_rows)
    df.to_csv(DATA_DIR / "dormancy_sim_summary.csv", index=False)
    print(df.to_string(index=False))


def fig4_convection_switch():
    """derivation.md §3.5 'strongest single result': lowering g can suppress convection in
    narrow stagnant lines (Ra < Ra_c), increasing net deposition, while tanks always convect.
    """
    NU = constants.water_kinematic_viscosity()
    ALPHA_TH = constants.water_thermal_diffusivity()
    BETA = constants.water_thermal_expansion()

    delta_T = 1.0  # K, representative cabin-to-line gradient
    geometries = (("6.35 mm line", 6.35e-3), ("25.4 mm filter housing", 25.4e-3), ("0.30 m tank", 0.30))

    fig, ax = plt.subplots(figsize=(7, 5.5))
    width = 0.25
    x = np.arange(len(geometries))
    for k, (label, g, color) in enumerate(GRAVITIES):
        Ra_vals = [buoyancy.rayleigh_number(g, BETA, delta_T, H, NU, ALPHA_TH) for _, H in geometries]
        bars = ax.bar(x + (k - 1) * width, np.log10(np.clip(Ra_vals, 1e-3, None)), width, label=f"{label} g", color=color)
    ax.axhline(np.log10(constants.RA_C), color="red", ls="--", lw=1.5, label=r"$Ra_c$ = 1708")
    ax.set_xticks(x)
    ax.set_xticklabels([g[0] for g in geometries])
    ax.set_ylabel(r"log10(Ra) at $\Delta T$ = 1 K")
    ax.set_title("Buoyant convection onset vs. gravity and geometry\n(below the red line: convection OFF, settling unopposed)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    out = FIG_DIR / "fig4_convection_switch_narrow_line.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig3_dormancy_accumulation()
    fig4_convection_switch()
