# plot__primordial_boost.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

# --- Configuration ---
# Use LaTeX fonts for a professional look matching the paper
# NOTE: If you don't have LaTeX installed on your system, this might cause issues.
# If it fails again, comment out these 3 lines.
try:
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['font.size'] = 14
except Exception as e:
    print(f"Warning: Could not set LaTeX fonts ({e}). Using default fonts.")

# --- Physical Modeling ---
# We model the growth of perturbations delta(a) from z=3000 down to z=1000.
# The scale factor 'a' is linear, representing time.
a_start = 1 / 3001  # z = 3000
a_end = 1 / 1001    # z = 1000
a = np.linspace(a_start, a_end, 500)

# 1. Standard Model (LambdaCDM) - Blue Dashed
# In the radiation era, growth is suppressed due to the Meszaros effect.
# It's modeled here as logarithmic growth, which looks flat on a linear plot.
delta_lcdm = 1 + 0.8 * np.log(a / a_start)

# 2. ECF Model (Spin-Torsion) - Red Solid
# The stiff phase (w=1) allows for linear growth (delta ~ a).
# We calibrate it to start at the same point and reach exactly 1.45x the LCDM value.
delta_lcdm_final = delta_lcdm[-1]
target_delta_ecf_final = delta_lcdm_final * 1.45

# Linear interpolation for the ECF curve
delta_ecf = 1 + (target_delta_ecf_final - 1) * (a - a_start) / (a_end - a_start)

# --- Plotting ---
try:
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define colors
    color_lcdm = '#0077BB' # Blue
    color_ecf = '#CC3311'  # Red

    # 1. Plots (INVERTED STYLES)
    # LambdaCDM: Blue dashed line (Reference)
    # ---> CORRECTION ICI : Ajout du 'r' avant les guillemets
    ax.plot(a, delta_lcdm, color=color_lcdm, linewidth=3, linestyle='--',
            label=r'Standard Model ($\Lambda$CDM)' + '\n(Radiation Stagnation)')

    # ECF: Red solid line (Main Result)
    ax.plot(a, delta_ecf, color=color_ecf, linewidth=3, linestyle='-',
            label='ECF Model (Spin-Torsion)\n(Stiff Phase Boost)')

    # 2. Recombination Area (Visual Guide)
    recomb_a_start = 1 / 1200
    recomb_a_end = a_end
    ax.axvspan(recomb_a_start, recomb_a_end, color='gray', alpha=0.15)
    # ---> CORRECTION ICI AUSSI
    ax.text((recomb_a_start + recomb_a_end)/2, 1.05, r'Recombination Era ($z \approx 1100$)',
            ha='center', va='bottom', color='dimgray', fontsize=12)

    # 3. Annotations & Highlights
    # Start Point
    ax.plot(a_start, 1, 'ko', markersize=8)
    # ---> CORRECTION ICI
    ax.text(a_start * 1.05, 1.02, r'Start ($z \approx 3000$)', ha='left', va='bottom', fontsize=11)

    # Final Boost Arrow & Text
    # The arrow shows the gap between the two curves at the end
    ax.annotate('', xy=(a_end, delta_ecf[-1]), xytext=(a_end, delta_lcdm[-1]),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    # The text emphasizes the factor, colored in red to match the ECF curve
    ax.text(a_end * 0.98, (delta_ecf[-1] + delta_lcdm[-1]) / 2,
            r'$\times 1.45$ Boost', ha='right', va='center', fontsize=14,
            fontweight='bold', color=color_ecf)

    # 4. Axes & Labels
    ax.set_xlabel(r'Scale Factor $a(t)$ (Time $\rightarrow$)', fontsize=16)
    ax.set_ylabel(r'Perturbation Growth $\delta(a) / \delta_{init}$', fontsize=16)
    ax.set_title('The ECF Primordial Boost: Overcoming Radiation Stagnation', fontsize=18, pad=20)

    # 5. Ticks & Grid
    # Add a secondary x-axis on top to show Redshift (z) for context
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    z_ticks = [3000, 2500, 2000, 1500, 1100]
    ax2.set_xticks([1/(z+1) for z in z_ticks])
    ax2.set_xticklabels([f'z={z}' for z in z_ticks], fontsize=11)

    # Final touches
    ax.grid(True, which='major', linestyle=':', alpha=0.6)
    ax.set_ylim(0.9, target_delta_ecf_final * 1.1) # Set y-limits to frame the data tightly
    ax.legend(loc='upper left', fontsize=13, frameon=True, framealpha=0.9)

    # --- Output ---
    # Utilisation de bbox_inches='tight' dans savefig est plus robuste que plt.tight_layout() seul
    output_path = 'figure_primordial_boost.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Figure saved to: {output_path}")
    # plt.show() # Uncomment to view the plot directly

except Exception as e:
    print(f"\nAN ERROR OCCURRED DURING PLOTTING:")
    print(str(e))
    # This helps diagnose if it's a LaTeX font issue vs something else
    if "UserWarning" in str(e) or "findfont" in str(e):
        print("\nTIP: This might be a font issue. Try commenting out the 'plt.rcParams' lines at the top.")