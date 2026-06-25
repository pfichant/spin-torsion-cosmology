
#!/usr/bin/env python3
"""
plot_gamma_z.py  — ECF Foundation II
────────────────────────────────────────────────────────────────────────────
Figure : Knot collision-rate evolution Γ(z)

Physical model
──────────────
  Γ(z) = Γ⁽⁰⁾ (1+z)^{3/2}

Two populations :
  • Micro-Knots : M ~ 10²⁴ kg, z_EW  ~ 1.5×10¹¹
  • Macro-Knots : M ~ 10⁵ M☉, z_QGP ~ 5×10¹¹

Present-day rates (ECF Foundation I) :
  Γ_μ⁽⁰⁾ ≈ 5×10⁻³⁹ s⁻¹
  Γ_M⁽⁰⁾ ≈ 1×10⁻²⁰ s⁻¹

Usage
─────
  python plot_gamma_z.py [--output fig_Gamma_z.png] [--dpi 300]

Author  : Pierre Fichant — CC BY 4.0
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

parser = argparse.ArgumentParser()
parser.add_argument('--output', default='fig_Gamma_z.png')
parser.add_argument('--dpi',    type=int, default=300)
args = parser.parse_args()

# ── Palette publication fond blanc ────────────────────────────────
BG      = 'white'
FG      = '#1a1a2e'
GR      = '#d0d4dd'
C_MICRO = '#1565c0'
C_MACRO = '#e65100'

LEGEND_KW = dict(
    facecolor='#f5f5f5', edgecolor='#aaaaaa',
    framealpha=0.97, labelcolor=FG, fontsize=10,
)

# ── Paramètres physiques ──────────────────────────────────────────
Gamma0_micro = 5e-39
Gamma0_macro = 1e-20
z_EW         = 1.5e11
z_QCD        = 5e11

z            = np.logspace(-1, 12.3, 4000)
Gamma_micro  = Gamma0_micro * (1 + z)**1.5
Gamma_macro  = Gamma0_macro * (1 + z)**1.5

# ── Figure ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6.5))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

ax.tick_params(which='both', direction='in', length=5, width=0.8,
               labelsize=10, colors=FG, top=True, right=True)
ax.tick_params(which='minor', length=3)
for sp in ax.spines.values():
    sp.set_edgecolor('#888'); sp.set_linewidth(0.8)
ax.grid(True, which='major', color=GR, lw=0.7, zorder=0)
ax.grid(True, which='minor', color=GR, lw=0.3, alpha=0.6, zorder=0)

ax.axvspan(1+z_EW*0.6,  1+z_EW*1.7,  alpha=0.07, color=C_MICRO, zorder=1)
ax.axvspan(1+z_QCD*0.6, 1+z_QCD*1.7, alpha=0.07, color=C_MACRO, zorder=1)
ax.axvline(1+z_EW,  color=C_MICRO, lw=1.2, ls=':', alpha=0.85, zorder=4)
ax.axvline(1+z_QCD, color=C_MACRO, lw=1.2, ls=':', alpha=0.85, zorder=4)

ax.loglog(1+z, Gamma_micro, color=C_MICRO, lw=2.5, zorder=5,
          label=r'Micro-Knot  $\Gamma_\mu(z)$  [$M\sim10^{24}$ kg]')
ax.loglog(1+z, Gamma_macro, color=C_MACRO, lw=2.5, zorder=5, ls='--',
          label=r'Macro-Knot  $\Gamma_M(z)$  [$M\sim10^5\,M_\odot$]')

ax.text(1+z_EW, 1e15,
        r'EW freeze-out'+'\n'+r'$z_{\rm EW}\!\sim\!1.5\!\times\!10^{11}$',
        color=C_MICRO, fontsize=8.5, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#eef4ff', ec=C_MICRO, alpha=0.92))
ax.text(1+z_QCD, 1e15,
        r'QCD/QGP'+'\n'+r'$z_{\rm QGP}\!\sim\!5\!\times\!10^{11}$',
        color=C_MACRO, fontsize=8.5, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#fff4ee', ec=C_MACRO, alpha=0.92))

z_sl = 3e7
idx  = np.argmin(np.abs(z - z_sl))
ax.text(1+z_sl*2.5, Gamma_micro[idx]*30, r'$\Gamma\propto(1+z)^{3/2}$',
        color=FG, fontsize=11, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', fc='#f5f5f5', ec=GR, alpha=0.92))

ax.axvline(1, color='#aaa', lw=0.8, ls='--', alpha=0.6)
ax.text(1.08, Gamma0_micro*5, 'today', color='#888', fontsize=8.5)

ax.set_xlim(0.9, 2e12); ax.set_ylim(1e-42, 1e18)
ax.set_xlabel(r'$1 + z$', fontsize=13, color=FG, labelpad=6)
ax.set_ylabel(r'Collision rate  $\Gamma\;[\mathrm{s}^{-1}]$', fontsize=13, color=FG, labelpad=6)
ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatterSciNotation())

ax.legend(**LEGEND_KW, loc='lower right', borderpad=0.8, handlelength=2.4)

fig.suptitle(r'Knot collision rate $\Gamma(z) = \Gamma^{(0)}\,(1+z)^{3/2}$ — ECF Foundation II',
             fontsize=13, fontweight='bold', color=FG, y=1.01)
ax.set_title(r'Micro-Knots crystallise at EW epoch; Macro-Knots form at QCD transition',
             fontsize=10, color='#666', pad=6)

plt.tight_layout()
import os as _os
_SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))

def _find_figs_dir(start):
    """Remonte l'arborescence pour trouver figures_output/."""
    d = start
    for _ in range(5):
        candidate = _os.path.join(d, "figures_output")
        if _os.path.isdir(candidate):
            return candidate
        parent = _os.path.dirname(d)
        if parent == d:
            break
        d = parent
    # Not found: create it next to script
    fallback = _os.path.join(_os.path.dirname(_SCRIPT_DIR), "figures_output")
    _os.makedirs(fallback, exist_ok=True)
    return fallback

_FIGS_DIR = _find_figs_dir(_SCRIPT_DIR)
# Make output path absolute so it works regardless of cwd
if not _os.path.isabs(args.output):
    args.output = _os.path.normpath(_os.path.join(_FIGS_DIR, args.output))

plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight', facecolor=BG)
plt.close()
print(f"[OK] {args.output}  (dpi={args.dpi})")

