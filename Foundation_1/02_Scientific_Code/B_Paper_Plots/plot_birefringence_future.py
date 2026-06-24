"""
plot_birefringence_future.py  --  v2  (15 Apr 2026)
====================================================
Figure: Cosmic Birefringence Prediction (Foundation I, Fig. 6)
Author: Pascal Fichant

Physical derivation  (F1 Extended v2, Sections 6 and 7)
---------------------------------------------------------
The torsion pseudo-vector S^mu couples to the photon sector via an
effective Chern-Simons term, inducing a rotation of the CMB polarisation
plane (F1 Eq. 6.x):

    beta = (g_CS / 2) int_{t_LSS}^{t_0} f_a(Omega_spin) S^0(t) dt
         = g_CS_eff * I

The torsion-weighted line-of-sight integral (F1 Section 6, DESI sub-section):

    I = S_ref * int_0^{z_LSS} dz / E(z)
      = 4.32 * 3.118 = 13.48

Calibrating g_CS_eff to the Minami-Komatsu (2020) Planck signal:

    g_CS_eff = beta_obs / I = 0.35 / 13.48 = 2.60e-2 deg

yields a self-consistent ECF prediction beta_ECF = 0.35 +/- 0.04 deg,
where sigma_ECF is propagated from the uncertainty on F_ion = 1.2765
(Table 1 of F1).

Remark (F1 Section 6, explicit statement):
    "beta_ECF is a consistency check, not a parameter-free prediction;
     LiteBIRD (sigma_beta ~ 0.1 deg) will convert it into a genuine
     falsifiable constraint."

Discrimination power: beta_ECF / sigma_LiteBIRD = 0.35 / 0.10 = 3.5 sigma
from the LCDM null hypothesis beta = 0.

Inputs matched to F1 Extended v2
---------------------------------
  beta_obs       = 0.35  +/- 0.14 deg    Minami & Komatsu (2020), Planck 2018
  beta_ECF       = 0.350 +/- 0.04 deg    ECF theory, propagated from F_ion
  sigma_LiteBIRD = 0.10  deg             LiteBIRD (PTEP 2023) forecast, F1 Section 7

Output
------
  FigureBirefringencePrediction.png  (300 dpi)
  Filename consistent with LaTeX reference in F1 Extended v2.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# ---------------------------------------------------------------------------
# Parameters  --  all values anchored to F1 Extended v2
# ---------------------------------------------------------------------------
BETA_OBS       = 0.35    # Minami & Komatsu (2020), Planck 2018 [deg]
SIGMA_OBS      = 0.14    # Planck 2018 polarisation 1-sigma uncertainty [deg]

BETA_ECF       = 0.350   # ECF prediction = g_CS_eff * I [deg]
SIGMA_ECF      = 0.04    # Propagated from F_ion = 1.2765 uncertainty [deg]

SIGMA_LITEBIRD = 0.10    # LiteBIRD (PTEP 2023) forecasted 1-sigma precision [deg]
                         # F1 Section 7: "testable at the 0.1 deg level by LiteBIRD"

OUTPUT_FILE    = 'Figure_Birefringence_Prediction.png'


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 11})

beta         = np.linspace(-0.35, 0.85, 2000)
pdf_planck   = norm.pdf(beta, BETA_OBS,  SIGMA_OBS)
pdf_ecf      = norm.pdf(beta, BETA_ECF,  SIGMA_ECF)
pdf_litebird = norm.pdf(beta, BETA_ECF,  SIGMA_LITEBIRD)
Y_MAX        = max(pdf_ecf) * 1.28


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.subplots_adjust(left=0.10, right=0.97, bottom=0.13, top=0.87)

ax.fill_between(beta, pdf_planck,   0, color='gray',    alpha=0.12)
ax.fill_between(beta, pdf_ecf,      0, color='#C00000', alpha=0.10)
ax.fill_between(beta, pdf_litebird, 0, color='#DAA520', alpha=0.18)

ax.plot(beta, pdf_planck,   color='#333333', linestyle='-',  linewidth=2,
        label=r'Planck 2018 (Minami & Komatsu): $\beta = 0.35 \pm 0.14°$')
ax.plot(beta, pdf_ecf,      color='#C00000', linewidth=2.5,
        label=r'ECF prediction:  $\beta_{\rm ECF} = 0.35 \pm 0.04°$')
ax.plot(beta, pdf_litebird, color='#9A6800', linewidth=2.5, linestyle='--',
        label=r'LiteBIRD forecast:  $\sigma_\beta \approx 0.10°$  (PTEP 2023)')
ax.axvline(0, color='steelblue', linestyle=':', linewidth=1.8,
           label=r'$\Lambda$CDM null ($\beta = 0$)')

ax.text(BETA_ECF + 0.025, max(pdf_ecf) * 0.97,
        r'$\beta_{\rm ECF} = 0.35°$',
        color='#900000', fontweight='bold', fontsize=10, va='top')

snr   = BETA_ECF / SIGMA_LITEBIRD
y_ann = max(pdf_litebird) * 0.42
ax.annotate('', xy=(0.0, y_ann), xytext=(BETA_ECF, y_ann),
            arrowprops=dict(arrowstyle='<->', color='steelblue', lw=1.4))
ax.text(BETA_ECF / 2, y_ann + 0.12, rf'${snr:.1f}\sigma$',
        ha='center', color='steelblue', fontsize=10, fontweight='bold')
ax.text(BETA_ECF / 2, y_ann - 0.28,
        r'with LiteBIRD $\sigma_\beta=0.10°$',
        ha='center', color='steelblue', fontsize=8.5, style='italic')

ax.set_xlim(-0.35, 0.85)
ax.set_ylim(0, Y_MAX)
ax.set_xlabel(r'Birefringence angle $\beta$  [degrees]', fontsize=12)
ax.set_ylabel(r'Probability density  [deg$^{-1}$]',     fontsize=12)
ax.set_title('Cosmic Birefringence: ECF Prediction vs. Current & Future Constraints',
             fontsize=12, pad=10)
ax.legend(loc='upper right', fontsize=9.8, framealpha=0.92,
          edgecolor='#ccc', handlelength=2.2, labelspacing=0.6)
ax.grid(True, linestyle=':', alpha=0.35, color='gray')
ax.tick_params(labelsize=10)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()
