"""
Script: Birefringence Prediction (Figure 6)
Paper: Foundation I
Author: Pascal Fichant
Date: 01/02/2026
Description: 
    Updated to align with the text value beta = 0.35 deg.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib

# Configuration Backend
matplotlib.use('Agg')
plt.rcParams.update({'font.size': 12, 'axes.labelsize': 14, 'figure.figsize': (10, 6), 'font.family': 'serif'})

def plot_birefringence_future():
    print(">>> Generating Figure 6: Birefringence Prediction...")
    
    # Axe X : Angle beta
    beta = np.linspace(-0.2, 0.8, 1000)
    
    # --- 1. PLANCK (Observation Minami & Komatsu 2020) ---
    mu_obs = 0.35
    sigma_obs = 0.14
    pdf_obs = norm.pdf(beta, mu_obs, sigma_obs)
    
    # --- 2. ECF PREDICTION (Votre Modèle) ---
    # MISE A JOUR : Alignement avec le texte et F_ION = 1.2765
    mu_ecf = 0.350  # <--- CORRECTION (était 0.342)
    sigma_ecf = 0.04 
    pdf_ecf = norm.pdf(beta, mu_ecf, sigma_ecf)

    # --- 3. LITEBIRD FORECAST (Futur) ---
    sigma_litebird = 0.02 
    pdf_litebird = norm.pdf(beta, mu_ecf, sigma_litebird)

    fig, ax = plt.subplots()

    # Planck (Gris)
    ax.plot(beta, pdf_obs, color='black', linestyle=':', linewidth=2, label='Planck 2018 (Minami & Komatsu)')
    ax.fill_between(beta, pdf_obs, 0, color='gray', alpha=0.1)

    # ECF Theory (Rouge)
    ax.plot(beta, pdf_ecf, color='#D00000', linewidth=3, label='ECF Prediction (Theory)')
    
    # Annotation de la valeur exacte
    ax.text(mu_ecf, max(pdf_ecf) + 0.5, rf'$\beta \approx {mu_ecf:.2f}^\circ$', 
            color='#D00000', ha='center', fontweight='bold')
    
    # LiteBIRD (Or)
    ax.plot(beta, pdf_litebird, color='#DAA520', linewidth=2.5, linestyle='-', label='Future: LiteBIRD Target')
    ax.fill_between(beta, pdf_litebird, 0, color='#DAA520', alpha=0.3)

    # Ligne Zéro (LCDM)
    ax.axvline(0, color='blue', linestyle='--', label=r'$\Lambda$CDM ($\beta=0$)')

    # Annotation LiteBIRD
    ax.annotate(r'$\mathbf{LiteBIRD}$ will distinguish' + '\n' + r'Signal from Noise ($>5\sigma$)', 
                xy=(0.35, 15), xycoords='data',
                xytext=(0.55, 15), textcoords='data',
                arrowprops=dict(facecolor='#DAA520', arrowstyle='->'),
                color='#B8860B', fontsize=11, fontweight='bold')

    # Mise en page
    ax.set_xlim(-0.2, 0.8)
    ax.set_ylim(0, 22) 
    
    ax.set_xlabel(r'Birefringence Angle $\beta$ (degrees)')
    ax.set_ylabel('Probability Density')
    ax.set_title(r'Cosmic Birefringence Prediction', fontsize=14, pad=15, fontweight='bold')
    
    ax.legend(loc='upper right')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig("Figure_Birefringence_Prediction.png", dpi=300)
    print("   [SUCCESS] Saved: Figure_Birefringence_Prediction.png")
    plt.close()

if __name__ == "__main__":
    plot_birefringence_future()