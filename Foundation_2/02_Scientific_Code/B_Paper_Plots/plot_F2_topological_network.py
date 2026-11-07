#!/usr/bin/env python3
"""
plot_F2_topological_network.py
================================
Foundation II — F2 PREPRINT v2
ECF topological structure: bubble picture (revised 30/08/2026)

OUTPUT: Fig_ECF_Topological_Network.png (300 dpi, white background)

PHYSICS (revised 30/08/2026 -- see F2 Sec. Topological Bestiary):
- 0D Micro-Knots: point defects (pi_2), generically near the centre of a bubble
- 2D Chiral Walls: independent CLOSED surfaces (pi_0, Z_2) -- NOT a connected
  network. Stable multi-way junctions do not exist for a two-phase (Z_2)
  wall sector; each wall bounds one interior domain on its own.
- 1D Torsion Strings: NOT an established connector between bubbles. Status:
  open problem (PO-F2-8), semi-topological at best, dynamical stability
  depends on the unresolved mass m_T. No edges are drawn between bubbles.
- 3D Torsion Fluid: fills the space between bubbles, drives dark energy.
- H1/H2 (revised): candidate mechanism is a magnetic dipole (sourced by s0
  at each node) exerting a Lorentz-force torque on infalling ionised gas --
  not a helical current carried by a string. Amplitude/direction not yet
  derived; H2 direction is not fixed by any principle in the corpus.
- H3, H4 (original "one-way cables" and "no dangling filaments"):
  WITHDRAWN outright. Not depicted.

This script replaces the earlier connected-network + H1-H4 figure (see
/tmp archive of the pre-30/08 version if a historical comparison is ever
needed).
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

np.random.seed(42)

# ── Output ──────────────────────────────────────────────────────────────────
# [CORRIGE 15/09/2026] Ce script creait un figures_output/ DANS son propre
# dossier, au lieu d'ecrire a cote du script comme tous les autres. Resultat :
# un B_Paper_Plots/figures_output/ parasite, que la centralisation du pipeline
# recopiait ensuite vers le vrai figures_output a la racine -- d'ou des PNG
# presents a deux endroits. Signale par Pascal le 15/09.
# On ecrit desormais dans le dossier du script ; la centralisation s'occupe
# du reste, comme pour les 112 autres.
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'Fig_ECF_Topological_Network.png')

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 150,
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
})

# Colors
C0D    = '#1144BB'   # blue   - 0D Micro-Knot nodes
C2D    = '#5544CC'   # indigo - 2D Chiral Wall (bubble boundary)
C3D    = '#228855'   # green  - 3D Torsion Fluid
C1D    = '#999999'   # grey   - 1D sector, OPEN status, drawn muted/dashed only
CBARY  = '#CC2222'   # red    - baryonic matter
CHALO  = '#88AADD'   # light blue - dark halo
CMAG   = '#CC8800'   # amber  - magnetic field lines (new H1/H2 candidate)
CWARN  = '#AA2222'   # warning red for withdrawn/open items

fig = plt.figure(figsize=(16, 10), facecolor='white')

gs = fig.add_gridspec(2, 3, height_ratios=[1.4, 1],
                       wspace=0.15, hspace=0.34,
                       left=0.02, right=0.98, top=0.91, bottom=0.06)

ax_net  = fig.add_subplot(gs[0, 0])   # bubble picture (was: connected network)
ax_mag  = fig.add_subplot(gs[0, 1])   # magnetic torque mechanism (was: internet analogy)
ax_leg  = fig.add_subplot(gs[0, 2])   # status legend (was: hierarchy + internet table)
ax_h1   = fig.add_subplot(gs[1, 0])   # H1, revised
ax_h2   = fig.add_subplot(gs[1, 1])   # H2, marked open
ax_h3   = fig.add_subplot(gs[1, 2])   # H3/H4 withdrawal notice

# ════════════════════════════════════════════════════════════════════════════
# PANEL A — Independent closed bubbles (replaces the connected network)
# ════════════════════════════════════════════════════════════════════════════
ax = ax_net
ax.set_facecolor('#F0F4F8')
ax.set_xlim(-0.1, 10.1)
ax.set_ylim(-0.1, 8.1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('ECF bubble picture\n(independent closed walls, $\\mathbb{Z}_2$)',
             fontsize=11, fontweight='bold', color='#111133', pad=6)

# 3D fluid background (fills space between bubbles)
bg = Rectangle((-0.1, -0.1), 10.3, 8.3, facecolor=C3D, alpha=0.05, zorder=0)
ax.add_patch(bg)

# Bubble centres, sizes, and irregular (foam-like) deformation -- NOT perfect
# circles, to avoid suggesting a geometric regularity the model does not
# predict (topology = closed sphere; geometry = irregular, foam-like).
bubbles = [
    (1.7, 6.3, 1.35, 220), (5.0, 6.9, 1.15, 350), (8.5, 6.3, 1.0, 180),
    (0.8, 3.3, 0.95, 160), (3.6, 4.3, 1.55, 500), (6.7, 3.9, 1.1, 250),
    (9.1, 3.6, 0.85, 200), (2.1, 1.1, 0.9, 140), (5.4, 1.4, 1.05, 280),
    (8.4, 1.1, 0.8, 160),
]

rng = np.random.default_rng(7)
theta = np.linspace(0, 2*np.pi, 60)
for (cx, cy, r, node_s) in bubbles:
    # irregular closed boundary: base radius + small random harmonic wobble
    wobble = np.ones_like(theta)
    for k in range(2, 5):
        wobble += (0.06 / k) * rng.standard_normal() * np.cos(k*theta + rng.uniform(0, 2*np.pi))
    rr = r * wobble
    xs = cx + rr * np.cos(theta)
    ys = cy + rr * np.sin(theta)
    poly = plt.Polygon(np.column_stack([xs, ys]), closed=True,
                        facecolor=C2D, alpha=0.10,
                        edgecolor=C2D, linewidth=1.4, zorder=2)
    ax.add_patch(poly)
    # node near centre (not exactly centred -- Israel repulsion pushes
    # residual matter outward over time, I69/30-08 chantier notes)
    nx, ny = cx + 0.08*r, cy - 0.05*r
    nr = np.sqrt(node_s) * 0.012
    glow = Circle((nx, ny), nr*2.3, facecolor=CHALO, edgecolor='none',
                  alpha=0.20, zorder=3)
    ax.add_patch(glow)
    ax.add_patch(Circle((nx, ny), nr, facecolor=C0D, edgecolor='white',
                         linewidth=1.3, zorder=5))

# Baryonic matter accumulating ON walls, near their mutual close approaches
# (NOT flowing along an edge -- ordinary gravitational infall onto the
# expanding wall, cf. Israel repulsion discussion)
ax.annotate('', xy=(5.3, 4.0), xytext=(6.0, 3.9),
            arrowprops=dict(arrowstyle='->', color=CBARY, lw=1.8,
                            mutation_scale=12), zorder=6)
ax.text(5.65, 4.25, 'gas accumulates\non walls (gravity)',
        fontsize=6.8, color=CBARY, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.15', fc='white', ec=CBARY,
                  alpha=0.85, lw=0.6))

leg_items = [
    mpatches.Patch(facecolor=C0D, label=r'0D Micro-Knot ($\pi_2$, near centre)'),
    mpatches.Patch(facecolor=C2D, alpha=0.3, label=r'2D Chiral Wall ($\pi_0$, closed, independent)'),
    mpatches.Patch(facecolor=C3D, alpha=0.25, label='3D Torsion Fluid (between bubbles)'),
    Line2D([0],[0], color=CBARY, lw=2, label='Baryonic infall (gravity)'),
]
ax.legend(handles=leg_items, loc='lower right', fontsize=6.5,
          framealpha=0.92, facecolor='#FAFAFA', edgecolor='#AAAAAA',
          handlelength=1.5, borderpad=0.5)
ax.text(5.0, -0.35,
        r'No 1D connector drawn: stable multi-way junctions do not exist for $\mathbb{Z}_2$ (I69). '
        r'1D sector: open problem (PO-F2-8).',
        fontsize=6.8, color=CWARN, ha='center', va='top', style='italic',
        transform=ax.transData, clip_on=False)


# ════════════════════════════════════════════════════════════════════════════
# PANEL B — Candidate mechanism: magnetic torque at a node (replaces the
# withdrawn "internet analogy", now carries the physics content of the
# revised H1/H2 candidate mechanism)
# ════════════════════════════════════════════════════════════════════════════
ax = ax_mag
ax.set_facecolor('#FFF8F0')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Candidate H1/H2 mechanism\n(magnetic torque, not a string current)',
             fontsize=10.5, fontweight='bold', color='#111133', pad=6)

# Node at centre
ax.add_patch(Circle((0, 0), 0.35, facecolor=C0D, edgecolor='white',
                     linewidth=1.5, zorder=6))
ax.text(0, -0.75, r'$B_{\rm knot}\sim9\times10^{-6}$ G', fontsize=7.5,
        color=CMAG, ha='center', va='top')

# Dipolar field lines (schematic loops through the node)
for a in [0.9, 1.6, 2.3, 3.0]:
    t = np.linspace(0.001, np.pi-0.001, 100)
    # simple dipole-like loop in the x-z plane, schematic only
    xline = a*np.sin(t)
    yline = a*np.cos(t)*np.sin(t)*1.6
    ax.plot(xline, yline+a*0.55, color=CMAG, lw=1.1, alpha=0.55, zorder=2)
    ax.plot(-xline, yline+a*0.55, color=CMAG, lw=1.1, alpha=0.55, zorder=2)
    ax.plot(xline, -(yline+a*0.55), color=CMAG, lw=1.1, alpha=0.55, zorder=2)
    ax.plot(-xline, -(yline+a*0.55), color=CMAG, lw=1.1, alpha=0.55, zorder=2)

# Infalling ionised gas (radial trajectory) + Lorentz-force kick
ax.annotate('', xy=(0.5, 0.5), xytext=(3.8, 3.8),
            arrowprops=dict(arrowstyle='->', color=CBARY, lw=1.8,
                            mutation_scale=12), zorder=7)
ax.text(3.6, 4.0, 'infalling\nionised gas', fontsize=7, color=CBARY,
        ha='center', va='bottom')
# net torque arrow (curved), schematic
ax.annotate('', xy=(1.3, -0.3), xytext=(0.5, 1.3),
            arrowprops=dict(arrowstyle='->', color='#116633', lw=2.0,
                            mutation_scale=12,
                            connectionstyle='arc3,rad=-0.5'), zorder=7)
ax.text(1.7, 0.4, r'net $\vec{L}$'+'\n(ion/electron\nmass asym.)',
        fontsize=6.8, color='#116633', ha='left', va='center')

ax.text(0, -4.4,
        'Not yet derived: amplitude, and whether the resulting spin is\n'
        'aligned (H1) or perpendicular (H2) to the filament -- depends on\n'
        'the node dipole orientation, not fixed by any corpus principle.',
        fontsize=7, color=CWARN, ha='center', va='top',
        style='italic')


# ════════════════════════════════════════════════════════════════════════════
# PANEL C — Status legend (replaces internet-analogy table + old hierarchy)
# ════════════════════════════════════════════════════════════════════════════
ax = ax_leg
ax.set_facecolor('#F4F8F4')
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Sector status (30/08/2026)', fontsize=11,
             fontweight='bold', color='#111133', pad=6)

levels = [
    ('3D Torsion Fluid', 'ESTABLISHED', C3D,
     r'$P_{\rm tors}<0$, drives dark energy', 6.7),
    ('2D Chiral Wall', 'ESTABLISHED', C2D,
     r'$\mathbb{Z}_2$, closed, independent (I69)', 5.0),
    ('1D Torsion sector', 'OPEN PROBLEM', CWARN,
     r'no Lagrangian foundation (I66); semi-\ntopological candidate, PO-F2-8', 3.3),
    ('0D Micro-Knot', 'ESTABLISHED', C0D,
     r'standard hedgehog, $\pi_2$', 1.6),
]

for name, status, col, pred, y in levels:
    box = FancyBboxPatch((0.3, y-0.62), 9.4, 1.15,
                          boxstyle='round,pad=0.08',
                          facecolor=col+'22', edgecolor=col,
                          linewidth=1.5, zorder=2)
    ax.add_patch(box)
    ax.text(1.0, y+0.18, name, fontsize=9.5, fontweight='bold',
            color=col, va='center', zorder=3)
    ax.text(1.0, y-0.22, pred, fontsize=7.2, color='#333333',
            va='center', style='italic', zorder=3)
    ax.text(9.0, y+0.18, status, fontsize=8, fontweight='bold',
            color=col, ha='right', va='center', zorder=3)

ax.text(5.0, 0.35,
        'No connected-network rule applies (the earlier '
        r'"$\partial\circ\partial=0$, no dangling cables"'
        '\nrule depended on the withdrawn 1D/junction structure -- see F2 text).',
        fontsize=6.8, color=CWARN, ha='center', va='center', style='italic')


# ════════════════════════════════════════════════════════════════════════════
# PANEL D — H1, revised: candidate rotation mechanism detail
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h1
ax.set_facecolor('#FFF8F0')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H1 (revised) — Coherent gas rotation near nodes\n'
             '(Wang+2021 $3.3\\sigma$; mechanism now magnetic, not string $J_5$)',
             fontsize=9.5, fontweight='bold', color=CMAG, pad=4)

# Node with dipole field, ionised gas spiralling in
ax.add_patch(Circle((5.0, 2.5), 0.4, facecolor=C0D, edgecolor='white',
                     lw=1.3, zorder=6))
for a in [0.8, 1.4, 2.0, 2.6]:
    tt = np.linspace(0, 2*np.pi, 100)
    ax.plot(5.0 + a*np.cos(tt), 2.5 + 0.4*a*np.sin(tt), color=CMAG,
            lw=1.0, alpha=0.5, zorder=2)

# Spiralling infall trajectory (schematic)
tt = np.linspace(0, 3*np.pi, 200)
rr = np.linspace(3.2, 0.5, 200)
xs = 5.0 + rr*np.cos(tt)
ys = 2.5 + 0.5*rr*np.sin(tt)
ax.plot(xs, ys, color=CBARY, lw=1.6, alpha=0.75, zorder=4)
ax.annotate('', xy=(xs[-1], ys[-1]), xytext=(xs[-8], ys[-8]),
            arrowprops=dict(arrowstyle='->', color=CBARY, lw=1.6,
                            mutation_scale=10), zorder=5)

ax.text(5.0, 0.0,
        r'Candidate: Lorentz torque on infalling ionised gas' '\n'
        r'from the node dipole $B_{\rm knot}$ (I/e mass asymmetry $\Rightarrow$ net spin).'
        '\nAmplitude and scaling: NOT YET DERIVED.',
        fontsize=8, color=CMAG, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#FFF4E8',
                  ec=CMAG, lw=0.8))


# ════════════════════════════════════════════════════════════════════════════
# PANEL E — H2, marked open (no ECF-specific mechanism proposed)
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h2
ax.set_facecolor('#F5F5F5')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H2 — Halo spin $\\perp$ filament (Rong+2025, $2\\sigma$)\n'
             'OPEN: no ECF-specific mechanism currently proposed',
             fontsize=9.5, fontweight='bold', color=CWARN, pad=4)

ax.plot([1.0, 9.0], [2.5, 2.5], color='#BBBBBB', lw=2.0, alpha=0.6, ls='--')
ax.add_patch(Circle((5.0, 2.5), 0.35, facecolor=C0D, edgecolor='white',
                     lw=1.2, alpha=0.7, zorder=5))
ax.add_patch(Ellipse((5.0, 2.5), 2.6, 2.6, color=CHALO, alpha=0.18, zorder=3))
ax.annotate('', xy=(5.0, 3.9), xytext=(5.0, 2.5),
            arrowprops=dict(arrowstyle='->', color='#888888', lw=2.0,
                            mutation_scale=14, ls='--'), zorder=6)
ax.text(5.3, 3.2, r'$\vec{L}_{\rm halo}$?', fontsize=9,
        color='#888888', va='center', style='italic')

ax.text(5.0, 0.2,
        'Observation is real (Rong \\& Wang 2025, $2\\sigma$).\n'
        'The original mechanism (multiple 1D strings converging at a node)\n'
        'required an unstable multi-way junction (I69) -- withdrawn.\n'
        'Provisional explanation: standard tidal torque theory (TTT).',
        fontsize=7.8, color='#555555', ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#EEEEEE',
                  ec='#999999', lw=0.8))


# ════════════════════════════════════════════════════════════════════════════
# PANEL F — H3 and H4: withdrawal notice (no replacement mechanism)
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h3
ax.set_facecolor('#FFF0F0')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H3 and H4 — WITHDRAWN (30/08/2026)',
             fontsize=10.5, fontweight='bold', color=CWARN, pad=4)

ax.text(5.0, 3.3,
        r'$\times$ H3: preferred flow along "one-way cables"',
        fontsize=9.5, color=CWARN, ha='center', va='center',
        fontweight='bold')
ax.text(5.0, 2.6,
        'Required a directed graph over 1D edges -- unfounded.\n'
        'Underlying physics (infall toward the more massive node)\n'
        'is generic gravity, already present in $\\Lambda$CDM.',
        fontsize=8, color='#555555', ha='center', va='center')

ax.plot([0.5, 9.5], [1.6, 1.6], color='#DDDDDD', lw=1.0)

ax.text(5.0, 1.0,
        r'$\times$ H4: filaments must terminate at nodes ("no dangling cables")',
        fontsize=9.5, color=CWARN, ha='center', va='center',
        fontweight='bold')
ax.text(5.0, 0.3,
        'Doubly unfounded: (i) unfounded 1D sector; (ii) even a standard\n'
        'cosmic string has no loose end to forbid -- Peter \\& Uzan \\S11.3.1\n'
        'show strings are infinite or closed loops. No replacement proposed.',
        fontsize=8, color='#555555', ha='center', va='center')


# ── Super title ──────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure M4 (revised 30/08/2026) — ECF topological structure: independent bubbles,\n'
    'open 1D sector, and the candidate magnetic mechanism replacing H1/H2  |  Foundation II, Topological Bestiary',
    fontsize=9.5, fontweight='bold', color='#111133', y=0.985)

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig(OUT, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {OUT}')
