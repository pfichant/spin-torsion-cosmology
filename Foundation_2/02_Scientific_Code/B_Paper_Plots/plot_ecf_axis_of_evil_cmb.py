
r"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_ecf_axis_of_evil_cmb.py
Author:        Pascal Fichant
Date:          February 2026 (v1.1 - Post-Review)
Description:   Visualizes the alignment of low-multipole moments (l=2,3)
               compared to higher modes, demonstrating the "Axis of Evil".
Data Source:   Planck 2018 (Commander) + ECF Projection
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
Description:   Visualizes the alignment of low-multipole moments (l=2,3)
               compared to higher modes, demonstrating the "Axis of Evil".
Data Source:   Planck 2018 (Commander) + ECF Projection
Output:        Fig3_Axis_of_Evil_ECF.png
=============================================================================
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

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

OUTPUT_FILE = os.path.join(_FOUNDATION2_DIR, "figures_output", "Fig3_Axis_of_Evil_ECF.png")
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data_S3_CMB_Multipoles.csv not found.")
        print(f"  Expected: {DATA_FILE}")
        print(f"  Fix: copy Data_S3_CMB_Multipoles.csv to:")
        print(f"       {os.path.join(_FOUNDATION2_DIR, 'data')}")
        return

    try:
        # --- CORRECTION CRITIQUE ICI ---
        # On ajoute comment='#' pour que Pandas ignore le texte d'en-tête
        df = pd.read_csv(DATA_FILE, comment='#')
        
        # On nettoie les noms de colonnes (enlève les espaces invisibles)
        df.columns = df.columns.str.strip()
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Extraction des données avec gestion d'erreurs
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
            # Si c'est un nombre, on le convertit
            phases.append(float(p))
        except:
            # Si c'est du texte ("Random"), on génère un angle aléatoire
            phases.append(np.random.uniform(0, 2*np.pi))
    
    # Polar Plot for Alignment
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    
    # Couleurs : Rouge pour l=2,3 (Alignés), Gris pour les autres
    colors = ['red' if l in [2,3] else 'gray' for l in l_modes]
    sizes = [150 if l in [2,3] else 50 for l in l_modes]
    
    # Tracé des points
    ax.scatter(phases, l_modes, c=colors, s=sizes, alpha=0.8, edgecolors='black')
    
    # Décoration du graphe
    max_l = int(l_modes.max())
    # On définit les cercles concentriques (yticks) de 2 à max_l
    ax.set_yticks(range(2, max_l + 1))
    ax.set_yticklabels([str(i) for i in range(2, max_l + 1)])
    
    ax.set_title("CMB Phase Alignment (The Axis of Evil)", fontsize=16, pad=20)
    
    # Zone d'alignement (Secteur rouge)
    # On dessine un secteur angulaire autour de 1.0 rad
    ax.fill_between(np.linspace(0.9, 1.1, 20), 0, max_l, color='red', alpha=0.1, label='Alignment Sector')
    
    # Légende manuelle pour être propre
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
