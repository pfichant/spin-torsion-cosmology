# Last modified: 02/09/2026, 11:10 (Paris time)
# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
# --- CONSTANTES PHYSIQUES ---
M_sun = 1.989e30        # Masse solaire en kg
kpc_to_m = 3.086e19     # 1 kpc en mètres
g_cm3_to_kg_m3 = 1000.0
# --- ECF PARAMETERS (from the paper, for NGC 6503) ---
# Best fit of the emcee chain on the 31 SPARC points (mcmc_ngc6503_sparc.py, 22/09/2026)
log_rho0 = -23.2517                    # Densité centrale (g/cm^3)
rho0 = (10**log_rho0) * g_cm3_to_kg_m3 # Conversion en kg/m^3
Rs_kpc = 1.7038                        # Rayon caractéristique (kpc)
Rs = Rs_kpc * kpc_to_m                 # Conversion en mètres

# [22/09/2026, N-5] Incertitude et covariance : covariance empirique de la
# chaine emcee sur SPARC reel (mcmc_ngc6503_sparc.py ; correlation -0.997).
# Les anciennes valeurs (0.05 / 0.04 / -0.01) venaient de plot_MCMC_NGC6503.py,
# dont les echantillons ne provenaient pas de la vraisemblance.
SIGMA_LOG_RHO0 = 0.04051   # dex
SIGMA_RS_KPC   = 0.09040   # kpc
COV_LOGRHO_RS  = -0.003651 # correlation -0.997 : Rs plus grand <-> coeur moins dense
COV_2D = np.array([[1.640719e-03, -3.651150e-03], [-3.651150e-03, 8.172475e-03]])

# --- PARAMÈTRES DE L'ASTRE TOPOLOGIQUE ---
M_ecf = 1e24  # Masse typique d'un astre ECF en kg (Masse planétaire)

# --- OBSERVED BARYONIC MASS ---
# Total visible mass (gas + stars) of NGC 6503, from SPARC table1:
# 0.5*L[3.6] (stars, 6.42e9) + 1.33*M_HI (gas, 2.32e9). The former 6.4e9 was stars only.
M_baryon_Msun = 8.742e9
M_baryon_kg = M_baryon_Msun * M_sun    # Conversion en kg

# --- FUNCTION: ECF HALO MASS ---
def masse_halo_ecf(rayon_kpc, log_rho0_val=log_rho0, Rs_kpc_val=Rs_kpc):
    """Calcule la masse du halo de matière noire (ECF) inclus dans un rayon donné.
    Parametree sur (log_rho0, Rs_kpc) pour permettre la propagation Monte-Carlo
    ci-dessous ; les valeurs par defaut reproduisent le calcul original."""
    rho0_val = (10**log_rho0_val) * g_cm3_to_kg_m3
    Rs_val = Rs_kpc_val * kpc_to_m
    r = rayon_kpc * kpc_to_m
    x = r / Rs_val
    # Integral of a pseudo-isothermal profile (regular ECF core)
    masse = 4 * np.pi * rho0_val * (Rs_val**3) * (x - np.arctan(x))
    return masse

# --- GALAXY CALCULATION (out to 15 kpc, the edge of the visible gas) ---
r_visible = 15.0  
M_halo = masse_halo_ecf(r_visible)

# Number of objects, and the ratio
N_astres = M_halo / M_ecf
ratio_local = M_halo / M_baryon_kg

# [02/09/2026] UNCERTAINTY PROPAGATION -- Monte Carlo draw from the (log_rho0,
# Rs_kpc) empirical covariance of the emcee chain on SPARC (mcmc_ngc6503_sparc.py,
# N-5, 22/09/2026; COV_2D above), propagated through the same
# mass integral used above. N=100000 draws is enough for a stable 68% band
# on a smooth, mildly nonlinear function of two correlated Gaussians.
np.random.seed(42)
_N_MC = 100_000
_mean_2d = np.array([log_rho0, Rs_kpc])
_draws = np.random.multivariate_normal(_mean_2d, COV_2D, _N_MC)
_M_halo_mc = np.array([masse_halo_ecf(r_visible, lr, rs) for lr, rs in _draws])
_ratio_mc = _M_halo_mc / M_baryon_kg
M_HALO_MED, M_HALO_LO, M_HALO_HI = np.percentile(_M_halo_mc, [50, 16, 84])
RATIO_MED, RATIO_LO, RATIO_HI = np.percentile(_ratio_mc, [50, 16, 84])

# --- RESULTS ---
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

print("-" * 62)
print("  UNCERTAINTY (Monte Carlo, 02/09/2026)")
print("-" * 62)
print(f"  Propagated from the (log_rho0, Rs) covariance of")
print(f"  the emcee chain on SPARC (mcmc_ngc6503_sparc.py, N-5) -- 68% interval, {_N_MC:,} draws:")
print(f"    M_halo = {M_HALO_MED/M_sun:.2e} M_sun  "
      f"[{M_HALO_LO/M_sun:.2e} , {M_HALO_HI/M_sun:.2e}]")
print(f"    ratio  = {RATIO_MED:.2f}  [{RATIO_LO:.2f} , {RATIO_HI:.2f}]")
print(f"  NOTE: this is a reconstructed Gaussian on the published summary")
print(f"  statistics, not the raw MCMC chain -- see header.")

# ── ⭐ CANONICAL OUTPUT (added 21/08/2026) ─────────────────────────────────
print()
print("-" * 62)
print("  CANONICAL OUTPUT  (comparable with the corpus)")
print("-" * 62)
print(f"  ECF dark/baryon ratio (NGC 6503, r < {r_visible:.0f} kpc) = {ratio_local:.2f}")
print()
print("  ⚠️ THIS IS *NOT* THE 5:1 OF F2 -- THE TWO ARE DIFFERENT QUANTITIES:")
print("     · F2's 5:1 is a GLOBAL, PRIMORDIAL ratio (Omega_DM/Omega_b), set")
print("       at torsion crystallisation near the electroweak scale (T ~ 159")
print("       GeV). A degrees-of-freedom equipartition over the 20:4")
print("       decomposition of the torsion tensor gives 20/4=5, within 6.7%")
print("       of the observed ~5.36 -- SUGGESTIVE, NOT ADOPTED: F2 itself")
print("       flags the ΔN/eta link as an open problem (PO-F2-1), and a")
print("       04/09/2026 attempt to derive a knot-survival fraction from")
print("       first principles did not confirm it (see")
print("       ECF_PROBLEME_ratio_DM_baryon_PO-F2-1.md).")
print("       It holds for the WHOLE universe, at the epoch dark matter is formed.")
print("     · the number above is a LOCAL, PRESENT-DAY ratio for ONE galaxy,")
print("       integrated out to an arbitrary radius -- it grows with that")
print("       radius and would differ for any other galaxy.")
print("     ⭐ Their numerical proximity is COINCIDENTAL, and the SPARC data")
print("       say so: 37 % of the 175 galaxies (sparc_ratio_statistics.py, which")
print("       fits nothing and so keeps all 175) fall between 4 and 7, and")
print("       the sample median is 4.2.")
print("       ⇒ landing near 5 is UNREMARKABLE -- it is the typical behaviour")
print("         of the sample, NOT a successful prediction.")
print("       See sparc_ratio_statistics.py for the full distribution.")
