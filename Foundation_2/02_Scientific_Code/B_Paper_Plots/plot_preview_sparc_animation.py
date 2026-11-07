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
import matplotlib.animation as animation

# ==========================================
# 1. Figure setup (dark mode)
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#0d1117')
fig.subplots_adjust(wspace=0.1)
fig.suptitle('ECF vs Newton : SPARC Kinematic Preview', color='white', fontsize=14, fontweight='bold')

for ax in (ax1, ax2):
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_facecolor('#0d1117')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')

ax1.set_title("Standard Baryonic (Keplerian Falloff)", color='#7ec8e3', fontsize=12)
ax2.set_title("ECF Torsion Halo (Flat Rotation Curve)", color='#e8a07e', fontsize=12)

# ==========================================
# 2. Star generation (spiral structure)
# ==========================================
N = 600
# Radial distribution (avoids the exact centre)
r = np.random.uniform(0.05, 1.0, N)**0.6 * 10
r = np.maximum(r, 0.8)

# Create two initial spiral arms
theta_offset = np.where(np.random.rand(N) > 0.5, 0, np.pi)
# The 1.2 factor sets the initial arm curvature
theta0 = theta_offset + (r * 1.2) + np.random.uniform(-0.25, 0.25, N)

# Initialise the scatter plots
scat1 = ax1.scatter([], [], s=4, c='#7ec8e3', alpha=0.8) # Newton en bleu
scat2 = ax2.scatter([], [], s=4, c='#e8a07e', alpha=0.8) # ECF en orange

def init():
    scat1.set_offsets(np.empty((0, 2)))
    scat2.set_offsets(np.empty((0, 2)))
    return scat1, scat2

# ==========================================
# 3. Time engine (frame updates)
# ==========================================
def update(frame):
    t = frame / 10.0
    
    # --- GALAXIE NEWTON ---
    # V ~ 1/sqrt(r) -> omega = V/r ~ 1/r^1.5
    omega_newton = 8.0 / (r**1.5)
    theta_n = theta0 - omega_newton * t
    xn = r * np.cos(theta_n)
    yn = r * np.sin(theta_n)
    scat1.set_offsets(np.column_stack((xn, yn)))

    # --- GALAXIE ECF ---
    # V = constante -> omega = V/r ~ 1/r
    omega_ecf = 3.5 / r
    theta_e = theta0 - omega_ecf * t
    xe = r * np.cos(theta_e)
    ye = r * np.sin(theta_e)
    scat2.set_offsets(np.column_stack((xe, ye)))
    
    return scat1, scat2

# ==========================================
# 4. Compilation et Sauvegarde
# ==========================================
print("Génération de l'animation en cours (150 frames)...")
ani = animation.FuncAnimation(fig, update, frames=150, init_func=init, blit=True, interval=50)

# Sauvegarde au format GIF
output_file = 'Preview_SPARC_Kinematics.gif'
ani.save(output_file, writer='pillow', fps=24)
print(f"Terminé ! Ouvrez le fichier '{output_file}' pour voir l'aperçu.")