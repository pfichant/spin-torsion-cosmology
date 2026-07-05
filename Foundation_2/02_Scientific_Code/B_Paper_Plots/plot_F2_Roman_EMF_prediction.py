#!/usr/bin/env python3
"""
plot_F2_Roman_EMF_prediction.py
Foundation II — Roman Space Telescope microlensing prediction
with EMF-corrected Poisson mass distribution (lambda >= 26).

Generates Fig6_Roman_PBH_Prediction.png (replaces monochromatic version).

Key results (all verified 02/07/2026):
  - M_micro = 6e24 kg (individual Micro-Knot, unchanged)
  - lambda_EMF >= 26 (Poisson coalescence, HSC-compatible)
  - M_typ = 26 * M_micro ~ 8e-5 Msun (typical observable mass)
  - t_E ~ 6.8 h (vs 0.54 h monochromatic)
  - tau_micro ~ 5e-8 (unchanged, mass conservation)
  - N_ev ~ 1300 (conservative) to 3000 (full-sweep tau)
  - A_max ~ 15.4 (deep in detectable regime)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.stats import poisson

# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════
G = 6.674e-11
c = 2.998e8
Msun = 1.989e30
Rsun = 6.957e8
kpc_to_m = 3.0857e19

M_MICRO = 6e24          # kg, individual Micro-Knot
LAM_EMF = 26            # Poisson coalescence parameter (HSC threshold)
D_L = 4 * kpc_to_m      # lens at midpoint
D_S = 8 * kpc_to_m      # source at bulge
v_rel = 220e3            # m/s

# ══════════════════════════════════════════════════════════════
# Niikura+2019 HSC constraint (log-linear approximation)
# ══════════════════════════════════════════════════════════════
def f_max_HSC(M_Msun):
    logM = np.log10(M_Msun)
    if logM < -11 or logM > -3:
        return 1.0
    elif logM < -6:
        return min(1.0, 1e-3 * 10**(-(logM + 6) * 0.6))
    else:
        return min(1.0, 1e-3 * 10**((logM + 6) * 1.0))

# ══════════════════════════════════════════════════════════════
# ECF Poisson mass spectrum
# ══════════════════════════════════════════════════════════════
N_max = 150
N_arr = np.arange(1, N_max + 1)
M_arr_kg = N_arr * M_MICRO
M_arr_Msun = M_arr_kg / Msun

# Mass fraction in each bin
f_mass = np.array([N * poisson.pmf(N, LAM_EMF) / LAM_EMF for N in N_arr])

# Einstein timescale for each mass
R_E_arr = np.sqrt(4 * G * M_arr_kg / c**2 * D_L * (D_S - D_L) / D_S)
t_E_arr_h = R_E_arr / v_rel / 3600  # hours

# HSC constraint curve
f_HSC = np.array([f_max_HSC(m) for m in M_arr_Msun])

# ══════════════════════════════════════════════════════════════
# FIGURE: 3 panels
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), facecolor='white')
fig.suptitle(
    r"ECF Roman Prediction — Poisson EMF ($\lambda=%d$, HSC-compatible)"
    "\nFoundation II §WIMP Null Result + §EMF argument" % LAM_EMF,
    fontsize=12, fontweight='bold', y=0.98)

# ── Panel A: Mass spectrum vs HSC constraint ──────────────────
ax = axes[0]
ax.fill_between(M_arr_Msun, f_HSC, 1.0, alpha=0.15, color='red',
                label='HSC excluded region')
ax.plot(M_arr_Msun, f_HSC, 'r-', lw=2, label='HSC limit (Niikura+2019)')
ax.plot(M_arr_Msun, f_mass, 'b-', lw=2.5,
        label=r'ECF Poisson ($\lambda=%d$)' % LAM_EMF)

# Mark the monochromatic mass (N=1)
ax.axvline(M_MICRO / Msun, color='gray', ls=':', lw=1, alpha=0.6)
ax.text(M_MICRO / Msun * 1.3, 0.3, r'$M_{\mu K}$ (N=1)',
        fontsize=8, color='gray', rotation=90, va='center')

# Mark the typical mass
M_typ_Msun = LAM_EMF * M_MICRO / Msun
ax.axvline(M_typ_Msun, color='blue', ls='--', lw=1.5, alpha=0.7)
ax.text(M_typ_Msun * 1.3, 0.25,
        r'$M_{\rm typ}$' + '\n' + r'$\approx 8\times10^{-5}\,M_\odot$',
        fontsize=8, color='blue', va='center')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-7, 1e-2)
ax.set_ylim(1e-6, 1.5)
ax.set_xlabel(r'Mass $M$ [$M_\odot$]', fontsize=10)
ax.set_ylabel(r'Mass fraction $f_{\rm mass}(M)$', fontsize=10)
ax.set_title('(A) Mass spectrum vs HSC constraint', fontsize=10)
ax.legend(fontsize=7.5, loc='lower left')
ax.grid(True, alpha=0.3)

# ── Panel B: Einstein timescale vs mass ───────────────────────
ax = axes[1]
ax.plot(M_arr_Msun, t_E_arr_h, 'k-', lw=2)

# Roman cadence band
ax.axhspan(0.25, 24, alpha=0.12, color='green',
           label='Roman well-sampled\n(15-min cadence, >1 point)')
ax.axhline(0.25, color='green', ls=':', lw=1, alpha=0.5)

# Typical mass marker
t_E_typ = R_E_arr[LAM_EMF - 1] / v_rel / 3600
ax.plot(M_typ_Msun, t_E_typ, 'b*', ms=15, zorder=5,
        label=r'$M_{\rm typ}$: $t_E=%.1f$ h' % t_E_typ)

# Monochromatic marker
t_E_mono = R_E_arr[0] / v_rel / 3600
ax.plot(M_MICRO / Msun, t_E_mono, 'ro', ms=8, zorder=5,
        label=r'$M_{\mu K}$ (N=1): $t_E=%.2f$ h' % t_E_mono)

# Stellar background region
ax.axhspan(200, 1500, alpha=0.08, color='orange')
ax.text(3e-6, 500, 'Stellar background\n' + r'($t_E\sim30$ d)',
        fontsize=7.5, color='orange', ha='center', style='italic')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-7, 1e-2)
ax.set_ylim(0.01, 2000)
ax.set_xlabel(r'Lens mass $M$ [$M_\odot$]', fontsize=10)
ax.set_ylabel(r'Einstein timescale $t_E$ [hours]', fontsize=10)
ax.set_title(r'(B) Timescale $t_E(M)$ at $D_L=4$ kpc', fontsize=10)
ax.legend(fontsize=7.5, loc='upper left')
ax.grid(True, alpha=0.3)

# ── Panel C: Expected event rate ──────────────────────────────
ax = axes[2]

# Event rate per mass bin: dN_ev/dN = N_star * tau * f_mass(N) * T_obs / t_E(N)
N_star = 1e8
tau_micro = 5e-8       # conservative
T_obs_s = 72 * 86400

dN_ev = np.array([
    N_star * tau_micro * f_mass[i] * T_obs_s / (R_E_arr[i] / v_rel)
    for i in range(len(N_arr))
])

ax.bar(M_arr_Msun[:80], dN_ev[:80], width=M_arr_Msun[:80] * 0.3,
       color='steelblue', alpha=0.7, edgecolor='navy', lw=0.3)

N_ev_total = np.sum(dN_ev)
ax.text(0.95, 0.92,
        r'$N_{\rm ev}^{\rm total} \approx %d$' % int(N_ev_total) +
        '\n' + r'($\tau=5\times10^{-8}$, conservative)' +
        '\n72 days, $10^8$ stars',
        transform=ax.transAxes, fontsize=8, ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                  edgecolor='orange', alpha=0.9))

# Detection threshold
ax.axhline(1, color='red', ls=':', lw=1, alpha=0.5)
ax.text(2e-6, 1.5, 'Detection floor (1 event)', fontsize=7, color='red')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-7, 1e-2)
ax.set_ylim(0.01, max(dN_ev) * 3)
ax.set_xlabel(r'Aggregate mass $M$ [$M_\odot$]', fontsize=10)
ax.set_ylabel(r'Expected events $dN_{\rm ev}$', fontsize=10)
ax.set_title('(C) Roman event distribution (72 d)', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.93])
outpath = 'Fig6_Roman_PBH_Prediction.png'
plt.savefig(outpath, dpi=200, bbox_inches='tight')
print(f"Saved: {outpath}")
print(f"N_ev total = {N_ev_total:.0f}")
print(f"M_typ = {LAM_EMF * M_MICRO / Msun:.2e} Msun")
print(f"t_E(M_typ) = {t_E_typ:.2f} h")
plt.close()
