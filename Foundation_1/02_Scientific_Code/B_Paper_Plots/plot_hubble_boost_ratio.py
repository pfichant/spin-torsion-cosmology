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

def plot_hubble_boost():
    print("Calcul du Torsion Boost...")
    
    # --- 1. PARAMÈTRES ---
    # LambdaCDM
    H0_lcdm = 67.4
    Om_lcdm = 0.315
    Or_lcdm = 4.15e-5 / (0.674**2) 
    Ol_lcdm = 1.0 - Om_lcdm - Or_lcdm

    # ECF Model
    H0_ecf = 73.04
    h_ratio = H0_ecf / H0_lcdm # ~1.083
    Om_ecf = 0.315 
    Or_ecf = 4.15e-5 / (0.7304**2) 
    
    # Calibrage Torsion
    z_peak = 7500
    a_peak = 1.0 / (1.0 + z_peak)
    Os0 = 0.093 * Or_ecf * (a_peak**2)
    Ol_ecf = 1.0 - Om_ecf - Or_ecf - Os0

    # --- 2. CALCUL H(z) ---
    z = np.logspace(0, 4.5, 1000) - 1.0
    z[0] = 0 
    a = 1.0 / (1.0 + z)

    E_lcdm = np.sqrt(Or_lcdm*a**(-4) + Om_lcdm*a**(-3) + Ol_lcdm)
    H_lcdm = H0_lcdm * E_lcdm

    E_ecf = np.sqrt(Or_ecf*a**(-4) + Om_ecf*a**(-3) + Ol_ecf + Os0*a**(-6))
    H_ecf = H0_ecf * E_ecf

    ratio = H_ecf / H_lcdm

    # --- 3. FIGURE ---
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Marges manuelles
    plt.subplots_adjust(left=0.12, right=0.95, top=0.92, bottom=0.12)

    # Plot Principal
    x_axis = 1 + z
    ax.semilogx(x_axis, ratio, 'r-', linewidth=3, label=r'Expansion Ratio $H_{ECF} / H_{\Lambda CDM}$')

    # Ligne de référence H0 ratio
    ax.axhline(h_ratio, color='gray', linestyle='--', alpha=0.5, label='Low-z difference (H0 Tension)')
    ax.text(1.5, h_ratio + 0.01, r'Late Time Physics ($H_0$ mismatch)', color='gray', fontsize=10)

    # Zone du "Boost"
    ax.fill_between(x_axis, h_ratio, ratio, where=(x_axis > 1000), color='red', alpha=0.15)
    
    # Annotation Recombinaison
    z_rec = 1100
    ax.axvline(1+z_rec, color='blue', linestyle=':', linewidth=2)
    ax.text(1+z_rec, 1.15, 'Recombination\n(CMB Released)', color='blue', rotation=90, va='bottom', ha='right', fontsize=10)

    # Annotation "The Boost" (Propre, sans code LaTeX parasite)
    ax.annotate('THE TORSION BOOST\n(Reduces $r_s$)', 
                xy=(8000, 1.25), xytext=(200, 1.4),
                arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle="arc3,rad=.2"),
                fontsize=12, fontweight='bold', color='#c0392b', 
                bbox=dict(boxstyle="round", fc="white", ec="red", alpha=0.8))

    # Esthétique
    ax.set_xlabel(r'Redshift ($1+z$)', fontweight='bold')
    ax.set_ylabel(r'Ratio $H(z)_{ECF} \, / \, H(z)_{\Lambda CDM}$', fontweight='bold')
    ax.set_title(r'Mechanism of $r_s$ Reduction: The Hubble Boost', fontsize=16, fontweight='bold', pad=15)
    
    ax.set_xlim(1, 30000)
    ax.set_ylim(1.0, 1.6) 
    ax.grid(True, which='both', linestyle=':', alpha=0.4)
    ax.legend(loc='upper left', frameon=True)

    # Save
    filename = 'Figure_Hubble_Boost_Ratio.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Image générée : {filename}")

if __name__ == "__main__":
    plot_hubble_boost()