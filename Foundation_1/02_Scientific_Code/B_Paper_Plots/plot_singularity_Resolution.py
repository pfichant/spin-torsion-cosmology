# plot_singularity_resolution.py
# Script ECF : Baseline Einstein-Cartan Unifiée
# Author: Pascal Fichant (2026)
# Creation: 11Jan2026
import numpy as np
import matplotlib.pyplot as plt

def plot_singularity_resolution():
    try:
        # Rayon approchant le centre (r -> 0)
        r = np.linspace(0.01, 2.0, 500)
        
        # Modele RG : Singularite en 1/r^2
        density_gr = 1 / (r**2)
        
        # Modele ECF : Torsion repulsive qui sature a la densite de Cartan
        rho_cartan = 50 
        density_ECF = 1 / (r**2 + (1/rho_cartan))
        
        plt.figure(figsize=(10, 6))
        
        # Courbe RG
        plt.plot(r, density_gr, 'r--', label='General Relativity (Singularity: Information Loss)', linewidth=2)
        
        # Courbe ECF
        plt.plot(r, density_ECF, 'b-', label='Einstein-Cartan ECF (Torsion Core: Information Preserved)', linewidth=3)
        
        # Zone de Rebond
        plt.axhline(y=rho_cartan, color='green', linestyle=':', label='Cartan Density Limit rho_C')
        plt.fill_between(r, 0, density_ECF, color='blue', alpha=0.1)

        plt.ylim(0, 60)
        plt.xlim(0, 2)
        
        # Suppression des symboles $ problematiques pour le terminal
        plt.xlabel('Radius r or Scale Factor a')
        plt.ylabel('Energy Density rho')
        plt.title('Resolution of the Singularity and Information Preservation')
        
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Sauvegarde
        filename = "Figure_Singularity_Resolution.png"
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Success: {filename} has been generated.")
        
    except Exception as e:
        print(f"An error occurred:\n{e}")

if __name__ == "__main__":
    plot_singularity_resolution()