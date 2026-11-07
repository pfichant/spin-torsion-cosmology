#!/usr/bin/env python3
"""
plot_F2_magnetic_fields.py
===========================
Foundation II — F2 PREPRINT v2 (work in progress)
Zenodo PREPRINT v1: doi:10.5281/zenodo.20629238

FIGURE: Fig_Magnetic_Fields_ECF.png
--------------------------------------
Comparative magnetic field profiles B(r) for all four ECF topological
defect classes, as a function of distance from the defect core.

PHYSICS SUMMARY
---------------
Each ECF defect class generates a distinct magnetic field via the
Chern-Simons coupling L_CS ~ kappa^2 * s0 * J5 (Carroll, Field & Jackiw
1990; doi:10.1103/PhysRevD.41.1231):

  0D Micro-Knot   (pi_2): dipolar B ~ r^{-3}
    - Origin: axial current J5 of extremal Kerr winding N=1
    - Surface field: ~10^15-10^20 T at r_s = 5.56 mm (T_c = 159 GeV)
    - Today (flux freezing, B ~ a^{-2}): DILUTION = (a_EW/a_0)^2 = 2.4e-31
      [computed 15/10/2026, see DILUTION below], giving 2.4e-12 - 2.4e-7 G at r_s.
      (The former provisional DILUTION = 1e-28 gave 1e-9 - 1e-4 G; the range
      10^{-13}-10^{-8} quoted in earlier text was in tesla, not gauss:
      audit v2, P1-022 / A-12.)
    - Profile: B(r) = B0_micro * (r_s / r)^3

  1D Torsion String (pi_1): solenoidal + helical along axis
    - Origin: helical axial current J5 with pitch lambda_hel (PO-F2-2)
    - Field: B_chiral ~ kappa^2 * s0 * mu_1D / r_core
    - Today: ~10^{-9}-10^{-6} G at r ~ r_core to 1 kpc
    - Profile: B(r) = B0_string * exp(-r / r_core_string) + B_bg

  2D Chiral Wall (pi_0): tangential, uniform on surface
    - Origin: Chern-Simons coupling at sigma+/sigma- phase boundary
    - Field confined to wall thickness delta_w ~ 10^{-18} m
    - Today at void boundaries: ~10^{-10}-10^{-6} G
    - Profile: B(r) = B0_wall * exp(-|r| / delta_w_eff)
      (effective comoving thickness)

  3D Torsion Fluid (no pi_k): isotropic, space-filling SCMB
    - Origin: global chiral helicity H != 0 of the condensate
    - Stochastic cosmological magnetic background (SCMB)
    - Today: ~10^{-17}-10^{-12} G (uniform background floor)
    - Non-erasable by turbulence (topological invariant H)
    - Profile: B_fluid = constant (space-filling)

KEY REFEREE NOTE
----------------
All field amplitudes involve the unknown axial condensate s0 and the
torsion-CS coupling constant kappa^2 * s0. The ranges quoted reflect
the uncertainty in s0; the PROFILES (radial dependences) are
model-independent consequences of the defect topology.

The cosmological dilution (a_EW/a_0)^2 = 2.4e-31 (computed 15/10/2026) is
applied to the 0D surface field. The 1D, 2D and 3D 'today' amplitudes are
hard-coded; they assume the former, undocumented factor 1e-28 and would be
~400 times lower with the computed one. They are provisional.

CANONICAL VALUES (Foundation II, Table tab:ecf_defect_summary)
---------------------------------------------------------------
  kappa^2 = 2.0766e-43 m/J
  r_s (Micro-Knot) = 5.56e-3 m (Schwarzschild radius = c/H, exact)
  r_core (String)  = 1e-18 m  (electroweak coherence)
  delta_w (Wall)   = 1e-18 m  (electroweak coherence)
  xi_KZ            ~ 60 Mpc   (Kibble-Zurek scale)
  M_micro          = 3.74e24 kg = c^3 / (2 G H_EW)   [+/- 0.05e24]

OBSERVATIONAL PREDICTIONS
--------------------------
  0D: none -- negligible alone and collectively (~1e-65 to 1e-60 G at the
      mean spacing d ~ 0.056 pc; corrected 18/10/2026, was 'contributes to
      intergalactic magnetic background')
  1D: Faraday rotation along filaments; LOFAR, MeerKAT
  2D: Faraday rotation gradient ACROSS void edges -> SKA
      preferred chirality (B flips sign at wall) -> discriminable
  3D: global helicity H != 0 at scales > 100 Mpc -> SKA, Roman
      distinct from dynamo models where <H> = 0

FALSIFICATION
-------------
  SKA detection of Faraday gradient across void edges with preferred
  chirality would confirm 2D wall field.
  Absence of helicity H != 0 at > 100 Mpc would falsify 3D SCMB.

OUTPUT
------
  Fig_Magnetic_Fields_ECF.png  (300 dpi, white background)

DEPENDENCIES
------------
  numpy >= 1.24, matplotlib >= 3.7

AUTHOR
------
  Pascal Fichant (ECF programme) — CC-BY 4.0
  Contact: p.fichant.research@gmail.com
  GitHub:  github.com/pfichant/spin-torsion-cosmology
"""
# Last modified: 15/10/2026 (Paris time) -- F2-A6, computed dilution factor

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── Output path ────────────────────────────────────────────────────────────────
def _find_figs_dir(start=__file__):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(6):
        c = os.path.join(d, 'figures_output')
        if os.path.isdir(c):
            return c
        p = os.path.dirname(d)
        if p == d:
            break
        d = p
    fb = os.path.join(os.path.dirname(os.path.abspath(start)), 'figures_output')
    os.makedirs(fb, exist_ok=True)
    return fb

FIGS = _find_figs_dir()

# ── Style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi':     150,
    'font.family':    'serif',
    'font.size':      12,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.linewidth': 1.2,
})

C_MICRO  = '#1144AA'   # blue  — 0D Micro-Knot
C_STRING = '#BB7700'   # amber — 1D Torsion String
C_WALL   = '#5566CC'   # indigo — 2D Chiral Wall
C_FLUID  = '#228844'   # green  — 3D Torsion Fluid
C_OBS_LO = '#AAAAAA'   # grey  — observational lower bound
C_OBS_HI = '#444444'   # dark  — observational upper bound

# ── Shared x-axis: distance in parsecs ─────────────────────────────────────────
# Range: 1e-10 pc (sub-AU, ~30 AU = 1 pc/200) to 1e9 pc (300 Mpc)
r_pc = np.logspace(-10, 9, 2000)   # parsecs
pc_to_m = 3.086e16                   # 1 pc in metres
r_m = r_pc * pc_to_m                 # metres

# ── Conversion: Gauss ──────────────────────────────────────────────────────────
# All fields in Gauss (CGS); 1 T = 1e4 G

# Cosmological dilution of a frozen-in magnetic field: B ~ a^{-2}.
# [15/10/2026, F2-A6] Computed with entropy conservation (g_s a^3 T^3 = const):
#   a_EW/a_0 = (g_s0 / g_s(T_c))^{1/3} * T_0 / T_c
#            = (3.909 / 106.75)^{1/3} * (2.3487e-13 GeV) / (159 GeV) = 4.9e-16
#   (a_EW/a_0)^2 = 2.4e-31   (2.2e-30 without the g_s factor).
# The former value 1e-28 was undocumented (audit v2, P1-022 / A-12), ~400 times
# too large; the former comment "(2.7 K / 1.5e15 K)^2 ~ 3.24e-31" was also off:
# that ratio squared is 3.24e-30.
_T0_GeV, _Tc_GeV, _gs0, _gsc = 2.7255 * 8.617333e-14, 159.0, 3.909, 106.75
DILUTION = ((_gs0 / _gsc)**(1/3) * _T0_GeV / _Tc_GeV)**2   # = 2.41e-31

# ─────────────────────────────────────────────────────────────────────────────
# 0D Micro-Knot: B(r) = B0_micro * (r_s / r)^3   [dipolar]
# ─────────────────────────────────────────────────────────────────────────────
# [27/08/2026] Value revised: the horizon mass is c^3/(2GH), not c^3/(GH),
# and T_c = 159 +/- 1 GeV (lattice, D'Onofrio+2014) rather than an unsourced
# epoch. See Scripts_F2/calculate_microknot_mass.py.
# NB: r_s and M_micro were mutually inconsistent before this date
# (1.5 mm implies 1.0e24 kg, not 6e24). They now satisfy r_s = 2GM/c^2 = c/H.
r_s_m = 5.56e-3         # Schwarzschild radius (m)
r_s_pc = r_s_m / pc_to_m

# Surface field range at T~159 GeV (s0 uncertainty): 10^15 - 10^20 T
B_micro_surface_lo = 1e15 * 1e4 * DILUTION   # Gauss today, lower s0
B_micro_surface_hi = 1e20 * 1e4 * DILUTION   # Gauss today, upper s0

B_micro_lo = B_micro_surface_lo * (r_s_m / r_m)**3
B_micro_hi = B_micro_surface_hi * (r_s_m / r_m)**3

# Clip to physically meaningful range
B_micro_lo = np.clip(B_micro_lo, 1e-25, 1e5)
B_micro_hi = np.clip(B_micro_hi, 1e-25, 1e5)

# ─────────────────────────────────────────────────────────────────────────────
# 1D Torsion String: solenoidal + helical
# B(r) ~ B0_string * exp(-r/r_core) (transverse to string)
# Along string: helical component (not shown in 1D radial profile)
# ─────────────────────────────────────────────────────────────────────────────
r_core_m = 1e-18        # electroweak coherence length (m)
r_core_pc = r_core_m / pc_to_m

# Field at r_core: ~ 10^-9 to 10^-6 G (after dilution)
B_string_lo = 1e-9 * np.exp(-r_m / (r_core_m * 1e20))
B_string_hi = 1e-6 * np.exp(-r_m / (r_core_m * 1e20))

# Long-range: falls to background ~ 10^-12 G beyond kpc
B_string_bg_lo = 1e-12
B_string_bg_hi = 1e-9
B_string_lo = np.maximum(B_string_lo, B_string_bg_lo)
B_string_hi = np.maximum(B_string_hi, B_string_bg_hi)

# ─────────────────────────────────────────────────────────────────────────────
# 2D Chiral Wall: tangential field at wall surface
# B(r) = B0_wall * exp(-|r| / r_eff)  where r is distance to wall
# After cosmological dilution, effective void-edge field: 10^-10 - 10^-6 G
# ─────────────────────────────────────────────────────────────────────────────
# Effective comoving thickness of the "diffuse" wall zone ~ 1 Mpc
r_wall_eff_pc = 1e6    # 1 Mpc effective void-wall zone
B_wall_lo = 1e-10 * np.exp(-r_pc / r_wall_eff_pc)
B_wall_hi = 1e-6  * np.exp(-r_pc / r_wall_eff_pc)
B_wall_lo = np.maximum(B_wall_lo, 1e-20)
B_wall_hi = np.maximum(B_wall_hi, 1e-20)

# ─────────────────────────────────────────────────────────────────────────────
# 3D Torsion Fluid: isotropic SCMB, space-filling, constant
# B_fluid ~ 10^-17 - 10^-12 G  (uniform background)
# ─────────────────────────────────────────────────────────────────────────────
B_fluid_lo = 1e-17 * np.ones_like(r_pc)
B_fluid_hi = 1e-12 * np.ones_like(r_pc)

# ── Reference: allowed IGMF range (observational constraints) ───────────────────────────────────────
# 22/10/2026 : bornes actuelles, comme dans le texte de F2 :
# CMB upper bound: B < 4.4e-9 G (Planck 2015 XIX)
# Blazar cascade lower bound: B > 3e-16 G (Neronov & Vovk 2010)
B_obs_upper = 4.4e-9
B_obs_lower = 3e-16

# ── Observational scales ───────────────────────────────────────────────────────
r_AU = 1.0 / 206265.0   # 1 AU in parsecs
r_pc_1 = 1.0            # 1 pc
r_kpc  = 1e3            # 1 kpc
r_Mpc  = 1e6            # 1 Mpc
r_Gpc  = 1e9            # 1 Gpc (horizon)

# ── Figure layout: 1 main panel + 1 summary panel ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), facecolor='white')
fig.subplots_adjust(wspace=0.28)

# ════════════════════════════════════════════════════════════════════════════════
# LEFT PANEL: All 4 field profiles on shared r axis
# ════════════════════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_facecolor('#F8F8FF')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-10, 1e9)
ax.set_ylim(1e-22, 1e2)
ax.set_xlabel(r'Distance $r$ from defect core  [pc]', fontsize=12)
ax.set_ylabel(r'Magnetic field strength  $B(r)$  [G]', fontsize=12)
ax.set_title('ECF magnetic field profiles\n(today, z = 0)', fontsize=13,
             fontweight='bold', color='#111111')

# Observational bounds
ax.axhspan(B_obs_lower, B_obs_upper, alpha=0.10, color='#888888',
           label='Allowed IGMF range\n' +
                 r'$3\times10^{-16}$–$4.4\times10^{-9}$ G (blazar + CMB)',
           zorder=1)
ax.axhline(B_obs_upper, color='#555555', lw=1.2, ls='--', alpha=0.6)
ax.axhline(B_obs_lower, color='#555555', lw=1.0, ls=':', alpha=0.5)

# 0D Micro-Knot
ax.fill_between(r_pc, B_micro_lo, B_micro_hi,
                color=C_MICRO, alpha=0.25, zorder=3)
ax.plot(r_pc, B_micro_lo, color=C_MICRO, lw=1.8, ls='-', zorder=4)
ax.plot(r_pc, B_micro_hi, color=C_MICRO, lw=1.8, ls='--', zorder=4)

# 1D Torsion String
ax.fill_between(r_pc, B_string_lo, B_string_hi,
                color=C_STRING, alpha=0.25, zorder=3)
ax.plot(r_pc, B_string_lo, color=C_STRING, lw=1.8, ls='-', zorder=4)
ax.plot(r_pc, B_string_hi, color=C_STRING, lw=1.8, ls='--', zorder=4)

# 2D Chiral Wall
ax.fill_between(r_pc, B_wall_lo, B_wall_hi,
                color=C_WALL, alpha=0.25, zorder=3)
ax.plot(r_pc, B_wall_lo, color=C_WALL, lw=1.8, ls='-', zorder=4)
ax.plot(r_pc, B_wall_hi, color=C_WALL, lw=1.8, ls='--', zorder=4)

# 3D Torsion Fluid (constant bands)
ax.fill_between(r_pc, B_fluid_lo, B_fluid_hi,
                color=C_FLUID, alpha=0.22, zorder=2)
ax.plot(r_pc, B_fluid_lo, color=C_FLUID, lw=1.8, ls='-', zorder=3)
ax.plot(r_pc, B_fluid_hi, color=C_FLUID, lw=1.8, ls='--', zorder=3)

# Scale markers
for rval, label in [(r_AU, '1 AU'), (r_pc_1, '1 pc'),
                     (r_kpc, '1 kpc'), (r_Mpc, '1 Mpc'), (r_Gpc, '1 Gpc')]:
    ax.axvline(rval, color='#BBBBBB', lw=0.9, ls=':', alpha=0.7, zorder=1)
    ax.text(rval * 1.08, 5e-22, label, fontsize=7.5, color='#666666',
            rotation=90, va='bottom')

# Profile labels
ax.text(3e-1, 1e0,  r'0D Micro-Knot (dipolar $\propto r^{-3}$): below plotted range' '\n' r'($<10^{-30}$ G for $r>10^{-10}$ pc)',
        fontsize=9, color=C_MICRO, fontweight='bold', ha='center')
ax.text(3e2,  2e-10,
        r'1D Torsion String' '\n' r'solenoidal + helical',
        fontsize=9, color=C_STRING, fontweight='bold', ha='center')
ax.text(3e7,  3e-8,
        r'2D Chiral Wall' '\n' r'tangential (void edge)',
        fontsize=9, color=C_WALL, fontweight='bold', ha='center')
ax.text(1e4,  3e-14,
        r'3D Torsion Fluid' '\n' r'isotropic SCMB',
        fontsize=9, color=C_FLUID, fontweight='bold', ha='center')

# Legend (line styles)
legend_elements = [
    Line2D([0], [0], color='#555555', lw=1.2, ls='-',
           label=r'Solid = lower $s_0$ bound'),
    Line2D([0], [0], color='#555555', lw=1.2, ls='--',
           label=r'Dashed = upper $s_0$ bound'),
    mpatches.Patch(facecolor='#888888', alpha=0.2,
                   label=r'Allowed IGMF $3\times10^{-16}$–$4.4\times10^{-9}$ G'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
          framealpha=0.88, facecolor='#F4F6FF', edgecolor='#334488')

ax.tick_params(which='both', direction='in', top=True, right=True)
for sp in ax.spines.values():
    sp.set_color('#AABBDD')

# ════════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL: Summary table with field properties
# ════════════════════════════════════════════════════════════════════════════════
ax2 = axes[1]
ax2.set_facecolor('white')
ax2.axis('off')

table_data = [
    ['Level', 'Field type', 'Profile', r'$B_0$ today [G]', 'Observable'],
    ['0D\nMicro-Knot', 'Dipolar\n(q=+/-1, pres.)', r'$r^{-3}$',
     '2e-12 to 2e-7 G', 'none\n(negligible)'],
    ['1D\nT. String*', 'Solenoidal\n+ helical $J_5$', r'$e^{-r/r_c}$+const',
     '1e-9 to 1e-6 G\n(prov.)', 'Faraday\nfilaments'],
    ['2D\nChiral Wall', 'Tangential\n(dtheta=pi, flips)',
     r'$e^{-r/r_w}$',
     '1e-10 to 1e-6 G\n(prov.)', 'SKA void\nedges'],
    ['3D\nT. Fluid', 'Isotropic SCMB\n(H!=0, global)',
     'constant',
     '1e-17 to 1e-12 G\n(prov.)', r'SKA $>$100 Mpc'],
]

colors_col = ['#E8EDF8'] + [
    ['#DDEEFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#DDEEFF'],
    ['#FFEEDD', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFEEDD'],
    ['#EEEEFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#EEEEFF'],
    ['#DDEEDD', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#DDEEDD'],
]
col_colors_header = ['#2244AA'] * 6
col_text_header   = ['white'] * 6

the_table = ax2.table(
    cellText=table_data[1:],
    colLabels=table_data[0],
    cellLoc='center',
    loc='center',
    bbox=[-0.04, 0.10, 1.08, 0.82],
)
the_table.auto_set_font_size(False)
the_table.set_fontsize(8.5)
the_table.auto_set_column_width(list(range(5)))

# Style header
for j in range(5):
    cell = the_table[0, j]
    cell.set_facecolor('#2244AA')
    cell.set_text_props(color='white', fontweight='bold', fontsize=8.5)

# Style rows
row_colors = [C_MICRO, C_STRING, C_WALL, C_FLUID]
for i in range(1, 5):
    for j in range(5):
        cell = the_table[i, j]
        if j == 0:
            cell.set_facecolor(row_colors[i-1])
            cell.set_text_props(color='white', fontweight='bold', fontsize=8.5)
        elif j == 4:
            cell.set_facecolor('#F0F4FF')
            cell.set_text_props(fontsize=8.5, color='#1133AA')
        else:
            cell.set_facecolor('#FAFAFA')
            cell.set_text_props(fontsize=8.0)
        cell.set_edgecolor('#CCCCDD')

ax2.set_title('ECF magnetic field summary\n(all four defect levels)',
              fontsize=13, fontweight='bold', color='#111111', pad=14)

# Note boxes below table
ax2.text(0.50, 0.07,
    r'$\kappa^2 = 2.0766\times10^{-43}$ m J$^{-1}$   |   '
    r'Dilution: $(a_{\rm EW}/a_0)^2\simeq2.4\times10^{-31}$ (0D; 1D–3D prov.)   |   '
    r'$s_0$ unknown (range shown)',
    transform=ax2.transAxes, fontsize=8, color='#444444',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.4', fc='#F0F4FF', ec='#334488',
              alpha=0.9, lw=0.8))

ax2.text(0.50, 0.02,
    'Referee note: IGMF amplitudes depend on s0 (unknown); '
    r'radial profiles are model-independent.'
    '\n*1D row: semi-topological, dynamical stability not established (open, PO-F2-8).',
    transform=ax2.transAxes, fontsize=7.5, color='#AA2222',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.3', fc='#FFF0F0', ec='#CC2222',
              alpha=0.85, lw=0.7))

# ── Suptitle ───────────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure M1 — ECF Magnetic Field Hierarchy: All Four Defect Levels\n'
    r'Origin: Chern-Simons $\mathcal{L}_{\rm CS}\propto\kappa^2 s_0 J_5$ | '
    r'Dilution $(a_{\rm EW}/a_0)^2$ | Foundation II Sec. Topological Zoology',
    fontsize=11, fontweight='bold', color='#111111', y=1.01)

# ── Save ───────────────────────────────────────────────────────────────────────
out = os.path.join(FIGS, 'Fig_Magnetic_Fields_ECF.png')
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {out}')
