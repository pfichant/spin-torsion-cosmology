
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
r"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_ecf_axis_of_evil_cmb.py
Author:        Pascal Fichant
Date:          February 2026 (v1.1 - Post-Review)
Description:   ILLUSTRATIVE schematic of a low-multipole (l=2,3) phase
               alignment ("Axis of Evil"); not a demonstration (N-6).
Data Source:   none -- illustrative phases, not Planck data (N-6, 22/09/2026)
Output:        Fig3_Axis_of_Evil_ECF.png
CHAPITRE       : 4 - The Axis of Evil
OBJECTIF       :Simuler la carte de température du CMB (Cosmic Microwave Background).
                Le script superpose :
                1. Un bruit de fond isotrope (Standard Model).
                2. Une composante structurée alignée (Quadripôle l=2 + Octopôle l=3).
                L'alignement de ces modes le long d'un plan préférentiel illustre la "signature
                vectorielle" laissée par le Spin primordial (Théorie ECF).
=============================================================================
"""

"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_ecf_axis_of_evil_cmb.py
Author:        Pascal Fichant
Date:          February 2026 (v1.2 - Fix CSV Parsing)
Description:   ILLUSTRATIVE schematic of a low-multipole (l=2,3) phase
               alignment ("Axis of Evil"); not a demonstration (N-6).
Data Source:   none -- illustrative phases, not Planck data (N-6, 22/09/2026)
Output:        Fig3_Axis_of_Evil_ECF.png
=============================================================================
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# [AJOUT 12/09/2026] Graine fixee : ce script utilisait np.random sans
# graine, produisant une figure differente a chaque execution.
np.random.seed(42)
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def _find_foundation_dir(start):
    d = start
    for _ in range(5):
        if os.path.isdir(os.path.join(d, "data")) and os.path.isdir(os.path.join(d, "output")):
            return d
        parent = os.path.dirname(d)
        if parent == d: break
        d = parent
    return os.path.dirname(_SCRIPT_DIR)

_FOUNDATION2_DIR = _find_foundation_dir(_SCRIPT_DIR)
DATA_FILE   = os.path.join(_FOUNDATION2_DIR, "data", "Data_S3_CMB_Multipoles.csv")

# Fallback: search in script's own directory and all parent data/ folders
if not os.path.exists(DATA_FILE):
    for search_root in [_SCRIPT_DIR, os.path.dirname(_SCRIPT_DIR),
                        os.path.dirname(os.path.dirname(_SCRIPT_DIR))]:
        candidate = os.path.join(search_root, "data", "Data_S3_CMB_Multipoles.csv")
        if os.path.exists(candidate):
            DATA_FILE = candidate
            break
        candidate2 = os.path.join(search_root, "Data_S3_CMB_Multipoles.csv")
        if os.path.exists(candidate2):
            DATA_FILE = candidate2
            break

# [CORRIGE 15/09/2026] La sortie passait par _find_foundation_dir(), qui
# remonte l'arborescence en cherchant un dossier contenant data/ ET output/.
# Or B_Paper_Plots contient les deux (la propagation de donnees les y cree) :
# la fonction s'arretait donc la et creait B_Paper_Plots/figures_output/.
# Second coupable du dossier parasite, apres plot_F2_topological_network.py.
# On ecrit desormais a cote du script ; la centralisation du pipeline fait
# le reste, comme pour les 112 autres.
#
# _FOUNDATION2_DIR reste utilise pour TROUVER les donnees en entree : la
# fonction est correcte pour cela, c'est son emploi en sortie qui ne l'etait pas.
OUTPUT_FILE = os.path.join(_SCRIPT_DIR, "Fig3_Axis_of_Evil_ECF.png")

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data_S3_CMB_Multipoles.csv not found.")
        print(f"  Expected: {DATA_FILE}")
        print(f"  Fix: copy Data_S3_CMB_Multipoles.csv to:")
        print(f"       {os.path.join(_FOUNDATION2_DIR, 'data')}")
        # RULE 23 (25/08/2026) -- a plot script that produces a DEGRADED
        # figure, or none at all, must exit with a non-zero code. Exiting 0
        # lies to every automated chain: that is how Figure 29 of F2 shipped
        # with ten "File Not Found" panels.
        sys.exit(1)

    try:
        # --- CORRECTION CRITIQUE ICI ---
        # comment='#' so that Pandas skips the header text
        df = pd.read_csv(DATA_FILE, comment='#')
        
        # Clean the column names (strip invisible whitespace)
        df.columns = df.columns.str.strip()
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Extract the data, with error handling
    try:
        l_modes = df['Multipole_l']
        phase_raw = df['Phase_Alignment_rad']
    except KeyError as e:
        print(f"Erreur de colonne : {e}")
        print(f"Colonnes trouvées : {df.columns.tolist()}")
        return

    phases = []
    for p in phase_raw:
        try:
            # If it is a number, convert it
            phases.append(float(p))
        except:
            # If it is text ("Random"), draw a random angle
            phases.append(np.random.uniform(0, 2*np.pi))
    
    # Polar Plot for Alignment
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    
    # Colours: red for l=2,3 (aligned), grey for the rest
    colors = ['red' if l in [2,3] else 'gray' for l in l_modes]
    sizes = [150 if l in [2,3] else 50 for l in l_modes]
    
    # Plot the points
    ax.scatter(phases, l_modes, c=colors, s=sizes, alpha=0.8, edgecolors='black')
    
    # Plot decoration
    max_l = int(l_modes.max())
    # Concentric circles (yticks) from 2 to max_l
    ax.set_yticks(range(2, max_l + 1))
    ax.set_yticklabels([str(i) for i in range(2, max_l + 1)])
    
    ax.set_title("Illustrative low-$\\ell$ phase alignment (schematic, not Planck data)", fontsize=16, pad=20)
    
    # Zone d'alignement (Secteur rouge)
    # On dessine un secteur angulaire autour de 1.0 rad
    ax.fill_between(np.linspace(0.9, 1.1, 20), 0, max_l, color='red', alpha=0.1, label='Alignment Sector')
    
    # Manual legend, for a cleaner result
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Aligned Modes (l=2,3)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='Random Modes (l>3)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
