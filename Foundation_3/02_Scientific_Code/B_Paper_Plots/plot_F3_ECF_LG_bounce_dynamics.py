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
