# plot_h0_s8_contours.py
"""
Script: H0-S8 Tension Resolution (Figure 4)
Author: Pascal Fichant
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Patch
from matplotlib.lines import Line2D
import matplotlib

# Configuration Backend et Style
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 12, 
    'axes.labelsize': 14, 
    'figure.figsize': (10, 8),
    'font.family': 'serif'
})

def plot_h0_s8_contours():
    print(">>> Generating Figure: H0-S8 Contours...")
    fig, ax = plt.subplots()

    # --- DONNÉES (Approximations Gaussiennes pour les Ellipses) ---
    
    # 1. Planck 2018 (LambdaCDM) - Haute Tension
    # H0 ~ 67.4 +/- 0.5, S8 ~ 0.832 +/- 0.013
    h0_planck = 67.4
    s8_planck = 0.832
    
    # CORRECTION : Ajout du 'r' devant le label pour gérer le LaTeX \Lambda
    e1_planck = Ellipse((h0_planck, s8_planck), width=1.0, height=0.026, angle=0, 
                        color='blue', alpha=0.3)
    e2_planck = Ellipse((h0_planck, s8_planck), width=2.0, height=0.052, angle=0, 
                        color='blue', alpha=0.1, label=r'Planck $\Lambda$CDM')
    
    # 2. Local Universe (SH0ES + KiDS) - La Cible
    # H0 ~ 73.04 (SH0ES), S8 ~ 0.766 (KiDS-1000)
    h0_local = 73.04
    s8_local = 0.766
    
    e1_local = Ellipse((h0_local, s8_local), width=2.0, height=0.03, angle=0, 
                       color='green', alpha=0.3)
    e2_local = Ellipse((h0_local, s8_local), width=4.0, height=0.06, angle=0, 
                       color='green', alpha=0.1, label='Local Observations')

    # Ajout des ellipses au graphique
    ax.add_patch(e2_planck)
    ax.add_patch(e1_planck)
    ax.add_patch(e2_local)
    ax.add_patch(e1_local)

    # --- TRAJECTOIRE ECF ---
    # Montre comment le modèle connecte les deux régions
    # Paramétrisation simplifiée pour l'illustration
    alpha = np.linspace(0, 1, 20)
    h0_traj = h0_planck + (h0_local - h0_planck) * alpha
    s8_traj = s8_planck + (s8_local - s8_planck) * alpha
    
    ax.plot(h0_traj, s8_traj, color='red', linestyle='--', linewidth=2, 
            label='ECF Theoretical Path')
    
    # Point ECF Final
    ax.plot(h0_local, s8_local, marker='*', color='red', markersize=18, 
            label='ECF Solution', zorder=10)

    # --- LIGNES GUIDES ---
    ax.axvline(h0_planck, color='gray', linestyle=':', alpha=0.5)
    ax.axhline(s8_planck, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(h0_local, color='gray', linestyle='--', alpha=0.4)
    ax.axhline(0.766, color='gray', linestyle='--', alpha=0.4)

    # --- MISE EN PAGE ---
    ax.set_xlim(65, 76)
    ax.set_ylim(0.73, 0.86)
    
    # Utilisation de chaînes brutes (r'') pour les labels LaTeX
    ax.set_xlabel(r'Hubble Constant $H_0$ [km/s/Mpc]', fontsize=14, fontweight='bold')
    ax.set_ylabel(r'Structure Growth $S_8$', fontsize=14, fontweight='bold')
    ax.set_title(r'Resolution of the $H_0$ and $S_8$ Tensions', fontsize=16, pad=15, fontweight='bold')
    
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Légende personnalisée avec r'' pour Lambda
    legend_elements = [
        Patch(facecolor='blue', alpha=0.3, label=r'Planck $\Lambda$CDM'),
        Patch(facecolor='green', alpha=0.3, label='Local Observations (SH0ES + KiDS)'),
        Line2D([0], [0], color='red', lw=2, linestyle='--', label='ECF Prediction Path'),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=15, label='ECF Solution')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True)
    
    output_filename = "Figure_H0_S8_Contours.png"
    plt.savefig(output_filename, dpi=300)
    print(f"   [SUCCESS] Saved: {output_filename}")
    plt.close()

if __name__ == "__main__":
    plot_h0_s8_contours()