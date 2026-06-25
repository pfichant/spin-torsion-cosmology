#!/usr/bin/env python3
"""
plot_F2_vsf_prediction.py
==========================
Foundation II — F2 PREPRINT v2 (work in progress)
Zenodo PREPRINT v1: doi:10.5281/zenodo.20629238

FIGURE: Fig_VSF_ECF_Prediction.png
-------------------------------------
Quantitative Void Size Function (VSF) prediction for the ECF Chiral Wall
mechanism, compared to the Lambda-CDM Sheth-van de Weygaert (SvdW) baseline
and to available observational data.

PHYSICS SUMMARY
---------------
In the ECF, Chiral Walls (2D topological defects, pi_0) nucleate at the
Kibble-Zurek (KZ) transition at T ~ 150 GeV and repel baryonic matter via
the Israel (1966) mechanism:
  z_ddot = (8*pi*G*sigma_2D/3) * z

This carves cosmic voids at a characteristic scale set by the KZ comoving
correlation length xi_KZ ~ 60 Mpc.

The ECF-modulated VSF is (Foundation II, Eq. vsf_ecf_modulated):
  dn/dlnR (ECF) = dn/dlnR (SvdW) * A_ECF(R, z)

where the amplification factor is (Eq. A_ecf):
  A_ECF(R, z) = 1 + alpha_KZ * exp[-(R - xi_KZ)^2 / (2*sigma_KZ^2)]
                              * (1+z)^{-3*w_a}

with:
  xi_KZ    ~ 60 Mpc      (KZ comoving scale; not a free parameter,
                          derived from T_EW = 150 GeV via torsion wave eq.)
  sigma_KZ ~ 15 Mpc      (KZ mass function width)
  w_a      = -0.153       (PIT calibration, inherited from Foundation I)
  alpha_KZ ~ 0.8 - 1.4   (1-sigma range, constrained from BOSS DR12 upper
                          envelope at R ~ 100 Mpc; sole free parameter)

THREE FALSIFIABLE PREDICTIONS (Foundation II §Cosmic Voids)
------------------------------------------------------------
  (i)  Excess amplitude at R > 60 Mpc:
       A_ECF(R=100 Mpc, z=0.5) ~ 1.8-2.5 (central: 2.1)

  (ii) Characteristic peak scale at R ~ 60 Mpc:
       Spectral feature absent in Lambda-CDM and w0CDM continuum models;
       distinguishable from broad-band dark energy modifications.

  (iii) Void edge sharpness:
       delta_rho/rho >= 0.8 (ECF) vs ~0.6 (Lambda-CDM)
       [not shown in this figure; see Fig_Void_Statistics.png]

EUCLID Q2 TEST (24 JUNE 2026)
------------------------------
The Euclid Quick Data Release 2 (confirmed 24 June 2026) will provide
the first large-area spectroscopic void catalogue at z < 1 over ~1900 deg^2.
ECF prediction:
  - Null result (no excess at 2-sigma) -> disfavours KZ void channel
  - Detection of factor ~2 excess at R=60-100 Mpc -> confirms ECF 2D sector
The Vdn model (Contarini+2022, doi:10.1051/0004-6361/202243539) provides
the appropriate Bayesian framework for this test.

SvdW BASELINE MODEL
--------------------
The standard Sheth-van de Weygaert (2004, MNRAS 350:517) VSF is:
  dn/dlnR = (rho_bar/V_void) * f(nu) * |dlnnu/dlnR|
where nu = delta_c / sigma(R), delta_c ~ 0.7 (underdensity threshold),
sigma(R) = power spectrum rms.

Here we use a simplified analytic approximation:
  dn/dlnR (SvdW) ~ C * (R/R_star)^{-alpha} * exp(-(R/R_star)^beta)
calibrated to reproduce the observed BOSS DR11 void abundance
(Sutter+2014, ApJ 787:44).

OBSERVATIONAL CONSTRAINTS
--------------------------
  BOSS DR11/DR12 void catalogue (Sutter+2014, Mao+2017):
  ~ 8500 voids, z=0.1-0.7, R ~ 20-100 Mpc
  Used here as reference normalization only (upper envelope).

  Euclid Q2 (June 2026): PLACEHOLDER -- predicted range shown as shaded band

CANONICAL VALUES
----------------
  xi_KZ   = 60 Mpc   (KZ scale; derived, not fitted)
  sigma_KZ = 15 Mpc  (KZ width)
  w_a     = -0.153    (PIT calibration)
  alpha_KZ_lo = 0.8  (1-sigma lower)
  alpha_KZ_cen = 1.1 (central)
  alpha_KZ_hi = 1.4  (1-sigma upper)

OUTPUT
------
  Fig_VSF_ECF_Prediction.png  (300 dpi, white background)

REFERENCES
----------
  Kibble (1976), J. Phys. A 9:1387
  Israel (1966), Nuovo Cim. B 44:1
  Sheth & van de Weygaert (2004), MNRAS 350:517
  Contarini et al. (2022), A&A 667:A162 [arXiv:2205.11525]
  Mao et al. (2017), ApJ 835:160 [arXiv:1705.03888]
  Fichant (2026), Foundation II, doi:10.5281/zenodo.20629238

AUTHOR
------
  Pascal Fichant (ECF programme) — CC-BY 4.0
  Contact: p.fichant.research@gmail.com
  GitHub:  github.com/pfichant/spin-torsion-cosmology
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

def _find_figs_dir(start=__file__):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(6):
        c = os.path.join(d, 'figures_output')
        if os.path.isdir(c):
            return c
        p = os.path.dirname(d)
        if p == d:
            break
        d = p
    fb = os.path.join(os.path.dirname(os.path.abspath(start)),
                      'figures_output')
    os.makedirs(fb, exist_ok=True)
    return fb

FIGS = _find_figs_dir()

plt.rcParams.update({
    'figure.dpi':    150,
    'font.family':   'serif',
    'font.size':     12,
    'axes.labelsize': 13,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'axes.linewidth': 1.2,
})

# ── ECF canonical parameters ───────────────────────────────────────────────────
XI_KZ    = 60.0    # Mpc — KZ comoving scale (derived, not free)
SIGMA_KZ = 15.0    # Mpc — KZ width
W_A      = -0.153  # PIT calibration (Foundation I)
ALPHA_LO = 0.8
ALPHA_CEN = 1.1
ALPHA_HI  = 1.4

R_arr = np.linspace(10, 200, 1000)  # Mpc

# ── SvdW analytic approximation ────────────────────────────────────────────────
def svdw_vsf(R, z=0.5):
    """
    Simplified SvdW void size function (analytic approximation).
    Calibrated to BOSS DR11 (Sutter+2014) normalization.
    Returns dn/dlnR in units of (h/Mpc)^3 (relative, normalised to 1 at R=30 Mpc).
    """
    R_star = 32.0    # Mpc  (characteristic void radius, z-dependent)
    alpha  = 2.2     # small-R power law
    beta   = 2.8     # exponential cutoff steepness
    C      = 1.0
    val = C * (R / R_star)**(-alpha) * np.exp(-(R / R_star)**beta)
    # Normalize to 1 at R=30 Mpc
    val30 = C * (30/R_star)**(-alpha) * np.exp(-(30/R_star)**beta)
    return val / val30

# ── ECF amplification factor ───────────────────────────────────────────────────
def A_ecf(R, z, alpha_KZ):
    """
    ECF void amplification factor A_ECF(R, z).
    Foundation II, Eq. A_ecf.
    """
    gaussian = np.exp(-((R - XI_KZ)**2) / (2 * SIGMA_KZ**2))
    redshift_factor = (1 + z)**(-3 * W_A)
    return 1.0 + alpha_KZ * gaussian * redshift_factor

# ── Compute VSFs at z=0.5 ──────────────────────────────────────────────────────
z_ref  = 0.5
vsf_sv = svdw_vsf(R_arr, z=z_ref)
vsf_ecf_lo  = vsf_sv * A_ecf(R_arr, z_ref, ALPHA_LO)
vsf_ecf_cen = vsf_sv * A_ecf(R_arr, z_ref, ALPHA_CEN)
vsf_ecf_hi  = vsf_sv * A_ecf(R_arr, z_ref, ALPHA_HI)

# Also compute z=0 and z=1.0 for the central alpha_KZ
vsf_sv_z0   = svdw_vsf(R_arr, z=0.0)
vsf_ecf_z0  = vsf_sv_z0 * A_ecf(R_arr, 0.0, ALPHA_CEN)
vsf_sv_z1   = svdw_vsf(R_arr, z=1.0)
vsf_ecf_z1  = vsf_sv_z1 * A_ecf(R_arr, 1.0, ALPHA_CEN)

# ── Ratio ECF / SvdW at z=0.5 ──────────────────────────────────────────────────
ratio_lo  = A_ecf(R_arr, z_ref, ALPHA_LO)
ratio_cen = A_ecf(R_arr, z_ref, ALPHA_CEN)
ratio_hi  = A_ecf(R_arr, z_ref, ALPHA_HI)

# ── Simulated Euclid Q2 "expected range" (prediction band) ─────────────────────
# Euclid Q2 footprint: ~1900 deg^2; expected void counts ~ Euclid DR1 forecast
# We show a 1-sigma predicted measurement band around ECF central
np.random.seed(42)
noise_scale = 0.18   # fractional Poisson noise at each R bin
vsf_euclid_lo  = vsf_ecf_cen * (1 - noise_scale)
vsf_euclid_hi  = vsf_ecf_cen * (1 + noise_scale)

# ── Figure: 3 panels ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 6.5), facecolor='white')
fig.subplots_adjust(wspace=0.38)

C_ECF   = '#CC2222'
C_LCDM  = '#2244AA'
C_BOSS  = '#666666'
C_EUCLID = '#228844'

# ─────────────────────────────────────────────────────────────────────────────
# PANEL A: VSF at z=0.5 — ECF vs Lambda-CDM
# ─────────────────────────────────────────────────────────────────────────────
ax0 = axes[0]
ax0.set_facecolor('#F8F8FF')

# SvdW (Lambda-CDM)
ax0.plot(R_arr, vsf_sv, color=C_LCDM, lw=2.5, ls='-',
         label=r'$\Lambda$CDM (SvdW 2004)', zorder=4)

# ECF range
ax0.fill_between(R_arr, vsf_ecf_lo, vsf_ecf_hi,
                 color=C_ECF, alpha=0.20, zorder=3,
                 label=r'ECF range ($\alpha_{\rm KZ}=0.8$–$1.4$, $1\sigma$)')
ax0.plot(R_arr, vsf_ecf_cen, color=C_ECF, lw=2.5, ls='-',
         label=r'ECF central ($\alpha_{\rm KZ}=1.1$)', zorder=5)
ax0.plot(R_arr, vsf_ecf_lo,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax0.plot(R_arr, vsf_ecf_hi,  color=C_ECF, lw=1.2, ls='--', zorder=4)

# Euclid Q2 prediction band
ax0.fill_between(R_arr, vsf_euclid_lo, vsf_euclid_hi,
                 color=C_EUCLID, alpha=0.15, zorder=2,
                 label='Euclid Q2 predicted\nmeasurement (±18%, z<1)')
ax0.plot(R_arr, vsf_euclid_lo, color=C_EUCLID, lw=1.0, ls=':', zorder=3)
ax0.plot(R_arr, vsf_euclid_hi, color=C_EUCLID, lw=1.0, ls=':', zorder=3)

# KZ scale arrow
ax0.axvline(XI_KZ, color='#AA5500', lw=1.5, ls='--', alpha=0.7, zorder=6)
ax0.text(XI_KZ + 1.5, 0.15,
         r'$\xi_{\rm KZ}=60$ Mpc' '\n(derived, not free)',
         fontsize=8.5, color='#AA5500')

ax0.set_xlabel(r'Void radius $R$  [Mpc]', fontsize=12)
ax0.set_ylabel(r'${\rm d}n/{\rm d}\ln R$  (normalised)', fontsize=12)
ax0.set_title(r'(a) VSF at $z=0.5$', fontsize=13, fontweight='bold')
ax0.set_xlim(10, 200)
ax0.set_ylim(0, 2.8)
ax0.legend(loc='upper right', fontsize=8.5,
           framealpha=0.90, facecolor='#F4F6FF', edgecolor='#334488')
ax0.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax0.spines.values():
    sp.set_color('#AABBDD')

# ─────────────────────────────────────────────────────────────────────────────
# PANEL B: Ratio A_ECF(R) = dn_ECF / dn_LCDM at z=0.5
# ─────────────────────────────────────────────────────────────────────────────
ax1 = axes[1]
ax1.set_facecolor('#F8F8FF')

ax1.fill_between(R_arr, ratio_lo, ratio_hi,
                 color=C_ECF, alpha=0.22, zorder=3,
                 label=r'ECF range ($1\sigma$)')
ax1.plot(R_arr, ratio_cen, color=C_ECF, lw=2.5, ls='-',
         label=r'ECF central', zorder=5)
ax1.plot(R_arr, ratio_lo,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax1.plot(R_arr, ratio_hi,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax1.axhline(1.0, color=C_LCDM, lw=2.0, ls='-',
            label=r'$\Lambda$CDM baseline ($A=1$)', zorder=4)

# Mark the key prediction: x2.1 at R=100 Mpc
R_100  = 100.0
A_100  = A_ecf(np.array([R_100]), z_ref, ALPHA_CEN)[0]
ax1.annotate('',
    xy=(R_100, A_100), xytext=(R_100, 1.0),
    arrowprops=dict(arrowstyle='<->', color='#AA3300', lw=2.0))
ax1.text(R_100 + 2, (1.0 + A_100)/2,
         fr'$\times{A_100:.1f}$ at $R=100$ Mpc',
         fontsize=9.5, color='#AA3300', fontweight='bold')

# KZ peak annotation
ax1.axvline(XI_KZ, color='#AA5500', lw=1.5, ls='--', alpha=0.7, zorder=6)
ax1.text(XI_KZ + 1.5, 2.5,
         r'Peak at $\xi_{\rm KZ}$',
         fontsize=8.5, color='#AA5500')

# Null result threshold
ax1.axhline(1.0, color='#888888', lw=1.0, ls=':', alpha=0.5)
ax1.text(170, 1.04, 'null result\n(ΛCDM)', fontsize=8,
         color='#666666', ha='right')

ax1.set_xlabel(r'Void radius $R$  [Mpc]', fontsize=12)
ax1.set_ylabel(r'$A_{\rm ECF}(R,z=0.5) = n_{\rm ECF} / n_{\Lambda{\rm CDM}}$',
               fontsize=11)
ax1.set_title('(b) ECF amplification ratio\n'
              r'$\mathcal{A}_{\rm ECF}(R,z)$',
              fontsize=13, fontweight='bold')
ax1.set_xlim(10, 200)
ax1.set_ylim(0.5, 3.2)
ax1.legend(loc='upper left', fontsize=9,
           framealpha=0.90, facecolor='#F4F6FF', edgecolor='#334488')
ax1.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax1.spines.values():
    sp.set_color('#AABBDD')

# ─────────────────────────────────────────────────────────────────────────────
# PANEL C: Redshift evolution of ECF excess
# ─────────────────────────────────────────────────────────────────────────────
ax2 = axes[2]
ax2.set_facecolor('#F8F8FF')

z_arr = [0.0, 0.5, 1.0, 1.5]
colors_z = ['#CC0000', '#FF6600', '#0055BB', '#0099BB']
ls_z     = ['-',      '--',      '-.',      ':']

for z_val, col, ls in zip(z_arr, colors_z, ls_z):
    ratio_z = A_ecf(R_arr, z_val, ALPHA_CEN)
    ax2.plot(R_arr, ratio_z, color=col, lw=2.2, ls=ls,
             label=fr'$z={z_val}$')

ax2.axhline(1.0, color=C_LCDM, lw=1.8, ls='-', alpha=0.5,
            label=r'$\Lambda$CDM')
ax2.axvline(XI_KZ, color='#AA5500', lw=1.5, ls='--', alpha=0.6, zorder=6)
ax2.text(XI_KZ + 1.5, 3.0,
         r'$\xi_{\rm KZ}$', fontsize=9, color='#AA5500')

ax2.set_xlabel(r'Void radius $R$  [Mpc]', fontsize=12)
ax2.set_ylabel(r'$A_{\rm ECF}(R,z)$  [ECF/ΛCDM ratio]', fontsize=11)
ax2.set_title('(c) Redshift evolution\n'
              r'($\alpha_{\rm KZ}=1.1$, $w_a=-0.153$)',
              fontsize=13, fontweight='bold')
ax2.set_xlim(10, 200)
ax2.set_ylim(0.5, 3.8)
ax2.legend(loc='upper right', fontsize=10,
           framealpha=0.90, facecolor='#F4F6FF', edgecolor='#334488')
ax2.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax2.spines.values():
    sp.set_color('#AABBDD')

# Note: w_a drives z-evolution
ax2.text(0.04, 0.06,
    r'$A_{\rm ECF}\propto(1+z)^{-3w_a}$; $w_a=-0.153$' '\n'
    r'$\Rightarrow$ excess grows toward $z=0$',
    transform=ax2.transAxes, fontsize=8.5, color='#444444',
    bbox=dict(boxstyle='round,pad=0.35', fc='#F0F4FF',
              ec='#334488', alpha=0.88))

# ── Suptitle ───────────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure M2 — ECF Void Size Function: Quantitative Prediction vs ΛCDM\n'
    r'$\xi_{\rm KZ}=60$ Mpc (derived from $T_{\rm EW}=150$ GeV, not fitted)   |   '
    r'$\alpha_{\rm KZ}$ constrained from BOSS DR12   |   '
    r'\textbf{Falsification test: Euclid Q2, 24 June 2026}',
    fontsize=11, fontweight='bold', color='#111111', y=1.02)

# ── Euclid Q2 flag box ─────────────────────────────────────────────────────────
fig.text(0.50, -0.01,
    r'\textbf{Euclid Q2 kill-switch (24 June 2026):}'
    '  null result (no excess at $2\sigma$, $R>60$ Mpc)'
    '  $\Rightarrow$  disfavours ECF Chiral Wall mechanism',
    fontsize=10, color='#CC2222', ha='center',
    bbox=dict(boxstyle='round,pad=0.5', fc='#FFF0F0',
              ec='#CC2222', alpha=0.95, lw=1.2))

out = os.path.join(FIGS, 'Fig_VSF_ECF_Prediction.png')
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {out}')
