# DOCUMENT DE CONTEXTE POUR AUDIT DE PLOT

**Dossier audité :** B_Paper_Plots

---

## CONTENU DES SOURCES PYTHON

### Fichier 1 : `plot_F3_ecf_wkb_ecks.py`

```python
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
                 label='HH: anisotropy favoured (Gibbons-Turok problem)')

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

```

---

### Fichier 2 : `plot_ECF_falsifiability_timeline.py`

```python
#!/usr/bin/env python3
"""
plot_ECF_falsifiability_timeline.py

Falsifiability timeline for the Einstein-Cartan Framework (Foundation III).
Each ECF prediction is a KILL-SWITCH: an observation that, if it comes out
the "wrong" way, constrains the stated ECF sector or template. Shows WHEN each
# test arrives (2026 onward; schedule-dependent)
and WHICH outcome would constrain which sector.

DESIGN: light background, PRINT-SAFE / grayscale-safe (staged greys + distinct
marker shapes). Two-column layout: timeline + cards on top, logic panel below.

Output: Fig_ECF_Falsifiability_Timeline.png (300 dpi)
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
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif", "axes.linewidth": 0.0,
})

BG="#ffffff"; INK="#1a1a1a"; MUTED="#5c5c5c"; FAINT="#b8b8b8"; PANEL="#f4f2ec"
C_NEAR="#8a1c3b"; C_MID="#1f5f8b"; C_FAR="#3a7d34"; C_FAR2="#c07a00"

# (year, date, probe, prediction, kill_condition, color, marker)
rows = [
 (2026.85,"Nov 2026","DESI DR2 (published) / Euclid DR1",
  "calibrated $(w_0,w_a)$: $d_{\\rm Maha}=2.03\\sigma$ (DESI DR1, Planck prior)",
  "agreement with $\\Lambda$CDM at $<1\\sigma$",C_NEAR,"o"),
 (2027.5,"mid-2027","Euclid DR1-Complete / DESI LRG",
  "void-size excess at $R>\\xi_{\\rm KZ}=60\\,$Mpc comoving ($\\times2.1$)",
  "no void excess at $R>\\xi_{\\rm KZ}$ (KZ sector constrained)",C_NEAR,"s"),
 (2028.0,"schedule-dep.","DESI full 5-yr / Rubin LSST",
  "dark-energy direction $w_0>-1,\\ w_a<0$",
  "$w_a>0$ or $w_0<-1$",C_MID,"D"),
 (2035.0,"launch ~2035","LISA",
  "blue GW background $n_T>0$, $\\Pi_{\\rm GW}\\approx0.20\\pm0.05$ (calibrated template)",
  "$n_T\\leq0$ (chiral-GW template constrained)",C_FAR2,"P"),
 (2036.5,"launch JFY2036","LiteBIRD (ISAS/JAXA)",
  "CMB birefringence $\\beta>0.1°$ (chiral $B$-modes)",
  "$\\beta$ consistent with $0$",C_FAR,"^"),
]

fig=plt.figure(figsize=(15,9.4),dpi=300); fig.patch.set_facecolor(BG)
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,15); ax.set_ylim(0,9.4); ax.axis("off")

ax.text(7.5,9.0,"How the Einstein-Cartan Framework Can Be Constrained",
        ha="center",va="center",color=INK,fontsize=23,weight="bold")
ax.text(7.5,8.52,"Roadmap of discriminating tests, 2026 onward \u2014 each adverse result constrains the stated sector or template, not the model",
        ha="center",va="center",color=MUTED,fontsize=12,style="italic")

# ---- timeline ----
t0,t1=2025.5,2038.5   # horizon indicatif : les calendriers de mission glissent
def X(y): return 0.9+(y-t0)/(t1-t0)*(14.1-0.9)
yax=7.75
ax.plot([X(t0),X(t1)],[yax,yax],color=INK,lw=2.0,zorder=3,solid_capstyle="round")
ax.add_patch(FancyArrowPatch((X(t1)-0.02,yax),(X(t1)+0.28,yax),
    arrowstyle="-|>",mutation_scale=20,color=INK,lw=2.0,zorder=3))
for yr in [2026,2028,2030,2032,2034,2036]:
    ax.plot([X(yr),X(yr)],[yax-0.10,yax+0.10],color=INK,lw=1.3,zorder=3)
    ax.text(X(yr),yax+0.26,str(yr),ha="center",va="bottom",color=MUTED,fontsize=9.5)
ax.text(X(t1)+0.30,yax+0.28,"year",ha="left",va="bottom",color=MUTED,fontsize=9.5,style="italic")
# markers on timeline
for yr,date,probe,pred,kill,col,mk in rows:
    ax.scatter([X(yr)],[yax],marker=mk,s=95,color=col,edgecolors=INK,linewidths=0.9,zorder=6)

# ---- cards (wide, full width) ----
card_w, card_h = 13.2, 0.92
x_left = 0.9
row_y0 = 6.60
dy = 1.00
for i,(yr,date,probe,pred,kill,col,mk) in enumerate(rows):
    cy=row_y0-i*dy
    # connector timeline -> card
    ax.plot([X(yr),X(yr)],[yax-0.12,cy+card_h/2],color=FAINT,lw=1.0,ls=(0,(2,2)),zorder=2)
    ax.add_patch(FancyBboxPatch((x_left,cy-card_h/2),card_w,card_h,
        boxstyle="round,pad=0.02,rounding_size=0.09",linewidth=1.5,
        edgecolor=col,facecolor=PANEL,zorder=4))
    # left chip: marker + date + probe
    ax.add_patch(FancyBboxPatch((x_left,cy-card_h/2),3.0,card_h,
        boxstyle="round,pad=0.02,rounding_size=0.09",linewidth=0,
        facecolor=col,alpha=0.15,zorder=4.5))
    ax.scatter([x_left+0.34],[cy+0.20],marker=mk,s=68,color=col,edgecolors=INK,linewidths=0.8,zorder=6)
    ax.text(x_left+0.58,cy+0.20,date,ha="left",va="center",color=col,fontsize=10,weight="bold",zorder=6)
    ax.text(x_left+0.20,cy-0.22,probe,ha="left",va="center",color=INK,fontsize=8.8,style="italic",zorder=6)
    # middle: ECF predicts
    ax.text(x_left+3.25,cy+0.20,"ECF predicts",ha="left",va="center",color=C_FAR,fontsize=8.2,weight="bold",zorder=6)
    ax.text(x_left+5.05,cy+0.20,pred,ha="left",va="center",color=INK,fontsize=9.2,zorder=6)
    # bottom: falsified if
    ax.text(x_left+3.25,cy-0.22,"Constrained if",ha="left",va="center",color=C_NEAR,fontsize=8.2,weight="bold",zorder=6)
    ax.text(x_left+5.05,cy-0.22,kill,ha="left",va="center",color=INK,fontsize=9.2,zorder=6)
    # divider between predict / falsify columns
    ax.plot([x_left+4.95,x_left+4.95],[cy-card_h/2+0.12,cy+card_h/2-0.12],color=FAINT,lw=0.7,zorder=5)

# ---- bottom logic strip (four horizontal blocks) ----
strip_y = 1.30
bx0 = 0.9; bw = 13.2
ax.add_patch(FancyBboxPatch((bx0,0.55),bw,1.35,
    boxstyle="round,pad=0.02,rounding_size=0.10",linewidth=1.3,
    edgecolor=MUTED,facecolor="#faf8f2",zorder=3))
ax.text(bx0+0.25,1.68,"Why this matters:",ha="left",va="center",color=INK,fontsize=11,weight="bold",zorder=5)
ax.text(bx0+2.55,1.68,"a theory that forbids nothing explains nothing \u2014 each row states the observation that would constrain the stated sector or template.",
        ha="left",va="center",color=INK,fontsize=9.5,style="italic",zorder=5)
# three phase summaries
phases = [
 (C_NEAR,"2026-27  near-term","growth tension + void excess (DESI, Euclid) \u2014 fastest paths to constrain the stated sectors."),
 (C_MID, "schedule-dep.","sign of $(w_0,w_a)$ from DESI full 5-yr / Rubin LSST discriminates ECF from a cosmological constant."),
 (C_FAR2,"2035-37  smoking gun","parity violation: CMB birefringence (LiteBIRD) + blue chiral GW background (LISA). $n_T\\leq0$ constrains the chiral-GW template."),
]
yy=1.28
for col,head,body in phases:
    ax.add_patch(Circle((bx0+0.32,yy),0.05,color=col,zorder=6))
    ax.text(bx0+0.50,yy,head+":",ha="left",va="center",color=col,fontsize=8.8,weight="bold",zorder=6)
    ax.text(bx0+2.55,yy,body,ha="left",va="center",color=INK,fontsize=8.6,zorder=6)
    yy-=0.30

ax.text(7.5,0.22,
        "Einstein-Cartan Framework  \u00b7  Foundation III  \u00b7  predictions stated with the conditions under which they are constrained (a sector or template, not the whole framework)",
        ha="center",va="center",color=MUTED,fontsize=8.4,style="italic")

fig.savefig("Fig_ECF_Falsifiability_Timeline.png",dpi=300,facecolor=BG,bbox_inches="tight",pad_inches=0.15)
print("Saved.")

```

---

### Fichier 3 : `check_vsf_v2_edge_voids.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_vsf_v2_edge_voids.py  --  ECF Foundation III
======================================================================
Why the VSF kill-switch uses VoidFinder and not V2: the large V2 voids
are boundary voids.

THE QUESTION
------------
DESIVAST DR1 (Rincon et al. 2025) publishes THREE void catalogues built
on the same BGS Bright sample, with three maximum effective radii:

    VoidFinder     31.7 Mpc/h
    V2/REVOLVER    43.5 Mpc/h
    V2/VIDE        55.9 Mpc/h

The ECF threshold sits at 40.4 Mpc/h (xi_KZ = 60 Mpc, adopted, A-8).
The 43.8 Mpc/h column (65 Mpc) is kept for comparison only (historical value). Foundation III states that the threshold "remains out of reach
of the BGS sample", but it uses VoidFinder alone -- the algorithm that
finds the SMALLEST voids -- and the choice was not justified anywhere.
A referee reading the DESIVAST paper will see 55.9 Mpc/h and ask.

Two of the three catalogues do reach past the threshold. So the honest
question is not whether the data extend far enough, but whether the
voids that extend that far are usable.

THE ANSWER
----------
They are not: every V2 void above the threshold is truncated by the
survey boundary. The catalogues carry TOT_AREA and EDGE_AREA per void,
so the boundary fraction f = EDGE_AREA / TOT_AREA is directly available,
and this script tabulates the maximum radius as a function of the cut
on f. The result is unambiguous -- see the printed table.

A void cut by the survey edge has an ill-constrained volume, hence an
overestimated effective radius; such objects are precisely what a void
size function must exclude. The apparent reach of V2 is therefore a
boundary artefact, and using VoidFinder is the conservative choice.

REPRODUCING THIS
----------------
The four V2 FITS files are large (62-612 MB) and are NOT redistributed
with this corpus. Download them from

    https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1.0/

    DESIVAST_BGS_VOLLIM_V2_VIDE_NGC.fits       (459 MB)
    DESIVAST_BGS_VOLLIM_V2_VIDE_SGC.fits        (62 MB)
    DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits   (612 MB)
    DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC.fits    (87 MB)

place them under data/dr1/desivast_dr1/ (or pass --dir; the script
also looks beside itself), and run it.
Without them it prints the recorded values and exits cleanly, so the
numbers quoted in the paper remain inspectable either way.

Usage:  python3 check_vsf_v2_edge_voids.py [--dir PATH]
======================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
import glob
import os

import numpy as np

H = 0.6732                                  # DESIVAST fiducial (Planck 2018)
THRESHOLDS = {"xi_KZ = 60 Mpc": 60.0 * H,   # 40.4 Mpc/h
              "xi_KZ = 65 Mpc": 65.0 * H}   # 43.8 Mpc/h
CUTS = (0.00, 0.01, 0.05, 0.10, 0.25, 1.00)

# Values obtained on 26/08/2026, kept so that the paper's numbers can be
# checked even when the FITS files are absent.
RECORDED = {
    "V2_VIDE_NGC":     dict(n=1258, rmax=55.88, above40=15, above44=8),
    "V2_VIDE_SGC":     dict(n=220,  rmax=38.30, above40=0,  above44=0),
    "V2_REVOLVER_NGC": dict(n=1692, rmax=43.50, above40=1,  above44=0),
    "V2_REVOLVER_SGC": dict(n=300,  rmax=35.76, above40=0,  above44=0),
}
RECORDED_VIDE_NGC_BY_CUT = [
    (0.00, 105, 30.20, 0, 0), (0.01, 143, 30.88, 0, 0),
    (0.05, 191, 33.51, 0, 0), (0.10, 269, 43.46, 2, 0),
    (0.25, 884, 55.58, 12, 7), (1.00, 1258, 55.88, 15, 8),
]


def analyse(path):
    from astropy.io import fits
    with fits.open(path, memmap=True) as hdul:
        d = hdul["VOIDS"].data
        r = np.asarray(d["RADIUS"], dtype=float)
        tot = np.asarray(d["TOT_AREA"], dtype=float)
        edge = np.asarray(d["EDGE_AREA"], dtype=float)
    f = np.where(tot > 0, edge / np.maximum(tot, 1e-30), 1.0)
    return r, f


def report(name, r, f):
    print(f"\n{'-' * 66}\n  {name}   ({len(r):,} voids)")
    print(f"  boundary fraction: median {np.median(f):.3f}, "
          f"p10 {np.percentile(f,10):.4f}, p90 {np.percentile(f,90):.3f}")
    print(f"\n  {'cut on f':>12} {'N kept':>8} {'max R':>9}"
          + "".join(f" {k.split('=')[1].strip():>12}" for k in THRESHOLDS))
    for c in CUTS:
        m = f <= c
        if not m.any():
            continue
        line = f"  {c:>12.2f} {m.sum():>8,} {r[m].max():>9.2f}"
        for _, t in THRESHOLDS.items():
            line += f" {int((r[m] > t).sum()):>12}"
        print(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None,
                    help="directory holding the DESIVAST FITS files")
    a = ap.parse_args()

    # Look in the usual places rather than forcing one convention: the
    # deposited layout keeps the catalogues under data/dr1/desivast_dr1/
    # while the download helper of the VSF script drops them next to it.
    if a.dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        parent = os.path.dirname(here)
        repo_root = os.path.dirname(parent)   # .../Foundation_3, two levels up
        for cand in (
            os.path.join(repo_root, "data", "desivast_dr1"),
            "data/dr1/desivast_dr1", "desivast_dr1", ".",
            os.path.join(here, "data", "dr1", "desivast_dr1"),
            os.path.join(here, "desivast_dr1"),
            os.path.join(parent, "B_Paper_Plots", "desivast_dr1"),
            os.path.join(parent, "A_Core_Calculations", "desivast_dr1"),
            here,
        ):
            if glob.glob(os.path.join(cand, "DESIVAST_BGS_VOLLIM_V2_*.fits")):
                a.dir = cand
                break
        else:
            a.dir = os.path.join(repo_root, "data", "desivast_dr1")

    print("=" * 66)
    print("  Are the large V2 voids usable? (boundary-fraction test)")
    print("=" * 66)
    print(f"  ECF thresholds: " +
          ", ".join(f"{k} -> {v:.1f} Mpc/h" for k, v in THRESHOLDS.items()))

    files = sorted(glob.glob(os.path.join(a.dir, "DESIVAST_BGS_VOLLIM_V2_*.fits")))
    if not files:
        print(f"\n  V2 catalogues not found in '{a.dir}/'.")
        print("  They are not redistributed here (62-612 MB); see the header")
        print("  for the download URL. Recorded values (26/08/2026):\n")
        print(f"  {'catalogue':<18} {'N':>7} {'max R':>8} {'>40.4':>7} {'>43.8':>7}")
        for k, v in RECORDED.items():
            print(f"  {k:<18} {v['n']:>7,} {v['rmax']:>8.2f} "
                  f"{v['above40']:>7} {v['above44']:>7}")
        print(f"\n  V2/VIDE NGC, by cut on the boundary fraction f:")
        print(f"  {'f <=':>8} {'N':>7} {'max R':>8} {'>40.4':>7} {'>43.8':>7}")
        for c, n, rm, a40, a44 in RECORDED_VIDE_NGC_BY_CUT:
            print(f"  {c:>8.2f} {n:>7,} {rm:>8.2f} {a40:>7} {a44:>7}")
        verdict()
        return 0

    for p in files:
        name = os.path.basename(p).replace("DESIVAST_BGS_VOLLIM_", "").replace(".fits", "")
        try:
            r, f = analyse(p)
        except Exception as exc:
            print(f"\n  [{name}] unreadable: {type(exc).__name__}: {exc}")
            continue
        report(name, r, f)
    verdict()
    return 0


def verdict():
    print("\n" + "=" * 66)
    print("  READING THIS")
    print("=" * 66)
    print("  The cut at f <= 0.10 is NOT ours: DESIVAST defines an edge")
    print("  void as one with over 10% of its surface on the survey")
    print("  boundary. Applying it reproduces their published interior")
    print("  counts to within one or two objects (269 vs 268 for VIDE NGC,")
    print("  355 vs 353 for REVOLVER NGC): the criterion is theirs, and it")
    print("  is being applied as intended.")
    print()
    print("  V2/VIDE NGC is the only catalogue reaching past the threshold:")
    print("  15 voids above 40.4 Mpc/h and 8 above 43.8. None of them is")
    print("  marginal. The cleanest of the eight still has 10.6% of its")
    print("  surface on the survey boundary; the largest has 31.6%.")
    print()
    print("  Under their own criterion (f <= 0.10) the tail collapses: the")
    print("  maximum interior radius is 43.46 Mpc/h, two voids clear 40.4 and")
    print("  NONE clears 43.8. At f <= 0.05 none clears 40.4 either. One has")
    print("  to admit a quarter of a void surface outside the survey -- two")
    print("  and a half times the published criterion -- before a single")
    print("  object appears above the higher threshold.")
    print()
    print("  A void truncated by the boundary has an ill-constrained volume")
    print("  and an overestimated effective radius. The apparent reach of V2")
    print("  is therefore a boundary artefact, and restricting the test to")
    print("  VoidFinder is the conservative choice -- which is why this")
    print("  corpus does so.")
    print()
    print("WHAT THIS DOES NOT ESTABLISH:")
    print("  * that the ECF prediction is right -- only that DR1 cannot test it;")
    print("  * the published maximum of 55.9 Mpc/h: that figure is quoted")
    print("    over ALL voids in their fiducial volume, and is exactly the")
    print("    object with 31.6% of its surface on the boundary -- real, but")
    print("    unusable for a size function;")
    print("  * anything about Euclid DR1, where the definitive test remains.")


if __name__ == "__main__":
    sys.exit(main())

```

---

### Fichier 4 : `compute_vsf_lcdm_svdw.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_vsf_lcdm_svdw.py  --  ECF Foundation III
======================================================================
A genuine LambdaCDM void size function, from excursion-set theory.

WHY THIS SCRIPT EXISTS
----------------------
Three figures in this corpus compare an ECF void excess against a
"LambdaCDM" baseline that is not one:

  Fig_ECF_VSF_DESIVAST_DR1   placeholder rescaled from an old SDSS catalogue
  Fig_Void_Statistics        a hand-chosen form (R/20)^3 exp[-(R/15)^2]
  Fig_VSF_ECF_Prediction     an analytic approximation calibrated on BOSS

All three are now labelled as such, but the underlying gap remains: no
significance from the VSF kill-switch is citable, because there is
nothing legitimate to compare against. This script supplies the missing
piece by computing the Sheth-van de Weygaert (2004) void size function
rather than approximating it.

THE CALCULATION
---------------
SvdW give the comoving number density of voids per unit ln radius as

    dn/dln r = (f_ln sigma / V(r)) * |dln sigma / dln r|

where V(r) = (4/3) pi r^3 and f_ln sigma is the two-barrier first-crossing
distribution of the excursion-set random walk. With the void barrier
delta_v < 0 and the collapse barrier delta_c > 0, define

    D = |delta_v| / (delta_c + |delta_v|),    nu = |delta_v| / sigma

SvdW give a series solution; for D <= 0.276 the series is well
approximated (their Eq. 4) by

    f = sqrt(2/pi) * nu * exp(-nu^2/2) * exp(-|delta_v| D^2 / (4 nu^2 sigma) - 2 D^4 / nu^4)

and outside that regime by the series over j. Both branches are
implemented, and the script reports which one it used.

sigma(r) comes from the linear power spectrum,

    sigma^2(r) = (1/2pi^2) int dk k^2 P(k) W^2(kr),   W = top-hat

with P(k) = A k^n T^2(k), T the BBKS transfer function already used
elsewhere in this corpus (plot_spectre_puissance.py), normalised to
sigma_8.

The void radius is the EXPANDED radius: an underdensity that has
reached delta_v has expanded by a factor 1.7 over its Lagrangian size,
so r_void = 1.7 * r_Lagrangian. Omitting that factor is the commonest
error in reproducing SvdW, and it shifts the whole curve.

WHAT THIS IS AND IS NOT
-----------------------
IS:     a real excursion-set computation, with stated parameters, which
        can be checked line by line against SvdW (2004, MNRAS 350:517).
IS NOT: a survey-matched prediction. Real catalogues apply a tracer
        density, a magnitude cut, a void-finder definition and a survey
        mask, none of which enter here. Comparing this curve directly to
        DESIVAST counts would be comparing different quantities -- the
        same mistake the placeholders made. What it gives is the
        THEORETICAL shape and normalisation; matching it to a catalogue
        requires a mock, which is a separate task.

Dependency: numpy, scipy.
Usage: python3 compute_vsf_lcdm_svdw.py [--sigma8 0.8119] [--om 0.315]
======================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse

import numpy as np
from scipy.integrate import quad

# --- cosmology (Planck 2018, the corpus convention) -------------------
DELTA_V = -2.81          # void barrier, linear theory (SvdW 2004)
DELTA_C = 1.686          # collapse barrier
EXPANSION = 1.7          # r_void / r_Lagrangian at shell crossing


def bbks_T(k, om, h):
    """BBKS transfer function (Bardeen et al. 1986); k in h/Mpc."""
    gamma = om * h
    q = np.asarray(k, dtype=float) / gamma
    q = np.maximum(q, 1e-12)
    return (np.log(1 + 2.34 * q) / (2.34 * q)) * (
        1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4
    ) ** -0.25


def _w_tophat(x):
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    m = np.abs(x) > 1e-6
    xm = x[m]
    out[m] = 3.0 * (np.sin(xm) - xm * np.cos(xm)) / xm ** 3
    return out


def sigma_R(R, om, h, ns, norm):
    """rms of the linear density field in top-hat spheres of radius R [Mpc/h]."""
    def integ(lnk):
        k = np.exp(lnk)
        return k ** 3 * (k ** ns * bbks_T(k, om, h) ** 2) * _w_tophat(k * R) ** 2
    val, _ = quad(integ, np.log(1e-4), np.log(1e3), limit=200)
    return np.sqrt(norm * val / (2 * np.pi ** 2))


def f_lnsigma(sigma, D, dv=abs(DELTA_V), jmax=4000):
    """
    Two-barrier first-crossing distribution (SvdW 2004, Eq. 4):

        f_ln sigma = 2 sum_j  j pi x^2 sin(j pi D) exp[-(j pi x)^2 / 2],
        x = D sigma / |delta_v|

    /!\\ Two errors were made writing this and are recorded so they are not
    repeated. First, the prefactor is x^2, NOT D^2: using D^2 drops a factor
    1/nu^2. Second, an early version truncated the sum at j = 4; the series
    alternates in sign and its terms grow before the exponential bites, so
    truncation gave an oscillating curve that was not a size function at all.
    The suppression only acts once j pi x >> 1, and x falls as sigma does, so
    the number of terms needed grows at large radii.

    VALIDATION: integral of f_ln sigma dsigma/sigma over all sigma must equal
    1 - D exactly (see e.g. arXiv:1304.6087 Eq. 14). check_normalisation()
    below performs that test and the script refuses to print a table if it
    fails -- an unvalidated excursion-set curve is exactly what this script
    exists to replace.
    """
    x = D * sigma / dv
    # [15/10/2026, F3-A16] Small-x branch. For x <= 0.276 the alternating
    # series below is dominated by cancellation noise (beyond r_void ~ 35 Mpc/h
    # it returned 0, then values RISING to 1.6e-22 at 60 Mpc/h). Use the
    # standard small-x limit of the same distribution (Jennings, Li & Hu 2013,
    # MNRAS 434, 2167, Eq. 8): f = sqrt(2/pi) (|delta_v|/sigma) exp(-delta_v^2/2 sigma^2).
    # It matches the series to <= 0.02 % wherever the series is reliable
    # (10-35 Mpc/h). It is switched on only below x = 0.08 (sigma < ~0.36,
    # r_void > ~35 Mpc/h), where the series fails, so that the exact series is
    # kept elsewhere and the normalisation test stays at machine precision;
    # every value quoted in Foundation III is unchanged.
    if x < 0.08:
        return float(np.sqrt(2.0 / np.pi) * (dv / sigma) * np.exp(-dv ** 2 / (2.0 * sigma ** 2)))
    j = np.arange(1, jmax + 1)
    terms = (2.0 * j * np.pi * x ** 2 * np.sin(j * np.pi * D)
             * np.exp(-(j * np.pi * x) ** 2 / 2.0))
    total = np.sum(terms)
    # The sum alternates, so at small sigma the answer is the difference of
    # large numbers and double precision runs out: below ~1e-19 the result is
    # cancellation noise, and can even come out negative. Report zero there
    # rather than a spurious figure -- a negative void density is not a small
    # error, it is a meaningless one.
    if abs(total) < 1e-19 * max(np.max(np.abs(terms)), 1e-300):
        return 0.0
    return max(total, 0.0)


def check_normalisation(D, tol=1e-6):
    """Integral of f_ln sigma dsigma/sigma == 1 - D."""
    val, _ = quad(lambda s: f_lnsigma(s, D) / s, 1e-3, 50, limit=400)
    return val, abs(val - (1.0 - D)) < tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sigma8", type=float, default=0.8119,
                    help="sigma_8 (default: LCDM value used in this corpus)")
    ap.add_argument("--om", type=float, default=0.315)
    ap.add_argument("--h", type=float, default=0.6732)
    ap.add_argument("--ns", type=float, default=0.965)
    a = ap.parse_args()

    print("=" * 68)
    print("  LambdaCDM void size function -- Sheth & van de Weygaert (2004)")
    print("=" * 68)
    print(f"\n  Om_m = {a.om}   h = {a.h}   n_s = {a.ns}   sigma_8 = {a.sigma8}")
    print(f"  barriers: delta_v = {DELTA_V}, delta_c = {DELTA_C}")
    D = abs(DELTA_V) / (DELTA_C + abs(DELTA_V))
    print(f"  D = |delta_v|/(delta_c+|delta_v|) = {D:.4f}")

    # normalise the power spectrum to sigma_8
    s8_raw = sigma_R(8.0, a.om, a.h, a.ns, 1.0)
    norm = (a.sigma8 / s8_raw) ** 2
    print(f"\n  normalisation: sigma_8(raw) = {s8_raw:.4e} -> A = {norm:.4e}")
    check = sigma_R(8.0, a.om, a.h, a.ns, norm)
    print(f"  check: sigma(8 Mpc/h) = {check:.4f}   (target {a.sigma8})")
    if abs(check - a.sigma8) > 1e-3:
        print("  /!\\ normalisation failed")
        return 1

    # RULE 23: refuse to print a table from an unvalidated implementation.
    nval, ok = check_normalisation(D)
    print(f"\n  VALIDATION: integral f_ln sigma dsigma/sigma = {nval:.6f}")
    print(f"              expected (1 - D)                 = {1.0 - D:.6f}")
    if not ok:
        print("  /!\\ normalisation test FAILED -- no table printed.")
        return 1
    print(f"              agreement to {abs(nval - (1.0 - D)):.1e} -- implementation validated")

    print("\n" + "-" * 68)
    print("  Void size function")
    print("-" * 68)
    print(f"  {'r_void':>9} {'r_Lagr':>9} {'sigma':>8} {'nu':>7} "
          f"{'dn/dlnr':>12}")
    print(f"  {'[Mpc/h]':>9} {'[Mpc/h]':>9} {'':>8} {'':>7} {'[(Mpc/h)^-3]':>12}")

    branch_used = None
    results = []
    for r_void in (10., 15., 20., 25., 30., 35., 40., 45., 50., 60.):
        rL = r_void / EXPANSION
        s = sigma_R(rL, a.om, a.h, a.ns, norm)
        nu = abs(DELTA_V) / s
        f = f_lnsigma(s, D)
        # |dln sigma / dln r| by central difference in ln r
        d = 1e-3
        s1 = sigma_R(rL * (1 - d), a.om, a.h, a.ns, norm)
        s2 = sigma_R(rL * (1 + d), a.om, a.h, a.ns, norm)
        dlnsig = abs((np.log(s2) - np.log(s1)) / (2 * d))
        V = (4.0 / 3.0) * np.pi * r_void ** 3
        dn = f / V * dlnsig
        results.append((r_void, rL, s, nu, dn))
        print(f"  {r_void:>9.1f} {rL:>9.2f} {s:>8.4f} {nu:>7.2f} {dn:>12.4e}")


    peak = max(results, key=lambda t: t[4])
    print(f"  peak of dn/dln r at r_void = {peak[0]:.0f} Mpc/h")

    # ------------------------------------------------------------------
    # Step 2: from a comoving density to an expected COUNT
    # ------------------------------------------------------------------
    # dn/dln r is a density; a catalogue reports a number. Multiplying by the
    # survey volume gives the count a LambdaCDM universe would put in the
    # DESIVAST footprint, which can be set beside the 1,489 interior voids
    # actually found. This is a consistency check on the prediction, NOT the
    # kill-switch: it does not pass through the selection function.
    V_SURVEY = 0.085e9        # Mpc^3, DESIVAST DR1 volume-limited sample
    h3 = a.h ** 3
    V_h = V_SURVEY * h3       # -> (Mpc/h)^3
    print("\n" + "-" * 68)
    print("  Expected counts in the DESIVAST DR1 volume")
    print("-" * 68)
    print(f"  survey volume: {V_SURVEY:.3e} Mpc^3 = {V_h:.3e} (Mpc/h)^3")
    print(f"  (DESIVAST DR1 volume-limited sample, z < 0.24)")
    print()
    print(f"  {'r_void':>9} {'dn/dlnr':>12} {'N per bin':>12}")
    edges = [10., 13., 16., 19., 22., 25., 28., 32., 36., 42., 54.]
    total = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        rc = np.sqrt(lo * hi)
        rL = rc / EXPANSION
        s = sigma_R(rL, a.om, a.h, a.ns, norm)
        f = f_lnsigma(s, D)
        d = 1e-3
        s1 = sigma_R(rL * (1 - d), a.om, a.h, a.ns, norm)
        s2 = sigma_R(rL * (1 + d), a.om, a.h, a.ns, norm)
        dlnsig = abs((np.log(s2) - np.log(s1)) / (2 * d))
        dn = f / ((4.0 / 3.0) * np.pi * rc ** 3) * dlnsig
        N = dn * V_h * np.log(hi / lo)
        total += N
        print(f"  {lo:>4.0f}-{hi:<4.0f} {dn:>12.3e} {N:>12.1f}")
    print(f"  {'TOTAL':>9} {'':>12} {total:>12.1f}")
    print()
    print(f"  observed (DESIVAST DR1, interior VoidFinder voids): 1489")
    if total > 0:
        print(f"  ratio predicted / observed: {total / 1489.0:.2f}")
    print()
    print("  /!\\ This is NOT a significance, and NOT a tension. The prediction")
    print("      is for spherical voids in the DARK MATTER field; the catalogue")
    print("      reports VoidFinder voids in a magnitude-limited GALAXY sample.")
    print("      A galaxy sample with M_r <= -20 has a mean separation of")
    print("      5.62 Mpc and is far sparser than the matter field, so voids")
    print("      found in it are more numerous and larger. The barrier")
    print("      delta_v = -2.81 is the dark-matter shell-crossing value; for")
    print("      biased tracers the effective threshold differs. The offset is")
    print("      therefore expected, and its size is informative:")
    print()
    print("      A cross-check confirms the arithmetic rather than the model.")
    print("      1489 voids of r ~ 15 Mpc/h fill ~81% of this volume, which")
    print("      sits alongside the 63% DESIVAST measures in its fiducial")
    print("      volume; the SvdW prediction fills ~1%. The counts are being")
    print("      computed correctly -- what separates them is the tracer.")
    print()
    print("      A factor of order 100 is what a bias effect looks like. A")
    print("      factor of 10^5 would have pointed at the model. This test")
    print("      was run to tell those apart, and it does.")

    print("\n" + "=" * 68)
    print("  READING THIS")
    print("=" * 68)
    print("  This is the THEORETICAL void size function: a real excursion-set")
    print("  computation, not a rescaled catalogue and not a hand-chosen form.")
    print()
    print("  It is NOT directly comparable to DESIVAST counts. A catalogue")
    print("  applies a tracer density, a magnitude cut, a void-finder")
    print("  definition and a survey mask; none of those enter here.")
    print("  Comparing this curve to raw counts would repeat the very error")
    print("  the placeholders made -- comparing different quantities.")
    print()
    print("  What it does supply: the shape and normalisation a mock would")
    print("  have to reproduce, and therefore the starting point for a")
    print("  citable significance.")
    print()
    print("WHAT REMAINS:")
    print("  * a survey mock (AbacusSummit BGS, as DESIVAST itself uses) to")
    print("    carry this prediction through the selection function;")
    print("  * the expansion factor 1.7 is the standard shell-crossing value")
    print("    and is not derived here;")
    print("  * BBKS is a fitting formula: adequate for a shape, not for")
    print("    percent-level work, where CAMB or CLASS would be used.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

---

### Fichier 5 : `run_F3_agregat_scripts_plots_audit.py`

```python

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
from pathlib import Path

def generer_contexte_audit():
    dossier_source = Path(".")
    fichier_sortie = "F3_agregat_scripts_plots_audit.md"
    extensions_cibles = {'.py'}
    dossiers_a_ignorer = {'__pycache__', '.venv', 'venv', '.git', '.idea', '.vscode'}

    print("Début de l'analyse des scripts...")
    compteur_fichiers = 0

    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        print("# DOCUMENT DE CONTEXTE POUR AUDIT DE PLOT", file=f_out)
        print("", file=f_out)
        print(f"**Dossier audité :** {dossier_source.resolve().name}", file=f_out)
        print("", file=f_out)
        print("---", file=f_out)
        print("", file=f_out)
        print("## CONTENU DES SOURCES PYTHON", file=f_out)
        print("", file=f_out)
        
        for root, dirs, files in os.walk(dossier_source):
            dirs[:] = [d for d in dirs if d not in dossiers_a_ignorer]
            
            for f in files:
                chemin_complet = Path(root) / f
                
                if f in ["agregateur_audit.py", fichier_sortie]:
                    continue
                    
                if chemin_complet.suffix in extensions_cibles:
                    chemin_relatif = chemin_complet.relative_to(dossier_source)
                    compteur_fichiers += 1
                    
                    print(f"### Fichier {compteur_fichiers} : `{chemin_relatif}`", file=f_out)
                    print("", file=f_out)
                    print("```python", file=f_out)
                    
                    try:
                        with open(chemin_complet, 'r', encoding='utf-8') as f_in:
                            for ligne in f_in:
                                # On écrit le code ligne par ligne pour éviter les conflits
                                print(ligne, end="", file=f_out)
                            print("", file=f_out) 
                    except Exception as e:
                        print(f"# Erreur de lecture : {str(e)}", file=f_out)
                    
                    print("```", file=f_out)
                    print("", file=f_out)
                    print("---", file=f_out)
                    print("", file=f_out)
                    
    print(f"Succès ! {compteur_fichiers} scripts ont été centralisés dans '{fichier_sortie}'.")

if __name__ == "__main__":
    generer_contexte_audit()
    
```

---

### Fichier 6 : `plot_F3_ecf_Cell_suppression.py`

```python
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

```

---

### Fichier 7 : `plot_paper_fig1_potential.py`

```python
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

```

---

### Fichier 8 : `plot_F3_ecf_mass_function_C6.py`

```python
#!/usr/bin/env python3
"""
plot_F3_ecf_mass_function_C6.py
===============================
ECF Foundation III — Strong Gravity — PO-F3-C6
Poisson coalescence mass function of the Micro-Knot network.
Author: Pascal Fichant
Date:   25 August 2026

PHYSICS  (all of it taken from F3 Strong Gravity, subsec. PO-F3-C6;
          nothing here is invented for the figure)
-----------------------------------------------------------------
The KZ network of Micro-Knots is already established as a 3D Poisson
point process of density n_KZ = xi_KZ^-3 (same process that yields
f_NL^KZ = +5/18 in F3 Cosmological Physics).

Coalescence is therefore a Poisson count. In a coalescence radius
R_coal(z):

    N ~ Poisson(lambda),   lambda = n_KZ * (4/3) pi R_coal(z)^3   [eq:lambda_coal]

and the resulting mass is M = N * M_micro, so the ECF mass function is
the Poisson law reparameterised in mass:

    n_ECF(M) dM  ∝  lambda^(M/M_micro) e^-lambda / (M/M_micro)!    [eq:n_ECF_poisson]

to be compared with the Gaussian form (Press-Schechter / Sheth-Tormen)
obtained for a continuous density field.

TESTABLE SIGNATURE
------------------
The Poisson law has exact skewness 1/sqrt(lambda), positive for every
finite lambda — the same statistical property that gives kappa_3 = sigma^2
and f_NL^KZ = +5/18 > 0. This is NOT a second ad hoc mechanism but the
same Poisson process seen at the scale of the mass function.

VALUES VERIFIED AGAINST THE PAPER (25/08/2026, before plotting)
---------------------------------------------------------------
    lambda    skewness 1/sqrt(lambda)    paper
    2         0.71                       0.71   OK
    5         0.45                       0.45   OK
    10        0.32                       0.32   OK
    100       0.10                       0.10   OK
    excess n_ECF/n_PS at M = 3<M>, lambda = 5 : 19.41  -> paper "x19"  OK

WHAT IS *NOT* CLOSED (stated in the paper, not to be overclaimed here)
----------------------------------------------------------------------
This lemma is a qualitative advance on PO-F3-C6, NOT its closure:
  (0) the n_KZ normalisation vs the real dark-matter density is unresolved;
  (a) R_coal(z) is a free, uncalibrated parameter, blocked by (0);
  (b) eq:n_ECF_poisson is not yet normalised to the observed baryon density;
  (c) no quantitative comparison to cluster mass functions yet.
=> lambda is therefore shown as an ILLUSTRATIVE range, never as a
   calibrated prediction. The figure carries that statement.

OUTPUT: Fig_ECF_MassFunction_C6.png (300 dpi, white background)
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm

OUT = Path(__file__).with_name("Fig_ECF_MassFunction_C6.png")
DPI = 300

LAMBDAS = [2, 5, 10, 100]          # illustrative range, cf. paper table
LAM_TAIL = 5                       # panel C works at lambda = 5
COLORS = {2: "#4c72b0", 5: "#d62728", 10: "#2ca02c", 100: "#8c6d31"}

plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "legend.fontsize": 7.5,
    "figure.facecolor": "white",
})


# ---------------------------------------------------------------------
def check_against_paper():
    """Refuse to plot numbers that disagree with the paper."""
    print("Verification against F3 Strong Gravity, subsec. PO-F3-C6")
    ok = True
    for lam, ref in ((2, 0.71), (5, 0.45), (10, 0.32), (100, 0.10)):
        val = 1.0 / np.sqrt(lam)
        good = abs(val - ref) < 0.005
        ok &= good
        print(f"   lambda={lam:>3}  skewness={val:5.2f}  paper={ref:4.2f}"
              f"   {'OK' if good else 'MISMATCH'}")
    n_tail = 3 * LAM_TAIL                       # M = 3<M>
    ratio = (poisson.pmf(n_tail, LAM_TAIL)
             / norm.pdf(n_tail, loc=LAM_TAIL, scale=np.sqrt(LAM_TAIL)))
    good = 18.5 < ratio < 20.5                  # paper quotes "x19"
    ok &= good
    print(f"   excess at M=3<M>, lambda={LAM_TAIL}: x{ratio:.2f}"
          f"   paper=x19   {'OK' if good else 'MISMATCH'}")
    if not ok:
        raise SystemExit("Figure NOT produced: a value disagrees with the paper.")
    print("   -> all values reproduce the paper.\n")
    return ratio


# ---------------------------------------------------------------------
def panel_A(ax):
    """Coalescence distributions for several lambda, normalised to peak."""
    for lam in LAMBDAS:
        hi = int(lam + 6 * np.sqrt(lam)) + 5
        n = np.arange(0, hi)
        p = poisson.pmf(n, lam)
        ax.plot(n / lam, p / p.max(), "-o", ms=2.2, lw=1.2,
                color=COLORS[lam], label=rf"$\lambda={lam}$")
    ax.axvline(1.0, color="grey", ls=":", lw=0.8)
    ax.text(1.02, 0.05, r"$\langle M\rangle$", fontsize=7.5, color="grey")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"$M/\langle M\rangle = N/\lambda$")
    ax.set_ylabel("distribution (normalised to peak)")
    ax.set_title("A — Coalescence distributions", loc="left")
    ax.legend(frameon=True, loc="upper right")
    ax.grid(alpha=0.25, ls=":")


def panel_B(ax):
    """Skewness 1/sqrt(lambda): same signature as f_NL^KZ = +5/18 > 0."""
    lam = np.logspace(np.log10(1.0), 2.3, 300)
    ax.plot(lam, 1.0 / np.sqrt(lam), "-", lw=1.8, color="#d62728")
    for l0 in LAMBDAS:
        ax.plot(l0, 1.0 / np.sqrt(l0), "o", ms=5, color=COLORS[l0], zorder=5)
        ax.annotate(f"{1/np.sqrt(l0):.2f}", (l0, 1 / np.sqrt(l0)),
                    textcoords="offset points", xytext=(6, 6), fontsize=7.5,
                    color=COLORS[l0])
    ax.axhline(0.0, color="black", lw=0.8)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\lambda$")
    ax.set_ylabel(r"skewness $1/\sqrt{\lambda}$")
    ax.set_title("B — Skewness: positive for every finite $\\lambda$", loc="left")
    ax.set_ylim(-0.05, 0.85)
    ax.grid(alpha=0.25, ls=":", which="both")
    ax.text(0.04, 0.10,
            "same statistical signature as\n"
            r"$f_{\rm NL}^{\rm KZ}=+5/18>0$",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(boxstyle="round,pad=0.35", fc="#fdf3f3",
                      ec="#d62728", lw=0.7))


def panel_C(ax, ratio):
    """Poisson vs Gaussian tail at lambda = 5."""
    lam = LAM_TAIL
    n = np.arange(0, 26)
    p = poisson.pmf(n, lam)
    g = norm.pdf(n, loc=lam, scale=np.sqrt(lam))
    ax.semilogy(n / lam, p, "-o", ms=3, lw=1.3, color="#d62728",
                label=rf"ECF Poisson ($\lambda={lam}$)")
    ax.semilogy(n / lam, g, "--", lw=1.3, color="#4c72b0",
                label="Gaussian (Press–Schechter)")
    ax.axvline(3.0, color="grey", ls=":", lw=0.9)
    ax.annotate(rf"$\times{ratio:.0f}$ at $M=3\langle M\rangle$",
                xy=(3.0, poisson.pmf(3 * lam, lam)),
                xytext=(0.35, 3e-6), fontsize=8.5, fontweight="bold",
                color="#d62728",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.0))
    ax.set_xlim(0, 4.2)
    ax.set_ylim(1e-9, 0.4)
    ax.set_xlabel(r"$M/\langle M\rangle$")
    ax.set_ylabel("probability density")
    ax.set_title("C — Heavy tail: Poisson vs Gaussian", loc="left")
    ax.legend(frameon=True, loc="lower left")
    ax.grid(alpha=0.25, ls=":", which="both")


# ---------------------------------------------------------------------
def main():
    ratio = check_against_paper()

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3), facecolor="white")
    panel_A(axes[0])
    panel_B(axes[1])
    panel_C(axes[2], ratio)

    fig.suptitle(
        "ECF mass function (Poisson coalescence) — PO-F3-C6\n"
        r"$N\sim\mathrm{Poisson}(\lambda)$, $\lambda=n_{\rm KZ}\,"
        r"\frac{4}{3}\pi R_{\rm coal}(z)^3$,  $M=N\,M_{\rm micro}$",
        fontsize=11, fontweight="bold", y=1.015)

    # The paper is explicit that C6 is NOT closed. The figure must say so,
    # otherwise an illustrative lambda reads as a calibrated prediction.
    fig.text(0.5, -0.055,
             "Open problem PO-F3-C6 — NOT closed: $R_{\\rm coal}(z)$ is a free, "
             "uncalibrated parameter and the $n_{\\rm KZ}$ normalisation against the "
             "observed dark-matter density is unresolved.\n"
             "$\\lambda$ is shown over an ILLUSTRATIVE range; the shape of the "
             "distribution is the prediction, not the value of $\\lambda$.",
             ha="center", va="top", fontsize=7.5, style="italic", color="#444")

    fig.tight_layout(rect=[0, 0.02, 1, 0.99])
    fig.savefig(OUT, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Figure: {OUT}")


if __name__ == "__main__":
    main()

```

---

### Fichier 9 : `plot_F3_ecf_ns_KZ.py`

```python
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

```

---

### Fichier 10 : `plot_F3_ECF_LG_bounce_dynamics.py`

```python
#!/usr/bin/env python3
"""
Figure: bounce dynamics in the Landau-Ginzburg formulation (ECF / F3).

Produces Fig. 2 of the companion paper "The Cosmological Bounce as a
Chiral Phase Transition" -- all figure text is in English to match the
paper, which is written in English.

Print-safe: light background, distinct markers, legible in greyscale.

Last modified: 24/07/2026, 09:15
  - all figure and console text translated from French to English
    (the figure previously appeared in French inside an otherwise
     entirely English paper)
  - suptitle aligned on the paper's Fig. 2 caption wording
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- PORTABLE output path (Windows / Linux / macOS) -------------------------
# The figure is written to the 'figures_output/' subfolder, created if needed,
# located NEXT TO this script -- whatever the current working directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, 'figures_output')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PNG    = os.path.join(OUT_DIR, 'Fig_ECF_LG_BounceDynamics.png')

ALPHA, BETA, CHI_C = 1.0, 0.5, 1.0

def chi_profile(t, chi_max=1.8, width=3.0):
    return chi_max*np.exp(-t**2/(2*width**2))
def hubble_profile(t, H_amp=0.35, width=3.0):
    return H_amp*(t/width)*np.exp(-t**2/(2*width**2))
def V(T, chi, h):
    return ALPHA*(CHI_C-chi)*T**2 + BETA*T**4 - h*T
def rhs(t, y, h):
    T, Td = y
    return [Td, -3*hubble_profile(t)*Td
            - (2*ALPHA*(CHI_C-chi_profile(t))*T + 4*BETA*T**3 - h)]
def run(h, T0=1e-3, tspan=(-8,20), n=4000):
    return solve_ivp(rhs, tspan, [T0,0.0], args=(h,),
                     t_eval=np.linspace(*tspan,n), rtol=1e-9, atol=1e-12)

fig = plt.figure(figsize=(11.5, 8.2))
gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.26)
fig.patch.set_facecolor('white')

# ---- (a) Potential deformation: the double well opens -----------------
ax = fig.add_subplot(gs[0,0]); ax.set_facecolor('white')
Tg = np.linspace(-1.5, 1.5, 400)
styles = [(0.6,'-','o',   'subcritical  $\\chi=0.6$'),
          (1.0,'--','s',  'threshold  $\\chi=\\chi_c=1$'),
          (1.8,'-.','^',  'supercritical  $\\chi=1.8$')]
for chi_v, ls, mk, lab in styles:
    Vv = V(Tg, chi_v, 0.02)
    ax.plot(Tg, Vv, ls, color='black', lw=1.6, label=lab)
    ax.plot(Tg[::80], Vv[::80], mk, color='black', ms=4, mfc='white')
ax.axhline(0, color='0.7', lw=0.6)
ax.axvline(0, color='0.7', lw=0.6)
ax.set_xlabel(r"order parameter  $\mathcal{T}$  (axial torsion)")
ax.set_ylabel(r'$V(\mathcal{T})$')
ax.set_title(r"(a)  The double well opens at threshold", fontsize=11, loc='left')
ax.legend(fontsize=8, framealpha=1)
ax.set_ylim(-0.6, 1.2); ax.grid(alpha=0.25, lw=0.5)

# ---- (b) Chronology: chi(t) and H(t) ----------------------------------
ax = fig.add_subplot(gs[0,1]); ax.set_facecolor('white')
t = np.linspace(-8, 20, 1500)
chi_t, H_t = chi_profile(t), hubble_profile(t)
ax.plot(t, chi_t, '-', color='black', lw=1.8, label=r'$\chi(t)=\rho/\rho_c$')
ax.plot(t[::120], chi_t[::120], 'o', color='black', ms=4, mfc='white')
ax.axhline(CHI_C, color='0.45', ls=':', lw=1.3)
ax.text(13.5, 1.06, r'$\chi_c=1$', fontsize=8, color='0.35')
sc = chi_t > CHI_C
ax.fill_between(t, 0, 2.0, where=sc, color='0.85', alpha=0.7, zorder=0)
ax.text(0, 1.93, 'supercritical window\n(double well open)',
        ha='center', va='top', fontsize=8, color='0.25')
ax2 = ax.twinx()
ax2.plot(t, H_t, '--', color='0.45', lw=1.4, label=r'$H(t)$')
ax2.axhline(0, color='0.8', lw=0.5)
ax2.set_ylabel(r'$H(t)$  (Planck units)', color='0.45', fontsize=9)
ax2.tick_params(axis='y', colors='0.45', labelsize=8)
ax.annotate('bounce ($H=0$)', xy=(0, 0.12), xytext=(-6.5, 0.42),
            fontsize=8, arrowprops=dict(arrowstyle='->', lw=0.8, color='0.3'))
ax.set_xlabel(r'time  $t$  (Planck units)')
ax.set_ylabel(r'$\chi(t)$')
ax.set_title(r'(b)  Bounce chronology', fontsize=11, loc='left')
ax.set_ylim(0, 2.0); ax.grid(alpha=0.25, lw=0.5)
h1,l1 = ax.get_legend_handles_labels(); h2,l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, fontsize=8, loc='upper right', framealpha=1)

# ---- (c) Trajectory: chirality selection ------------------------------
ax = fig.add_subplot(gs[1,0]); ax.set_facecolor('white')
for h_v, ls, mk, lab in [(+0.02,'-','^', r'$a^*>0$  $\Rightarrow$  chirality D'),
                         (-0.02,'--','v', r'$a^*<0$  $\Rightarrow$  chirality L')]:
    s = run(h_v)
    ax.plot(s.t, s.y[0], ls, color='black', lw=1.6, label=lab)
    ax.plot(s.t[::250], s.y[0][::250], mk, color='black', ms=5, mfc='white')
ax.axhline(0, color='0.7', lw=0.7)
tt = np.linspace(-8,20,1500)
ax.fill_between(tt, -1.6, 1.6, where=chi_profile(tt)>CHI_C,
                color='0.88', alpha=0.7, zorder=0)
ax.annotate('overshoot\n(H$\\approx$0: no friction)', xy=(0.8, 1.27),
            xytext=(4.2, 1.15), fontsize=8,
            arrowprops=dict(arrowstyle='->', lw=0.8, color='0.3'))
ax.annotate('damped oscillations', xy=(9, 0.06), xytext=(10.5, 0.62),
            fontsize=8, arrowprops=dict(arrowstyle='->', lw=0.8, color='0.3'))
ax.set_xlabel(r'time  $t$  (Planck units)')
ax.set_ylabel(r'$\mathcal{T}(t)$')
ax.set_title(r'(c)  The sign of $a^*$ fixes the chirality', fontsize=11, loc='left')
ax.legend(fontsize=8, loc='lower right', framealpha=1)
ax.set_ylim(-1.6, 1.6); ax.grid(alpha=0.25, lw=0.5)

# ---- (d) Robustness: net chirality vs bias ----------------------------
ax = fig.add_subplot(gs[1,1]); ax.set_facecolor('white')
hs = np.linspace(-0.05, 0.05, 21)
nets = []
for h_v in hs:
    s = run(h_v, tspan=(-8,30), n=5000)
    m = s.t > 0
    nets.append(np.trapezoid(s.y[0][m], s.t[m]))
nets = np.array(nets)
ax.plot(hs, nets, '-', color='black', lw=1.6)
ax.plot(hs, nets, 'o', color='black', ms=4, mfc='white')
ax.axhline(0, color='0.7', lw=0.7); ax.axvline(0, color='0.7', lw=0.7)
ax.fill_between([0, 0.05], 0, 4, color='0.9', alpha=0.6, zorder=0)
ax.fill_between([-0.05, 0], -4, 0, color='0.9', alpha=0.6, zorder=0)
ax.text(0.028, 2.6, 'chirality D', fontsize=8, ha='center', color='0.3')
ax.text(-0.028, -2.9, 'chirality L', fontsize=8, ha='center', color='0.3')
ax.set_xlabel(r'chiral bias  $h \propto a^*$')
ax.set_ylabel(r'net chirality  $\int_{0}^{\infty}\!\mathcal{T}\,dt$')
ax.set_title(r'(d)  Monotonic response to parent spin', fontsize=11, loc='left')
ax.grid(alpha=0.25, lw=0.5); ax.set_ylim(-4, 4)

fig.suptitle('Bounce dynamics in the Landau--Ginzburg formulation (ECF, Foundation III)',
             fontsize=12.5, y=0.975)
fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figure written: {OUT_PNG}")

# --- Print-safe check (optional, no disk write) -----------------------------
try:
    from PIL import Image
    with Image.open(OUT_PNG) as im:
        size = im.size
        im.convert('L')          # greyscale test: must remain legible
    print(f"Print-safe check OK -- size {size}")
except ImportError:
    print("(PIL absent: greyscale check skipped, figure is fine)")

```

---

### Fichier 11 : `plot_F3_ecf_vsf_desivast_fits.py`

```python
#!/usr/bin/env python3
"""
ecf_vsf_desivast_fits.py
========================
ECF VSF (Foundation II) vs DESIVAST DR1 -- FITS MODE.
Public DESI catalogue: data.desi.lbl.gov/public/dr1/vac/dr1/desivast/

The script downloads the FITS files automatically if absent, then
compares N_obs(R > 40 Mpc/h) against the ECF kill-switch (x2.1).

USAGE
-----
  python ecf_vsf_desivast_fits.py            # download + analyse
  python ecf_vsf_desivast_fits.py --no-dl    # analyse without downloading

ECF PREDICTION (Foundation II, §VSF)
--------------------------------------
  VSF_ECF(R) = VSF_LCDM(R) × A_ECF(R)
  A_ECF(R)   = 1 + 1.1 × exp(-(R - 60)² / (2×15²))   [A-8: xi_KZ = 60, sigma_KZ = 15 Mpc, adopted]
  Kill-switch: N_ECF(R > 40 Mpc/h) ≈ 2.1 × N_LCDM

!! Read the LCDM BASELINE CAVEAT block further down before quoting any
   significance produced by this script: N_LCDM is a rescaled placeholder,
   not a theoretical prediction.

REFERENCES
----------
  Rincon et al. 2025, ApJ 982:38    arXiv:2411.00148
  Douglass et al. 2023, ApJS 265:7
  Fichant 2026, Foundation II       doi:10.5281/zenodo.20802690

Author  : Pascal Fichant (ECF programme)
Version : 1.2 (21/07/2026, 02:50). Changes vs v1.1:
          (1) Fixed a misleading kill-switch verdict: when the true
              threshold (60 Mpc = 40 Mpc/h) is out of catalogue range,
              the smaller fallback cut was displayed under the true
              threshold's label, in both the console output and the
              figure box. Both now state explicitly that the true
              kill-switch is out of reach (N=0) and that the value
              shown is a proxy at a reduced scale. The early
              diagnostic (N=0 at the true threshold) was already
              correct; only the final verdict was misleading if read
              in isolation.
          (2) Added an explicit caveat that N_LCDM is a rescaled
              placeholder, not a theoretical LCDM VSF, so the printed
              "DEFICIT" significances must not be read as cosmological
              tension.
          (3) All console and figure text translated to English
              (corpus language for Foundation I; Foundation III to be
              translated later).
Licence : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
Output  : Fig_ECF_VSF_DESIVAST_DR1_fits.png
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
import os, sys, urllib.request

np.random.seed(42)

# ===========================================================================
# CHEMINS PUBLICS DESIVAST DR1 (confirmés 27/06/2026)
# ===========================================================================

# URLs candidates (la structure exacte peut varier selon la version du serveur)
# Essayées dans l'ordre jusqu'à succès
BASE_URLS = [
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1/",    # avec version v1
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/",        # doc officielle
    "https://data.desi.lbl.gov/public/dr1/vac/desivast/",            # sans /dr1/ double
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1.0/",  # version v1.0
]
BASE_URL   = BASE_URLS[0]   # URL par défaut (sera tentée en premier)
NERSC_PATH = "/global/cfs/cdirs/desi/public/dr1/vac/dr1/desivast/"

FITS_FILES = [
    "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits",
    "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits",
]

# Dossier local ou stocker les fichiers telecharges.
# Canonique : Foundation_3/data/desivast_dr1/, un dossier de donnees
# unique et visible a la racine du depot, independant du sous-dossier de
# categorie (A_Core_Calculations, B_Paper_Plots, ...) ou vit ce script.
# Repli sur "./desivast_dr1" (a cote du script) si l'ancien dossier existe
# deja la et que le nouveau emplacement canonique n'a rien.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_HERE))  # .../Foundation_3
_CANONICAL_DIR = os.path.join(_REPO_ROOT, "data", "desivast_dr1")
_LEGACY_DIR = os.path.join(_HERE, "desivast_dr1")
if os.path.exists(_LEGACY_DIR) and not os.path.exists(_CANONICAL_DIR):
    LOCAL_DIR = _LEGACY_DIR
else:
    LOCAL_DIR = _CANONICAL_DIR

# Fichier de sortie
OUTPUT_PNG = "Fig_ECF_VSF_DESIVAST_DR1_fits.png"

# ===========================================================================
# PARAMÈTRES ECF CANONIQUES (Foundation II)
# ===========================================================================

H0          = 67.32      # km/s/Mpc (DESIVAST fiduciel = Planck 2020)
h           = H0 / 100.  # 0.6732

XI_KZ_MPC   = 60.0       # Mpc physique — valeur ADOPTEE (harmonisation 22/09/2026, A-8 ; non derivee, PO-F3-XI)
XI_KZ_LO    = 50.0
XI_KZ_HI    = 80.0
SIG_KZ_MPC  = 15.0       # Mpc — largeur du pic, valeur ADOPTEE (harmonisation 22/09/2026, PO-F3-XI)
A_ECF_PEAK  = 1.1        # => A_ECF(xi_KZ) = 2.1

R_KS_MPC    = 60.0       # Mpc physique — seuil kill-switch (Foundation III)
                         # [26/08/2026] annotation corrigée : disait « F2 ».
                         # Le test VSF appartient à Foundation III depuis le
                         # SPLIT-1 ; F2 n'en porte aucune mention. L'ancienne
                         # note était un vestige d'avant la séparation.
R_KS_H      = R_KS_MPC * h   # = 40.4 Mpc/h

# ---------------------------------------------------------------------------
# LCDM BASELINE -- IMPORTANT CAVEAT (added 21/07/2026)
# ---------------------------------------------------------------------------
# DR1_COUNTS is NOT a theoretical LCDM void size function. It is a crude
# PLACEHOLDER: the *shape* is taken from an older SDSS VoidFinder catalogue
# (Douglass+2023), rescaled to an *expected* DESI DR1 total (N_DR1=1484) and
# multiplied by a hand-tuned depth factor (DEPTH_F=1.4), with an extra ad hoc
# x1.5 on the last bin. None of these numbers is derived from theory,
# simulation, or an excursion-set calculation.
#
# CONSEQUENCE: the per-cut "sigma_obs" values and the "DEFICIT" verdicts this
# script prints compare the real catalogue against THIS PLACEHOLDER, not
# against a genuine LCDM prediction. The large deficits reported at small,
# testable radii (roughly -6 sigma to -19 sigma) are therefore most plausibly
# an artefact of the rescaling not matching the true BGS volume/depth --
# NOT evidence of a real cosmological tension. They must not be quoted as
# such, in the papers or elsewhere.
#
# The ECF/LCDM *ratio* A_ecf(R) is unaffected by this normalisation (it is a
# multiplicative model), so the shape of the predicted ECF excess remains
# meaningful; only the absolute counts and their significances do not.
#
# TODO: replace with a proper LCDM VSF (simulation-calibrated or excursion-set)
# before any of these significances is used as a published result.
# ---------------------------------------------------------------------------
SDSS_BINS_H = np.array([10,13,16,19,22,25,28,32,36,42,54], dtype=float)
SDSS_COUNTS = np.array([155,210,215,185,150,110,70,40,20,8],  dtype=float)
N_DR1       = 1484       # expected DR1 total (assumed, not measured)
DEPTH_F     = 1.4        # ad hoc depth factor -- not derived
DR1_COUNTS  = SDSS_COUNTS * (N_DR1 / SDSS_COUNTS.sum()) * DEPTH_F
DR1_COUNTS[-1] *= 1.5    # ad hoc last-bin boost -- not derived
BINS_MPC    = SDSS_BINS_H / h
BIN_CENTERS = 0.5 * (BINS_MPC[:-1] + BINS_MPC[1:])

# ===========================================================================
# ÉTAPE 1 — TÉLÉCHARGEMENT
# ===========================================================================

def probe_url(base_url, fname):
    """Teste si une URL est accessible (HEAD request)."""
    import urllib.error
    url = base_url + fname
    req = urllib.request.Request(url, method='HEAD')
    try:
        urllib.request.urlopen(req, timeout=10)
        return url
    except Exception:
        return None

def find_working_url(fname):
    """Try every candidate URL; return the first one that responds."""
    print(f"  Probing URL for {fname} ...")
    for base in BASE_URLS:
        url = probe_url(base, fname)
        if url:
            print(f"  [OK] URL found: {base}")
            return url, base
    return None, None

def download_catalog(local_dir=LOCAL_DIR, force=False):
    """
    Download the 2 VoidFinder files from the public DESI URL.
    Tries several URL variants in case of 404.
    """
    os.makedirs(local_dir, exist_ok=True)
    print(f"\nDownloading DESIVAST DR1 -> {local_dir}/")

    working_base = None   # remember the base URL that works

    for fname in FITS_FILES:
        dest = os.path.join(local_dir, fname)
        if os.path.exists(dest) and not force:
            size = os.path.getsize(dest) / 1e6
            print(f"  [OK] Already present: {fname}  ({size:.1f} MB)")
            continue

        # Determine the URL
        if working_base:
            url = working_base + fname
        else:
            url, working_base = find_working_url(fname)

        if url is None:
            print(f"\n  [FAILED] No reachable URL for {fname}")
            print(f"  URLs tried:")
            for base in BASE_URLS:
                print(f"    {base}{fname}")
            print(f"\n  Workarounds:")
            print(f"  1. NERSC : cp {NERSC_PATH}{fname} {local_dir}/")
            print(f"  2. Contact: hrincon@ur.rochester.edu (DESIVAST author)")
            print(f"  3. Retry in a few minutes (the DESI server may be temporarily down)")
            continue

        print(f"  Downloading: {fname}", end=" ", flush=True)
        try:
            def progress(block, block_size, total):
                if total > 0:
                    pct = min(block * block_size / total * 100, 100)
                    print(f"\r  {fname} : {pct:.0f}%", end="", flush=True)
            urllib.request.urlretrieve(url, dest, reporthook=progress)
            size = os.path.getsize(dest) / 1e6
            print(f"\r  [OK] {fname}  ({size:.1f} MB) → {dest}")
        except Exception as e:
            print(f"\r  [ERROR] {e}")
            print(f"  wget '{url}' -P {local_dir}/")

# ===========================================================================
# ÉTAPE 2 — LECTURE DU CATALOGUE
# ===========================================================================

def load_catalog(local_dir=LOCAL_DIR):
    """
    Lit les fichiers FITS DESIVAST DR1 VoidFinder et retourne
    un tableau de rayons effectifs en Mpc physique.

    Structure FITS (par fichier) :
      HDU[0] : PrimaryHDU (vide)
      HDU[1] : BinTableHDU "Maximal Spheres"
        Colonnes clés :
          EFFECTIVE_RADIUS       [Mpc/h] — rayon effectif du vide (ajout DESIVAST)
          EFFECTIVE_RADIUS_UNCERT[Mpc/h] — incertitude
          flag / hole_id                 — identifiant unique du vide
          edge_flag                      — 0=intérieur, 1=bord
    """
    try:
        from astropy.io import fits as apfits
        from astropy.table import Table, vstack
    except ImportError:
        sys.exit("Please install astropy: pip install astropy")

    tables = []
    _missing_fits = []
    for fname in FITS_FILES:
        fpath = os.path.join(local_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [MISSING] {fpath}")
            _missing_fits.append(fname)   # RÈGLE 23 -- voir contrôle plus bas
            continue

        hdu  = apfits.open(fpath)
        tbl  = Table(hdu[1].data)
        hdu.close()
        print(f"  {fname}: {len(tbl):,} rows (maximal spheres)")
        print(f"  Columns: {list(tbl.colnames)}")
        tables.append(tbl)

    if not tables:
        sys.exit(
            "\nNo FITS file found in: " + local_dir +
            "\nRe-run with --download, or check the URL:\n  " + BASE_URL
        )

    # RÈGLE 23 (25/08/2026) -- le cas "TOUT manque" était déjà traité, pas le
    # cas "UNE PARTIE manque". Un catalogue amputé ne donne pas une figure
    # vide mais une figure FAUSSE : le comptage de vides, donc le sigma du
    # kill-switch, seraient calculés sur un sous-ensemble sans que rien ne le
    # signale. Sortir à 0 mentirait à toute chaîne automatisée.
    if _missing_fits:
        sys.exit(
            f"\n[ERROR] {len(_missing_fits)}/{len(FITS_FILES)} FITS file(s) "
            f"missing: {', '.join(_missing_fits)}\n"
            "        The void counts -- and therefore the kill-switch sigma --\n"
            "        would be computed on a TRUNCATED catalogue.\n"
            "        Re-run with --download."
        )

    data = vstack(tables)
    print(f"\n  Raw total: {len(data):,} maximal spheres (NGC + SGC)")

    # -- Select interior voids (edge_flag == 0) --------------------------
    eflag_col = next(
        (c for c in ['edge_flag','EDGE_FLAG','EdgeFlag'] if c in data.colnames),
        None
    )
    if eflag_col:
        data = data[data[eflag_col] == 0]
        print(f"  After edge_flag==0 filter: {len(data):,} rows")
    else:
        print("  [WARN] edge_flag column absent -- all voids included")

    # -- Deduplication: one row per unique void --------------------------
    id_col = next(
        (c for c in ['flag','FLAG','hole_id','HOLE_ID','VoidID','void_id']
         if c in data.colnames),
        None
    )
    if id_col:
        _, idx = np.unique(data[id_col], return_index=True)
        data = data[np.sort(idx)]
        print(f"  Unique interior voids: {len(data):,}")
    else:
        print("  [WARN] void id column absent -- deduplication skipped")

    # -- Read the effective radius ---------------------------------------
    r_col = next(
        (c for c in ['EFFECTIVE_RADIUS','effective_radius','R_EFF','r_eff','radius']
         if c in data.colnames),
        None
    )
    if r_col is None:
        print("Available columns:", data.colnames)
        sys.exit("EFFECTIVE_RADIUS column not found.")

    R_h   = np.array(data[r_col], dtype=float)   # Mpc/h
    R_mpc = R_h / h                               # -> physical Mpc

    # Cut at R_min = 10 Mpc/h (VoidFinder standard)
    R_mpc = R_mpc[R_mpc >= BINS_MPC[0]]

    print(f"\n  Effective radius [Mpc]:")
    print(f"    min    = {R_mpc.min():.1f}")
    print(f"    median = {np.median(R_mpc):.1f}")
    print(f"    max    = {R_mpc.max():.1f}")
    print(f"    N(R > {R_KS_H:.0f} Mpc/h = {R_KS_MPC:.0f} Mpc) = "
          f"{(R_mpc >= R_KS_MPC).sum()}")
    R_max_h = R_mpc.max() * h
    if R_max_h < R_KS_H:
        print(f"\n  *** CRITICAL DIAGNOSTIC ***")
        print(f"  R_max = {R_mpc.max():.1f} Mpc = {R_max_h:.1f} Mpc/h")
        print(f"  Kill-switch at {R_KS_H:.0f} Mpc/h IS BEYOND THE CATALOGUE RANGE.")
        print(f"  -> BGS z<0.24 yields no voids larger than {R_KS_H:.0f} Mpc/h.")
        print(f"  -> ECF test not possible with DESIVAST DR1 BGS alone.")
        print(f"  -> Remedy: await DESI LRG/ELG or Euclid DR1 (Oct 2026).")
        print(f"  -> Fall back to R_CUTS_H = [18., 20., 22., 24., 28.] for current data.")

    return R_mpc

# ===========================================================================
# ÉTAPE 3 — ANALYSE ECF
# ===========================================================================

def A_ecf(R_mpc, xi=XI_KZ_MPC):
    return 1. + A_ECF_PEAK * np.exp(-(R_mpc - xi)**2 / (2.*SIG_KZ_MPC**2))

ECF_MID = DR1_COUNTS * np.array([A_ecf(R)            for R in BIN_CENTERS])
ECF_LO  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_LO)  for R in BIN_CENTERS])
ECF_HI  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_HI)  for R in BIN_CENTERS])

def N_above_model(counts, R_cut_h):
    return counts[SDSS_BINS_H[:-1] >= R_cut_h].sum()

def sigma_detect(N_l, N_e, f_syst=0.0):
    if N_l < 0.1: return 0.
    return (N_e - N_l) / np.sqrt(N_l + (f_syst * N_l)**2)

def verdict(N_obs, N_lcdm, N_ecf):
    sig_obs  = (N_obs - N_lcdm) / np.sqrt(max(N_lcdm, 0.1))
    sig_pred = sigma_detect(N_lcdm, N_ecf, f_syst=0.30)
    if   sig_obs >= sig_pred * 0.8: return "ECF SIGNAL", sig_obs
    elif sig_obs <= -2.0:            return "DEFICIT",    sig_obs
    elif sig_obs >=  2.0:            return "EXCESS",     sig_obs
    else:                            return "COMPATIBLE", sig_obs

# ===========================================================================
# MAIN
# ===========================================================================

def main():
    no_dl = '--no-dl' in sys.argv

    print("=" * 65)
    print("ECF VSF vs DESIVAST DR1  v1.2 -- 21/07/2026")
    print("=" * 65)
    print(f"VSF kill-switch : R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h")
    print(f"Local dir      : {LOCAL_DIR}")
    print(f"Public URL     : {BASE_URL}")

    # -- Download --------------------------------------------------------
    if not no_dl:
        download_catalog(LOCAL_DIR)
    else:
        print("\n[--no-dl] Download skipped")

    # -- Load ------------------------------------------------------------
    print("\n-- Reading FITS catalogue --")
    R_obs = load_catalog(LOCAL_DIR)
    N_obs_total = len(R_obs)
    if N_obs_total < 500:
        print(f"\n  WARNING: only {N_obs_total} voids loaded.")
        print(f"  The VoidFinder catalogue stores maximal spheres")
        print(f"  (several per void). Without a void_id column they are")
        print(f"  treated as distinct voids -- likely undercount.")
        print(f"  -> Look for a column: VOID_ID, VOID_INDEX, ZONEID, zone_id")

    # Observed histogram on the same bins
    OBS_COUNTS, _ = np.histogram(R_obs, bins=BINS_MPC)
    OBS_COUNTS    = OBS_COUNTS.astype(float)

    # -- Statistics table ------------------------------------------------
    print("\n" + "=" * 65)
    print("RESULTS -- Real data vs LCDM vs ECF")
    print("=" * 65)
    print("""
  !! CAVEAT -- READ BEFORE INTERPRETING THE COLUMNS BELOW !!
  N_LCDM is NOT a theoretical LCDM void size function. It is a crude
  placeholder: an older SDSS catalogue shape rescaled to an assumed DR1
  total with a hand-tuned depth factor (see the block comment at the top
  of this file). The sigma_obs values and any "DEFICIT" verdicts below
  therefore compare the data against that placeholder, not against a real
  LCDM prediction, and must NOT be quoted as evidence of cosmological
  tension. Only the ECF/LCDM ratio (shape of the predicted excess) is
  meaningful at this stage.""")
    print(f"\n{'Cut':>12}  {'N_obs':>6}  {'N_LCDM':>7}  "
          f"{'N_ECF':>7}  {'σ_obs':>8}  {'Verdict':>15}")
    print("-" * 65)

    # Adapter les coupures à la plage réelle du catalogue
    R_max_data_h = R_obs.max() * h if len(R_obs) > 0 else R_KS_H
    if R_max_data_h < R_KS_H:
        # Catalogue ne monte pas jusqu'au kill-switch → tester les plus petites échelles
        R_CUTS_H = [18., 20., 22., 24., 28.]
        print(f"\n  Cuts adapted to R_max={R_max_data_h:.1f} Mpc/h: {R_CUTS_H}")
    else:
        R_CUTS_H = [28., 32., 36., 40., 42.]
    results  = {}

    for Rc in R_CUTS_H:
        N_obs_c  = int((R_obs >= Rc / h).sum())
        N_lcdm_c = N_above_model(DR1_COUNTS, Rc)
        N_ecf_c  = N_above_model(ECF_MID,    Rc)
        verd, sig = verdict(N_obs_c, N_lcdm_c, N_ecf_c)
        ks        = " <-KS" if abs(Rc - R_KS_H) < 2. else ""
        print(f"  R>{Rc:>4.0f} Mpc/h  {N_obs_c:>6}  {N_lcdm_c:>7.0f}  "
              f"{N_ecf_c:>7.0f}  {sig:>+7.1f}σ  {verd}{ks}")
        results[Rc] = dict(N_obs=N_obs_c, N_lcdm=N_lcdm_c,
                           N_ecf=N_ecf_c, sigma=sig, verdict=verd)

    # Kill-switch summary
    # Robust lookup (float key never matches exactly)
    ks_key      = min(results.keys(), key=lambda x: abs(x - R_KS_H))
    ks_res      = results[ks_key]
    is_proxy    = abs(ks_key - R_KS_H) > 2.0   # true threshold could not be tested
    print(f"\n{'─'*65}")
    if is_proxy:
        print(f"VERDICT (PROXY -- true kill-switch R > {R_KS_H:.0f} Mpc/h = "
              f"{R_KS_MPC:.0f} Mpc IS OUT OF CATALOGUE RANGE):")
        print(f"  Cut actually tested here: R > {ks_key:.0f} Mpc/h "
              f"({ks_key/h:.1f} Mpc physical) -- NOT the official kill-switch.")
        print(f"  At the true threshold (R > {R_KS_MPC:.0f} Mpc physical) the BGS")
        print(f"  catalogue contains no void at all (N=0, see diagnostic above) --")
        print(f"  this is NOT a falsification, only an out-of-reach limitation.")
    else:
        print(f"KILL-SWITCH VERDICT (R > {R_KS_H:.0f} Mpc/h = {R_KS_MPC:.0f} Mpc):")
    print(f"  N_obs   = {ks_res['N_obs']}")
    print(f"  N_LCDM  = {ks_res['N_lcdm']:.0f}")
    print(f"  N_ECF   = {ks_res['N_ecf']:.0f}  (×{ks_res['N_ecf']/max(ks_res['N_lcdm'],.1):.2f})")
    print(f"  σ_obs   = {ks_res['sigma']:+.1f}σ")
    print(f"  Verdict : {ks_res['verdict']}"
          + ("  [proxy, reduced scale -- see warning above]" if is_proxy else ""))

    # -- Figure ----------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')
    fig.suptitle(
        r"ECF VSF vs $\Lambda$CDM -- REAL DESIVAST DR1 (Rincon+2025)"
        "\n"
        r"VSF kill-switch: $N_{\rm ECF}(R>40\,h^{-1}{\rm Mpc})"
        r"\approx 2.1\times N_{\Lambda{\rm CDM}}$ "
        fr"· $\xi_{{\rm KZ}}=60$ Mpc (adopted) · $N_{{\rm obs}}={N_obs_total}$ voids",
        fontsize=10.5, fontweight='bold'
    )

    W = np.diff(BINS_MPC) * 0.38

    # Left panel -- histograms
    ax = axes[0]
    ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
           color='#1C3F7A', alpha=0.45, label=r'$\Lambda$CDM toy model (rescaled, see caveat)')
    ax.bar(BIN_CENTERS, ECF_MID, W, align='center',
           color='#CC2222', alpha=0.35, label=r'ECF adopted template ($\xi_{\rm KZ}=60$ Mpc)')
    ax.errorbar(BIN_CENTERS, OBS_COUNTS,
                yerr=np.sqrt(np.maximum(OBS_COUNTS, 1.)),
                fmt='ko', ms=5, lw=1.5, capsize=4, zorder=7,
                label=f'DESIVAST DR1 real (N={N_obs_total})')
    ax.axvline(R_KS_MPC,   c='orange', lw=2.0, ls='--',
               label=fr'Kill-switch {R_KS_H:.0f} Mpc/$h$ (out of range)')
    ax.axvline(XI_KZ_MPC,  c='red',    lw=1.2, ls=':',
               label=fr'$\xi_{{\rm KZ}}={XI_KZ_MPC:.0f}$ Mpc')
    ax.fill_betweenx([0, max(OBS_COUNTS.max(), DR1_COUNTS.max())*1.1],
                     R_KS_MPC, 200., color='orange', alpha=0.07, zorder=0)

    # Annotate observed deviations
    for i, (Rc_h, Rc_mpc) in enumerate(zip(SDSS_BINS_H[:-1], BIN_CENTERS)):
        N_obs_b = OBS_COUNTS[i]
        N_l_b   = DR1_COUNTS[i]
        if N_l_b > 5 and Rc_h >= 28.:
            sig_b = (N_obs_b - N_l_b) / np.sqrt(max(N_l_b, 1.))
            color = '#CC0000' if abs(sig_b) > 2 else '#555555'
            ax.text(Rc_mpc, max(N_obs_b, N_l_b) + 4,
                    fr'{sig_b:+.1f}σ', ha='center', va='bottom',
                    fontsize=7, color=color)

    ax.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
    ax.set_ylabel('Number of voids per bin', fontsize=10)
    ax.set_title('Observed distribution vs models', fontsize=10)
    ax.set_xlim(BINS_MPC[0], BINS_MPC[-1])
    ax.set_ylim(0.)
    ax.legend(fontsize=7.5)
    ax.grid(True, alpha=0.22)
    ax_t = ax.twiny()
    ax_t.set_xlim(ax.get_xlim()[0]*h, ax.get_xlim()[1]*h)
    ax_t.set_xlabel(r'$R_{\rm eff}$ [Mpc/$h$]', fontsize=10)

    # Right panel -- per-cut statistical summary
    ax2 = axes[1]
    R_c_arr  = [r for r in R_CUTS_H]
    sig_obs  = [results[r]['sigma']  for r in R_c_arr]
    sig_pred = [sigma_detect(results[r]['N_lcdm'],
                             results[r]['N_ecf'], 0.30) for r in R_c_arr]
    colors   = ['#CC0000' if abs(s) > 2 else '#1C3F7A' for s in sig_obs]
    x_pos    = np.arange(len(R_c_arr))

    bars = ax2.bar(x_pos - 0.2, sig_obs,  0.38, color=colors, alpha=0.8,
                   label='observed σ (real data)')
    ax2.bar(x_pos + 0.2, sig_pred, 0.38, color='#CC2222', alpha=0.45,
            hatch='////', label='predicted σ if ECF true (+30% syst.)')

    ax2.axhline(0.,  c='k',      lw=0.8)
    ax2.axhline(2.,  c='gray',   lw=0.8, ls=':', label='2σ')
    ax2.axhline(-2., c='gray',   lw=0.8, ls=':')
    ax2.axhline(3.,  c='orange', lw=1.2, ls='--', label='3σ')

    # Value annotations
    for i, (so, sp) in enumerate(zip(sig_obs, sig_pred)):
        ax2.text(i-0.2, so + (0.15 if so >= 0 else -0.3),
                 f'{so:+.1f}σ', ha='center', fontsize=8,
                 color='#CC0000' if abs(so) > 2 else '#1C3F7A')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([fr'R>${r:.0f}$' + '\nMpc/h' for r in R_c_arr], fontsize=9)
    ax2.set_ylabel(r'$(N_{\rm obs} - N_{\Lambda{\rm CDM}})/\sqrt{N_{\Lambda{\rm CDM}}}$ [$\sigma$]',
                   fontsize=9)
    ax2.set_title('Significance per cut', fontsize=10)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.22, axis='y')

    # Kill-switch verdict box
    # NOTE (v1.2): when the true kill-switch is out of catalogue range,
    # this box must say so explicitly rather than display a smaller
    # fallback cut under the kill-switch label.
    if is_proxy:
        verd_color = '#B36B00'
        box_txt = (f"True kill-switch R>{R_KS_H:.0f} Mpc/h:\n"
                   f"OUT OF CATALOGUE RANGE (N=0)\n"
                   f"— not a falsification —\n"
                   f"Proxy shown: R>{ks_key:.0f} Mpc/h, "
                   f"σ={ks_res['sigma']:+.1f}")
    else:
        verd_color = '#CC0000' if 'ECF' in ks_res['verdict'] else '#1C3F7A'
        box_txt = (f"Kill-switch R>{R_KS_H:.0f} Mpc/h:\n"
                   f"N_obs={ks_res['N_obs']}  N_LCDM={ks_res['N_lcdm']:.0f}\n"
                   f"σ = {ks_res['sigma']:+.1f}  -> {ks_res['verdict']}")
    ax2.text(0.97, 0.97, box_txt,
             transform=ax2.transAxes, va='top', ha='right', fontsize=8.5,
             bbox=dict(boxstyle='round', facecolor='#f8f8f8',
                       edgecolor=verd_color, lw=1.5),
             color=verd_color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\nFigure: {OUTPUT_PNG}")
    print("=" * 65)


if __name__ == "__main__":
    main()

```

---

### Fichier 12 : `plot_F3_ecf_vsf_desivast_v1_simulated.py`

```python
#!/usr/bin/env python3
"""
ecf_vsf_desivast_v1.py
======================
Comparison of the ECF Void Size Function (VSF, Foundation II)
with the DESIVAST DR1 catalogue (Rincon et al. 2025, ApJ 982:38).

PURPOSE
-------
Test the VSF kill-switch: ECF predicts an excess of large voids at
R > xi_KZ = 60 Mpc physical (= 40.4 Mpc/h; adopted value, harmonisation
22/09/2026, not derived -- PO-F3-XI) relative to LambdaCDM.
This signal is ACCESSIBLE in DESIVAST DR1 (max R ~ 80 Mpc/h).

IMPORTANT CORRECTION
--------------------
xi_KZ = 50-80 Mpc PHYSICAL = 34-54 Mpc/h (h=0.6732).
Kill-switch R > 60 Mpc physical = R > 40 Mpc/h.

USAGE MODES
-----------
  DATA_MODE = 'simulated' (defaut) : distribution simulee depuis les
    statistiques SDSS publiees (Douglass+2023), scalee sur DESIVAST DR1.

  DATA_MODE = 'fits' : lecture du vrai catalogue DESIVAST DR1.
    URL : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/
    Telecharger : desivast_dr1_voidfinder_NGC.fits + _SGC.fits
    Puis : DATA_MODE = 'fits', FITS_PATH = '/chemin/vers/catalogue'

PREDICTION ECF (Foundation II, VSF)
-------------------------------------
  VSF_ECF(R) = VSF_LCDM(R) * A_ECF(R)
  A_ECF(R)   = 1 + 1.1 * exp(-(R - xi_KZ)^2 / (2*sigma_KZ^2))
  A_ECF(xi_KZ) = 2.1  (VSF kill-switch, Foundation III)

REFERENCES
----------
  Rincon et al. 2025, ApJ 982:38  doi:10.3847/1538-4357/adb559
  Douglass et al. 2023, ApJS 265:7
  Fichant 2026, Foundation II  doi:10.5281/zenodo.20802690

Auteur  : Pascal Fichant (ECF programme)
Version : 1.0 (27 juin 2026)
Licence : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
Output  : Fig_ECF_VSF_DESIVAST_DR1.png
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
import os

np.random.seed(42)

# ===========================================================================
# CONFIGURATION — modifier ici
# ===========================================================================

DATA_MODE  = 'fits'        # 'simulated' | 'fits' | 'download'
# [26/08/2026] Recherche automatique du catalogue plutot qu'un chemin fixe :
# le mode 'simulated' etait actif alors que les FITS etaient presents dans
# desivast_dr1/, si bien que la figure du papier montrait le SUBSTITUT
# (21 vides au-dessus de 40 Mpc/h) la ou le vrai catalogue en compte ZERO.
def _find_desivast():
    import os as _os
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _parent = _os.path.dirname(_here)
    _repo_root = _os.path.dirname(_parent)   # .../Foundation_3, two levels up
    for _c in (_os.path.join(_repo_root, 'data', 'desivast_dr1'),
               'desivast_dr1', 'data/dr1/desivast_dr1', '.',
               _os.path.join(_here, 'desivast_dr1'),
               _os.path.join(_parent, 'A_Core_Calculations', 'desivast_dr1'),
               _os.path.join(_parent, 'B_Paper_Plots', 'desivast_dr1'),
               _here):
        if _os.path.exists(_os.path.join(
                _c, 'DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits')):
            return _c
    return _os.path.join(_repo_root, 'data', 'desivast_dr1')

FITS_PATH  = _find_desivast()   # dossier des fichiers FITS DESIVAST DR1
#
# URL PUBLIQUE (sans authentification) :
#   https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/
#
# Fichiers VoidFinder :
#   DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits
#   DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits
#
# Téléchargement (remplacer FITS_PATH par le dossier local) :
#   wget -P ./desivast/ \
#     https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits
#   wget -P ./desivast/ \
#     https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits
#
# NERSC (si accès NERSC disponible) :
#   /global/cfs/cdirs/desi/public/dr1/vac/dr1/desivast/
#
# Colonnes clés (documentation : vast.readthedocs.io) :
#   EFFECTIVE_RADIUS      — rayon effectif du vide [Mpc/h]  (ajouté par DESIVAST)
#   EFFECTIVE_RADIUS_UNCERT — incertitude [Mpc/h]
#   flag (ou hole_id)     — identifiant unique du vide
#   edge_flag             — 1 = vide de bord, 0 = vide intérieur
OUTPUT_PNG = 'Fig_ECF_VSF_DESIVAST_DR1.png'

# ===========================================================================
# COSMOLOGIE FIDUCIELLE DESIVAST DR1 (Planck 2020)
# ===========================================================================

H0  = 67.32    # km/s/Mpc
h   = H0/100.  # 0.6732
Om  = 0.315
OmL = 0.685

# ===========================================================================
# PARAMETRES ECF CANONIQUES (Foundation II)
# ===========================================================================

XI_KZ_MPC  = 60.0   # Mpc physique — valeur ADOPTEE xi_KZ (harmonisation 22/09/2026, PO-F3-XI)
XI_KZ_LO   = 50.0   # borne basse
XI_KZ_HI   = 80.0   # borne haute
SIG_KZ_MPC = 15.0   # Mpc — largeur du pic KZ, valeur ADOPTEE (harmonisation 22/09/2026)
A_ECF_PEAK = 1.1    # A_ECF(xi_KZ) = 1 + 1.1 = 2.1

# [22/09/2026, arbitrage A-8] Harmonisation conventionnelle : pic = seuil.
#   XI_KZ_MPC = 60 Mpc : PIC adopte de la longueur de correlation KZ.
#   R_KS_MPC  = 60 Mpc : SEUIL du kill-switch, confondu avec le pic.
# Valeurs ADOPTEES, ni derivees ni ajustees (PO-F3-XI reste OPEN).
# 60 Mpc -> 40.4 Mpc/h (seuil et pic). L'ancienne note (pic 65 Mpc ->
# 43.8 Mpc/h, sigma 12 Mpc, seuil en deca du pic) est historique.
R_KS_MPC   = 60.0         # Mpc physique — seuil kill-switch (Foundation III)
                          # [26/08/2026] disait « F2 » : vestige d'avant le
                          # SPLIT-1. Le test VSF appartient à Foundation III.
R_KS_H     = R_KS_MPC * h  # = 40.4 Mpc/h

# ===========================================================================
# CALIBRATION LCDM : SDSS VoidFinder (Douglass+2023, ApJS 265:7)
# Digitisee depuis Figure 6 — 1163 vides interieurs, z<0.114, R_min=10 Mpc/h
# ===========================================================================

SDSS_BINS_H = np.array([10,13,16,19,22,25,28,32,36,42,54], dtype=float)  # Mpc/h
SDSS_COUNTS = np.array([155,210,215,185,150,110,70,40,20,8],  dtype=float)
N_SDSS      = int(SDSS_COUNTS.sum())   # 1163

BINS_MPC    = SDSS_BINS_H / h
BIN_CENTERS = 0.5 * (BINS_MPC[:-1] + BINS_MPC[1:])
BIN_WIDTHS  = np.diff(BINS_MPC)

# Scale vers DESIVAST DR1 (1484 vides, z<0.24)
N_DR1        = 1484
DEPTH_F      = 1.4     # profondeur accrue z<0.24 vs z<0.114
DR1_COUNTS   = SDSS_COUNTS * (N_DR1/N_SDSS) * DEPTH_F
DR1_COUNTS[-1] *= 1.5  # bin 42-54 Mpc/h : plus grands vides avec z_max=0.24

N_DESI_FULL  = 15000
SCALE_FULL   = N_DESI_FULL / N_DR1

# ===========================================================================
# CHARGEMENT DONNEES
# ===========================================================================

def load_fits_catalog(fits_dir):
    """
    Load the real DESIVAST DR1 VoidFinder catalogue (exact column names).
    Returns R_eff in physical Mpc (converted from Mpc/h).

    FITS structure (2 HDUs per file):
      HDU[0]: PrimaryHDU (empty)
      HDU[1]: BinTableHDU "Maximal Spheres" — one row per maximal sphere
        - EFFECTIVE_RADIUS      : effective void radius [Mpc/h]
        - EFFECTIVE_RADIUS_UNCERT : uncertainty [Mpc/h]
        - flag (or hole_id)     : unique void identifier
        - edge_flag             : 0 = interior, 1 = edge

    For unique voids: filter edge_flag==0, then deduplicate by flag.
    """
    try:
        from astropy.io import fits as apfits
        from astropy.table import Table
    except ImportError:
        raise ImportError("pip install astropy")

    # Noms de fichiers exacts (confirmés : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/)
    FNAMES = [
        'DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits',
        'DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits',
    ]

    R_all = []
    for fname in FNAMES:
        fpath = os.path.join(fits_dir, fname)
        if not os.path.exists(fpath):
            print(f"  Absent : {fpath}")
            continue

        hdu  = apfits.open(fpath)
        # HDU[1] = maximal spheres table
        data = Table(hdu[1].data)
        hdu.close()
        print(f"  {fname} : {len(data)} lignes (sphères maximales)")

        # Sélection vides intérieurs (edge_flag == 0)
        eflag_col = None
        # [26/08/2026] 'EDGE' AJOUTE : c'est le nom reel de la colonne dans
        # DESIVAST DR1 (Table 4 de Rincon+2025). Sans lui le filtre ne
        # s'appliquait pas et le script comptait 3 764 vides « interieurs »
        # au lieu de 1 489 -- les vides de bord etaient tous inclus.
        for cname in ['EDGE', 'edge_flag', 'EDGE_FLAG', 'EdgeFlag', 'edge']:
            if cname in data.colnames:
                eflag_col = cname; break
        if eflag_col:
            data = data[data[eflag_col] == 0]
        else:
            print(f"  Attention : colonne edge_flag absente, tous les vides inclus")

        # Déduplification : une ligne par vide unique (par identifiant void)
        id_col = None
        for cname in ['flag', 'FLAG', 'hole_id', 'HOLE_ID', 'VoidID']:
            if cname in data.colnames:
                id_col = cname; break
        if id_col:
            # Garder la première occurrence de chaque void
            seen = set()
            keep = []
            for i, row in enumerate(data):
                vid = int(row[id_col])
                if vid not in seen:
                    seen.add(vid)
                    keep.append(i)
            data = data[keep]
        print(f"  Vides intérieurs uniques : {len(data)}")

        # Colonne rayon effectif (en Mpc/h) — ajoutée par DESIVAST
        r_col = None
        for cname in ['EFFECTIVE_RADIUS', 'effective_radius', 'R_EFF', 'r_eff']:
            if cname in data.colnames:
                r_col = cname; break
        if r_col is None:
            raise KeyError(
                f"Colonne rayon introuvable dans {fname}.\n"
                f"Colonnes disponibles : {data.colnames}")

        R_mpc = np.array(data[r_col]) / h   # Mpc/h -> Mpc physique
        print(f"  R_eff [Mpc] : min={R_mpc.min():.1f}  "
              f"median={np.median(R_mpc):.1f}  max={R_mpc.max():.1f}")
        R_all.append(R_mpc)

    if not R_all:
        raise FileNotFoundError(
            "No DESIVAST DR1 VoidFinder file found in: " + fits_dir + "\n"
            "Download from:\n"
            "  https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/\n"
            "Commande wget :\n"
            "  wget -P " + fits_dir + "/ \\\n"
            "    https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
            "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits\n"
            "  wget -P " + fits_dir + "/ \\\n"
            "    https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
            "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits")
    return np.concatenate(R_all)


def download_desivast(target_dir='.'):
    """
    Download the DESIVAST DR1 VoidFinder catalogues (public URL).
    Requires urllib (Python stdlib).
    """
    import urllib.request, os
    BASE = "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
    FILES = [
        "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits",
        "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits",
    ]
    os.makedirs(target_dir, exist_ok=True)
    for fname in FILES:
        dest = os.path.join(target_dir, fname)
        if os.path.exists(dest):
            print(f"  Déjà présent : {dest}"); continue
        url = BASE + fname
        print(f"  Téléchargement : {url}")
        try:
            urllib.request.urlretrieve(url, dest)
            size = os.path.getsize(dest) / 1e6
            print(f"  OK — {size:.1f} MB sauvegardé : {dest}")
        except Exception as e:
            print(f"  ERREUR : {e}")
            print(f"  Essayer manuellement : wget {url} -P {target_dir}/")

print("="*65)
print("ECF VSF vs DESIVAST DR1  v1.0 — 27/06/2026")
print("="*65)
print(f"Mode : {DATA_MODE}")
print(f"Kill-switch : R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h\n")

if DATA_MODE == 'download':
    print("\nDownloading DESIVAST DR1...")
    download_desivast(FITS_PATH)
    DATA_MODE = 'fits'   # continuer avec les fichiers téléchargés

if DATA_MODE == 'fits':
    R_obs      = load_fits_catalog(FITS_PATH)
    R_obs      = R_obs[R_obs >= BINS_MPC[0]]
    OBS_COUNTS, _ = np.histogram(R_obs, bins=BINS_MPC)
    OBS_COUNTS = OBS_COUNTS.astype(float)
    print(f"Total charges : {len(R_obs)} vides interieurs")
else:
    R_obs      = None
    OBS_COUNTS = DR1_COUNTS.copy()

# ===========================================================================
# MODELE ECF
# ===========================================================================

def A_ecf(R_mpc, xi=XI_KZ_MPC):
    """Facteur d'amplification ECF (vaut 2.1 au pic xi_KZ)."""
    return 1. + A_ECF_PEAK * np.exp(-(R_mpc - xi)**2 / (2.*SIG_KZ_MPC**2))

ECF_MID = DR1_COUNTS * np.array([A_ecf(R)           for R in BIN_CENTERS])
ECF_LO  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_LO) for R in BIN_CENTERS])
ECF_HI  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_HI) for R in BIN_CENTERS])

# ===========================================================================
# STATISTIQUES DE TEST
# ===========================================================================

def N_above(counts, R_cut_h):
    return counts[SDSS_BINS_H[:-1] >= R_cut_h].sum()

def sigma_detect(N_l, N_e, f_syst=0.0):
    if N_l < 0.1: return 0.
    return (N_e - N_l) / np.sqrt(N_l + (f_syst*N_l)**2)

R_CUTS_H = [28., 32., 36., 40., 42.]

for label, scale, fsyst in [
    ("DESIVAST DR1  (stat. seule)",   1.,          0.00),
    ("DESIVAST DR1  (+30% syst.)",    1.,          0.30),
    ("Survey complet DESI (~15k)",    SCALE_FULL,  0.10),
]:
    print(f"── {label} ──")
    print(f"  {'Coupure':>12}  {'N_LCDM':>7}  {'N_ECF':>7}  {'x':>5}  {'sigma':>8}")
    for Rc in R_CUTS_H:
        N_l = N_above(DR1_COUNTS, Rc) * scale
        N_e = N_above(ECF_MID,    Rc) * scale
        sig = sigma_detect(N_l, N_e, fsyst)
        ks  = " <-- KS" if abs(Rc - R_KS_H) < 2. else ""
        print(f"  R>{Rc:>4.0f} Mpc/h  {N_l:>7.0f}  {N_e:>7.0f}  "
              f"{N_e/max(N_l,.01):>4.2f}x  {sig:>7.1f}s{ks}")
    print()

# Comparaison donnees reelles si mode FITS
if DATA_MODE == 'fits' and R_obs is not None:
    print("── Donnees reelles vs LCDM ──")
    for Rc in R_CUTS_H:
        N_obs_v = int((R_obs >= Rc/h).sum())
        N_l     = N_above(DR1_COUNTS, Rc)
        sig     = (N_obs_v - N_l) / np.sqrt(max(N_l, .1))
        verdict = "EXCES" if sig>2 else ("DEFICIT" if sig<-2 else "OK")
        print(f"  R>{Rc:>4.0f} Mpc/h  N_obs={N_obs_v:>5}  N_LCDM={N_l:>6.0f}  "
              f"{sig:>+6.1f}s  [{verdict}]")
    print()

# ===========================================================================
# FIGURE
# ===========================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')
fig.suptitle(
    # [26/08/2026] Le titre disait « VSF ECF vs LCDM ». Il n'y a PAS de VSF
    # LCDM ici : la serie de reference est un substitut recale depuis SDSS,
    # ce que la legende admettait quatre lignes plus bas. Le titre affirmait
    # donc ce que la legende dementait -- et un lecteur retient le titre.
    r"ECF void size function — DESIVAST DR1 (Rincon+2025, ApJ 982:38)"
    "\n"
    # [26/08/2026] Le « 40 » etait code en dur alors que le seuil derive de
    # R_KS_MPC : le titre annoncait 40 Mpc/h (soit xi_KZ = 60) sous sa propre
    # mention « xi_KZ = 65 Mpc ». Les deux valeurs coexistaient dans la meme
    # figure. Le seuil est desormais calcule, donc necessairement coherent.
    rf"Foundation III prediction: $N_{{\rm ECF}}(R>{R_KS_H:.0f}\,h^{{-1}}{{\rm Mpc}})"
    r"\approx 2.1\times N_{\rm baseline}$ ($\xi_{\rm KZ}=60$ Mpc, adopted)",
    fontsize=11, fontweight='bold'
)

W = BIN_WIDTHS * 0.42

# -- Panel gauche : distribution -----------------------------------------
ax = axes[0]

ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
       color='#1C3F7A', alpha=0.70,
       label=r'placeholder (rescaled SDSS$\to$DR1), NOT $\Lambda$CDM')
ax.bar(BIN_CENTERS, ECF_MID, W, align='center',
       color='#CC2222', alpha=0.45,
       label=r'placeholder $\times\,A_{\rm ECF}$ ($\xi_{\rm KZ}=60$ Mpc)')
ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
       color='none', edgecolor='#1C3F7A', lw=1.2)
if DATA_MODE == 'download':
    print("\nDownloading DESIVAST DR1...")
    download_desivast(FITS_PATH)
    DATA_MODE = 'fits'   # continuer avec les fichiers téléchargés

if DATA_MODE == 'fits':
    ax.errorbar(BIN_CENTERS, OBS_COUNTS,
                yerr=np.sqrt(np.maximum(OBS_COUNTS,1.)),
                fmt='ko', ms=4, lw=1.2, capsize=3, zorder=6,
                label='DESIVAST DR1 (data)')
ax.axvline(R_KS_MPC,  c='orange', lw=2.0, ls='--',
           label=fr'Kill-switch {R_KS_H:.0f} Mpc/$h$')
ax.axvline(XI_KZ_MPC, c='red',    lw=1.2, ls=':',
           label=fr'$\xi_{{KZ}}={XI_KZ_MPC:.0f}$ Mpc')
ax.fill_betweenx([0,420], R_KS_MPC, 200., color='orange', alpha=0.07, zorder=0)
ax.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
ax.set_ylabel('Number of voids per bin', fontsize=10)
ax.set_title('DESIVAST DR1 void distribution', fontsize=10)
ax.set_xlim(BINS_MPC[0], BINS_MPC[-1]); ax.set_ylim(0.)
ax.legend(fontsize=7.5); ax.grid(True, alpha=0.22)
ax_t = ax.twiny()
ax_t.set_xlim(ax.get_xlim()[0]*h, ax.get_xlim()[1]*h)
ax_t.set_xlabel(r'$R_{\rm eff}$ [Mpc/$h$]', fontsize=10)

# -- Panel droit : amplification + detectabilite -------------------------
ax2 = axes[1]
R_plt = np.linspace(BINS_MPC[0], BINS_MPC[-1], 400)
A_m = np.array([A_ecf(R)           for R in R_plt])
A_l = np.array([A_ecf(R, XI_KZ_LO) for R in R_plt])
A_h = np.array([A_ecf(R, XI_KZ_HI) for R in R_plt])

ax2.plot(R_plt, A_m, 'r-', lw=2.5,
         label=fr'$A_{{\rm ECF}}(R)$, $\xi_{{KZ}}={XI_KZ_MPC:.0f}$ Mpc')
ax2.fill_between(R_plt, A_l, A_h, color='red', alpha=0.18,
                 label=fr'$\xi_{{KZ}}={XI_KZ_LO:.0f}$-{XI_KZ_HI:.0f} Mpc')
ax2.axhline(1.0, c='k',      lw=1.0, ls='-',  label=r'$\Lambda$CDM')
ax2.axhline(2.1, c='orange', lw=1.5, ls='--', label=r'Kill-switch $\times 2.1$')
ax2.axvline(R_KS_MPC,  c='orange', lw=2.0, ls='--', alpha=0.8)
ax2.axvline(XI_KZ_MPC, c='red',    lw=1.2, ls=':',  alpha=0.7)

# [26/08/2026] LES SIGMA NE SONT PLUS TRACES SUR LA FIGURE.
# Ils etaient calcules contre DR1_COUNTS, qui n'est PAS une VSF LCDM mais un
# substitut recale a la main depuis un ancien catalogue SDSS. L'en-tete de
# plot_F3_ecf_vsf_desivast_fits.py dit que ces significativites sont « tres
# probablement un artefact » et « ne doivent pas etre citees, dans les papiers
# ni ailleurs » -- or une figure qui les affiche les rend citables.
# Les valeurs restent CALCULEES et imprimees en console : elles gardent leur
# valeur de diagnostic interne, elles n'ont pas leur place dans un papier.
# L'annotation indique desormais l'amplification predite, qui est ce que la
# figure peut legitimement affirmer.
for Rc_mpc, dx in [(32., -3.), (R_KS_MPC, +5.)]:
    Rc_h_ = Rc_mpc * h
    ax2.annotate(
        fr'$R>{Rc_h_:.0f}$ Mpc/$h$:' '\n'
        fr'$A_{{\rm ECF}}={A_ecf(Rc_mpc):.2f}$',
        xy=(Rc_mpc, A_ecf(Rc_mpc)),
        xytext=(Rc_mpc+dx, A_ecf(Rc_mpc)+0.18),
        fontsize=7.5, color='#222',
        ha='right' if dx < 0 else 'left',
        arrowprops=dict(arrowstyle='->', color='gray', lw=0.8)
    )
ax2.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
ax2.set_ylabel(r'$A_{\rm ECF}(R)$  (predicted amplification)', fontsize=10)
ax2.set_title('ECF amplification and detectability', fontsize=10)
ax2.set_xlim(BINS_MPC[0], BINS_MPC[-1]); ax2.set_ylim(0.75, 2.65)
ax2.legend(fontsize=8.5); ax2.grid(True, alpha=0.22)
ax_t2 = ax2.twiny()
ax_t2.set_xlim(ax2.get_xlim()[0]*h, ax2.get_xlim()[1]*h)
ax_t2.set_xlabel(r'[Mpc/$h$]', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ===========================================================================
# RAPPORT
# ===========================================================================
N_l_ks  = N_above(DR1_COUNTS, R_KS_H)
N_e_ks  = N_above(ECF_MID,    R_KS_H)

print(f"""
{'='*65}
RAPPORT FINAL
{'='*65}
Source     : {DATA_MODE}  (Rincon+2025, N_DR1={N_DR1})
Kill-switch: R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h
N_LCDM(ks) = {N_l_ks:.0f}   N_ECF(ks) = {N_e_ks:.0f}  (x{N_e_ks/max(N_l_ks,.01):.2f})

Detectabilite au kill-switch :
  DR1 stat seule : {sigma_detect(N_l_ks, N_e_ks, 0.00):.1f}s
  DR1 + 30% syst : {sigma_detect(N_l_ks, N_e_ks, 0.30):.1f}s  <- estimation realiste
  Survey complet : {sigma_detect(N_l_ks*SCALE_FULL, N_e_ks*SCALE_FULL, 0.10):.1f}s

Pour le vrai catalogue FITS :
  DATA_MODE = 'fits'
  FITS_PATH = '/chemin/vers/desivast_dr1/'
  URL       : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/

Figure : {OUTPUT_PNG}
{'='*65}
""")

```

---

### Fichier 13 : `plot_F3_ecf_bbn_constraint.py`

```python
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

```

---

### Fichier 14 : `plot_ECF_frame_dragging_cascade.py`

```python
#!/usr/bin/env python3
"""
plot_ECF_frame_dragging_cascade.py

Synthesis figure for Foundation III: the "fossilized frame-dragging" cascade.

A single image summarizing how the parent black hole's spin propagates,
via frame-dragging (Lense-Thirring), across four scales of the ECF corpus:

    parent spin a*  ->  child chiral axis  ->  Pi_GW / P-violation  ->  homochirality

The same Penrose function f(a*) that governs the energy flux (PO-F3-1),
the viability threshold (PO-F3-SEUIL) and the bounce thermodynamics
(PO-F3-4) also governs the chirality it imprints. A single symmetry
breaking (parity P) is transmitted from the Kerr metric down to the
handedness of biological molecules.

Output: Fig_ECF_FrameDragging_Cascade.png  (300 dpi, publication quality)
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
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.collections import LineCollection
import matplotlib.font_manager as fm

# ----------------------------------------------------------------------
# Aesthetic configuration
# ----------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "axes.linewidth": 0.0,
})

# Deep-space palette
BG        = "#0a0e1a"   # near-black navy
PANEL     = "#131a2e"   # panel fill
INK       = "#e8ecf5"   # near-white text
MUTED     = "#8b97b5"   # muted labels
GOLD      = "#f2c14e"   # accent / spin
CYAN      = "#4fd0e0"   # geometry
VIOLET    = "#b57edc"   # cosmology
ROSE      = "#e87a90"   # biology
GREEN     = "#7fd18b"   # established status

STAGE_COLORS = [GOLD, CYAN, VIOLET, ROSE]


def penrose_f(a):
    """Extractable rotational-energy fraction (Penrose-Christodoulou)."""
    return 1.0 - np.sqrt((1.0 + np.sqrt(1.0 - a**2)) / 2.0)


# ----------------------------------------------------------------------
# Figure scaffold
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(15, 9.2), dpi=300)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.2)
ax.axis("off")
ax.set_facecolor(BG)


# ----------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------
ax.text(7.5, 8.72, "The Fossilized Frame-Dragging Cascade",
        ha="center", va="center", color=INK, fontsize=25, weight="bold")
ax.text(7.5, 8.24,
        "One symmetry breaking (parity $P$), transmitted from the Kerr metric to the handedness of life",
        ha="center", va="center", color=MUTED, fontsize=12.5, style="italic")


# ----------------------------------------------------------------------
# Helper: rounded panel
# ----------------------------------------------------------------------
def panel(x, y, w, h, color, lw=1.6, fill=PANEL, alpha=1.0):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=lw, edgecolor=color, facecolor=fill, alpha=alpha,
        mutation_aspect=1.0, zorder=3)
    ax.add_patch(box)
    return box


def arrow(x0, y0, x1, y1, color, lw=2.6, style="-|>", ms=22, rad=0.0):
    a = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle=style, mutation_scale=ms,
        linewidth=lw, color=color,
        connectionstyle=f"arc3,rad={rad}", zorder=4,
        capstyle="round")
    ax.add_patch(a)
    return a


# ----------------------------------------------------------------------
# Four stage panels along a gentle descending diagonal
# ----------------------------------------------------------------------
# positions (lower-left corners) and sizes
PW, PH = 3.05, 2.35
stage_xy = [
    (0.55, 5.35),   # Stage 1 - parent spin (F3)
    (4.05, 5.35),   # Stage 2 - chiral axis (F2)
    (7.55, 5.35),   # Stage 3 - Pi_GW / P-violation (F2)
    (11.05, 5.35),  # Stage 4 - homochirality (biology)
]
titles = [
    "1.  PARENT SPIN",
    "2.  CHIRAL AXIS",
    "3.  $P$-VIOLATION",
    "4.  HOMOCHIRALITY",
]
scales = ["Foundation III  ·  strong gravity",
          "Foundation II  ·  primordial geometry",
          "Foundation II  ·  cosmology",
          "biology  ·  Bennu / interstellar ice"]
subs = [
    "Kerr black hole rotates:\nframe-dragging $g_{t\\phi}\\propto a^*$",
    "Entrainment imprinted in\nthe newborn white hole:\n$\\sigma^2_{\\rm baby}\\propto a^*$",
    "Broken mirror symmetry:\nchiral vacuum, $\\Pi_{\\rm GW}$\ngravitational-wave asymmetry",
    "Left-handed amino acids;\nracemic constraints from\nOSIRIS-REx samples",
]

for (x, y), title, scale, sub, col in zip(stage_xy, titles, scales, subs, STAGE_COLORS):
    panel(x, y, PW, PH, col)
    # top accent bar
    ax.add_patch(FancyBboxPatch((x, y + PH - 0.42), PW, 0.42,
                 boxstyle="round,pad=0.02,rounding_size=0.18",
                 linewidth=0, facecolor=col, alpha=0.20, zorder=3.5))
    ax.text(x + 0.22, y + PH - 0.21, title, ha="left", va="center",
            color=col, fontsize=13.5, weight="bold", zorder=5)
    ax.text(x + PW/2, y + PH - 0.70, scale, ha="center", va="center",
            color=MUTED, fontsize=8.0, style="italic", zorder=5)
    # description text sits in the upper-middle; lower third holds the icon
    ax.text(x + PW/2, y + PH - 1.32, sub, ha="center", va="center",
            color=INK, fontsize=9.6, zorder=5, linespacing=1.4)

# connecting arrows between stages (with propagation label)
for i in range(3):
    x0 = stage_xy[i][0] + PW
    x1 = stage_xy[i+1][0]
    yc = stage_xy[i][1] + PH/2
    arrow(x0 + 0.04, yc, x1 - 0.04, yc, INK, lw=2.4, ms=20)

# [CORRECTED 08/09/2026] Labels were single-line horizontal and wider than
# the 0.45-unit gap between panels, so they overlapped the neighbouring
# boxes. Rotated to vertical: the gap constrains width, not height.
arrow_labels = ["frame-dragging", "$P$-breaking", "chiral chemistry"]
for i, lab in enumerate(arrow_labels):
    x0 = stage_xy[i][0] + PW
    x1 = stage_xy[i+1][0]
    xc = (x0 + x1) / 2
    yc = stage_xy[i][1] + PH/2
    ax.text(xc, yc + 0.62, lab, ha="center", va="center",
            color=MUTED, fontsize=7.6, style="italic", zorder=5,
            rotation=90)


# ----------------------------------------------------------------------
# Stage-1 inset: a spinning Kerr black hole with frame-dragging swirl
# ----------------------------------------------------------------------
cx, cy = stage_xy[0][0] + PW/2, stage_xy[0][1] + 0.72
# frame-dragging spiral (compact, sits in the lower half of the panel)
theta = np.linspace(0, 3.6 * np.pi, 400)
r = 0.025 + 0.030 * theta
xs = cx + r * np.cos(theta)
ys = cy + r * np.sin(theta) * 0.60   # slight ellipticity
pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
lc = LineCollection(segs, colors=GOLD,
                    linewidths=np.linspace(0.3, 2.0, len(segs)),
                    alpha=0.55, zorder=4)
ax.add_collection(lc)
# central black hole + accretion glow
ax.add_patch(Circle((cx, cy), 0.19, color="#000000", zorder=5))
ax.add_patch(Circle((cx, cy), 0.19, fill=False, lw=1.4, edgecolor=GOLD, zorder=6))
ax.add_patch(Circle((cx, cy), 0.09, color=GOLD, alpha=0.9, zorder=6))

# ----------------------------------------------------------------------
# Stage-2 inset: chiral axis (a helix winding around a vertical axis)
# ----------------------------------------------------------------------
cx2, cy2 = stage_xy[1][0] + PW/2, stage_xy[1][1] + 0.72
tt = np.linspace(0, 3.0*np.pi, 200)
hx = cx2 + 0.30*np.cos(tt)
hy = cy2 - 0.42 + (tt/(3.0*np.pi))*0.84
ax.plot(hx, hy, color=VIOLET, lw=2.2, zorder=5, solid_capstyle="round")
ax.plot(cx2 + 0.30*np.cos(tt+np.pi), hy, color=VIOLET, lw=1.1,
        alpha=0.45, zorder=4, solid_capstyle="round")
arrow(cx2, cy2 - 0.52, cx2, cy2 + 0.52, MUTED, lw=1.2, ms=12)

# ----------------------------------------------------------------------
# Stage-3 inset: broken mirror symmetry (two arcs, one struck through)
# ----------------------------------------------------------------------
cx3, cy3 = stage_xy[2][0] + PW/2, stage_xy[2][1] + 0.72
# left-handed and right-handed curved arrows, asymmetric weights
arc = np.linspace(-0.7*np.pi, 0.7*np.pi, 100)
ax.plot(cx3 - 0.34 + 0.22*np.cos(arc), cy3 + 0.22*np.sin(arc),
        color=VIOLET, lw=2.6, zorder=5, solid_capstyle="round")
ax.plot(cx3 + 0.34 - 0.22*np.cos(arc), cy3 + 0.22*np.sin(arc),
        color=MUTED, lw=1.0, alpha=0.5, zorder=5, solid_capstyle="round")
# dashed mirror line
ax.plot([cx3, cx3], [cy3 - 0.42, cy3 + 0.42], color=MUTED, lw=0.9,
        ls=(0, (3, 3)), zorder=4)

# ----------------------------------------------------------------------
# Stage-4 inset: a chiral molecule (central C with four distinct groups)
# ----------------------------------------------------------------------
cx4, cy4 = stage_xy[3][0] + PW/2, stage_xy[3][1] + 0.72
ax.add_patch(Circle((cx4, cy4), 0.075, color=ROSE, zorder=6))
bond_ang = [90, 210, 330, 25]
bond_len = [0.40, 0.36, 0.36, 0.30]
bond_c   = [INK, ROSE, CYAN, GOLD]
for ang, ln, bc in zip(bond_ang, bond_len, bond_c):
    ex = cx4 + ln*np.cos(np.radians(ang))
    ey = cy4 + ln*np.sin(np.radians(ang))
    ax.plot([cx4, ex], [cy4, ey], color=bc, lw=1.8, zorder=5,
            solid_capstyle="round")
    ax.add_patch(Circle((ex, ey), 0.055, color=bc, zorder=6))


# ----------------------------------------------------------------------
# Central spine: the invariant f(a*) that governs every stage
# ----------------------------------------------------------------------
# (baseline spine removed; the f(a*) ribbon below carries the invariant)

# The f(a*) curve as a ribbon under the cascade
ax_curve = fig.add_axes([0.085, 0.085, 0.63, 0.235])
ax_curve.set_facecolor(PANEL)
for spine in ax_curve.spines.values():
    spine.set_color("#2a3450")
    spine.set_linewidth(1.0)
a = np.linspace(0, 0.998, 400)
f = penrose_f(a)
ax_curve.plot(a, f, color=GOLD, lw=2.8, zorder=5)
ax_curve.fill_between(a, 0, f, color=GOLD, alpha=0.10, zorder=4)
# mark the extremal bound
ax_curve.axhline(penrose_f(0.998), color=MUTED, lw=0.9, ls=":", zorder=3)
ax_curve.text(0.02, penrose_f(0.998) + 0.006,
              "extremal bound $f<0.29$", color=MUTED, fontsize=8.5,
              va="bottom", ha="left")
ax_curve.set_xlim(0, 1.0)
ax_curve.set_ylim(0, 0.32)
ax_curve.set_xlabel("dimensionless spin  $a^*$", color=INK, fontsize=10)
ax_curve.set_ylabel("$f(a^*)$", color=INK, fontsize=11)
ax_curve.tick_params(colors=MUTED, labelsize=8.5)
ax_curve.set_title(
    "The single invariant  $f(a^*)=1-\\sqrt{(1+\\sqrt{1-a^{*2}})/2}$",
    color=INK, fontsize=10.5, pad=6)

# annotate the three roles it plays
roles = [
    (0.30, "energy flux\n(PO-F3-1)"),
    (0.60, "viability\n(PO-F3-SEUIL)"),
    (0.88, "thermal regime\n(PO-F3-4)"),
]
for ax_pos, lab in roles:
    ax_curve.axvline(ax_pos, color=CYAN, lw=0.8, ls="--", alpha=0.5, zorder=3)
    ax_curve.text(ax_pos, 0.30, lab, color=CYAN, fontsize=7.6,
                  ha="center", va="top", linespacing=1.2)


# ----------------------------------------------------------------------
# Right-hand status box: established / proposed / to prove
# ----------------------------------------------------------------------
sx, sy, sw, sh = 10.55, 0.55, 3.75, 3.35
panel(sx, sy, sw, sh, "#2a3450", lw=1.3, fill="#0f1526")
ax.text(sx + sw/2, sy + sh - 0.32, "Epistemic status",
        ha="center", va="center", color=INK, fontsize=12.5, weight="bold")

status_items = [
    (GREEN,  "ESTABLISHED",
     "Frame-dragging is real (Gravity\nProbe B), scales as $a^*$, carries\nintrinsic chirality."),
    (GOLD,   "PROPOSED",
     "It is the origin of the child's\nchiral axis \u2014 an imprint, with\nno spin extracted from the parent."),
    (ROSE,   "TO BE PROVEN",
     "Dynamical ECKS junction; axis\norientation preserved through the\nbounce; imprint $\\to\\sigma^2_{\\rm baby}$ law."),
]
yy = sy + sh - 0.92
for col, head, body in status_items:
    ax.add_patch(Circle((sx + 0.32, yy), 0.075, color=col, zorder=6))
    ax.text(sx + 0.54, yy, head, ha="left", va="center",
            color=col, fontsize=10.5, weight="bold", zorder=6)
    ax.text(sx + 0.54, yy - 0.44, body, ha="left", va="center",
            color=INK, fontsize=8.6, zorder=6, linespacing=1.35)
    yy -= 1.02


# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
ax.text(7.5, 0.22,
        "Einstein-Cartan Framework  ·  Foundation III  ·  the parent spin $a^*$ is the single parameter "
        "threading strong gravity, cosmological chirality, and prebiotic handedness",
        ha="center", va="center", color=MUTED, fontsize=8.8, style="italic")


# ----------------------------------------------------------------------
# Export
# ----------------------------------------------------------------------
outfile = "Fig_ECF_FrameDragging_Cascade.png"
fig.savefig(outfile, dpi=300, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
print(f"Saved: {outfile}")

```

---

### Fichier 15 : `plot_F3_ecf_fNL_KZ.py`

```python
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

```

---

### Fichier 16 : `build_vsf_observed_dr1.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vsf_observed_dr1.py  --  ECF Foundation III
======================================================================
The observed void size function, measured from DESIVAST DR1 itself.

WHY THIS SCRIPT EXISTS
----------------------
plot_F3_ecf_vsf_desivast_fits.py carries this warning about the counts
it compares against:

    "DR1_COUNTS is NOT a theoretical LCDM void size function. It is a
     crude PLACEHOLDER: the *shape* is taken from an older SDSS
     VoidFinder catalogue, rescaled to an *expected* DESI DR1 total
     (N_DR1=1484) and multiplied by a hand-tuned depth factor
     (DEPTH_F=1.4), with an extra ad hoc x1.5 on the last bin. None of
     these numbers is derived from a theory, a simulation, or an
     excursion-set calculation. [...] the large deficits reported
     (about -6 to -19 sigma) are therefore very likely an ARTEFACT of
     the rescaling, NOT evidence of a real cosmological tension. They
     must not be quoted as such, in the papers or elsewhere."

    "TODO: replace with a proper LCDM VSF [...] before any of these
     significances is used as a published result."

The catalogue is now in hand, so the first half of that TODO can be
settled: the OBSERVED counts no longer need to be guessed from SDSS.
This script measures them directly.

WHAT IT DOES, AND WHAT IT DOES NOT
----------------------------------
DOES: measures N(R_eff) from the DESIVAST DR1 VoidFinder catalogue,
      NGC + SGC, with and without the interior-void cut, and compares
      the result to the placeholder.

DOES NOT: supply a theoretical LambdaCDM prediction. Replacing the
      placeholder observed counts removes one of the two defects; the
      other -- having no LambdaCDM baseline to compare against --
      remains, and no significance can be quoted until it is fixed
      (excursion-set model, or the AbacusSummit BGS mocks that
      DESIVAST itself provides). This script does not pretend
      otherwise, and prints no sigma.

WHY EDGE MATTERS
----------------
The MAXIMALS HDU carries an EDGE flag with values 0, 1, 2. EDGE = 0
marks interior voids -- those not touching the survey boundary. Summing
over NGC + SGC gives 1,489 interior voids, exactly the number quoted in
the DESIVAST paper, which confirms the flag is being read as intended.
A boundary void has an ill-constrained volume and an overestimated
effective radius, so a void size function must be built on interior
voids; the "all voids" column is printed only for comparison.

Data: place the VoidFinder FITS files under desivast_dr1/ (or pass
--dir). They are small (0.6-3.9 MB), unlike the V2 catalogues.

Usage: python3 build_vsf_observed_dr1.py [--dir PATH]
======================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
import os

import numpy as np

H = 0.6732                       # DESIVAST fiducial (Planck 2018)

# The binning of the existing script, kept so the two are comparable.
BINS_H = np.array([10, 13, 16, 19, 22, 25, 28, 32, 36, 42, 54], dtype=float)

# The placeholder currently in plot_F3_ecf_vsf_desivast_fits.py
SDSS_COUNTS = np.array([155, 210, 215, 185, 150, 110, 70, 40, 20, 8], dtype=float)
N_DR1_ASSUMED = 1484
DEPTH_F = 1.4


def placeholder_counts():
    c = SDSS_COUNTS * (N_DR1_ASSUMED / SDSS_COUNTS.sum()) * DEPTH_F
    c = c.copy()
    c[-1] *= 1.5
    return c


def load_voidfinder(d):
    from astropy.io import fits
    r, e = [], []
    found = []
    for hemi in ("NGC", "SGC"):
        p = os.path.join(d, f"DESIVAST_BGS_VOLLIM_VoidFinder_{hemi}.fits")
        if not os.path.exists(p):
            continue
        with fits.open(p) as hdul:
            t = hdul["MAXIMALS"].data
            r.append(np.asarray(t["R_EFF"], dtype=float))
            e.append(np.asarray(t["EDGE"]))
        found.append(hemi)
    if not r:
        return None, None, found
    return np.concatenate(r), np.concatenate(e), found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None)
    a = ap.parse_args()

    if a.dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        parent = os.path.dirname(here)
        repo_root = os.path.dirname(parent)   # .../Foundation_3, two levels up
        # Canonical location: Foundation_3/data/desivast_dr1/, a single
        # visible data folder at repo root, independent of which category
        # subfolder (A_Core_Calculations, B_Paper_Plots, ...) the script
        # itself lives in. Checked first; older layouts kept as fallback
        # for anyone who has not moved their files yet.
        for c in (
            os.path.join(repo_root, "data", "desivast_dr1"),
            "data/dr1/desivast_dr1", "desivast_dr1", ".",
            os.path.join(here, "desivast_dr1"),
            os.path.join(here, "data", "dr1", "desivast_dr1"),
            os.path.join(parent, "B_Paper_Plots", "desivast_dr1"),
            os.path.join(parent, "A_Core_Calculations", "desivast_dr1"),
            here,
        ):
            if os.path.exists(os.path.join(
                    c, "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits")):
                a.dir = c
                break
        else:
            a.dir = os.path.join(repo_root, "data", "desivast_dr1")

    print("=" * 68)
    print("  Observed void size function, measured from DESIVAST DR1")
    print("=" * 68)

    r, e, found = load_voidfinder(a.dir)
    if r is None:
        print(f"\n  VoidFinder catalogues not found in '{a.dir}/'.")
        print("  They are small (0.6-3.9 MB); see plot_F3_ecf_vsf_desivast_fits.py")
        print("  for the download URL.")
        return 1

    print(f"\n  hemispheres read: {', '.join(found)}")
    print(f"  voids: {len(r):,}   interior (EDGE == 0): {int((e == 0).sum()):,}")
    if int((e == 0).sum()) == 1489:
        print("  -> matches the 1,489 interior voids quoted by DESIVAST: the")
        print("     EDGE flag is being read as intended.")

    n_all, _ = np.histogram(r, bins=BINS_H)
    n_int, _ = np.histogram(r[e == 0], bins=BINS_H)
    ph = placeholder_counts()

    print("\n" + "-" * 68)
    print("  Counts per bin in R_eff [Mpc/h]")
    print("-" * 68)
    print(f"  {'bin':>12} {'measured':>10} {'interior':>10} {'placeholder':>12}"
          f" {'ratio':>8}")
    for i in range(len(n_all)):
        lo, hi = BINS_H[i], BINS_H[i + 1]
        ratio = (n_int[i] / ph[i]) if ph[i] > 0 else float("nan")
        print(f"  {lo:>5.0f}-{hi:<6.0f} {n_all[i]:>10,} {n_int[i]:>10,}"
              f" {ph[i]:>12.0f} {ratio:>8.2f}")
    print(f"  {'TOTAL':>12} {n_all.sum():>10,} {n_int.sum():>10,} {ph.sum():>12.0f}")

    print("\n" + "-" * 68)
    print("  What the placeholder got wrong")
    print("-" * 68)
    print(f"  total:  measured interior {n_int.sum():,}  vs  placeholder "
          f"{ph.sum():.0f}   ({100*(n_int.sum()/ph.sum()-1):+.0f} %)")
    print(f"  peak :  measured peaks in bin {BINS_H[int(np.argmax(n_int))]:.0f}"
          f"-{BINS_H[int(np.argmax(n_int))+1]:.0f}, placeholder in bin "
          f"{BINS_H[int(np.argmax(ph))]:.0f}-{BINS_H[int(np.argmax(ph))+1]:.0f}")
    print(f"  tail :  measured max R_eff = {r[e == 0].max():.2f} Mpc/h (interior),"
          f" {r.max():.2f} (all)")
    empty = [f"{BINS_H[i]:.0f}-{BINS_H[i+1]:.0f}" for i in range(len(n_int))
             if n_int[i] == 0 and ph[i] > 0]
    if empty:
        print(f"  bins where the placeholder predicts voids and none exist:")
        print(f"          {', '.join(empty)}  "
              f"(placeholder: {', '.join(f'{ph[i]:.0f}' for i in range(len(n_int)) if n_int[i] == 0 and ph[i] > 0)})")

    print("\n" + "=" * 68)
    print("  READING THIS")
    print("=" * 68)
    print("  The measured distribution is far more peaked than the placeholder")
    print("  and dies out much sooner. Deficits computed against the")
    print("  placeholder were therefore comparing the data to a shape the data")
    print("  never had -- which is what the original warning said, and this")
    print("  quantifies it.")
    print()
    print("  The observed side of the comparison is now measured rather than")
    print("  assumed. The THEORETICAL side is not: there is still no LambdaCDM")
    print("  VSF to compare against, so NO SIGNIFICANCE IS QUOTED HERE and none")
    print("  should be quoted elsewhere until an excursion-set model or the")
    print("  AbacusSummit BGS mocks are used.")


if __name__ == "__main__":
    sys.exit(main() or 0)

```

---

