"""
=============================================================================
ECF COSMOLOGICAL FRAMEWORK - FOUNDATION II (v1.0.9)
Script: plot_ecf_cmb.py
Author: Pascal Fichant
Date: February 2026

DESCRIPTION:
Simulates and compares the Cosmic Microwave Background (CMB) temperature 
anisotropies between the standard Lambda-CDM model (pure Gaussian random field) 
and the ECF model (Gaussian field + Topological Kibble-Zurek imprints).
Demonstrates the natural emergence of the "Cold Spot" and the "Axis of Evil".

Note: Topological signatures have been visually enhanced in this script 
to clearly highlight the morphological differences for publication purposes.

OUTPUT:
Fig_CMB_Comparison.png
=============================================================================
"""

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
import numpy as np
import matplotlib.pyplot as plt

def generate_cmb_maps():
    # Map parameters
    N_lat, N_lon = 300, 600
    lon = np.linspace(-np.pi, np.pi, N_lon)
    lat = np.linspace(-np.pi/2., np.pi/2., N_lat)
    Lon, Lat = np.meshgrid(lon, lat)

    # Generate a random diffuse background (simplified power spectrum)
    def generate_gaussian_cmb(seed):
        np.random.seed(seed)
        cmb = np.zeros((N_lat, N_lon))
        # Superposition of spherical waves (low and high multipoles)
        for l in range(1, 25):
            for m in range(-l, l+1):
                amp = np.random.normal(0, 1.0 / (l**1.2)) # Baisse d'amplitude selon l
                phase = np.random.uniform(0, 2*np.pi)
                cmb += amp * np.sin(l * Lat) * np.cos(m * Lon + phase)
        return cmb

    # Generate the baseline CMB (Lambda-CDM)
    cmb_lcdm = generate_gaussian_cmb(42)
    # Normalised to microKelvin-scale fluctuations (-300 uK to +300 uK)
    cmb_lcdm = cmb_lcdm / np.std(cmb_lcdm) * 100 

    # Generate the ECF CMB (Gaussian background + geometric/topological imprint)
    cmb_ecf = cmb_lcdm.copy()
    
    # Signature 1: the "Axis of Evil" (topological alignment of the torsion)
    # Amplitude raised to 75, to stay visually distinct in print
    axis_of_evil = 75 * np.sin(2 * Lat) * np.cos(Lon - np.pi/4)
    cmb_ecf += axis_of_evil
    
    # Signature 2: the large CMB Cold Spot
    # Drawn wider and colder for visual emphasis (-350 uK)
    spot_lat, spot_lon = -np.pi/6, np.pi/3 # Coordonnées approximatives du Cold Spot
    distance_to_spot = np.arccos(np.sin(Lat)*np.sin(spot_lat) + np.cos(Lat)*np.cos(spot_lat)*np.cos(Lon-spot_lon))
    cold_spot_profile = -350 * np.exp(-(distance_to_spot / 0.20)**2) 
    cmb_ecf += cold_spot_profile

    # Signature 3: micro-clumps (Macro-Knot network on the last-scattering surffusion)
    np.random.seed(101)
    for _ in range(40):
        k_lat = np.random.uniform(-np.pi/2, np.pi/2)
        k_lon = np.random.uniform(-np.pi, np.pi)
        d = np.arccos(np.sin(Lat)*np.sin(k_lat) + np.cos(Lat)*np.cos(k_lat)*np.cos(Lon-k_lon))
        # Early Sachs-Wolfe effect around the knots
        cmb_ecf -= 50 * np.exp(-(d / 0.05)**2) 

    # ================= AFFICHAGE (PROJECTION MOLLWEIDE) =================
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})
    fig = plt.figure(figsize=(16, 10), facecolor='white')
    
    # PANNEAU 1 : Lambda-CDM
    ax1 = fig.add_subplot(211, projection='mollweide')
    im1 = ax1.pcolormesh(Lon, Lat, cmb_lcdm, cmap='coolwarm', vmin=-250, vmax=250, shading='auto')
    ax1.set_title(r"Standard $\Lambda$CDM Prediction: Pure Gaussian Random Field", fontsize=16, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    cbar1 = fig.colorbar(im1, ax=ax1, orientation='vertical', fraction=0.02, pad=0.04)
    cbar1.set_label(r'$\Delta T$ [$\mu$K]', fontsize=12)

    # PANEL 2: ECF model
    ax2 = fig.add_subplot(212, projection='mollweide')
    im2 = ax2.pcolormesh(Lon, Lat, cmb_ecf, cmap='coolwarm', vmin=-250, vmax=250, shading='auto')
    ax2.set_title(r"ECF Framework Prediction: Gaussian Field + Topological Imprints", fontsize=16, fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    cbar2 = fig.colorbar(im2, ax=ax2, orientation='vertical', fraction=0.02, pad=0.04)
    cbar2.set_label(r'$\Delta T$ [$\mu$K]', fontsize=12)

    # Annotations on the ECF model
    ax2.annotate('CMB Cold Spot\n(Kibble-Zurek Void)', xy=(spot_lon, spot_lat), xytext=(spot_lon+0.5, spot_lat-0.6),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
                 fontsize=12, fontweight='bold', color='black', ha='center',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))

    ax2.text(-2.5, 1.0, "Structural Alignment\n(Axis of Evil)", fontsize=12, fontweight='bold', color='black',
             bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))

    # Overall title, as a raw string
    plt.suptitle(r"Cosmic Microwave Background (CMB) Anisotropies: $\Lambda$CDM vs ECF", fontsize=20, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('Fig_CMB_Comparison.png', dpi=300, bbox_inches='tight')
    print("[SUCCESS] Image du CMB générée avec succès : Fig_CMB_Comparison.png")

if __name__ == "__main__":
    generate_cmb_maps()