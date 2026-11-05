"""
plot_BAO_HighVisibility_v2.py
Author: Pascal Fichant (2026)
Figure: BAO Hubble Diagram (figbao, Section 5)
Paper:  Foundation I

Physics:
    ECF preserves DM(z)/rs despite higher H0 via a proportionally reduced rs.
    The ratio DM/rs is the measured BAO observable, invariant under the
    joint recalibration (H0, rs) -> (73.04, 135.65).

Inputs (paper Table tabpriors + Table tabchi2breakdown):
    H0_PLANCK = 67.4   km/s/Mpc  (Planck 2018)
    RS_PLANCK = 147.1  Mpc       (Sec. 3, Tab. trilemma)
    H0_ECF    = 73.04  km/s/Mpc  (Sec. 5 best-fit)
    RS_ECF    = 135.65 Mpc       (Sec. 3 calibrated; A-6)
    OM0       = 0.315            (LCDM curve only; ECF uses omega_m/h^2 = 0.2669, A-7)
    DH0       = 1.04   km/s/Mpc  (paper sigma(H0), Table tabpriors)

BAO data (z = 1.48 traced to its primary source; z = 0.38, 0.51, 0.61 = Alam+2017
consensus D_M*(r_d,fid/r_d) = 1512.39 / 1975.22 / 2306.68 Mpc divided by r_d,fid = 147.78,
as quoted by two secondary sources (Khadka & Ratra 2021 Tab. 1; A&A 2022 aa41204-21 Tab. 5,
D_V cross-check); primary table not read line by line (to be confirmed); errors 0.17/0.21/0.22
not re-verified (to be confirmed). Until 04/10/2026 the script carried 15.45 at z = 0.61
(implied r_d = 149.3 Mpc, inconsistent with the two other bins) and 13.36 at z = 0.51.
Any chi^2 built on these four points is a DIAGONAL, INDICATIVE comparison -- no covariance):
    z=0.38, 0.51, 0.61 : BOSS DR12, Alam+2017
    z=1.48             : eBOSS DR16 QSO consensus, Hou+2021 : 30.21 +/- 0.79
                         (38.4 +/- 1.1 and 30.85 +/- 0.80 : untraced, WITHDRAWN)

V1 -> V2 fixes:
    [1] matplotlib.use('Agg') added — headless environment safety
    [2] plt.rcParams.update() moved before plt.figure()
    [3] DH0 band: +/-1.0 -> +/-1.04 km/s/Mpc (paper sigma(H0) = 1.04)
    [4] RS_PLANCK: 147.09 -> 147.1 Mpc (inter-script consistency)
    [5] plt.close() added after plt.savefig()
    [6] annotation string: mixed raw/non-raw -> single clean raw string
"""
# Last modified: 21/08/2026, 16:05 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
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
from scipy.integrate import quad

# --- 1. PARAMETERS ---
H0_PLANCK = 67.4
RS_PLANCK = 147.1
H0_ECF    = 73.04
RS_ECF    = 135.65   # [A-6] was 135.8
OM0       = 0.315            # Planck (LCDM curve)
OM_ECF    = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
C_LIGHT   = 299792.458
DH0       = 1.04   # 1-sigma H0 uncertainty (paper Table tabpriors)

plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

# --- 2. COSMOLOGICAL FUNCTIONS ---
def hubble_E(z, om=OM0):
    """E(z) = H(z)/H0 for flat LCDM late-time expansion."""
    return np.sqrt(om * (1+z)**3 + (1 - om))

def get_DM_rs(z, h0, rs):
    """Transverse comoving distance / sound horizon: DM(z)/rs.
    [A-7] Omega_m = omega_m/h^2 : Planck value for H0=67.4, ECF value otherwise."""
    if z == 0:
        return 0.0
    om = OM0 if abs(h0-67.4) < 1e-9 else OM_ECF
    integ, _ = quad(lambda zp: 1.0 / hubble_E(zp, om), 0, z)
    return (C_LIGHT / h0) * integ / rs

# --- 3. BAO OBSERVATIONAL DATA ---
# BOSS DR12 (Alam+2017): z = 0.38, 0.51, 0.61
# eBOSS DR16 QSO (Hou+2021), consensus: z = 1.48, D_M/r_d = 30.21 +/- 0.79 (30.22 used 22/09-12/10/2026 by mistake)
# [P3/Q1, 22/09/2026] 30.85 +/- 0.80 withdrawn: no retrievable source.
bao_data = {
    'z':   np.array([0.38,  0.51,  0.61,  1.48]),
    'val': np.array([10.23, 13.37, 15.61, 30.21]),   # [04/10/2026, decision 7-compl] z=0.51: 13.36 -> 13.37 (1975.22/147.78); z=0.61: 15.45 -> 15.61 (2306.68/147.78, Alam+2017 consensus, r_d,fid = 147.78 Mpc)
    'err': np.array([0.166, 0.206, 0.251, 0.79])   # [05/10/2026, ALAM-ERR] BOSS DR12: stat (+) syst, Alam+2017 Table 7 / 147.78 (was 0.17, 0.21, 0.22 = stat only at z=0.61)
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

ax.plot(z_plot, y_planck, color='navy', ls='-', lw=3.0,  zorder=2,
        label=r'$\Lambda$CDM  ($H_0=67.4$, $r_s=147.1$ Mpc)')

# 17/08/2026 audit: the LCDM curve was fully hidden under the ECF one, so the
# legend announced a curve the reader could not see. The coincidence of the two
# D_M/r_s ratios IS the point of this figure, so ECF is now drawn as a dashed
# overlay on top of the solid LCDM line: both remain visible where they agree.
ax.plot(z_plot, y_ecf,    color='crimson',  lw=2.5, ls=(0, (6, 4)), zorder=3,
        label=r'ECF  ($H_0=73.04$, $r_s=135.65$ Mpc, $\Omega_m=0.267$)')

ax.errorbar(bao_data['z'], bao_data['val'], yerr=bao_data['err'],
            fmt='ko', capsize=4, elinewidth=1.6, ms=5, zorder=4,
            label='BOSS DR12 + eBOSS DR16 QSO')

ax.set_xlim(0.1, 1.7)
ax.set_ylim(5, 35)
ax.set_xlabel(r'Redshift  $z$', fontsize=12)
ax.set_ylabel(r'$D_M(z) / r_s$', fontsize=12)
# 17/08/2026 audit: the title read "BAO Geometric Consistency (figbao)" —
# "figbao" is the LaTeX label of the figure, which had leaked onto the image
# and is visible in the published PDF (Fig. 5).
ax.set_title('BAO Geometric Consistency',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='lower right', framealpha=0.92)
ax.grid(True, ls=':', alpha=0.4)

plt.tight_layout()
plt.savefig('Figure_BAO_HighVisibility.png', dpi=300)
plt.close()
print('[SUCCESS] Saved: Figure_BAO_HighVisibility.png')
