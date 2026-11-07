#!/usr/bin/env python3
"""
ecf_Cell_suppression.py
=======================
ECF Foundation III — Low-ell CMB power spectrum suppression
Author: Pascal Fichant
Date:   June 2026
Docstring corrected 01/09/2026 (self-correction already present in the
script body, l.97, never propagated up here -- caught while cross-checking
Architecture Appendix F, "Methods behind each prediction").

PHYSICS
-------
The KZ network introduces a characteristic scale xi_KZ ~ 60 Mpc.
At angular scales corresponding to R > xi_KZ, the Poisson fluctuations
of the network are suppressed by the form factor W_KZ(k*xi_KZ), xi_KZ being
read as the cell RADIUS (same convention as the VSF threshold R_void > xi_KZ).
[CORRIGE 15/10/2026, decision F3-A2 (B) : l'en-tete et le panneau P(k)
portaient W(k*xi/2) (xi = diametre) alors que le calcul des C_ell utilise
x = l/l_KZ (xi = rayon) ; facteur 2 dans l'argument. Convention rayon retenue.]

For multipole l, the effective wavenumber is k_eff = l/chi_*
(Limber approximation, chi_* = 14000 Mpc).

The ECF C_ell suppression factor, with the CORRECT argument
(see in-code derivation below, "Correct argument: x = l / l_KZ"):
  S_ECF(l) = W_KZ(k_eff * xi_KZ)
           = [3(sin(x) - x*cos(x))/x^3]^2  where x = l / l_KZ
  l_KZ = chi_* / xi_KZ ~ 233   (suppression onset, NOT at l~10)

KEY RESULT:
  l ~ 233: suppression ~18% (testable with ACT/SPT/CMB-S4, sigma ~ few %)
  The Planck low-l anomaly (l<10) is NOT explained by xi_KZ=60 Mpc -- an
  earlier version of this file mistakenly placed the suppression scale
  near l~10; that placement is superseded (see the explicit correction
  and print() diagnostics further down confirming l_KZ~233).

EPISTEMIC STATUS:
  - Testable prediction, distinct from the (unrelated) Planck low-l anomaly
  - Rigorous derivation of xi_KZ itself requires CLASS-EC (Foundation IV)

OUTPUT: Fig_ECF_Cell_Suppression.png (300 dpi)

REFERENCES:
  - Planck 2018 CMB low-ell anomaly: Akrami+2020 arXiv:1906.02552
  - Bennett+2013 WMAP 9yr: anomaly confirmed at ~2.5 sigma
  - Schwarz+2016 review of CMB anomalies: arXiv:1510.07929
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
from matplotlib.lines import Line2D
from pathlib import Path

# ── Output ───────────────────────────────────────────────────────────────────
OUT_DIR  = Path(__file__).parent / 'figures_output'
OUT_DIR.mkdir(exist_ok=True)
OUT_FILE = OUT_DIR / 'Fig_ECF_Cell_Suppression.png'

# ── ECF canonical parameters ─────────────────────────────────────────────────
XI_KZ     = 60.0    # Mpc  KZ correlation length (central value)
XI_KZ_LO  = 50.0    # Mpc  lower bound
XI_KZ_HI  = 80.0    # Mpc  upper bound
CHI_STAR  = 14000.0 # Mpc  comoving distance to recombination
NS        = 0.9649  # scalar spectral index (Planck 2018)
AS        = 2.1e-9  # scalar amplitude

# ── Planck low-ell anomaly data ──────────────────────────────────────────────
# Ratio C_ell^obs / C_ell^LCDM from Planck 2018 TT (Akrami+2020, Fig 3)
# Approximate values from literature
PLANCK_L = np.array([2,  3,  4,  5,  6,  7,  8,  9,  10,
                     12, 15, 20, 25, 30])
PLANCK_RATIO = np.array([0.14, 0.68, 1.05, 0.77, 0.92, 0.98, 0.83, 0.75, 0.72,
                          0.88, 0.91, 0.95, 0.98, 1.00])
# Cosmic variance sigma: sqrt(2/(2l+1))
PLANCK_CV = np.sqrt(2.0 / (2*PLANCK_L + 1))

# ── Form factor functions ────────────────────────────────────────────────────

def W_tophat_sq(x):
    """
    Top-hat window function squared (Fourier transform of sphere).
    W^2(x) = [3(sin(x) - x*cos(x))/x^3]^2
    """
    x = np.where(np.abs(x) < 1e-6, 1e-6, x)
    return (3.0 * (np.sin(x) - x*np.cos(x)) / x**3)**2


def S_ECF(l, xi=XI_KZ, chi=CHI_STAR):
    """
    ECF suppression factor for C_ell.
    Correct argument: x = l / l_KZ where l_KZ = chi_* / xi_KZ
    S_ECF(l) = W^2(l * xi_KZ / chi_*)
    Suppression onset at l_KZ = chi_*/xi_KZ ~ 233 (NOT at l~10)
    """
    l_KZ = chi / xi   # ~ 14000/60 ~ 233
    x = np.asarray(l, dtype=float) / l_KZ
    return W_tophat_sq(x)


def delta_C_over_C(l, xi=XI_KZ):
    """Fractional suppression: (C_LCDM - C_ECF) / C_LCDM = 1 - S_ECF."""
    return 1.0 - S_ECF(l, xi)


# ── Primordial power spectrum (Harrison-Zel'dovich + ECF modulation) ─────────

def P_prim_LCDM(k, As=AS, ns=NS, k_pivot=0.05):
    """Standard primordial scalar power spectrum."""
    return As * (k / k_pivot)**(ns - 1)


def P_prim_ECF(k, xi=XI_KZ, As=AS, ns=NS, k_pivot=0.05):
    """
    ECF modulated primordial spectrum.
    P_ECF(k) = P_LCDM(k) * W^2(k * xi_KZ)   [15/10/2026 : etait k*xi/2]
    """
    x = k * xi
    return P_prim_LCDM(k, As, ns, k_pivot) * W_tophat_sq(x)


# ── Angular correlation function C(theta) ────────────────────────────────────

def C_theta_LCDM(theta_deg, l_max=100):
    """
    Angular correlation function C(theta) = sum_l (2l+1)/(4pi) C_l P_l(cos theta)
    Approximated using Harrison-Zel'dovich spectrum.
    """
    theta = np.radians(theta_deg)
    cos_t = np.cos(theta)
    l_vals = np.arange(2, l_max+1, dtype=float)

    # Approximate C_l^LCDM ∝ 1/(l(l+1)) (Sachs-Wolfe plateau)
    C_l = 1.0 / (l_vals * (l_vals + 1))
    C_l /= C_l.sum()  # normalise

    # Legendre polynomials via recurrence
    result = 0.0
    P_prev2 = np.ones_like(l_vals)   # P_0
    P_prev1 = cos_t * np.ones_like(l_vals)  # P_1

    for i, l in enumerate(l_vals):
        if l == 2:
            P_l = 0.5*(3*cos_t**2 - 1)
        elif l == 3:
            P_l = 0.5*(5*cos_t**3 - 3*cos_t)
        elif l >= 4:
            # Will compute below
            pass
        result += (2*l+1)/(4*np.pi) * C_l[i] * P_l if l <= 3 else 0

    # Full computation via vectorised recurrence
    Pl = np.zeros(l_max+1)
    Pl[0] = 1.0
    Pl[1] = cos_t
    for ll in range(2, l_max+1):
        Pl[ll] = ((2*ll-1)*cos_t*Pl[ll-1] - (ll-1)*Pl[ll-2]) / ll

    C_l_full = np.zeros(l_max+1)
    for ll in range(2, l_max+1):
        C_l_full[ll] = 1.0 / (ll*(ll+1))
    C_l_full /= C_l_full[2:].sum()

    C_theta = sum((2*ll+1)/(4*np.pi) * C_l_full[ll] * Pl[ll]
                  for ll in range(2, l_max+1))
    return C_theta


def C_theta_ECF(theta_deg, xi=XI_KZ, l_max=100):
    """C(theta) with ECF suppression at low ell."""
    theta = np.radians(theta_deg)
    cos_t = np.cos(theta)

    Pl = np.zeros(l_max+1)
    Pl[0] = 1.0
    Pl[1] = cos_t
    for ll in range(2, l_max+1):
        Pl[ll] = ((2*ll-1)*cos_t*Pl[ll-1] - (ll-1)*Pl[ll-2]) / ll

    C_l_full = np.zeros(l_max+1)
    for ll in range(2, l_max+1):
        C_l_full[ll] = 1.0 / (ll*(ll+1))

    # Apply ECF suppression
    for ll in range(2, l_max+1):
        C_l_full[ll] *= S_ECF(ll, xi=xi)

    C_l_full /= C_l_full[2:].sum()  # renormalise

    C_theta = sum((2*ll+1)/(4*np.pi) * C_l_full[ll] * Pl[ll]
                  for ll in range(2, l_max+1))
    return C_theta


# ── Main figure ───────────────────────────────────────────────────────────────

def make_figure():
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), facecolor='white')
    fig.suptitle(
        'ECF Low-ell CMB: True suppression at l~233, NOT l<10\n'
        r'$S_\mathrm{ECF}(\ell)=W^2(\ell/\ell_\mathrm{KZ})$, '
        r'$\ell_\mathrm{KZ}=\chi_*/\xi_\mathrm{KZ}\approx233$  |  '
        'Planck l<10 anomaly: OPEN QUESTION in ECF',
        fontsize=10.5, fontweight='bold', y=0.99)

    C_ECF  = '#1144BB'
    C_LCDM = '#888888'
    C_PL   = '#228855'
    C_BAND = '#AABBEE'
    C_CV   = '#CCCCCC'

    l_fine = np.linspace(2, 100, 500)

    # ── Panel A: Suppression factor S_ECF(l) ──────────────────────────────
    ax = axes[0, 0]

    S_central = S_ECF(l_fine, XI_KZ)
    S_lo      = S_ECF(l_fine, XI_KZ_LO)
    S_hi      = S_ECF(l_fine, XI_KZ_HI)

    ax.fill_between(l_fine, S_lo, S_hi, alpha=0.20, color=C_ECF,
                    label=r'ECF 1$\sigma$ ($\xi_{\mathrm{KZ}}=50$–80 Mpc)')
    ax.plot(l_fine, S_central, color=C_ECF, lw=2.5,
            label=r'ECF central ($\xi_{\mathrm{KZ}}=60$ Mpc)')
    ax.axhline(1.0, color=C_LCDM, lw=1.5, ls='--',
               label=r'$\Lambda$CDM ($S=1$)')

    # Mark l=10
    s10 = S_ECF(10, XI_KZ)
    ax.plot(10, s10, 'o', color=C_ECF, ms=10, zorder=5)
    ax.annotate(f'$\\ell=10$: $S={s10:.2f}$\n(suppression {(1-s10)*100:.0f}%)',
                xy=(10, s10), xytext=(22, 0.55),
                arrowprops=dict(arrowstyle='->', color=C_ECF, lw=1.5),
                fontsize=9, color=C_ECF, fontweight='bold')

    # Cosmic variance band
    l_int = np.arange(2, 101)
    cv = np.sqrt(2.0/(2*l_int+1))
    ax.fill_between(l_int, 1-cv, 1+cv, alpha=0.12, color=C_CV,
                    label='Cosmic variance $\\pm1\\sigma$')

    ax.set_xlabel(r'Multipole $\ell$', fontsize=11)
    ax.set_ylabel(r'$S_{\mathrm{ECF}}(\ell) = C_\ell^{\mathrm{ECF}}/C_\ell^{\Lambda\mathrm{CDM}}$',
                  fontsize=10)
    ax.set_title('Panel A — ECF suppression factor $S_{\\mathrm{ECF}}(\\ell)$',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=8.5, loc='lower right')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(2, 50)
    ax.set_ylim(0.0, 1.25)

    # ── Panel B: Comparison with Planck low-ell data ───────────────────────
    ax = axes[0, 1]

    # ECF prediction band
    S_lo_pts = S_ECF(PLANCK_L, XI_KZ_LO)
    S_hi_pts = S_ECF(PLANCK_L, XI_KZ_HI)
    S_cen_pts= S_ECF(PLANCK_L, XI_KZ)

    ax.fill_between(PLANCK_L, S_lo_pts, S_hi_pts,
                    alpha=0.25, color=C_ECF, label=r'ECF 1$\sigma$')
    ax.plot(PLANCK_L, S_cen_pts, color=C_ECF, lw=2.5,
            label=r'ECF prediction $S_{\mathrm{ECF}}(\ell)$')

    # Planck data points
    ax.errorbar(PLANCK_L, PLANCK_RATIO, yerr=PLANCK_CV,
                fmt='o', color=C_PL, ms=6, elinewidth=1.5,
                capsize=3, label='Planck 2018 TT (approx.)', zorder=5)

    ax.axhline(1.0, color=C_LCDM, lw=1.5, ls='--',
               label=r'$\Lambda$CDM')

    # Cosmic variance
    l_cv = np.arange(2, 31)
    cv2  = np.sqrt(2.0/(2*l_cv+1))
    ax.fill_between(l_cv, 1-cv2, 1+cv2, alpha=0.10, color=C_CV)

    # Arrow: Planck anomaly region
    ax.axvspan(2, 12, alpha=0.06, color='orange',
               label='Planck anomaly region ($\\ell<12$)')

    ax.set_xlabel(r'Multipole $\ell$', fontsize=11)
    ax.set_ylabel(r'$C_\ell / C_\ell^{\Lambda\mathrm{CDM}}$', fontsize=11)
    ax.set_title('Panel B — ECF vs Planck 2018 TT low-$\\ell$',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(2, 30)
    ax.set_ylim(0.0, 1.6)

    # Epistemic warning
    ax.text(0.02, 0.97,
            'Epistemic note: Planck data\napproximate; ECF suppression\n'
            'within cosmic variance\n(not a closed prediction)',
            transform=ax.transAxes, fontsize=8,
            color='#884400', va='top',
            bbox=dict(boxstyle='round,pad=0.3', fc='#FFF4E8',
                      ec='#CC6600', lw=1.5))

    # ── Panel C: Primordial power spectrum P(k) ────────────────────────────
    ax = axes[1, 0]

    k_range = np.logspace(-4, 0, 500)  # Mpc^-1
    P_LCDM  = P_prim_LCDM(k_range)
    P_ECF_c = P_prim_ECF(k_range, XI_KZ)
    P_ECF_lo= P_prim_ECF(k_range, XI_KZ_LO)
    P_ECF_hi= P_prim_ECF(k_range, XI_KZ_HI)

    ax.loglog(k_range, P_LCDM / P_LCDM.max(),
              color=C_LCDM, lw=2.0, ls='--',
              label=r'$\Lambda$CDM (Harrison-Zel\'dovich)')
    ax.fill_between(k_range,
                    P_ECF_lo / P_LCDM.max(),
                    P_ECF_hi / P_LCDM.max(),
                    alpha=0.20, color=C_ECF)
    ax.loglog(k_range, P_ECF_c / P_LCDM.max(),
              color=C_ECF, lw=2.5,
              label=r'ECF: $P_{\mathrm{KZ}}(k) = P_{\Lambda}(k)\,W^2(k\xi)$')

    # Mark k_KZ
    k_KZ = 1.0 / XI_KZ   # 15/10/2026 : k = l_KZ/chi_* = 1/xi_KZ (etait 2*pi/xi_KZ)
    ax.axvline(k_KZ, color=C_ECF, lw=1.2, ls=':', alpha=0.7)
    ax.text(k_KZ*1.2, 0.3, r'$k_{\mathrm{KZ}}=1/\xi_{\mathrm{KZ}}\leftrightarrow\ell_{\mathrm{KZ}}$',
            fontsize=8, color=C_ECF, rotation=90, va='center')

    # Mark large-scale modes
    for l_mark, label in [(2, r'$\ell=2$'), (10, r'$\ell=10$'),
                           (100, r'$\ell=100$')]:
        k_m = l_mark / CHI_STAR
        ax.axvline(k_m, color='#AA6600', lw=0.8, ls=':', alpha=0.5)
        ax.text(k_m*1.3, 1e-3, label, fontsize=7.5,
                color='#AA6600', rotation=90, va='bottom')

    ax.set_xlabel(r'Wavenumber $k$ [Mpc$^{-1}$]', fontsize=11)
    ax.set_ylabel(r'$P(k)$ (normalised)', fontsize=11)
    ax.set_title('Panel C — Primordial power spectrum $P(k)$',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)
    ax.set_xlim(1e-4, 1e0)
    ax.set_ylim(1e-4, 2.0)

    # ── Panel D: Angular correlation function C(theta) ────────────────────
    ax = axes[1, 1]

    theta_vals = np.linspace(5, 175, 80)
    C_lcdm_arr = np.array([C_theta_LCDM(t) for t in theta_vals])
    C_ecf_arr  = np.array([C_theta_ECF(t, XI_KZ) for t in theta_vals])
    C_ecf_lo   = np.array([C_theta_ECF(t, XI_KZ_LO) for t in theta_vals])
    C_ecf_hi   = np.array([C_theta_ECF(t, XI_KZ_HI) for t in theta_vals])

    # Normalise to C_LCDM at theta=10 deg
    norm = C_lcdm_arr[np.argmin(np.abs(theta_vals - 10))]
    C_lcdm_arr /= norm
    C_ecf_arr  /= norm
    C_ecf_lo   /= norm
    C_ecf_hi   /= norm

    ax.fill_between(theta_vals, C_ecf_lo, C_ecf_hi,
                    alpha=0.20, color=C_ECF, label=r'ECF 1$\sigma$')
    ax.plot(theta_vals, C_lcdm_arr, color=C_LCDM, lw=2.0,
            ls='--', label=r'$\Lambda$CDM')
    ax.plot(theta_vals, C_ecf_arr, color=C_ECF, lw=2.5,
            label=r'ECF ($\xi_{\mathrm{KZ}}=60$ Mpc)')
    ax.axhline(0, color='black', lw=0.8, alpha=0.4)

    # Planck anomaly: C(theta>60) is consistent with zero in data
    ax.axvspan(60, 180, alpha=0.05, color='orange',
               label=r'$C(\theta)$ anomaly region ($\theta>60°$)')
    ax.axvline(60, color='orange', lw=1.2, ls=':', alpha=0.7)
    ax.text(62, ax.get_ylim()[0]*0.6 if ax.get_ylim()[0] < 0 else -0.3,
            r'$60°$', fontsize=9, color='orange')

    ax.set_xlabel(r'Angular separation $\theta$ [deg]', fontsize=11)
    ax.set_ylabel(r'$C(\theta)$ (normalised at $10°$)', fontsize=11)
    ax.set_title(r'Panel D — Angular correlation $C(\theta)$'
                 '\n(best falsifiable test)',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=8.5, loc='upper right')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(5, 175)

    ax.text(0.02, 0.05,
            r'Key test: $C(\theta>60°)\approx 0$ in Planck' '\n'
            r'ECF predicts suppression in this range' '\n'
            r'Measurable with LiteBIRD full-sky',
            transform=ax.transAxes, fontsize=8,
            color='#226633', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', fc='#E8F4E8',
                      ec='#228855', lw=1.5))

    # ── Footer ────────────────────────────────────────────────────────────
    fig.text(0.5, 0.005,
             r'ECF: $\xi_{\mathrm{KZ}}=60$ Mpc (Foundation II) | '
             r'$S_{\mathrm{ECF}}(\ell)=W^2(\ell\,\xi_{\mathrm{KZ}}/\chi_*)$ | '
             'Planck data: Akrami+2020 (arXiv:1906.02552, approx.) | '
             'Anomaly review: Schwarz+2016 (arXiv:1510.07929)',
             ha='center', fontsize=7.5, color='#444444',
             bbox=dict(boxstyle='round,pad=0.25', fc='#F5F5FF',
                       ec='#AAAACC', lw=0.7))

    fig.subplots_adjust(left=0.07, right=0.97, top=0.91,
                        bottom=0.07, hspace=0.38, wspace=0.32)
    fig.savefig(OUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'[OK] -> {OUT_FILE}')


if __name__ == '__main__':
    print('='*65)
    print('ECF Low-ell Suppression — Summary')
    print('='*65)
    print(f'\nxi_KZ = {XI_KZ} Mpc, chi_* = {CHI_STAR} Mpc')
    print(f'\nSuppression S_ECF(l) = W^2(l*xi_KZ/chi_*) = W^2(l/l_KZ):')
    print(f'  {"l":>4}  {"S_ECF":>8}  {"Suppr %":>9}  {"CV sigma":>9}')
    print(f'  {"-"*40}')
    for l in [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50]:
        S = S_ECF(l)
        cv = np.sqrt(2/(2*l+1))
        flag = ' <-- Planck anomaly' if l <= 10 else ''
        print(f'  {l:>4}  {S:>8.4f}  {(1-S)*100:>8.1f}%  '
              f'{cv*100:>8.1f}%{flag}')

    print(f'\nEpistemic status:')
    l_KZ = CHI_STAR / XI_KZ
    print(f'  - l_KZ = chi_*/xi_KZ = {l_KZ:.0f} (true suppression scale)')
    print(f'  - ECF suppresses C_ell at l~233, NOT at l<10')
    print(f'  - Planck low-l anomaly (l<10) is NOT explained by xi_KZ=60Mpc')
    print(f'  - This is an OPEN QUESTION: what explains Planck l<10 anomaly in ECF?')
    print(f'  - Testable at l~233 with ACT/SPT/CMB-S4 (sigma~few %)')
    print(f'  - Requires CLASS-EC for rigorous derivation')
    print()

    make_figure()
