#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Foundation III — Le cœur de Cartan : résolution TOV avec torsion
#  Fichant, P. (2026).   Fichier : core_tov_torsion.py   (item CORE-1)
#  Dernière modification : 20/07/2026, 22:55
#
#  EMPLACEMENT (dépôt GitHub) :
#     Foundation_3/02_Scientific_Code/A_Core_Calculations/
# =============================================================================
#
#  OBJET
#  -----
#  Préciser la structure du cœur de Cartan — le noyau dense qui remplace la
#  singularité — au-delà de l'argument d'ordre de grandeur.
#
#  CE QUI EST DÉMONTRÉ ICI
#  -----------------------
#   (T1) rho <= rho_c            : exact (Friedmann-torsion).
#   (T2) rho <  rho_c / 2        : NOUVEAU. Un cœur STATIQUE LIÉ ne peut pas
#        dépasser la moitié de la densité de Cartan. Le « facteur d'ordre 1 »
#        laissé indéterminé dans les versions antérieures vaut exactement 1/2.
#   (T3) Un cœur statique EXIGE un horizon interne : sous un horizon de
#        Schwarzschild, la coordonnée r est du genre temps et aucune solution
#        statique n'existe. Le cœur relève donc des TROUS NOIRS RÉGULIERS.
#
#  CE QUI EST MODÉLISÉ (et non dérivé)
#  -----------------------------------
#   La forme de Hayward (cœur de Sitter, deux horizons) est le modèle standard
#   de trou noir régulier. Elle N'EST PAS dérivée du lagrangien d'Einstein-
#   Cartan. Les grandeurs L, R_core, M_core en découlent ÉTANT DONNÉ ce modèle.
#
#  RÉSERVE D'ÉCHELLE (importante)
#  ------------------------------
#   Le cœur est d'ordre PLANCKIEN. Le préfacteur numérique (0.49, 1, 2...) n'a
#   PAS de contenu physique : à l'échelle de l_Pl, la description classique
#   (RG, Einstein-Cartan, Hayward) sort de son domaine de validité. Seul
#   R_core ~ l_Pl est significatif.
#   Cette limite n'est pas propre à l'ECF : elle affecte identiquement
#   l'étoile de Planck de la gravité quantique à boucles.
#
#  Reproductibilité : Python >= 3.9, numpy, scipy. Déterministe.
# =============================================================================

import numpy as np
from scipy.optimize import brentq

SEP = "=" * 74

# --- Constantes --------------------------------------------------------------
G, c, hbar = 6.674e-11, 2.998e8, 1.055e-34
RHO_C = c**5 / (hbar * G**2)          # densité de Cartan = densité de Planck
l_P   = np.sqrt(hbar * G / c**3)
m_P   = np.sqrt(hbar * c / G)
M_SUN = 1.989e30

print(SEP)
print("  LE CŒUR DE CARTAN — résolution TOV avec torsion  (item CORE-1)")
print(SEP)
print(f"  rho_c = c^5/(hbar G^2) = {RHO_C:.4e} kg/m3   (= densité de Planck)")
print(f"  l_Pl  = {l_P:.4e} m        m_Pl = {m_P:.4e} kg")

# =============================================================================
#  T1/T2 — La densité est bornée, et plus finement qu'on ne le croyait
# =============================================================================
print()
print(SEP)
print("  T2 — Un cœur statique lié exige rho < rho_c / 2")
print(SEP)
print("""
  Équation d'état raide (celle du corpus pour la phase stiff) : P = rho c^2.
  La correction de torsion la PRÉSERVE :

      rho_eff = rho (1 - rho/rho_c)        P_eff = rho_eff c^2

  Or rho_eff n'est PAS monotone : elle culmine en rho = rho_c/2.
""")
u = np.linspace(0, 1, 11)
print("     rho/rho_c    rho_eff/rho_c = P_eff/(rho_c c^2)")
for ui in u:
    tag = "   <-- MAXIMUM" if abs(ui - 0.5) < 1e-9 else ""
    print(f"       {ui:.1f}          {ui*(1-ui):.4f}{tag}")

print("""
  Un cœur LIÉ à l'équilibre hydrostatique doit satisfaire SIMULTANÉMENT :
      (C1)  dP_eff/dr < 0     [équation TOV]
      (C2)  drho/dr   < 0     [la densité décroît vers l'extérieur]

  Or   dP_eff/dr = rho_c c^2 (1 - 2 rho/rho_c) drho/dr.

  Substituer (C2) dans (C1) impose (1 - 2 rho/rho_c) > 0, soit :

          ===>   rho(r) < rho_c / 2   PARTOUT dans le cœur.

  INTERPRÉTATION. Au-delà de rho_c/2 :
      dP_eff/d(rho) = c^2 (1 - 2 rho/rho_c) < 0
  Ajouter de la matière RÉDUIT la pression de soutien — la torsion mord plus
  vite que la gravité n'ajoute. Il n'y a plus de mode sonore, et aucune
  configuration statique liée n'existe. La branche rho > rho_c/2 est
  dynamiquement exclue.
""")
print(f"  ===> rho_core < rho_c/2 = {0.5*RHO_C:.4e} kg/m3   [DÉMONTRÉ]")

# =============================================================================
#  T3 — Pas de solution statique sous un horizon de Schwarzschild
# =============================================================================
print()
print(SEP)
print("  T3 — Un cœur statique EXIGE un horizon interne")
print(SEP)
print("""
  OBSTACLE. Sous un horizon de Schwarzschild (r < 2GM/c^2), la coordonnée r
  devient du GENRE TEMPS : aucun observateur statique ne peut exister, tout
  chute vers l'intérieur. Chercher un équilibre hydrostatique statique sous
  l'horizon des événements est donc MAL POSÉ.

  RÉSOLUTION : les TROUS NOIRS RÉGULIERS (Bardeen, Hayward). Structure :
      * cœur central de type de Sitter (densité ~ constante)
      * DEUX horizons : externe (événements) et interne (Cauchy)
      * entre les deux : région dynamique
      * SOUS l'horizon interne : la région redevient STATIQUE   <-- le cœur

  (Popławski a lui-même exposé la collapse avec torsion dans un ouvrage
   consacré aux trous noirs réguliers, Springer 2023.)
""")

# =============================================================================
#  Structure de Hayward, avec L FIXÉE par la borne rho_c/2
# =============================================================================
print(SEP)
print("  STRUCTURE  (forme de Hayward — MODÈLE, non dérivé d'ECKS)")
print(SEP)

RHO_CORE = 0.5 * RHO_C                                  # borne DÉMONTRÉE
L = np.sqrt(3 * c**2 / (8 * np.pi * G * RHO_CORE))      # longueur de Hayward

print(f"""
  La longueur L du cœur n'est PAS ajustée : elle est fixée par rho_core.

      L = sqrt( 3 c^2 / (8 pi G rho_core) )  avec  rho_core = rho_c/2

      L = {L:.4e} m  =  {L/l_P:.3f} l_Pl        <-- échelle planckienne
""")

def f_metric(r, M):
    """Fonction métrique de Hayward : f(r) = 1 - 2GM r^2 / (c^2 (r^3 + 2GM L^2/c^2))."""
    rs = 2 * G * M / c**2
    return 1.0 - rs * r**2 / (r**3 + rs * L**2)

print(f"  {'Trou noir':>14s} {'r- (m)':>13s} {'r+ (m)':>13s} {'R_s (m)':>13s} {'r-/l_Pl':>9s}")
print("  " + "-" * 68)
for name, M in [("10 M_sun", 10*M_SUN), ("1e6 M_sun", 1e6*M_SUN), ("1e9 M_sun", 1e9*M_SUN)]:
    rs = 2 * G * M / c**2
    r_out = brentq(f_metric, 0.5*rs, 2*rs, args=(M,), xtol=1e-30)
    rr = np.logspace(np.log10(L*1e-3), np.log10(0.9*rs), 40000)
    ff = f_metric(rr, M)
    sc = np.where(np.diff(np.sign(ff)) != 0)[0]
    r_in = rr[sc[0]] if sc.size else float("nan")
    print(f"  {name:>14s} {r_in:13.4e} {r_out:13.4e} {rs:13.4e} {r_in/l_P:9.4f}")

R_core = L
M_core = (4*np.pi/3) * RHO_CORE * R_core**3
print(f"""
  LECTURE
    * r+ (horizon externe) ~ R_s : l'objet est INDISCERNABLE d'un trou noir de
      Schwarzschild vu de l'extérieur — cohérent avec la contrainte de
      compacité GWTC-3 (C = 0.5).
    * r- (horizon interne) est d'échelle PLANCKIENNE, essentiellement
      indépendant de la masse du trou noir.
    * Le cœur, enfoui sous r-, est totalement INVISIBLE de l'extérieur.
    * Le cœur ne « contient » PAS la masse M du trou noir : c'est un noyau
      planckien ; la masse est portée par le champ entre r- et r+.

    R_core ~ L         = {R_core:.3e} m  ~ l_Pl
    M_core ~ (4pi/3) rho_core R_core^3 = {M_core:.3e} kg ~ {M_core/m_P:.2f} m_Pl

  ATTENTION — le préfacteur ({R_core/l_P:.2f} l_Pl) n'a PAS de contenu physique.
  À l'échelle de Planck, la description classique sort de son domaine de
  validité. Seul  R_core ~ l_Pl  est significatif.
""")

print(SEP)
print("  BILAN CORE-1")
print(SEP)
print("""
  DÉMONTRÉ
    * rho <= rho_c                        (exact, Friedmann-torsion)
    * rho <  rho_c/2 pour un cœur statique lié  [NOUVEAU — le facteur
      d'ordre 1 vaut exactement 1/2]
    * un cœur statique EXIGE un horizon interne  -> trou noir régulier

  MODÉLISÉ
    * la forme de Hayward (cœur de Sitter, deux horizons) n'est pas dérivée
      du lagrangien d'Einstein-Cartan
    * L, R_core, M_core en découlent ÉTANT DONNÉ ce modèle

  RESTE OUVERT
    * dérivation du cœur depuis l'action ECKS complète (sans forme
      métrique postulée) -- travail pluri-session, déféré à Foundation IV.
    * [MAJ 16/07/2026] Le critère de nucléation t_dyn << t_acc est
      désormais QUANTIFIÉ (marge de 15-17 ordres de grandeur en régime
      standard ISM/Eddington) -- voir cartan_core.py, TEST 4. Le régime
      hypercritique (collapsar/GRB, item CORE-1-HYPERACC) reste ouvert,
      mais FUSIONNÉ au point précédent (dérivation ab initio) plutôt que
      traité comme un problème séparé : il requiert le même ingrédient
      manquant (réponse dynamique du cœur à un afflux trop rapide).
""")
