# plot_h0_s8_contours.py  —  v4 referee
# =============================================================================
# SCRIPT  : H0-S8 Tension Resolution (Figure 4)
# Paper   : Foundation I: The Metric Universe (Extended v2)
# Author  : Pascal Fichant (2026)
# Section : Section 4-5, Table tabpriors, cross-checked by script06S8resolution.py
#
# INPUTS (F1 Section 5, Table tabpriors):
#   Planck 2018 LCDM  H0 = 67.4  +/- 0.5   S8 = 0.832 +/- 0.013  [Planck2020]
#   SH0ES 2021        H0 = 73.04 +/- 1.04                          [Riess2021]
#   KiDS-1000                               S8 = 0.766 +/- 0.014  [Heymans2021]
#   ECF best-fit      H0 = 73.04  S8 = 0.766  F_ion=1.2765  Delta_chi2=-39.5
#
# PHYSICAL MECHANISM (Section 3-4):
#   H0 = 67.4 * (147.1/135.8) = 73.01 km/s/Mpc via rs reduction (Section 3)
#   S8 = 0.832*(1 - eps_spin*(F_ion-1)) = 0.760 via G_eff suppression (Section 4)
#   Both effects share F_ion as their unique common parameter.
#
# BUG FIX v1->v2: matplotlib.Ellipse rotates in raw data coords.
#   H0 range ~12 units, S8 range ~0.14 units (ratio ~86x).
#   FIX: parametric filled polygons, rotation on numpy arrays before plotting.
#
# CORRECTIONS v1->v2 (physics):
#   - ECF trajectory curved (cosine H0, power-law t^0.7 for S8), not linear.
#   - KiDS-1000 and SH0ES plotted separately (orthogonal observables).
#   - angle=0 for SH0ES and KiDS (no H0-S8 tilt for these surveys).
#   - Planck tilt=-20 deg retained (H0-S8 anti-correlation r~-0.45).
#   - LaTeX: r'\Lambda', not r'\\Lambda'.
#   - bbox_inches='tight' added.
#
# CORRECTION v2->v3: sx_planck inflated to 1.5 (3x physical) — still a band.
#
# CORRECTION v3->v4 (READABILITY FIX — v4 is the correct version):
#   Display aspect ratio = (H0_range/S8_range)*(fig_h/fig_w)
#                        = (12/0.14)*(7.5/11) = 58.4
#   Physical ratio sx/sy = 0.5/0.013 = 38.5 => vertical band on screen.
#   v3 ratio sx/sy = 1.5/0.013 = 115 => still a band (worse).
#   FIX: sx=1.5 (3x physical), sy=0.025 (2x physical) => sx/sy=60 ~ 58.4
#   => Planck ellipse visually elliptical with tilt -20 deg clearly shown.
#   Caption discloses: sigma_H0_display=1.5, sigma_S8_display=0.025 (illustrative).
# =============================================================================

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 13,
    'font.family': 'serif',
    'axes.linewidth': 1.2,
})


def add_ellipses(ax, cx, cy, sx, sy, angle_deg, color):
    # Parametric filled polygons — immune to axis aspect ratio distortion.
    # cx, cy    : centre (data coordinates)
    # sx, sy    : 1-sigma half-axes (may be inflated for display; see header)
    # angle_deg : tilt in degrees (data coordinates)
    # color     : fill and edge color
    theta = np.radians(angle_deg)
    t = np.linspace(0, 2 * np.pi, 200)
    for nsig, alpha in [(1, 0.32), (2, 0.12)]:
        x_ell = nsig * sx * np.cos(t)
        y_ell = nsig * sy * np.sin(t)
        x_rot = cx + x_ell * np.cos(theta) - y_ell * np.sin(theta)
        y_rot = cy + x_ell * np.sin(theta) + y_ell * np.cos(theta)
        ax.fill(x_rot, y_rot, color=color, alpha=alpha,
                edgecolor=color, linewidth=1.4)


def plot_h0_s8_contours():
    planck_h0, planck_s8 = 67.4,  0.832   # Planck 2018 LCDM [Planck2020]
    ecf_h0,    ecf_s8   = 73.04, 0.766   # ECF best-fit, F1 Section 5

    fig, ax = plt.subplots(figsize=(11, 7.5))
    plt.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.22)

    # Planck 2018 LCDM — tilt -20 deg (H0-S8 anti-correlation r ~ -0.45)
    # sx=1.5 (3x physical 0.5), sy=0.025 (2x physical 0.013)
    # sx/sy = 60 matches display aspect ratio 58.4 => ellipse clearly visible
    add_ellipses(ax, planck_h0, planck_s8, 1.5, 0.025, -20, 'royalblue')

    # SH0ES 2021 — constrains H0 tightly; S8 unconstrained — angle=0
    add_ellipses(ax, 73.04, 0.766, 1.04, 0.014, 0, 'forestgreen')

    # KiDS-1000 — constrains S8 tightly; H0 unconstrained — angle=0
    # H0 centre=70 is illustrative (midpoint of Planck/SH0ES range)
    add_ellipses(ax, 70.0, 0.766, 2.0, 0.014, 0, 'darkorange')

    # ECF trajectory parameterised by F_ion in [1.0, 1.2765]
    # H0: cosine profile — fast non-linear rise driven by rs reduction (Section 3)
    # S8: power-law t^0.7 — slower fall driven by G_eff suppression (Section 4)
    t       = np.linspace(0, 1, 80)
    h0_path = planck_h0 + (ecf_h0 - planck_h0) * (1 - np.cos(np.pi / 2 * t))
    s8_path = planck_s8 + (ecf_s8  - planck_s8) * t ** 0.7
    ax.plot(h0_path, s8_path, color='crimson', linestyle='--',
            linewidth=2.2, zorder=8)

    # ECF best-fit point
    ax.plot(ecf_h0, ecf_s8, marker='*', color='crimson', markersize=20,
            markeredgecolor='darkred', markeredgewidth=0.8, zorder=10)

    # Reference grid lines
    for xv, col in [(planck_h0, 'royalblue'), (ecf_h0, 'crimson')]:
        ax.axvline(xv, color=col, linestyle=':', alpha=0.35, linewidth=1)
    for yv, col in [(planck_s8, 'royalblue'), (ecf_s8, 'crimson')]:
        ax.axhline(yv, color=col, linestyle=':', alpha=0.35, linewidth=1)

    ax.set_xlim(64.5, 76.5)
    ax.set_ylim(0.730, 0.870)
    ax.set_xlabel(r'$H_0$ [km s$^{-1}$ Mpc$^{-1}$]', fontweight='bold')
    ax.set_ylabel(r'$S_8 \equiv \sigma_8\,(\Omega_m/0.3)^{0.5}$', fontweight='bold')
    ax.set_title(
        r'Joint $H_0$--$S_8$ Tension Resolution -- ECF Framework (F1 Sections 4-5)',
        fontsize=14, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.45)

    # Short in-plot disclosure — full values documented in LaTeX caption
    ax.text(0.02, 0.04,
            r'$\dagger$ Planck ellipse inflated for visibility (see caption)',
            transform=ax.transAxes, fontsize=9, color='royalblue',
            style='italic', alpha=0.85)

    legend_elements = [
        Patch(facecolor='royalblue', alpha=0.35, edgecolor='royalblue',
              label=r'Planck 2018 $\Lambda$CDM  ($H_0=67.4$, $S_8=0.832$)$^\dagger$'),
        Patch(facecolor='forestgreen', alpha=0.35, edgecolor='forestgreen',
              label=r'SH0ES 2021  ($H_0=73.04\pm1.04$ km/s/Mpc)'),
        Patch(facecolor='darkorange', alpha=0.35, edgecolor='darkorange',
              label=r'KiDS-1000  ($S_8=0.766\pm0.014$, $H_0$ unconstrained)'),
        Line2D([0], [0], color='crimson', lw=2.2, linestyle='--',
               label=r'ECF path  ($F_{ion}$: $1.0\to1.2765$)'),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='crimson',
               markeredgecolor='darkred', markersize=15,
               label=r'ECF best-fit  ($H_0=73.04$, $S_8=0.766$, $\Delta\chi^2=-39.5$)'),
    ]
    ax.legend(handles=legend_elements,
              loc='upper center', bbox_to_anchor=(0.5, -0.16),
              ncol=2, framealpha=0.95, edgecolor='gray',
              fontsize=10.5, handlelength=2.0, columnspacing=1.2)

    plt.savefig('Figure_H0_S8_Contours.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    plot_h0_s8_contours()