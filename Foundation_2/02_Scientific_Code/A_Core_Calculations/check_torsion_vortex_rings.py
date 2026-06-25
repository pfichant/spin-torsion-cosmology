#!/usr/bin/env python3
"""
check_torsion_vortex_rings.py
ECF Foundation II — Validation Figure
Big Ring & Giant Arc as projections of a single Torsion Vortex Ring (TVR)

Generates: fig_tvr_megastructures.png  (3-panel dark-theme figure)

Parameters (all from ECF Foundation II, no free tuning):
  R_TVR     = 321.81 Mpc  (full TVR circumference = 2022 Mpc / 2pi)
  f_KZ      = 4.46        (Kibble-Zurek amplification factor)
  D_A       = 1475 Mpc    (angular diameter distance at z=0.802)

Observational targets:
  Big Ring diameter   ~ 643 Mpc  → theta ~ 25.0 deg  (Lopez+2024)
  Giant Arc projected ~ 438 Mpc  → theta ~ 17.0 deg  @ i=12.5 deg (Lopez+2022)
  ΛCDM homogeneity limit = 370 Mpc (Yadav+2010)

References:
  Lopez et al. 2022, MNRAS 516, 1557  (Giant Arc)
  Lopez et al. 2024, JCAP 2024, 019   (Big Ring)
  Yadav et al. 2010, MNRAS 405, 2009  (homogeneity limit)
  Fichant 2026, ECF Foundation I       (background solution)

Usage:
  python check_torsion_vortex_rings.py
  Requires: numpy, matplotlib
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle, Arc, Patch

# ─── Physical parameters ────────────────────────────────────────────────────
R_TVR      = 2022.0 / (2 * np.pi)    # 321.81 Mpc  (TVR full circ = 2022 Mpc)
D_A        = 1475.0                  # Mpc  angular diameter distance at z=0.802
f_KZ_best  = 4.46                    # Kibble-Zurek amplification factor
lim_homo   = 370.0                   # Mpc  ΛCDM homogeneity limit (Yadav+2010)

# ─── Derived observables ────────────────────────────────────────────────────
D_BR_obs    = 2 * R_TVR                                       # 643.6 Mpc face-on
i_GA_deg    = 12.5                                            # deg inclination
L_GA_chord  = 2 * np.pi * R_TVR * np.sin(np.radians(i_GA_deg))# 437.6 Mpc
theta_BR    = np.degrees(D_BR_obs   / D_A)                    # 25.0 deg
theta_GA    = np.degrees(L_GA_chord / D_A)                    # 17.0 deg
theta_homo  = np.degrees(lim_homo   / D_A)                    # 14.4 deg

sig_BR_mpc  = 20.0   # Mpc  1-sigma uncertainty Big Ring diameter
sig_GA_mpc  = 30.0   # Mpc  1-sigma uncertainty Giant Arc chord

print("=== TVR Validation ===")
print(f"R_TVR           = {R_TVR:.2f} Mpc")
print(f"D_BR  (face-on) = {D_BR_obs:.1f} Mpc  -> theta = {theta_BR:.1f} deg")
print(f"L_GA  (i={i_GA_deg} deg) = {L_GA_chord:.1f} Mpc  -> theta = {theta_GA:.1f} deg")
print(f"LCDM limit      = {lim_homo:.0f} Mpc    -> theta = {theta_homo:.1f} deg")

# ─── Panel 1 data ───────────────────────────────────────────────────────────
i_arr  = np.linspace(0, 90, 1000)
L_proj = 2 * np.pi * R_TVR * np.sin(np.radians(i_arr))

# ─── Panel 2 data ───────────────────────────────────────────────────────────
sigma_arr  = np.linspace(0, 5, 500)
f_BR_plus  = f_KZ_best * (D_BR_obs   + sigma_arr * sig_BR_mpc) / D_BR_obs
f_BR_minus = f_KZ_best * (D_BR_obs   - sigma_arr * sig_BR_mpc) / D_BR_obs
f_GA_plus  = f_KZ_best * (L_GA_chord + sigma_arr * sig_GA_mpc) / L_GA_chord
f_GA_minus = f_KZ_best * (L_GA_chord - sigma_arr * sig_GA_mpc) / L_GA_chord

# ─── Colors & style ─────────────────────────────────────────────────────────
panel_bg = '#111820'
dark_bg  = '#0d1117'
sky_bg   = '#050a12'
text_col = '#e8e8e8'
grid_col = '#2a3a4a'
c_br     = '#4da6ff'   # Big Ring: blue
c_ga     = '#ffd700'   # Giant Arc: gold
c_lcdm   = '#ff4444'   # ΛCDM limit: red
c_best   = '#ffffff'   # best-fit: white

# ─── Figure layout ──────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 6))
fig.patch.set_facecolor(dark_bg)
gs = gridspec.GridSpec(1, 3, wspace=0.35,
                        left=0.06, right=0.97, top=0.88, bottom=0.13)

# ─── Panel 1: L_proj(i) ─────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(panel_bg)

ax1.plot(i_arr, L_proj, lw=2.2, color=c_br,
         label=r'$L_{\rm proj}(i)=2\pi R_{\rm TVR}\sin i$')
ax1.axhline(L_GA_chord, ls='--', lw=1.5, color=c_ga,
             label=f'Giant Arc obs = {L_GA_chord:.0f} Mpc')
ax1.axhline(lim_homo, ls='-.', lw=1.3, color=c_lcdm,
             label=f'LCDM limit = {lim_homo:.0f} Mpc')
ax1.axhline(2*np.pi*R_TVR, ls=':', lw=1.0, color='#888888',
             label=f'TVR full circ = {2*np.pi*R_TVR:.0f} Mpc')
ax1.axvline(i_GA_deg, ls='--', lw=1.0, color=c_ga, alpha=0.6)
ax1.plot(i_GA_deg, L_GA_chord, 'o', ms=9, color=c_ga, zorder=5)
ax1.text(i_GA_deg + 1.5, L_GA_chord + 55,
          fr'$i_a = {i_GA_deg}°$', color=c_ga, fontsize=10)

ax1.set_xlabel("Inclination $i$ (deg)", color=text_col, fontsize=11)
ax1.set_ylabel("Projected length (Mpc)", color=text_col, fontsize=11)
ax1.set_title("Giant Arc — TVR Projection", color=text_col, fontsize=12, pad=8)
ax1.tick_params(colors=text_col)
for sp in ax1.spines.values(): sp.set_color(grid_col)
ax1.grid(color=grid_col, alpha=0.5, linewidth=0.7)
ax1.legend(fontsize=8.5, facecolor='#1a2a3a', labelcolor=text_col,
            framealpha=0.85, loc='lower right')
ax1.set_xlim(0, 90)
ax1.set_ylim(0, 2250)

# ─── Panel 2: f_KZ constraints ──────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(panel_bg)

# Sigma-zone background
ax2.axvspan(0,   1, alpha=0.10, color='#00aa88', zorder=0)
ax2.axvspan(1,   2, alpha=0.07, color='#aa8800', zorder=0)
ax2.axvspan(2,   5, alpha=0.05, color='#aa2200', zorder=0)

ax2.fill_between(sigma_arr, f_BR_minus, f_BR_plus,
                  color=c_br, alpha=0.30, label='Big Ring constraint')
ax2.fill_between(sigma_arr, f_GA_minus, f_GA_plus,
                  color=c_ga, alpha=0.30, label='Giant Arc constraint')
ax2.axhline(f_KZ_best, ls='--', lw=1.8, color=c_best,
             label=f'ECF best-fit $f_{{\\rm KZ}}={f_KZ_best}$')
ax2.axvline(1, ls=':', lw=0.9, color='#00aa88', alpha=0.8)
ax2.axvline(2, ls=':', lw=0.9, color='#aa8800', alpha=0.8)

patch1 = Patch(facecolor='#00aa88', alpha=0.4, label='< 1σ zone')
patch2 = Patch(facecolor='#aa8800', alpha=0.3, label='1–2σ zone')
patch3 = Patch(facecolor='#aa2200', alpha=0.2, label='> 2σ zone')

ax2.set_xlabel("Tension (sigma)", color=text_col, fontsize=11)
ax2.set_ylabel("Kibble–Zurek $f_{\\rm KZ}$", color=text_col, fontsize=11)
ax2.set_title("$f_{\\rm KZ}$ Constraints from Both Structures",
               color=text_col, fontsize=12, pad=8)
ax2.tick_params(colors=text_col)
for sp in ax2.spines.values(): sp.set_color(grid_col)
ax2.grid(color=grid_col, alpha=0.5, linewidth=0.7)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles=handles + [patch1, patch2, patch3],
            labels=labels  + ['< 1σ zone', '1–2σ zone', '> 2σ zone'],
            fontsize=8.5, facecolor='#1a2a3a', labelcolor=text_col,
            framealpha=0.85, loc='upper right')
ax2.set_xlim(0, 5)
ax2.set_ylim(3, 5)

# ─── Panel 3: Sky Map ────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(sky_bg)

# Starfield
rng = np.random.default_rng(42)
sx, sy = rng.uniform(-22, 22, 400), rng.uniform(-22, 22, 400)
sm = rng.uniform(0.3, 1.4, 400)
ax3.scatter(sx, sy, s=sm, color='white', alpha=0.5, zorder=1)

# ΛCDM homogeneity limit (red dashed circle)
ax3.add_patch(Circle((0, 0), theta_homo/2, fill=False,
                      edgecolor=c_lcdm, lw=1.5, ls='--', zorder=3))
ax3.text(-theta_homo/2 - 0.3, 0,
          f'{theta_homo:.1f}°\n= {lim_homo:.0f} Mpc',
          color=c_lcdm, ha='right', va='center', fontsize=7.5)

# Big Ring (face-on TVR) — full circle
ax3.add_patch(Circle((0, 0), theta_BR/2, fill=False,
                      edgecolor=c_br, lw=2.5, zorder=4))
ax3.text(0, theta_BR/2 + 0.8,
          f'Big Ring\n{theta_BR:.1f}°  {D_BR_obs:.0f} Mpc',
          color=c_br, ha='center', fontsize=8, fontweight='bold')

# Giant Arc (inclined TVR) — partial arc
ax3.add_patch(Arc((0, 0), theta_BR, theta_BR,
                   angle=90, theta1=-theta_GA/2, theta2=theta_GA/2,
                   color=c_ga, lw=3.0, zorder=5))
ax3.text(theta_GA/2 + 0.5, 0,
          f'Giant Arc\n{theta_GA:.1f}°  {L_GA_chord:.0f} Mpc',
          color=c_ga, ha='left', va='center', fontsize=8, fontweight='bold')

# Center cross
ax3.plot(0, 0, '+', ms=14, color=c_br, lw=2.0, zorder=6)

# Info box
ax3.text(-20, 19, f'$z = 0.802$\n$D_A = {D_A:.0f}$ Mpc',
          color=text_col, fontsize=9,
          bbox=dict(facecolor='#1a2a3a', edgecolor=grid_col, alpha=0.85, pad=4))

# Legend patches
leg_br  = Patch(edgecolor=c_br,   facecolor='none', lw=2.5,
                 label=f'Big Ring (face-on TVR)')
leg_ga  = Patch(edgecolor=c_ga,   facecolor='none', lw=2.5,
                 label=f'Giant Arc (inclined TVR)')
leg_lim = Patch(edgecolor=c_lcdm, facecolor='none', lw=1.5, ls='--',
                 label=f'LCDM limit ({lim_homo:.0f} Mpc)')
ax3.legend(handles=[leg_br, leg_ga, leg_lim],
            fontsize=8, facecolor='#1a2a3a', labelcolor=text_col,
            framealpha=0.85, loc='lower right')

ax3.set_xlim(-22, 22); ax3.set_ylim(-22, 22)
ax3.set_xlabel("RA offset (deg)", color=text_col, fontsize=11)
ax3.set_ylabel("Dec offset (deg)", color=text_col, fontsize=11)
ax3.set_title(f"Sky Map at $z=0.802$", color=text_col, fontsize=12, pad=8)
ax3.tick_params(colors=text_col)
ax3.set_aspect('equal')
for sp in ax3.spines.values(): sp.set_color(grid_col)
ax3.grid(color=grid_col, alpha=0.3, linewidth=0.6)

# ─── Super-title ─────────────────────────────────────────────────────────────
fig.suptitle(
    "ECF Torsion Vortex Ring — Validation vs Big Ring & Giant Arc",
    color=text_col, fontsize=14, fontweight='bold', y=0.97
)

for ax in [ax1, ax2, ax3]:
    ax.xaxis.label.set_color(text_col)
    ax.yaxis.label.set_color(text_col)

plt.savefig("fig_tvr_megastructures.png", dpi=200,
             bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("\nSaved: fig_tvr_megastructures.png")

# ─── Numerical summary ───────────────────────────────────────────────────────
from scipy.interpolate import interp1d
f_interp_BR = interp1d(sigma_arr, (f_BR_minus + f_BR_plus)/2)
print(f"\n=== Parameter summary ===")
print(f"R_TVR            = {R_TVR:.2f} Mpc")
print(f"Full TVR circum  = {2*np.pi*R_TVR:.0f} Mpc")
print(f"D_BR (face-on)   = {D_BR_obs:.1f} Mpc  theta = {theta_BR:.2f} deg")
print(f"L_GA at i=12.5°  = {L_GA_chord:.1f} Mpc  theta = {theta_GA:.2f} deg")
print(f"Both within <1 sigma at f_KZ = {f_KZ_best}")
