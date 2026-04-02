# plot_structure_zoom.py
# Author: Pascal Fichant (2026)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter

# --- 1. MODÉLISATION PHYSIQUE ---
def get_a_evolution(t_arr, model='ECF'):
    t_bounce, t_eq, t_today = 1e-35, 1.5e12, 4.35e17
    if model == 'LCDM':
        # Expansion standard LambdaCDM
        a = np.where(t_arr < t_eq, (t_arr/t_eq)**0.5, (t_arr/t_eq)**(2/3))
        a_today = (t_today/t_eq)**(2/3)
    else:
        # Modèle ECF (Spin-Torsion) : a ~ t^(1/3) après le rebond
        a = np.where(t_arr < t_bounce, (t_arr/t_bounce)**(1/3), 
                     np.where(t_arr < t_eq, (t_arr/t_bounce)**0.5, 
                              ((t_eq/t_bounce)**0.5) * (t_arr/t_eq)**(2/3)))
        a_today = ((t_eq/t_bounce)**0.5) * (t_today/t_eq)**(2/3)
    return a / a_today

# --- 2. PRÉPARATION DES DONNÉES (Zoom sur les structures + Énergie Noire) ---
time_zoom = np.logspace(11, 18.3, 1000)
a_l_z = get_a_evolution(time_zoom, 'LCDM')
a_e_z = get_a_evolution(time_zoom, 'ECF')
temp_l_z = 2.725 / a_l_z
temp_e_z = 2.725 / a_e_z

# --- 3. CRÉATION DU GRAPHIQUE ---
fig, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# TITRE GÉNÉRAL DE LA FIGURE
fig.suptitle(r'Detailed Chronology of Structure Formation & Dark Energy Onset', 
             fontsize=16, fontweight='bold', y=0.95)

# ÈRES COSMOLOGIQUES ET COLORATION
eras_z = [
    {'name': 'Dark Ages', 'start': 1e11, 'end': 1e15, 'color': 'limegreen', 'alpha': 0.3},
    {'name': 'Structure Formation', 'start': 1e15, 'end': 3e17, 'color': 'darkorange', 'alpha': 0.4},
    {'name': 'Dark Energy Era', 'start': 3e17, 'end': 1e19, 'color': 'salmon', 'alpha': 0.35}
]

for era in eras_z:
    ax3.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'])
    ax4.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'])
    
    # Placement intelligent du texte des ères
    if era['name'] == 'Dark Energy Era':
        ax3.text(era['start']*1.5, 5e-3, era['name'], ha='center', va='bottom', fontsize=13, fontweight='bold', color='darkslategray')
    else:
        mid = np.sqrt(era['start'] * era['end'])
        ax3.text(mid, 5e-3, era['name'], ha='center', va='bottom', fontsize=13, fontweight='bold', color='darkslategray')

# TRACÉ DES COURBES (Épaisseurs affinées)
# Courbe bleue (LCDM) : Pointillé plus fin (linewidth=4 au lieu de 10)
ax3.loglog(time_zoom, a_l_z, color='blue', linestyle='--', linewidth=4, alpha=0.5, label=r'Standard $\Lambda$CDM')
ax3.loglog(time_zoom, a_e_z, color='red', linestyle='-', linewidth=2.5, label=r'ECF Prediction')

ax4.loglog(time_zoom, temp_l_z, color='blue', linestyle='--', linewidth=4, alpha=0.5)
ax4.loglog(time_zoom, temp_e_z, color='red', linestyle='-', linewidth=2.5)

# JALONS (Pivots temporels)
pivots = {
    'Recombination': 1.1e13, 
    'Cosmic Dawn': 3e15, 
    'Galaxy Assembly': 2e16, 
    'Today (z=0)': 4.35e17
}

for name, tp in pivots.items():
    ax3.axvline(tp, color='black', linewidth=1.5, linestyle=':')
    ax3.text(tp, 2e-2, f' {name}', rotation=90, va='bottom', fontsize=11, fontweight='bold')

# AXE X SUPÉRIEUR (Redshift z)
secax3 = ax3.secondary_xaxis('top')
t_ticks_z = [1.1e13, 1e14, 3e15, 2e16, 4.35e17]
z_labels_z = ['1100', '150', '20', '3', '0']
secax3.set_xticks(t_ticks_z)
secax3.xaxis.set_major_formatter(FixedFormatter(z_labels_z))

# Style de l'axe Z (Unité et étiquettes)
for label in secax3.get_xticklabels():
    label.set_fontweight('bold')
    label.set_color('darkred')
secax3.set_xlabel(r'Redshift ($z$)', fontsize=13, fontweight='bold', color='darkred', labelpad=12)

# ESTHÉTIQUE FINALE
ax3.set_ylabel(r'Scale Factor $a(t)$', fontsize=12)
ax4.set_ylabel(r'Temperature $T(t)$ [K]', fontsize=12)
ax4.set_xlabel(r'Cosmic Time $t$ [seconds]', fontsize=12)
ax3.legend(loc='lower right', fontsize=12, framealpha=1)

# Limites pour bien voir l'accélération à la fin
ax3.set_ylim(1e-4, 5) 
ax4.set_ylim(1, 1e5)

plt.tight_layout(rect=[0, 0, 1, 0.93]) 
plt.savefig('Figure_Structure_Zoom.png', dpi=300)
# plt.show()