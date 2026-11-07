"""
=============================================================================
ECF COSMOLOGICAL FRAMEWORK - FOUNDATION II (Version 1.0.9)
Script: plot_void_statistics.py
Author: Pascal Fichant
Date: February 2026
=============================================================================

DESCRIPTION:
This script generates a single-panel ILLUSTRATIVE figure: a 2D slice of an
ECF mock galaxy survey (Voronoi-based toy displacement), showing the
top-down filament/void geometry qualitatively.

[22/09/2026, decision N-1] The former right panel is REMOVED. It showed
simulated points labelled "Observations (SDSS BOSS Catalog)" (generated
from the ECF curve itself plus noise), hand-chosen curves and hard-coded
chi2 values (1.14 / 4.82); the mock CSV 'sdss_boss_void_data.csv' is no
longer written. No VSF and no goodness-of-fit statistic are produced here;
the quantitative VSF template is plot_F2_vsf_prediction.py (Fig. M2).

OUTPUTS:
- 'Fig_Void_Statistics.png' (single panel, mock slice, illustrative)
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import pandas as pd

def generate_void_statistics():
    # Set publication formatting
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})
    fig, ax1 = plt.subplots(1, 1, figsize=(7.5, 6), facecolor='white')
    
    # ==========================================
    # PANEL 1: ECF Mock Galaxy Survey (Slice)
    # ==========================================
    np.random.seed(101)
    n_voids = 60
    points = np.random.rand(n_voids, 2)
    vor = Voronoi(points)
    
    n_galaxies = 5000
    gx, gy = np.random.rand(n_galaxies), np.random.rand(n_galaxies)
    
    # Simulate Top-Down baryonic siphoning towards the filaments
    for j in range(n_galaxies):
        dist = np.sqrt((vor.vertices[:, 0] - gx[j])**2 + (vor.vertices[:, 1] - gy[j])**2)
        nearest = np.argmin(dist)
        target_x, target_y = vor.vertices[nearest]
        gx[j] += (target_x - gx[j]) * 0.85 * np.random.uniform(0.5, 1.0)
            
    ax1.set_facecolor('black')
    ax1.scatter(gx, gy, s=1.5, color='cyan', alpha=0.6)
    ax1.set_title("ECF Mock Survey Slice (illustrative, not data)", fontsize=14, fontweight='bold')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlim(0.05, 0.95)
    ax1.set_ylim(0.05, 0.95)

    # [22/09/2026, decision N-1] Former PANEL 2 (VSF with simulated
    # "SDSS BOSS" points, mock CSV export and hard-coded chi2 values)
    # REMOVED. No VSF and no fit statistic are produced by this script.

    # Global Figure Formatting
    plt.suptitle("Large-Scale Structure: ECF mock slice (illustrative)", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('Fig_Void_Statistics.png', dpi=300, bbox_inches='tight')
    print("[SUCCESS] Publication-ready figure generated: Fig_Void_Statistics.png")

if __name__ == "__main__":
    generate_void_statistics()
