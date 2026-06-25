#!/usr/bin/env python3
"""
ECF — plot_CosmicEvolution.py
Referee version: white background, same content, annotated for readability.
Transition Cosmic Discus → Quasi-Sphere with modern anchor point.
ε = (a⊥ − a∥)/a vs log10(t)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from scipy.interpolate import make_interp_spline

BG, RED, WH = 'white', '#c0392b', '#111111'
TXT = '#1f2d3d'

fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
ax.set_facecolor(BG)

log_t = np.array([-44,-42,-40,-38,-36,-34,-30,-25,-20,-15,-11,-8,-5,0,1,13,17.15])
eps   = np.array([0.84,0.83,0.79,0.76,0.70,0.55,0.30,0.18,0.13,0.10,0.075,0.06,0.04,0.02,0.01,0.000030,0.000025])

t_fine = np.linspace(-44, 17.15, 1000)
spl    = make_interp_spline(log_t, eps, k=3)
eps_f  = np.clip(spl(t_fine), 0, 1)

# Background bands indicate the successive cosmological eras.
ax.axvspan(-44,-36, color='#e8b4b8', alpha=0.18)
ax.axvspan(-36,-11, color='#b4c8e8', alpha=0.18)
ax.axvspan(-11, 13, color='#b8e8c4', alpha=0.13)
ax.axvspan( 13,17.5,color='#c8e8b4', alpha=0.13)

# Main red curve: schematic evolution of the ellipticity parameter ε.
ax.plot(t_fine, eps_f, color=RED, linewidth=3.2, zorder=5)
ax.axhline(0, color='#aaaaaa', linewidth=1.2, linestyle='--', alpha=0.5)

key_pts = {
    -44: (0.84, 'Bounce\n"Cosmic Discus"\nΩ/H ≫ 1', (3.0, -0.32)), 
    -11: (0.075,'EW freeze-out\nMicro-Knots',    (2.0, 0.12)),
     13: (0.00008,'Recombination\nToday ε ~ 3×10⁻⁶',(0.5, 0.12)),
}

# Key epochs are annotated to guide the reader through the timeline.
for x,(y,lbl,off) in key_pts.items():
    ax.plot(x, y, 'o', color=RED, markersize=9, zorder=6)
    ax.annotate(lbl, xy=(x,y), xytext=(x+off[0], y+off[1]), color=WH,
                fontsize=9.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=RED, linewidth=1.8),
                arrowprops=dict(arrowstyle='->', color='#666666'))

# Configuration des 4 fenêtres géométriques le long de l'évolution cosmique
# Le 4ème marqueur (Now) intègre la valeur numérique de l'ellipticité demandée
for cx, cy, rx, ry, col, lbl, sub_lbl in [
        (-39, 0.77, 6.0, 0.05, '#e8a0a0', 'Oblate', ''),
        (-20, 0.13, 4.5, 0.09, '#e8a0a0', 'Ellipsoid', ''),
        (  0, 0.02, 3.5, 0.11, '#7ec8e3', 'Quasi-Sphere', ''),
        ( 14.8, 0.000025, 3.2, 0.11, '#2ca02c', 'Now', 'ε ≈ 3×10⁻⁶')]:
    
    ax.add_patch(Ellipse((cx, cy), rx, ry, facecolor='none', edgecolor=col, linewidth=2.5, alpha=0.85, zorder=4))
    
    # Construction du texte avec saut de ligne si une valeur numérique est présente
    label_text = f"{lbl}\n{sub_lbl}" if sub_lbl else lbl
    ax.text(cx, cy + ry/2 + 0.02, label_text, color=TXT, fontsize=9.5, fontweight='bold', ha='center', va='bottom')

for x,lbl in [(-41,'Bounce & Inflation'),(-22,'Radiation'),(6,'Matter'),(15,'Dark Energy')]:
    ax.text(x, 0.95, lbl, color=TXT, fontsize=11, ha='center', alpha=0.75)

ax.set_xticks([-44,-36,-11,-5,0,13,17.15])
ax.set_xticklabels(['-44\nBounce','-36\nInflation','-11\nEW','-5\nQGP','0\n1 s','+13\nRecomb.','Now'],
                    color=WH, fontsize=9.5)
ax.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
ax.set_yticklabels(['0','0.2','0.4','0.6','0.8','1'], color=TXT, fontsize=10)
ax.tick_params(colors=WH)
for sp in ax.spines.values(): sp.set_edgecolor('#444444')
ax.set_xlim(-46, 18); ax.set_ylim(-0.04, 1.05)
ax.set_xlabel('log₁₀ ( t / s )', color=TXT, fontsize=13, labelpad=8)
ax.set_ylabel('Ellipticity ε = (a⊥ − a∥) / a', color=TXT, fontsize=12, labelpad=10)
ax.set_title('ECF — Transition «Cosmic Discus» → Quasi-Sphère\n'
             'F2 | Fig_CosmicEvolution | ε = (a⊥ − a∥)/a vs log₁₀(t)',
             color=TXT, fontsize=13, fontweight='bold', pad=14)

plt.tight_layout()
fig.savefig('Fig_CosmicEvolution.png', dpi=180, bbox_inches='tight', facecolor=BG)
print("Saved: Fig_CosmicEvolution.png")