"""
================================================================================
FIGURE BAO: GEOMETRIC CONSISTENCY CHECK
Foundation I: Unified Resolution of Cosmological Tensions
================================================================================
Description:
    Generates the plot comparing ECF and Planck LambdaCDM against BAO data.
    Demonstrates that ECF preserves the geometric ratio D_M(z)/r_s despite
    a higher H0, thanks to the reduced sound horizon r_s.

    UPDATED: 
    - Fixed Title rendering (removed LaTeX command).
    - Corrected eBOSS data point (30.85 instead of 38.4).
    - Aligned parameters with paper (135.8 Mpc).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- 1. PARAMÈTRES PHYSIQUES (Cohérence Papier) ---
# Lambda-CDM (Planck 2018)
H0_PLANCK = 67.4
RS_PLANCK = 147.09

# ECF Model (Foundation I - Optimized)
H0_ECF = 73.04        # SH0ES Target
RS_ECF = 135.8        # Calculated Geometric Match
OM0    = 0.315        # Matter Density (Fixed)
C_LIGHT = 299792.458

# --- 2. FONCTIONS COSMOLOGIQUES ---
def hubble_E(z):
    """Normalized Hubble Parameter E(z) = H(z)/H0 assuming Flat LCDM late-time expansion"""
    return np.sqrt(OM0 * (1+z)**3 + (1 - OM0))

def get_DM_rs(z, h0, rs):
    """
    Computes the observable ratio: Transverse Comoving Distance / Sound Horizon
    ratio = (c/H0 * integral(1/E(z))) / rs
    """
    if z == 0: return 0
    # Comoving distance integral
    integ, _ = quad(lambda zp: 1.0 / hubble_E(zp), 0, z)
    D_M = (C_LIGHT / h0) * integ
    return D_M / rs

# --- 3. DONNÉES OBSERVATIONNELLES (CORRIGÉES) ---
# Sources: BOSS DR12 & eBOSS DR16
# z: Redshift
# val: D_M(z) / r_s
# err: Error 1-sigma
bao_data = {
    'z':   np.array([0.38,  0.51,  0.61,  1.48]),
    'val': np.array([10.23, 13.36, 15.45, 30.85]), # CORRIGÉ (30.85 est la bonne valeur eBOSS)
    'err': np.array([0.17,  0.21,  0.22,  0.80])
}

# --- 4. GÉNÉRATION DES COURBES ---
z_plot = np.linspace(0.1, 1.7, 200)

# Courbe Planck (Bleu)
y_planck = [get_DM_rs(z, H0_PLANCK, RS_PLANCK) for z in z_plot]

# Courbe ECF (Rouge)
y_ecf = [get_DM_rs(z, H0_ECF, RS_ECF) for z in z_plot]

# Zone d'erreur visuelle pour ECF (~1% incertitude sur H0)
y_ecf_upper = [get_DM_rs(z, H0_ECF - 1.0, RS_ECF) for z in z_plot]
y_ecf_lower = [get_DM_rs(z, H0_ECF + 1.0, RS_ECF) for z in z_plot]

# --- 5. VISUALISATION ---
plt.figure(figsize=(10, 7))
# On utilise une police serif standard mais sans forcer le mode TeX complet pour éviter les bugs de titre
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

# A. Modèle Planck
plt.plot(z_plot, y_planck, color='navy', linestyle='--', linewidth=2.5, 
         label=rf'$\Lambda$CDM Planck ($H_0={H0_PLANCK}, r_s={RS_PLANCK:.1f}$)', zorder=2)

# B. Modèle ECF
plt.plot(z_plot, y_ecf, color='crimson', linestyle='-', linewidth=3, 
         label=rf'ECF Model ($H_0={H0_ECF}, r_s={RS_ECF:.1f}$)', zorder=3)

# C. Zone d'incertitude ECF
plt.fill_between(z_plot, y_ecf_lower, y_ecf_upper, color='crimson', alpha=0.15, 
                 label=r'ECF $H_0 \pm 1$ km/s/Mpc')

# D. Points de Données BAO
plt.errorbar(bao_data['z'], bao_data['val'], yerr=bao_data['err'], 
             fmt='o', color='black', ecolor='black', capsize=5, elinewidth=2, markeredgewidth=2,
             label='BOSS/eBOSS Data ($D_M/r_s$)', zorder=4)

# Esthétique
# CORRECTION DU TITRE : Utilisation de fontweight='bold' au lieu de \textbf{}
plt.title('Geometric Consistency: BAO Hubble Diagram', fontsize=16, fontweight='bold', pad=15)
plt.xlabel(r'Redshift $z$', fontsize=14)
plt.ylabel(r'$D_M(z) / r_s$', fontsize=14)
plt.legend(fontsize=11, loc='upper left', frameon=True, framealpha=0.9)
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlim(0.1, 1.7)
plt.ylim(5, 35)

# Annotation explicative
plt.text(1.0, 15, 
         r"ECF matches BAO data" "\n" r"with $H_0 \approx 73$ due to" "\n" r"smaller $r_s$ ($135.8$ Mpc)", 
         fontsize=11, color='darkred', 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

plt.tight_layout()
plt.savefig('Figure_BAO_HighVisibility.png', dpi=300)
# plt.show()