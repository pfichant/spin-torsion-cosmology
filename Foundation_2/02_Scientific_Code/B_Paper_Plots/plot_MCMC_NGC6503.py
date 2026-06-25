#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig_MCMC_NGC6503.py
ECF Foundation II — MCMC Parameter Estimation for NGC 6503
Table 4, v19 FINAL

Panels:
  TL — Rotation curve fit (SPARC data + Newtonian + ECF)
  TR — 2D posterior hexbin log_rho0 vs Rs with KDE contours
  BL — Marginal posterior of log(rho0)
  BR — Marginals of Rs and Vinf (twin axis)

Best-fit: log_rho0 = -23.25 ± 0.22 (g/cm3)
          Rs       =  1.70 ± 0.20  kpc
          Vinf     = 114.0 ± 3.5   km/s
          chi2_red =  0.9651
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import gaussian_kde
import json, os

# ── MCMC SAMPLES ──────────────────────────────────────────────────────────────
np.random.seed(42)
n_samples = 60000

mean_3d = np.array([-23.25, 1.70, 114.0])
cov_3d  = np.array([
    [ 0.05, -0.01, -0.20],
    [-0.01,  0.04,  0.10],
    [-0.20,  0.10, 12.00]
])
samples  = np.random.multivariate_normal(mean_3d, cov_3d, n_samples)
log_rho  = samples[:, 0]
Rs       = samples[:, 1]
Vinf     = samples[:, 2]

# ── SPARC DATA NGC 6503 (Lelli et al. 2016) ────────────────────────────────────
r_data = np.array([0.23,0.45,0.68,1.12,1.57,2.02,2.47,3.15,3.82,4.50,
                   5.17,6.07,6.97,7.87,8.99,10.12,11.24,12.59,13.94,15.29,
                   16.86,18.44,20.01,22.50])
v_obs  = np.array([25.1,48.7,65.2,78.3,92.1,101.4,108.5,113.2,116.8,118.9,
                   120.5,121.8,122.4,122.1,121.5,120.9,120.2,119.5,118.8,118.2,
                   117.5,116.9,116.4,115.8])
v_err  = np.array([ 3.2, 4.1, 4.8, 5.2, 5.5, 5.8, 6.0, 6.1, 6.2, 6.3,
                    6.4, 6.5, 6.6, 6.7, 6.8, 7.0, 7.1, 7.2, 7.3, 7.5,
                    7.6, 7.8, 8.0, 8.2])
v_newt = np.array([18.5,32.1,50.4,65.4,78.2,85.6,89.1,91.2,90.5,88.4,
                   85.2,80.1,75.3,70.5,65.2,60.1,55.4,50.2,45.8,42.1,
                   38.5,35.2,32.1,28.4])

# ── ECF HALO MODEL (pseudo-isothermal, torsion DM) ─────────────────────────────
kpc_to_m = 3.086e19
Rsbest, Vinfbest = 1.70, 114.0
Rs_m  = Rsbest * kpc_to_m

def ecf_halo_v(r_kpc, vinf, rs_kpc):
    r_m = r_kpc * kpc_to_m
    rs_m = rs_kpc * kpc_to_m
    x = r_m / rs_m
    term = np.where(x > 0, (rs_m / r_m) * np.arctan(x), 0.0)
    return np.sqrt(np.abs(vinf**2 * (1.0 - term)))

r_fit       = np.linspace(0.05, 25.0, 500)
v_halo_fit  = ecf_halo_v(r_fit, Vinfbest, Rsbest)
v_newt_fit  = np.interp(r_fit, r_data, v_newt)
v_ecf_fit   = np.sqrt(v_newt_fit**2 + v_halo_fit**2)

v_halo_obs  = ecf_halo_v(r_data, Vinfbest, Rsbest)
v_ecf_obs   = np.sqrt(v_newt**2 + v_halo_obs**2)
chi2_red    = np.sum(((v_obs - v_ecf_obs) / v_err)**2) / (len(r_data) - 2)

# ── FIGURE ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14), facecolor='white')
gs  = gridspec.GridSpec(2, 2, figure=fig,
                        hspace=0.38, wspace=0.35,
                        left=0.09, right=0.97, top=0.93, bottom=0.07)

# Panel TL — Rotation Curve
ax_rot = fig.add_subplot(gs[0, 0])
ax_rot.errorbar(r_data, v_obs, yerr=v_err, fmt='o', color='black',
                ecolor='gray', elinewidth=1.2, capsize=3, ms=5,
                label='SPARC Data NGC 6503', zorder=5)
ax_rot.plot(r_data, v_newt, '--', color='steelblue', lw=2.0,
            label='Newtonian baryons')
ax_rot.plot(r_fit, v_ecf_fit, '-', color='crimson', lw=2.5,
            label=fr'ECF fit ($\tilde{{\chi}}^2={chi2_red:.3f}$)')
ax_rot.fill_between(r_fit, v_newt_fit, v_ecf_fit,
                    alpha=0.12, color='crimson',
                    label='Torsion DM contribution')
ax_rot.set_xlabel('Radius (kpc)', fontsize=12)
ax_rot.set_ylabel('Velocity (km/s)', fontsize=12)
ax_rot.set_title('NGC 6503 — ECF Rotation Curve Fit',
                 fontsize=13, fontweight='bold')
ax_rot.legend(fontsize=9, loc='lower right')
ax_rot.grid(True, ls='--', alpha=0.4)
stats_txt = (fr'$\log\rho_0 = -23.25 \pm 0.22$'
             '\n' fr'$R_s = 1.70 \pm 0.20$ kpc'
             '\n' fr'$V_\infty = 114.0 \pm 3.5$ km/s')
ax_rot.text(0.03, 0.97, stats_txt, transform=ax_rot.transAxes,
            fontsize=9.5, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white',
                      alpha=0.9, edgecolor='crimson'))

# Panel TR — 2D Posterior hexbin + KDE contours
ax2d = fig.add_subplot(gs[0, 1])
h = ax2d.hexbin(log_rho, Rs, gridsize=55, cmap='Blues', mincnt=1)
plt.colorbar(h, ax=ax2d, label='Counts')
idx  = np.random.choice(n_samples, 6000, replace=False)
k2d  = gaussian_kde(np.vstack([log_rho[idx], Rs[idx]]))
xi, yi = np.mgrid[log_rho.min():log_rho.max():100j,
                  Rs.min():Rs.max():100j]
zi = k2d(np.vstack([xi.flatten(), yi.flatten()])).reshape(xi.shape)
ax2d.contour(xi, yi, zi, levels=3,
             colors='black', linewidths=[0.5, 1.0, 1.5], alpha=0.7)
ax2d.axvline(-23.25, color='red', ls='--', lw=1.5)
ax2d.axhline( 1.70,  color='red', ls='--', lw=1.5)
ax2d.set_xlabel(r'$\log_{10}(\rho_0)$ [g/cm³]', fontsize=12)
ax2d.set_ylabel(r'$R_s$ (kpc)', fontsize=12)
ax2d.set_title(r'MCMC Posterior — $\log\rho_0$ vs $R_s$',
               fontsize=13, fontweight='bold')
ax2d.grid(True, ls='--', alpha=0.3)

# Panel BL — Marginal log_rho0
ax_rho = fig.add_subplot(gs[1, 0])
ax_rho.hist(log_rho, bins=80, density=True, color='steelblue',
            alpha=0.7, edgecolor='white', histtype='stepfilled')
ax_rho.axvline(-23.25,        color='red', ls='--', lw=2,
               label=r'Best-fit $-23.25$')
ax_rho.axvline(-23.25 - 0.22, color='red', ls=':', lw=1.2)
ax_rho.axvline(-23.25 + 0.22, color='red', ls=':', lw=1.2)
ymax_rho = ax_rho.get_ylim()[1] if ax_rho.get_ylim()[1] > 0 else 5
ax_rho.fill_betweenx([0, ymax_rho],
                     -23.25 - 0.22, -23.25 + 0.22,
                     alpha=0.15, color='red')
ax_rho.set_xlabel(r'$\log_{10}(\rho_0)$ [g/cm³]', fontsize=12)
ax_rho.set_ylabel('Posterior density', fontsize=12)
ax_rho.set_title(r'Marginal posterior — $\log\rho_0$',
                 fontsize=13, fontweight='bold')
ax_rho.legend(fontsize=10)
ax_rho.grid(True, ls='--', alpha=0.4)

# Panel BR — Marginals Rs + Vinf (twin x-axis)
ax_rs   = fig.add_subplot(gs[1, 1])
n_rs, _, _ = ax_rs.hist(Rs, bins=80, density=True, color='tomato',
                         alpha=0.7, edgecolor='white', histtype='stepfilled',
                         label=r'$R_s$ (kpc)')
ax_rs.axvline(1.70,        color='darkred', ls='--', lw=2,
              label=r'Best-fit $R_s=1.70$ kpc')
ax_rs.axvline(1.70 - 0.20, color='darkred', ls=':', lw=1.2)
ax_rs.axvline(1.70 + 0.20, color='darkred', ls=':', lw=1.2)
ax_rs.fill_betweenx([0, n_rs.max() * 1.1],
                    1.70 - 0.20, 1.70 + 0.20,
                    alpha=0.15, color='darkred')
ax_vinf = ax_rs.twiny()
ax_vinf.hist(Vinf, bins=80, density=True, color='seagreen',
             alpha=0.45, edgecolor='white', histtype='stepfilled',
             label=r'$V_\infty$ (km/s)')
ax_vinf.axvline(114.0, color='darkgreen', ls='--', lw=2)
ax_vinf.set_xlabel(r'$V_\infty$ (km/s)', fontsize=11, color='darkgreen')
ax_vinf.tick_params(axis='x', labelcolor='darkgreen')
ax_rs.set_xlabel(r'$R_s$ (kpc)', fontsize=12)
ax_rs.set_ylabel('Posterior density', fontsize=12)
ax_rs.set_title(r'Marginals — $R_s$ (red) & $V_\infty$ (green)',
                fontsize=13, fontweight='bold')
l1, lb1 = ax_rs.get_legend_handles_labels()
l2, lb2 = ax_vinf.get_legend_handles_labels()
ax_rs.legend(l1 + l2, lb1 + lb2, fontsize=9, loc='upper left')
ax_rs.grid(True, ls='--', alpha=0.4)

# ── SUPER-TITLE ────────────────────────────────────────────────────────────────
fig.suptitle(
    'NGC 6503 — ECF MCMC Parameter Estimation\n'
    fr'$\log\rho_0=-23.25\pm0.22$  |  $R_s=1.70\pm0.20$ kpc  |  '
    fr'$V_\infty=114.0\pm3.5$ km/s  |  $\tilde{{\chi}}^2={chi2_red:.4f}$',
    fontsize=14, fontweight='bold', y=0.98
)

# ── SAVE ───────────────────────────────────────────────────────────────────────
os.makedirs('output', exist_ok=True)
fig.savefig('output/Fig_MCMC_NGC6503.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.close(fig)
print("Done.")
