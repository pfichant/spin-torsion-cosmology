#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_architecture_sync.py — alignement architecture / papiers
==============================================================

À LANCER AVANT CHAQUE ARCHIVE ECF_CORPUS_COMPLET.

L'architecture (FR + EN) est un document de synthèse : elle recopie des
valeurs sans les justifier, donc elle HÉRITE SANS ÊTRE RELUE. Son risque
propre n'est pas la valeur fausse mais la valeur PÉRIMÉE — corrigée dans un
papier et restée ici.

Le 19/08/2026, sept valeurs périmées y ont été trouvées, dont une dans une
équation de fermeture. Elles dataient de corrections faites la veille.

⚠️ PIÈGE PRINCIPAL, rencontré deux fois : les deux versions n'écrivent pas
les nombres pareil. La version française écrit « 39{,}5 » là où l'anglaise
écrit « 39.5 ». Un balayage réglé sur une seule notation ne voit rien.
Ce script normalise avant de comparer.

Usage :
    python check_architecture_sync.py [chemin-du-corpus]

Sortie 0 si tout est aligné, 1 sinon.
"""
# Last modified: 19/08/2026, 09:37 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys, os, re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

FR = os.path.join(ROOT, "ECF_Architecture_Briques.md")
EN = os.path.join(ROOT, "ECF_Architecture_Briques_EN.md")

# --------------------------------------------------------------------------
# Valeurs RETIRÉES du corpus : elles ne doivent apparaître nulle part.
# Chaque entrée porte la raison — sans elle, un futur lecteur ne saura pas
# s'il regarde une régression ou un faux positif.
WITHDRAWN = [
    (r'39\.5',              "Delta chi2 = -39.5",
     "le budget omettait la ligne eBOSS et utilisait un chi2_H0 = 30.5 sans source ; total derivable = -39.4"),
    (r'31\.5',              "Delta AIC = -31.5",   "consequence du precedent : -31.4"),
    (r'(?<![0-9.])8\.2(?![0-9])', "Delta BIC = -8.2", "consequence du precedent : -8.1"),
    (r'1\.65\s*\\times\s*10\^\{-7\}', "Omega_spin,0 = 1.65e-7",
     "c'etait un RATIO rho_spin/rho_r affiche comme un parametre de densite, avec deux ordres perdus ; valeur reelle 1.5e-13"),
    (r'0\.853',             "sigma_8 = 0.853",
     "sigma_8 et S_8 etaient inverses : 0.832 EST le S_8 de Planck"),
    (r'1\.2791',            "F_ion = 1.2791",      "residu d'une version anterieure ; valeur 1.2765"),
    (r'0\.0030',            "sigma(F_ion) = 0.0030",
     "ne se reproduit pas depuis les contraintes declarees ; recalcul = 0.021"),
    (r'PO-F3-9',            "le code PO-F3-9",
     "n'existe que dans un document jamais depose ; decrire le solveur manquant"),
    (r'30\s*[-–]\s*35',     "Cosmic Dawn z = 30-35",
     "non derivable de B_ECF = 1.45, qui donne 27-29"),
    (r'10\^\{-22\}',        "rho_spin/rho_Lambda ~ 1e-22", "la formule donne 2.2e-13"),
    (r'10\^\{-60\}',        "Omega_spin,0 ~ 1e-60",        "47 ordres sous la valeur du script"),
]

# Valeurs qui DOIVENT être présentes, et en nombre ÉGAL dans les deux versions.
# Verifier la disparition ne suffit pas : un retour de version peut ramener
# la valeur fautive AVEC son remplacement absent.
# NOTE : on exige la PRESENCE dans les deux versions, pas l'egalite stricte
# du nombre d'occurrences. Les deux redactions different legitimement — la
# version anglaise repete un nombre la ou la francaise le sous-entend. Exiger
# l'egalite produisait un faux positif sur H_0 (FR 11, EN 14).
# Ce qui compte : aucune valeur presente d'un cote et ABSENTE de l'autre.
REQUIRED_BOTH = [
    (r'39\.4',                        "Delta chi2 = -39.4"),
    (r'1\.5\s*\\times\s*10\^\{-13\}', "Omega_spin,0 = 1.5e-13"),
    (r'0\.832',                       "S_8 (Planck) = 0.832"),
    (r'1\.2765',                      "F_ion = 1.2765"),
    (r'135\.8',                       "r_s = 135.8 Mpc"),
    (r'73\.04',                       "H_0 = 73.04"),
    (r'0\.766',                       "S_8 (ECF) = 0.766"),
    (r'12\.74',                       "t_0 = 12.74 Gyr"),
]


def normalise(txt):
    """FR ecrit 39{,}5, EN ecrit 39.5 — sans cela, le balayage ne voit rien."""
    return re.sub(r'\{,\}', '.', txt)


def read(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return normalise(f.read())


results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


fr, en = read(FR), read(EN)
if fr is None or en is None:
    print("  FAIL  architecture introuvable")
    print(f"        -> {FR if fr is None else EN}")
    sys.exit(1)

for pat, label, why in WITHDRAWN:
    a, b = len(re.findall(pat, fr)), len(re.findall(pat, en))
    check(f"retiree: {label}", not (a or b), f"FR:{a} EN:{b} — {why}")

for pat, label in REQUIRED_BOTH:
    a, b = len(re.findall(pat, fr)), len(re.findall(pat, en))
    check(f"presente des deux cotes: {label}", a > 0 and b > 0, f"FR:{a} EN:{b}")

# Les deux versions doivent avoir la meme ossature : une section ajoutee d'un
# cote et pas de l'autre est le premier signe d'une divergence de reflets.
# La mention de symetrie et du depot groupe doit rester dans les deux
# en-tetes : c'est ce qu'un refere lit avant tout le reste, et c'est la seule
# trace, dans le document lui-meme, de la regle des documents-reflets.
for pat, label in [(r'symétri|symmetric', "mention de la symetrie FR/EN"),
                   (r'Zenodo',            "mention du depot Zenodo"),
                   (r'DOI',               "mention du DOI")]:
    a_, b_ = bool(re.search(pat, fr)), bool(re.search(pat, en))
    check(f"en-tete: {label}", a_ and b_, f"FR:{a_} EN:{b_}")

h_fr = len(re.findall(r'(?m)^#{1,3} ', fr))
h_en = len(re.findall(r'(?m)^#{1,3} ', en))
check("meme nombre de sections FR/EN", abs(h_fr - h_en) <= 1, f"FR:{h_fr} EN:{h_en}")

print("=" * 70)
print("  ARCHITECTURE — ALIGNEMENT SUR LES PAPIERS")
print("=" * 70)
failed = 0
for name, ok, detail in results:
    if ok:
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")
        print(f"        -> {detail}")
print("-" * 70)
print(f"  {len(results) - failed} passes, {failed} echecs, {len(results)} total")
if failed:
    print("\n  ⚠️  Corriger AVANT de produire l'archive ECF_CORPUS_COMPLET.")
    print("      Rappel : toute correction vaut pour LES DEUX versions (documents-reflets).")
print("=" * 70)
sys.exit(1 if failed else 0)
