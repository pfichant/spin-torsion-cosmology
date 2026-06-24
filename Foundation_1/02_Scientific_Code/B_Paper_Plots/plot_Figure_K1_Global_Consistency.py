#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_Figure_K1_Global_Consistency.py  --  v2  (17 Apr 2026)
============================================================
Figure K1: Global Geometric Consistency with Planck 2018
Foundation I Extended, Appendix K Section K.1  (v2-150426)

Author: Pascal Fichant

Physical derivation
-------------------
Phenomenological CMB TT power spectrum (single-panel):

  D_l = 5000 * (l/100)^{-0.6} * exp(-l/d_scale) * cos^2(pi*l/l_peak) + 50
  Sachs-Wolfe plateau (l < 30): D_l = 1000 * (l/10)^{-1.5}

  Parameters (F1 Appendix K Table K):
    l_peak          = 220       First acoustic peak (Planck 2018)
    d_LCDM          = 1400      LCDM Silk damping scale [dimensionless]
    d_ECF           = 1320      ECF damping scale; consistent with K3 and Table K
                                (v1 used 1360, which was inconsistent with
                                 the 5.7% reduction required by Table K)
    phase_shift_ECF = 0.02*pi   Delta_z_rec ~ 22  (F1 §6; consistent with K3)
    floor           = 50 muK^2  Planck 2018 noise convention  (v1 used 200)

  Key consistency check (F1 Appendix K §K.1):
    - Peak positions preserved: theta_* = rs/DA conserved at 10^-6 level
      because H0 increase and rs reduction are proportionally compensated.
    - chi2 Planck high-ell: LCDM=2345.2, ECF=2347.0 -> Delta=+1.8 (F1 Table 5)
      Figure K1 illustrates this near-neutrality graphically.

  Simulated Planck-like data (NOT real Planck data):
    30 log-spaced points l in [50, 2500], anchored on LCDM model, seed=42.
    Error model: sigma_rel = 5% * (l/1000)^0.5
    (illustrative: cosmic-variance dominated at low-l, instrumental at high-l)

  Angular scale conversion (secondary x-axis):
    theta [deg] = 180 / ell   (standard CMB convention)

Corrections v1 -> v2
--------------------
  [1] d_ECF: 1360 -> 1320  (Table K; inter-script consistency with K3)
  [2] floor Dl: +200 -> +50  (Planck convention; consistency with K3)
  [3] ylim: [0,6500] -> [0,4500]  (65% empty space eliminated)
  [4] label 'Planck 2018 Data' -> 'Simulated Planck-like data'
  [5] phase_shift_ECF: 0 -> 0.02*pi  (Delta_z_rec=22, F1 §6; consistency K3)
  [6] matplotlib.use('Agg') added before pyplot import
  [7] l2theta: 1e-10 guard -> np.where  (standard safe division)
  [8] Docstring added

Output
------
    Figure_K1_Global_Consistency.png   (300 dpi)
    LaTeX: \\includegraphics{Figure_K1_Global_Consistency}
           \\label{fig:k1global}   (F1 Appendix K §K.1)
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


L_PEAK          = 220
D_SCALE_LCDM    = 1400
D_SCALE_ECF     = 1320
DL_FLOOR        = 50
PHASE_SHIFT_ECF = 0.02 * np.pi
N_DATA          = 30
SEED            = 42
OUTPUT_FILE     = 'Figure_K1_Global_Consistency.png'


def generate_spectrum(ell, d_scale, phase=0.0):
    osc = np.cos(np.pi * ell / L_PEAK + phase) ** 2
    Dl  = 5000 * (ell / 100) ** (-0.6) * np.exp(-ell / d_scale) * osc + DL_FLOOR
    Dl[ell < 30] = 1000 * (ell[ell < 30] / 10) ** (-1.5)
    return Dl


def l2theta(l):
    return 180.0 / np.where(l == 0, np.inf, l)

def theta2l(t):
    return 180.0 / np.where(t == 0, np.inf, t)


ell    = np.linspace(2, 2500, 1000)
dl_l   = generate_spectrum(ell, D_SCALE_LCDM, phase=0.0)
dl_e   = generate_spectrum(ell, D_SCALE_ECF,  phase=PHASE_SHIFT_ECF)

np.random.seed(SEED)
sample_l  = np.geomspace(50, 2500, N_DATA)
sample_dl = np.interp(sample_l, ell, dl_l)
errors    = sample_dl * 0.05 * (sample_l / 1000) ** 0.5


plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'axes.linewidth': 1.2})

fig, ax = plt.subplots(figsize=(11, 7))
fig.subplots_adjust(left=0.09, right=0.62, top=0.88, bottom=0.10)

ax.plot(ell, dl_l, color='royalblue', ls='--', lw=2.2, alpha=0.85,
        label=r'$\Lambda$CDM  ($H_0=67.4$, $d_{\rm silk}=1400$)')
ax.plot(ell, dl_e, color='firebrick', lw=2.2,
        label=r'ECF  ($H_0=73.0$, $d_{\rm silk}=1320$, F1 App. K)')
ax.errorbar(sample_l, sample_dl, yerr=errors,
            fmt='o', color='black', alpha=0.45, ms=3.5, elinewidth=0.9,
            capsize=1.5,
            label=r'Simulated Planck-like data  ($\Delta\chi^2=+1.8$, F1 Table 5)')

ax.set_xlabel(r'Multipole Moment $\ell$', fontsize=13)
ax.set_ylabel(r'$\mathcal{D}_\ell^{TT}$ [$\mu$K$^2$]', fontsize=13)
ax.set_title('Global Geometric Consistency — Planck 2018\n(F1 App. K §K.1)',
             fontsize=12.5, fontweight='bold')
ax.set_xlim(20, 2500)
ax.set_ylim(0, 4500)
ax.grid(True, ls=':', alpha=0.30)
ax.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1.02, 1.0),
          framealpha=0.93, edgecolor='#bbb', handlelength=1.8,
          borderpad=0.9, labelspacing=0.7)

secax = ax.secondary_xaxis('top', functions=(l2theta, theta2l))
secax.set_xticks([180, 360, 900, 1800])
secax.set_xticklabels([r'$1°$', r'$0.5°$', r'$0.2°$', r'$0.1°$'])
secax.set_xlabel('Angular Scale [deg]', fontsize=11, labelpad=4)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()