import numpy as np
import matplotlib.pyplot as plt

# ECF mass-function parameters
masses_solar = np.logspace(-7, 7, 500) # De 10^-7 à 10^7 Masses solaires
# [27/08/2026] alpha was 1.9, described as a 'typical' power-law index.
# Foundation II states alpha = 5/2, fixed by the Kibble-Zurek universality
# class for a U(1) vector defect in 3+1 dimensions, and explicitly NOT a
# free fit parameter. A figure that plots a different exponent than the one
# the paper declares non-adjustable contradicts the paper.
alpha = 2.5 # KZ universality class (U(1) vector defect, 3+1 D) -- not fitted
M_max = 1e6 # Coupure exponentielle (Macro-Noeuds max)

# Fonction de masse (dn/dM)
# [CORRIGE 16/09/2026 — C-P0-06] alpha est l'indice SPECTRAL (5/2), pas
# l'exposant de dn/dM. Foundation II ecrit : « alpha = 5/2 => dn/dM ~ M^(-7/2) »,
# et compute_poisson_isocurvature.py integre bien les moments de M^(-7/2).
# Ce script appliquait alpha directement a dn/dM, soit M^(-5/2) : une pente
# differente d'une unite, sur la seule figure du spectre de masse.
dn_dM = (masses_solar**(-(alpha + 1.0))) * np.exp(-masses_solar / M_max)

# Visualisation professionnelle
plt.figure(figsize=(10, 6))
plt.plot(masses_solar, dn_dM, color='purple', lw=3, label="ECF Kibble-Zurek Mass Spectrum")

# Annotations for the Micro- and Macro-Knots
# [27/08/2026] Was 1e-6 Msun. The Micro-Knot mass is the electroweak horizon
# mass, 3.74e24 kg = 1.88e-6 Msun (calculate_microknot_mass.py).
M_MICRO_MSUN = 3.74e24 / 1.98892e30
plt.axvline(M_MICRO_MSUN, color='blue', linestyle='--',
            label="Micro-Knots (EW horizon mass)")
plt.text(M_MICRO_MSUN * 1.5, 1e10, "Halo Fluid\n(N ~ $10^{18}$)", color='blue', fontsize=11)

# Raw string ('r' prefix) for correct LaTeX rendering
plt.axvline(1e5, color='red', linestyle='--', label=r"Macro-Knots (~$10^5 M_\odot$)")
plt.text(1e5 * 1.5, 1e-6, "SMBH Seeds\n(N ~ 1)", color='red', fontsize=11)

# Formatage du graphe (Log-Log obligatoire en astro)
plt.xscale('log')
plt.yscale('log')

# Raw string ('r' prefix), and English wording for the paper
plt.xlabel(r"Topological Defect Mass ($M_\odot$)", fontsize=12, fontweight='bold')
plt.ylabel(r"Number Density $dn/dM$ (Arbitrary Units)", fontsize=12, fontweight='bold')
plt.title("ECF Knot Mass Spectrum (Kibble-Zurek Distribution)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()

plt.savefig("ECF_Mass_Spectrum.png", dpi=300)
# plt.show()