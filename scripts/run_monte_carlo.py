"""Monte Carlo uncertainty propagation. derivation.md §7.3(b), §9.9.

CORRECTED (Phase 4 red-team, redteam_report.md Finding 4.9): reports per-branch (single-cell
diffusion-branch vs floc interception-branch) statistics, not a combined mixture median/interval.
The original combined "median 0.154 g_E, 90% interval [1.2e-4, 1.44] g_E" landed in the empty
valley of a bimodal distribution where no actual sample sits (visible as a dip in the histogram)
and is not a meaningful summary of either population.

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
    is_large = result.is_large_mode

    import pandas as pd

    branch_summaries = []
    for branch_name, mask in (("single_cell_diffusion_branch", ~is_large), ("floc_interception_branch", is_large)):
        gvals = g_star_over_gE[mask]
        finite = np.isfinite(gvals) & (gvals > 0)
        p5, p50, p95 = np.percentile(gvals[finite], [5, 50, 95])
        branch_summaries.append({
            "branch": branch_name, "n_samples": int(mask.sum()),
            "g_star_p5_over_gE": p5, "g_star_p50_over_gE": p50, "g_star_p95_over_gE": p95,
            "P_Ga_dep_gt_1_at_Earth": (result.Ga_dep_at_earth[mask] > 1).mean(),
            "P_Ga_dep_gt_1_at_Mars": (result.Ga_dep_at_mars[mask] > 1).mean(),
            "P_Ga_dep_gt_1_at_Moon": (result.Ga_dep_at_moon[mask] > 1).mean(),
        })
    summary_df = pd.DataFrame(branch_summaries)
    print(summary_df.to_string(index=False))
    summary_df.to_csv(DATA_DIR / "monte_carlo_g_star_summary.csv", index=False)

    pd.DataFrame({
        "d_um": result.d * 1e6, "delta_rho": result.delta_rho, "D_tube_mm": result.D_tube * 1e3,
        "T_K": result.T_K, "is_large_mode": result.is_large_mode, "g_star_over_gE": g_star_over_gE,
        "Ga_dep_earth": result.Ga_dep_at_earth, "Ga_dep_mars": result.Ga_dep_at_mars, "Ga_dep_moon": result.Ga_dep_at_moon,
    }).to_csv(DATA_DIR / "monte_carlo_g_star_samples.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for mask, color, name in ((~is_large, "steelblue", "single cells (diffusion branch)"), (is_large, "darkorange", "flocs (interception branch)")):
        vals = g_star_over_gE[mask]
        finite_vals = vals[np.isfinite(vals) & (vals > 0)]
        axes[0].hist(np.log10(finite_vals), bins=40, color=color, alpha=0.55, label=name, density=True)
    axes[0].axvline(np.log10(constants.G_MARS / constants.G_EARTH), color="black", ls="--", lw=1, label="Mars g")
    axes[0].axvline(np.log10(constants.G_MOON / constants.G_EARTH), color="dimgray", ls=":", lw=1, label="Moon g")
    axes[0].set_xlabel(r"$\log_{10}(g^* / g_{Earth})$")
    axes[0].set_ylabel("density")
    axes[0].set_title(f"$g^*$ distribution BY BRANCH (N={N_SAMPLES:,})\n(reported separately -- see redteam_report.md Finding 4.9)")
    axes[0].legend(fontsize=7)

    labels = ["Earth", "Mars", "Moon"]
    x = np.arange(3)
    width = 0.35
    for k, (branch_mask, color, name) in enumerate(((~is_large, "steelblue", "cells"), (is_large, "darkorange", "flocs"))):
        probs = [(result.Ga_dep_at_earth[branch_mask] > 1).mean(), (result.Ga_dep_at_mars[branch_mask] > 1).mean(), (result.Ga_dep_at_moon[branch_mask] > 1).mean()]
        bars = axes[1].bar(x + (k - 0.5) * width, probs, width, color=color, label=name)
        for xi, p in zip(x + (k - 0.5) * width, probs):
            axes[1].text(xi, p + 0.02, f"{p:.2f}", ha="center", fontsize=8)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].set_ylabel(r"P($Ga_{dep} > 1$), by branch")
    axes[1].set_title("Probability gravity dominates wall-delivery,\nreported per particle-size branch")
    axes[1].set_ylim(0, 1.15)
    axes[1].legend(fontsize=8)

    fig.tight_layout()
    out = FIG_DIR / "fig5_monte_carlo_g_star.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
