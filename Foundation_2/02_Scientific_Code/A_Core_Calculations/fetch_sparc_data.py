#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
FILENAME       : fetch_sparc_data.py
DESCRIPTION    : Downloads official SPARC rotation curves (Reliable Mirror).
                 Computes Vbar and saves to CSV.
TARGETS        : 10 Representative Galaxies (Clean Sample).
=============================================================================
"""

import os
import requests
import zipfile
import io
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
# URL stable (Zenodo) pour éviter les blocages serveurs
SPARC_ZIP_URL = "https://zenodo.org/records/16284118/files/Rotmod_LTG.zip"
OUTPUT_DIR = "data"

# LISTE NETTOYÉE (10 Galaxies, sans UGC 2885)
TARGET_GALAXIES = [
    "NGC6503", "NGC3198", "NGC2403", "NGC2841", "NGC2903", 
    "NGC3521", "NGC5055", "NGC7331", "DDO154", "NGC7814"
]

# Standards M/L
ML_DISK = 0.5   
ML_BULGE = 0.7  

def fetch_and_process_sparc():
    print(f"[INFO] Connexion au serveur de données ({SPARC_ZIP_URL})...")
    
    # Header pour éviter le blocage 403/10061
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        r = requests.get(SPARC_ZIP_URL, headers=headers, timeout=30)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("[OK] Archive téléchargée.")
    except Exception as e:
        print(f"[ERREUR] Impossible de télécharger : {e}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"[INFO] Traitement de l'échantillon propre ({len(TARGET_GALAXIES)} galaxies)...")
    
    count = 0
    for filename in z.namelist():
        base_name = os.path.basename(filename).split('_')[0]
        
        if base_name in TARGET_GALAXIES:
            with z.open(filename) as f:
                try:
                    df = pd.read_csv(f, sep=r'\s+', names=[
                        'Rad', 'Vobs', 'Verr', 'Vgas', 'Vdisk', 'Vbulge'
                    ], usecols=[0, 1, 2, 3, 4, 5], comment='#')
                except:
                    continue

            # Calcul V_bar
            v_gas_sq = np.abs(df['Vgas']) * df['Vgas']
            v_disk_sq = df['Vdisk']**2 * ML_DISK
            v_bulge_sq = df['Vbulge']**2 * ML_BULGE
            
            v_bar_sq = (v_gas_sq + v_disk_sq + v_bulge_sq).clip(lower=0)
            df['Vbar'] = np.sqrt(v_bar_sq)

            # Formatage Nom
            if base_name.startswith("NGC") or base_name.startswith("DDO"):
                formatted_name = base_name[:3] + " " + base_name[3:]
            else:
                formatted_name = base_name

            # Sauvegarde
            out_path = os.path.join(OUTPUT_DIR, f"{formatted_name}.csv")
            final_df = df[['Rad', 'Vobs', 'Verr', 'Vbar']]
            final_df.columns = ['Radius', 'Vobs', 'Verr', 'Vbar']
            
            final_df.to_csv(out_path, index=False)
            print(f"  -> {formatted_name}.csv généré")
            count += 1

    print("-" * 50)
    print(f"[SUCCÈS] {count} fichiers prêts dans '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    fetch_and_process_sparc()
