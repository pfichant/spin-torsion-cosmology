#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_euclid_pk_S8.py  --  v2  (17 Apr 2026)
============================================
Figure double-panel: Matter Power Spectrum P(k) -- ECF vs LCDM
Foundation I Extended, Sections 4-5  (v2-150426)

Author: Pascal Fichant

Physical derivation
-------------------
Transfer function (BBKS 1986):
    T(k) = [ln(1+2.34q)/(2.34q)] * [1 + 3.89q + (16.1q)^2
            + (5.46q)^3 + (6.71q)^4]^{-1/4}
    q = k / (Omega_m * h^2)   [h/Mpc]
    Omega_m = omega_m/h^2 = 0.2669,  h = 0.7304  (A-7; was 0.315, Planck 2018)

    v1 bug: q = k/(Omega_m*h)  ->  k_eq shifted by factor 1/h = 1.49.
    v2 fix: q = k/(Omega_m*h^2) = k/0.168  (correct BBKS normalisation).

ECF torsion suppression (F1 Sec. 4):
    G_eff(k) = G_N [1 - alpha * k^2/k_cut^2]     (ECKS leading-order gradient)
    Regularised Lorentzian, T^2 in [0,1] for all k:
    T_tors^2(k) = 1 - A_sup * k^2 / (k^2 + k_cut^2)
    A_sup = 0.15,  k_cut = 0.10 h/Mpc  (F1 Sec. 4-5)
    T^2(k_cut)    = 0.925
    T^2(k>>k_cut) = 0.850  (15% maximum suppression)
    Status (DEC-A7-POST-07C, 22/09/2026): phenomenological, not canonical;
    NOT calibrated on S8 = 0.766; its articulation with gamma_spin is not
    demonstrated (no double counting). Propagated into sigma8 on the CAMB
    LCDM reference of the A-7 background, A_sup = 0.15 gives S8 ~ 0.740 and
    A_sup ~ 0.053 would reproduce 0.766 (diagnostic only,
    calc_S8_reference_camb_A7.py).

S8 values (F1 Sec. 5):
    S8_LCDM = 0.832 (Planck 2018) ; sigma8_LCDM = 0.832/sqrt(0.315/0.3) = 0.8119
    S8_ECF  = 0.766  observational target (KiDS-1000), not an ECF prediction;
              the P(k) curves below are not normalised to it and T^2 is not
              propagated into sigma8 here (Delta_chi^2 = -39.5: historical)

Euclid simulated forecast:
    15 log-spaced k in [0.032, 2.0] h/Mpc, sigma_rel=3%, seed=42.

Output
------
    Figure_Euclid_Pk_S8.png  (300 dpi)
"""
# Last modified: 25/08/2026, 21:49 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ---------------------------------------------------------------------------
# Parameters -- anchored to F1 Extended v2-150426
# ---------------------------------------------------------------------------
H0           = 73.04
h            = H0 / 100.0
Omega_m      = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
Omega_m_LCDM = 0.315   # Planck, used only for the LCDM sigma8 label
ns           = 0.965
# [18/08/2026 audit] These two lines were inverted. They read
#   sigma8_LCDM = 0.832 ; S8_LCDM = sigma8_LCDM*sqrt(Omega_m/0.3) = 0.853
# but 0.832 is Planck's S_8, not its sigma_8 (Planck 2018: sigma_8 = 0.811,
# S_8 = 0.832). Every other place in F1 uses S_8^LCDM = 0.832 -- including
# Eq. (19), on which gamma_spin = 0.3116 was calibrated (historical) -- so this figure was
# the only one displaying 0.853. Two orphan scripts written four days later
# (plot_spectre_puissance.py, plot_S8_resolution.py) already had it right.
# The ECF side was always computed correctly; only the LCDM side was inverted.
S8_LCDM      = 0.832                                  # Planck 2018
sigma8_LCDM  = S8_LCDM / np.sqrt(Omega_m_LCDM / 0.3)  # = 0.8119

k_cut        = 0.10           # h/Mpc  (F1 Sec. 4)
A_sup        = 0.15           # phenomenological, not canonical; NOT calibrated on S8 = 0.766 (DEC-A7-POST-07C)
S8_ECF       = 0.766          # KiDS-1000 target (label only; not used in the curves)

k_disc_lo    = 0.08
k_disc_hi    = 0.30

# 17/08/2026 audit: this line read an absolute POSIX path, /tmp/Figure_...png.
# It was the only absolute path in the whole F1 set. Two consequences: the
# figure landed outside the repository tree, so run_all_simulations_F1.py
# never collected it (verified: 30 of 31 figures centralized, this one not),
# and on Windows that path does not exist at all. Now relative, like every
# other script in the set.
OUTPUT_FILE  = 'Figure_Euclid_Pk_S8.png'


# ---------------------------------------------------------------------------
# BBKS transfer function  (Bardeen et al. 1986)
# ---------------------------------------------------------------------------
k    = np.logspace(-2.5, 0.5, 500)
q    = k / (Omega_m * h**2)          # correct: Omega_m*h^2 = 0.168
T_k  = (np.log(1.0 + 2.34*q) / (2.34*q) *
        (1.0 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25))
Pk_LCDM = k**ns * T_k**2 * 1e4       # [h^-3 Mpc^3]


# ---------------------------------------------------------------------------
# ECF torsion suppression
# ---------------------------------------------------------------------------
T_tors_sq = 1.0 - A_sup * k**2 / (k**2 + k_cut**2)
Pk_ECF    = Pk_LCDM * T_tors_sq


# ---------------------------------------------------------------------------
# Simulated Euclid forecast
# ---------------------------------------------------------------------------
k_euclid     = np.logspace(-1.5, 0.3, 15)
Pk_th_euclid = np.interp(k_euclid, k, Pk_ECF)
np.random.seed(42)
sigma_rel    = 0.03
Pk_data      = Pk_th_euclid + np.random.normal(0, sigma_rel * Pk_th_euclid)
yerr         = sigma_rel * np.abs(Pk_data)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 13,
                     'axes.linewidth': 1.4})

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(left=0.14, right=0.96, top=0.92, bottom=0.10, hspace=0.08)
gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

ax1 = fig.add_subplot(gs[0])
ax1.loglog(k, Pk_LCDM, 'b--', lw=2.0,
           label=rf'$\Lambda$CDM ($S_8={S8_LCDM:.3f}$, $\sigma_8={sigma8_LCDM:.3f}$)')
ax1.loglog(k, Pk_ECF,  'r-',  lw=2.8,
           label=r'ECF phenomenological $T^2(k)$ ($A_{\rm sup}=0.15$, not canonical)')
ax1.errorbar(k_euclid, Pk_data, yerr=yerr,
             fmt='o', color='k', ecolor='gray', elinewidth=1.5, capsize=3, ms=5,
             label=r'Euclid forecast (simulated, $\sigma_{\rm rel}=3\%$)')
ax1.axvspan(k_disc_lo, k_disc_hi, color='green', alpha=0.08,
            label=r'Discrimination window ($0.08$–$0.30\,h\,{\rm Mpc}^{-1}$)')
ax1.text(0.095, 600,
         r'Torsion suppression ($A_{\rm sup}=0.15$, $k_{\rm cut}=0.10\,h\,{\rm Mpc}^{-1}$)',
         color='#c0392b', fontsize=9.5, fontstyle='italic')
ax1.set_ylabel(r'$P(k)$  [$h^{-3}\,{\rm Mpc}^3$]', fontsize=13)
ax1.set_xlim(0.005, 2.0)
ax1.set_ylim(10, 3e4)
ax1.grid(True, which='both', ls=':', alpha=0.35)
ax1.legend(loc='lower left', fontsize=9.5, framealpha=0.92, edgecolor='#ccc')
ax1.set_xticklabels([])
ax1.set_title('Matter Power Spectrum: ECF torsion vs $\\Lambda$CDM — Euclid forecast',
              fontsize=12.5, fontweight='bold', pad=9)

ax2 = fig.add_subplot(gs[1])
ratio_th   = Pk_ECF / Pk_LCDM
ratio_data = Pk_data / np.interp(k_euclid, k, Pk_LCDM)
ratio_err  = yerr    / np.interp(k_euclid, k, Pk_LCDM)
ax2.semilogx(k, ratio_th, 'r-', lw=2.0)
ax2.axhline(1.0, color='b', ls='--', lw=1.5)
ax2.errorbar(k_euclid, ratio_data, yerr=ratio_err,
             fmt='o', color='k', ecolor='gray', elinewidth=1.5, capsize=3, ms=4)
ax2.axvspan(k_disc_lo, k_disc_hi, color='green', alpha=0.10)
ax2.text(0.105, 0.793, 'Discrimination window', color='darkgreen', fontsize=9.0)
ax2.axhline(1.0 - A_sup, color='#c0392b', ls=':', lw=1.2, alpha=0.7)
# 17/08/2026 audit: this label was clipped by the right-hand axis (visible in
# the published PDF, Fig. 8). Moved left and right-aligned so it stays inside.
ax2.text(0.98, 0.855, r'$T^2_{\rm min}=0.85$', color='#c0392b', fontsize=9,
         ha='right')
ax2.set_xlabel(r'Wavenumber $k$  [$h\,{\rm Mpc}^{-1}$]', fontsize=13)
ax2.set_ylabel(r'$P_{\rm ECF}/P_{\Lambda}$', fontsize=12)
ax2.set_xlim(0.005, 2.0)
ax2.set_ylim(0.75, 1.08)
ax2.grid(True, which='both', ls=':', alpha=0.35)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()

# [E2, 22/09/2026 -- DEC-A7-POST-07C] Status of the suppression drawn above.
print(f"Saved: {OUTPUT_FILE}")
print(f"T^2(k) = 1 - A_sup k^2/(k^2 + k_cut^2), A_sup = {A_sup}, k_cut = {k_cut} h/Mpc:")
print("  phenomenological, not canonical; NOT calibrated on S8 = 0.766 (DEC-A7-POST-07C)")
print("  articulation with gamma_spin not demonstrated (no double counting)")
print("  A_sup ~ 0.053 would reproduce 0.766 on the CAMB A-7 reference (diagnostic only,")
print("  calc_S8_reference_camb_A7.py); A_sup = 0.15 there gives S8 ~ 0.740")
