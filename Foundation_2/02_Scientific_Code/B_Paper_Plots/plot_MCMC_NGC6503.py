#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
plot_MCMC_NGC6503.py -- 06/10/2026 (FIG-NGC6503-01), promoted 07/10/2026
Four-panel figure of the NGC 6503 MCMC, drawn from the REAL chain of
Scripts_F2/mcmc_ngc6503_sparc.py (SPARC rotmod file, 31 points, emcee 32 walkers,
6000 steps, 2000 burn-in, fixed seed placed before the sampler -- REPRO-01b).

Replaces the former plot_MCMC_NGC6503.py, which drew 60,000 samples from a Gaussian
with hard-coded mean/covariance (seed 42) and printed +-0.22 / +-0.20 / V_inf 114.0 +- 3.5,
values that F2 declares superseded.

Every number shown is computed from the chain: medians and 16-84 % intervals, best fit
(maximum log-probability sample), chi2_nu = chi2_min/(N-2), correlation log rho0 - R_s.
Output: Fig_MCMC_NGC6503.png
"""
import os, sys, io, contextlib, runpy
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

ICI = os.path.dirname(os.path.abspath(__file__))
CHAIN_SCRIPT = os.path.normpath(os.path.join(ICI, "..", "mcmc_ngc6503_sparc.py"))
if not os.path.exists(CHAIN_SCRIPT):
    print(f"[ERROR] {CHAIN_SCRIPT} not found"); sys.exit(1)       # RULE 23: no degraded figure
with contextlib.redirect_stdout(io.StringIO()):
    M = runpy.run_path(CHAIN_SCRIPT)
ch, vi, out = M["ch"], M["vi"], M["out"]
r, v, e, vbar2, best = M["r"], M["v"], M["e"], M["vbar2"], M["best"]
vinf_kms = M["vinf_kms"]
lrho, rs = ch[:, 0], ch[:, 1]

def fmt(q, nd):
    m, up, dn = q
    return rf"{m:.{nd}f}^{{+{up:.{nd}f}}}_{{-{dn:.{nd}f}}}"

s_rho, s_rs, s_v = fmt(out["log10_rho0"], 3), fmt(out["Rs"], 3), fmt(out["Vinf"], 2)
chi2nu, corr = out["chi2_red_min"], out["corr_lrho_Rs"]

# best-fit rotation curve
rr = np.linspace(max(r.min() * 0.5, 0.05), r.max() * 1.03, 400)
vb_interp = np.sqrt(np.clip(np.interp(rr, r, vbar2), 0, None))
vi_best = vinf_kms(*best)
def vhalo(x_r, rs_):
    x = x_r / rs_
    return np.sqrt(np.abs(vi_best ** 2 * (1 - np.arctan(x) / x)))
v_tot = np.sqrt(vb_interp ** 2 + vhalo(rr, best[1]) ** 2)

fig = plt.figure(figsize=(16, 13))
gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.28)
fig.suptitle("NGC 6503 — ECF halo MCMC (SPARC, 31 points)\n"
             rf"$\log_{{10}}\rho_0={s_rho}$  |  $R_s={s_rs}$ kpc  |  $V_\infty={s_v}$ km/s  |  "
             rf"$\chi^2_\nu={chi2nu:.2f}$  |  corr$(\log\rho_0,R_s)={corr:.3f}$",
             fontsize=14, fontweight="bold")

# (1) rotation curve
ax = fig.add_subplot(gs[0, 0])
ax.errorbar(r, v, yerr=e, fmt="o", color="black", ms=4, capsize=2, label="SPARC data (NGC 6503)")
ax.plot(rr, vb_interp, "--", color="steelblue", lw=2, label="Newtonian baryons")
ax.plot(rr, v_tot, "-", color="crimson", lw=2.5, label=rf"ECF fit (best, $\chi^2_\nu={chi2nu:.2f}$)")
ax.fill_between(rr, vb_interp, v_tot, color="crimson", alpha=0.12, label="Torsion DM contribution")
ax.set_xlabel("Radius (kpc)"); ax.set_ylabel("Velocity (km/s)")
ax.set_title("Rotation curve, best-fit sample", fontweight="bold"); ax.grid(ls=":", alpha=0.5)
ax.legend(loc="lower right", fontsize=9)

# (2) 2D posterior: hexbin + KDE contours enclosing 68 / 95 / 99.7 %
ax2 = fig.add_subplot(gs[0, 1])
hb = ax2.hexbin(lrho, rs, gridsize=60, cmap="Blues", mincnt=1)
fig.colorbar(hb, ax=ax2, label="Counts")
sub = ch[np.random.default_rng(0).choice(len(ch), size=min(20000, len(ch)), replace=False)]
kde = gaussian_kde(sub.T)
dens = kde(sub.T)
levels = sorted(np.percentile(dens, [100 - 99.7, 100 - 95.0, 100 - 68.0]))
X, Y = np.meshgrid(np.linspace(lrho.min(), lrho.max(), 150), np.linspace(rs.min(), rs.max(), 150))
Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
ax2.contour(X, Y, Z, levels=levels, colors="k", linewidths=[0.8, 1.2, 1.6])
ax2.axvline(best[0], color="red", ls="--", lw=1.5); ax2.axhline(best[1], color="red", ls="--", lw=1.5)
ax2.set_xlabel(r"$\log_{10}\rho_0$ [g cm$^{-3}$]"); ax2.set_ylabel(r"$R_s$ (kpc)")
ax2.set_title(rf"Joint posterior (68/95/99.7 %), corr $={corr:.3f}$", fontweight="bold")

# (3) marginal log rho0
ax3 = fig.add_subplot(gs[1, 0])
ax3.hist(lrho, bins=80, density=True, color="steelblue", alpha=0.7)
p16, p50, p84 = np.percentile(lrho, [16, 50, 84])
ax3.axvline(best[0], color="red", ls="--", lw=2, label=rf"best fit {best[0]:.3f}")
for x_ in (p16, p84): ax3.axvline(x_, color="red", ls=":", lw=1.3)
ax3.axvspan(p16, p84, color="red", alpha=0.08, label=rf"median ${s_rho}$")
ax3.set_xlabel(r"$\log_{10}\rho_0$ [g cm$^{-3}$]"); ax3.set_ylabel("Posterior density")
ax3.set_title(r"Marginal posterior — $\log_{10}\rho_0$", fontweight="bold"); ax3.legend(fontsize=9)

# (4) marginals R_s (red) and V_inf (green, twin axis)
ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(rs, bins=80, density=True, color="tomato", alpha=0.7, label=rf"$R_s={s_rs}$ kpc")
ax4.axvline(best[1], color="darkred", ls="--", lw=2, label=rf"best fit $R_s={best[1]:.3f}$ kpc")
ax4.set_xlabel(r"$R_s$ (kpc)", color="darkred"); ax4.set_ylabel("Posterior density")
ax4b = ax4.twiny()
ax4b.hist(vi, bins=80, density=True, color="seagreen", alpha=0.45, label=rf"$V_\infty={s_v}$ km/s")
ax4b.set_xlabel(r"$V_\infty$ (km/s)", color="darkgreen")
h1, l1 = ax4.get_legend_handles_labels(); h2, l2 = ax4b.get_legend_handles_labels()
ax4.legend(h1 + h2, l1 + l2, fontsize=9, loc="upper right")
ax4b.set_title(r"Marginals — $R_s$ (red) and $V_\infty$ (green)", fontweight="bold", pad=10)

OUT = os.path.join(ICI, "Fig_MCMC_NGC6503.png")
fig.savefig(OUT, dpi=150, bbox_inches="tight")
print(f"[OK] {OUT}")
print(f"log10_rho0 = {s_rho} ; R_s = {s_rs} kpc ; V_inf = {s_v} km/s ; chi2_nu = {chi2nu:.4f} ; corr = {corr:.4f}")
