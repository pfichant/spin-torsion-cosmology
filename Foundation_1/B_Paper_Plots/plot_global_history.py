# plot_global_history.py
# Author: Pascal Fichant (2026)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter

# --- 1. MODÉLISATION PHYSIQUE ---
def get_a_evolution(t_arr, model='ECF'):
    t_bounce, t_eq, t_today = 1e-35, 1.5e12, 4.35e17
    if model == 'LCDM':
        # Expansion standard
        a = np.where(t_arr < t_eq, (t_arr/t_eq)**0.5, (t_arr/t_eq)**(2/3))
        a_today = (t_today/t_eq)**(2/3)
    else:
        # Modèle ECF (Spin-Torsion)
        a = np.where(t_arr < t_bounce, (t_arr/t_bounce)**(1/3), 
                     np.where(t_arr < t_eq, (t_arr/t_bounce)**0.5, 
                              ((t_eq/t_bounce)**0.5) * (t_arr/t_eq)**(2/3)))
        a_today = ((t_eq/t_bounce)**0.5) * (t_today/t_eq)**(2/3)
    return a / a_today

# --- 2. PRÉPARATION DES DONNÉES (60 ordres de grandeur) ---
time_full = np.logspace(-43, 18.5, 1200) # Extension vers le futur (Énergie Noire)
a_l = get_a_evolution(time_full, 'LCDM')
a_e = get_a_evolution(time_full, 'ECF')
temp_l = 2.725 / a_l
temp_e = 2.725 / a_e

# --- 3. CRÉATION DU GRAPHIQUE ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# TITRE GÉNÉRAL
fig.suptitle(r'Global History from Big Bounce to Dark Energy Era', 
             fontsize=16, fontweight='bold', y=0.95)

# COLORATION DES ÈRES
eras = [
    {'name': 'Spin-Torsion', 'start': 1e-43, 'end': 1e-35, 'color': 'mediumorchid', 'alpha': 0.45},
    {'name': 'Radiation', 'start': 1e-35, 'end': 1.1e13, 'color': 'dodgerblue', 'alpha': 0.3},
    {'name': 'Matter', 'start': 1.1e13, 'end': 3e17, 'color': 'limegreen', 'alpha': 0.2},
    {'name': 'Dark Energy', 'start': 3e17, 'end': 1e19, 'color': 'salmon', 'alpha': 0.3}
]

for era in eras:
    ax1.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'])
    ax2.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'])
    
    # Placement des labels (ajustement pour l'énergie noire à droite)
    if era['name'] != 'Dark Energy':
        mid = np.sqrt(era['start'] * era['end'])
        ax1.text(mid, 1e-31, era['name'], rotation=90, ha='center', va='bottom', 
                 fontsize=11, fontweight='bold')
    else:
        ax1.text(era['start']*2, 1e-31, 'Dark Energy', rotation=90, ha='center', 
                 va='bottom', fontsize=11, fontweight='bold')

# TRACÉ DES COURBES
# Discrimination : Bleu épais pointillé derrière Rouge plein
ax1.loglog(time_full, a_l, color='blue', linestyle='--', linewidth=4, alpha=0.45, label=r'Standard $\Lambda$CDM')
ax1.loglog(time_full, a_e, color='red', linestyle='-', linewidth=2.5, label=r'ECF Model')

ax2.loglog(time_full, temp_l, color='blue', linestyle='--', linewidth=4, alpha=0.45)
ax2.loglog(time_full, temp_e, color='red', linestyle='-', linewidth=2.5)

# AXE X SUPÉRIEUR (Redshift z)
secax1 = ax1.secondary_xaxis('top')
t_ticks = [1e-35, 1e-21, 1e-7, 1.1e13, 3e15, 4.35e17]
z_labels = [r'$10^{32}$', r'$10^{20}$', r'$10^{10}$', '1100', '20', '0']
secax1.set_xticks(t_ticks)
secax1.xaxis.set_major_formatter(FixedFormatter(z_labels))

# Style de l'axe Z
for label in secax1.get_xticklabels():
    label.set_fontweight('bold')
    label.set_color('darkred')
secax1.set_xlabel(r'Redshift ($z$)', fontsize=13, fontweight='bold', color='darkred', labelpad=12)

# ESTHÉTIQUE
ax1.set_ylabel(r'Scale Factor $a(t)$', fontsize=12)
ax2.set_ylabel(r'Temperature $T(t)$ [K]', fontsize=12)
ax2.set_xlabel(r'Cosmic Time $t$ [seconds]', fontsize=12)
ax1.legend(loc='upper left', fontsize=11, framealpha=1)
ax1.set_ylim(1e-35, 100)
ax2.set_ylim(1e-1, 1e33)

plt.tight_layout(rect=[0, 0, 1, 0.93])

# Save the figure
plt.savefig("Figure_global_history.png", dpi=300, bbox_inches='tight')
print(f"Plot generated successfully")

# Display the figure
# plt.show()