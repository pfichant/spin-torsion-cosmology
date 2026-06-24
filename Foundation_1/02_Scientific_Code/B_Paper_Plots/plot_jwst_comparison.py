#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script      : plot_jwst_comparison.py  [v2 - referee]
# Paper       : Foundation I: The Metric Universe (Fichant 2026)
# Figure      : fig:jwstcomparison  (Section 6)
# Corrections : JADES-z14-0 z=14.178/M_UV=-20.3 (Carniani+2024);
#               ECF limit = mag_lcdm - 1.5 (B_ECF=1.45, App. E);
#               LaTeX escapes fixed; matplotlib.use('Agg') before pyplot.
# Output      : Figure_JWST_ECF_comparison.png

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

plt.rcParams.update({
    'font.size': 13, 'axes.labelsize': 14, 'legend.fontsize': 11,
    'font.family': 'serif', 'axes.linewidth': 1.5
})

def plot_jwst_comparison():
    z = np.linspace(8, 15, 200)

    mag_lcdm = -22.0 + 0.8 * (z - 8)
    mag_ecf  = mag_lcdm - 1.5          # B_ECF=1.45 -> ~1.5 mag boost (App. E)

    jwst_jades = [
        (10.603, -21.5, 'GN-z11'),
        (13.20,  -19.8, 'JADES-z13'),
        (14.178, -20.3, 'JADES-z14-0'),  # Carniani+2024
    ]
    jwst_ceers = [(11.4,  -20.3, "Maisie's")]
    jwst_glass = [(12.35, -20.5, 'GLASS-z12')]

    label_pos = {
        'GN-z11':      (9.3,  -22.1),
        "Maisie's":    (9.5,  -20.0),
        'GLASS-z12':   (11.0, -19.5),
        'JADES-z13':   (11.8, -19.2),
        'JADES-z14-0': (13.0, -21.5),
    }

    fig, ax = plt.subplots(figsize=(10, 6.5))
    plt.subplots_adjust(left=0.10, right=0.72, top=0.91, bottom=0.12)

    ax.fill_between(z, mag_ecf, mag_lcdm, color='crimson', alpha=0.12, zorder=1)
    ax.plot(z, mag_lcdm, color='royalblue', linestyle='--', linewidth=2,   zorder=2)
    ax.plot(z, mag_ecf,  color='crimson',   linestyle='-',  linewidth=2.5, zorder=2)

    def annotate_points(dataset, marker, color):
        for (zx, mx, lbl) in dataset:
            ax.plot(zx, mx, marker=marker, color=color, markersize=9, zorder=5,
                    markeredgecolor='white', markeredgewidth=0.5)
            tx, ty = label_pos[lbl]
            ax.annotate(lbl, xy=(zx, mx), xytext=(tx, ty),
                        fontsize=9, fontweight='bold', color=color,
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.0,
                                        connectionstyle='arc3,rad=0.1'),
                        bbox=dict(boxstyle='round,pad=0.15', fc='white',
                                  ec='none', alpha=0.7))

    annotate_points(jwst_jades, 'o', 'black')
    annotate_points(jwst_ceers, 's', 'darkorange')
    annotate_points(jwst_glass, '^', 'teal')

    ax.set_xlabel(r'Redshift $z$', fontweight='bold')
    ax.set_ylabel(r'$M_\mathrm{UV}$ [mag]', fontweight='bold')
    ax.set_title(r'JWST High-$z$ Galaxies vs. ECF Prediction (F1 Sec.6)',
                 fontsize=13, fontweight='bold', pad=10)
    ax.invert_yaxis()
    ax.set_xlim(8.5, 15.0)
    ax.set_ylim(-22.6, -18.8)
    ax.text(14.3, -22.4, r'brighter $\uparrow$', fontsize=9, color='gray', style='italic')
    ax.grid(True, linestyle=':', alpha=0.5)

    legend_elements = [
        Line2D([0],[0], color='royalblue', lw=2, linestyle='--',
               label=r'$\Lambda$CDM limit (hierarchical)'),
        Line2D([0],[0], color='crimson', lw=2.5,
               label=r'ECF limit ($B_\mathrm{ECF}=1.45$, App. E)'),
        Patch(facecolor='crimson', alpha=0.20, label='ECF structural advantage'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='black',
               markersize=8, label='JADES (Carniani+2024, Robertson+2023)'),
        Line2D([0],[0], marker='s', color='w', markerfacecolor='darkorange',
               markersize=8, label='CEERS (Finkelstein+2022)'),
        Line2D([0],[0], marker='^', color='w', markerfacecolor='teal',
               markersize=8, label='GLASS (Naidu+2022)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left',
              bbox_to_anchor=(1.02, 1.0), framealpha=0.96,
              edgecolor='black', fontsize=10)

    plt.savefig('Figure_JWST_ECF_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    plot_jwst_comparison()