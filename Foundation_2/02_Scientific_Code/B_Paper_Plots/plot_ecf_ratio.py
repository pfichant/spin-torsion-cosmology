import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# ECF FRAMEWORK: THERMODYNAMIC EVOLUTION OF THE COSMIC MASS RATIO (ZONED)
# =============================================================================

# --- 1. Constants and Time Array (in SECONDS) ---
sec_per_year = 3.154e7
t_start_sec = 1e-11 # Topological Freeze-Out (Electroweak)
t_end_sec = 13.4e9 * sec_per_year # ECF Present Epoch (13.4 Gyr)

# Logarithmic time array strictly originating at the freeze-out event
t_sec = np.logspace(np.log10(t_start_sec), np.log10(t_end_sec), 3000)
log_t = np.log10(t_sec)

# Sigmoid function for smooth phenomenological phase transitions
def sigmoid(x, x0, k):
    return 1 / (1 + np.exp(-k * (x - x0)))

# --- 2. Phenomenological Evolution Model ---
log_t_primordial = 0.0 # Annihilation peak around 1 second (log10(1)=0)

# Dark Matter (DM) Evolution:
M_DM = 5.0 - 0.5 * sigmoid(log_t, log_t_primordial, 2.0) - 0.05 * sigmoid(log_t, 16.0, 1.5)

# Baryonic Matter (BM) Evolution:
drop_prim_bm = 1.0 - (4.5 / 5.4) # approx 16.67%
drop_sec_bm = 0.03
M_BM = 1.0 - drop_prim_bm * sigmoid(log_t, log_t_primordial, 2.0) - drop_sec_bm * sigmoid(log_t, 16.0, 1.5)

# Cosmic Mass Ratio R(t)
Ratio = M_DM / M_BM

# --- 3. Plotting the Data ---
fig, ax1 = plt.subplots(figsize=(12, 7))

color_dm = '#1f77b4' # Blue
color_bm = '#d62728' # Red
color_ratio = '#2ca02c' # Green

# Left Y-axis (Masses)
ax1.set_xlabel('Cosmic Time (Seconds) - Log Scale', fontsize=12, fontweight='bold')
ax1.set_ylabel('Relative Mass (Fraction of initial baryonic mass)', fontsize=12, fontweight='bold')
ax1.set_xscale('log')
ax1.set_xlim(left=t_start_sec, right=t_end_sec) 

# =============================================================================
# --- ADDING BACKGROUND ZONES (COSMIC ERAS) ---
# =============================================================================
t_1_sec = 1.0 # 1 second
t_cmb_sec = 365000 * sec_per_year # Recombination Epoch

# Zone 1: Primordial Annihilation Epoch (Hot & Dense)
ax1.axvspan(t_start_sec, t_1_sec, color='orange', alpha=0.15)
ax1.text(np.sqrt(t_start_sec * t_1_sec), 5.3, 'Primordial Annihilation\nEpoch (PTA)', 
         color='darkorange', fontsize=10, ha='center', va='center', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

# Zone 2: Cosmic Expansion & Cooling (Dark Ages / Flat ratio)
ax1.axvspan(t_1_sec, t_cmb_sec, color='cyan', alpha=0.1)
ax1.text(np.sqrt(t_1_sec * t_cmb_sec), 5.3, 'Cosmic Expansion\n& Cooling', 
         color='teal', fontsize=10, ha='center', va='center', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

# Zone 3: Structure Formation & Secular Annihilation
ax1.axvspan(t_cmb_sec, t_end_sec, color='purple', alpha=0.1)
ax1.text(np.sqrt(t_cmb_sec * t_end_sec), 5.3, 'Structure Formation\n& Secular Annihilation', 
         color='purple', fontsize=10, ha='center', va='center', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))
# =============================================================================

# Plotting the mass curves
line1 = ax1.plot(t_sec, M_DM, color=color_dm, linewidth=2.5, label='Topological Dark Matter ($M_{DM}$)')
line2 = ax1.plot(t_sec, M_BM, color=color_bm, linewidth=2.5, label='Baryonic Matter ($M_{BM}$)')
ax1.set_ylim(0, 5.5)

# Right Y-axis (Ratio)
ax2 = ax1.twinx()
ax2.set_ylabel('Mass Ratio ($R = M_{DM}/M_{BM}$)', color=color_ratio, fontsize=12, fontweight='bold')
line3 = ax2.plot(t_sec, Ratio, color=color_ratio, linewidth=4.0, linestyle='-', label='Evolution Ratio $R(t)$')
ax2.tick_params(axis='y', labelcolor=color_ratio)
ax2.set_ylim(4.5, 5.8)

# --- 4. Annotating Key Epochs ---
# A. Topological Freeze-Out (Electroweak)
ax2.axvline(x=t_start_sec, color='black', linestyle='--', linewidth=1.5)
ax2.scatter(t_start_sec, 5.0, color=color_ratio, s=80, zorder=5)
ax2.text(t_start_sec * 3, 4.6, ' Topological Freeze-Out\n ($t=10^{-11}$ s)\n Ratio = 5.0', fontsize=10)

# B. Recombination (CMB)
ax2.axvline(x=t_cmb_sec, color='black', linestyle='--', linewidth=1.5)
ax2.scatter(t_cmb_sec, 5.4, color=color_ratio, s=80, zorder=5)
ax2.text(t_cmb_sec * 2, 4.9, ' Recombination (CMB)\n ($t=365,000$ yr)\n Ratio = 5.4', fontsize=10)

# C. Present Epoch
r_now = Ratio[-1]
ax2.axvline(x=t_end_sec, color='black', linestyle='--', linewidth=1.5)
ax2.scatter(t_end_sec, r_now, color=color_ratio, s=80, zorder=5)
# Moved label slightly to fit within the boundaries
ax2.text(t_end_sec * 0.0001, r_now + 0.1, f' Present Epoch\n ($t=13.4$ Gyr)\n Ratio $\\approx$ {r_now:.2f}', fontsize=10, fontweight='bold')

# Legends
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center left', fontsize=11, framealpha=0.9)

plt.title('Secular Thermodynamic Evolution of Cosmic Masses with Era Zoning (ECF)', fontsize=14, fontweight='bold')
plt.tight_layout()

# Save for LaTeX compilation (PDF is required for high quality vector graphics)
plt.savefig('Fig_ECF_Ratio_Evolution.png', dpi=300, bbox_inches='tight')
# plt.show()
