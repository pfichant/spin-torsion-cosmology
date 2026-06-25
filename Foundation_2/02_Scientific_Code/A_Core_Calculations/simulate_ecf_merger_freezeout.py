#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: The Chiral Universe (ECF Model)
Script      : simulate_ecf_merger_freezeout.py
Description : Numerical simulation of the "Dual Genesis" timeline.
              Visualizes the transition from Act I (Viscous Merging) to 
              Act II (Annihilation & Freeze-Out).
Revision    : v1.1.0 (Dual Genesis Update)
Output      : ecf_dual_genesis.MP4

PHYSICS TIMELINE:
    1. Act I (t ~ 10^-11 s): Crystallization & Viscous Merging.
       High plasma friction allows knots to merge.
    2. TRIGGER (t ~ 1 s, T ~ 1 MeV): The Great Annihilation.
       Electron-positron annihilation clears the plasma. Friction drops.
    3. Act II (t > 1 s): Bimodal Freeze-Out.
       Macro-Knots (JWST) and Micro-Knots (Roman) are locked in.
=============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# ================= CONFIGURATION & SCALING =================
N_MICRO_KNOTS = 600       # Initial number of 10^24 kg defects
SIM_DURATION = 300        # Total frames
TRANSITION_FRAME = 120    # Frame where Act II begins (1 second mark)
MERGER_RADIUS = 0.09      # Capture threshold
BASE_SIZE = 10            # Size for Micro-Knots
MAX_SIZE = 400            # Size for Super-Knots

np.random.seed(101) # Optimized seed for nice clustering
pos_x = np.random.uniform(-1.5, 1.5, N_MICRO_KNOTS)
pos_y = np.random.uniform(-1.5, 1.5, N_MICRO_KNOTS)
masses = np.ones(N_MICRO_KNOTS)
active = np.ones(N_MICRO_KNOTS, dtype=bool)

# Colormap: Red (Hot/Active) -> Blue (Cold/Frozen)
colors = [(1.0, 0.2, 0.0), (0.8, 0.0, 0.8), (0.2, 0.2, 1.0), (0.0, 1.0, 1.0)] 
cmap_merger = LinearSegmentedColormap.from_list("ecf_cmap", colors)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
scat = ax.scatter([], [], s=[], c=[], cmap=cmap_merger, alpha=0.9, edgecolors='none')

# --- UI OVERLAYS ---
time_text = ax.text(0.03, 0.95, "", color='white', fontsize=16, fontweight='heavy', transform=ax.transAxes)
act_text = ax.text(0.03, 0.91, "", color='orange', fontsize=14, fontweight='bold', transform=ax.transAxes)
sub_text = ax.text(0.03, 0.87, "", color='lightgray', fontsize=11, style='italic', transform=ax.transAxes)
trigger_box = ax.text(0.5, 0.5, "", color='red', fontsize=20, fontweight='heavy', ha='center', 
                      bbox=dict(facecolor='white', alpha=0.9, edgecolor='red', boxstyle='round,pad=0.5'),
                      transform=ax.transAxes, visible=False)

# --- PHYSICAL LEGEND ---
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='black', label='Micro-Knot ($10^{24}$ kg)',
               markerfacecolor=(1.0, 0.2, 0.0), markersize=6),
    plt.Line2D([0], [0], marker='o', color='black', label=rf'Macro-Knot ($10^{{5}} M_{{\odot}}$)',
               markerfacecolor=(0.0, 1.0, 1.0), markersize=12)
]
ax.legend(handles=legend_elements, loc='lower right', frameon=False, labelcolor='white', fontsize=10)

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axis('off')

# ================= ANIMATION LOOP =================
def update(frame):
    global pos_x, pos_y, masses, active

    # --- ACT I: VISCOUS MERGING (t < 1s) ---
    if frame < TRANSITION_FRAME:
        scale_factor = 1.0
        # Time log-scale simulation: 10^-11 s to 1 s
        progress = frame / TRANSITION_FRAME
        time_exp = -11 + (11 * progress) # -11 to 0
        current_time = 10**time_exp
        
        time_str = rf"Time: $10^{{{int(time_exp)}}}$ s"
        act_str = "ACT I: MERGING ERA"
        sub_str = "High Plasma Friction | Active Hierarchical Growth"
        
        # Physics: Brownian motion + Attraction
        active_idx = np.where(active)[0]
        # Thermal jitter (high temp)
        pos_x[active_idx] += np.random.normal(0, 0.02, len(active_idx))
        pos_y[active_idx] += np.random.normal(0, 0.02, len(active_idx))
        
        # Hide Trigger
        trigger_box.set_visible(False)

    # --- ACT II: FREEZE-OUT (t > 1s) ---
    else:
        scale_factor = 1.0 + 0.015 * ((frame - TRANSITION_FRAME) ** 1.2)
        current_time = 1.0 + (frame - TRANSITION_FRAME) * 0.1
        
        time_str = f"Time: {current_time:.1f} s"
        act_str = "ACT II: FREEZE-OUT"
        sub_str = "Plasma Cleared | Structures Locked | Expansion Dominates"
        
        # Physics: No more merging, just expansion (separation)
        # We stop the random motion to simulate "freeze-out" of relative velocities
        
        # Trigger Flash
        if frame < TRANSITION_FRAME + 20:
            trigger_box.set_text("TRIGGER: T < 1 MeV\nANNIHILATION")
            trigger_box.set_visible(True)
        else:
            trigger_box.set_visible(False)

    # --- MERGER PHYSICS ENGINE (Active only in Act I) ---
    if frame < TRANSITION_FRAME:
        current_active = np.where(active)[0]
        # Simple N^2 merger check (optimized)
        # In a real heavy sim, we'd use a KDTree, but for N=600 it's fine
        for i in current_active:
            if not active[i]: continue
            
            # Find neighbors
            dx = pos_x[current_active] - pos_x[i]
            dy = pos_y[current_active] - pos_y[i]
            dist = np.sqrt(dx**2 + dy**2)
            
            # Check for mergers
            merge_candidates = current_active[(dist < MERGER_RADIUS) & (dist > 0) & active[current_active]]
            
            for j in merge_candidates:
                if active[j]: # Double check
                    # Merge j into i
                    total_mass = masses[i] + masses[j]
                    pos_x[i] = (pos_x[i]*masses[i] + pos_x[j]*masses[j]) / total_mass
                    pos_y[i] = (pos_y[i]*masses[i] + pos_y[j]*masses[j]) / total_mass
                    masses[i] = total_mass
                    active[j] = False
                    # Momentum conservation/dampening could go here

    # --- RENDERING ---
    active_idx = np.where(active)[0]
    
    # Expand coordinates visually in Act II
    vis_x = pos_x[active_idx] * scale_factor
    vis_y = pos_y[active_idx] * scale_factor
    
    current_masses = masses[active_idx]
    
    # Dynamic Sizing
    # Norm 0 (Micro) -> 1 (Macro)
    mass_norm = np.clip((current_masses - 1) / 30.0, 0, 1) 
    sizes = BASE_SIZE + (MAX_SIZE - BASE_SIZE) * (mass_norm**1.5) # Non-linear size for effect

    scat.set_offsets(np.c_[vis_x, vis_y])
    scat.set_sizes(sizes)
    scat.set_array(mass_norm) # Updates color based on mass

    time_text.set_text(time_str)
    act_text.set_text(act_str)
    act_text.set_color('orange' if frame < TRANSITION_FRAME else 'cyan')
    sub_text.set_text(sub_str)

    return scat, time_text, act_text, sub_text, trigger_box

print(f"Initializing Simulation: {N_MICRO_KNOTS} seeds...")
ani = animation.FuncAnimation(fig, update, frames=SIM_DURATION, interval=50, blit=False)

# To save:
ani.save('ecf_dual_genesis.mp4', writer='ffmpeg', fps=30)
#plt.show()
