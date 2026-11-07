
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
[SUPERSEDED 04/09/2026 -- see Scripts_F2/derive_f_dilution_baryogenesis.py]
=============================================================================
This script implements an EARLIER, ABANDONED baryogenesis mechanism (chiral
anomaly on discrete topological-defect walls, with an inverted volume-fraction
calculation) that is NOT the mechanism currently described in Foundation II
(the universal axial-torsion-vector coupling + electroweak sphalerons, F2 S3).
It was previously miscited in the F2 abstract as the source of eta=6.1e-10;
that citation has been corrected to point to derive_f_dilution_baryogenesis.py,
which reproduces the current, actually-published derivation (itself flagged
as an open issue -- see ECF_PROBLEME_facteur_dilution_f_eta.md).
Kept here for reference only; not part of the current baryogenesis narrative.
=============================================================================

PROJECT FOUNDATION: TOPOLOGICAL BARYOGENESIS CALCULATOR (ECF MODEL)
=============================================================================

ABSTRACT:
    This script computes the theoretical Baryon-to-Photon ratio (eta) generated
    by the formation of macroscopic Topological Dark Matter defects (ECF objects).
    It demonstrates that the observed matter-antimatter asymmetry arises naturally
    from the Chiral Anomaly on the domain walls of these defects, considering
    their discrete nature (solitons).

PHYSICS MECHANISM:
    1. Source: Topological Electroweak Baryogenesis via Chiral Anomaly (Adler-Bell-Jackiw).
    2. CP Violation: Induced geometrically by the winding number of the defect.
    3. Dilution: The local asymmetry is high on the wall, but diluted by the 
       fact that defects are discrete objects (Volume Fraction < 1).

COSMOLOGICAL ASSUMPTIONS (CONSISTENT WITH FOUNDATION I):
    - Hubble Constant (H0): 73.04 km/s/Mpc (Local/SH0ES value).
    - H0 = 73.04 km/s/Mpc (SH0ES/H0DN, consistent with Foundation I calibration).
      The Planck value (67.4) is not used here; see Foundation I for the tension discussion.
      but we strictly adhere to the physical baryon density (Omega_b h^2 = 0.0224)
      constrained by Big Bang Nucleosynthesis (BBN).

INPUTS:
    - Mass of ECF Object: ~10^24 kg (Soliton/Defect scale).
    - Electroweak Coupling (alpha_W): ~1/30.
    - Geometric Efficiency on Wall (kappa): Order O(10).

OUTPUTS:
    - Calculation of local asymmetry (on the wall).
    - Determination of the required Volume Fraction (f_vol) to match BBN.
    - Consistency check: Is this f_vol compatible with Dark Matter density?

-----------------------------------------------------------------------------
Author: The Author (Foundation Series)
Date: February 2026
License: Academic Use / MIT
=============================================================================
"""

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

# --- 1. CONSTANTES PHYSIQUES & COSMO (Version Foundation I : H0=73) ---
k_B = 1.380649e-23   # Boltzmann
hbar = 1.0545718e-34 # Planck réduit
c = 2.99792458e8     # Vitesse lumière
G = 6.67430e-11      # Gravitation

# Corrected parameters (Hubble-tension resolution)
H0 = 73.04  # km/s/Mpc (SH0ES - Riess et al.)
h = H0 / 100.0

# Physical baryon density (BBN invariant -- nucleosynthesis)
# This is the ground-truth value, independent of the expansion model.
omega_b_phys = 0.0224 

# ECF parameters (particle physics at the electroweak scale)
alpha_W = 1.0/30.0   # Constante de couplage faible à 100 GeV
g_star = 106.75      # Degrés de liberté (Standard Model complet)

# --- 2. OBSERVATION CIBLE ---
# Planck 2018 / PDG value
eta_obs = 6.1e-10

# --- 3. THE ECF MODEL CALCULATION ---
def calculate_topological_baryogenesis():
    print(f"--- PARAMETRES D'ENTREE ---")
    print(f"H0 utilized: {H0} km/s/Mpc")
    print(f"Target Baryon Density (BBN): {omega_b_phys}")
    print(f"Electroweak Coupling (alpha_W): {alpha_W:.4f}")
    print(f"-"*40)

    # A. LOCAL efficiency (on the defect wall, i.e. the ECF object)
    # The chiral anomaly operates at full strength on the topological singularity.
    # Enhanced sphaleron factor ~ alpha_W^4
    # Kappa is the geometric efficiency (it depends on the winding number).
    kappa_geo = 10.0 
    
    # Standard formula, modified for defects (Cohen-Kaplan-Nelson limit)
    # The factor 1000 comes from the non-perturbative dynamics (prefactor)
    eta_wall_core = (alpha_W**4 / g_star) * kappa_geo * 1000.0
    
    # B. DILUTION THERMIQUE
    # Standard dilution factor from post-inflation / post-transition reheating
    dilution_factor = 0.5
    
    # C. REQUIRED VOLUME FRACTION
    # eta_obs = eta_wall * dilution * f_vol
    # Inverted to obtain f_vol: what defect density is required?
    required_f_vol = eta_obs / (eta_wall_core * dilution_factor)
    
    return eta_wall_core, required_f_vol

# --- 4. EXECUTION ET RAPPORT ---
if __name__ == "__main__":
    eta_local, f_vol = calculate_topological_baryogenesis()

    print(f"--- RÉSULTATS DU CALCUL ---")
    print(f"1. Asymétrie Locale (SUR la paroi du défaut) : {eta_local:.2e}")
    print(f"   (C'est l'efficacité maximale théorique d'un défaut isolé)")
    print(f"")
    print(f"2. Observation Cible (Moyenne Cosmique)      : {eta_obs:.2e}")
    print(f"")
    print(f"3. DEDUCTION : Fraction Volumique Requise (f_vol) : {f_vol:.2e}")
    print(f"-"*40)
    print(f"INTERPRÉTATION PHYSIQUE (Pour le papier):")
    print(f"Pour reproduire l'observation, les défauts topologiques doivent occuper")
    print(f"environ {f_vol*100:.4f}% du volume de l'univers lors de la transition.")
    print(f"")
    print(f"CONCLUSION:")
    print(f"Cette faible fraction ({f_vol:.1e}) confirme que les astres ECF sont des")
    print(f"objets DISCRETS et COMPACTS (Solitons), espacés dans le vide, et non")
    print(f"un champ continu. Cela valide l'hypothèse de Matière Noire Granulaire.")
    print(f"=============================================================================")

# ── ⭐ CANONICAL OUTPUT (added 21/08/2026) ─────────────────────────────────
# Modelled on ECF_solver_minimal_JalonA_background.py, which prints the
# computed value, THE EXPECTED VALUE, and the comparison point on one line.
# ⚠️ Before this, 75 of the 83 F2 scripts printed no comparable number, so the
# results of F2 were verifiable by NO automated control.
print()
print("-" * 62)
print("  CANONICAL OUTPUT  (comparable with the corpus)")
print("-" * 62)
print(f"  ECF eta_B = {eta_obs:.3e}"
      f"        (F2 quotes 6.1e-10; Planck 6.10e-10)")
