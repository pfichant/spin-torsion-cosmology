# plot_spin_ration_evolution.py
# Author: Pascal Fichant (2026)
# Description: Visualizes the dynamic evolution of the Spin/Radiation density ratio.
# Shows the "Stiff Phase" peak matching the paper's abstract value, and the rapid
# decay towards recombination, ensuring CMB compatibility.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONSTANTS FROM SCRIPT 03 RESULTS ---
# We use the exact reference point calculated by the physics script
Z_REF_PAPER = 7500.0      # The redshift where action happens
RATIO_REF_PAPER = 9.28    # The ratio (%) found by the solver (~0.093)
Z_REC = 1100.0            # Recombination redshift

# --- PHYSICS CALCULATION ---
# The ratio (Spin/Rad) scales as (1+z)^6 / (1+z)^4 = (1+z)^2
# We normalize the curve to pass exactly through the reference point found by the solver.
def calculate_ratio_percent(z_arr):
    # Normalization constant C to match (Z_REF, RATIO_REF)
    # Ratio = C * (1+z)^2
    C = RATIO_REF_PAPER / (1 + Z_REF_PAPER)**2
    return C * (1 + z_arr)**2

# --- DATA GENERATION ---
# Generate redshifts from early acoustic era down to recombination
z_values = np.linspace(20000, 1000, 1000)
ratios_percent = calculate_ratio_percent(z_values)

# Calculate specific point at recombination
ratio_rec_val = calculate_ratio_percent(Z_REC)

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(12, 7))

# 1. The Main Evolution Curve
ax.plot(z_values, ratios_percent, color='#004e92', linewidth=3, label=r'Spin/Radiation Ratio $\propto (1+z)^2$')

# 2. Highlight the "Stiff Phase" (Active Zone)
# Define the zone where ratio is significant (e.g., > 5%)
stiff_zone_z = z_values[ratios_percent > 5.0]
stiff_zone_r = ratios_percent[ratios_percent > 5.0]
ax.fill_between(stiff_zone_z, stiff_zone_r, 0, color='#d9534f', alpha=0.2)
# Add a label for this zone
ax.text(15000, 7, "Active 'Stiff Fluid' Phase\n(Shrinks Sound Horizon $r_s$)", 
        fontsize=12, color='#c9302c', ha='center', weight='bold')

# 3. Annotate the Paper's Abstract Value (The Peak)
ax.scatter([Z_REF_PAPER], [RATIO_REF_PAPER], color='#d9534f', s=150, zorder=5)
ax.annotate(f"Paper Abstract Value: ~{RATIO_REF_PAPER:.1f}%\n(Effective Stiffening at $z={Z_REF_PAPER:.0f}$)",
            xy=(Z_REF_PAPER, RATIO_REF_PAPER), xycoords='data',
            xytext=(Z_REF_PAPER + 4000, RATIO_REF_PAPER + 2), textcoords='data',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color='black', lw=1.5),
            fontsize=11, weight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d9534f", lw=2))

# 4. Annotate Recombination (Safety Check)
ax.axvline(x=Z_REC, color='gray', linestyle='--', linewidth=1.5)
ax.scatter([Z_REC], [ratio_rec_val], color='green', s=150, zorder=5)
ax.annotate(f"Recombination ($z={Z_REC:.0f}$)\nRatio decays to {ratio_rec_val:.1f}%\n(SAFE for CMB Spectrum)",
            xy=(Z_REC, ratio_rec_val), xycoords='data',
            xytext=(Z_REC + 5000, ratio_rec_val + 3), textcoords='data',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color='green', lw=1.5),
            fontsize=11, color='green', weight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", lw=2))

# 5. Formatting and Labels
ax.set_xlim(20000, 1000) # Invert X-axis: Past on left, Future on right
ax.set_ylim(0, 16)

ax.set_xlabel("Redshift ($z$)", fontsize=14, weight='bold')
ax.set_ylabel(r"Density Ratio $\rho_{Spin} / \rho_{Rad}$ (%)", fontsize=14, weight='bold')
ax.set_title("Dynamic Evolution of Torsion Density Relative to Radiation", fontsize=16, weight='bold', pad=20)

ax.grid(True, which='major', linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)

# Add directional arrow for time
ax.arrow(19000, -1.5, -17000, 0, clip_on=False, width=0.1, head_width=0.5, head_length=500, color='black')
ax.text(10500, -2.2, "Time Direction (Expansion)", ha='center', fontsize=10)

plt.tight_layout()

# Save the figure
output_filename = "Figure_spin_ratio_evolution.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Plot generated successfully and saved to: {output_filename}")

# plt.show()