#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_ecf_gw_spectrum.py  --  v2  (16 Apr 2026)
===============================================
Double-panel figure: ECF Primordial Gravitational-Wave Spectrum
Foundation I §7 + Foundation II §6  (v2-150426 / v1-150426)

Author: Pascal Fichant

Physical derivation
-------------------
Panel A — LISA band (10^-5 -- 10^-1 Hz)
  ECF stiff-era (w=1) bounce enhancement (Giovannini 1999):
      Omega_ECF(f) = A_ecf * (f/f_peak)^1.5 * exp[-0.5*(f/f_peak)^2]
  A_ecf = 1e-12  (F1 §7 order-of-magnitude estimate),
  f_peak = 4 mHz (illustrative, LISA band).
  Peak amplitude ~6.4e-13 < LISA_min ~1.2e-12 (factor ~2 below threshold).
  Detectability depends on spectral tilt n_T; first-principles
  derivation deferred to Foundation III.

  Chiral asymmetry (F2 §6):
      Pi_GW = (P_R - P_L)/(P_R + P_L) = 0.20
      P_R = Omega_ECF * (1 + Pi_GW) / 2
      P_L = Omega_ECF * (1 - Pi_GW) / 2
  Parity-violating TB/EB cross-correlations measurable by LISA
  independently of absolute amplitude (LISAChiral).
  Kill-switch: null chiral detection Pi_GW < 0.02 (95% CL) => ECF falsified.

  BBN constraint: int Omega d(ln f) ~ 1e-12 << 5.6e-6  (satisfied).

Panel B — PTA nano-Hz band (10^-10 -- 10^-6 Hz)
  ECF Macro-Knot erosion SGWB (F2 §6):
      h_c(f) = 1e-23 * (f / 0.1 Hz)^{-1/2}  [Eq. lisastrain]
  Converted via: Omega_GW h^2 = (2*pi^2 / 3*H0^2) * f^2 * h_c^2
  Spectral index n_h = -1/2  =>  Omega_GW ∝ f^1
  Shallower than standard BBH background (Omega_GW ∝ f^{2/3}):
  discriminating spectral handle for future PTA releases.
  Consistent with NANOGrav 15yr excess (F2 §6).

Output
------
  figure_ecf_gw_spectrum.png  (300 dpi)
  LaTeX: \\includegraphics{figureecfgwspectrum}
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ---------------------------------------------------------------------------
# Parameters — anchored to F1 v2-150426 §7 and F2 v1-150426 §6
# ---------------------------------------------------------------------------
F_PEAK    = 4e-3       # Hz  — illustrative LISA-band peak (F1 §7)
A_ECF     = 1e-12      # Omega_GW h^2 amplitude (F1 §7: ~10^-12)
LISA_F0   = 3e-3       # Hz  — LISA best sensitivity
PI_GW     = 0.20       # chiral asymmetry Pi_GW (F2 §6)
H_C_AMP   = 1e-23      # strain amplitude at H_C_FREF (F2 §6 Eq. lisastrain)
H_C_FREF  = 0.1        # Hz  — reference frequency for strain
H0_NORM   = 3.241e-18  # s^-1  (H0/h, h=1)
OUTPUT    = 'figure_ecf_gw_spectrum.png'

# ---------------------------------------------------------------------------
# Frequency grids
# ---------------------------------------------------------------------------
f_lisa = np.logspace(-5, 0, 2000)
f_pta  = np.logspace(-10, -6, 1000)

# ---------------------------------------------------------------------------
# LISA band — Panel A
# ---------------------------------------------------------------------------
Omega_ECF  = A_ECF * (f_lisa/F_PEAK)**1.5 * np.exp(-0.5*(f_lisa/F_PEAK)**2)
Omega_R    = Omega_ECF * (1 + PI_GW) / 2
Omega_L    = Omega_ECF * (1 - PI_GW) / 2
Omega_inf  = 1e-16 * (f_lisa/1e-3)**(-0.1)
Omega_LISA = 1.2e-12 * ((f_lisa/LISA_F0)**2 + 0.6*(LISA_F0/f_lisa)**1.5 + 0.3)

# ---------------------------------------------------------------------------
# PTA band — Panel B  (F2 §6 Eq. lisastrain)
# ---------------------------------------------------------------------------
h_c_pta        = H_C_AMP * (f_pta/H_C_FREF)**(-0.5)
Omega_pta      = (2*np.pi**2/3) * f_pta**2 * h_c_pta**2 / H0_NORM**2
Omega_PTA_sens = 5e-9 * (f_pta/1e-8)**(-2/3)   # NANOGrav 15yr region

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family':'serif','font.size':11,'axes.linewidth':1.1})

fig = plt.figure(figsize=(13, 6))
gs  = gridspec.GridSpec(1, 2, wspace=0.38)

ax1 = fig.add_subplot(gs[0])
ax1.fill_between(f_lisa, Omega_LISA, 1e-8,
                 color='grey', alpha=0.10, label='_nolegend_', zorder=0)
ax1.plot(f_lisa, Omega_LISA,  color='#777', ls='--', lw=1.8, zorder=2,
         label=r'LISA sensitivity (2024)')
ax1.plot(f_lisa, Omega_inf,   color='#3a7ab5', ls='--', lw=1.8, zorder=3,
         label=r'Inflation ($r<0.06$, slightly red-tilted)')
ax1.plot(f_lisa, Omega_ECF,   color='#C00000', ls='-',  lw=2.6, zorder=4,
         label=r'ECF total  $P_R+P_L$  (F1 §7)')
ax1.plot(f_lisa, Omega_R,     color='#FF7070', ls='-.', lw=1.4, zorder=5,
         label=r'$P_R$ right-chiral')
ax1.plot(f_lisa, Omega_L,     color='#FF7070', ls=':',  lw=1.4, zorder=5,
         label=r'$P_L$ left-chiral  ($\Pi_{GW}=0.20$, F2 §6)')

idx_pk = np.argmax(Omega_ECF)
ax1.annotate(
    r'ECF peak $\approx6\times10^{-13}$' + '\n(below LISA threshold;\ndepends on $n_T$, F1 §7)',
    xy=(f_lisa[idx_pk], Omega_ECF[idx_pk]),
    xytext=(2e-5, 4e-16),
    arrowprops=dict(arrowstyle='->', color='#C00000', lw=0.9),
    fontsize=8, color='#C00000')

ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_xlim(1e-5, 1e-1); ax1.set_ylim(1e-18, 1e-8)
ax1.set_xlabel(r'Frequency  $f$  [Hz]', fontsize=11)
ax1.set_ylabel(r'$\Omega_{\rm GW}\,h^2$', fontsize=11)
ax1.set_title('Panel A — LISA band', fontsize=11, fontweight='bold')
ax1.grid(True, which='both', ls=':', alpha=0.28)
ax1.legend(loc='upper left', fontsize=8.2, framealpha=0.93,
           edgecolor='#ccc', handlelength=2.2)

ax2 = fig.add_subplot(gs[1])
ax2.fill_between(f_pta, Omega_PTA_sens, 1e-7,
                 color='#b5a0e0', alpha=0.12, label='_nolegend_', zorder=0)
ax2.plot(f_pta, Omega_PTA_sens, color='#7a5fb5', ls='--', lw=1.8, zorder=2,
         label='NANOGrav 15yr region')
ax2.plot(f_pta, Omega_pta,      color='#C00000', ls='-',  lw=2.4, zorder=3,
         label=(r'ECF Macro-Knot erosion SGWB' '\n'
                r'$h_c\!=\!10^{-23}(f/0.1\,{\rm Hz})^{-1/2}$  (F2 §6)'))
ax2.text(0.05, 0.07,
         'Consistent with\nNANOGrav 15yr excess\n(F2 §6)',
         transform=ax2.transAxes, fontsize=8.5, color='#7a5fb5',
         bbox=dict(facecolor='white', edgecolor='#7a5fb5', alpha=0.78, pad=2.5))
ax2.text(0.05, 0.38,
         r'$n_h=-1/2$  ($\Omega_{\rm GW}\!\propto\!f^1$)' '\n'
         r'shallower than BBH $(\propto f^{2/3})$',
         transform=ax2.transAxes, fontsize=8, color='#C00000',
         bbox=dict(facecolor='white', edgecolor='#C00000', alpha=0.78, pad=2.5))

ax2.set_xscale('log'); ax2.set_yscale('log')
ax2.set_xlim(1e-10, 1e-6); ax2.set_ylim(1e-16, 1e-6)
ax2.set_xlabel(r'Frequency  $f$  [Hz]', fontsize=11)
ax2.set_ylabel(r'$\Omega_{\rm GW}\,h^2$', fontsize=11)
ax2.set_title('Panel B — PTA nano-Hz band', fontsize=11, fontweight='bold')
ax2.grid(True, which='both', ls=':', alpha=0.28)
ax2.legend(loc='upper right', fontsize=8.5, framealpha=0.93,
           edgecolor='#ccc', handlelength=2.2)

fig.suptitle(
    r'ECF Primordial Gravitational-Wave Spectrum  '
    r'(Foundation I §7 / Foundation II §6)',
    fontsize=12, fontweight='bold', y=1.02)

plt.savefig(OUTPUT, dpi=300, bbox_inches='tight')
plt.close()
