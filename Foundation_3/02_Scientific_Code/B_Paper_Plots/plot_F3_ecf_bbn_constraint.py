#!/usr/bin/env python3
"""
ecf_bbn_constraint.py
=====================
ECF Foundation III — BBN Constraint on Torsion Density
Author: Pascal Fichant
Date:   June 2026

STATUS (audit v2, arbitrages A-1/A-2, 22/09/2026)
-------------------------------------------------
HISTORICAL DIAGNOSTIC -- NOT A BBN TEST. BBN compatibility is NOT
DEMONSTRATED (PO-ECF-SPIN-NORM, PO-ECF-BBN-SPIN both OPEN).
  - S2_VOL below has no producing calculation and is dimensionally
    inconsistent; it has been withdrawn from Foundation II (A-1).
  - The a^-6 law applied here to <S^2>_vol contradicts Foundation II
    (a^-3, a^-3(1+w)); the identity of this sector with the stiff
    branch of Foundation I is not settled (A-2).
The script is kept only to reproduce the withdrawn figure.

PHYSICS (as originally coded)
-----------------------------
ρ_spin(T) = -(1/4) κ ⟨S²⟩_vol^(0) · (a₀/a(T))⁶   (κ = 8πG/c⁴; the constant
named KAPPA2 below holds the value of κ, not κ²)

Dilution assumed: ρ_spin ∝ a⁻⁶  (stiff era)
Standard radiation: ρ_r = (π²/30) g*(T) T⁴

OUTPUT OF THE CODE (not a result): |ρ_spin| / ρ_r at T=1 MeV ≈ 2e-51

OUTPUT: Fig_ECF_BBN_Constraint.png (300 dpi)

REFERENCES:
  - Foundation II §Canonical Parameters (κ², ⟨S²⟩_vol)
  - Kolb & Turner, The Early Universe (1990)
  - Cyburt et al. 2016, Rev.Mod.Phys. 88, 015004 (BBN review)
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
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
import matplotlib.ticker as ticker
from pathlib import Path

# ── Output ───────────────────────────────────────────────────────────────────
OUT_DIR = Path(__file__).parent / 'figures_output'
OUT_DIR.mkdir(exist_ok=True)
OUT_FILE = OUT_DIR / 'Fig_ECF_BBN_Constraint.png'

# ── ECF canonical parameters (Foundation II) ─────────────────────────────────
KAPPA2      = 2.0766e-43   # [m/J]  value of kappa = 8 pi G / c^4 (NOT kappa^2)
S2_VOL      = 3.88e-39     # WITHDRAWN (A-1): no producer, units inconsistent; historical only
P_TORS_0    = 0.25 * KAPPA2 * S2_VOL  # NOT a pressure in SI (kappa*S2 has units of kg); historical only

# ── Physical constants (SI) ──────────────────────────────────────────────────
C      = 2.99792458e8    # [m/s]
HBAR   = 1.054571817e-34 # [J·s]
KB     = 1.380649e-23    # [J/K]
EV     = 1.602176634e-19 # [J]
MEV    = EV * 1e6        # [J]
GEV    = EV * 1e9        # [J]

# ── Cosmological parameters ──────────────────────────────────────────────────
T0_K    = 2.7255         # CMB temperature today [K]
T0_EV   = KB * T0_K / EV  # [eV]  ~2.35e-4 eV
T_EW    = 159e9 * EV     # [J]   electroweak scale ~159 GeV
T_BBN   = 1e6 * EV       # [J]   BBN scale ~1 MeV

# ── Effective relativistic degrees of freedom ─────────────────────────────────
# g*(T) for Standard Model
# Values from Kolb & Turner Table 3.1
G_STAR_DATA = {
    # T [eV]: g*
    1e-4:    3.91,    # today (photons + neutrinos)
    4e-4:    3.91,    # recombination
    3e5:     3.91,    # before e+e- annihilation
    5e5:     10.75,   # after e+e- annihilation (neutrino decoupling)
    1e6:     10.75,   # T_BBN = 1 MeV
    1e8:     10.75,   # 100 MeV
    2e8:     17.25,   # QCD transition (pions)
    3e8:     61.75,   # above QCD, below EW
    1e10:    106.75,  # T > 300 GeV (full SM)
    1e14:    106.75,  # electroweak scale
}

def g_star(T_eV):
    """Effective relativistic dof at temperature T [eV] (interpolated)."""
    Ts = np.array(sorted(G_STAR_DATA.keys()))
    gs = np.array([G_STAR_DATA[t] for t in Ts])
    return np.interp(np.log10(T_eV), np.log10(Ts), gs)

def g_star_s(T_eV):
    """Entropic dof (g*S) — approximate equal to g* for T > 1 MeV."""
    return g_star(T_eV)

# ── Scale factor ratio ────────────────────────────────────────────────────────
def a0_over_a(T_J):
    """
    a₀/a(T) from entropy conservation:
    a₀/a(T) = (T/T₀) · [g*S(T₀)/g*S(T)]^(1/3)
    """
    T_eV = T_J / EV
    T0_eV_local = T0_EV
    ratio = (T_eV / T0_eV_local) * (g_star_s(T0_eV_local) / g_star_s(T_eV))**(1/3)
    return ratio

# ── Torsion density ──────────────────────────────────────────────────────────
def rho_spin(T_J):
    """
    |ρ_spin(T)| = (1/4) κ² ⟨S²⟩_vol^(0) · (a₀/a(T))⁶
    Units: [Pa = J/m³]
    """
    ratio = a0_over_a(T_J)
    return P_TORS_0 * ratio**6

# ── Radiation density ────────────────────────────────────────────────────────
def rho_radiation(T_J):
    """
    ρ_r(T) = (π²/30) g*(T) (k_B T)⁴ / (ℏc)³
    Units: [J/m³]
    """
    T_eV = T_J / EV
    gs = g_star(T_eV)
    return (np.pi**2 / 30) * gs * T_J**4 / (HBAR * C)**3

# ── Main calculation ─────────────────────────────────────────────────────────

def compute_constraint():
    """Compute and print BBN constraint."""
    T_range_J = np.logspace(
        np.log10(0.1e-3 * EV),   # 0.1 meV  (today ~T0)
        np.log10(200e9 * EV),     # 200 GeV  (electroweak)
        2000
    )

    rho_s = np.array([rho_spin(T) for T in T_range_J])
    rho_r = np.array([rho_radiation(T) for T in T_range_J])
    ratio = rho_s / rho_r

    # Key values
    T_bbn_J   = 1e6 * EV
    rs_bbn    = rho_spin(T_bbn_J)
    rr_bbn    = rho_radiation(T_bbn_J)
    ratio_bbn = rs_bbn / rr_bbn

    T_ew_J    = 150e9 * EV
    rs_ew     = rho_spin(T_ew_J)
    rr_ew     = rho_radiation(T_ew_J)
    ratio_ew  = rs_ew / rr_ew

    a0_bbn = a0_over_a(T_bbn_J)
    a0_ew  = a0_over_a(T_ew_J)

    print('=' * 65)
    print('ECF BBN Constraint — Torsion vs Radiation Energy Density')
    print('=' * 65)
    print()
    print('ECF canonical parameters:')
    print(f'  κ²          = {KAPPA2:.4e} m/J')
    print(f'  ⟨S²⟩_vol    = {S2_VOL:.2e} kg²·m/s²')
    print(f'  P_tors(z=0) = {P_TORS_0:.2e}  (historical input, withdrawn A-1; not a pressure in SI)')
    print()
    print(f'Scale factor ratios:')
    print(f'  a₀/a(T_BBN = 1 MeV)  = {a0_bbn:.3e}')
    print(f'  a₀/a(T_EW  = 159 GeV) = {a0_ew:.3e}')
    print()
    print(f'At T_BBN = 1 MeV:')
    print(f'  |ρ_spin|  = {rs_bbn:.2e} J/m³')
    print(f'  ρ_r       = {rr_bbn:.2e} J/m³')
    print(f'  RATIO     = {ratio_bbn:.2e}  (= 10^{np.log10(ratio_bbn):.1f})')
    print()
    print(f'At T_EW = 159 GeV:')
    print(f'  |ρ_spin|  = {rs_ew:.2e} J/m³')
    print(f'  ρ_r       = {rr_ew:.2e} J/m³')
    print(f'  RATIO     = {ratio_ew:.2e}  (= 10^{np.log10(ratio_ew):.1f})')
    print()
    print('HISTORICAL DIAGNOSTIC (not a BBN test; compatibility NOT demonstrated,')
    print('  PO-ECF-SPIN-NORM / PO-ECF-BBN-SPIN OPEN; inputs withdrawn, arbitrages A-1/A-2):')
    print(f'  coded ratio |ρ_spin|/ρ_r ≈ 10^{np.log10(ratio_bbn):.0f} (not a physical result)')

    # Observational BBN constraint: δN_eff < 0.4 (Cyburt+2016)
    # ΔN_eff ~ (43/7) × (ρ_spin/ρ_r) at T_BBN
    delta_Neff = (43/7) * ratio_bbn
    print()
    print(f'  ΔN_eff (torsion contribution) = {delta_Neff:.2e}')
    print(f'  Observational limit: ΔN_eff < 0.4 (Cyburt+2016)')
    print(f'  (coded value only: {0.4/max(delta_Neff, 1e-100):.1e}x below this limit; not a test)')

    return T_range_J, rho_s, rho_r, ratio, ratio_bbn


# ── Figure ────────────────────────────────────────────────────────────────────

def make_figure(T_range_J, rho_s, rho_r, ratio, ratio_bbn):
    """Generate 3-panel BBN constraint figure."""
    # Use mathtext (no usetex needed)
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral' 
    """Generate 3-panel BBN constraint figure."""

    T_eV = T_range_J / EV

    fig, axes = plt.subplots(1, 3, figsize=(16, 6), facecolor='white')
    fig.suptitle(
        'ECF BBN diagnostic (HISTORICAL, withdrawn inputs) — Torsion vs Radiation energy density\n'
        r'$|\rho_{{\rm spin}}|=\frac{{1}}{{4}}\kappa^2\langle S^2\rangle^{{(0)}}(a_0/a)^6$'
        r' vs $\rho_r=\frac{{\pi^2}}{{30}}g_*(T)T^4/(\hbar c)^3$',
        fontsize=11, fontweight='bold', y=0.99)

    C_SPIN = '#CC2222'
    C_RAD  = '#1144BB'
    C_RATIO= '#228855'
    C_BBN  = '#FF6600'
    C_EW   = '#8800CC'

    # ── Panel A: Energy densities ─────────────────────────────────────────
    ax = axes[0]

    ax.loglog(T_eV, rho_r, color=C_RAD, lw=2.5,
              label=r'$\rho_r(T)$ (radiation)')
    ax.loglog(T_eV, rho_s, color=C_SPIN, lw=2.5, ls='--',
              label=r'$|\rho_{\rm spin}(T)|$ (ECF torsion)')

    # Mark key temperatures
    for T_mark, label, color in [
        (1e-3, 'today\n~0.1 meV', '#888888'),
        (T_BBN/EV, r'$T_{\rm BBN}$'+'\n1 MeV', C_BBN),
        (T_EW/EV, r'$T_{\rm EW}$'+'\n159 GeV', C_EW),
    ]:
        ax.axvline(T_mark, color=color, lw=1.2, ls=':', alpha=0.7)
        ax.text(T_mark * 1.5, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 1e50,
                label, fontsize=7.5, color=color, va='top')

    ax.set_xlabel(r'Temperature $T$ [eV]', fontsize=11)
    ax.set_ylabel(r'Energy density [J m$^{-3}$]', fontsize=11)
    ax.set_title('Panel A — Energy densities', fontsize=10, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(1e-4, 2e14)

    # Add vertical lines after axes is set up
    ax.axvline(1e-3, color='#888888', lw=1.2, ls=':', alpha=0.7)
    ax.axvline(T_BBN/EV, color=C_BBN, lw=1.5, ls=':', alpha=0.8)
    ax.axvline(T_EW/EV, color=C_EW, lw=1.5, ls=':', alpha=0.8)

    # ── Panel B: Ratio |ρ_spin|/ρ_r ──────────────────────────────────────
    ax = axes[1]

    ax.loglog(T_eV, ratio, color=C_RATIO, lw=2.5,
              label=r'$|\rho_{\rm spin}|/\rho_r$')

    ax.axhline(1.0, color='black', lw=1.5, ls='--', alpha=0.5,
               label='Equal contribution ($= 1$)')
    # [ARBITRAGE 04/10/2026, point 9, option A] The 'BBN safety margin' line is removed:
    # it presented a verdict criterion for a ratio built on withdrawn inputs (A-1/A-2).

    ax.axvline(T_BBN/EV, color=C_BBN, lw=1.5, ls=':', alpha=0.8)
    ax.axvline(T_EW/EV, color=C_EW, lw=1.5, ls=':', alpha=0.8)

    # Annotate BBN point
    rs_bbn = rho_spin(T_BBN)
    rr_bbn = rho_radiation(T_BBN)
    r_bbn  = rs_bbn / rr_bbn
    # [ARBITRAGE 04/10/2026] The marker and the label 'BBN: ratio ~ 1e-51' are removed:
    # the level depends on the <S^2> normalisation, which is not established (PO-ECF-SPIN-NORM).
    ax.text(T_BBN/EV * 2, 1e-30,
            r'$T_{\rm BBN}$ = 1 MeV' + '\n' + r'level set by withdrawn inputs',
            fontsize=8.5, color=C_BBN, va='bottom', fontweight='bold')

    ax.set_xlabel(r'Temperature $T$ [eV]', fontsize=11)
    ax.set_ylabel(r'$|\rho_{\rm spin}|/\rho_r$', fontsize=11)
    ax.set_title(r'Panel B — $|\rho_{\rm spin}|/\rho_r$ ratio', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8.5, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(1e-4, 2e14)

    # ── Panel C: Key epochs summary table ─────────────────────────────────
    ax = axes[2]
    ax.axis('off')
    ax.set_title('Panel C — historical values (withdrawn inputs)', fontsize=10, fontweight='bold')

    epochs = [
        ('Today ($T_0$)',       T0_EV,      '$T_0 \\approx 2.4 \\times 10^{-4}$ eV'),
        ('Recombin. ($z$~1100)', 0.26,      '$T \\approx 0.26$ eV'),
        ('$e^+e^-$ annihil.',   5e5,        '$T \\approx 0.5$ MeV'),
        ('BBN ($T_{\\rm BBN}$)', 1e6,       '$T = 1$ MeV'),
        ('QCD transition',      2e8,        '$T \\approx 200$ MeV'),
        ('EW scale ($T_{\\rm EW}$)', 1.5e11,'$T = 150$ GeV'),
    ]

    col_labels = ['Epoch', '$T$ [eV]', '$|\\rho_{\\rm spin}|/\\rho_r$']   # 'BBN safe?' column removed (04/10/2026)
    rows = []
    for name, T_ev, _ in epochs:
        T_j = T_ev * EV
        rs = rho_spin(T_j)
        rr = rho_radiation(T_j)
        r  = rs / rr
        log_r = np.log10(r) if r > 0 else -999
        rows.append([name, f'$10^{{{np.log10(T_ev):.1f}}}$',
                     f'$10^{{{log_r:.0f}}}$'])

    tbl = ax.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc='center',
        loc='center',
        bbox=[0.0, 0.15, 1.0, 0.75],
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)

    # Style header
    for j in range(3):
        tbl[0, j].set_facecolor('#1144BB')
        tbl[0, j].set_text_props(color='white', fontweight='bold')

    # Style BBN row (row 4 = index 4, since header is 0)
    bbn_row = 4  # BBN epoch
    for j in range(3):
        tbl[bbn_row, j].set_facecolor('#FFF0E0')
        tbl[bbn_row, j].set_text_props(color='#AA4400', fontweight='bold')

    # Conclusion box (04/10/2026): no verdict, no numerical result; states the status only.
    ax.text(0.5, 0.07,
            'HISTORICAL DIAGNOSTIC -- not a BBN test\n'
            r'$\langle S^2\rangle$ normalisation not fixed (PO-ECF-SPIN-NORM)' + '\n'
            'BBN compatibility NOT demonstrated (PO-ECF-BBN-SPIN)',
            transform=ax.transAxes,
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', fc='#F2F2F2',
                      ec='#666666', lw=1.5))

    # Caption
    fig.text(0.5, 0.01,
             r'Historical inputs (withdrawn, A-1/A-2): $\kappa=8\pi G/c^4$, '
             r'$\langle S^2\rangle_{vol}^{(0)}$ normalisation not established | '
             r'$\rho_{spin}\propto a^{-6}$ assumed | '
             'Reference: Cyburt et al. 2016, Rev.Mod.Phys. 88, 015004',
             ha='center', fontsize=8, color='#444444',
             bbox=dict(boxstyle='round,pad=0.25', fc='#F5F5FF',
                       ec='#AAAACC', lw=0.7))

    fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.12, wspace=0.35)
    fig.savefig(OUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'\n[OK] → {OUT_FILE}')


if __name__ == '__main__':
    T_range, rho_s, rho_r, ratio, ratio_bbn = compute_constraint()
    make_figure(T_range, rho_s, rho_r, ratio, ratio_bbn)
