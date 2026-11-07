#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECF_solver_minimal_JalonA_background.py
=======================================
Projet CLASS-EC — Bloc 1, étape « solveur minimal standalone », JALON A.

But du Jalon A : reproduire et VALIDER le fond cosmologique de l'ECF
(matière + rayonnement + dette de torsion en CPL calibré, sous la fermeture
plate Ω_total = 1), et retrouver les repères de Foundation I :
  - le franchissement du « phantom divide » (w = -1) vers z ~ 1,7 ;
  - un âge de l'univers ~ 12,7 milliards d'années.

C'est la BASELINE calibrée. Le Jalon B (étape suivante) remplacera le w(a)
POSÉ ici par un w(z) DÉRIVÉ du couplage torsion-courbure, et comparera.

Statut épistémique de ce fichier : [Calibré]. Rien n'est dérivé ici ;
on vérifie seulement que le fond calibré est correctement reproduit.

Dépendances : numpy, scipy, matplotlib.
"""
# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
# [CORRIGE 15/09/2026] Le chemin de sortie etait « /mnt/user-data/outputs/ »,
# un chemin absolu de l'environnement ou le script a ete ecrit. Il ne peut
# exister sur aucune autre machine : FileNotFoundError garanti chez quiconque
# reproduit le corpus. Remplace par une sortie dans le dossier du script.

import os
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# ECF background parameters (calibrated in Foundation I; H0 from REV-2)
# ----------------------------------------------------------------------
H0     = 73.04          # km/s/Mpc  — valeur ECF calibrée (SH0ES ; cf. REV-2)
# [D3, 22/09/2026 -- DEC-A7-POST-05] Fond ECF explicite (H0 = 73.04) : Omega_i =
# omega_i/h_ECF^2 (A-7 pour la matiere, meme convention pour le rayonnement).
# Etaient Om = 0.30 (valeur ronde) et Or = 9.2e-5 (h Planck).
Om     = (0.02237 + 0.1200)/0.7304**2   # matière (ordinaire + noire), aujourd'hui : 0.266868
Or     = 2.4728e-5*(1 + (7/8)*(4/11)**(4/3)*3.046)/0.7304**2   # rayonnement : 7.8417e-5
w0, wa = -0.904, -0.153 # CPL calibré (Foundation I)
Ode    = 1.0 - Om - Or  # fermeture TIP : Ω_total = 1 (univers plat)

KM_S_MPC_TO_PER_GYR = 1.02271e-3   # 1 km/s/Mpc  ->  1/Gyr

# ----------------------------------------------------------------------
# Background: CPL dark-energy density, H(a), w(a)
# ----------------------------------------------------------------------
def f_de(a):
    """rho_DE(a) / rho_DE(1) pour w(a) = w0 + wa (1-a)  (formule CPL)."""
    return a**(-3.0*(1.0 + w0 + wa)) * np.exp(-3.0*wa*(1.0 - a))

def E(a):
    """H(a) / H0."""
    return np.sqrt(Om*a**-3 + Or*a**-4 + Ode*f_de(a))

def w_de(a):
    return w0 + wa*(1.0 - a)

# ----------------------------------------------------------------------
# JALON A.1 — franchissement du phantom divide  w(a) = -1
# ----------------------------------------------------------------------
a_cross = 1.0 - (-1.0 - w0)/wa       # résout w0 + wa(1-a) = -1
z_cross = 1.0/a_cross - 1.0
print("="*64)
print("JALON A — reproduction du fond ECF")
print("="*64)
print(f"A.1  Franchissement w=-1 : a = {a_cross:.3f}, z = {z_cross:.3f}   (attendu ~1,7)")

# ----------------------------------------------------------------------
# MILESTONE A.2 -- age of the universe
# ----------------------------------------------------------------------
H0g = H0 * KM_S_MPC_TO_PER_GYR                       # 1/Gyr
I, _ = quad(lambda a: 1.0/(a*E(a)), 1e-8, 1.0, limit=200)
age  = I / H0g
# AUDIT NOTE (15/08, updated D3 22/09/2026): age computed along the CPL trajectory
# (w0,wa) -- 12.78 Gyr with the former Om=0.30, 13.19 Gyr with Om = omega_m/h^2
# (A-7). This DIFFERS BY CONSTRUCTION from the canonical t0 of Foundation I
# (13.33 Gyr post-A-7, script_09_cosmic_ages.py), which applies STRICTLY to the w=-1 ansatz
# (see F1, note b of the age table). Same integrand H(z)^-1, different
# definitions of w. Do not conflate the two.
print(f"A.2  Age of the universe: {age:.2f} Gyr             (CPL trajectory; the w=-1 t0 is script_09's; 1/H0 = {1/H0g:.2f} Gyr)")

# ----------------------------------------------------------------------
# MILESTONE A.3 -- H(z) and w(z) at a few reference redshifts
# ----------------------------------------------------------------------
print("A.3  Repères :")
for z in [0.0, 0.5, 1.0, 2.0, 1089.0]:
    a = 1.0/(1.0+z)
    print(f"       z={z:>7.1f} : H={H0*E(a):>10.1f} km/s/Mpc, w_DE={w_de(a):+.3f}")

# ----------------------------------------------------------------------
# Automatic validations (the milestone's own test)
# ----------------------------------------------------------------------
assert abs(z_cross - 1.7) < 0.15, "le franchissement n'est pas vers z~1,7"
assert 12.0 < age < 13.5,          "l'âge est hors de la plage ECF attendue"
print("-"*64)
print("JALON A VALIDÉ : fond ECF reproduit (franchissement z~1,7 ; âge cohérent).")
print("Prochain : JALON B — remplacer le w(a) POSÉ par un w(z) DÉRIVÉ du couplage.")
print("="*64)

# ----------------------------------------------------------------------
# w(z) figure (baseline -- the analogue of Figure 9.1 in the book)
# ----------------------------------------------------------------------
z  = np.linspace(0.0, 2.5, 500)
a  = 1.0/(1.0+z)
plt.figure(figsize=(7.2, 4.6))
plt.axhline(-1.0, ls="--", c="gray", lw=1.3, label="w = -1 (constante cosmologique)")
plt.plot(z, w_de(a), c="#1f3b66", lw=2.2, label="ECF — dette gelée (CPL calibré)")
plt.axvline(z_cross, ls=":", c="crimson", lw=1.4, alpha=0.8)
plt.annotate(f"franchit -1 à z ≈ {z_cross:.2f}", xy=(z_cross, -1.0),
             xytext=(z_cross+0.05, -0.92), color="crimson", fontsize=9)
plt.scatter([0.0], [w0], c="#1f3b66", zorder=5)
plt.annotate(f"aujourd'hui : w0 = {w0}", xy=(0.0, w0), xytext=(0.12, -0.885), fontsize=9)
plt.xlabel("décalage vers le rouge z  (vers le passé →)")
plt.ylabel("w  (pression / densité)")
plt.title("Solveur minimal ECF — Jalon A : w(z) du fond (baseline calibrée)")
plt.ylim(-1.05, -0.86)
plt.legend(loc="lower left", fontsize=9)
plt.tight_layout()
# [CORRIGE 15/09/2026] Sortie deplacee vers _generated/ : cette courbe est
# un diagnostic du solveur, pas une figure du papier. Elle n'est citee par
# aucun document et n'a pas sa place dans figures_output, que la
# centralisation reserve aux figures publiees. _generated/ est exclu du
# balayage depuis ce matin, pour la meme raison que les frames d'animation.
_DIAG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_generated")
os.makedirs(_DIAG, exist_ok=True)
plt.savefig(os.path.join(_DIAG, "ECF_solver_JalonA_wz.png"), dpi=130)
print("Figure : ECF_solver_JalonA_wz.png")
