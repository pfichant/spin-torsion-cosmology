#!/usr/bin/env python3
"""
plot_F2_topological_network.py
================================
Foundation II — F2 PREPRINT v2
ECF Topological Network: 4-level hierarchy with highway predictions H1-H4

OUTPUT: Fig_ECF_Topological_Network.png (300 dpi, white background)

PHYSICS:
- 0D Micro-Knots: network nodes (routers/servers)
- 1D Torsion Strings: edges/cables connecting nodes
- 2D Chiral Walls: faces/membranes bounding cells
- 3D Torsion Fluid: volume/background medium
- H1: filament rotation (helical J5)
- H2: halo spin perpendicular to filament
- H3: asymmetric matter flow node-to-node
- H4: no dangling filaments (topological constraint)
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse, FancyBboxPatch
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap

np.random.seed(42)

# ── Output ──────────────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'figures_output', 'Fig_ECF_Topological_Network.png')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

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
C1D    = '#BB6600'   # amber  - 1D Torsion String edges
C2D    = '#5544CC'   # indigo - 2D Chiral Wall faces
C3D    = '#228855'   # green  - 3D Torsion Fluid
CBARY  = '#CC2222'   # red    - baryonic matter
CHALO  = '#88AADD'   # light blue - dark halo

fig = plt.figure(figsize=(16, 10), facecolor='white')
fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.06,
                    wspace=0.12, hspace=0.35)

# ── LAYOUT: 2 rows × 3 cols ──────────────────────────────────────────────────
# Top: [big network panel] [internet analogy] [hierarchy legend]
# Bottom: [H1 rotation] [H2 spin] [H3+H4 flow+forbidden]

gs = fig.add_gridspec(2, 3, height_ratios=[1.4, 1],
                       wspace=0.15, hspace=0.32,
                       left=0.02, right=0.98, top=0.93, bottom=0.06)

ax_net  = fig.add_subplot(gs[0, 0])   # main network
ax_ana  = fig.add_subplot(gs[0, 1])   # internet analogy
ax_leg  = fig.add_subplot(gs[0, 2])   # hierarchy legend
ax_h1   = fig.add_subplot(gs[1, 0])   # H1 rotation
ax_h2   = fig.add_subplot(gs[1, 1])   # H2 spin
ax_h3   = fig.add_subplot(gs[1, 2])   # H3+H4

# ════════════════════════════════════════════════════════════════════════════
# PANEL A — Main ECF topological network
# ════════════════════════════════════════════════════════════════════════════
ax = ax_net
ax.set_facecolor('#F0F4F8')
ax.set_xlim(-0.1, 10.1)
ax.set_ylim(-0.1, 8.1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('ECF Topological Network\n(Cosmic Web structure)',
             fontsize=11, fontweight='bold', color='#111133', pad=6)

# Node positions (0D Micro-Knots at intersections)
nodes = {
    'A': (1.5, 6.5), 'B': (5.0, 7.0), 'C': (8.5, 6.5),
    'D': (0.5, 3.5), 'E': (3.5, 4.5), 'F': (6.5, 4.0),
    'G': (9.2, 3.8), 'H': (2.0, 1.0), 'I': (5.5, 1.5),
    'J': (8.5, 1.2),
}

# 2D Chiral Wall faces (void boundaries) — polygons between nodes
faces = [
    ['A', 'B', 'E', 'D'],
    ['B', 'C', 'G', 'F', 'E'],
    ['D', 'E', 'H'],
    ['E', 'F', 'I', 'H'],
    ['F', 'G', 'J', 'I'],
]

# Draw 2D faces (Chiral Walls)
for face in faces:
    pts = np.array([nodes[n] for n in face])
    # Centroid slightly inward
    cx, cy = pts.mean(axis=0)
    pts_in = pts + 0.08 * (np.array([[cx,cy]] * len(pts)) - pts)
    poly = plt.Polygon(pts_in, closed=True,
                       facecolor=C2D, alpha=0.08,
                       edgecolor=C2D, linewidth=1.2, linestyle='--')
    ax.add_patch(poly)
    # Face label
    ax.text(cx, cy, r'$\pi_0$', fontsize=7, color=C2D, alpha=0.6,
            ha='center', va='center', style='italic')

# Draw 1D Torsion Strings (edges)
edges = [
    ('A','B'), ('B','C'), ('A','D'), ('B','E'), ('C','G'),
    ('D','E'), ('E','F'), ('F','G'), ('D','H'), ('E','H'),
    ('E','I'), ('F','I'), ('G','J'), ('H','I'), ('I','J'),
    ('E','G'),  # diagonal
]

for n1, n2 in edges:
    x1, y1 = nodes[n1]
    x2, y2 = nodes[n2]
    # Add slight helical wiggle to edges
    t = np.linspace(0, 1, 40)
    perp = np.array([-(y2-y1), (x2-x1)])
    plen = np.linalg.norm(perp)
    if plen > 0:
        perp /= plen
    wiggle = 0.12 * np.sin(4 * np.pi * t)
    xs = x1 + t*(x2-x1) + wiggle * perp[0]
    ys = y1 + t*(y2-y1) + wiggle * perp[1]
    ax.plot(xs, ys, color=C1D, lw=1.6, alpha=0.75, zorder=3)

# Draw 0D nodes (Micro-Knots)
node_sizes = {'A': 220, 'B': 350, 'C': 180, 'D': 160, 'E': 500,
              'F': 250, 'G': 200, 'H': 140, 'I': 280, 'J': 160}

for name, (x, y) in nodes.items():
    s = node_sizes[name]
    r = np.sqrt(s) * 0.018
    # Halo glow
    glow = Circle((x, y), r*2.5, facecolor=CHALO, edgecolor='none', alpha=0.18, zorder=3)
    ax.add_patch(glow)
    # Node
    circ = Circle((x, y), r, facecolor=C0D, edgecolor='white',
                  linewidth=1.5, zorder=5)
    ax.add_patch(circ)
    # Mass label for main nodes
    if name in ['E', 'B']:
        lbl = r'$N_{\rm MK}$' if name == 'E' else r'$N_{\rm mK}$'
        ax.text(x, y-r-0.22, lbl, fontsize=6.5, color=C0D,
                ha='center', va='top', zorder=6)

# 3D fluid shading (background)
from matplotlib.patches import Rectangle
bg = Rectangle((-0.1, -0.1), 10.3, 8.3,
               facecolor=C3D, alpha=0.04, zorder=0)
ax.add_patch(bg)

# Baryonic matter flow arrow (red)
ax.annotate('', xy=(5.8, 5.2), xytext=(4.2, 5.8),
            arrowprops=dict(arrowstyle='->', color=CBARY,
                            lw=2.0, mutation_scale=14),
            zorder=7)
ax.text(4.7, 5.65, 'baryons', fontsize=7.5, color=CBARY,
        ha='center', va='bottom', zorder=8, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.15', fc='white', ec=CBARY,
                  alpha=0.85, lw=0.7))

# Legend inside panel
leg_items = [
    mpatches.Patch(facecolor=C0D, label=r'0D Micro-Knot (node, $\pi_2$)'),
    Line2D([0],[0], color=C1D, lw=2, label=r'1D Torsion String (edge, $\pi_1$)'),
    mpatches.Patch(facecolor=C2D, alpha=0.3, label=r'2D Chiral Wall (face, $\pi_0$)'),
    mpatches.Patch(facecolor=C3D, alpha=0.25, label='3D Torsion Fluid (volume)'),
    Line2D([0],[0], color=CBARY, lw=2, label='Baryonic flow'),
]
ax.legend(handles=leg_items, loc='lower right', fontsize=6.5,
          framealpha=0.92, facecolor='#FAFAFA', edgecolor='#AAAAAA',
          handlelength=1.5, borderpad=0.5)


# ════════════════════════════════════════════════════════════════════════════
# PANEL B — Internet analogy
# ════════════════════════════════════════════════════════════════════════════
ax = ax_ana
ax.set_facecolor('#F8F8F0')
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Internet analogy\n(topological equivalence)',
             fontsize=11, fontweight='bold', color='#111133', pad=6)

# Two-column comparison table
cols = ['ECF Structure', 'Internet equivalent']
rows = [
    ['0D Micro-Knot', 'Server / Router'],
    ['1D Torsion String', 'Backbone cable'],
    ['2D Chiral Wall', 'Domain firewall'],
    ['3D Torsion Fluid', 'Background signal'],
    ['Baryonic matter', 'Data packets'],
    ['Galaxy formation', 'Server cluster'],
    [r'$\partial\circ\partial=0$', 'No dangling cables'],
]
colors_row = [C0D, C1D, C2D, C3D, CBARY, '#888844', '#444444']

# Header
ax.text(2.5, 7.5, cols[0], fontsize=9, fontweight='bold',
        color='white', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', fc='#222244', ec='none'))
ax.text(7.5, 7.5, cols[1], fontsize=9, fontweight='bold',
        color='white', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', fc='#224422', ec='none'))

for i, (ecf, inet) in enumerate(rows):
    y = 6.5 - i * 0.88
    col = colors_row[i]
    ax.text(2.5, y, ecf, fontsize=8.5, color=col, ha='center', va='center',
            fontweight='bold' if i < 4 else 'normal',
            bbox=dict(boxstyle='round,pad=0.3', fc=col+'18', ec=col,
                      lw=0.8, alpha=0.9))
    ax.text(7.5, y, inet, fontsize=8.5, color='#333333',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='#EEEEEE',
                      ec='#AAAAAA', lw=0.6))
    # Arrow
    ax.annotate('', xy=(5.2, y), xytext=(4.0, y),
                arrowprops=dict(arrowstyle='->', color='#888888',
                                lw=1.0, mutation_scale=10))

# Key rule box
ax.text(5.0, 0.35,
        r'Rule: $\partial\circ\partial=0$  →  cables always end at servers',
        fontsize=8, color='#222244', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', fc='#EEF0FF',
                  ec='#334488', lw=1.2, alpha=0.95))


# ════════════════════════════════════════════════════════════════════════════
# PANEL C — Hierarchy legend with dimensional chain
# ════════════════════════════════════════════════════════════════════════════
ax = ax_leg
ax.set_facecolor('#F4F8F4')
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('Dimensional hierarchy\n' + r'$\partial\circ\partial = 0$',
             fontsize=11, fontweight='bold', color='#111133', pad=6)

levels = [
    ('3D Torsion Fluid', 'Volume\n(dark energy)', C3D,
     r'$P_{\rm tors}<0$, $w_{\rm eff}=-0.904$', 7.1),
    ('2D Chiral Wall', 'Face\n(void boundary)', C2D,
     r'$\beta=0.35°$, LiteBIRD', 5.4),
    ('1D Torsion String', 'Edge\n(cosmic filament)', C1D,
     r'Rotation H1, $3.3\sigma$', 3.7),
    ('0D Micro-Knot', 'Node\n(galaxy seed)', C0D,
     r'$\tilde\chi^2=0.80$, Roman', 2.0),
]

for name, geom, col, pred, y in levels:
    # Box
    box = FancyBboxPatch((0.3, y-0.55), 9.4, 1.05,
                          boxstyle='round,pad=0.08',
                          facecolor=col+'22', edgecolor=col,
                          linewidth=1.5, zorder=2)
    ax.add_patch(box)
    ax.text(1.2, y+0.08, name, fontsize=9, fontweight='bold',
            color=col, va='center', zorder=3)
    ax.text(1.2, y-0.28, pred, fontsize=7.5, color='#333333',
            va='center', style='italic', zorder=3)
    ax.text(8.8, y-0.1, geom, fontsize=7.5, color=col,
            ha='right', va='center', zorder=3)

# Arrows between levels
for y_top, y_bot in [(6.6, 6.05), (4.9, 4.35), (3.2, 2.65)]:
    ax.annotate('', xy=(5.0, y_bot), xytext=(5.0, y_top),
                arrowprops=dict(arrowstyle='->', color='#666666',
                                lw=1.5, mutation_scale=12),
                zorder=4)
    ax.text(5.4, (y_top+y_bot)/2, r'$\partial$', fontsize=10,
            color='#666666', va='center')

# Stability note
ax.text(5.0, 0.6,
        r'Each level stable: $\tau_{\rm evap}>10^{83}$ yr',
        fontsize=8, color='#226622', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.35', fc='#E8F4E8',
                  ec='#228855', lw=1.0))


# ════════════════════════════════════════════════════════════════════════════
# PANEL D — H1: Filament rotation
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h1
ax.set_facecolor('#FFF8F0')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H1 — Filament rotation\n(helical $J_5$, Wang+2021: $3.3\\sigma$)',
             fontsize=10, fontweight='bold', color='#BB6600', pad=4)

# Draw a filament as a helix
t = np.linspace(0, 4*np.pi, 200)
x_fil = np.linspace(0.5, 9.5, 200)
y_fil = 2.5 + 0.45 * np.sin(t)
y_fil2 = 2.5 - 0.45 * np.sin(t)

ax.plot(x_fil, y_fil, color=C1D, lw=2.0, alpha=0.85)
ax.plot(x_fil, y_fil2, color=C1D, lw=2.0, alpha=0.40, ls='--')

# Node at each end
for xn, yn in [(0.5, 2.5), (9.5, 2.5)]:
    ax.add_patch(Circle((xn, yn), 0.35, facecolor=C0D, edgecolor='white',
                         lw=1.2, zorder=5))

# Rotation arrows around filament
for xi in [2.5, 5.0, 7.5]:
    ax.annotate('', xy=(xi, 3.15), xytext=(xi+0.7, 2.5),
                arrowprops=dict(arrowstyle='->', color='#CC4400',
                                lw=1.5, mutation_scale=12), zorder=6)
    ax.annotate('', xy=(xi-0.7, 2.5), xytext=(xi, 1.85),
                arrowprops=dict(arrowstyle='->', color='#CC4400',
                                lw=1.5, mutation_scale=12), zorder=6)

# Red-blue galaxies (rotation signal)
for i, (xi, col, lbl) in enumerate([(3.5, '#CC2222','receding'),
                                       (4.0, '#2244CC','approaching'),
                                       (6.0, '#CC2222','receding'),
                                       (6.5, '#2244CC','approaching')]):
    yi = 2.5 + (0.8 if col=='#CC2222' else -0.8)
    ax.add_patch(Circle((xi, yi), 0.15, facecolor=col, edgecolor='none', zorder=5, alpha=0.85))

ax.text(5.0, 0.0, r'$\Omega_{\rm fil}\propto\mu_{1D}\lambda_{\rm hel}^{-1}$'
        '\n' + r'reversal at $\xi_{\rm KZ}\sim60$ Mpc',
        fontsize=8, color='#BB6600', ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#FFF4E8',
                  ec='#BB6600', lw=0.8))

ax.text(5.0, 4.5, r'$\vec{J}_5$ helical current',
        fontsize=8.5, color=C1D, ha='center', va='top',
        style='italic')


# ════════════════════════════════════════════════════════════════════════════
# PANEL E — H2: Halo spin perpendicular
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h2
ax.set_facecolor('#F0F8F0')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H2 — Halo spin $\\perp$ filament\n(Rong+2025, $2\\sigma$)',
             fontsize=10, fontweight='bold', color='#226633', pad=4)

# Horizontal filament
ax.plot([0.5, 9.5], [2.5, 2.5], color=C1D, lw=2.5, alpha=0.8)

# Nodes
for xn in [0.5, 5.0, 9.5]:
    ax.add_patch(Circle((xn, 2.5), 0.35, facecolor=C0D, edgecolor='white', lw=1.2, zorder=5))

# Halo at central node with perpendicular spin arrow
ax.add_patch(Ellipse((5.0, 2.5), 2.8, 2.8, color=CHALO,
                      alpha=0.22, zorder=3))
# Spin arrow (vertical = perpendicular to horizontal filament)
ax.annotate('', xy=(5.0, 4.1), xytext=(5.0, 2.5),
            arrowprops=dict(arrowstyle='->', color='#116633',
                            lw=2.5, mutation_scale=16), zorder=7)
ax.text(5.3, 3.4, r'$\vec{L}_{\rm halo}$', fontsize=10,
        color='#116633', va='center', fontweight='bold')
ax.text(5.3, 4.2, r'$\perp$ filament', fontsize=8,
        color='#116633', va='bottom')

# Filament direction arrow
ax.annotate('', xy=(7.5, 2.5), xytext=(6.5, 2.5),
            arrowprops=dict(arrowstyle='->', color=C1D,
                            lw=1.5, mutation_scale=12), zorder=6)
ax.text(7.0, 2.15, 'filament', fontsize=7.5, color=C1D, ha='center')

# Right-angle symbol
ax.plot([4.75, 4.75, 5.0], [2.5, 2.72, 2.72],
        color='#116633', lw=1.2, alpha=0.7)

ax.text(5.0, 0.0,
        r'Geometric consequence of conical deficit' '\n'
        r'$\delta = 8\pi G\mu_{1D}/c^2$ at string endpoints',
        fontsize=8, color='#226633', ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='#E8F4E8',
                  ec='#228855', lw=0.8))


# ════════════════════════════════════════════════════════════════════════════
# PANEL F — H3: Asymmetric flow + H4: No dangling filaments
# ════════════════════════════════════════════════════════════════════════════
ax = ax_h3
ax.set_facecolor('#F0F0F8')
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5)
ax.axis('off')
ax.set_title('H3 — Asymmetric flow  |  H4 — No dangling filaments\n'
             '(DESI+Euclid: testable now)',
             fontsize=10, fontweight='bold', color='#333388', pad=4)

# H3: left half — two nodes of different mass, asymmetric flow
ax.text(2.5, 4.6, 'H3: Matter flow', fontsize=8.5, color='#333388',
        ha='center', fontweight='bold')

# Small node (low N)
ax.add_patch(Circle((0.8, 2.5), 0.25, facecolor=C0D, edgecolor='white',
                     lw=1.0, alpha=0.7, zorder=5))
ax.text(0.8, 1.8, r'$N_{\rm small}$', fontsize=7, color=C0D, ha='center')

# Large node (high N)
ax.add_patch(Circle((4.5, 2.5), 0.55, facecolor=C0D, edgecolor='white', lw=1.5, zorder=5))
ax.add_patch(Ellipse((4.5, 2.5), 2.5, 2.5, color=CHALO,
                      alpha=0.18, zorder=3))
ax.text(4.5, 1.5, r'$N_{\rm large}$ (Macro-Knot)', fontsize=7,
        color=C0D, ha='center')

# Filament between them
ax.plot([1.05, 3.95], [2.5, 2.5], color=C1D, lw=2.0, alpha=0.75)

# Asymmetric baryon flow arrows (more toward large node)
for xi, lw, alpha in [(2.5, 2.0, 0.9), (3.0, 1.5, 0.7), (3.5, 1.0, 0.5)]:
    ax.annotate('', xy=(xi+0.45, 2.5), xytext=(xi, 2.5),
                arrowprops=dict(arrowstyle='->', color=CBARY,
                                lw=lw, mutation_scale=10*alpha,
                                alpha=alpha), zorder=6)

ax.text(2.5, 3.2, r'$\dot{M}_{\rm flow}\propto\Delta N$',
        fontsize=8, color=CBARY, ha='center',
        bbox=dict(boxstyle='round,pad=0.2', fc='#FFE8E8',
                  ec=CBARY, lw=0.7))

# Divider
ax.plot([5.3, 5.3], [-0.5, 4.8], color='#CCCCCC', lw=1.0, ls=':')

# H4: right half — forbidden dangling filament
ax.text(8.0, 4.6, 'H4: No dangling\nfilaments', fontsize=8.5,
        color='#333388', ha='center', fontweight='bold')

# Valid network (node at both ends)
ax.add_patch(Circle((6.2, 3.5), 0.22, facecolor=C0D, edgecolor='white', lw=1.0, zorder=5))
ax.add_patch(Circle((9.8, 3.5), 0.22, facecolor=C0D, edgecolor='white', lw=1.0, zorder=5))
ax.plot([6.42, 9.58], [3.5, 3.5], color=C1D, lw=1.8, alpha=0.8)
ax.text(8.0, 3.9, r'$\checkmark$ valid', fontsize=8,
        color='#228855', ha='center')

# Void (empty)
void_circ = Circle((8.5, 1.5), 0.8, facecolor='#EEEEEE',
                    alpha=0.8, edgecolor='#AAAAAA', lw=1.0,
                    linestyle='--', zorder=2)
ax.add_patch(void_circ)
ax.text(8.5, 1.5, 'void', fontsize=7.5, color='#888888',
        ha='center', va='center', style='italic')

# Dangling filament (forbidden)
ax.add_patch(Circle((6.2, 1.5), 0.22, facecolor=C0D, edgecolor='white', lw=1.0, zorder=5))
ax.plot([6.42, 7.7], [1.5, 1.5], color=C1D, lw=1.8, alpha=0.6)
# Red X
ax.plot([7.9, 8.2], [1.7, 1.4], color='red', lw=2.5, zorder=8)
ax.plot([7.9, 8.2], [1.4, 1.7], color='red', lw=2.5, zorder=8)
ax.text(8.0, 0.7, r'$\times$ forbidden', fontsize=8,
        color='red', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', fc='#FFE8E8',
                  ec='red', lw=0.8))
ax.text(8.0, 0.1, r'$\partial\circ\partial=0$', fontsize=8.5,
        color='#333388', ha='center',
        bbox=dict(boxstyle='round,pad=0.25', fc='#EEEEFF',
                  ec='#334488', lw=0.8))


# ── Super title ──────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure M4 — ECF Topological Network: The Cosmic Web as a 4-level topological object\n'
    '0D nodes -> 1D edges -> 2D faces -> 3D volume  |  '
    'boundary rule d(d)=0  |  Foundation II, Topological Bestiary',
    fontsize=9.5, fontweight='bold', color='#111133', y=0.995)

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig(OUT, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f'[OK] -> {OUT}')
