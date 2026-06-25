#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_askap_topological_erosion.py
Foundation II – The Chiral Universe
Author: Pascal Fichant
Date: May 2026

PURPOSE
-------
Generates Fig_ASKAP_Topological_Erosion.png

Illustrative ECF light curve for a Long-Period Transient (Sec. sec:lpterosion).
Models periodic radio bursts from the gradual topological erosion of a captured
Micro-Knot (M ~ 1e24 kg) orbiting a white dwarf or neutron star.

PHYSICAL MODEL  (Eq. in Sec. sec:lpterosion, Foundation II)
-------------------------------------------------------------
  F_ECF(t) = F0 * exp(-t / tau_er) * sum_{k=0}^{N_max} G(t - k*P, sigma)

where G(t, sigma) = exp(-t^2 / (2*sigma^2))  is a Gaussian pulse.

The abrupt termination at t = N_max * P models the exhaustion of the
quantized topological charge after N_max orbital passages.

PARAMETERS  (ASKAP J142431.2-612611, Pritchard 2026)
------------------------------------------------------
  P        = 36 min   Keplerian orbital period
  tau_er   = 8 days   topological erosion timescale
  N_max    = 320      8 days / 36 min  (orbital passages until charge exhausted)
  sigma    = 0.5 min  Gaussian pulse half-width (FWHM ~ 1.2 min << P)
  F0       = 1.0      normalised peak flux

OUTPUT
------
  Fig_ASKAP_Topological_Erosion.png   (300 dpi, dark-theme, 2-panel)

USAGE
-----
  python plot_askap_topological_erosion.py

DEPENDENCIES
------------
  numpy, matplotlib (standard)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
P_min    = 36.0          # orbital period [minutes]
tau_days = 8.0           # erosion timescale [days]
N_max    = 320           # total orbital passages before charge exhaustion
sigma    = 0.5           # Gaussian pulse half-width [minutes]
F0       = 1.0           # normalised peak flux

# Unit conversions
P_days   = P_min / 1440.0
sigma_d  = sigma / 1440.0

# ─────────────────────────────────────────────────────────────────────────────
# PANEL A DATA – pulse peaks (one per passage)
# ─────────────────────────────────────────────────────────────────────────────
k_arr   = np.arange(N_max + 1)
t_peaks = k_arr * P_days
amp_arr = F0 * np.exp(-t_peaks / tau_days)

# Exponential envelope
t_env    = np.linspace(0, tau_days, 1000)
envelope = F0 * np.exp(-t_env / tau_days)

# ─────────────────────────────────────────────────────────────────────────────
# PANEL B DATA – resolved Gaussians over first 6 hours
# ─────────────────────────────────────────────────────────────────────────────
t_zoom    = np.linspace(0, 6 / 24, 4000)   # 6 h in days
flux_zoom = np.zeros_like(t_zoom)
for k in range(int(6 * 60 / P_min) + 2):
    t_k = k * P_days
    amp = F0 * np.exp(-t_k / tau_days)
    flux_zoom += amp * np.exp(-0.5 * ((t_zoom - t_k) / sigma_d) ** 2)

# ─────────────────────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────────────────────
darkbg  = '#0d1117'
panelbg = '#111820'
gridcol = '#2a3a4a'
textcol = '#e8e8e8'
red_ecf = '#e05252'
gold    = '#ffd700'
white   = '#ffffff'
ltblue  = '#7ecff7'

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE
# ─────────────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5),
                                gridspec_kw={'width_ratios': [3, 1.2]})
fig.patch.set_facecolor(darkbg)

for ax in (ax1, ax2):
    ax.set_facecolor(panelbg)
    ax.tick_params(colors=textcol, labelsize=10)
    for sp in ax.spines.values():
        sp.set_color(gridcol)
    ax.grid(color=gridcol, alpha=0.45, linewidth=0.6)

# ── Panel A ───────────────────────────────────────────────────────────────────
ax1.vlines(t_peaks * 24, 0, amp_arr, color=red_ecf, lw=0.9, alpha=0.75,
           label=r'ECF pulse train  $F_\mathrm{ECF}(t)$')
ax1.plot(t_env * 24, envelope, color=gold, lw=2.2, ls='--', alpha=0.9,
         label=r'Erosion envelope  $F_0\,e^{-t/\tau_\mathrm{er}}$')
ax1.axvline(tau_days * 24, color=white, lw=1.4, ls=':', alpha=0.7,
            label=rf'Charge exhaustion  ($N_\mathrm{{max}}={N_max}$)')
ax1.axvspan(0, 6, color=ltblue, alpha=0.08, label='Zoom window (Panel B)')

ax1.annotate('Abrupt cutoff\n(topological charge\nexhausted)',
             xy=(tau_days * 24 - 0.3, 0.12),
             xytext=(tau_days * 24 - 22, 0.28),
             color=white, fontsize=9.5, fontweight='bold', ha='center',
             arrowprops=dict(arrowstyle='->', color=white, lw=1.2))

info = (fr'$P = {P_min:.0f}$ min $\;\;$ $\tau_{{\mathrm{{er}}}} = {tau_days:.0f}$ days'
        fr'$\;\;$ $N_{{\mathrm{{max}}}} = {N_max}$ passages')
ax1.text(0.02, 0.97, info, transform=ax1.transAxes, fontsize=10.5,
         color=textcol, va='top',
         bbox=dict(facecolor=panelbg, edgecolor=gridcol, alpha=0.9, pad=5))

ax1.set_xlim(-1, (tau_days + P_days) * 24)
ax1.set_ylim(-0.04, 1.14)
ax1.set_xlabel('Time [hours]', color=textcol, fontsize=12, fontweight='bold')
ax1.set_ylabel(r'Normalised Flux $F / F_0$', color=textcol, fontsize=12, fontweight='bold')
ax1.set_title('Full 8-day Light Curve  (320 pulses)', color=textcol, fontsize=12, pad=8)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(24))
ax1.xaxis.set_minor_locator(ticker.MultipleLocator(6))
ax1.tick_params(which='minor', colors=gridcol, length=3)
ax1.legend(loc='upper right', fontsize=9.5, facecolor='#1a2a3a',
           labelcolor=textcol, framealpha=0.9, edgecolor=gridcol)

# ── Panel B ───────────────────────────────────────────────────────────────────
ax2.plot(t_zoom * 24 * 60, flux_zoom, color=red_ecf, lw=1.5, alpha=0.9)
k6 = int(6 * 60 / P_min)
for k in range(k6 + 1):
    t_k_min = k * P_min
    amp     = F0 * np.exp(-k * P_days / tau_days)
    ax2.plot(t_k_min, amp, 'o', color=gold, ms=5, zorder=5)

ax2.annotate('', xy=(P_min, 0.92), xytext=(0, 0.92),
             arrowprops=dict(arrowstyle='<->', color=gold, lw=1.5))
ax2.text(P_min / 2, 0.96, f'$P = {P_min:.0f}$ min',
         color=gold, ha='center', fontsize=9.5)

ax2.set_xlim(0, 6 * 60)
ax2.set_ylim(-0.04, 1.14)
ax2.set_xlabel('Time [minutes]', color=textcol, fontsize=12, fontweight='bold')
ax2.set_title('Zoom: first 6 hours\n(10 individual pulses)',
              color=textcol, fontsize=12, pad=8)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(60))
ax2.xaxis.set_minor_locator(ticker.MultipleLocator(18))
ax2.tick_params(which='minor', colors=gridcol, length=3)

# ── Super-title ───────────────────────────────────────────────────────────────
fig.suptitle(
    r'ECF Topological Erosion — ASKAP J142431.2$-$612611 template'
    '\n'
    r'Periodic pulses from a captured Micro-Knot ($M \sim 10^{24}$ kg) '
    r'eroded by tidal stress at each periastron passage',
    color=textcol, fontsize=11.5, y=1.01
)

plt.tight_layout()
os.makedirs('output', exist_ok=True)
outfile = 'Fig_ASKAP_Topological_Erosion.png'
plt.savefig(outfile, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f'Saved: {outfile}')
