# plot_Fig_k3_Residuals_Angles.py
# Script pour la Figure K3 (Résidus et Prédictions)
# 1.0.5 28/01/26
import numpy as np
import matplotlib.pyplot as plt

# --- 1. MODÉLISATION PHYSIQUE (Indispensable pour générer les courbes) ---
def generate_spectrum_model(model_type='LCDM'):
    # Génération étendue jusqu'à l=3500 pour bien voir la chute
    ell = np.linspace(2, 3500, 1000)
    l_peak = 220 
    
    if model_type == 'LCDM':
        damping_scale = 1400
        amplitude_scale = 1.0
        phase_shift = 0.0
    else: # ECF Model (Einstein-Cartan-Fermions)
        # La torsion augmente l'amortissement (Silk Damping)
        damping_scale = 1320 
        amplitude_scale = 1.0 
        phase_shift = 0.0 

    oscillations = np.cos(np.pi * (ell) / l_peak + phase_shift)**2
    
    # Formule phénoménologique du spectre de puissance Dl
    Dl = 5000 * (ell/100)**(-0.6) * np.exp(-ell/damping_scale) * oscillations * amplitude_scale + 50
    # Correction plateau Sachs-Wolfe à bas l
    Dl[ell < 30] = 1000 * (ell[ell<30]/10)**(-1.5)
    
    return ell, Dl

# --- 2. GÉNÉRATION DES DONNÉES ---
l_lcdm, dl_lcdm = generate_spectrum_model('LCDM')
l_ecf, dl_ecf = generate_spectrum_model('ECF')

# Fonctions de conversion Multipole <-> Angle
def l2theta(l): return 180.0/(l+1e-10)
def theta2l(t): return 180.0/(t+1e-10)

# --- 3. GRAPHIQUE AVEC RÉSIDUS (FIGURE K3) ---
fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
mask = l_lcdm > 1200

# Panel du Haut : Comparaison des modèles
ax3.plot(l_lcdm[mask], dl_lcdm[mask], label=r'$\Lambda$CDM Baseline', color='blue', linestyle='--', linewidth=2)
ax3.plot(l_lcdm[mask], dl_ecf[mask], label=r'ECF Prediction', color='red', linewidth=2)
ax3.axvspan(2200, 3000, color='gold', alpha=0.3, label='CMB-S4 Discrimination Zone')

ax3.set_ylabel(r'$\mathcal{D}_\ell^{TT} [\mu K^2]$', fontsize=12)
ax3.set_title(r'Power Spectrum Divergence & Residuals', fontsize=14)
ax3.legend(fontsize=11)
ax3.grid(True, linestyle=':', alpha=0.6)
ax3.set_ylim(0, 1000)

# Axe secondaire en degrés (en haut)
secax3 = ax3.secondary_xaxis('top', functions=(l2theta, theta2l))
secax3.set_xlabel('Angular Scale [degrees]', fontsize=12)
secax3.set_xticks([0.15, 0.1, 0.08, 0.06])
secax3.set_xticklabels(['0.15°', '0.10°', '0.08°', '0.06°'])

# Panel du Bas : Résidus (Différence ECF - LCDM)
residuals = dl_ecf - dl_lcdm
ax4.plot(l_lcdm[mask], residuals[mask], color='black', linewidth=1.5)
ax4.fill_between(l_lcdm[mask], residuals[mask], 0, where=(residuals[mask]<0), color='red', alpha=0.3)
ax4.axhline(0, color='blue', linestyle='--')

# Zone de sensibilité CMB-S4 (Bande verte)
ax4.fill_between(l_lcdm[mask], -1, 1, color='green', alpha=0.2, label=r'CMB-S4 Sensitivity ($\pm 1 \sigma$)')

ax4.set_ylabel(r'$\Delta \mathcal{D}_\ell$ (ECF - $\Lambda$CDM)', fontsize=10)
ax4.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
ax4.legend(loc='lower left', fontsize=9)
ax4.grid(True, linestyle=':', alpha=0.6)
ax4.set_ylim(-15, 5)

plt.tight_layout()
plt.subplots_adjust(hspace=0.05)
plt.savefig('Figure_K3_Residuals_Angles.png', dpi=300)
# plt.show()