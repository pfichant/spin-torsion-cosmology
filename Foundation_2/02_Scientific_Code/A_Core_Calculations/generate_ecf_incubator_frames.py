#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script      : generate_ecf_incubator_frames.py
Author      : Pascal Fichant
Description : 
    Generates an image sequence visualizing the formation of a Population III 
    star at the core of an invisible ECF Topological Knot (10^5 M_sun).
    Includes a cosmic time counter to demonstrate the accelerated star 
    formation predicted by the ECF model (JWST compatibility).
    
    The script simulates:
    1. The gravitational lensing effect of the transparent knot on the starry background.
    2. The gravitational collapse of a primordial gas cloud towards the center.
    3. The compression, heating, and final ignition of the first star.
    
Dependencies: numpy, matplotlib
=============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# ================= CONFIGURATION =================
OUTPUT_DIR = "ecf_incubator_frames"
N_FRAMES = 100       
IMG_SIZE = 800       
N_STARS = 2000       
LENS_STRENGTH = 0.08 

# --- NEW: COSMIC TIME TIMELINE (in Millions of Years after Bounce) ---
TIME_START_MYR = 50.0  # Gas starts falling into the topological knot
TIME_END_MYR = 55.0    # Star ignites (very rapid collapse due to pre-existing well)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Starting generation of {N_FRAMES} frames in ./{OUTPUT_DIR}/...")

def apply_gravitational_lensing(x, y, strength):
    r2 = x**2 + y**2 + 1e-6 
    displacement = strength / np.sqrt(r2)
    x_lensed = x + x * displacement
    y_lensed = y + y * displacement
    return x_lensed, y_lensed

def generate_gas_cloud(grid_size, center_sigma, intensity):
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    R2 = X**2 + Y**2
    Gas = intensity * np.exp(-R2 / (2 * center_sigma**2))
    return Gas

colors = [(0, 0, 0, 0), (0.5, 0, 0, 0.2), (0.8, 0.3, 0, 0.6), (1, 0.8, 0.2, 0.9), (1, 1, 1, 1)]
gas_cmap = LinearSegmentedColormap.from_list("gas_heat", colors, N=256)

np.random.seed(42) 
stars_x_orig = np.random.uniform(-1.5, 1.5, N_STARS)
stars_y_orig = np.random.uniform(-1.5, 1.5, N_STARS)
stars_sizes = np.random.uniform(0.5, 4.0, N_STARS) 

stars_x_lensed, stars_y_lensed = apply_gravitational_lensing(stars_x_orig, stars_y_orig, LENS_STRENGTH)

# ================= MAIN ANIMATION LOOP =================
for i in range(N_FRAMES):
    progress = i / (N_FRAMES - 1)
    
    # Calculate current cosmic time based on progress
    current_time_myr = TIME_START_MYR + progress * (TIME_END_MYR - TIME_START_MYR)
    
    fig, ax = plt.subplots(figsize=(IMG_SIZE/100, IMG_SIZE/100), dpi=100)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    ax.scatter(stars_x_lensed, stars_y_lensed, s=stars_sizes, color='white', alpha=0.7, edgecolors='none', zorder=1)
    
    current_sigma = 0.6 * (1.0 - 0.96 * progress)
    current_intensity = 0.2 + 0.8 * (progress**2) 
    Gas = generate_gas_cloud(300, current_sigma, current_intensity)
    ax.imshow(Gas, extent=[-1, 1, -1, 1], origin='lower', cmap=gas_cmap, alpha=0.9, zorder=2)
    
    if progress > 0.9:
        ignition_stage = (progress - 0.9) / 0.1 
        flash_size = ignition_stage * 150
        ax.scatter([0], [0], s=flash_size, color='white', edgecolors='yellow', linewidth=2, zorder=3)
        ax.text(0, 0.8, "Pop III Star Ignition!", color='white', fontsize=14, ha='center', fontweight='bold', zorder=4)

    # --- NEW: DISPLAY THE COSMIC TIME ON SCREEN ---
    #time_label = f"Cosmic Time: {current_time_myr:.2f} Myr"
    time_label = f"Time after Bounce: {current_time_myr:.2f} Myr"
    ax.text(-0.95, -0.85, time_label, color='white', fontsize=12, fontweight='bold', zorder=4)
    
    ax.text(-0.95, -0.95, f"Frame: {i+1}/{N_FRAMES}", color='gray', fontsize=10, zorder=4)
    ax.text(-0.95, 0.90, "ECF Model: Topological Knot\nGravitational Incubator", color='lightblue', fontsize=12, zorder=4)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    filename = os.path.join(OUTPUT_DIR, f"frame_{i:03d}.png")
    plt.tight_layout(pad=0)
    plt.savefig(filename, facecolor='black')
    plt.close(fig)
    
    if (i + 1) % 10 == 0:
        print(f"Generated {i + 1}/{N_FRAMES} frames...")

print(f"\nSuccess! All {N_FRAMES} frames have been saved in the '{OUTPUT_DIR}' directory.")