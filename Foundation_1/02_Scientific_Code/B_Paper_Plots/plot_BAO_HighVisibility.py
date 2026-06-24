"""
plot_BAO_HighVisibility_v2.py
Author: Pascal Fichant (2026)
Figure: BAO Hubble Diagram (figbao, Section 5)
Paper:  Foundation I – Unified Resolution of Cosmological Tensions

Physics:
    ECF preserves DM(z)/rs despite higher H0 via a proportionally reduced rs.
    The ratio DM/rs is the measured BAO observable, invariant under the
    joint recalibration (H0, rs) -> (73.04, 135.8).

Inputs (paper Table tabpriors + Table tabchi2breakdown):
    H0_PLANCK = 67.4   km/s/Mpc  (Planck 2018)
    RS_PLANCK = 147.1  Mpc       (Sec. 3, Tab. trilemma)
    H0_ECF    = 73.04  km/s/Mpc  (Sec. 5 best-fit)
    RS_ECF    = 135.8  Mpc       (Sec. 3 calibrated)
    OM0       = 0.315            (fixed, Table tabpriors)
    DH0       = 1.04   km/s/Mpc  (paper sigma(H0), Table tabpriors)

BAO data (all four points confirmed against primary sources):
    z=0.38, 0.51, 0.61 : BOSS DR12, Alam+2017
    z=1.48             : eBOSS DR16 QSO, Hou+2021 — corrected from 38.4 -> 30.85

V1 -> V2 fixes:
    [1] matplotlib.use('Agg') added — headless environment safety
    [2] plt.rcParams.update() moved before plt.figure()
    [3] DH0 band: +/-1.0 -> +/-1.04 km/s/Mpc (paper sigma(H0) = 1.04)
    [4] RS_PLANCK: 147.09 -> 147.1 Mpc (inter-script consistency)
    [5] plt.close() added after plt.savefig()
    [6] annotation string: mixed raw/non-raw -> single clean raw string
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- 1. PARAMETERS ---
H0_PLANCK = 67.4
RS_PLANCK = 147.1
H0_ECF    = 73.04
RS_ECF    = 135.8
OM0       = 0.315
C_LIGHT   = 299792.458
DH0       = 1.04   # 1-sigma H0 uncertainty (paper Table tabpriors)

plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

# --- 2. COSMOLOGICAL FUNCTIONS ---
def hubble_E(z):
    """E(z) = H(z)/H0 for flat LCDM late-time expansion."""
    return np.sqrt(OM0 * (1+z)**3 + (1 - OM0))

def get_DM_rs(z, h0, rs):
    """Transverse comoving distance / sound horizon: DM(z)/rs."""
    if z == 0:
        return 0.0
    integ, _ = quad(lambda zp: 1.0 / hubble_E(zp), 0, z)
    return (C_LIGHT / h0) * integ / rs

# --- 3. BAO OBSERVATIONAL DATA ---
# BOSS DR12 (Alam+2017): z = 0.38, 0.51, 0.61
# eBOSS DR16 QSO (Hou+2021): z = 1.48  [corrected from transcription error 38.4 -> 30.85]
bao_data = {
    'z':   np.array([0.38,  0.51,  0.61,  1.48]),
    'val': np.array([10.23, 13.36, 15.45, 30.85]),
    'err': np.array([0.17,  0.21,  0.22,  0.80])
}

# --- 4. MODEL CURVES ---
z_plot       = np.linspace(0.01, 1.7, 300)
y_planck     = [get_DM_rs(z, H0_PLANCK,      RS_PLANCK) for z in z_plot]
y_ecf        = [get_DM_rs(z, H0_ECF,         RS_ECF)    for z in z_plot]
y_ecf_upper  = [get_DM_rs(z, H0_ECF - DH0,   RS_ECF)    for z in z_plot]
y_ecf_lower  = [get_DM_rs(z, H0_ECF + DH0,   RS_ECF)    for z in z_plot]

# --- 5. PLOT ---
fig, ax = plt.subplots(figsize=(9, 5.5))
fig.subplots_adjust(top=0.88)

ax.fill_between(z_plot, y_ecf_lower, y_ecf_upper,
                color='crimson', alpha=0.15, zorder=1)

ax.plot(z_plot, y_planck, color='navy', ls='--', lw=2,  zorder=2,
        label=r'$\Lambda$CDM  ($H_0=67.4$, $r_s=147.1$ Mpc)')

ax.plot(z_plot, y_ecf,    color='crimson',  lw=2.5, zorder=3,
        label=r'ECF  ($H_0=73.04$, $r_s=135.8$ Mpc)')

ax.errorbar(bao_data['z'], bao_data['val'], yerr=bao_data['err'],
            fmt='ko', capsize=4, elinewidth=1.6, ms=5, zorder=4,
            label='BOSS DR12 + eBOSS DR16 QSO')

ax.set_xlim(0.1, 1.7)
ax.set_ylim(5, 35)
ax.set_xlabel(r'Redshift  $z$', fontsize=12)
ax.set_ylabel(r'$D_M(z) / r_s$', fontsize=12)
ax.set_title('BAO Geometric Consistency  (figbao)',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='lower right', framealpha=0.92)
ax.grid(True, ls=':', alpha=0.4)

plt.tight_layout()
plt.savefig('Figure_BAO_HighVisibility.png', dpi=300)
plt.close()
print('[SUCCESS] Saved: Figure_BAO_HighVisibility.png')
