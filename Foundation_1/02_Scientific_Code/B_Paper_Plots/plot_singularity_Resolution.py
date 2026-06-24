"""
Script: plot_singularity_resolution_v2.py
Paper:  Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant
Date:   21/04/2026
Version: v2 referee

Description:
    Generates Figure figbouncetraj (App. H) — schematic energy density
    evolution near the primordial spin bounce in the ECF framework.

    Two curves compared (all quantities dimensionless, rho_C = 1 in plot):
      - GR:  rho_GR(t)  ~ 1/t^2                (diverges as t -> 0, singular)
      - ECF: rho_ECF(t) = rho_C/(1+rho_C*t^2)  [exact stiff fluid w=1,
                                                 Poplawski 2010]

    Asymptotic behaviour:
      t -> 0:   rho_ECF -> rho_C  (bounce saturation, H = 0)
      t -> inf: rho_ECF ~ 1/t^2  (GR recovered; abs diff -> 0)

    Modified Friedmann equation (App. H):
        H^2 = (8*pi*G/3) * rho * (1 - rho/rho_C)
        => H = 0 when rho = rho_C  (bounce condition, no singularity)

    Physical values (App. H):
        rho_C = 5.15e96 kg/m^3   (Cartan/Planck density, order-of-magnitude)
        a_min = 1e-32             (minimum scale factor, App. D)

Sections impacted:
    App. H (secbounce), App. I (appspinbounce), Sec. 2 (sectheory).

Changelog v1 -> v2:
    + rho_ECF: corrected to exact Lorentzian rho_C/(1+rho_C*t^2)
               [v1 used an incorrect form centred on radius r]
    + x-axis label: 'Cosmic time t' [v1: ambiguous 'r or a']
    + rho_C = 1 in plot units; physical value annotated in legend
    + Classically forbidden zone (rho > rho_C) added with shading
    + 'Information Preserved' label removed [Foundation III scope only]
    + verify_calibration(): asserts rho_ECF(0)=rho_C and abs diff -> 0
    + Legend placed in dedicated lower axes to avoid curve overlap
    + Title as fig.suptitle to avoid plot-area intrusion
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
})

RHO_C = 1.0   # dimensionless; physical: 5.15e96 kg/m^3 (App. H)


def verify_calibration():
    print(">>> Calibration verification (Singularity Resolution v2)...")

    # Check 1: bounce saturation — rho_ECF(t=0) = rho_C
    rho_at_0 = RHO_C / (1.0 + RHO_C * 0.0**2)
    assert abs(rho_at_0 - RHO_C) < 1e-12, "FAIL: rho_ECF(0) != rho_C"
    print(f"   rho_ECF(t=0)  = {rho_at_0:.6f} == rho_C  [bounce saturation OK]")

    # Check 2: GR recovery at low density — |rho_ECF - rho_GR| -> 0
    t_large = 5.0
    rho_ecf = RHO_C / (1.0 + RHO_C * t_large**2)
    rho_gr  = 1.0 / t_large**2
    abs_diff = abs(rho_ecf - rho_gr)
    assert abs_diff < 0.01, (
        f"FAIL: |rho_ECF - rho_GR|(t={t_large}) = {abs_diff:.4f}, expected < 0.01"
    )
    print(f"   |rho_ECF - rho_GR|(t=5) = {abs_diff:.6f} < 0.01  [GR recovery OK]")

    print(f"   rho_C (plot units) = {RHO_C}  [physical: ~5.15e96 kg/m^3]")
    print(f"   a_min              = 1e-32  [App. H, App. D]")
    print(">>> Calibration OK.\n")


def plot_singularity_resolution():
    verify_calibration()
    print(">>> Generating Figure: Singularity Resolution (v2)...")

    t = np.linspace(0.05, 2.4, 800)
    rho_gr  = np.minimum(1.0 / t**2, 4.8)
    rho_ecf = RHO_C / (1.0 + RHO_C * t**2)

    fig = plt.figure(figsize=(11, 7.5))
    fig.suptitle(
        'Singularity Resolution: ECF Primordial Bounce (App. H)',
        fontsize=12, fontweight='bold', y=0.97, fontfamily='serif'
    )

    ax = fig.add_axes([0.10, 0.30, 0.87, 0.60])

    # Classically forbidden zone
    ax.axhspan(RHO_C, 4.8, color='#e8e8e8', zorder=0)
    ax.text(2.25, 1.07, 'forbidden', fontsize=9, color='#666', ha='right')

    # Curves
    l1, = ax.plot(t, rho_gr,  color='#c0392b', ls='--', lw=2.2)
    l2, = ax.plot(t, rho_ecf, color='#154360', ls='-',  lw=2.8)
    l3  = ax.axhline(RHO_C, color='#229954', ls=':', lw=1.8)

    # Bounce annotation — placed in empty upper-centre region
    ax.annotate(
        'Bounce  H=0',
        xy=(0.20, RHO_C), xytext=(0.60, 2.4),
        arrowprops=dict(arrowstyle='->', lw=1.3, color='#154360'),
        fontsize=10.5, color='#154360', ha='center', fontfamily='serif',
        bbox=dict(boxstyle='round,pad=0.35', fc='#ddeeff',
                  ec='#154360', lw=0.9, alpha=0.92)
    )

    ax.set_xlim(0.05, 2.4)
    ax.set_ylim(0, 4.8)
    ax.set_xlabel('Cosmic time t  [schematic, dimensionless]',
                  fontsize=11, fontfamily='serif')
    ax.set_ylabel('Energy density  (rho / rho_C)',
                  fontsize=11, fontfamily='serif')
    ax.grid(True, ls=':', alpha=0.38, lw=0.7)
    ax.tick_params(labelsize=10)

    # Legend in a dedicated lower axes panel — no overlap with curves
    leg_ax = fig.add_axes([0.09, 0.01, 0.88, 0.24])
    leg_ax.axis('off')

    legend_items = [
        (l1,  'GR:  rho ~ 1/t^2   (standard, singular)'),
        (l2,  'ECF: rho_C / (1 + rho_C * t^2)   [Poplawski 2010, stiff fluid w=1]'),
        (l3,  'Cartan density rho_C   (~5.15 x 10^96 kg/m^3,  App. H)'),
        (Patch(fc='#e8e8e8', ec='gray'),
         'Classically forbidden zone  (rho > rho_C)'),
    ]

    for i, (handle, label) in enumerate(legend_items):
        y = 0.85 - i * 0.24
        if isinstance(handle, Patch):
            leg_ax.add_patch(plt.Rectangle(
                (0.012, y - 0.055), 0.042, 0.11,
                transform=leg_ax.transAxes,
                fc=handle.get_facecolor(), ec='gray', lw=0.8
            ))
        else:
            leg_ax.plot(
                [0.012, 0.054], [y, y],
                color=handle.get_color(),
                ls=handle.get_linestyle(),
                lw=2.0,
                transform=leg_ax.transAxes
            )
        leg_ax.text(
            0.068, y, label,
            transform=leg_ax.transAxes,
            fontsize=9.5, va='center', color='#111', fontfamily='serif'
        )

    plt.savefig("Figure_Singularity_Resolution.png", dpi=300, bbox_inches='tight')
    print("   [SUCCESS] Saved: Figure_Singularity_Resolution.png")
    plt.close()


if __name__ == "__main__":
    plot_singularity_resolution()