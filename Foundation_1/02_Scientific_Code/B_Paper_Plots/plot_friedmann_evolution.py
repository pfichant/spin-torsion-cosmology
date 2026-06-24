"""
================================================================================
SCRIPT : Cosmic Energy Density Evolution (Friedmann Equations)
Paper  : Foundation I -- Extended Version
Author : Pascal Fichant (2026)
Description :
    Plots the evolution of background energy densities vs scale factor a.
    Planck 2018 amplitudes: Omega_Lambda=0.685, Omega_m=0.315, Omega_r=9e-5.
    Three epoch markers (BBN, Spin-Radiation equality, Matter-Radiation equality).
================================================================================
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 13,
    'axes.labelsize': 15,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})


def plot_friedmann_densities():
    a = np.logspace(-10, 0, 1000)

    # Planck 2018 normalised amplitudes (arbitrary units, correct slopes)
    rho_lambda = 0.685 * np.ones_like(a)
    rho_matter = 0.315 * a**(-3)
    rho_rad    = 9.0e-5 * a**(-4)
    rho_spin   = 9.8e-18 * a**(-6)

    fig, ax = plt.subplots(figsize=(11, 7))
    plt.subplots_adjust(left=0.12, right=0.65, top=0.91, bottom=0.11)

    ax.plot(a, rho_spin,   color='purple', linestyle='-',  linewidth=3,
            label=r'Spin/Torsion  $\rho_{\rm spin} \propto a^{-6}$')
    ax.plot(a, rho_rad,    color='red',    linestyle='--', linewidth=2,
            label=r'Radiation  $\rho_r \propto a^{-4}$')
    ax.plot(a, rho_matter, color='blue',   linestyle='-.', linewidth=2,
            label=r'Matter  $\rho_m \propto a^{-3}$')
    ax.plot(a, rho_lambda, color='green',  linestyle=':',  linewidth=2.5,
            label=r'Dark Energy  $\rho_\Lambda \approx$ const')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-10, 1)
    ax.set_ylim(1e-2, 1e45)
    ax.set_xlabel(r'Scale Factor $a$', fontweight='bold', labelpad=8)
    ax.set_ylabel(r'$\rho_i(a)$ [Arbitrary Units]', fontweight='bold', labelpad=8)
    ax.set_title('Dominance of Torsion in the Early Universe',
                 fontsize=15, fontweight='bold', pad=10)

    ax.grid(True, which='major', ls=':', alpha=0.35)
    ax.grid(True, which='minor', ls=':', alpha=0.12)

    # Epoch markers (analytically derived from Planck 2018 amplitudes)
    a_bbn = 3.0e-9                          # BBN constraint
    a_sr  = (9.8e-18 / 9.0e-5)**0.5        # Spin-Radiation equality ~ 3.3e-7
    a_eq  = 9.0e-5 / 0.315                 # Matter-Radiation equality ~ 2.86e-4

    epochs = [
        (a_bbn, 'darkorange', 'BBN',      5e41),
        (a_sr,  'purple',     'Spin=Rad', 5e28),
        (a_eq,  'dimgray',    'Mat=Rad',  5e6),
    ]
    for a_v, col, lbl, y_lbl in epochs:
        ax.axvline(a_v, color=col, linestyle='--', alpha=0.5, linewidth=1.1)
        ax.text(a_v * 2.5, y_lbl, lbl, color=col, fontsize=10, va='center',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.85, ec='none'))

    # Legend placed outside the plot area (right margin)
    ax.legend(loc='upper left', bbox_to_anchor=(1.03, 1.0),
              framealpha=0.97, edgecolor='black', fontsize=11,
              title='Components', title_fontsize=11)

    filename = 'Figure_Friedmann_Evolution.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")
    print(f"  a_bbn = {a_bbn:.2e}  (BBN)")
    print(f"  a_sr  = {a_sr:.3e}  (Spin-Radiation equality)")
    print(f"  a_eq  = {a_eq:.3e}  (Matter-Radiation equality)")


if __name__ == '__main__':
    plot_friedmann_densities()