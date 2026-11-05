#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stamp_headers.py — horodatage des en-tetes des livrables ECF
=============================================================

Regle posee par Pascal le 19/08/2026 : chaque fichier livrable porte, dans son
en-tete, la date ET l'heure de sa derniere modification.

POURQUOI. Un document de synthese ne dit pas de lui-meme s'il est a jour. Sans
horodatage visible, on ne peut pas savoir si l'architecture qu'on lit precede
ou suit la correction d'hier — et c'est exactement le defaut qui a laisse sept
valeurs perimees dans l'architecture jusqu'au 19/08.

L'heure de reference est l'heure de Paris, LUE et jamais estimee (mtime du
fichier), conformement a la regle d'horodatage du corpus.

Usage :
    python stamp_headers.py [chemin]          # met a jour
    python stamp_headers.py [chemin] --check  # verifie seulement (sortie 0/1)

En mode --check, sortie 1 si un livrable a ete modifie apres l'horodatage
qu'il affiche : c'est le controle a passer avant toute archive.
"""
# Last modified: 19/08/2026, 09:36 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys, os, re, subprocess
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

args = [a for a in sys.argv[1:] if not a.startswith("--")]
CHECK = "--check" in sys.argv
ROOT = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

# Livrables : tout ECF_*.md, sauf les archives de session et les points de
# sauvegarde, qui sont dates par nature et ne doivent pas etre re-horodates.
EXCLURE = re.compile(r'(POINT_DE_SAUVEGARDE|RAPPORT_MODIFICATIONS|_20\d\d-)')


def heure_paris(ts):
    """Paris = UTC+2 en aout (heure d'ete). L'heure est LUE, jamais estimee."""
    return datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=2)))


def mtime_reel(path):
    """Le mtime du fichier ; c'est la seule source de verite sur sa date."""
    return os.path.getmtime(path)


def format_fr(dt):
    return f"{dt.day} {MOIS[dt.month - 1]} {dt.year}, {dt:%Hh%M} (heure de Paris)"


def format_en(dt):
    return f"{dt:%d %B %Y, %H:%M} (Paris time)".replace(" 0", " ")


fichiers = sorted(f for f in os.listdir(ROOT)
                  if f.startswith("ECF_") and f.endswith(".md")
                  and not EXCLURE.search(f))

modifies, perimes = [], []

for nom in fichiers:
    chemin = os.path.join(ROOT, nom)
    with open(chemin, encoding="utf-8") as fh:
        contenu = fh.read()

    dt = heure_paris(mtime_reel(chemin))
    est_en = nom.endswith("_EN.md")
    stamp = format_en(dt) if est_en else format_fr(dt)
    ligne = (f"*Last updated: {stamp}*" if est_en
             else f"*Dernière mise à jour : {stamp}*")

    # 1. marqueur de gabarit jamais substitue (BUILD_TIMESTAMP_FR/EN)
    if "BUILD_TIMESTAMP" in contenu:
        if CHECK:
            perimes.append((nom, "marqueur BUILD_TIMESTAMP non substitue"))
            continue
        contenu = re.sub(r'BUILD_TIMESTAMP_[A-Z]+', stamp, contenu)
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(contenu)
        modifies.append((nom, stamp))
        continue

    # 2. ligne d'horodatage deja presente : la comparer au mtime
    m = re.search(r'(?m)^\*(?:Dernière mise à jour|Last updated)\s*:\s*(.+?)\*$',
                  contenu)
    if m:
        # Tolerance a la minute : ecrire l'horodatage change le mtime, donc une
        # comparaison a la seconde declarerait perime le fichier qu'on vient de
        # tamponner. On ne signale que les ecarts d'au moins une minute.
        affiche = m.group(1).strip()
        mm = re.search(r'(\d{1,2})\s*[h:]\s*(\d{2})', affiche)
        if mm:
            ecart = abs((dt.hour * 60 + dt.minute)
                        - (int(mm.group(1)) * 60 + int(mm.group(2))))
            meme_jour = (str(dt.day) in affiche and MOIS[dt.month - 1] in affiche) \
                        or f"{dt:%d %B}" in affiche
            if meme_jour and ecart <= 1:
                continue
        if affiche == stamp:
            continue
        if CHECK:
            perimes.append((nom, f"affiche « {m.group(1)[:44]} », modifie le {stamp}"))
            continue
        contenu = contenu[:m.start()] + ligne + contenu[m.end():]
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(contenu)
        modifies.append((nom, stamp))
        continue

    # 3. aucune ligne : l'inserer apres le titre de niveau 1
    if CHECK:
        perimes.append((nom, "aucune ligne d'horodatage"))
        continue
    # certains documents commencent par un titre de niveau 2 : accepter # ou ##
    m = re.search(r'(?m)^#{1,2} .+$', contenu)
    if not m:
        continue
    contenu = contenu[:m.end()] + "\n\n" + ligne + contenu[m.end():]
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(contenu)
    modifies.append((nom, stamp))

# ==========================================================================
# LES SCRIPTS
# ==========================================================================
# Un script depose sans date ne permet pas de savoir s'il correspond a la
# figure publiee. Le corpus portait trois formes concurrentes ("Date:",
# "Last modified:", "Dernière modification :") et la plupart des scripts
# n'en avaient aucune — y compris certains modifies la veille.
#
# On ecrit une ligne UNIQUE et normalisee dans l'en-tete de commentaires,
# APRES la docstring quand il y en a une (une insertion avant la degraderait
# en simple expression et supprimerait __doc__ — defaut rencontre le 15/08).

SCRIPT_DIRS = [os.path.join(ROOT, "Scripts_F1")]
LIGNE_SCRIPT = "# Last modified: {} (Paris time)"
# (?m)$ ne matche pas avant un \r : sans \r? le motif ne retrouve jamais la
# ligne dans un fichier CRLF, et chaque passe en empile une nouvelle.
MOTIF_SCRIPT = re.compile(r'(?m)^# Last modified: .*\(Paris time\)\r?$')

# Appartenance au corpus. Les lots F1 et F2 portent les MEMES NOMS pour des
# scripts differents : un fichier isole de son dossier devient inidentifiable.
# La ligne est donc ecrite dans le fichier lui-meme, sous l'horodatage.
# Le dossier d'origine fait foi ; a etendre quand F3/F4/architecture arriveront.
CORPUS_PAR_DOSSIER = {"Scripts_F1": "Foundation I", "Scripts_F2": "Foundation II"}
LIGNE_CORPUS = "# Corpus: {} — github.com/pfichant/spin-torsion-cosmology"
MOTIF_CORPUS = re.compile(r'(?m)^# Corpus: .*spin-torsion-cosmology\r?$')


def fin_docstring(txt):
    """Position juste apres la docstring de module, ou apres le shebang."""
    m = re.match(r'(?s)\s*(#![^\r\n]*[\r\n]+)?(#[^\r\n]*coding[^\r\n]*[\r\n]+)?\s*'
                 r'(?P<q>"""|\'\'\')', txt)
    if m:
        q = m.group('q')
        fin = txt.find(q, m.end())
        if fin != -1:
            return txt.find("\n", fin + 3) + 1
    # pas de docstring : apres les lignes d'en-tete (shebang, coding)
    pos = 0
    for ligne in txt.split("\n"):
        if ligne.startswith("#!") or "coding" in ligne[:30]:
            pos += len(ligne) + 1
        else:
            break
    return pos


scripts = []
for d in SCRIPT_DIRS:
    if os.path.isdir(d):
        scripts += [os.path.join(d, f) for f in sorted(os.listdir(d))
                    if f.endswith(".py")]

sc_modifies, sc_perimes = [], []
for chemin in scripts:
    with open(chemin, encoding="utf-8", errors="replace", newline="") as fh:
        contenu = fh.read()
    nl = "\r\n" if "\r\n" in contenu else "\n"
    dt = heure_paris(mtime_reel(chemin))
    stamp = f"{dt:%d/%m/%Y, %H:%M}"
    ligne = LIGNE_SCRIPT.format(stamp)
    nom = os.path.basename(chemin)

    # ligne d'appartenance : ecrite une fois, jamais re-ecrite ensuite
    corpus = CORPUS_PAR_DOSSIER.get(os.path.basename(os.path.dirname(chemin)))
    if corpus and not MOTIF_CORPUS.search(contenu):
        if CHECK:
            sc_perimes.append((nom, "aucune ligne d'appartenance au corpus"))
        else:
            mh = MOTIF_SCRIPT.search(contenu)
            if mh:
                # (?m)$ s'arrete AVANT le \r : inserer la, c'est couper la fin
                # de ligne en deux. On se place apres le saut de ligne complet.
                pos = contenu.find("\n", mh.end()) + 1
            else:
                pos = fin_docstring(contenu)
            contenu = contenu[:pos] + LIGNE_CORPUS.format(corpus) + nl + contenu[pos:]
            with open(chemin, "w", encoding="utf-8", newline="") as fh:
                fh.write(contenu)

    m = MOTIF_SCRIPT.search(contenu)
    if m:
        if m.group(0) == ligne:
            continue
        mm = re.search(r'(\d{2}):(\d{2})', m.group(0))
        if mm and f"{dt:%d/%m/%Y}" in m.group(0):
            ecart = abs((dt.hour * 60 + dt.minute)
                        - (int(mm.group(1)) * 60 + int(mm.group(2))))
            if ecart <= 1:
                continue
        if CHECK:
            sc_perimes.append((nom, f"affiche {m.group(0)[17:34]}, modifie le {stamp}"))
            continue
        contenu = contenu[:m.start()] + ligne + contenu[m.end():]
    else:
        if CHECK:
            sc_perimes.append((nom, "aucune ligne d'horodatage"))
            continue
        i = fin_docstring(contenu)
        contenu = contenu[:i] + ligne + nl + contenu[i:]
    with open(chemin, "w", encoding="utf-8", newline="") as fh:
        fh.write(contenu)
    sc_modifies.append((nom, stamp))

print("=" * 72)
print("  HORODATAGE DES LIVRABLES" + ("  —  VERIFICATION" if CHECK else ""))
print("=" * 72)
if CHECK:
    for nom, raison in perimes:
        print(f"  PERIME  {nom}")
        print(f"          -> {raison}")
    for nom, raison in sc_perimes:
        print(f"  PERIME  {nom}  [script]")
        print(f"          -> {raison}")
    print("-" * 72)
    print(f"  documents : {len(fichiers) - len(perimes)}/{len(fichiers)} a jour  |  "
          f"scripts : {len(scripts) - len(sc_perimes)}/{len(scripts)} a jour")
    perimes = perimes + sc_perimes
    if perimes:
        print("\n  ⚠️  Lancer sans --check AVANT de produire l'archive.")
    print("=" * 72)
    sys.exit(1 if perimes else 0)
else:
    for nom, stamp in modifies:
        print(f"  MAJ  {nom:44s} {stamp}")
    for nom, stamp in sc_modifies:
        print(f"  MAJ  {nom:44s} {stamp}  [script]")
    print("-" * 72)
    print(f"  {len(modifies)} document(s) et {len(sc_modifies)} script(s) horodates "
          f"({len(fichiers)} documents, {len(scripts)} scripts au total)")
    print("=" * 72)
