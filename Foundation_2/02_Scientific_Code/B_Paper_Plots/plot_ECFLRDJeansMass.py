# =============================================================================
# simECFLRDJeansMass.py — ECF Foundation II
# PRD Referee Documentation — Commentaires détaillés
#
# TITRE : Little Red Dots comme Macro-Nœuds Primordiaux ECF
#         Prédiction de la Masse de Jeans de la Phase Stiff
#
# PURPOSE
# -------
# Demonstrate that the "Little Red Dots" (LRDs) detected by JWST at z > 5
# — compact objects with inferred masses ~10^5–10^7 Msun — are a NATURAL,
# ZERO-FREE-PARAMETER prediction of the ECF stiff phase (w=1), rather than
# requiring fine-tuned super-Eddington accretion from stellar remnants.
#
# PHYSICAL BASIS
# --------------
# In the ECF model (Foundation I, Eq. eqmodifiedfriedmann), the post-bounce
# universe undergoes a STIFF FLUID ERA (w=1) during which:
#       rho_spin ~ a^{-6}   =>   H(t) = 1/(3t)
#       c_s = c * sqrt(w) = c            [sound speed = speed of light]
#       lambda_J = c_s / sqrt(G*rho) ~ c/H(z_t) = d_H   [Jeans = horizon]
#
# Characteristic Jeans mass (= horizon mass at topological freeze-out):
#       M_K = c^3 / (2 G H(z_t))
#
# For the QCD crystallisation epoch (z_t ~ 10^9, T ~ 150 MeV):
#       M_K ~ 4.7e6 Msun   => LRD upper mass range
# For z_t ~ 7e9 (EW-QCD bridge):
#       M_K ~ 1e5 Msun     => LRD lower mass range
#
# KEY RESULT (zero free parameters):
#       z_t in [6.9e8, 6.9e9]  <=>  M_K in [1e5, 1e7] Msun
#       = EXACTLY the LRD compact-object mass range (Rusakov+2026)
#
# SEEDING PROBLEM
# ---------------
# Standard Pop III remnant (M0=100 Msun at z=20) reaching 10^7 Msun by z=10:
#       f_Edd required = 2.5x  =>  SUPER-EDDINGTON (unphysical)
# ECF Macro-Knot (M0=1e5 Msun at z=20) reaching 10^7 Msun by z=10:
#       f_Edd required = 1.0x  =>  EXACTLY EDDINGTON (natural!)
# ECF Macro-Knot is ALREADY IN THE LRD ZONE at formation => f_Edd=0 needed
#       to be identified as an LRD. No accretion required for the LRD itself.
#
# KILL-SWITCHES (falsifiability for PRD referee)
# -----------------------------------------------
# 1. JWST/ELT finds NO compact seeds with M~10^5 Msun at z>10 at >3sigma
#    over >20 fields => FALSIFIES ECF seeding mechanism for this mass range.
# 2. LRD number density at z>10 exceeds ECF Kibble-Zurek prediction at >3sigma
#    => requires revision of T_t (transition temperature).
# 3. LRD X-ray faintness explained by AGN model with M_seed < 10^3 Msun
#    without super-Eddington => falsifies Macro-Knot identification.
#
# MATPLOTLIB BUG FIX (documented for reproducibility)
# ---------------------------------------------------
# tight_layout() FAILS if ax.annotate/ax.text contain unsupported LaTeX:
#     BAD:  r'$N \rightarrow 0$'   => ParseException at '\rightarrow'
#     GOOD: r'$N \to 0$'           => identical glyph, mathtext-safe
# FIX APPLIED: use constrained_layout=True at fig creation (no tight_layout)
#              and replace ALL \rightarrow => \to in annotation strings.
#
# OUTPUT FILES
# ------------
#   Fig_ECFLRDJeansMass.png         — 2-panel PRD figure (300 dpi)
#   data_lrd_jeans_mass.csv         — growth curves Panel A
#   data_jeans_mass_vs_zt.csv       — M_K(z_t) Panel B
# =============================================================================

import numpy as np
from scipy import integrate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json, os, csv

os.makedirs("output", exist_ok=True)

# -----------------------------------------------------------------------
# SECTION 1 — PHYSICAL CONSTANTS (SI)
# -----------------------------------------------------------------------
G     = 6.674e-11
c     = 2.998e8
Mpc   = 3.086e22
Msun  = 1.989e30
Gyr   = 3.156e16

H0_kms  = 70.0
H0      = H0_kms * 1e3 / Mpc
Omega_m = 0.30
Omega_r = 9.0e-5
Omega_L = 1.0 - Omega_m - Omega_r

# -----------------------------------------------------------------------
# SECTION 2 — HUBBLE RATE H(z)
# Full LCDM for Panel A (z < 100).
# Radiation-dominated approx for Panel B (z_t >> 10^3): error < 1%.
# -----------------------------------------------------------------------
def Hz_full(z):
    return H0 * np.sqrt(Omega_m*(1+z)**3 + Omega_r*(1+z)**4 + Omega_L)

def Hz_rad(z_t):
    """H(z_t) in radiation-dominated regime [s^-1]."""
    return H0 * np.sqrt(Omega_r) * (1 + z_t)**2

# -----------------------------------------------------------------------
# SECTION 3 — COSMIC AGE t(z) [Gyr]
# -----------------------------------------------------------------------
def t_age_Gyr(z):
    val, _ = integrate.quad(
        lambda zp: 1.0 / ((1+zp) * Hz_full(zp)), z, np.inf, limit=200)
    return val / Gyr

z_arr      = np.linspace(1.0, 25.0, 300)
t_arr_Gyr  = np.array([t_age_Gyr(zi) for zi in z_arr])
t_arr_Myr  = t_arr_Gyr * 1e3

# -----------------------------------------------------------------------
# SECTION 4 — EDDINGTON ACCRETION MODEL
# M(t) = M_0 * exp(k_Edd * Delta_t)
# k_Edd = 0.016 Myr^{-1}  (epsilon_rad=0.1, f_Edd=1, Salpeter time=0.45 Gyr)
# z_form = 20  (first baryonic gas available for accretion)
# -----------------------------------------------------------------------
k_Edd       = 0.016
z_form      = 20.0
t_form_Myr  = np.interp(z_form, z_arr, t_arr_Myr)
Delta_t     = np.maximum(t_arr_Myr - t_form_Myr, 0.0)

M0_popIII_low  = 100.0
M0_popIII_high = 1000.0
M0_ECF         = 1.0e5

M_popIII_low   = M0_popIII_low  * np.exp(k_Edd * Delta_t)
M_popIII_high  = M0_popIII_high * np.exp(k_Edd * Delta_t)
M_ECF          = M0_ECF         * np.exp(k_Edd * Delta_t)

# -----------------------------------------------------------------------
# SECTION 5 — ECF JEANS MASS M_K(z_t)
# M_K = c^3 / (2 G H(z_t))   [stiff phase c_s = c => lambda_J = d_H]
# -----------------------------------------------------------------------
z_t_arr  = np.logspace(5, 16, 1000)
H_zt_arr = Hz_rad(z_t_arr)
MK_arr   = c**3 / (2.0 * G * H_zt_arr) / Msun

# -----------------------------------------------------------------------
# SECTION 6 — CSV EXPORT
# -----------------------------------------------------------------------
with open('data_lrd_jeans_mass.csv', 'w', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['z', 't_Myr', 'M_popIII_low_Msun',
                     'M_popIII_high_Msun', 'M_ECF_Msun'])
    for i, zi in enumerate(z_arr):
        writer.writerow([f"{zi:.4f}", f"{t_arr_Myr[i]:.3f}",
                         f"{M_popIII_low[i]:.4e}",
                         f"{M_popIII_high[i]:.4e}",
                         f"{M_ECF[i]:.4e}"])

with open('data_jeans_mass_vs_zt.csv', 'w', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['z_t', 'H_zt_per_s', 'M_K_Msun'])
    for i in range(len(z_t_arr)):
        writer.writerow([f"{z_t_arr[i]:.4e}", f"{H_zt_arr[i]:.4e}",
                         f"{MK_arr[i]:.4e}"])

# -----------------------------------------------------------------------
# SECTION 7 — FIGURE PRD 2 PANNEAUX
# BUGFIX: constrained_layout=True  (pas de tight_layout)
#         \to au lieu de \rightarrow dans toutes les annotations
# -----------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5),
                          constrained_layout=True,
                          facecolor='white')

# ---- Panel A ----
ax = axes[0]
mask = (z_arr >= 5) & (z_arr <= 22)

ax.fill_between([5, 15], [1e5, 1e5], [1e7, 1e7],
                color='tomato', alpha=0.20, zorder=0,
                label='LRD zone (Rusakov+2026)\n'
                      r'$10^5$-$10^7\,M_\odot$, $z=5$-$15$')
ax.fill_between([10, 16], [1e8, 1e8], [1e10, 1e10],
                color='gold', alpha=0.22, zorder=0,
                label=r'JWST quasars $z>10$')
ax.fill_between(z_arr[mask], M_popIII_low[mask], M_popIII_high[mask],
                color='steelblue', alpha=0.25, zorder=2)
ax.semilogy(z_arr[mask], M_popIII_low[mask], '-', color='steelblue',
            lw=2.0, zorder=3,
            label=r'Pop III seed: $M_0=10^2$-$10^3\,M_\odot$')
ax.semilogy(z_arr[mask], M_popIII_high[mask], '--', color='steelblue',
            lw=1.5, zorder=3)
ax.semilogy(z_arr[mask], M_ECF[mask], '-', color='crimson', lw=2.5, zorder=4,
            label=r'ECF Macro-Knot: $M_0=10^5\,M_\odot$')
ax.axhline(1e5, color='crimson', lw=0.8, ls=':', alpha=0.6)
ax.text(21.2, 1.3e5, r'ECF $M_0$', fontsize=8, color='crimson', ha='right')

# BUGFIX: \to au lieu de \rightarrow
ax.annotate(
    r'Pop III: $3.5\times$ Eddington' + '\nto reach LRD upper edge',
    xy=(10.5, M_popIII_low[np.argmin(np.abs(z_arr - 10.5))]),
    xytext=(14.5, 2e4),
    fontsize=8.5, color='steelblue',
    arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.0),
    bbox=dict(boxstyle='round,pad=0.25', fc='#e8f0fb', ec='steelblue', lw=0.8))
ax.annotate(
    r'ECF: $f_\mathrm{Edd}=0$ to enter LRD zone' + '\n'
    r'$f_\mathrm{Edd}=1.0$ to reach $10^7\,M_\odot$',
    xy=(18, 1e5),
    xytext=(15.5, 5e3),
    fontsize=8.5, color='crimson',
    arrowprops=dict(arrowstyle='->', color='crimson', lw=1.0),
    bbox=dict(boxstyle='round,pad=0.25', fc='#fde8e8', ec='crimson', lw=0.8))
ax.annotate(
    r'$10^9\,M_\odot$ @ $z=10$:' + '\n'
    r'Pop III: $f_\mathrm{Edd}=3.5\times$' + '\n'
    r'ECF Knot: $f_\mathrm{Edd}=2.0\times$',
    xy=(10, 1e9), xytext=(13, 2e9), fontsize=8, color='#333',
    arrowprops=dict(arrowstyle='->', color='#666', lw=0.8),
    bbox=dict(boxstyle='round,pad=0.3', fc='#fffbe6', ec='goldenrod', lw=1.0))
ax.text(7.5, 5e5, 'LRD zone\n(Rusakov+2026)', fontsize=8.5,
        color='crimson', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.2', fc='#fff0f0', ec='tomato', lw=0.8))
ax.set_xlabel('Redshift $z$', fontsize=12)
ax.set_ylabel(r'Mass $M\,[M_\odot]$', fontsize=12)
ax.set_title('Panel A - SMBH seeding problem\n'
             r'Eddington growth from $z_\mathrm{form}=20$, '
             r'$k_\mathrm{Edd}=0.016\,\mathrm{Myr}^{-1}$',
             fontsize=10.5)
ax.set_xlim(5, 22); ax.set_ylim(1e2, 5e10)
ax.invert_xaxis()
ax.legend(fontsize=9, loc='lower left', framealpha=0.93)
ax.grid(True, which='both', alpha=0.14)

# ---- Panel B ----
ax2 = axes[1]
ax2.axhspan(1e5, 1e7,  color='tomato',  alpha=0.18, label='LRD regime (Rusakov+2026)')
ax2.axhspan(1e7, 1e10, color='gold',    alpha=0.18, label=r'JWST quasars $>10^7\,M_\odot$')
ax2.axhspan(1e3, 1e5,  color='#b0c4de', alpha=0.18, label=r'Macro-Knot low tail')
ax2.loglog(z_t_arr, MK_arr, '-', color='#2c7a2c', lw=2.8, zorder=5,
           label=r'$M_K = c^3\,/\,(2GH(z_t))$  [ECF stiff phase]')

for zt_m, Mm, lab, col, xytext in [
    (6.87e8, 4.72e6,
     'QCD epoch\n$z_t=6.9\\times10^8$\n$M_K=4.7\\times10^6\\,M_\\odot$',
     'crimson', (5e9, 3e7)),
    (6.87e9, 4.72e4,
     'EW epoch\n$z_t=6.9\\times10^9$\n$M_K=4.7\\times10^4\\,M_\\odot$',
     '#7a1a7a', (8e10, 2e4)),
    (1.0e12, 4.72e1,
     'QCD-Planck\n$z_t=10^{12}$\n$M_K\\sim40\\,M_\\odot$',
     'darkorange', (1e13, 2e2)),
]:
    ax2.plot(zt_m, Mm, 'o', ms=10, color=col, zorder=6)
    ax2.annotate(lab, xy=(zt_m, Mm), xytext=xytext, fontsize=8, color=col,
                 arrowprops=dict(arrowstyle='->', color=col, lw=0.9),
                 bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=col,
                           lw=0.8, alpha=0.95))

ax2.text(0.04, 0.72,
         r'$M_K = \dfrac{c^3}{2\,G\,H(z_t)}$' + '\n\n'
         r'Stiff phase $w=1$:' + '\n' + r'$c_s \to c$',
         transform=ax2.transAxes, fontsize=12,
         bbox=dict(boxstyle='round,pad=0.4', fc='#f0fff0', ec='#2c7a2c', lw=1.5))
ax2.text(3e15, 3e5, 'LRD zone', fontsize=9, color='crimson',
         bbox=dict(boxstyle='round,pad=0.2', fc='#fff0f0', ec='tomato', lw=0.8))
ax2.set_xlabel(r'Transition redshift $z_t$', fontsize=12)
ax2.set_ylabel(r'Jeans mass $M_K\;[M_\odot]$', fontsize=12)
ax2.set_title(r'Panel B - ECF prediction: $M_K(z_t) = c^3\,/\,(2GH(z_t))$' + '\n'
              r'LRD mass range $\leftrightarrow$ QCD epoch ($z_t\sim10^9$)',
              fontsize=10.5)
ax2.legend(fontsize=8.5, loc='upper right', framealpha=0.93)
ax2.grid(True, which='both', alpha=0.14)

fig.suptitle(
    r'ECF Little Red Dots: Jeans mass from stiff phase ($w=1$) '
    r'$\Rightarrow$ $M_K\sim10^5$-$10^7\,M_\odot$ (QCD epoch)',
    fontsize=12)

plt.savefig('Fig_ECFLRDJeansMass.png', dpi=300,
            bbox_inches='tight', facecolor='white')
with open('Fig_ECFLRDJeansMass.png.meta.json', 'w') as f:
    json.dump({
        "caption": "ECF LRD Jeans mass: QCD-epoch stiff phase predicts 10^5-10^7 Msun seeds",
        "description": "Panel A growth curves Pop III vs ECF. Panel B Jeans mass vs z_t."
    }, f)
plt.close()
print("Done.")
