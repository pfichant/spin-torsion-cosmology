#!/usr/bin/env python3
"""
plot_F3_ecf_wkb_ecks.py
Potentiel WKB Wheeler-DeWitt ECKS (Foundation III §PO-F3-ISO)
Forme correcte : U_FRW(a) = a^2 - Lambda/3 * a^4 (Hartle-Hawking classique)
              U_ECKS(a) = a^2 - Lambda/3 * a^4 + alpha/a^2  (+ torsion)
              U_Bianchi = U_ECKS + beta^2/a^2 (+ anisotropie)
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
from scipy.integrate import quad
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings; warnings.filterwarnings('ignore')

# Paramètres (adimensionnels — a en unités de l_Pl, Lambda redimensionné)
LAMBDA = 1.0     # Lambda * l_Pl^2 (unités réduites)
ALPHA  = 0.05    # couplage torsion ECF (alpha = kappa^2 * s^2 * l_Pl^4)
BETA2  = 0.08    # amplitude anisotropie Bianchi (beta+^2 + beta-^2)

# Potentiels
def U_GR(a):
    return a**2 - (LAMBDA/3.)*a**4

def U_ECKS(a):
    if a < 1e-6: return 1e9
    return a**2 - (LAMBDA/3.)*a**4 + ALPHA/a**2

def U_BIANCHI(a):
    if a < 1e-6: return 1e9
    return U_ECKS(a) + BETA2/a**2

# Points remarquables
a_star_GR = float(np.sqrt(3./LAMBDA))  # zero de U_GR : a* = sqrt(3/Lambda)

# Zero de U_ECKS (> a_star_GR car torsion eleve U)
try:
    a_star_ECKS = brentq(U_ECKS, a_star_GR, 3.*a_star_GR)
except:
    a_star_ECKS = a_star_GR * 1.05

# Zero de U_Bianchi (encore plus grand)
try:
    a_star_BIANCHI = brentq(U_BIANCHI, a_star_ECKS, 4.*a_star_GR)
except:
    a_star_BIANCHI = a_star_ECKS * 1.05

# Maximum de U_GR (dU/da = 2a - 4*Lambda/3 * a^3 = 0 => a_max = sqrt(3/2Lambda))
a_max_GR = float(np.sqrt(3./(2.*LAMBDA)))
a_max_ECKS = a_max_GR  # approx (torsion negligible at moderate a)

# Actions WKB : S_E = integral_0^{a_*} sqrt(U) da (dans la zone U > 0)
def S_WKB(U_func, a_star):
    """WKB integral over the classically forbidden region (U > 0)."""
    eps  = 1e-3
    def integrand(a):
        U = U_func(a)
        return np.sqrt(max(U, 0.)) if U > 0 else 0.
    result, _ = quad(integrand, eps, a_star, limit=200, epsabs=1e-6)
    return result

S_GR    = S_WKB(U_GR,    a_star_GR)
S_ECKS  = S_WKB(U_ECKS,  a_star_ECKS)
S_BIANCHI = S_WKB(U_BIANCHI, a_star_BIANCHI)

print("="*55)
print("RESULTATS WKB ECKS")
print("="*55)
print(f"  a_star (GR)     = {a_star_GR:.4f}")
print(f"  a_star (ECKS)   = {a_star_ECKS:.4f}  (+{(a_star_ECKS-a_star_GR)/a_star_GR*100:.1f}%)")
print(f"  a_star (Bianchi)= {a_star_BIANCHI:.4f}  (+{(a_star_BIANCHI-a_star_GR)/a_star_GR*100:.1f}%)")
print(f"  S_E (GR)        = {S_GR:.5f}")
print(f"  S_E (ECKS)      = {S_ECKS:.5f}  (delta = {S_ECKS-S_GR:+.5f})")
print(f"  S_E (Bianchi)   = {S_BIANCHI:.5f}  (delta vs FRW = {S_BIANCHI-S_ECKS:+.5f})")
print()
print("  Hartle-Hawking P (prop) exp(+2 S_E):")   # 15/10/2026 : libelle etait exp(+S_E), calcul inchange
print(f"    P_HH(ECKS)/P_HH(GR)      = exp({2*(S_ECKS-S_GR):+.3f}) = {np.exp(2*(S_ECKS-S_GR)):.3f}")
print(f"    P_HH(Bianchi)/P_HH(FRW)  = exp({2*(S_BIANCHI-S_ECKS):+.3f}) = {np.exp(2*(S_BIANCHI-S_ECKS)):.3f}")
print()
print("  Vilenkin P (prop) exp(-2 S_E):")   # 15/10/2026 : libelle etait exp(-S_E), calcul inchange
print(f"    P_V(ECKS)/P_V(GR)         = exp({-2*(S_ECKS-S_GR):+.3f}) = {np.exp(-2*(S_ECKS-S_GR)):.3f}")
print(f"    P_V(Bianchi)/P_V(FRW)     = exp({-2*(S_BIANCHI-S_ECKS):+.3f}) = {np.exp(-2*(S_BIANCHI-S_ECKS)):.3f}")
print("  => Vilenkin SUPPRESSES anisotropic geometries (Bianchi).")

# ── Figure ───────────────────────────────────────────────────────────────
a_arr = np.linspace(0.02, 2.3*a_star_GR, 800)
U_GR_arr = np.array([U_GR(a) for a in a_arr])
U_ECKS_arr = np.array([U_ECKS(a) for a in a_arr])
U_B_arr    = np.array([U_BIANCHI(a) for a in a_arr])

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), facecolor='white')
fig.suptitle(
    r"WKB analysis: $U_{\rm ECKS}(a) = a^2 - \frac{\Lambda}{3}a^4 + \frac{\alpha}{a^2}$"
    " — Foundation III §PO-F3-ISO\n"
    r"(reduced units $[a]=l_{\rm Pl}$, illustrative parameters)",
    fontsize=10.5, fontweight='bold')

# Panel gauche : potentiels
ax = axes[0]
clip = 0.8
ax.plot(a_arr, np.clip(U_GR_arr, -clip, clip), 'k--', lw=1.8, label=r'$U_{\rm GR}$ (no torsion)')
ax.plot(a_arr, np.clip(U_ECKS_arr, -clip, clip), 'r-', lw=2.5, label=r'$U_{\rm ECKS}$ (+ torsion $\alpha/a^2$)')
ax.plot(a_arr, np.clip(U_B_arr, -clip, clip), 'b:', lw=2.0, label=r'$U_{\rm Bianchi}$ (+ anisotropy $\beta_\pm$)')
ax.axhline(0., c='gray', lw=0.8)

# Remplissage zones
ax.fill_betweenx([-clip, clip], 0., a_star_GR,   color='#FFBB44', alpha=0.15)
ax.fill_betweenx([-clip, clip], a_star_GR, 2.3*a_star_GR, color='#88AAEE', alpha=0.15)

# Marqueurs
label_offsets = [
    (a_star_GR,      '#444444', r'$a_*^{\rm GR}$',      'right', -0.02),
    (a_star_ECKS,    '#CC2222', r'$a_*^{\rm ECKS}$',    'left',   0.10),
    (a_star_BIANCHI, '#2244CC', r'$a_*^{\rm Bianchi}$', 'left',   0.22),
]
for a_v, c, lbl, ha, y_off in label_offsets:
    ls = '--' if c == '#444444' else '-.'
    ax.axvline(a_v, c=c, lw=1.2, ls=ls)
    y_lbl = -clip + 0.06 + y_off
    x_lbl = a_v - 0.03 if ha == 'right' else a_v + 0.03
    ax.annotate(lbl, xy=(a_v, -clip + 0.06), xytext=(x_lbl, y_lbl),
                ha=ha, va='center', fontsize=7.5, color=c,
                arrowprops=dict(arrowstyle='-', color=c, lw=0.6,
                                 shrinkA=0, shrinkB=2))

ax.text(a_star_GR/2., 0.15, 'Tunnelling\nregion', ha='center', fontsize=9,
        color='#884400', fontweight='bold')
ax.text(a_star_GR*1.4, -0.35, 'Classical\nregion\n(de Sitter)', ha='center',
        fontsize=9, color='#224488', fontweight='bold')

ax.set_xlabel(r"Scale factor $a$ (units of $l_{\rm Pl}$)", fontsize=11)
ax.set_ylabel(r'$U_{\rm ECKS}(a)$ [Planck units]', fontsize=10)
ax.set_title("WdW potential — effect of torsion and anisotropy", fontsize=10)
ax.legend(fontsize=8, loc='lower right')
ax.set_xlim(0., 2.3*a_star_GR); ax.set_ylim(-clip, clip)
ax.grid(True, alpha=0.2)

# -- Inset : mur intérieur ECF (zoom petit a) --
axins = ax.inset_axes([0.44, 0.46, 0.53, 0.44])
a_ins = np.linspace(0.04, 0.65, 400)
axins.plot(a_ins, np.clip([U_GR(a)      for a in a_ins], -0.1, 9.), 'k--', lw=1.5, label='GR')
axins.plot(a_ins, np.clip([U_ECKS(a)    for a in a_ins], -0.1, 9.), 'r-',  lw=2.0, label='ECKS')
axins.plot(a_ins, np.clip([U_BIANCHI(a) for a in a_ins], -0.1, 9.), 'b:',  lw=1.8, label='Bianchi')
axins.axhline(0., c='gray', lw=0.5)
axins.set_xlim(0.04, 0.65); axins.set_ylim(-0.1, 9.)
axins.set_xlabel("$a$ (zoom)", fontsize=7)
axins.set_title("ECF inner wall\n" + r"($\alpha/a^2\!\to\!+\infty$)", fontsize=7.5)
axins.tick_params(labelsize=6)
axins.grid(True, alpha=0.25)
axins.legend(fontsize=6, loc='upper right')
axins.text(0.32, 6.5, r'Torsion $\nearrow$', fontsize=7.5, color='red', ha='center')

# Boîte résumé actions
box_txt = (fr"$S_E^{{\rm GR}} = {S_GR:.3f}$ (exact)" + '\n' +
           fr"$S_E^{{\rm ECKS}} = {S_ECKS:.3f}$ ({S_ECKS-S_GR:+.3f})" + '\n' +
           fr"$S_E^{{\rm Bianchi}} = {S_BIANCHI:.3f}$ ({S_BIANCHI-S_ECKS:+.3f})" + '\n' +
           r"(cutoff $\varepsilon=10^{-3}$, illustrative)")
ax.text(0.02, 0.98, box_txt, transform=ax.transAxes,
        va='top', ha='left', fontsize=7.5,
        bbox=dict(boxstyle='round', fc='#F8F8F0', ec='gray', lw=0.8))

# Panel droit : probabilités HH et Vilenkin
ax2 = axes[1]
beta_arr = np.linspace(0., 0.5, 300)

# Contribution de l'anisotropie à S_E (proportionnelle à beta^2 * I_aniso)
I_aniso, _ = quad(lambda a: 1./(a**2 * np.sqrt(max(U_ECKS(a), 1e-6))),
                  0.05, a_star_ECKS, limit=200)
delta_S_beta = beta_arr**2 * I_aniso

# P_HH ∝ exp(+2 S_E), P_V ∝ exp(-2 S_E)  (P = |Psi|^2 ; corrige 15/10/2026)
# delta_S = S_E^{FRW+beta} - S_E^{FRW} = delta_S_beta
P_HH_ratio = np.exp(+2.*delta_S_beta)  # aniso MORE likely in HH
P_V_ratio  = np.exp(-2.*delta_S_beta)  # aniso LESS likely in Vilenkin

ax2.plot(beta_arr, P_V_ratio,  'r-',  lw=2.5,
         label=r'Vilenkin : $P_V^{\rm aniso}/P_V^{\rm FRW} = e^{-2\Delta S}$')
ax2.plot(beta_arr, P_HH_ratio, 'b--', lw=2.0,
         label=r'Hartle-Hawking : $P_{\rm HH}^{\rm aniso}/P_{\rm HH}^{\rm FRW} = e^{+2\Delta S}$')
ax2.axhline(1., c='k', lw=0.8, ls=':')
ax2.axhline(0.5, c='orange', lw=1., ls=':', label='50% threshold')
ax2.fill_between(beta_arr, P_V_ratio, 1., color='red', alpha=0.12,
                 label='Vilenkin: isotropy favoured')
ax2.fill_between(beta_arr, P_HH_ratio, 1., color='blue', alpha=0.10,
                 label='HH: anisotropy favoured (no-boundary anisotropy problem)')

ax2.annotate(
    'Vilenkin selects\nisotropy\n' +
    fr'(conjecture F3-ISO-WdW)',
    xy=(0.25, np.exp(-2.*0.25**2*I_aniso)),
    xytext=(0.30, 0.30),
    fontsize=8, color='red',
    arrowprops=dict(arrowstyle='->', color='red', lw=0.8)
)
ax2.annotate(
    'HH: anisotropy\nmore probable\n(classic ambiguity)',
    xy=(0.20, np.exp(2.*0.20**2*I_aniso)),
    xytext=(0.25, 2.2),
    fontsize=8, color='blue',
    arrowprops=dict(arrowstyle='->', color='blue', lw=0.8)
)

ax2.set_xlabel(r'Anisotropy amplitude $|\beta_\pm|$', fontsize=11)
ax2.set_ylabel(r'Probability ratio vs isotropic FRW', fontsize=10)
ax2.set_title("Cosmological wave-function prescription\n"
              "and selection of isotropy", fontsize=10)
ax2.legend(fontsize=7.5, loc='upper right')
ax2.set_xlim(0., 0.5); ax2.set_ylim(0., 3.0)
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('Fig_ECF_WKB_ECKS.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("\nFigure : Fig_ECF_WKB_ECKS.png")
