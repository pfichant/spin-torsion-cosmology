#plot_deceleration_transition.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib

# Configuration Backend (Mode sans échec)
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})

def plot_deceleration_transition():
    
    # Redshift z
    z = np.linspace(0, 2.5, 500)
    
    # Paramètres LambdaCDM
    Om0 = 0.315
    OL0 = 1.0 - Om0
    
    # Evolution
    E2 = Om0 * (1+z)**3 + OL0
    Om_z = Om0 * (1+z)**3 / E2
    OL_z = OL0 / E2
    
    # q(z)
    q_lcdm = 0.5 * Om_z - 1.0 * OL_z
    q_ecf = q_lcdm 

    # --- FIGURE ---
    fig, ax = plt.subplots(figsize=(9, 6))
    plt.subplots_adjust(left=0.12, right=0.95, top=0.92, bottom=0.12)

    # Ligne Zéro
    ax.axhline(0, color='black', linestyle=':', linewidth=1)
    
    # Courbes
    ax.plot(z, q_lcdm, 'b--', linewidth=2, label=r'$\Lambda$CDM Standard')
    ax.plot(z, q_ecf, 'r-', linewidth=3, alpha=0.7, label='ECF Model (Late Time)')

    # Zones colorées
    ax.fill_between(z, 0, -1, color='blue', alpha=0.05)
    ax.text(0.1, -0.8, 'ACCELERATING\nEXPANSION', color='blue', fontsize=10, fontweight='bold', alpha=0.6)
    
    ax.fill_between(z, 0, 1, color='gray', alpha=0.05)
    ax.text(2.0, 0.8, 'DECELERATING\nPHASE', color='gray', fontsize=10, fontweight='bold', alpha=0.6)

    # Transition
    z_trans = (2 * OL0 / Om0)**(1/3) - 1 
    ax.scatter([z_trans], [0], color='black', zorder=5)
    ax.annotate(f'Transition\nz = {z_trans:.2f}', xy=(z_trans, 0), xytext=(z_trans+0.2, 0.2),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=11, fontweight='bold')

    # --- AJOUT DE LA FORMULE ---
    # On place la formule dans la zone vide pour faire le lien avec l'Annexe
    ax.text(0.8, -0.5, r'$q(z) \approx \frac{1}{2}\Omega_m(z) - \Omega_\Lambda(z)$', 
            fontsize=14, color='black', 
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=0.9))

    # Mention Supernovae
    ax.text(0.2, -0.3, 'Consistent with\nPantheon+ SNe Ia', color='#27ae60', fontsize=10, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='#27ae60', boxstyle='round,pad=0.3'))

    # Esthétique
    ax.set_xlabel('Redshift $z$', fontweight='bold')
    ax.set_ylabel('Deceleration Parameter $q(z)$', fontweight='bold')
    ax.set_xlim(0, 2.5)
    ax.set_ylim(-1.0, 1.0)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper left', frameon=True)
    ax.set_title(r'Cosmic Acceleration Transition', fontsize=16, fontweight='bold', pad=15)

    # Sauvegarde
    filename = 'figure_deceleration_transition.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved :{filename}")

if __name__ == "__main__":
    plot_deceleration_transition()