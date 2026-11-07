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
#  ECF / F3 — Oscillations de torsion post-rebond : portee observationnelle
#  Fichant, P. (2026).  Fichier : osc_gw_frequency.py   (item OSC-1)
# =============================================================================
#
#  OBJET : estimer la frequence, redshiftee jusqu'a aujourd'hui, des
#  oscillations de torsion mises en evidence par lg_bounce_dynamics.py,
#  et confronter cette frequence aux bandes des detecteurs d'ondes
#  gravitationnelles.
#
#  CONCLUSION (annoncee d'emblee, pour eviter toute surinterpretation) :
#    La frequence tombe vers ~1e11 Hz (bande UHF-GW). AUCUN detecteur
#    actuel ou planifie n'y a acces. De plus, le mode homogene (k=0) ne
#    source PAS de GW (il faut un quadrupole). Toute revendication de
#    "fossiles gravitationnels detectables" serait donc PREMATUREE.
#    Ce script documente une LIMITE, non une prediction.
# =============================================================================
import numpy as np

hbar, c, G = 1.055e-34, 2.998e8, 6.674e-11
t_P   = np.sqrt(hbar*G/c**5)
GeV_K = 1.16e13

OMEGA_REDUIT = 1.79      # omega = sqrt(4|a2|), mesure dans le prototype
T_BOUNCE_GeV = 9.9e18    # temperature au rebond (valeur canonique F3)
T_TODAY_K    = 2.725     # CMB

f_source = OMEGA_REDUIT / (2*np.pi*t_P)
redshift = T_TODAY_K / (T_BOUNCE_GeV * GeV_K)
f_today  = f_source * redshift

print("="*70)
print("Oscillations de torsion post-rebond — frequence aujourd'hui")
print("="*70)
print(f"  omega (unites de Planck)   : {OMEGA_REDUIT}")
print(f"  f_source                   : {f_source:.3e} Hz")
print(f"  facteur de redshift a/a0   : {redshift:.3e}")
print(f"  => f_aujourd'hui           : {f_today:.3e} Hz  ({f_today/1e9:.0f} GHz)")
print()
print("  Bandes de detection :")
for name, lo, hi in [("Pulsar Timing Array", 1e-9, 1e-7),
                     ("LISA",                1e-4, 1e-1),
                     ("LIGO / Virgo",        1e1,  1e3),
                     ("Einstein Telescope",  1e0,  1e4)]:
    print(f"    {name:22s} [{lo:.0e}, {hi:.0e}] Hz : "
          f"{'DANS LA BANDE' if lo <= f_today <= hi else 'hors bande'}")
print(f"""
  => La frequence excede de ~8 ordres de grandeur la limite superieure
     d'Einstein Telescope. Elle releve de la bande UHF-GW, pour laquelle
     seules des propositions exploratoires existent (cavites resonantes,
     conversion graviton-photon / effet Gertsenshtein), tres loin des
     sensibilites requises.

  DOUBLE RESERVE :
    (1) frequence hors de portee de tout instrument actuel ou planifie ;
    (2) le prototype integre un champ HOMOGENE T(t) : le mode k=0 n'a pas
        de moment quadrupolaire et ne source donc AUCUNE onde
        gravitationnelle. Etablir une signature exigerait de passer a
        T(x,t), de calculer le quadrupole, puis Omega_GW(f).

  STATUT : source POTENTIELLE de GW de tres haute frequence ; ni
  l'amplitude ni le spectre ne sont etablis. Non falsifiable en l'etat.
""")
