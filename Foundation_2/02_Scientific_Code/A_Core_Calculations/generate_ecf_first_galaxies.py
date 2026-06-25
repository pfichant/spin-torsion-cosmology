
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script      : generate_ecf_first_galaxies.py
Description : 
    Visualisation de la formation des premières galaxies (Modèle ECF).
    Inclut des commentaires dynamiques affichés à l'écran selon la phase 
    temporelle (Dark Ages, Toile Cosmique, Aube Cosmique).
=============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# ================= CONFIGURATION =================
OUTPUT_DIR = "ecf_first_galaxies_frames"
N_FRAMES = int(os.environ.get('ECF_N_FRAMES', '20'))   # Full run: set ECF_N_FRAMES=100
IMG_SIZE = 800       
GRID_SIZE = 400      

TIME_START_MYR = 100.0  
TIME_END_MYR = 500.0    

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Génération de {N_FRAMES} images dans ./{OUTPUT_DIR}/...")

# Coordonnées et masses des 5 nœuds topologiques invisibles
np.random.seed(42)
knots_x = np.array([0.2, -0.5, 0.6, -0.3, 0.0])
knots_y = np.array([0.3, 0.1, -0.4, -0.6, 0.8])
knots_mass = np.array([1.5, 1.0, 1.2, 0.8, 1.4])

colors = [(0, 0, 0, 1), (0.2, 0, 0.3, 1), (0.6, 0.1, 0.2, 1), (1, 0.6, 0.1, 1), (1, 1, 0.9, 1)]
cmap_cosmic = LinearSegmentedColormap.from_list("cosmic_web", colors, N=256)

x = np.linspace(-1, 1, GRID_SIZE)
y = np.linspace(-1, 1, GRID_SIZE)
X, Y = np.meshgrid(x, y)

# ================= BOUCLE PRINCIPALE =================
for i in range(N_FRAMES):
    progress = i / (N_FRAMES - 1)
    current_time_myr = TIME_START_MYR + progress * (TIME_END_MYR - TIME_START_MYR)
    
    # --- DÉTERMINATION DU COMMENTAIRE DYNAMIQUE (LA PHASE) ---
    if current_time_myr < 250.0:
        phase_title = "Phase 1: The Dark Ages"
        phase_desc = "Diffuse primordial gas permeates the expanding universe."
        desc_color = "lightgray"
    elif current_time_myr < 400.0:
        phase_title = "Phase 2: Cosmic Web Formation"
        phase_desc = "Gas flows into the massive pre-existing topological knots."
        desc_color = "orange"
    else:
        phase_title = "Phase 3: The Cosmic Dawn"
        phase_desc = "Gas ignites at knot centers. First galaxies form rapidly (JWST era)."
        desc_color = "cyan"
    
    # Calcul de la carte de densité du gaz
    base_noise = np.random.normal(0, 0.05 * (1 - progress), (GRID_SIZE, GRID_SIZE))
    density_map = np.zeros((GRID_SIZE, GRID_SIZE)) + base_noise
    
    for k in range(len(knots_x)):
        dx = X - knots_x[k]
        dy = Y - knots_y[k]
        r2 = dx**2 + dy**2
        
        sigma = 0.4 - 0.35 * progress
        intensity = knots_mass[k] * (0.1 + progress**3 * 2.5)
        density_map += intensity * np.exp(-r2 / (2 * sigma**2))
        
        # Formation des filaments
        for j in range(k + 1, len(knots_x)):
            line_dx = knots_x[j] - knots_x[k]
            line_dy = knots_y[j] - knots_y[k]
            line_len2 = line_dx**2 + line_dy**2
            
            t_proj = ((X - knots_x[k]) * line_dx + (Y - knots_y[k]) * line_dy) / (line_len2 + 1e-6)
            t_proj = np.clip(t_proj, 0, 1) 
            proj_x = knots_x[k] + t_proj * line_dx
            proj_y = knots_y[k] + t_proj * line_dy
            
            dist2_to_line = (X - proj_x)**2 + (Y - proj_y)**2
            fil_sigma = 0.08 * (1 - 0.5 * progress)
            fil_intensity = 0.3 * (1 - progress*0.5) 
            
            density_map += fil_intensity * np.exp(-dist2_to_line / (2 * fil_sigma**2))

    density_map = np.clip(density_map, 0, 3.0) / 3.0
    
    # --- AFFICHAGE ---
    fig, ax = plt.subplots(figsize=(IMG_SIZE/100, IMG_SIZE/100), dpi=100)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    ax.imshow(density_map, extent=[-1, 1, -1, 1], origin='lower', cmap=cmap_cosmic)
    
    # --- TEXTES GLOBAUX ---
    time_label = f"Time after Big Bounce: {current_time_myr:.1f} Myr"
    ax.text(-0.95, -0.85, time_label, color='white', fontsize=14, fontweight='bold', zorder=4)
    ax.text(-0.95, 0.90, "ECF Model: First Galaxies Formation", color='lightblue', fontsize=12, fontweight='bold', zorder=4)
    ax.text(-0.95, -0.95, f"Frame: {i+1}/{N_FRAMES}", color='gray', fontsize=10, zorder=4)
    
    # --- COMMENTAIRE DYNAMIQUE (En bas à droite) ---
    ax.text(0.95, -0.85, phase_title, color=desc_color, fontsize=12, fontweight='bold', ha='right', zorder=4)
    ax.text(0.95, -0.92, phase_desc, color='white', fontsize=10, ha='right', zorder=4)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    filename = os.path.join(OUTPUT_DIR, f"frame_{i:03d}.png")
    plt.tight_layout(pad=0)
    plt.savefig(filename, facecolor='black')
    plt.close(fig)
    
    if (i + 1) % 10 == 0:
        print(f"{i + 1}/{N_FRAMES} images générées...")

print(f"\nSuccès ! Les {N_FRAMES} images sont sauvegardées dans '{OUTPUT_DIR}'.")
