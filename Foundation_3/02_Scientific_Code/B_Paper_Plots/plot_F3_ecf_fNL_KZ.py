#!/usr/bin/env python3
"""
ecf_fNL_KZ.py
=============
ECF Foundation III — Non-Gaussianity f_NL^KZ from Kibble-Zurek network
Author: Pascal Fichant
Date:   June 2026

PHYSICS
-------
The KZ network of Micro-Knots is a 3D Poisson point process
with number density n_KZ = ξ_KZ^{-3}.

For a Poisson field, all cumulants are equal to the mean:
  ⟨δN^k⟩_c = ⟨N⟩   for all k

The reduced bispectrum parameter f_NL^local is:
  f_NL^local = (5/18) × κ_3/σ²
             = (5/18) × (1/N_KZ) / (ξ_KZ/d_H)³
             = (5/18) × 1/N_KZ × N_KZ
             = 5/18 ≈ 0.28   (3D, before projection)

CMB projection: WITHDRAWN (audit v2, lot S). f_NL is defined on the primordial
  field (zeta = zeta_g + 3/5 f_NL zeta_g^2); a linear projection y = a x rescales
  <y^3>/<y^2>^2 by 1/a, so no ×(1/3) or ×(1/3)² factor applies. The f_NL_CMB
  estimator below is kept only for traceability of earlier versions.
  STATUS: 5/18 = raw 3D Poisson statistic, CONDITIONAL (Poisson→ζ bridge not
  demonstrated); value at the CMB OPEN.

KEY RESULT:
  raw 3D Poisson statistic 5/18 ≈ 0.28; coherent-limit estimator
  0.0010–0.0016 (xi_KZ = 50–80 Mpc, not derived)
  COMPATIBLE with Planck PR3: f_NL = -0.9 ± 5.1
  DISTINCTIVE from inflation: f_NL^infl ≈ -0.015 (opposite sign)
  Future CMB surveys: the CMB-S4 forecast sigma(f_NL) ~ 0.3 predates the end of
  DOE/NSF support (July 2025) and is no longer available.
  [15/10/2026, F3-A16: figure and printed summary aligned with the paper --
  the x1/3 'CMB projected' value is no longer drawn, the decision tree is
  conditional, and nothing is labelled 'confirmed'.]

OUTPUT: Fig_ECF_fNL_KZ.png (300 dpi)
"""

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
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# ── Output ───────────────────────────────────────────────────────────────────
OUT_DIR = Path(__file__).parent / 'figures_output'
OUT_DIR.mkdir(exist_ok=True)
OUT_FILE = OUT_DIR / 'Fig_ECF_fNL_KZ.png'

# ── ECF parameters ───────────────────────────────────────────────────────────
XI_KZ_VALUES = np.array([50, 60, 80])   # Mpc — 1σ range
XI_KZ_CENTRAL = 60.0                     # Mpc — central value
R_H = 14000.0                            # Mpc — Hubble distance

# ── Planck constraints (PR3) ─────────────────────────────────────────────────
F_NL_PLANCK = -0.9
F_NL_PLANCK_SIGMA = 5.1

# Planck PR4: Jung, Citran, van Tent, Dumilly & Aghanim, arXiv:2504.00884 (2025),
# full T+E: f_NL^local = -0.1 +/- 5.0.
# [CORRIGE 15/10/2026, F3-A3 : etait -0.8 +/- 4.5 attribue a "Carron+2022 lensing", sans source]
F_NL_PLANCK_PR4 = -0.1
F_NL_PLANCK_PR4_SIGMA = 5.0

# ── Inflation Maldacena relation ─────────────────────────────────────────────
NS = 0.9649   # Planck 2018
F_NL_INFLATION = 5*(NS - 1)/12   # ~ -0.015

# ── f_NL^KZ derivation ───────────────────────────────────────────────────────

def compute_fNL_KZ(xi_kz, r_H=R_H):
    """
    Compute f_NL^KZ for a Poisson KZ network.

    Three estimators:
    1. Full 3D bispectrum (before CMB projection)
    2. After Sachs-Wolfe projection (3D -> 2D CMB)
    3. Lower bound (coherent scale limit)
    """
    N_KZ = (r_H / xi_kz)**3
    sigma2 = (xi_kz / r_H)**3
    sigma  = np.sqrt(sigma2)

    # Poisson third cumulant
    kappa3 = 1.0 / N_KZ   # = sigma2 (since N_KZ = sigma2^{-1})

    # ── Estimator 1: 3D Poisson bispectrum ────────────────────────────────
    # B^Poisson(k1,k2,k3) = (1/n_bar)[P(k1)P(k2) + cyc]
    # f_NL^local = (5/18) κ_3/σ^2
    # Note: for Poisson, κ_3 = σ^2 exactly, so f_NL^3D = 5/18
    f_NL_3D = (5.0/18.0) * kappa3 / sigma2   # = 5/18 ≈ 0.278

    # ── Estimator 2: CMB projection (Sachs-Wolfe) ─────────────────────────
    # δT/T = (1/3) δ_m at large scales (Sachs-Wolfe)
    # ⟨(δT/T)³⟩ ∝ (1/3)³ ⟨δ_m³⟩
    # f_NL^CMB = f_NL^3D × (1/3)  [linear approximation]
    beta_SW = 1.0/3.0
    f_NL_CMB = f_NL_3D * beta_SW

    # ── Estimator 3: Coherent network limit ───────────────────────────────
    # At scales R >> ξ_KZ, the Poisson fluctuations go as
    # f_NL^coh ~ (5/18) / N_KZ^{1/3}
    f_NL_coh = (5.0/18.0) / N_KZ**(1.0/3.0)

    return {
        'N_KZ':     N_KZ,
        'sigma':    sigma,
        'sigma2':   sigma2,
        'kappa3':   kappa3,
        'f_NL_3D':  f_NL_3D,
        'f_NL_CMB': f_NL_CMB,
        'f_NL_coh': f_NL_coh,
    }


def print_results():
    print('=' * 65)
    print('f_NL^KZ — ECF Kibble-Zurek Non-Gaussianity')
    print('=' * 65)
    print(f'\nξ_KZ central = {XI_KZ_CENTRAL} Mpc, range = {XI_KZ_VALUES} Mpc')
    print(f'd_H = {R_H} Mpc')
    print()

    r = compute_fNL_KZ(XI_KZ_CENTRAL)
    print(f'N_KZ  = (d_H/ξ_KZ)³ = {r["N_KZ"]:.3e}')
    print(f'σ     = (ξ_KZ/d_H)^(3/2) = {r["sigma"]:.3e}')
    print(f'κ₃    = 1/N_KZ = {r["kappa3"]:.3e} = σ²')
    print()
    print(f'f_NL^KZ (3D Poisson bispectrum)  = {r["f_NL_3D"]:.4f}')
    print(f'f_NL^KZ (x1/3 SW, WITHDRAWN)     = {r["f_NL_CMB"]:.4f}   [traceability only]')
    print(f'f_NL^KZ (coherent network limit) = {r["f_NL_coh"]:.6f}')
    print()
    print(f'f_NL^inflation (Maldacena) = {F_NL_INFLATION:.4f}')
    print(f'f_NL^Planck PR3 = {F_NL_PLANCK:.1f} ± {F_NL_PLANCK_SIGMA:.1f}')
    print()
    print('KEY RESULTS:')
    print(f'  1. f_NL^KZ is POSITIVE → opposite sign from inflation')
    print(f'  2. raw 3D value: f_NL = 5/18 ≈ 0.28, conditional on the Poisson->zeta bridge')
    print(f'  3. value at the CMB: OPEN (no projection factor applies)')
    print(f'  4. COMPATIBLE with Planck PR3 (-0.9 ± 5.1) and PR4 (-0.1 ± 5.0)')
    print(f'  5. future CMB surveys; pre-2025 CMB-S4 forecast sigma ~ 0.3 no longer available')
    print()

    # Range over ξ_KZ
    print('Sensitivity to ξ_KZ:')
    for xi in XI_KZ_VALUES:
        rv = compute_fNL_KZ(xi)
        print(f'  ξ_KZ={xi:3.0f} Mpc: '
              f'f_NL^3D={rv["f_NL_3D"]:.4f}, '
              f'f_NL^CMB(withdrawn)={rv["f_NL_CMB"]:.4f}, '
              f'f_NL^coh={rv["f_NL_coh"]:.6f}')

    print()
    print('PHYSICAL INTERPRETATION:')
    print('  The KZ Poisson network generates a POSITIVE f_NL.')
    print('  This is because overdense regions (clusters of Micro-Knots)')
    print('  are more clustered than a Gaussian field predicts.')
    print('  The discreteness of the network is the source of')
    print('  non-Gaussianity, not quantum vacuum fluctuations.')
    print()
    print('CONDITIONAL STATISTIC (Poisson->zeta bridge not established):')
    print(f"  raw 3D f_NL^KZ = 5/18 = {compute_fNL_KZ(XI_KZ_CENTRAL)['f_NL_3D']:.4f}; value at the CMB OPEN")
    print('  (x1/3 "CMB projection" withdrawn: f_NL is not rescaled by a linear projection)')
    print(f'  Sign: POSITIVE (vs inflation: NEGATIVE)')
    print(f'  pre-2025 CMB-S4 forecast sigma(f_NL) ~ 0.3 (DOE/NSF support ended July 2025)')
    print(f'  A measurement f_NL < -1 at >2σ would disfavour ECF KZ')


# ── Figure ───────────────────────────────────────────────────────────────────

def make_figure():
    plt.rcParams['mathtext.fontset'] = 'stix'
    r_central = compute_fNL_KZ(XI_KZ_CENTRAL)

    fig, axes = plt.subplots(1, 3, figsize=(16, 6), facecolor='white')
    fig.suptitle(
        r'$f_{\rm NL}^{\rm KZ}$ — ECF Non-Gaussianity from Kibble-Zurek Poisson network' '\n'
        r'3D Poisson: $f_{\rm NL}^{\rm KZ}=5/18\approx+0.28$  |  '
        r'(raw 3D statistic, conditional; value at the CMB open)  |  Compatible with Planck PR3/PR4',
        fontsize=11, fontweight='bold', y=0.99)

    C_KZ   = '#1144BB'
    C_INF  = '#CC2222'
    C_PL   = '#228855'
    C_CMBS4 = '#AA6600'

    # ── Panel A: f_NL vs ξ_KZ ─────────────────────────────────────────────
    ax = axes[0]
    xi_range = np.linspace(30, 120, 200)
    fNL_3D   = np.array([compute_fNL_KZ(xi)['f_NL_3D']  for xi in xi_range])
    fNL_CMB  = np.array([compute_fNL_KZ(xi)['f_NL_CMB'] for xi in xi_range])
    fNL_coh  = np.array([compute_fNL_KZ(xi)['f_NL_coh'] for xi in xi_range])

    ax.plot(xi_range, fNL_3D,  color=C_KZ,  lw=2.5, label=r'$f_\mathrm{NL}^\mathrm{KZ}$ (3D Poisson)')
    ax.plot(xi_range, fNL_coh, color=C_KZ,  lw=1.5, ls=':',
            label=r'$f_{\rm NL}^{\rm KZ}$ (coherent limit, not derived)')

    # Planck 1σ and 2σ bands
    ax.axhspan(F_NL_PLANCK - F_NL_PLANCK_SIGMA,
               F_NL_PLANCK + F_NL_PLANCK_SIGMA,
               alpha=0.12, color=C_PL, label=r'Planck PR3 $1\sigma$')
    ax.axhspan(F_NL_PLANCK - 2*F_NL_PLANCK_SIGMA,
               F_NL_PLANCK + 2*F_NL_PLANCK_SIGMA,
               alpha=0.06, color=C_PL, label='Planck PR3 2-sigma')
    ax.axhline(F_NL_PLANCK, color=C_PL, lw=1.5, ls='-', alpha=0.7)

    # Inflation value
    ax.axhline(F_NL_INFLATION, color=C_INF, lw=1.5, ls='--',
               label=r'Inflation (Maldacena) $\approx -0.015$')
    ax.axhline(0, color='black', lw=0.8, alpha=0.4)

    # ξ_KZ range
    ax.axvspan(50, 80, alpha=0.12, color=C_KZ, label=r'ECF $\xi_{\rm KZ}$ range')
    ax.axvline(XI_KZ_CENTRAL, color=C_KZ, lw=1.2, ls=':', alpha=0.7)

    ax.set_xlabel(r'$\xi_\mathrm{KZ}$ [Mpc]', fontsize=11)
    ax.set_ylabel(r'$f_{NL}^{KZ}$', fontsize=11)
    ax.set_title(r'Panel A — $f_{NL}^{KZ}$ vs $\xi_{KZ}$',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=7.5, loc='upper right')
    ax.grid(True, alpha=0.2)
    ax.set_ylim(-8, 0.5)

    # ── Panel B: Comparison with experiments ──────────────────────────────
    ax = axes[1]
    ax.set_xlim(-12, 4)
    ax.set_ylim(-0.5, 5.5)
    ax.axis('off')
    ax.set_title(r'Panel B — $f_{\rm NL}$ comparison',
                 fontsize=10, fontweight='bold')

    experiments = [
        ('Planck PR3 (2019)',    F_NL_PLANCK,    F_NL_PLANCK_SIGMA,    C_PL,   0),
        ('Planck PR4 (2025)',    F_NL_PLANCK_PR4, F_NL_PLANCK_PR4_SIGMA, '#559955', 1),
        ('CMB-S4 forecast (pre-2025)', 0.0,        0.3,                   C_CMBS4, 2),
        ('Inflation (Maldacena)', F_NL_INFLATION,  0.001,                 C_INF,  3),
    ]

    ecf_vals = [
        (r'$f_{NL}^{KZ}$ (raw 3D, cond.)', r_central['f_NL_3D'],  0.03, C_KZ, 4),
    ]

    for name, val, err, col, y in experiments:
        ax.errorbar(val, y, xerr=err, fmt='o', color=col,
                    ms=8, elinewidth=2, capsize=5, zorder=5)
        ax.text(val + err + 0.2, y, f'{val:.2f} ± {err:.1f}',
                fontsize=8.5, va='center', color=col)
        ax.text(-11.5, y, name, fontsize=8.5, va='center', color='#333333')

    # ECF values (rightmost, marked differently)
    for name, val, err, col, y in ecf_vals:
        ax.plot(val, y, 's', color=col, ms=10, zorder=6,
                markeredgecolor='#111111', markeredgewidth=1.5)
        ax.text(val + 0.2, y, f'+{val:.3f}', fontsize=8.5,
                va='center', color=col, fontweight='bold')
        ax.text(-11.5, y, name, fontsize=8.0, va='center', color=col,
                fontweight='bold')

    ax.axvline(0, color='black', lw=0.8, alpha=0.4)

    # Arrow showing sign difference
    ax.annotate('', xy=(r_central['f_NL_3D'], 4),
                xytext=(F_NL_INFLATION, 3),
                arrowprops=dict(arrowstyle='<->', color='#884400',
                                lw=1.5, mutation_scale=14))
    ax.text(-3, 3.9, 'Opposite sign!', fontsize=8.5, color='#884400',
            ha='center', style='italic', fontweight='bold')

    ax.set_xlabel(r'$f_{NL}^{local}$', fontsize=11)

    # ── Panel C: Decision diagram ──────────────────────────────────────────
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title(r'Panel C — Falsifiability tree for $f_{\rm NL}^{\rm KZ}$',
                 fontsize=10, fontweight='bold')

    def box(ax, x, y, w, h, text, fc, ec='black', fs=8.5):
        rect = mpatches.FancyBboxPatch((x, y), w, h, alpha=0.18,
                                        boxstyle='round,pad=0.12',
                                        facecolor=fc, edgecolor=ec, lw=1.2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, text, ha='center', va='center',
                fontsize=fs, fontweight='bold',
                color='#111111' if fc not in ['#FAFAFA','#FFF4E8','#E8F4E8'] else '#222222')

    box(ax, 1.0, 6.2, 8.0, 1.2,
        'Future CMB survey measures f_NL\n(Poisson->zeta bridge required first)', '#334466', '#1144BB', fs=8)

    box(ax, 0.2, 3.8, 4.0, 1.6,
        'f_NL > 0 at >1σ\n(positive)', '#115522', '#228855')

    box(ax, 5.6, 3.8, 4.0, 1.6,
        'f_NL < -1 at >2σ\n(negative, large)', '#661122', '#CC2222')

    box(ax, 0.2, 1.5, 4.0, 1.7,
        'KZ channel\nsupported\n(conditional, not\na confirmation)', '#228855', '#115522')

    box(ax, 5.6, 1.5, 4.0, 1.7,
        'ECF KZ channel\ndisfavoured\n(wrong sign)', '#CC2222', '#881100')

    for x1, y1, x2, y2 in [
        (5.0, 6.2, 2.2, 5.4),
        (5.0, 6.2, 7.6, 5.4),
        (2.2, 3.8, 2.2, 3.2),
        (7.6, 3.8, 7.6, 3.2),
    ]:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#444444',
                                   lw=1.5, mutation_scale=13))

    ax.text(3.0, 5.9, 'YES (+)', fontsize=9,
            color='#228855', fontweight='bold', ha='center')
    ax.text(7.0, 5.9, 'NO (-)', fontsize=9,
            color='#CC2222', fontweight='bold', ha='center')

    ax.text(5.0, 0.5,
            r'ECF: raw 3D $f_{\rm NL}^{\rm KZ}=5/18$ (conditional); value at the CMB open' '\n'
            r'Inflation: $f_{NL}^{infl} \approx -0.015$  (negative)' '\n'
            r'=> Sign is the key discriminant',
            ha='center', fontsize=8, color='#333333',
            bbox=dict(boxstyle='round,pad=0.3', fc='#F5F5FF',
                      ec='#AAAACC', lw=0.8))

    # Caption
    fig.text(0.5, 0.01,
             r'ECF KZ network: Poisson with $n_{KZ}=\xi_{KZ}^{-3}$, '
             r'$\xi_{KZ}=60$ Mpc | '
             r'$f_{NL}^{local}=(5/18)\kappa_3/\sigma^2$ | '
             r'Planck PR3: $f_{NL}=-0.9 \pm 5.1$ (Akrami+2020) | '
             r'pre-2025 CMB-S4 forecast: $\sigma(f_{NL})\sim 0.3$',
             ha='center', fontsize=8, color='#444444',
             bbox=dict(boxstyle='round,pad=0.25', fc='#F5F5FF',
                       ec='#AAAACC', lw=0.7))

    fig.subplots_adjust(left=0.06, right=0.98, top=0.88,
                        bottom=0.12, wspace=0.30)
    fig.savefig(OUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'\n[OK] -> {OUT_FILE}')


if __name__ == '__main__':
    print_results()
    make_figure()
