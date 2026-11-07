# =============================================================================
# simECFLRDJeansMass.py — ECF Foundation II
# PRD referee documentation -- detailed comments
#
# TITLE: Little Red Dots as primordial ECF Macro-Knots
#         Hubble causal mass scale at topological freeze-out
#         [REQUALIFIE 17/09/2026 — MEMO 43]
#
# PURPOSE
# -------
# Demonstrate that the "Little Red Dots" (LRDs) detected by JWST at z > 5
# — compact objects with inferred masses ~10^5–10^7 Msun — are a NATURAL,
# causal Hubble mass scale (NOT a zero-free-parameter prediction of an object:
# the collapse efficiency eps_coll = M_object/M_H is NOT derived), rather than
# requiring fine-tuned super-Eddington accretion from stellar remnants.
#
# PHYSICAL BASIS
# --------------
# In the ECF model (Foundation I, Eq. eqmodifiedfriedmann), the post-bounce
# universe undergoes a STIFF FLUID ERA (w=1) during which:
#       rho_spin ~ a^{-6}   =>   H(t) = 1/(3t)
#       c_s = c * sqrt(w) = c            [sound speed = speed of light]
#       lambda_J ~ c/H(z_t) = d_H ONLY in the stiff regime (c_s -> c).
#       [ATTENTION : la Grande Annihilation est HORS du regime stiff,
#        que le corpus termine vers t ~ 1e-11 s. Ne pas etiqueter la
#        courbe « stiff phase » pour l'epoque GA.]
#
# Hubble-sphere mass (NOT automatically a Jeans mass outside the stiff regime,
# and NOT a Macro-Knot mass):
#       M_K = c^3 / (2 G H(z_t))
#
# For the Great Annihilation freeze-out (z_t ~ 10^9, T ~ 0.2-1.6 MeV,
# e+e- annihilation epoch):
#       M_K ~ 1.0e7 Msun at z_t = 6.9e8   => LRD upper mass range (computed, omega_r = 4.1834e-5)
# For z_t ~ 7e9 (upper edge of the Great Annihilation window):
#       M_K ~ 1.0e5 Msun at z_t = 6.9e9   => LRD lower mass range (computed)
# For reference, the true QCD confinement transition (z_t ~ 1e12,
# T ~ 235 MeV) gives M_K ~ 5 Msun (computed: 4.8) -- far below the LRD range, confirming
# that it is the Great Annihilation window, not the QCD transition, that
# is cosmologically relevant here.
#
# CAVEAT (ARBITRAGE 02/10/2026, point 4): H(z_t) above is the RADIATION-ONLY expansion
# rate (Omega_r only; no spin term). In the ECF background (A-7 spin term extrapolated to
# z_t) H is larger by a factor ~3.8e4 (z_t = 6.9e8) to ~3.8e5 (z_t = 6.9e9), which would
# reduce M_K by about 4.6 to 5.6 orders of magnitude (to ~3e2 and ~0.3 Msun). Whether the
# spin term applies at these z_t is the same open question as PO-ECF-BBN-SPIN.
#
# KEY RESULT (radiation-only H; NOT zero free parameters):
#       z_t in [6.9e8, 6.9e9]  <=>  M_K in [1e5, 1e7] Msun
#       = same ORDER OF MAGNITUDE as the LRD compact-object mass range
#         (Rusakov+2026). Cette proximite motive l'echelle ; elle ne
#         demontre ni la formation d'objets compacts ni une population.
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
# REVISION HISTORY
# -----------------
# rev1 (Foundation II, Zenodo): original release. Epoch labels on Panel B
#   ("QCD epoch" / "EW epoch" / "QCD-Planck") were misassigned relative
#   to the actual temperature at each plotted z_t (verified 17/07/2026):
#     z_t=6.87e8 -> T=0.16 MeV  (Great Annihilation, NOT QCD)
#     z_t=6.87e9 -> T=1.6  MeV  (Great Annihilation, NOT EW)
#     z_t=1.0e12 -> T=235  MeV  (true QCD epoch, mislabeled "QCD-Planck")
#   The underlying physics/numbers (M_K values) were NOT affected --
#   only the epoch names attached to them.
# rev2 (Foundation II, this file): epoch labels corrected throughout (panel B
#   point annotations, panel B title, figure suptitle, meta.json caption)
#   to reflect the verified temperatures above. No numerical change.
# rev3 (23/10/2026): LRD observational window corrected. The LRD zone was drawn at
#   z = 5-15 (range not given by Rusakov+2026); observed LRDs lie mostly at z ~ 4-9,
#   spectroscopically confirmed up to z = 9.29 (Taylor+2025, arXiv:2505.04609).
#   Zone now z = 4-9.3. The box "JWST quasars z>10, 1e8-1e10 Msun" (no such measured
#   objects) is replaced by the measured black holes UHZ1 and J1342+0928.
#   Consequence: at f_Edd = 1 the ECF seed exceeds 1e7 Msun by z ~ 10, so LRD masses at
#   z = 4-9 need f_Edd <~ 0.85-0.3 (computed below); a stellar seed at f_Edd = 1 also
#   reaches 1e5-1e6 Msun at z ~ 8-7. The LRD mass range alone does not discriminate seeds.
#   Also: growth drawn solid only for z <= z_form (dotted plateau before: assumption).
#   Also: MoM-z14 redshift marker (no BH mass); panel B title/legend/spin reserve.
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
# [D3, 22/09/2026 -- DEC-A7-POST-05] Generic round background (H0 = 70, Omega_m = 0.30),
# illustrative Jeans-mass scales: NOT the ECF background (A-7: 0.267 at H0 = 73.04). Kept.
Omega_m = 0.30
# [ARBITRAGE 02/10/2026, point 4] Omega_r derived from omega_r = Omega_r h^2 = 4.1834e-5
# (photons + 3 massless neutrinos), consistent with the corpus; the former 9.0e-5
# overestimated H(z) in radiation domination by ~2.7 % (=> M_K ~ 2.7 % too low... see MEMO).
omega_r = 4.1834e-5
Omega_r = omega_r / (H0_kms/100.0)**2
Omega_L = 1.0 - Omega_m - Omega_r

# -----------------------------------------------------------------------
# SECTION 2 — HUBBLE RATE H(z)
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
# -----------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5),
                          constrained_layout=True,
                          facecolor='white')

# ---- Panel A ----
ax = axes[0]
mask = (z_arr >= 4) & (z_arr <= 22)

ax.fill_between([4, 9.3], [1e5, 1e5], [1e7, 1e7],
                color='tomato', alpha=0.20, zorder=0,
                label='LRD zone: masses of Rusakov+2026,\n'
                      r'$10^5$-$10^7\,M_\odot$; observed at $z\approx4$-$9.3$')
# measured early black holes (values as in plot_growth_comparison.py)
for (zo, mo, lab, dx, dy) in [(10.07, 4e7, 'UHZ1 (z=10.07)', 0.4, 1.0),
                              (7.54, 7.8e8, 'J1342+0928 (z=7.54)', 0.4, 1.0)]:
    ax.plot(zo, mo, 'o', color='black', ms=8, zorder=7)
    ax.annotate(lab, xy=(zo, mo), xytext=(zo+dx, mo*3), fontsize=8.5, zorder=7)
ax.plot([], [], 'o', color='black', ms=8, label='Measured black holes')
ax.axvline(14.44, color='0.45', ls=':', lw=1.3, zorder=1)
ax.text(14.3, 1.5e10, 'MoM-z14: spectroscopic galaxy\nrecord ($z=14.44$), no BH mass', fontsize=8,
        color='0.35', ha='right', va='center')
mask_g = mask & (z_arr <= z_form + 0.1)   # growth phase (solid)
mask_p = mask & (z_arr >= z_form - 0.1)   # before z_form: no growth by assumption (dotted)
ax.fill_between(z_arr[mask_g], M_popIII_low[mask_g], M_popIII_high[mask_g],
                color='steelblue', alpha=0.25, zorder=2)
ax.semilogy(z_arr[mask_g], M_popIII_low[mask_g], '-', color='steelblue',
            lw=2.0, zorder=3,
            label=r'Pop III seed: $M_0=10^2$-$10^3\,M_\odot$')
ax.semilogy(z_arr[mask_g], M_popIII_high[mask_g], '--', color='steelblue',
            lw=1.5, zorder=3)
ax.semilogy(z_arr[mask_g], M_ECF[mask_g], '-', color='crimson', lw=2.5, zorder=4,
            label=r'ECF Macro-Knot: $M_0=10^5\,M_\odot$')
def _f_needed(z, Mtarget, M0):
    dt = np.interp(z, z_arr, t_arr_Myr) - t_form_Myr
    return np.log(Mtarget / M0) / (k_Edd * dt)
_fa, _fb, _fc = (_f_needed(z, 1e7, M0_ECF) for z in (9.3, 7.0, 5.0))
_pa = M0_popIII_low * np.exp(k_Edd * (np.interp(7.0, z_arr, t_arr_Myr) - t_form_Myr))
for _M, _c in ((M_popIII_low, 'steelblue'), (M_popIII_high, 'steelblue'), (M_ECF, 'crimson')):
    ax.semilogy(z_arr[mask_p], _M[mask_p], ':', color=_c, lw=1.4, zorder=3)
ax.text(21.0, 3.4e5, 'no growth before\n$z_\\mathrm{form}=20$ (assumption)', fontsize=7.5,
        color='crimson', ha='center', va='bottom')
ax.axhline(1e5, color='crimson', lw=0.8, ls=':', alpha=0.6)
ax.text(21.2, 1.3e5, r'ECF $M_0$', fontsize=8, color='crimson', ha='right')

ax.annotate(
    'ECF seed at $f_\\mathrm{Edd}=1$ exceeds $10^7\\,M_\\odot$ by $z\\approx10$:\n'
    r'to stay in the LRD mass range it needs' + '\n'
    r'$f_\mathrm{Edd}\lesssim%.2f$ ($z=9.3$), $%.2f$ ($z=7$), $%.2f$ ($z=5$)' % (_fa, _fb, _fc),
    xy=(9.3, M_ECF[np.argmin(np.abs(z_arr-9.3))]), xytext=(21.5, 4e8), fontsize=8.5, color='crimson',
    arrowprops=dict(arrowstyle='->', color='crimson', lw=1.0),
    bbox=dict(boxstyle='round,pad=0.25', fc='#fde8e8', ec='crimson', lw=0.8))
ax.annotate(
    'Pop III seed at $f_\\mathrm{Edd}=1$ (low edge):\n'
    r'$\approx10^{%d}\,M_\odot$ at $z=7$, inside the LRD mass range' % int(round(np.log10(_pa))),
    xy=(7.0, _pa), xytext=(18.5, 2.5e4), fontsize=8.5, color='steelblue',
    arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.0),
    bbox=dict(boxstyle='round,pad=0.25', fc='#e8f0fb', ec='steelblue', lw=0.8))
ax.text(6.6, 5e5, 'LRD zone', fontsize=8.5,
        color='crimson', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.2', fc='#fff0f0', ec='tomato', lw=0.8))
ax.set_xlabel('Redshift $z$', fontsize=12)
ax.set_ylabel(r'Mass $M\,[M_\odot]$', fontsize=12)
ax.set_title('Panel A - SMBH seeding problem\n'
             r'Eddington growth from $z_\mathrm{form}=20$, '
             r'$k_\mathrm{Edd}=0.016\,\mathrm{Myr}^{-1}$' + '\n(generic background $H_0=70$, $\\Omega_m=0.3$; illustrative)',
             fontsize=10.5)
ax.set_xlim(4, 22); ax.set_ylim(1e2, 5e10)
ax.invert_xaxis()
ax.legend(fontsize=9, loc='lower left', framealpha=0.93)
ax.grid(True, which='both', alpha=0.14)

# ---- Panel B ----
ax2 = axes[1]
ax2.axhspan(1e5, 1e7,  color='tomato',  alpha=0.18, label='LRD BH masses, electron-scattering corrected (Rusakov+2026)')
ax2.axhspan(4e7, 8e8, color='gold',    alpha=0.18, label=r'Measured early BHs (UHZ1, J1342+0928)')
ax2.axhspan(1e3, 1e5,  color='#b0c4de', alpha=0.18, label=r'Macro-Knot low tail')
ax2.loglog(z_t_arr, MK_arr, '-', color='#2c7a2c', lw=2.8, zorder=5,
           label=r'$M_K = c^3\,/\,(2GH(z_t))$  [radiation-only $H$]')

# REV2 (17/07/2026): epoch labels corrected to match the verified
# temperature at each z_t (see REVISION HISTORY above). Numerical
# values (z_t, M_K) are UNCHANGED from rev1 -- only the physical
# epoch name attached to each point was wrong.
# [ARBITRAGE 02/10/2026, point 4] Marker values were hard-coded (4.72e6, 4.72e4, 47.2)
# and did NOT lie on the curve computed above (~1.0e7, 1.0e5, 4.8 Msun). They are now
# computed from the same function as the curve; labels are generated from the values.
def _MK(zt):
    return c**3 / (2.0 * G * Hz_rad(zt)) / Msun
def _fmt(m):
    e = int(np.floor(np.log10(m)))
    return r'%.2f\times10^{%d}' % (m / 10**e, e) if m >= 1e3 else r'%.1f' % m
for zt_m, lab, col, xytext in [
    (6.87e8,
     'Great Annihilation\n$z_t=6.9\\times10^8$ ($T\\approx0.16$ MeV)\n$M_K=%s\\,M_\\odot$' % _fmt(_MK(6.87e8)),
     'crimson', (5e9, 3e7)),
    (6.87e9,
     'Great Annihilation\n$z_t=6.9\\times10^9$ ($T\\approx1.6$ MeV)\n$M_K=%s\\,M_\\odot$' % _fmt(_MK(6.87e9)),
     '#7a1a7a', (8e10, 2e4)),
    (1.0e12,
     'QCD epoch\n$z_t=10^{12}$ ($T\\approx235$ MeV)\n$M_K=%s\\,M_\\odot$' % _fmt(_MK(1.0e12)),
     'darkorange', (1e13, 2e2)),
]:
    Mm = _MK(zt_m)
    ax2.plot(zt_m, Mm, 'o', ms=10, color=col, zorder=6)
    ax2.annotate(lab, xy=(zt_m, Mm), xytext=xytext, fontsize=8, color=col,
                 arrowprops=dict(arrowstyle='->', color=col, lw=0.9),
                 bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=col,
                           lw=0.8, alpha=0.95))

ax2.text(0.04, 0.72,
         r'$M_K = \dfrac{c^3}{2\,G\,H(z_t)}$' + '\n\n'
         r'Radiation-only $H(z_t)$;' + '\n' + r'spin term not included' + '\n' + r'(with it $M_K$ falls by $\sim5$ dex: open)',
         transform=ax2.transAxes, fontsize=12,
         bbox=dict(boxstyle='round,pad=0.4', fc='#f0fff0', ec='#2c7a2c', lw=1.5))
ax2.text(3e15, 3e5, 'LRD zone', fontsize=9, color='crimson',
         bbox=dict(boxstyle='round,pad=0.2', fc='#fff0f0', ec='tomato', lw=0.8))
ax2.set_xlabel(r'Transition redshift $z_t$', fontsize=12)
ax2.set_ylabel(r'Jeans mass $M_K\;[M_\odot]$', fontsize=12)
ax2.set_title(r'Panel B - ECF causal mass scale: $M_K(z_t) = c^3\,/\,(2GH(z_t))$' + '\n'
              r'LRD mass range $\leftrightarrow$ Great Annihilation ($z_t\sim10^9$)',
              fontsize=10.5)
ax2.legend(fontsize=8.5, loc='upper right', framealpha=0.93)
ax2.grid(True, which='both', alpha=0.14)

fig.suptitle(
    r'ECF Little Red Dots: Hubble mass $M_K$ at the Great Annihilation epoch '
    r'(radiation-only $H$): $M_K\sim10^5$-$10^7\,M_\odot$',
    fontsize=12)

plt.savefig('Fig_ECFLRDJeansMass.png', dpi=300,
            bbox_inches='tight', facecolor='white')
with open('Fig_ECFLRDJeansMass.png.meta.json', 'w') as f:
    json.dump({
        "caption": "ECF LRD causal mass scale: Hubble-sphere mass c^3/(2GH) at the Great-Annihilation epoch (radiation-only H), 10^5-10^7 Msun; Jeans mass proper smaller by 3^(3/2) (c_s = c/sqrt(3))",
        "description": "Panel A growth curves Pop III vs ECF. Panel B Jeans mass vs z_t."
    }, f)
plt.close()
print("Done.")
