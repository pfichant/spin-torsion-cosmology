#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_euclid_pk_S8.py  --  v2  (17 Apr 2026)
============================================
Figure double-panel: Matter Power Spectrum P(k) -- ECF vs LCDM
Foundation I Extended, Sections 4-5  (v2-150426)

Author: Pascal Fichant

Physical derivation
-------------------
Transfer function (BBKS 1986):
    T(k) = [ln(1+2.34q)/(2.34q)] * [1 + 3.89q + (16.1q)^2
            + (5.46q)^3 + (6.71q)^4]^{-1/4}
    q = k / (Omega_m * h^2)   [h/Mpc]
    Omega_m = 0.315,  h = 0.7304  (Planck 2018 / F1 Sec. 5)

    v1 bug: q = k/(Omega_m*h)  ->  k_eq shifted by factor 1/h = 1.49.
    v2 fix: q = k/(Omega_m*h^2) = k/0.168  (correct BBKS normalisation).

ECF torsion suppression (F1 Sec. 4):
    G_eff(k) = G_N [1 - alpha * k^2/k_cut^2]     (ECKS leading-order gradient)
    Regularised Lorentzian, T^2 in [0,1] for all k:
    T_tors^2(k) = 1 - A_sup * k^2 / (k^2 + k_cut^2)
    A_sup = 0.15,  k_cut = 0.10 h/Mpc  (F1 Sec. 4-5)
    T^2(k_cut)    = 0.925
    T^2(k>>k_cut) = 0.850  (15% maximum suppression)

S8 values (F1 Sec. 5):
    S8_LCDM = 0.832 * sqrt(0.315/0.3) = 0.853
    S8_ECF  = 0.766  (Delta_chi^2 = -39.5 vs LCDM)

Euclid simulated forecast:
    15 log-spaced k in [0.032, 2.0] h/Mpc, sigma_rel=3%, seed=42.

Output
------
    Figure_Euclid_Pk_S8.png  (300 dpi)
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ---------------------------------------------------------------------------
# Parameters -- anchored to F1 Extended v2-150426
# ---------------------------------------------------------------------------
H0           = 73.04
h            = H0 / 100.0
Omega_m      = 0.315
ns           = 0.965
sigma8_LCDM  = 0.832
S8_LCDM      = sigma8_LCDM * np.sqrt(Omega_m / 0.3)   # = 0.853

k_cut        = 0.10           # h/Mpc  (F1 Sec. 4)
A_sup        = 0.15           # calibrated on S8_ECF=0.766  (F1 Sec. 5)
S8_ECF       = 0.766

k_disc_lo    = 0.08
k_disc_hi    = 0.30

OUTPUT_FILE  = '/tmp/Figure_Euclid_Pk_S8.png'


# ---------------------------------------------------------------------------
# BBKS transfer function  (Bardeen et al. 1986)
# ---------------------------------------------------------------------------
k    = np.logspace(-2.5, 0.5, 500)
q    = k / (Omega_m * h**2)          # correct: Omega_m*h^2 = 0.168
T_k  = (np.log(1.0 + 2.34*q) / (2.34*q) *
        (1.0 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25))
Pk_LCDM = k**ns * T_k**2 * 1e4       # [h^-3 Mpc^3]


# ---------------------------------------------------------------------------
# ECF torsion suppression
# ---------------------------------------------------------------------------
T_tors_sq = 1.0 - A_sup * k**2 / (k**2 + k_cut**2)
Pk_ECF    = Pk_LCDM * T_tors_sq


# ---------------------------------------------------------------------------
# Simulated Euclid forecast
# ---------------------------------------------------------------------------
k_euclid     = np.logspace(-1.5, 0.3, 15)
Pk_th_euclid = np.interp(k_euclid, k, Pk_ECF)
np.random.seed(42)
sigma_rel    = 0.03
Pk_data      = Pk_th_euclid + np.random.normal(0, sigma_rel * Pk_th_euclid)
yerr         = sigma_rel * np.abs(Pk_data)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 13,
                     'axes.linewidth': 1.4})

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(left=0.14, right=0.96, top=0.92, bottom=0.10, hspace=0.08)
gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

ax1 = fig.add_subplot(gs[0])
ax1.loglog(k, Pk_LCDM, 'b--', lw=2.0,
           label=r'$\Lambda$CDM ($S_8=0.853$, $\sigma_8=0.832$)')
ax1.loglog(k, Pk_ECF,  'r-',  lw=2.8,
           label=r'ECF torsion ($S_8=0.766$, F1 Sec. 5)')
ax1.errorbar(k_euclid, Pk_data, yerr=yerr,
             fmt='o', color='k', ecolor='gray', elinewidth=1.5, capsize=3, ms=5,
             label=r'Euclid forecast (simulated, $\sigma_{\rm rel}=3\%$)')
ax1.axvspan(k_disc_lo, k_disc_hi, color='green', alpha=0.08,
            label=r'Discrimination window ($0.08$--$0.30\,h\,{\rm Mpc}^{-1}$)')
ax1.text(0.095, 600,
         r'Torsion suppression ($A_{\rm sup}=0.15$, $k_{\rm cut}=0.10\,h\,{\rm Mpc}^{-1}$)',
         color='#c0392b', fontsize=9.5, fontstyle='italic')
ax1.set_ylabel(r'$P(k)$  [$h^{-3}\,{\rm Mpc}^3$]', fontsize=13)
ax1.set_xlim(0.005, 2.0)
ax1.set_ylim(10, 3e4)
ax1.grid(True, which='both', ls=':', alpha=0.35)
ax1.legend(loc='lower left', fontsize=9.5, framealpha=0.92, edgecolor='#ccc')
ax1.set_xticklabels([])
ax1.set_title(r'Matter Power Spectrum: ECF torsion vs $\Lambda$CDM -- Euclid forecast',
              fontsize=12.5, fontweight='bold', pad=9)

ax2 = fig.add_subplot(gs[1])
ratio_th   = Pk_ECF / Pk_LCDM
ratio_data = Pk_data / np.interp(k_euclid, k, Pk_LCDM)
ratio_err  = yerr    / np.interp(k_euclid, k, Pk_LCDM)
ax2.semilogx(k, ratio_th, 'r-', lw=2.0)
ax2.axhline(1.0, color='b', ls='--', lw=1.5)
ax2.errorbar(k_euclid, ratio_data, yerr=ratio_err,
             fmt='o', color='k', ecolor='gray', elinewidth=1.5, capsize=3, ms=4)
ax2.axvspan(k_disc_lo, k_disc_hi, color='green', alpha=0.10)
ax2.text(0.105, 0.793, 'Discrimination window', color='darkgreen', fontsize=9.0)
ax2.axhline(1.0 - A_sup, color='#c0392b', ls=':', lw=1.2, alpha=0.7)
ax2.text(1.25, 0.855, r'$T^2_{\rm min}=0.85$', color='#c0392b', fontsize=9)
ax2.set_xlabel(r'Wavenumber $k$  [$h\,{\rm Mpc}^{-1}$]', fontsize=13)
ax2.set_ylabel(r'$P_{\rm ECF}/P_{\Lambda}$', fontsize=12)
ax2.set_xlim(0.005, 2.0)
ax2.set_ylim(0.75, 1.08)
ax2.grid(True, which='both', ls=':', alpha=0.35)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()
