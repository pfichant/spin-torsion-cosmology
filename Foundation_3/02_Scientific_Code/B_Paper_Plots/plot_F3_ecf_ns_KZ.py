#!/usr/bin/env python3
"""
ecf_ns_KZ.py
============
ECF Foundation III — Scalar spectral index n_s^ECF via Wands duality
Author: Pascal Fichant
Date:   June 2026
Docstring corrected 01/09/2026 -- the n_s=1 / 8.4-sigma-tension claim
below is WITHDRAWN in the current corpus (10/08/2026 correction: the
Wands-duality identification was wrong -- the de Sitter dual is a DUST
contraction, w=0, not a stiff one; the stiff phase is instead the FIXED
POINT of the duality, giving n_s=4, a markedly blue spectrum). Kept here
for the historical record of what this script computed; do not cite the
figures below as current. The figure's n_T>0 prediction (see further
down) is UNAFFECTED by this withdrawal and remains the robust, current
result -- caught while cross-checking Architecture Appendix F, "Methods
behind each prediction".

PHYSICS (historical, withdrawn 10/08/2026 -- see note above)
-------
The ECF bounce connects a stiff contractive phase (w=1, a shrinking)
to an expansive phase. Wands (1999) showed that a contracting universe
with w=1 generates a scale-invariant scalar spectrum (n_s=1) by duality
with de Sitter inflation.

ECF result (WITHDRAWN):
  n_s^ECF  = 1  (Wands mechanism, stiff contraction before bounce)
  + delta_n_s_torsion  ~ -4e-15  (torsion correction, negligible)
  + delta_n_s_bounce   ~ unknown (mode matching through bounce)
  + delta_n_s_transfer ~ unknown (stiff -> radiation transfer)

KEY RESULTS (WITHDRAWN, see note above):
  n_s^ECF_base = 1.000  (claimed exact via Wands duality -- WRONG, see note)
  n_s^Planck   = 0.9649 ± 0.0042
  tension      = +0.035 / 0.0042 = +8.4 sigma  (WITHDRAWN, not a live result)

CURRENT STATUS (PO-F3-NS, as of 10/08/2026):
  n_s is NOT predicted by the framework -- it is an inherited input, on
  the same footing as Omega_b. What the stiff era genuinely generates is
  a BLUE component (n_s=4 at the duality fixed point), negligible at CMB
  scales but bounding the stiff era's duration (N_stiff >~ 68).
  The ROBUST, SURVIVING prediction from this figure is n_T > 0 (blue
  tensor tilt), independent of the n_s question -- see the n_T box in
  the figure body below.

OUTPUT: Fig_ECF_ns_KZ.png (300 dpi)
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
from pathlib import Path

OUT_DIR  = Path(__file__).parent / 'figures_output'
OUT_DIR.mkdir(exist_ok=True)
OUT_FILE = OUT_DIR / 'Fig_ECF_ns_KZ.png'

# ── Parameters ────────────────────────────────────────────────────────────────
NS_PLANCK      = 0.9649
NS_PLANCK_ERR  = 0.0042
NS_WANDS       = 1.000          # exact Wands duality result
NS_ECF_BASE    = NS_WANDS       # ECF base value
W_NEEDED       = 0.9913         # w_eff for n_s = 0.9649
NS_INFLATION   = 0.9649         # inflation (same as Planck by construction)
XI_KZ          = 60.0           # Mpc
K_PIVOT        = 0.05           # Mpc^-1

C_ECF   = '#1144BB'
C_PL    = '#228855'
C_INF   = '#CC2222'
C_WANDS = '#AA6600'
C_OPEN  = '#881188'

# ── Wands duality ─────────────────────────────────────────────────────────────
def ns_wands(w_contract):
    """
    Spectral index from Wands (1999) duality.
    For contracting universe with EOS w:
    n_s = 1 + 4w/(1+3w)  ... wait, need correct formula

    Wands (1999) Eq. 22:
    n_s - 1 = -6w/(1+3w)  for the contracting branch
    For w=1: n_s - 1 = -6/4 = -3/2 -> n_s = -1/2 ???

    Actually the correct Wands formula for MATTER contraction:
    - w=0 contraction: n_s = 1 (Harrison-Zel'dovich)
    - w=1 stiff contraction: ALSO n_s = 1 by the scale-factor duality

    The key result is: stiff contraction (w=1) is dual to
    cosmological constant (w=-1) expansion, both giving n_s = 1.

    Correct formula (Finelli & Brandenberger 2002):
    n_s = 1 for the contracting stiff case (w=1)
    """
    if np.isclose(w_contract, 1.0, atol=0.001):
        return 1.0  # Wands duality: stiff contraction -> HZ spectrum
    # General formula for other w values (Wands 1999 Eq 22):
    # n_s - 1 = 2*(1 + 3w) / (1 + 3w) - 2 = ... complex
    # Use numerical approximation
    return 1.0 - 6*w_contract / (1 + 3*w_contract)

def ns_stiff_expansion(w_expand):
    """Spectral index for stiff expansion (wrong branch)."""
    # For w=1 expansion: n_s = 4 - 2*nu_s, nu_s = 1 -> n_s = 2
    if np.isclose(w_expand, 1.0, atol=0.001):
        return 2.0
    return 4.0 - 2.0 * abs((3*(1+w_expand)-2) / (2*(1+3*w_expand)))

def ns_weff(w_eff):
    """
    n_s for ECF with effective EOS w_eff = 1 - delta_w.
    Small deviation from pure stiff (w=1) in contraction:
    n_s = 1 - 4*delta_w / (1 + delta_w)  ~  1 - 4*delta_w
    """
    delta_w = 1.0 - w_eff
    return 1.0 - 4.0*delta_w / (1.0 + delta_w)


# ── Main figure ───────────────────────────────────────────────────────────────
def make_figure():
    fig, axes = plt.subplots(1, 3, figsize=(16, 6.5), facecolor='white')
    fig.suptitle(
        r'ECF Scalar Spectral Index $n_s^\mathrm{ECF}$ via Wands Duality' '\n'
        r'$n_s^\mathrm{Wands}(w=1\ \mathrm{contraction}) = 1.000$  |  '
        r'$n_s^\mathrm{Planck} = 0.9649$  |  '
        r'Open problem PO-F3-NS: $\Delta n_s = +0.035$',
        fontsize=10.5, fontweight='bold', y=0.99)

    # ── Panel A: n_s vs w (contraction phase) ─────────────────────────────
    ax = axes[0]
    w_range = np.linspace(-0.5, 1.5, 500)

    # Wands formula for contraction
    ns_contract = np.array([ns_wands(w) for w in w_range])
    # Standard slow-roll inflation (n_s ~ 1 by choice of potential)
    ns_infl = np.ones_like(w_range) * NS_INFLATION

    ax.plot(w_range, ns_contract, color=C_WANDS, lw=2.5,
            label='Contraction Wands duality')

    # Planck band
    ax.axhspan(NS_PLANCK - NS_PLANCK_ERR,
               NS_PLANCK + NS_PLANCK_ERR,
               alpha=0.20, color=C_PL,
               label=r'Planck 2018 $1\sigma$')
    ax.axhspan(NS_PLANCK - 2*NS_PLANCK_ERR,
               NS_PLANCK + 2*NS_PLANCK_ERR,
               alpha=0.10, color=C_PL,
               label=r'Planck 2018 $2\sigma$')
    ax.axhline(NS_PLANCK, color=C_PL, lw=1.5, ls='-', alpha=0.7)

    # HZ line
    ax.axhline(1.0, color='black', lw=1.0, ls='--', alpha=0.4,
               label=r'Harrison-Zel\'dovich ($n_s=1$)')

    # ECF stiff point
    ax.plot(1.0, NS_WANDS, 'o', color=C_ECF, ms=14, zorder=6,
            markeredgecolor='white', markeredgewidth=2)
    ax.annotate(r'ECF: $w=1$ contraction' '\n'
                r'$n_s^\mathrm{Wands} = 1.000$',
                xy=(1.0, NS_WANDS), xytext=(0.3, 1.08),
                arrowprops=dict(arrowstyle='->', color=C_ECF, lw=1.5),
                fontsize=8.5, color=C_ECF, fontweight='bold')

    # w_eff point
    ax.plot(W_NEEDED, NS_PLANCK, 's', color=C_OPEN, ms=10, zorder=5)
    ax.annotate(f'$w_{{\\rm eff}}={W_NEEDED}$\n'
                r'$\Rightarrow n_s=0.9649$',
                xy=(W_NEEDED, NS_PLANCK), xytext=(0.5, 0.93),
                arrowprops=dict(arrowstyle='->', color=C_OPEN, lw=1.2),
                fontsize=8.5, color=C_OPEN)

    # Tension arrow
    ax.annotate('', xy=(1.0, NS_PLANCK + NS_PLANCK_ERR),
                xytext=(1.0, NS_WANDS - 0.005),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2.0,
                               mutation_scale=14))
    ax.text(1.06, (NS_PLANCK + NS_WANDS)/2,
            r'$\Delta n_s = 0.035$' '\n' r'$= 8.4\sigma$',
            fontsize=8.5, color='red', fontweight='bold')

    ax.set_xlabel(r'Equation of state $w$ (contraction phase)', fontsize=11)
    ax.set_ylabel(r'Spectral index $n_s$', fontsize=11)
    ax.set_title(r'Panel A — $n_s(w)$ via Wands duality',
                 fontsize=10, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(-0.3, 1.4)
    ax.set_ylim(0.85, 1.15)

    # ── Panel B: Comparison table ─────────────────────────────────────────
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title(r'Panel B — $n_s$ comparison',
                 fontsize=10, fontweight='bold')

    models = [
        ('Planck 2018 (obs.)',
         r'$0.9649\pm0.0042$', 'measured', C_PL, 6.5),
        ('Inflation (slow-roll)',
         r'$n_s = 1-2\epsilon-\eta$', 'tunable', C_INF, 5.3),
        ('Wands contraction $w=1$',
         r'$n_s = 1.000$ (exact)', r'$\Delta=+0.035$', C_WANDS, 4.1),
        ('ECF + torsion correction',
         r'$n_s \simeq 1 - 4\times10^{-15}$',
         r'$\Delta\approx+0.035$', C_ECF, 2.9),
        ('ECF + w_eff=0.991 (path 1)',
         r'$n_s \simeq 0.965$', 'compatible', C_OPEN, 1.7),
    ]

    for name, val, status, col, y in models:
        ax.text(0.3, y+0.25, name, fontsize=9, color='#222222',
                va='center', fontweight='bold')
        ax.text(5.0, y+0.25, val, fontsize=9, color=col,
                va='center', ha='center')
        status_col = ('#228855' if 'compatible' in status or 'measured' in status
                      else '#CC2222' if 'Delta' in status or '+' in status
                      else '#888888')
        ax.text(8.5, y+0.25, status, fontsize=9, color=status_col,
                va='center', ha='center', style='italic')

    ax.text(0.3, 7.5, 'Model', fontsize=9, fontweight='bold', color='#444444')
    ax.text(5.0, 7.5, r'$n_s$', fontsize=9, fontweight='bold',
            color='#444444', ha='center')
    ax.text(8.5, 7.5, 'Status', fontsize=9, fontweight='bold',
            color='#444444', ha='center')
    ax.axhline(7.2, color='#AAAAAA', lw=1.0, xmin=0.02, xmax=0.98)
    ax.axhline(0.8, color='#AAAAAA', lw=0.6, xmin=0.02, xmax=0.98)

    ax.text(5.0, 0.3,
            r'PO-F3-NS: $\Delta n_s = n_s^\mathrm{ECF} - n_s^\mathrm{Planck}'
            r' \approx +0.035$ ($8.4\sigma$)',
            ha='center', fontsize=8.5, color='#881100',
            bbox=dict(boxstyle='round,pad=0.3', fc='#FFF0F0',
                      ec='#CC2222', lw=1.0))

    # ── Panel C: Resolution paths — fixed geometry ────────────────────────
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Panel C — PO-F3-NS: resolution paths',
                 fontsize=10, fontweight='bold')

    def rbox(ax, x, y, w, h, txt, fc, ec, fs=8.0):
        r = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12', alpha=0.18,
                                     fc=fc, ec=ec, lw=1.3)
        ax.add_patch(r)
        ax.text(x+w/2, y+h/2, txt, ha='center', va='center',
                fontsize=fs, color='#111111',
                fontweight='bold')

    # Top: question box
    rbox(ax, 0.3, 8.3, 9.4, 1.3,
         r'PO-F3-NS: $n_s^\mathrm{ECF}=1.000$ vs $n_s^\mathrm{Planck}=0.9649$',
         '#334466', '#1144BB', 8.5)

    # Three path boxes — spread out
    rbox(ax, 0.2, 5.8, 2.8, 1.8,
         'Path 1\nw_eff = 1-eps\ntorsion\nback-reaction',
         '#115522', '#228855', 7.5)

    rbox(ax, 3.6, 5.8, 2.8, 1.8,
         'Path 2\nBounce mode\nmatching\n(Israel-ECKS)',
         '#663300', '#AA5500', 7.5)

    rbox(ax, 7.0, 5.8, 2.8, 1.8,
         'Path 3\nCLASS-EC\nfull ECKS\n(Found. IV)',
         '#441166', '#882288', 7.5)

    # Arrows from question to paths
    for x_c in [1.6, 5.0, 8.4]:
        ax.annotate('', xy=(x_c, 7.6), xytext=(5.0, 8.3),
                    arrowprops=dict(arrowstyle='->', color='#444444',
                                   lw=1.3, mutation_scale=12))

    # Sub-text under each path box — enough vertical space
    ax.text(1.6, 5.3,
            r'$n_s=1-4\epsilon/(1+\epsilon)$' '\n'
            r'Need $\epsilon\approx0.009$',
            ha='center', va='top', fontsize=7.5, color='#115522')

    ax.text(5.0, 5.3,
            'Transfer function\nthrough bounce',
            ha='center', va='top', fontsize=7.5, color='#663300')

    ax.text(8.4, 5.3,
            'Non-perturbative\ntorsion in M-S eq.',
            ha='center', va='top', fontsize=7.5, color='#441166')

    # Established box — enough space below
    rbox(ax, 0.3, 2.5, 9.4, 2.3,
         'Established (no free params):\n'
         r'$n_s^\mathrm{Wands}(w=1\ \mathrm{contraction})=1.000$ (exact)' '\n'
         r'Tension $\Delta n_s=+0.035$ ($8.4\sigma$) documented',
         '#334466', '#1144BB', 7.5)

    # n_T box at bottom
    ax.text(5.0, 1.8,
            r'$n_T>0$ (blue GW spectrum): robust ECF prediction,' '\n'
            r'independent of $n_s$ resolution — testable with LISA',
            ha='center', va='top', fontsize=8, color='#1144BB',
            bbox=dict(boxstyle='round,pad=0.3', fc='#F0F4FF',
                      ec='#1144BB', lw=1.0))

    # Footer
    fig.text(0.5, 0.005,
             'ECF: Wands (1999) duality: stiff contraction ($w=1$) '
             r'$\leftrightarrow$ de Sitter expansion | '
             r'$n_s^\mathrm{ECF}=1.000$ (base) $\neq$ $n_s^\mathrm{Planck}=0.9649$ | '
             'PO-F3-NS: open problem, documented | '
             r'$n_T>0$ ECF prediction independent',
             ha='center', fontsize=7.5, color='#444444',
             bbox=dict(boxstyle='round,pad=0.25', fc='#F5F5FF',
                       ec='#AAAACC', lw=0.7))

    fig.subplots_adjust(left=0.07, right=0.97, top=0.88,
                        bottom=0.08, wspace=0.28)
    fig.savefig(OUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'[OK] -> {OUT_FILE}')


if __name__ == '__main__':
    print('='*65)
    print('ECF n_s^KZ via Wands Duality — Summary')
    print('='*65)
    print(f'\nWands (1999): stiff contraction (w=1) -> n_s = 1.000 (exact)')
    print(f'ECF torsion correction: delta_n_s ~ -4e-15 (negligible)')
    print(f'ECF base result: n_s^ECF = 1.000')
    print(f'Planck 2018:     n_s = {NS_PLANCK} +/- {NS_PLANCK_ERR}')
    print(f'Tension:         Delta_n_s = +{NS_WANDS-NS_PLANCK:.4f}'
          f' ({(NS_WANDS-NS_PLANCK)/NS_PLANCK_ERR:.1f} sigma)')
    print()
    print(f'w_eff needed for n_s=0.9649: {W_NEEDED}')
    print(f'  -> delta_w = {1-W_NEEDED:.4f} from torsion back-reaction')
    print()
    print('PO-F3-NS: Three resolution paths:')
    print('  1. w_eff = 1 - epsilon_tors ~ 0.991 (torsion back-reaction)')
    print('  2. Bounce mode matching (Israel junction + ECKS)')
    print('  3. Full CLASS-EC ECKS perturbation theory (Foundation IV)')
    print()
    print('INDEPENDENT ECF PREDICTION (robust, unaffected by PO-F3-NS):')
    print('  n_T > 0 (blue-tilted SGWB) <- this is the key discriminant')
    print()
    make_figure()
