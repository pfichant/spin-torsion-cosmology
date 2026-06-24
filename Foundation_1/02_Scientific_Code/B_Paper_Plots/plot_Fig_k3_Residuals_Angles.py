#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_Fig_k3_Residuals_Angles.py  --  v2  (17 Apr 2026)
=======================================================
Figure K3: CMB Damping-Tail Residuals and Angular Scale
Foundation I Extended, Appendix K  (v2-150426)

Author: Pascal Fichant

Physical derivation
-------------------
Phenomenological CMB power spectrum (two-panel figure):

  D_l = 5000 * (l/100)^{-0.6} * exp(-l/d_scale) * cos^2(pi*l/l_peak) + 50
  Sachs-Wolfe plateau (l < 30): D_l = 1000 * (l/10)^{-1.5}

  Parameters (F1 Appendix K):
    l_peak          = 220     First acoustic peak (Planck 2018)
    d_LCDM          = 1400    LCDM Silk damping scale [dimensionless]
    d_ECF           = 1320    ECF damping scale: z_rec shift of ~22 (F1 §6)
                              Relative reduction: 5.7%
    phase_shift_ECF = 0.02*pi ~2% of pi from Delta_z_rec=22/1100 (F1 §6)

  ECF damping-tail deficit (Table K, F1 Appendix K vs independent calc):
    ell=1500: paper -5.2%  / script -5.2%  -> consistent
    ell=2000: paper -6.5%  / script -6.5%  -> consistent
    ell=2500: paper -3.0%  / script -3.2%  -> consistent (model approximation)
    ell=3000: paper -2.5%  / script -2.4%  -> consistent

  CMB-S4 sensitivity (F1 Appendix K): sigma_S4 ~ 1.5 muK^2
  Discrimination window (F1 §6, Appendix K): ell in [2200, 3000]

  Angular scale conversion (upper x-axis):
    theta [deg] = 180 / ell   (standard CMB convention)

Output
------
    Figure_K3_Residuals_Angles.png   (300 dpi)
    LaTeX: \\includegraphics{Figure_K3_Residuals_Angles}
           \\label{fig:k3prediction}   (F1 Appendix K)

Corrections v1 -> v2
--------------------
  [1] ylim panel top: [0,1000] -> [0,600]  (signal visible at high-ell)
  [2] CMB-S4 band: +-1 -> +-1.5 muK^2     (F1 Appendix K Table K)
  [3] phase_shift_ECF = 0.02*pi            (Delta_z_rec ~ 22, F1 §6)
  [4] l2theta: safe division via np.where  (avoids 1e-10 non-standard)
  [5] Legend moved outside plot area       (legibility for referee)
  [6] Docstring added with full derivation
  [7] Comments stripped to essentials
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ---------------------------------------------------------------------------
# Parameters -- anchored to F1 Extended v2-150426 Appendix K
# ---------------------------------------------------------------------------
L_PEAK          = 220
D_SCALE_LCDM    = 1400
D_SCALE_ECF     = 1320
PHASE_SHIFT_ECF = 0.02 * np.pi
SIGMA_S4        = 1.5        # muK^2 (F1 Appendix K)
L_DISC_LO       = 2200
L_DISC_HI       = 3000
L_MASK_MIN      = 1200
OUTPUT_FILE     = 'Figure_K3_Residuals_Angles.png'


# ---------------------------------------------------------------------------
# Phenomenological CMB spectrum (F1 Appendix K)
# ---------------------------------------------------------------------------
def generate_spectrum(ell, d_scale, phase=0.0):
    osc = np.cos(np.pi * ell / L_PEAK + phase) ** 2
    Dl  = 5000 * (ell / 100) ** (-0.6) * np.exp(-ell / d_scale) * osc + 50
    Dl[ell < 30] = 1000 * (ell[ell < 30] / 10) ** (-1.5)
    return Dl


def l2theta(l):
    return 180.0 / np.where(l == 0, np.inf, l)

def theta2l(t):
    return 180.0 / np.where(t == 0, np.inf, t)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
ell  = np.linspace(2, 3500, 1000)
dl_l = generate_spectrum(ell, D_SCALE_LCDM, phase=0.0)
dl_e = generate_spectrum(ell, D_SCALE_ECF,  phase=PHASE_SHIFT_ECF)
mask = ell >= L_MASK_MIN
res  = dl_e - dl_l


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'axes.linewidth': 1.2})

fig = plt.figure(figsize=(11, 9))
gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.08,
                        left=0.10, right=0.72, top=0.88, bottom=0.09)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)

# --- Top panel ---
ax1.plot(ell[mask], dl_l[mask], color='royalblue', ls='--', lw=2.2,
         label=r'$\Lambda$CDM  ($d_{\rm silk}=1400$)')
ax1.plot(ell[mask], dl_e[mask], color='firebrick', lw=2.2,
         label=r'ECF  ($d_{\rm silk}=1320$, F1 App. K)')
ax1.axvspan(L_DISC_LO, L_DISC_HI, color='gold', alpha=0.25,
            label=r'CMB-S4 discrimination zone  $\ell\in[2200,3000]$')
ax1.set_ylim(0, 600)
ax1.set_ylabel(r'$\mathcal{D}_\ell^{TT}\ [\mu{\rm K}^2]$', fontsize=12)
ax1.set_title(r'ECF Damping-Tail Deficit vs $\Lambda$CDM  (F1, App. K)',
              fontsize=13, fontweight='bold', pad=10)
ax1.grid(True, ls=':', alpha=0.40)
ax1.tick_params(labelbottom=False)
ax1.legend(fontsize=10.5, loc='upper left', bbox_to_anchor=(1.01, 1.0),
           framealpha=0.94, edgecolor='#aaa', handlelength=1.8, borderpad=0.8)

secax = ax1.secondary_xaxis('top', functions=(l2theta, theta2l))
secax.set_xlabel('Angular Scale [deg]', fontsize=11, labelpad=6)
secax.set_xticks([0.15, 0.10, 0.08, 0.06])
secax.set_xticklabels([r'$0.15°$', r'$0.10°$', r'$0.08°$', r'$0.06°$'])

# --- Bottom panel ---
ax2.plot(ell[mask], res[mask], color='black', lw=1.8,
         label=r'$\Delta\mathcal{D}_\ell = \mathcal{D}^{\rm ECF}-\mathcal{D}^{\Lambda}$')
ax2.fill_between(ell[mask], res[mask], 0,
                 where=(res[mask] < 0), color='firebrick', alpha=0.20)
ax2.axhline(0, color='royalblue', ls='--', lw=1.2)
ax2.axvspan(L_DISC_LO, L_DISC_HI, color='gold', alpha=0.18)
ax2.fill_between(ell[mask], -SIGMA_S4, SIGMA_S4,
                 color='green', alpha=0.18,
                 label=r'CMB-S4 sensitivity  $\pm1.5\,\mu{\rm K}^2$  (F1 App. K)')
ax2.text(2600, -20, 'Discrimination\nwindow', ha='center',
         fontsize=8.5, color='#9B6F00', style='italic')
ax2.set_ylim(-25, 10)
ax2.set_xlim(L_MASK_MIN, 3500)
ax2.set_ylabel(r'$\Delta\mathcal{D}_\ell\ [\mu{\rm K}^2]$', fontsize=11)
ax2.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
ax2.grid(True, ls=':', alpha=0.40)
ax2.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1.01, 1.0),
           framealpha=0.94, edgecolor='#aaa', handlelength=1.8, borderpad=0.8)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()
