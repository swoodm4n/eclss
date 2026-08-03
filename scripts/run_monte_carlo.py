"""Monte Carlo uncertainty propagation. derivation.md §7.3(b), §9.9.

Produces:
  results/figures/fig5_monte_carlo_g_star.png
  results/data/monte_carlo_g_star.csv
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclss_gravity import constants, hydrodynamics, uncertainty  # noqa: E402

FIG_DIR = ROOT / "results" / "figures"
DATA_DIR = ROOT / "results" / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

N_SAMPLES = 10_000


def main():
    r1 = hydrodynamics.REGIME_R1_WPA_NOMINAL
    result = uncertainty.monte_carlo_g_star(r1.Q, r1.L, n_samples=N_SAMPLES, seed=uncertainty.RNG_SEED)

    g_star_over_gE = result.g_star / constants.G_EARTH
    finite = np.isfinite(g_star_over_gE)
    p5, p50, p95 = np.percentile(g_star_over_gE[finite], [5, 50, 95])

    p_dominant_mars = (result.Ga_dep_at_mars > 1).mean()
    p_dominant_moon = (result.Ga_dep_at_moon > 1).mean()
    p_dominant_earth = (result.Ga_dep_at_earth > 1).mean()

    summary = {
        "n_samples": N_SAMPLES,
        "seed": uncertainty.RNG_SEED,
        "g_star_p5_over_gE": p5,
        "g_star_p50_over_gE": p50,
        "g_star_p95_over_gE": p95,
        "P_Ga_dep_gt_1_at_Earth": p_dominant_earth,
        "P_Ga_dep_gt_1_at_Mars": p_dominant_mars,
        "P_Ga_dep_gt_1_at_Moon": p_dominant_moon,
    }
    print(summary)

    import pandas as pd

    pd.DataFrame([summary]).to_csv(DATA_DIR / "monte_carlo_g_star_summary.csv", index=False)
    pd.DataFrame({
        "d_um": result.d * 1e6, "delta_rho": result.delta_rho, "D_tube_mm": result.D_tube * 1e3,
        "T_K": result.T_K, "g_star_over_gE": g_star_over_gE,
        "Ga_dep_earth": result.Ga_dep_at_earth, "Ga_dep_mars": result.Ga_dep_at_mars, "Ga_dep_moon": result.Ga_dep_at_moon,
    }).to_csv(DATA_DIR / "monte_carlo_g_star_samples.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    finite_vals = g_star_over_gE[np.isfinite(g_star_over_gE) & (g_star_over_gE > 0)]
    axes[0].hist(np.log10(finite_vals), bins=60, color="steelblue", alpha=0.8)
    axes[0].axvline(np.log10(constants.G_MARS / constants.G_EARTH), color="darkorange", ls="--", label="Mars g")
    axes[0].axvline(np.log10(constants.G_MOON / constants.G_EARTH), color="dimgray", ls="--", label="Moon g")
    axes[0].axvline(np.log10(p50), color="black", ls="-", lw=1, label=f"median = {p50:.3g} $g_E$")
    axes[0].set_xlabel(r"$\log_{10}(g^* / g_{Earth})$")
    axes[0].set_ylabel("Monte Carlo samples")
    axes[0].set_title(f"$g^*$ distribution (N={N_SAMPLES:,})\n90% interval: [{p5:.3g}, {p95:.3g}] $g_E$")
    axes[0].legend(fontsize=8)

    labels = ["Earth", "Mars", "Moon"]
    probs = [p_dominant_earth, p_dominant_mars, p_dominant_moon]
    axes[1].bar(labels, probs, color=["steelblue", "darkorange", "dimgray"])
    axes[1].set_ylabel(r"P($Ga_{dep} > 1$) across sampled particle population")
    axes[1].set_title("Probability gravity dominates wall-delivery,\naccounting for size/density/geometry uncertainty")
    axes[1].set_ylim(0, 1)
    for i, p in enumerate(probs):
        axes[1].text(i, p + 0.02, f"{p:.2f}", ha="center")

    fig.tight_layout()
    out = FIG_DIR / "fig5_monte_carlo_g_star.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
