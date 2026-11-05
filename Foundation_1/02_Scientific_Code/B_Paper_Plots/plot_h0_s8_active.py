#!/usr/bin/env python3
# Last modified: 09/10/2026, 08:49 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
"""
plot_h0_s8_active.py — Foundation I, Fig. fig:contours (FIG-ACTIVES, 09/10/2026)

The H0–S8 plane on the ACTIVE background (A-7, Omega_m = omega_m/h^2 = 0.267).
Replaces plot_h0_s8_contours.py (historical calibration gamma_spin = 0.3116,
Omega_m = 0.315), archived in Scripts_SUPERSEDED/.

  ECF : H0 = 73.04, calibrated through r_s = 135.65 Mpc (vertical line).
        No ECF value of S8: the growth of structure needs a perturbative chain
        not yet available (OPEN).
  Grey diamond : CAMB LCDM reference on the closure background, S8 ~ 0.780
        (Foundation I, Sec. tensions) -- a conditional reference, NOT an ECF prediction.
  Planck 2018 LCDM: H0 = 67.4 +/- 0.5, S8 = 0.832 +/- 0.013 (1 sigma, true size).
  SH0ES: 73.04 +/- 1.04 ; KiDS-1000: S8 = 0.766 +0.020/-0.014.
Output: Figure_H0_S8_Active.png
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

H0_ECF, RS_ECF, OM_ECF = 73.04, 135.65, 0.267
S8_CAMB_REF = 0.780

fig, ax = plt.subplots(figsize=(10, 6.2))
ax.add_patch(Ellipse((67.4, 0.832), 2*0.5, 2*0.013, color='royalblue', alpha=0.45,
             label=r'Planck 2018 $\Lambda$CDM ($H_0=67.4\pm0.5$, $S_8=0.832\pm0.013$)'))
ax.axvspan(73.04-1.04, 73.04+1.04, color='green', alpha=0.15, label=r'SH0ES ($H_0=73.04\pm1.04$)')
ax.axhspan(0.766-0.014, 0.766+0.020, color='orange', alpha=0.2,
           label=r'KiDS-1000 ($S_8=0.766^{+0.020}_{-0.014}$, $H_0$ unconstrained)')
ax.axvline(H0_ECF, color='crimson', lw=2.5,
           label=r'ECF: $H_0=73.04$ (calibrated on $r_s=135.65$ Mpc, $\Omega_m=0.267$)')
ax.annotate('', xy=(H0_ECF, 0.73), xytext=(H0_ECF, 0.86),
            arrowprops=dict(arrowstyle='<->', color='crimson', lw=1.5))
ax.text(73.35, 0.845, 'ECF $S_8$: OPEN\n(no perturbative chain;\nno ECF value)', color='crimson', fontsize=10, va='top')
ax.plot(H0_ECF, S8_CAMB_REF, 'D', color='gray', ms=9, mfc='white', mew=2,
        label=r'CAMB $\Lambda$CDM reference on the closure background: $S_8\simeq0.780$ (conditional, not an ECF prediction)')
ax.set_xlim(64.5, 76.5); ax.set_ylim(0.72, 0.87)
ax.set_xlabel(r'$H_0$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=12); ax.set_ylabel(r'$S_8$', fontsize=12)
ax.set_title(r'The $H_0$–$S_8$ plane on the active background ($\Omega_m=\omega_m/h^2$)', fontsize=13)
ax.legend(fontsize=8.3, loc='lower left'); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('Figure_H0_S8_Active.png', dpi=300)
print('Saved: Figure_H0_S8_Active.png')
