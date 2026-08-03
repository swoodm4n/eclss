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
    """Dormancy simulation, 6.35 mm line at dT=1 K, 1 year. derivation.md §3.5, §5.7.

    CORRECTED (Phase 4 red-team, redteam_report.md §3): an earlier version of dormancy.py
    omitted the eq. (5.3) biofilm growth term mu(S_w)*X. With it omitted, this figure
    claimed a ~10^5-10^6x lunar/Earth difference in final deposited mass -- an artifact of
    denying the deposited biomass the ability to grow (see limitations.md). With the term
    restored (correct per the derivation), the actual, honest finding is more nuanced and,
    on reflection, more interesting:

    - The DEPOSITION RATE CONSTANT k_i(g) (how fast suspended cells reach the wall) differs
      by ~1700x between Earth/Mars (convection ON, Ra>Ra_c, fast turbulent delivery) and
      Moon (convection OFF, Ra<Ra_c, slow unopposed settling) -- this is the real, robust,
      transport-driven gravity effect, and it is large.
    - But the LONG-TIME (1 year) accumulated deposit converges to nearly the same value at
      all three gravity levels, because growth kinetics (deliberately g-independent, eq 4.1,
      phi(g)=1) dominate the overall timescale once ANY biofilm seed exists -- growth reaches
      the same substrate-limited ceiling (Y*S0) regardless of how fast that seed arrived.

    So: gravity matters for the TRANSIENT (how quickly a deposit forms -- operationally
    relevant to post-dormancy restart/flush timing) but, in this model, does not change the
    year-long steady-state outcome. That is the finding this figure now reports.
    """
    classes = [particles.P1_CELL, particles.P3_MEDIAN_FLOC]
    C0 = {particles.P1_CELL.label: 5e-6, particles.P3_MEDIAN_FLOC.label: 5e-7}  # kg-dry/m^3, rough anchor to ISS potable spec
    H_LINE = 6.35e-3
    DELTA_T_LINE = 1.0

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    summary_rows = []
    for label, g, color in GRAVITIES:
        result = dormancy.simulate_dormancy(
            classes, C0, S0=3.0, H=H_LINE, g=g, duration_s=ONE_YEAR_S,
            kinetic_params=kin.KineticParams(), delta_T=DELTA_T_LINE, n_eval=2000,
        )
        t_days = result.t / 86400.0
        axes[0].plot(t_days, result.X * 1e6, color=color, label=f"{label} g")  # mg/m^2
        for pc in classes:
            ls = "-" if pc is particles.P1_CELL else "--"
            axes[1].plot(t_days, result.C[pc.label] / (C0[pc.label] or 1), color=color, ls=ls,
                         label=f"{label} g, {pc.label.split(' (')[0]}")

        # Deposition-rate diagnostic: k_i(g) for the single-cell class, from the same
        # settling_rate_constant used inside simulate_dormancy (dormancy.py), reported
        # directly since it -- not the long-time X -- is where gravity actually shows up.
        mu_visc = constants.water_viscosity()
        nu = constants.water_kinematic_viscosity()
        alpha_th = constants.water_thermal_diffusivity()
        beta = constants.water_thermal_expansion()
        v_s, _, _ = particles.settling_velocity(particles.P1_CELL.a, particles.P1_CELL.delta_rho, g, mu=mu_visc)
        D_v, Ra = dormancy.vertical_mixing_diffusivity(particles.P1_CELL.a, mu_visc, 298.15, g, beta, H_LINE, DELTA_T_LINE, nu, alpha_th)
        k_cell = dormancy.settling_rate_constant(v_s, H_LINE, D_v)
        deposition_timescale_s = 1.0 / k_cell if k_cell > 0 else float("inf")

        summary_rows.append({
            "gravity": label, "g_m_s2": g, "Ra": result.Ra,
            "deposition_timescale_cell_s": deposition_timescale_s,
            "deposition_timescale_cell_hours": deposition_timescale_s / 3600.0,
            "X_final_mg_m2_1yr": result.X[-1] * 1e6,
            "C_cell_frac_remaining": result.C[particles.P1_CELL.label][-1] / C0[particles.P1_CELL.label],
            "C_floc_frac_remaining": result.C[particles.P3_MEDIAN_FLOC.label][-1] / C0[particles.P3_MEDIAN_FLOC.label],
        })

    axes[0].set_xlabel("dormancy duration (days)")
    axes[0].set_ylabel(r"deposited areal biomass $X$ (mg m$^{-2}$)")
    axes[0].set_xscale("log")
    axes[0].set_xlim(1e-3, 400)
    axes[0].set_title("Deposit growth: transient divergence, long-time convergence\n(x-axis log-scaled to show both regimes)")
    axes[0].legend(fontsize=8)

    axes[1].set_xlabel("dormancy duration (days)")
    axes[1].set_ylabel("suspended fraction remaining, $C(t)/C_0$")
    axes[1].set_xscale("log")
    axes[1].set_xlim(1e-3, 400)
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-12, 2.0)  # floor out floating-point noise well below any physically meaningful level
    axes[1].set_title("Suspended biomass depletion (solid=cell, dashed=100 $\\mu$m floc)")
    axes[1].legend(fontsize=7, ncol=2)

    fig.suptitle(
        "Dormancy simulation (6.35 mm line, 1 year, $\\Delta T$=1 K)\n"
        "Deposition RATE differs ~1700x by gravity (Ra>Ra_c convection at Earth/Mars vs. Ra<Ra_c at Moon);\n"
        "long-time OUTCOME converges because g-independent growth kinetics dominate once any deposit seeds"
    )
    fig.tight_layout()
    out = FIG_DIR / "fig3_dormancy_biofilm_accumulation.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")

    df = pd.DataFrame(summary_rows)
    df.to_csv(DATA_DIR / "dormancy_sim_summary.csv", index=False)
    print(df.to_string(index=False))
    print(
        "\nCORRECTED interpretation (see redteam_report.md §3, limitations.md): the ~1700x spread in "
        "deposition_timescale_cell_hours is the real, robust, transport-driven gravity effect. The "
        "near-identical X_final_mg_m2_1yr across gravity levels is NOT a null result for the gravity "
        "criterion -- it shows growth kinetics, not transport, set the long-time outcome once ANY seed "
        "deposit exists, which happens well within a year at every gravity level tested here."
    )


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
