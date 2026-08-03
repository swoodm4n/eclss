"""Headline figure: deterministic gravity-relevance regime map. derivation.md §7.3(a), §9.9.

Produces:
  results/figures/fig1_regime_map_size_vs_g.png   -- Ga_dep and Lambda_g contours in (d, g) space
  results/figures/fig2_g_star_vs_diameter.png      -- sensitivity of g* to the ASSUMED tube diameter
  results/data/regime_sweep_headline.csv           -- the numeric table backing both figures
"""

import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclss_gravity import constants, criteria, hydrodynamics  # noqa: E402

FIG_DIR = ROOT / "results" / "figures"
DATA_DIR = ROOT / "results" / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

MU = constants.water_viscosity()
RHO_F = constants.water_density()
T_K = 298.15


def fig1_regime_map():
    """Ga_dep(d, g) and Lambda_g(d, g) contours for the WPA nominal line (R1).

    Two Phase-4 red-team corrections applied (redteam_report.md Findings 2.2, 2.8):
    - delta_rho is now log-interpolated smoothly between the cell and floc nominal values
      over one octave around 7 um, instead of a hard step -- the original step produced a
      non-physical kink in the Ga_dep=1 contour (this map is a heuristic single surface across
      two different particle populations, not a claim that delta_rho truly varies with size).
    - Points evaluated outside Stokes validity (Re_p > 0.34, mostly large-d/high-g corners)
      are counted and reported rather than silently accepted; the closed forms still return a
      value there (biased high) since a full map re-solved with Schiller-Naumann at every grid
      point is not needed for the qualitative regime picture, but the caveat is not hidden.
    """
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w, tau_w, _ = hydrodynamics.wall_shear(r1.U, r1.D, RHO_F, MU)

    d_vals = np.logspace(np.log10(0.5e-6), np.log10(1000e-6), 150)  # 0.5 to 1000 um
    g_vals_ms2 = np.logspace(np.log10(1e-6 * constants.G_EARTH), np.log10(10 * constants.G_EARTH), 150)

    Ga = np.zeros((len(g_vals_ms2), len(d_vals)))
    Lam = np.zeros((len(g_vals_ms2), len(d_vals)))
    delta_rho_small = 93.0  # P1 cell nominal
    delta_rho_large = 50.0  # floc nominal
    n_outside_validity = 0
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for i, g in enumerate(g_vals_ms2):
            for j, d in enumerate(d_vals):
                a = d / 2.0
                # smooth log-space blend over one octave (3.5-14 um) around the 7 um crossover
                blend = np.clip((np.log(d) - np.log(3.5e-6)) / (np.log(14e-6) - np.log(3.5e-6)), 0.0, 1.0)
                delta_rho = delta_rho_small * (1 - blend) + delta_rho_large * blend
                Ga[i, j] = criteria.ga_dep_closed_form(a, delta_rho, g, MU, T_K, gamma_w, r1.L, r1.D)
                Lam[i, j] = criteria.lambda_g(a, delta_rho, g, MU, r1.L, r1.U, r1.D)
        n_outside_validity = len(caught)
    n_total = len(g_vals_ms2) * len(d_vals)
    print(f"fig1: {n_outside_validity}/{n_total} grid points ({100*n_outside_validity/n_total:.1f}%) "
          f"outside Stokes validity (Re_p > 0.34); biased high there, mostly large-d/high-g corner.")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    for ax, Z, title, label in (
        (axes[0], Ga, r"$Ga_{dep}$ (wall-delivery: gravity vs. hydrodynamic)", r"$Ga_{dep}$"),
        (axes[1], Lam, r"$\Lambda_g$ (Hazen number: settle within segment?)", r"$\Lambda_g$"),
    ):
        cs = ax.contourf(d_vals * 1e6, g_vals_ms2 / constants.G_EARTH, np.log10(np.clip(Z, 1e-12, 1e12)), levels=30, cmap="RdBu_r")
        ax.contour(d_vals * 1e6, g_vals_ms2 / constants.G_EARTH, Z, levels=[1.0], colors="black", linewidths=2.0)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.axhline(constants.G_MARS / constants.G_EARTH, color="darkorange", ls="--", lw=1.2, label="Mars g")
        ax.axhline(constants.G_MOON / constants.G_EARTH, color="dimgray", ls="--", lw=1.2, label="Moon g")
        ax.axhline(1.0, color="steelblue", ls="--", lw=1.2, label="Earth g")
        ax.set_xlabel(r"particle/floc diameter $d$ ($\mu$m)")
        ax.set_ylabel(r"$g / g_{Earth}$")
        ax.set_title(title)
        fig.colorbar(cs, ax=ax, label=f"log10({label})")
        ax.legend(loc="lower right", fontsize=8)

    fig.suptitle("Gravity-relevance regime map, WPA nominal line (R1). Black contour: criterion = 1.")
    fig.tight_layout()
    out = FIG_DIR / "fig1_regime_map_size_vs_g.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


def fig2_g_star_vs_diameter():
    """Reproduce derivation.md §3.2 table: g* sensitivity to the ASSUMED tube diameter."""
    from eclss_gravity.particles import P1_CELL

    Q = hydrodynamics.REGIME_R1_WPA_NOMINAL.Q
    L = hydrodynamics.REGIME_R1_WPA_NOMINAL.L
    diameters = np.array(hydrodynamics.STANDARD_TUBE_DIAMETERS_M)
    g_stars = []
    for D in diameters:
        U = hydrodynamics.bulk_velocity(Q, D)
        gamma_w, _, _ = hydrodynamics.wall_shear(U, D, RHO_F, MU)
        g_star = criteria.g_star_dif(P1_CELL.a, P1_CELL.delta_rho, MU, T_K, gamma_w, L, D)
        g_stars.append(g_star / constants.G_EARTH)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(diameters * 1000, g_stars, "o-", color="steelblue")
    ax.axhline(constants.G_MARS / constants.G_EARTH, color="darkorange", ls="--", label="Mars g")
    ax.axhline(constants.G_MOON / constants.G_EARTH, color="dimgray", ls="--", label="Moon g")
    ax.axvline(6.35, color="gray", ls=":", lw=1, label="assumed D = 1/4 in")
    ax.set_xlabel("assumed WPA/UPA line internal diameter (mm)")
    ax.set_ylabel(r"single-cell crossover $g^* / g_{Earth}$")
    ax.set_title("Sensitivity of $g^*$ to the one ASSUMED geometric input")
    ax.legend()
    fig.tight_layout()
    out = FIG_DIR / "fig2_g_star_vs_diameter.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")

    df = pd.DataFrame({"D_mm": diameters * 1000, "g_star_over_gE": g_stars})
    df.to_csv(DATA_DIR / "g_star_vs_diameter.csv", index=False)


def headline_table():
    """The single numeric table backing derivation.md §8.6, regenerated (not copy-pasted)."""
    from eclss_gravity.particles import P1_CELL, P3_MEDIAN_FLOC, P4_LARGE_FLOC

    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    gamma_w, tau_w, _ = hydrodynamics.wall_shear(r1.U, r1.D, RHO_F, MU)

    rows = []
    for label, g in (("Earth", constants.G_EARTH), ("Mars", constants.G_MARS), ("Moon", constants.G_MOON)):
        rows.append({
            "gravity": label,
            "Ga_dep_cell_R1": criteria.ga_dep_closed_form(P1_CELL.a, P1_CELL.delta_rho, g, MU, T_K, gamma_w, r1.L, r1.D),
            "Ga_dep_floc100um_R1": criteria.ga_dep_closed_form(P3_MEDIAN_FLOC.a, P3_MEDIAN_FLOC.delta_rho, g, MU, T_K, gamma_w, r1.L, r1.D),
            "Lambda_g_floc100um_R1": criteria.lambda_g(P3_MEDIAN_FLOC.a, P3_MEDIAN_FLOC.delta_rho, g, MU, r1.L, r1.U, r1.D),
            "Lambda_g_floc183um_R1": criteria.lambda_g(P4_LARGE_FLOC.a, P4_LARGE_FLOC.delta_rho, g, MU, r1.L, r1.U, r1.D),
            "Sigma_g_floc183um_R1": criteria.sigma_g(P4_LARGE_FLOC.a, P4_LARGE_FLOC.delta_rho, g, MU, gamma_w),
        })
    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "regime_sweep_headline.csv", index=False)
    print(df.to_string(index=False))
    print(f"wrote {DATA_DIR / 'regime_sweep_headline.csv'}")


if __name__ == "__main__":
    headline_table()
    fig1_regime_map()
    fig2_g_star_vs_diameter()
