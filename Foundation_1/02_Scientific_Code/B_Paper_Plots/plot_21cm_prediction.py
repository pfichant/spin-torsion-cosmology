# plot_21cm_prediction.py
# Author: Pascal Fichant (2026)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Configuration pour éviter les erreurs d'affichage
import matplotlib
matplotlib.use('Agg')

"""
Script: 21cm Prediction (Figure 8)
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant
Date: 01/02/2026
Description: 
    Updates the 21cm prediction plot with the correct Delta r_s value (-11.4 Mpc)
    derived from the numerical validation log.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib

# Configuration Backend (Headless)
matplotlib.use('Agg')

# Style Global
plt.rcParams.update({
    'font.size': 12, 
    'axes.labelsize': 14, 
    'figure.figsize': (10, 6),
    'font.family': 'serif'
})

def plot_21cm_prediction():
    print(">>> Generating Figure 8: 21cm Prediction...")
    
    # Axe X : Horizon sonore comobile rs
    x = np.linspace(130, 155, 1000)
    
    # --- 1. MODÈLE ECF (Spin-Torsion) ---
    # Valeur validée par votre log : 135.8 Mpc
    mu_ecf = 135.8  
    sigma_ecf = 1.5
    pdf_ecf = norm.pdf(x, mu_ecf, sigma_ecf)
    
    # --- 2. PLANCK ΛCDM (Référence) ---
    # Valeur standard : 147.2 Mpc
    mu_planck = 147.2
    sigma_planck = 0.3
    pdf_planck = norm.pdf(x, mu_planck, sigma_planck)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Trace ECF (Rouge)
    ax.plot(x, pdf_ecf, color='#D00000', linewidth=3, label='ECF Prediction (Spin-Torsion)')
    ax.fill_between(x, pdf_ecf, 0, color='#D00000', alpha=0.2)
    # Label ECF
    ax.text(mu_ecf, max(pdf_ecf) + 0.05, f'{mu_ecf:.1f} Mpc', 
            ha='center', color='#D00000', fontweight='bold')

    # Trace Planck (Bleu)
    ax.plot(x, pdf_planck, color='blue', linestyle='--', linewidth=2, label=r'Planck $\Lambda$CDM')
    ax.fill_between(x, pdf_planck, 0, color='blue', alpha=0.1)
    # Label Planck
    ax.text(mu_planck, max(pdf_planck) + 0.05, f'{mu_planck:.1f} Mpc', 
            ha='center', color='blue')

    # --- TENSION VISUALIZATION ---
    arrow_y = 0.15
    # Flèche double
    ax.annotate('', xy=(mu_ecf, arrow_y), xytext=(mu_planck, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    
    # Calcul dynamique du Delta
    delta_rs = mu_ecf - mu_planck # 135.8 - 147.2 = -11.4
    mid_point = (mu_ecf + mu_planck) / 2
    
    # Texte Delta (Fond blanc pour lisibilité)
    ax.text(mid_point, arrow_y + 0.02, rf'$\Delta r_s \approx {delta_rs:.1f}$ Mpc', 
            ha='center', fontsize=12, fontweight='bold', backgroundcolor='white')
    
    # Boîte "STRONG TENSION"
    ax.text(mid_point, arrow_y - 0.08, r'STRONG TENSION (> 5$\sigma$)', ha='center', 
            color='#800000', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#800000", lw=2))

    # Mise en page
    ax.set_xlim(129, 156)
    ax.set_ylim(0, 1.6) 
    ax.set_xlabel(r'Comoving Sound Horizon $r_s$ [Mpc]')
    ax.set_ylabel('Probability Density')
    ax.set_title(r'21cm Forecast - Sound Horizon Shift', fontsize=14, pad=15, fontweight='bold')
    
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Sauvegarde
    output_filename = "Figure_21cm_ECF_Prediction.png"
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"   [SUCCESS] Saved: {output_filename}")
    plt.close()

if __name__ == "__main__":
    plot_21cm_prediction()
    