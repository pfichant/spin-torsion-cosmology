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
Kibble-Zurek (KZ) transition at T ~ 159 GeV and repel baryonic matter via
the Israel (1966) mechanism:
  z_ddot = (8*pi*G*sigma_2D/3) * z

This carves cosmic voids at a characteristic scale set by the KZ comoving
correlation length xi_KZ ~ 60 Mpc.

The ECF-modulated VSF is (Foundation II, Eq. vsf_ecf_modulated):
  dn/dlnR (ECF) = dn/dlnR (SvdW) * A_ECF(R)

where the amplification factor is (Eq. A_ecf):
  A_ECF(R) = 1 + alpha_KZ * exp[-(R - xi_KZ)^2 / (2*sigma_KZ^2)]
  [22/09/2026, N-10 option (a)] the factor (1+z)^{-3*w_a} is WITHDRAWN
  (no derivation); no z-evolution is claimed; z-dependence open (PO-F3-XI).

with:
  xi_KZ    ~ 60 Mpc      (KZ comoving scale; ADOPTED value, calibration
                          procedure not documented (A-10, 22/09/2026); NOT
                          derived from T_EW -- see PO-F3-XI and the
                          canonical-values note below for the
                          24-orders-of-magnitude gap)
  sigma_KZ ~ 15 Mpc      (KZ mass function width)
  alpha_KZ ~ 0.8 - 1.4   (ADOPTED interval, central 1.1; calibration
                          procedure not documented -- N-8, 22/09/2026)

THREE FALSIFIABLE PREDICTIONS (Foundation II §Cosmic Voids)
------------------------------------------------------------
  (i)  Excess amplitude at the peak of the adopted spatial template:
       1 + alpha_KZ ~ 2.1 at R = xi_KZ (no value at a given z is claimed)

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
  xi_KZ   = 60 Mpc   (KZ scale; ADOPTED value, calibration procedure not
                     documented (A-10), NOT derived. This line read
                     'derived, not fitted' until 26/08/2026, which
                     contradicted Foundation II: direct Kibble-Zurek
                     dilution from T_EW misses the observed scale by
                     some 24 orders of magnitude, and the microscopic
                     origin is an open problem -- PO-F3-XI.)
  sigma_KZ = 15 Mpc  (KZ width)
  (w_a no longer enters A_ECF: factor withdrawn, N-10)
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
XI_KZ    = 60.0    # Mpc — KZ comoving scale (adopted, not derived — PO-F3-XI)
SIGMA_KZ = 15.0    # Mpc — KZ width
W_A      = -0.153  # no longer used by A_ecf (N-10, option (a), 22/09/2026); kept for reference
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
    # [22/09/2026, N-10 option (a)] the factor (1+z)^{-3*w_a} is withdrawn
    # (no derivation). The argument z is kept for call compatibility and is
    # not used: A_ECF depends on R only. z-dependence: PO-F3-XI (OPEN).
    return 1.0 + alpha_KZ * gaussian

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
                 label=r'ECF range ($\alpha_{\rm KZ}=0.8$–$1.4$, adopted)')
ax0.plot(R_arr, vsf_ecf_cen, color=C_ECF, lw=2.5, ls='-',
         label=r'ECF central ($\alpha_{\rm KZ}=1.1$)', zorder=5)
ax0.plot(R_arr, vsf_ecf_lo,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax0.plot(R_arr, vsf_ecf_hi,  color=C_ECF, lw=1.2, ls='--', zorder=4)

# Euclid Q2 prediction band
ax0.fill_between(R_arr, vsf_euclid_lo, vsf_euclid_hi,
                 color=C_EUCLID, alpha=0.15, zorder=2,
                 label='Euclid DR1 predicted\nmeasurement (±18%, z<1)')
ax0.plot(R_arr, vsf_euclid_lo, color=C_EUCLID, lw=1.0, ls=':', zorder=3)
ax0.plot(R_arr, vsf_euclid_hi, color=C_EUCLID, lw=1.0, ls=':', zorder=3)

# KZ scale arrow
ax0.axvline(XI_KZ, color='#AA5500', lw=1.5, ls='--', alpha=0.7, zorder=6)
ax0.text(XI_KZ + 1.5, 0.15,
         r'$\xi_{\rm KZ}=60$ Mpc' '\n(adopted, not derived — PO-F3-XI)',
         fontsize=8.5, color='#AA5500')

ax0.set_xlabel(r'Void radius $R$  [Mpc]', fontsize=12)
ax0.set_ylabel(r'${\rm d}n/{\rm d}\ln R$  (normalised)', fontsize=12)
ax0.set_title(r'(a) VSF (adopted template, no $z$-dependence claimed)', fontsize=13, fontweight='bold')
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
                 label=r'ECF range ($\alpha_{\rm KZ}$ adopted)')
ax1.plot(R_arr, ratio_cen, color=C_ECF, lw=2.5, ls='-',
         label=r'ECF central', zorder=5)
ax1.plot(R_arr, ratio_lo,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax1.plot(R_arr, ratio_hi,  color=C_ECF, lw=1.2, ls='--', zorder=4)
ax1.axhline(1.0, color=C_LCDM, lw=2.0, ls='-',
            label=r'$\Lambda$CDM baseline ($A=1$)', zorder=4)

# [N-7] Mark the amplitude at the peak of the adopted spatial template
R_pk   = XI_KZ
A_pk   = A_ecf(np.array([R_pk]), z_ref, ALPHA_CEN)[0]
ax1.annotate('',
    xy=(R_pk, A_pk), xytext=(R_pk, 1.0),
    arrowprops=dict(arrowstyle='<->', color='#AA3300', lw=2.0))
ax1.text(R_pk + 2, (1.0 + A_pk)/2,
         fr'$1+\alpha_{{\rm KZ}}\simeq{A_pk:.1f}$ at peak (adopted)',
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
ax1.set_ylabel(r'$A_{\rm ECF}(R) = n_{\rm ECF} / n_{\Lambda{\rm CDM}}$',
               fontsize=11)
ax1.set_title('(b) ECF amplification ratio\n'
              r'$\mathcal{A}_{\rm ECF}(R)$',
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

# [N-10, option (a), 22/09/2026] The factor (1+z)^{-3 w_a} is withdrawn:
# A_ECF no longer depends on z. A single curve is drawn; the redshift
# dependence of the VSF excess remains to be derived (PO-F3-XI).
ax2.plot(R_arr, A_ecf(R_arr, 0.0, ALPHA_CEN), color='#CC0000', lw=2.2, ls='-',
         label=r'$\alpha_{\rm KZ}=1.1$ (any $z$: no evolution claimed)')

ax2.axhline(1.0, color=C_LCDM, lw=1.8, ls='-', alpha=0.5,
            label=r'$\Lambda$CDM')
ax2.axvline(XI_KZ, color='#AA5500', lw=1.5, ls='--', alpha=0.6, zorder=6)
ax2.text(XI_KZ + 1.5, 3.0,
         r'$\xi_{\rm KZ}$', fontsize=9, color='#AA5500')

ax2.set_xlabel(r'Void radius $R$  [Mpc]', fontsize=12)
ax2.set_ylabel(r'$A_{\rm ECF}(R)$  [ECF/ΛCDM ratio]', fontsize=11)
ax2.set_title('(c) No redshift evolution claimed\n'
              r'($\alpha_{\rm KZ}=1.1$; PO-F3-XI)',
              fontsize=13, fontweight='bold')
ax2.set_xlim(10, 200)
ax2.set_ylim(0.5, 3.8)
ax2.legend(loc='upper right', fontsize=10,
           framealpha=0.90, facecolor='#F4F6FF', edgecolor='#334488')
ax2.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax2.spines.values():
    sp.set_color('#AABBDD')

# Note [N-10]: no z-evolution claimed
ax2.text(0.04, 0.06,
    r'$z$-dependence of $A_{\rm ECF}$ not derived' '\n'
    r'(factor $(1+z)^{-3w_a}$ withdrawn; PO-F3-XI)',
    transform=ax2.transAxes, fontsize=8.5, color='#444444',
    bbox=dict(boxstyle='round,pad=0.35', fc='#F0F4FF',
              ec='#334488', alpha=0.88))

# ── Suptitle ───────────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure M2 — ECF Void Size Function: Quantitative Prediction vs ΛCDM\n'
    r'$\xi_{\rm KZ}=60$ Mpc (adopted value, not derived; PO-F3-XI)   |   '
    r'$\alpha_{\rm KZ}$ adopted (calibration not documented)   |   '
    'Falsification test: Euclid DR1-Complete (mid-2027)',
    fontsize=11, fontweight='bold', color='#111111', y=1.02)

# ── Euclid Q2 flag box ─────────────────────────────────────────────────────────
fig.text(0.50, -0.01,
    'Euclid DR1-Complete (mid-2027) kill-switch:'
    '  a null result (no excess at $2\\sigma$, $R>60$ Mpc)'
    '  $\\Rightarrow$  would disfavour the ECF Chiral Wall template',
    fontsize=10, color='#CC2222', ha='center',
    bbox=dict(boxstyle='round,pad=0.5', fc='#FFF0F0',
              ec='#CC2222', alpha=0.95, lw=1.2))

out = os.path.join(FIGS, 'Fig_VSF_ECF_Prediction.png')
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {out}')
