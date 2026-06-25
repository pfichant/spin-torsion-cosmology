import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la fonction de masse ECF
masses_solar = np.logspace(-7, 7, 500) # De 10^-7 à 10^7 Masses solaires
alpha = 1.9 # Indice de loi de puissance typique
M_max = 1e6 # Coupure exponentielle (Macro-Noeuds max)

# Fonction de masse (dn/dM)
dn_dM = (masses_solar**(-alpha)) * np.exp(-masses_solar / M_max)

# Visualisation professionnelle
plt.figure(figsize=(10, 6))
plt.plot(masses_solar, dn_dM, color='purple', lw=3, label="ECF Kibble-Zurek Mass Spectrum")

# Annotations pour les Micro et Macro Noeuds
plt.axvline(1e-6, color='blue', linestyle='--', label="Micro-Knots (GRB Progenitors)")
plt.text(1e-6 * 1.5, 1e10, "Halo Fluid\n(N ~ $10^{18}$)", color='blue', fontsize=11)

# Ajout du 'r' devant la chaîne pour le rendu LaTeX
plt.axvline(1e5, color='red', linestyle='--', label=r"Macro-Knots (~$10^5 M_\odot$)")
plt.text(1e5 * 1.5, 1e-6, "SMBH Seeds\n(N ~ 1)", color='red', fontsize=11)

# Formatage du graphe (Log-Log obligatoire en astro)
plt.xscale('log')
plt.yscale('log')

# Ajout du 'r' et traduction en anglais pour l'article
plt.xlabel(r"Topological Defect Mass ($M_\odot$)", fontsize=12, fontweight='bold')
plt.ylabel(r"Number Density $dn/dM$ (Arbitrary Units)", fontsize=12, fontweight='bold')
plt.title("ECF Knot Mass Spectrum (Kibble-Zurek Distribution)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()

plt.savefig("ECF_Mass_Spectrum.png", dpi=300)
# plt.show()