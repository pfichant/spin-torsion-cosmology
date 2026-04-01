#plot_cosmic_history.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib

# Configuration Backend
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})

def plot_cosmic_history():
    # --- 1. PARAMÈTRES PHYSIQUES (Identique) ---
    a = np.logspace(-6, 0, 1000)
    z = (1.0 / a) - 1.0
    
    Om0 = 0.315    
    Or0 = 9e-5     
    OL0 = 1.0 - Om0 - Or0 
    
    # Calibrage Torsion
    z_peak = 7500
    a_peak = 1.0 / (1.0 + z_peak)
    Os0 = 0.093 * Or0 * (a_peak**2)
    
    # Évolution
    rho_r = Or0 * a**(-4)
    rho_m = Om0 * a**(-3)
    rho_L = OL0 * a**(0)    
    rho_s = Os0 * a**(-6)   
    
    rho_tot = rho_r + rho_m + rho_L + rho_s
    
    Omega_r = rho_r / rho_tot
    Omega_m = rho_m / rho_tot
    Omega_L = rho_L / rho_tot
    Omega_s = rho_s / rho_tot
    Omega_k = 1.0 - (Omega_r + Omega_m + Omega_L + Omega_s)

    # --- 2. CRÉATION FIGURE (CORRIGÉE) ---
    # On ajoute constrained_layout=True pour mieux gérer les marges complexes
    fig = plt.figure(figsize=(12, 10)) 
    
    # Ajustement manuel des marges pour laisser la place aux labels
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25)
    
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    
    # --- PANNEAU DU HAUT ---
    ax1 = plt.subplot(gs[0])
    ax1.plot(a, Omega_r, color='#e67e22', linestyle='--', linewidth=2.5, label=r'Radiation ($\Omega_r$)')
    ax1.plot(a, Omega_m, color='#2ecc71', linewidth=2.5, label=r'Matter ($\Omega_m$)')
    ax1.plot(a, Omega_L, color='#3498db', linewidth=2.5, label=r'Dark Energy ($\Omega_\Lambda$)')
    ax1.plot(a, Omega_s, color='#e74c3c', linewidth=3.5, label=r'Torsion ($\Omega_{spin}$)')
    
    ax1.fill_between(a, 0, Omega_s, color='#e74c3c', alpha=0.3)
    
    # Annotations simplifiées pour lisibilité
    ax1.text(3e-6, 0.5, 'Torsion\nDominated', color='#c0392b', fontsize=10, ha='center', fontweight='bold')
    ax1.text(1e-4, 0.8, 'Radiation', color='#d35400', fontsize=10, ha='center')
    ax1.text(1e-1, 0.8, 'Matter', color='#27ae60', fontsize=10, ha='center')
    ax1.text(0.7, 0.8, 'DE', color='#2980b9', fontsize=10, ha='center')
    
    ax1.set_xscale('log')
    ax1.set_ylabel(r'Density Parameter $\Omega_i(a)$', fontweight='bold')
    ax1.set_ylim(0, 1.1)
    ax1.set_xlim(1e-6, 1)
    ax1.grid(True, which='both', linestyle=':', alpha=0.4)
    ax1.legend(loc='center right', framealpha=0.9, fancybox=True, shadow=True)
    ax1.set_xticklabels([]) 
    ax1.set_title('Cosmic History: Evolution of Density Parameters', fontsize=18, fontweight='bold', pad=15)

    # --- PANNEAU DU BAS ---
    ax2 = plt.subplot(gs[1])
    ax2.plot(a, Omega_k, color='purple', linewidth=2, label=r'Curvature $\Omega_k$')
    ax2.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    ax2.set_xscale('log')
    ax2.set_xlim(1e-6, 1)
    ax2.set_ylim(-0.05, 0.05)
    ax2.set_ylabel(r'$\Omega_k$', fontweight='bold')
    ax2.set_xlabel(r'Scale Factor $a = (1+z)^{-1}$', fontweight='bold')
    ax2.grid(True, which='both', linestyle=':', alpha=0.4)
    ax2.legend(loc='upper right', fontsize=10)
    
    # Axe Redshift (La source du warning précédent)
    ax2_top = ax2.twiny()
    ax2_top.set_xlim(ax2.get_xlim())
    ax2_top.set_xscale('log')
    z_ticks = [10000, 1000, 10, 0]
    z_tick_locs = [1.0/(1+z) for z in z_ticks]
    z_tick_labels = [f'z={z}' for z in z_ticks]
    ax2_top.set_xticks(z_tick_locs)
    ax2_top.set_xticklabels(z_tick_labels, fontsize=10)

    # --- SAUVEGARDE SANS TIGHT_LAYOUT ---
    # On utilise bbox_inches='tight' ici au lieu de plt.tight_layout() avant
    filename = 'Figure_Cosmic_History_Omegas.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved: {filename}")

if __name__ == "__main__":
    plot_cosmic_history()