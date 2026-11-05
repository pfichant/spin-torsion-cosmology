"""
================================================================================
SCRIPT : Cosmic Energy Density Evolution (Friedmann Equations)
Paper  : Foundation I -- Extended Version
Author : Pascal Fichant (2026)
Description :
    Plots the evolution of background energy densities vs scale factor a.
    Planck 2018 amplitudes: Omega_Lambda=0.685, Omega_m=0.315,
    Omega_r = omega_r/h^2 = 4.1834e-5/0.674^2 = 9.21e-5 (was 9e-5 until 04/10/2026).
    Matter-radiation equality a_eq = Omega_r/Omega_m = 2.92e-4 (z_eq = 3420, LCDM column
    of F1); the ECF background (omega_m = 0.14237) gives 2.94e-4 (z_eq = 3402).
    Three epoch markers (BBN, Spin-Radiation equality, Matter-Radiation equality).
================================================================================
"""
# Last modified: 19/08/2026, 09:37 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


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
    # [04/10/2026, decision T9] omega_r = 4.1834e-5 (canonical), h = 0.674 (Planck column of F1):
    # Omega_r = 9.21e-5 instead of the former 9.0e-5, which put equality at 2.86e-4 (z ~ 3500).
    OMEGA_R    = 4.1834e-5 / 0.674**2
    rho_rad    = OMEGA_R * a**(-4)
    # [16/10/2026, F1-A3] ILLUSTRATIVE spin normalisation, ~3e4 below the calibrated one
    # (Omega_spin/Omega_r = 0.093 at z_ref = 5600, i.e. Omega_spin,0 ~ 2.7e-13, crossing at
    # a ~ 5.4e-5, z ~ 1.8e4; PO-ECF-SPIN-NORM, PO-ECF-BBN-SPIN). Slopes are exact.
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
    # [18/08/2026 audit] a_bbn = 3.0e-9 corresponds to T ~ 78 keV, i.e. the
    # END of nucleosynthesis; its onset (T ~ 1 MeV) is at a = 2.4e-10.
    # Either way BBN falls to the LEFT of the spin-radiation crossing shown
    # here, i.e. in the regime where the spin term dominates. The figure is
    # correct on this point; it was the F1 caption that claimed the opposite
    # ("subdominant by ~1e6 at BBN"), and that claim was withdrawn on
    # 18/08/2026. The marker is kept because the hierarchy it shows is the
    # substance of the figure.
    a_bbn = 3.0e-9                          # BBN (end; T ~ 78 keV)
    a_sr  = (9.8e-18 / OMEGA_R)**0.5       # Spin-Radiation equality ~ 3.3e-7 (illustrative normalisation)
    a_eq  = OMEGA_R / 0.315                # Matter-Radiation equality ~ 2.92e-4 (z_eq ~ 3420)

    epochs = [
        (a_bbn, 'darkorange', 'BBN',      5e41),
        (a_sr,  'purple',     'Spin=Rad', 5e28),
        (a_eq,  'dimgray',    'Mat=Rad',  5e12),
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
    print(f"  a_sr  = {a_sr:.3e}  (Spin-Radiation equality, ILLUSTRATIVE normalisation)")
    print(f"  calibrated normalisation (Omega_spin,0 ~ 2.7e-13): crossing at a ~ 5.4e-5 (z ~ 1.8e4)")
    print(f"  a_eq  = {a_eq:.3e}  (Matter-Radiation equality)")


if __name__ == '__main__':
    plot_friedmann_densities()