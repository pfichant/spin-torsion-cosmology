import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib

# Configuration Backend
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})

def plot_euclid_prediction():
    print("Génération des données...")
    # --- 1. MODÉLISATION PHYSIQUE ---
    k = np.logspace(-2.5, 0.5, 500)
    
    # Forme approximative du Spectre P(k) standard
    q = k / (0.315 * 0.67) 
    T_k = np.log(1 + 2.34*q) / (2.34*q) * (1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
    ns = 0.965
    Pk_LCDM = k**ns * T_k**2 * 10000 

    # Modèle ECF
    suppression_factor = 1.0 - 0.15 * (k**2 / (k**2 + 0.1**2)) 
    Pk_ECF = Pk_LCDM * suppression_factor

    # --- 2. SIMULATION EUCLID DATA ---
    k_euclid = np.logspace(-1.5, 0.3, 15) 
    Pk_theory_at_data = np.interp(k_euclid, k, Pk_ECF)
    
    np.random.seed(42)
    noise = np.random.normal(0, 0.02 * Pk_theory_at_data) 
    Pk_data = Pk_theory_at_data + noise
    yerr = 0.03 * Pk_data 

    # --- 3. CRÉATION FIGURE ---
    print("Création de la figure...")
    fig = plt.figure(figsize=(10, 8))
    
    # Marges manuelles (Anti-Crash)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.10, hspace=0.1)
    
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

    # PANEL HAUT : P(k)
    ax1 = plt.subplot(gs[0])
    
    ax1.loglog(k, Pk_LCDM, 'b--', linewidth=2, label=r'$\Lambda$CDM ($S_8=0.832$)')
    ax1.loglog(k, Pk_ECF, 'r-', linewidth=3, label=r'ECF Torsion ($S_8=0.766$)')
    
    ax1.errorbar(k_euclid, Pk_data, yerr=yerr, fmt='o', color='black', 
                 ecolor='gray', elinewidth=1.5, capsize=3, markersize=5, 
                 label='Euclid Forecast')

    # --- CORRECTION DU TEXTE ROUGE ---
    # On enlève le \textbf{} qui causait l'affichage parasite
    ax1.text(0.1, 200, 'Structure Suppression', color='#c0392b', fontsize=12, fontweight='bold')
    
    ax1.set_ylabel(r'$P(k)$ [$h^{-3}$ Mpc$^3$]', fontweight='bold')
    ax1.set_xlim(0.005, 2)
    ax1.set_ylim(10, 3e4)
    ax1.grid(True, which='both', linestyle=':', alpha=0.4)
    ax1.legend(loc='lower left', frameon=True)
    ax1.set_xticklabels([]) 
    ax1.set_title(r'Galaxy Power Spectrum Prediction: $S_8$ Resolution', fontsize=16, fontweight='bold', pad=10)

    # PANEL BAS : RATIO
    ax2 = plt.subplot(gs[1])
    
    ratio_theory = Pk_ECF / Pk_LCDM
    ratio_data = Pk_data / np.interp(k_euclid, k, Pk_LCDM)
    ratio_err = yerr / np.interp(k_euclid, k, Pk_LCDM)

    ax2.semilogx(k, ratio_theory, 'r-', linewidth=2)
    ax2.axhline(1, color='b', linestyle='--', linewidth=1.5) 
    
    ax2.errorbar(k_euclid, ratio_data, yerr=ratio_err, fmt='o', color='black', 
                 ecolor='gray', elinewidth=1.5, capsize=3, markersize=4)

    # Zone de discrimination
    ax2.fill_between(k, 0.8, 0.9, color='green', alpha=0.1)
    
    ax2.set_xlabel(r'Wavenumber $k$ [$h$ Mpc$^{-1}$]', fontweight='bold')
    ax2.set_ylabel(r'$P_{ECF}/P_{\Lambda}$', fontweight='bold', fontsize=12)
    ax2.set_xlim(0.005, 2)
    ax2.set_ylim(0.75, 1.1)
    ax2.grid(True, which='both', linestyle=':', alpha=0.4)

    # Sauvegarde
    filename = 'Figure_Euclid_Pk_S8.png'
    print(f"Sauvegarde dans {filename}...")
    plt.savefig(filename, dpi=300) 
    print("Image finale générée (Texte corrigé).")

if __name__ == "__main__":
    plot_euclid_prediction()