"""
=============================================================================
[FR] SIMULATION COSMOLOGIQUE ECF : DU "BIG BOUNCE" AUX GALAXIES JWST (z=10)
[EN] ECF COSMOLOGICAL SIMULATION: FROM THE "BIG BOUNCE" TO JWST GALAXIES (z=10)
=============================================================================
Auteur / Author : Pascal Fichant
Papier / Paper  : "Foundation II: The Chiral Universe" (v1.0.5)
=============================================================================
"""

"""
=============================================================================
[FR] SIMULATION COSMOLOGIQUE ECF : DU "BIG BOUNCE" AUX GALAXIES JWST (z=10)
[EN] ECF COSMOLOGICAL SIMULATION: FROM THE "BIG BOUNCE" TO JWST GALAXIES (z=10)
=============================================================================
Auteur / Author : Pascal Fichant
Papier / Paper  : "Foundation II: The Chiral Universe" (v1.0.5)
=============================================================================
"""

import imageio_ffmpeg
import matplotlib as mpl
import os

# Configuration de FFmpeg
mpl.rcParams['animation.ffmpeg_path'] = imageio_ffmpeg.get_ffmpeg_exe()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Ellipse, Circle

# ==========================================
# RÉGLAGES DE LA LANGUE / LANGUAGE SETTINGS
# ==========================================
LANGUE = 'EN'  # USER CHOOSE 'FR' ou 'EN'

TEXTES = {
    'FR': {
        'main_title': "SIMULATION COSMOLOGIQUE ECF",
        'credit': "Paper: Foundation II: The Chiral Universe\nAuthor: Pascal Fichant (Feb 2026)",
        'p1_t': "Phase I : Le Grand Rebond (Disque Cosmique)",
        'p1_i': "Densité de spin extrême, géométrie aplatie par la force centrifuge",
        'p2_t': "Phase II : Ère Rigide & Cristallisation Topologique",
        'p2_i': "Gel des défauts géométriques (Micro-Nœuds solitoniques de Matière Noire)",
        'p3_t': "Phase III : Fusion Hiérarchique & Annihilation",
        'p3_i': "Survie du gaz baryonique. Naissance du Super-Nœud central",
        'p4_t': "Phase IV : La Centrifugeuse Chirale",
        'p4_i': "La torsion géométrique force le gaz en rotation rapide (Lense-Thirring)",
        'p5_t': "Phase V : Allumage de la Graine Lourde (JWST)",
        'p5_i': "Effondrement direct. Apparition d'une galaxie spirale mature",
        'smbh': "Création du Trou Noir Supermassif\n(Spin quasi-maximal) →"
    },
    'EN': {
        'main_title': "ECF COSMOLOGICAL SIMULATION",
        'credit': "Paper: Foundation II: The Chiral Universe\nAuthor: Pascal Fichant (Feb 2026)",
        'p1_t': "Phase I: Big Spin Bounce (Cosmic Discus)",
        'p1_i': "Extreme spin density, geometry flattened by centrifugal forces",
        'p2_t': "Phase II: Stiff Era & Topological Crystallization",
        'p2_i': "Freezing of geometric defects (Solitonic Dark Matter Micro-Knots)",
        'p3_t': "Phase III: Hierarchical Merging & Annihilation",
        'p3_i': "Baryonic gas survives. Birth of the central Super-Knot",
        'p4_t': "Phase IV: The Chiral Centrifuge",
        'p4_i': "Geometric torsion forces primordial gas into rapid rotation (Lense-Thirring)",
        'p5_t': "Phase V: Heavy Seed Ignition (JWST)",
        'p5_i': "Direct monolithic collapse. Emergence of a mature spiral galaxy",
        'smbh': "Supermassive Black Hole Ignition\n(Near-maximal spin) →"
    }
}

T = TEXTES[LANGUE]

# ==========================================
# CONFIGURATION DE LA SCÈNE ET DES TEMPS
# ==========================================
pause_frames = 75 
steps = [100, 250, 400, 500, 600]
n_frames = steps[-1] + (len(steps) * pause_frames)

fig, ax = plt.subplots(figsize=(12, 9), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(-16, 16)
ax.set_ylim(-16, 16)
ax.axis('off')

# Titre Principal Haut
ax.text(0, 15.2, T['main_title'], color='white', fontsize=22, ha='center', va='top', fontweight='bold')

# Crédits Bas Gauche
credit_text = ax.text(-15.5, -14, T['credit'], color='gray', fontsize=10, va='bottom', ha='left', family='monospace')

# HUD de Phase (Haut)
title_text = ax.text(0, 13.2, "", color='white', fontsize=17, ha='center', va='center', fontweight='bold')
info_text = ax.text(0, 11.8, "", color='cyan', fontsize=12, ha='center', va='center', style='italic')

# Redshift Bas Centre
z_text = ax.text(0, -15.5, "", color='lightgray', fontsize=14, ha='center', va='bottom')

# SMBH Bas Droite
smbh_label = ax.text(15.5, -14, "", color='red', fontsize=11, va='bottom', ha='right', fontweight='bold')

# Objets
universe = Ellipse((0,0), width=0, height=0, color='white', alpha=0.9)
ax.add_patch(universe)
knots = ax.scatter([], [], s=15, color='black', zorder=3)
gas = ax.scatter([], [], s=5, color='orange', alpha=0.7, zorder=4)
superknot = Circle((0,0), radius=0, color='black', zorder=5)
ax.add_patch(superknot)
quasar = Circle((0,0), radius=0, color='white', alpha=0.9, zorder=6)
ax.add_patch(quasar)

np.random.seed(42)
n_knots, n_gas = 80, 400
knot_angles, knot_radii = np.random.uniform(0, 2*np.pi, n_knots), np.random.uniform(2, 12, n_knots)
gas_angles, gas_radii = np.random.uniform(0, 2*np.pi, n_gas), np.random.uniform(3, 14, n_gas)

def get_effective_frame(abs_f):
    accum = 0
    for s in steps:
        if abs_f > (s + accum):
            if abs_f < (s + accum + pause_frames): return s - 1 
            accum += pause_frames
        else: break
    return abs_f - accum

def update(absolute_frame):
    frame = get_effective_frame(absolute_frame)
    
    if frame < 250 or frame > 260:
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        title_text.set_color('white')

    # Logique des phases
    if frame < 100:
        prog = frame / 100.0
        universe.set_width(2 + 10 * prog)
        universe.set_height(0.5 + 2 * prog) 
        universe.set_color((1.0, 1.0 - 0.2*prog, 1.0 - 0.2*prog)) 
        knots.set_offsets(np.empty((0, 2)))
        gas.set_offsets(np.empty((0, 2)))
        superknot.set_radius(0)
        quasar.set_radius(0)
        smbh_label.set_text("")
        title_text.set_text(T['p1_t'])
        info_text.set_text(T['p1_i'])
        z_text.set_text("t ~ 10⁻⁴³ s")
        
    elif frame < 250:
        prog = (frame - 100) / 150.0
        universe.set_width(12 + 4 * prog)
        universe.set_height(2.5 + 13.5 * prog) 
        universe.set_color((0.8 - 0.7*prog, 0.8 - 0.7*prog, 0.9)) 
        if frame > 140:
            k_x = knot_radii * np.cos(knot_angles + prog * np.pi)
            k_y = knot_radii * np.sin(knot_angles + prog * np.pi)
            knots.set_offsets(np.c_[k_x, k_y])
        title_text.set_text(T['p2_t'])
        info_text.set_text(T['p2_i'])
        z_text.set_text("t ~ 10⁻³⁵ s")

    elif frame < 400:
        prog = (frame - 250) / 150.0
        if 250 <= frame <= 260:
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            title_text.set_color('black')
        universe.set_color((0.05, 0.05, 0.1)) 
        k_r = knot_radii * (1.0 - prog)
        knots.set_offsets(np.c_[k_r * np.cos(knot_angles + prog * 2*np.pi), k_r * np.sin(knot_angles + prog * 2*np.pi)])
        if frame > 280:
            gas.set_offsets(np.c_[gas_radii * np.cos(gas_angles), gas_radii * np.sin(gas_angles)])
        if frame > 310:
            superknot.set_radius(0.6 * (frame - 310) / 90.0) 
        title_text.set_text(T['p3_t'])
        info_text.set_text(T['p3_i'])
        z_text.set_text("z ≫ 25")

    elif frame < 500:
        prog = (frame - 400) / 100.0
        knots.set_offsets(np.empty((0, 2)))
        superknot.set_radius(0.6)
        g_r = gas_radii * (1.0 - 0.4 * prog)
        g_theta = gas_angles + prog * 8 * np.pi / g_r 
        gas.set_offsets(np.c_[g_r * np.cos(g_theta), g_r * np.sin(g_theta)])
        title_text.set_text(T['p4_t'])
        info_text.set_text(T['p4_i'])
        z_text.set_text("z ~ 30 → 15")

    else:
        prog = (frame - 500) / 100.0
        g_r = gas_radii * 0.6
        g_theta = gas_angles + (1.0 + prog * 2) * 8 * np.pi / g_r
        gas.set_offsets(np.c_[g_r * np.cos(g_theta), g_r * np.sin(g_theta)])
        quasar.set_radius(1.2 * prog)
        if frame > 530:
            smbh_label.set_text(T['smbh'])
        title_text.set_text(T['p5_t'])
        info_text.set_text(T['p5_i'])
        z_text.set_text("z ~ 10")

    return universe, knots, gas, superknot, quasar, title_text, info_text, z_text, smbh_label

# Animation
ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=40, blit=False)

# Sauvegarde sécurisée
nom_fichier = f"ECF_Simulation_v1.4_{LANGUE}.mp4"
try:
    if os.path.exists(nom_fichier): os.remove(nom_fichier) # Supprime si existe déjà
    print(f"Lancement de la génération : {nom_fichier}")
    writer = animation.FFMpegWriter(fps=25, bitrate=5000)
    ani.save(nom_fichier, writer=writer, dpi=180) # Dpi légèrement réduit pour stabilité
    print("Animation terminée avec succès.")
except Exception as e:
    print(f"Erreur lors de la sauvegarde : {e}")