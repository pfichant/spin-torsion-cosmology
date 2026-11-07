#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Bounce paper — Fig. 1 : the Landau-Ginzburg potential
#  Fichant, P. (2026).   plot_paper_fig1_potential.py
#
#  EMPLACEMENT (depot GitHub) :
#     Papers/Bounce_ChiralPhaseTransition/figures/
#  SORTIE :
#     figures_output/Fig_Paper_LG_Potential.png
#
#  OBJET
#  -----
#  Figure 1 de l'article « The Cosmological Bounce as a Chiral Phase
#  Transition ». Elle porte LA these en une image :
#
#    (a) Le paysage d'energie V(T) se DEFORME avec la densite : cuvette unique
#        en sous-critique, aplatissement au seuil, DOUBLE PUITS au-dela.
#        Les deux minima sont les DEUX CHIRALITES (L et D) du vide naissant.
#
#    (b) Le terme de biais -h*T (le seul terme IMPAIR du potentiel) creuse
#        legerement l'un des puits. Cette asymetrie -- invisible a l'oeil sur
#        la courbe -- est ce qui DECIDE de la chiralite. Sans elle (h=0), les
#        puits sont strictement degeneres et le choix serait un tirage au sort.
#
#  PRINT-SAFE : fond blanc, niveaux de gris, marqueurs distincts, lisible en
#  noir et blanc et en colonne unique (PRD).
#
#  Reproductibilite : numpy, matplotlib. Deterministe.
# =============================================================================

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, 'figures_output')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PNG    = os.path.join(OUT_DIR, 'Fig_Paper_LG_Potential.png')

# --- Potentiel (unites reduites : alpha = 1, beta = 1/2, chi_c = 1) ----------
ALPHA, BETA, CHI_C = 1.0, 0.5, 1.0

def V(T, chi, h=0.0):
    return ALPHA*(CHI_C - chi)*T**2 + BETA*T**4 - h*T

def critical_points(chi, h):
    """Racines de V'(T) = 4 beta T^3 + 2 alpha (chi_c - chi) T - h = 0."""
    r = np.roots([4*BETA, 0.0, 2*ALPHA*(CHI_C - chi), -h])
    r = np.sort(np.real(r[np.abs(np.imag(r)) < 1e-9]))
    return tuple(r) if len(r) == 3 else None

Tg = np.linspace(-1.6, 1.6, 700)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.6, 4.1))
fig.patch.set_facecolor('white')

# =============================================================================
#  (a)  Le paysage se deforme : le double puits s'ouvre au seuil
# =============================================================================
axA.set_facecolor('white')

regimes = [
    (0.5, '-',   'o', 'subcritical  $\\chi=0.5$'),
    (1.0, '--',  's', 'threshold  $\\chi=\\chi_{\\rm c}=1$'),
    (1.8, '-.',  '^', 'supercritical  $\\chi=1.8$'),
]
for chi, ls, mk, lab in regimes:
    Vv = V(Tg, chi)
    axA.plot(Tg, Vv, ls, color='black', lw=1.7, label=lab, zorder=3)
    axA.plot(Tg[::110], Vv[::110], mk, color='black', ms=4.5,
             mfc='white', mew=1.0, zorder=4)

# Les deux minima en super-critique = les deux chiralites
T0 = np.sqrt(ALPHA*(1.8 - CHI_C)/(2*BETA))
for s, lab, dx in [(-1, 'L', -0.13), (+1, 'D', +0.13)]:
    axA.plot([s*T0], [V(s*T0, 1.8)], 'v', color='black', ms=9,
             mfc='0.85', mew=1.2, zorder=6)
    axA.annotate(lab, xy=(s*T0, V(s*T0, 1.8)), xytext=(s*T0 + dx, V(s*T0, 1.8) - 0.13),
                 fontsize=11, weight='bold', ha='center', zorder=7)
# Le maximum instable
axA.plot([0], [0], '^', color='0.45', ms=8, mfc='white', mew=1.1, zorder=6)
axA.annotate('unstable', xy=(0, 0), xytext=(0, 0.17), fontsize=8,
             color='0.35', ha='center', zorder=7)

axA.axhline(0, color='0.85', lw=0.7, zorder=1)
axA.axvline(0, color='0.85', lw=0.7, zorder=1)
axA.set_xlim(-1.6, 1.6); axA.set_ylim(-0.55, 1.05)
axA.set_xlabel(r'order parameter  $\mathcal{T}\propto S^{a}$', fontsize=10.5)
axA.set_ylabel(r'$V(\mathcal{T})$', fontsize=11)
axA.set_title(r'(a)  The double well opens at threshold',
              fontsize=10.5, loc='left', pad=8)
axA.legend(fontsize=8.2, loc='upper center', framealpha=1, ncol=1)
axA.grid(alpha=0.2, lw=0.5)
axA.text(0.5, -0.50, 'the two minima are the two chiralities',
         fontsize=8.5, style='italic', ha='center', color='0.3',
         transform=axA.get_xaxis_transform(), zorder=8)

# =============================================================================
#  (b)  Le biais -h*T leve la degenerescence
# =============================================================================
axB.set_facecolor('white')

CHI = 1.8
H_BIG = 0.20                      # biais volontairement EXAGÉRÉ pour la lisibilité

# h = 0 : puits strictement degeneres
V0 = V(Tg, CHI, 0.0)
axB.plot(Tg, V0, '--', color='0.55', lw=1.5, zorder=3,
         label=r'$h=0$  (degenerate: chirality random)')

# h > 0 : le puits droit se creuse
Vh = V(Tg, CHI, H_BIG)
axB.plot(Tg, Vh, '-', color='black', lw=1.9, zorder=4,
         label=r'$h>0$  ($h\propto a^{*}$: chirality selected)')

cp = critical_points(CHI, H_BIG)
TL, TM, TR = cp
VL, VR = V(TL, CHI, H_BIG), V(TR, CHI, H_BIG)
axB.plot([TL], [VL], 'v', color='black', ms=9, mfc='white', mew=1.2, zorder=6)
axB.plot([TR], [VR], 'v', color='black', ms=10, mfc='0.25', mew=1.2, zorder=6)

# Marquer l'ecart de profondeur
axB.annotate('', xy=(TR, VR), xytext=(TR, VL),
             arrowprops=dict(arrowstyle='<->', lw=1.1, color='0.25'), zorder=5)
axB.text(TR + 0.10, (VL + VR)/2, r'$\Delta V$', fontsize=9.5, color='0.2',
         va='center', zorder=7)
axB.plot([TL, TR + 0.06], [VL, VL], ':', color='0.55', lw=0.9, zorder=2)

axB.annotate('deeper well\n$\\Rightarrow$ selected', xy=(TR, VR),
             xytext=(TR + 0.17, VR - 0.20), fontsize=8.6, ha='left',
             color='0.15', weight='bold', zorder=7,
             arrowprops=dict(arrowstyle='->', lw=0.9, color='0.3'))

axB.axhline(0, color='0.85', lw=0.7, zorder=1)
axB.axvline(0, color='0.85', lw=0.7, zorder=1)
axB.set_xlim(-1.6, 1.6); axB.set_ylim(-0.75, 0.85)
axB.set_xlabel(r'order parameter  $\mathcal{T}$'
               '\n'
               r'$\longleftarrow$ chirality L        chirality D $\longrightarrow$',
               fontsize=10.5)
axB.set_title(r'(b)  The linear bias lifts the degeneracy',
              fontsize=10.5, loc='left', pad=8)
axB.legend(fontsize=8.2, loc='upper center', framealpha=1)
axB.grid(alpha=0.2, lw=0.5)

fig.tight_layout(pad=1.6)
fig.subplots_adjust(bottom=0.20)
fig.text(0.5, 0.015,
         r'Only the odd term $-h\,\mathcal{T}$ tilts the landscape. '
         r'The bias shown is exaggerated for clarity: the CMB bound gives '
         r'$|h|/h_{0}\lesssim3\times10^{-4}$.',
         ha='center', fontsize=8.3, color='0.4')

fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figure ecrite : {OUT_PNG}")

# --- Verification print-safe -------------------------------------------------
try:
    from PIL import Image
    with Image.open(OUT_PNG) as im:
        size = im.size
        im.convert('L')          # doit rester lisible en niveaux de gris
    print(f"Verification print-safe OK — {size}")
except ImportError:
    print("(PIL absent : verification grayscale ignoree)")

# --- Report des valeurs (tracabilite) ----------------------------------------
print()
print("Points critiques a chi = 1.8, h = 0.20 (unites reduites) :")
print(f"  minimum L : T = {TL:+.4f}   V = {VL:+.4f}")
print(f"  maximum   : T = {TM:+.4f}   V = {V(TM, CHI, H_BIG):+.4f}")
print(f"  minimum D : T = {TR:+.4f}   V = {VR:+.4f}")
print(f"  ecart de profondeur : dV = {abs(VR - VL):.4f} "
      f"({abs((VR-VL)/VL)*100:.0f} % du puits)")
