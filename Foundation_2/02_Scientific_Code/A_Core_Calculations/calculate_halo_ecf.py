import numpy as np
# --- CONSTANTES PHYSIQUES ---
M_sun = 1.989e30        # Masse solaire en kg
kpc_to_m = 3.086e19     # 1 kpc en mètres
g_cm3_to_kg_m3 = 1000.0
# --- PARAMÈTRES ECF (issus de votre papier pour NGC 6503) ---
# Résultats de votre ajustement MCMC (Foundation II, Section 3.4)
log_rho0 = -23.25                      # Densité centrale (g/cm^3) / 1.0.7
rho0 = (10**log_rho0) * g_cm3_to_kg_m3 # Conversion en kg/m^3
Rs_kpc = 1.70                          # Rayon caractéristique (kpc) / 1.0.7
Rs = Rs_kpc * kpc_to_m                 # Conversion en mètres

# --- PARAMÈTRES DE L'ASTRE TOPOLOGIQUE ---
M_ecf = 1e24  # Masse typique d'un astre ECF en kg (Masse planétaire)

# --- MASSE BARYONIQUE OBSERVÉE ---
# La masse totale visible (gaz + étoiles) de NGC 6503 selon SPARC
M_baryon_Msun = 6.4e9                  # 6.4 milliards de masses solaires
M_baryon_kg = M_baryon_Msun * M_sun    # Conversion en kg

# --- FONCTION : MASSE DU HALO ECF ---
def masse_halo_ecf(rayon_kpc):
    """Calcule la masse du halo de matière noire (ECF) inclus dans un rayon donné."""
    r = rayon_kpc * kpc_to_m
    x = r / Rs
    # Intégrale d'un profil pseudo-isotherme (cœur régulier ECF)
    masse = 4 * np.pi * rho0 * (Rs**3) * (x - np.arctan(x))
    return masse

# --- CALCULS POUR LA GALAXIE (Jusqu'à 15 kpc, le bord du gaz visible) ---
r_visible = 15.0  
M_halo = masse_halo_ecf(r_visible)

# Calcul du nombre d'objets et du ratio
N_astres = M_halo / M_ecf
ratio_local = M_halo / M_baryon_kg

# --- AFFICHAGE DES RÉSULTATS ---
print("\n" + "="*60)
print(f"ANALYSE ECF DE LA GALAXIE NGC 6503 (à r = {r_visible} kpc)")
print("="*60)
print(f"Masse Baryonique (Visible) : {M_baryon_kg:.2e} kg  ({M_baryon_Msun:.2e} M_sun)")
print(f"Masse du Halo ECF (Sombre) : {M_halo:.2e} kg  ({M_halo/M_sun:.2e} M_sun)")
print("-" * 60)
print(f"RATIO LOCAL (Halo Sombre / Matière Visible) : {ratio_local:.1f}")
print(f"NOMBRE D'ASTRES ECF (de 10^24 kg)           : {N_astres:.2e} objets")
print(f"--> Soit environ {N_astres/1e17:.1f} centaines de millions de milliards d'astres !")
print("="*60 + "\n")
