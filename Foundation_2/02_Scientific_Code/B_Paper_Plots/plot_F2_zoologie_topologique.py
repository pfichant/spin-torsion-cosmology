#!/usr/bin/env python3
"""
plot_F2_zoologie_topologique.py
================================
Foundation II — F2 PREPRINT v2
Generates the 5 figures of the ECF Topological Zoology section:

  Fig_MicroKnot_0D.png
  Fig_MacroKnot_1D_Wake.png
  Fig_DomainWall_2D.png
  Fig_ChiralFluid_3D.png
  Fig_ECF_Topological_Architecture.png

Visibility design (v3 — white background, referee-ready):
  - White background (#FFFFFF), light-gray 3D panes
  - 12pt minimum font everywhere, bold titles
  - Thicker lines/markers for clarity at print resolution
  - Annotations in opaque light boxes (no dark-on-dark)
  - All labels in English

Author  : Pascal Fichant (ECF programme)
Licence : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

# ── Global ECF palette (white background) ─────────────────────────────────────
BG       = '#FFFFFF'
BG_AX    = '#F8F8FF'
C_TEXT   = '#111111'      # main text / titles
C_SUB    = '#333333'      # subtitles / axis labels
C_TICK   = '#555555'      # ticks
C_NODE   = '#1a1a1a'      # 0D node fill
C_NODE_E = '#2244AA'      # 0D node edge / halo
C_FIL    = '#CC8800'      # 1D filament (darker amber for contrast on white)
C_WALL   = '#5566CC'      # 2D wall
C_FLUID  = '#3355AA'      # 3D fluid legend swatch
C_PINK   = '#CC2288'      # hedgehog vectors
C_CYAN   = '#0099AA'      # deflected geodesics
C_RED    = '#CC2222'      # repulsion / wake
C_GOLD   = '#AA7700'      # expelled gas trajectories
C_GREEN  = '#228844'      # DESI band
C_ANNOT  = '#222244'      # annotation text

ANNOT_BOX = dict(boxstyle='round,pad=0.5', facecolor='#EEF0FF',
                 alpha=0.95, edgecolor='#3355AA', lw=1.2)

LEGEND_KW = dict(framealpha=0.92, facecolor='#F4F6FF',
                  edgecolor='#3355AA', labelcolor=C_TEXT)

plt.rcParams.update({
    'figure.dpi'     : 300,
    'font.family'    : 'serif',
    'font.size'      : 12,
    'axes.labelsize' : 12,
    'axes.titlesize' : 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
})

# ── Output path resolution ─────────────────────────────────────────────────────
def _find_figs_dir(start=__file__):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(6):
        cand = os.path.join(d, 'figures_output')
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    fallback = os.path.join(os.path.dirname(os.path.abspath(start)), 'figures_output')
    os.makedirs(fallback, exist_ok=True)
    return fallback

FIGS = _find_figs_dir()

def save(fig, name):
    path = os.path.join(FIGS, name)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'[OK] {name}  ->  {path}')

def style3d(ax):
    """Apply consistent light style to a 3D axis."""
    ax.set_facecolor(BG_AX)
    ax.tick_params(colors=C_TICK, labelsize=9)
    ax.xaxis.label.set_color(C_SUB)
    ax.yaxis.label.set_color(C_SUB)
    ax.zaxis.label.set_color(C_SUB)
    ax.xaxis.pane.fill = True
    ax.yaxis.pane.fill = True
    ax.zaxis.pane.fill = True
    ax.xaxis.pane.set_facecolor('#FAFAFF')
    ax.yaxis.pane.set_facecolor('#FAFAFF')
    ax.zaxis.pane.set_facecolor('#FAFAFF')
    ax.xaxis.pane.set_edgecolor('#BBBBDD')
    ax.yaxis.pane.set_edgecolor('#BBBBDD')
    ax.zaxis.pane.set_edgecolor('#BBBBDD')
    ax.grid(False)


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — 0D Micro-Knot
# ═════════════════════════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(13, 10), facecolor=BG)
ax1  = fig1.add_subplot(111, projection='3d')
style3d(ax1)
ax1.axis('off')

# Central singularity
ax1.scatter([0],[0],[0], color=C_NODE, s=300, zorder=10,
            edgecolors=C_NODE_E, linewidths=1.8)

# Hedgehog field
N_vec = 9
r0 = 0.60
for th in np.linspace(0.15, np.pi-0.15, N_vec):
    for ph in np.linspace(0, 2*np.pi, N_vec*2, endpoint=False):
        ox = r0*np.sin(th)*np.cos(ph)
        oy = r0*np.sin(th)*np.sin(ph)
        oz = r0*np.cos(th)
        n  = np.sqrt(ox**2+oy**2+oz**2)
        ax1.quiver(ox, oy, oz, ox/n*0.30, oy/n*0.30, oz/n*0.30,
                   length=0.30, normalize=True,
                   color=C_PINK, alpha=0.90, linewidth=1.3,
                   arrow_length_ratio=0.28)

# Deflected null-geodesics
n_rays = 14
for y0 in np.linspace(-1.5, 1.5, n_rays):
    t   = np.linspace(-2.0, 2.0, 300)
    imp = abs(y0)+0.12
    alpha = 0.38/(imp+0.18)
    yt  = np.where(t<0, y0, y0 - np.sign(y0)*alpha*(t/(abs(t)+0.25)))
    col = C_CYAN if abs(y0)<0.55 else '#66AACC'
    lw  = 1.6 if abs(y0)<0.55 else 1.0
    ax1.plot(t, yt, np.zeros_like(t), color=col, alpha=0.75, lw=lw)

# Light halo
u = np.linspace(0, 2*np.pi, 120)
for r_h, al in [(0.35,0.22),(0.55,0.13),(0.80,0.07)]:
    ax1.plot(r_h*np.cos(u), r_h*np.sin(u), np.zeros_like(u),
             color=C_NODE_E, alpha=al, lw=2.5)

ax1.set_title(
    'ECF 0D Micro-Knot — Topological hedgehog & gravitational microlensing\n'
    r'$M_{\mu K}=6\times10^{24}$ kg $= c^3/GH_{\rm EW}$  |  '
    r'$r_s\simeq1.5$ mm  |  $r_{\rm KZ}\simeq3$ cm  |  '
    r'$T_H=2.7$ mK $\ll T_{\rm CMB}$  |  $t_{\rm evap}>10^{83}$ yr',
    color=C_TEXT, fontsize=12, fontweight='bold', pad=16)

h1 = mlines.Line2D([],[],color=C_NODE, marker='o', ls='None',
                   markersize=10, markeredgecolor=C_NODE_E,
                   label=r'0D singularity ($M_{\mu K}=6\times10^{24}$ kg)')
h2 = mlines.Line2D([],[],color=C_PINK, lw=2.5,
                   label=r'$\nabla\hat{\Phi}$ (topological winding $N=1$)')
h3 = mlines.Line2D([],[],color=C_CYAN, lw=2.0,
                   label='Null geodesics (microlensing)')
ax1.legend(handles=[h1,h2,h3], loc='upper left', fontsize=10, **LEGEND_KW)

ax1.text2D(0.02, 0.06,
    r'Winding: $N = \frac{1}{8\pi}\oint\epsilon^{ijk}'
    r'\hat{\Phi}\cdot(\partial_j\hat{\Phi}\times\partial_k\hat{\Phi})\,d^2x$'
    '\n'
    r'Same helicity: coagulate ($N{+}N\to2N$)  |  Opp. helicity: annihilate ($N{-}N\to0$)'
    '\n'
    r'Kill-switch [Roman]: $\tau_{\rm micro}<5\times10^{-8}$ at $3\sigma$  |  '
    r'Phoebe (Key+2026): $1.4\sigma$ from KZ peak'
    '\n'
    r'[ILLUSTRATIVE — Foundation II §Micro-Knots]',
    transform=ax1.transAxes, fontsize=9.5, color=C_ANNOT,
    va='bottom', bbox=ANNOT_BOX)

ax1.view_init(elev=24, azim=35)
plt.tight_layout()
save(fig1, 'Fig_MicroKnot_0D.png')


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — 1D Torsion String / Baryonic wake
# ═════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(15, 9))
fig2.patch.set_facecolor(BG)
ax2.set_facecolor(BG_AX)

# Central string
ax2.plot(0, 0, 'o', color=C_NODE, markersize=14, zorder=10, lw=0)
ax2.annotate(
    '1D Torsion String\n'
    r'$\mu_{1D}\sim10^{14}$ kg/m  |  helical $\vec{J}_5$',
    xy=(0,0), xytext=(0.28, 0.70),
    color=C_TEXT, fontsize=11, fontweight='bold',
    arrowprops=dict(arrowstyle='->', color=C_TEXT, lw=1.5))

# Conical deficit angle
delta_vis = 0.22
cone = np.pi/2 - delta_vis/2
theta_arc = np.linspace(-cone, cone, 200)
r_c = 2.2
ax2.plot(r_c*np.cos(theta_arc), r_c*np.sin(theta_arc),
         color=C_FIL, lw=2.5, ls='--', alpha=0.95,
         label=r'Conical space ($\delta=8\pi G\mu_{1D}/c^2$; physical: $\sim10^{-6}$ rad)')
wedge = mpatches.Wedge((0,0), r_c,
                        90-np.degrees(cone), 90+np.degrees(cone),
                        color=C_FIL, alpha=0.12)
ax2.add_patch(wedge)
ax2.text(0.0, 2.0,
         r'Deficit angle $\delta = 8\pi G\mu_{1D}/c^2$',
         ha='center', color=C_FIL, fontsize=10.5,
         bbox=dict(boxstyle='round,pad=0.3', fc='#FFF6E8', ec=C_FIL, alpha=0.92))

# Incoming/deflected geodesics
for y0 in np.linspace(-1.6, 1.6, 18):
    imp = abs(y0)+0.02
    alpha_k = delta_vis*0.5*np.sign(y0)/(imp+0.10)
    t_in  = np.linspace(-2.6, 0.05, 180)
    t_out = np.linspace(0.05, 2.6, 180)
    y_out = y0 - alpha_k*t_out
    col = C_CYAN if abs(y0)<0.55 else '#66AACC'
    lw  = 1.8 if abs(y0)<0.55 else 1.1
    ax2.plot(t_in,  y0*np.ones_like(t_in),  color=col, lw=lw, alpha=0.80)
    ax2.plot(t_out, y_out,                   color=col, lw=lw, alpha=0.80)

# Baryonic wake
x_w = np.linspace(0.3, 2.6, 80)
w_w = 0.55*np.exp(-0.40*(x_w-0.3))
ax2.fill_between(x_w, -w_w, w_w, color=C_RED, alpha=0.25,
                 label='Baryonic wake (Lyman-α overdensity)')
ax2.plot(x_w, np.zeros_like(x_w), color=C_RED, lw=2.5, alpha=0.90)

# Velocity kick annotation
ax2.text(0.85, -0.65,
         r'$\delta v \approx 4\pi G\mu_{1D} v_s\gamma_s$',
         color=C_RED, fontsize=11, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='#FFF0F0', ec=C_RED, alpha=0.92))

ax2.set_xlim(-2.7, 2.7)
ax2.set_ylim(-2.1, 2.4)
ax2.set_aspect('equal')
ax2.axvline(0, color=C_TEXT, lw=0.8, alpha=0.25, ls=':')
ax2.set_xlabel('x  [arb. units]', color=C_SUB, fontsize=12)
ax2.set_ylabel('y  [arb. units]', color=C_SUB, fontsize=12)
ax2.tick_params(colors=C_TICK, labelsize=10)
for sp in ax2.spines.values():
    sp.set_color('#AABBDD')

ax2.set_title(
    'ECF 1D Torsion String — Conical deficit angle & baryonic wake\n'
    r'$\pi_1(\mathcal{M})\neq0$  |  $\delta=8\pi G\mu_{1D}/c^2\sim10^{-6}$ rad  |  '
    r'$\delta v=4\pi G\mu_{1D}v_s\gamma_s$  |  '
    r'Reconnects (no merge/annihilate)  |  Helical $\vec{J}_5$',
    color=C_TEXT, fontsize=12, fontweight='bold', pad=14)

ax2.legend(loc='upper left', fontsize=10.5, **LEGEND_KW)

ax2.text(0.02, 0.05,
    r'No Newtonian $1/r^2$ attraction — baryonic wake via velocity kick $\delta v$'
    '\n'
    r'$M(1\,{\rm kpc})\sim10^3\,M_\odot$  |  '
    r'$M(1\,{\rm Mpc})\sim10^6\,M_\odot$  |  '
    r'$\xi_{\rm KZ}\sim50$--$80$ Mpc (segment length)'
    '\n'
    r'Kill-switch [LISA]: GW burst $f\sim50$ mHz + torsion tail $\tau_T\sim10^6$ s'
    '\n'
    r'[ILLUSTRATIVE — Foundation II §Torsion Strings; deficit exaggerated]',
    transform=ax2.transAxes, fontsize=9.5, color=C_ANNOT,
    va='bottom', bbox=ANNOT_BOX)

plt.tight_layout()
save(fig2, 'Fig_MacroKnot_1D_Wake.png')


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — 2D Domain Wall
# ═════════════════════════════════════════════════════════════════════════════
fig3 = plt.figure(figsize=(13, 10), facecolor=BG)
ax3  = fig3.add_subplot(111, projection='3d')
style3d(ax3)

N = 55
xw = np.linspace(-2.2, 2.2, N)
yw = np.linspace(-2.2, 2.2, N)
X, Y = np.meshgrid(xw, yw)
Z = 0.10*np.sin(np.pi*X/1.6)*np.cos(np.pi*Y/1.6)

ax3.plot_surface(X, Y, Z, alpha=0.55, color=C_WALL,
                 rstride=2, cstride=2, linewidth=0, antialiased=True)

# Phase labels
ax3.text(0, 0, 1.8, r'Phase $\sigma_+$ ($+$helicity)',
         color='#2244AA', fontsize=11, ha='center', fontweight='bold')
ax3.text(0, 0,-1.8, r'Phase $\sigma_-$ ($-$helicity)',
         color='#AA2222', fontsize=11, ha='center', fontweight='bold')

# Repulsive arrows
for xa in np.linspace(-1.6, 1.6, 5):
    for ya in np.linspace(-1.6, 1.6, 5):
        ax3.quiver(xa, ya,  0.12, 0, 0,  0.65,
                   color=C_RED, alpha=0.85, linewidth=1.6,
                   arrow_length_ratio=0.32)
        ax3.quiver(xa, ya, -0.12, 0, 0, -0.65,
                   color=C_RED, alpha=0.85, linewidth=1.6,
                   arrow_length_ratio=0.32)

# Expelled gas trajectories
np.random.seed(42)
for _ in range(22):
    xp = np.random.uniform(-1.9, 1.9)
    yp = np.random.uniform(-1.9, 1.9)
    t_t = np.linspace(0, 1.6, 60)
    z_t = 0.06 + 0.55*(np.exp(0.95*t_t)-1)
    ax3.plot(xp*np.ones_like(t_t), yp*np.ones_like(t_t), z_t,
             color=C_GOLD, lw=1.4, alpha=0.70)

ax3.set_title(
    'ECF 2D Chiral Wall — Topological repulsion & cosmic void formation\n'
    r'$\pi_0(\mathcal{M})\neq0$  |  $\sigma_{2D}\sim10^{49}$ kg/m$^2$  |  '
    r'$\delta_w\sim10^{-18}$ m  |  $R_w\sim\xi_{\rm KZ}\sim60$ Mpc  |  '
    r'$\beta_{\rm ECF}=0.35^\circ$ (birefringence)',
    color=C_TEXT, fontsize=12, fontweight='bold', pad=16)

h_wall = mlines.Line2D([],[],color=C_WALL, lw=8, alpha=0.7,
                        label=r'2D Chiral Wall ($\sigma_+/\sigma_-$ boundary)')
h_arr  = mlines.Line2D([],[],color=C_RED,  lw=2.5,
                        label=r'Israel repulsion: $\ddot{z}=\frac{8\pi G\sigma_{2D}}{3}z$')
h_traj = mlines.Line2D([],[],color=C_GOLD, lw=2.0,
                        label=r'Baryonic gas $z(t)\propto e^{\sqrt{8\pi G\sigma_{2D}/3}\,t}$')
ax3.legend(handles=[h_wall,h_arr,h_traj], loc='upper left',
           fontsize=10, **LEGEND_KW)

ax3.text2D(0.02, 0.06,
    r'$\pi_0(\mathcal{M})\neq\emptyset$ $\Rightarrow$ 2D Chiral Walls  |  '
    r'Expands at $\sim c$  |  Opp. chirality: partial annihilation $\to$ GW + 3D fluid'
    '\n'
    r'Dual void mechanism: Wall creates sharp boundary  +  3D fluid sustains expansion'
    '\n'
    r'Kill-switch [LiteBIRD]: $\beta<0.1^\circ$ at $3\sigma$  |  '
    r'Planck PR4: $0.32^\circ\pm0.11^\circ$  |  ACT DR6: $0.215^\circ\pm0.074^\circ$'
    '\n'
    r'[ILLUSTRATIVE — Foundation II §Chiral Walls]',
    transform=ax3.transAxes, fontsize=9.5, color=C_ANNOT,
    va='bottom', bbox=ANNOT_BOX)

ax3.set_zlim(-2.3, 2.3)
ax3.view_init(elev=26, azim=42)
plt.tight_layout()
save(fig3, 'Fig_DomainWall_2D.png')


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — 3D Chiral Fluid (dynamical dark energy)
# ═════════════════════════════════════════════════════════════════════════════
fig4 = plt.figure(figsize=(16, 7), facecolor=BG)

# Left panel: 3D volume
ax4a = fig4.add_subplot(121, projection='3d')
style3d(ax4a)

np.random.seed(7)
N_pts = 320
xp = np.random.uniform(-1.6, 1.6, N_pts)
yp = np.random.uniform(-1.6, 1.6, N_pts)
zp = np.random.uniform(-1.6, 1.6, N_pts)
dens = np.exp(-(xp**2+yp**2+zp**2)/2.5)
sc = ax4a.scatter(xp, yp, zp, c=dens, cmap='plasma', s=18, alpha=0.55,
                  vmin=0, vmax=1)
cbar = fig4.colorbar(sc, ax=ax4a, pad=0.02, shrink=0.6, aspect=20)
cbar.ax.tick_params(colors=C_SUB, labelsize=8)
cbar.set_label(r'$\langle S^2\rangle_{\rm vol}$ (normalized)', color=C_SUB, fontsize=9)

for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
    dx, dy = 0.65*np.cos(ang), 0.65*np.sin(ang)
    ax4a.quiver(0,0,0, dx,dy,0, color='#CC6600', alpha=0.90,
                length=1.0, arrow_length_ratio=0.28, linewidth=1.9)
for dz in [1.0, -1.0]:
    ax4a.quiver(0,0,0, 0,0,dz, color='#CC6600', alpha=0.90,
                length=1.0, arrow_length_ratio=0.28, linewidth=1.9)

ax4a.set_title(
    '3D Chiral Fluid\n'
    r'Residual $\langle S^2\rangle_{\rm vol}$ + pressure $P_{\rm tors}$',
    color=C_TEXT, fontsize=11, fontweight='bold', pad=12)
ax4a.view_init(elev=22, azim=32)

# Right panel: w(z)
ax4b = fig4.add_subplot(122)
ax4b.set_facecolor(BG_AX)
for sp in ax4b.spines.values():
    sp.set_color('#AABBDD')

w0, wa = -0.904, -0.153
z_arr = np.linspace(0, 3.5, 400)
a_arr = 1/(1+z_arr)
w_ecf  = w0 + wa*(1-a_arr)
w_lcdm = -1.0*np.ones_like(z_arr)

ax4b.plot(z_arr, w_ecf,  color=C_RED,  lw=3.0,
          label=rf'ECF: $w_0={w0}$, $w_a={wa}$ (a priori, PIT)')
ax4b.plot(z_arr, w_lcdm, color='#666666', lw=2.0, ls='--',
          label=r'$\Lambda$CDM: $w=-1$')
ax4b.fill_between(z_arr, w_ecf, w_lcdm, where=(w_ecf>w_lcdm),
                  alpha=0.15, color=C_RED, label='ECF > ΛCDM')
ax4b.axhspan(-1.06, -0.90, alpha=0.14, color=C_GREEN,
             label='DESI DR2 (schematic)')
ax4b.axhline(-1, color='#888888', lw=1.0, ls=':')

# Phantom crossing annotation
ax4b.annotate(
    r'$w_0+w_a=-1.057$' + '\n(phantom crossing stabilised by PGT)',
    xy=(3.2, w0+wa*(1-1/(1+3.2))),
    xytext=(1.6, -1.16),
    color=C_RED, fontsize=9.5,
    arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.2),
    bbox=dict(boxstyle='round,pad=0.3', fc='#FFF0F0', ec=C_RED, alpha=0.92))

ax4b.set_xlabel(r'Redshift $z$', color=C_SUB, fontsize=12)
ax4b.set_ylabel(r'Equation of state $w(z)$', color=C_SUB, fontsize=12)
ax4b.set_title(r'Dynamical dark energy $w(z) = w_0 + w_a(1-a)$',
               color=C_TEXT, fontsize=12, fontweight='bold')
ax4b.tick_params(colors=C_SUB, labelsize=10)
ax4b.legend(fontsize=9.5, **LEGEND_KW)
ax4b.grid(True, color='#DDDDF0', alpha=0.60, ls=':')

ax4b.text(0.04, 0.06,
    r'$P_{\rm tors}=-\frac{1}{4}\kappa^2\langle S^2\rangle_{\rm vol}$'
    '\n' r'$\langle S^2\rangle_{\rm vol}^{(0)}\simeq3.88\times10^{-39}$ kg$^2$m/s$^2$'
    '\n' r'$P_{\rm tors}^{(0)}\simeq-2\times10^{-82}$ Pa  |  $\kappa^2=2.0766\times10^{-43}$ m J$^{-1}$'
    '\n' r'Not a topological defect — volume-filling condensate  |  $f_{\rm fluid}\sim0.73$'
    '\n[Diagonal errors — full covariance: Foundation III]',
    transform=ax4b.transAxes, fontsize=9.5, color=C_ANNOT,
    va='bottom', bbox=ANNOT_BOX)

fig4.suptitle(
    'ECF 3D Torsion Fluid — Dynamical dark energy from chiral condensate dilution\n'
    r'No homotopy obstruction — residue of KZ crystallisation  |  $L_{\rm coh}\sim4.4$ Gpc',
    color=C_TEXT, fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
save(fig4, 'Fig_ChiralFluid_3D.png')


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — ECF Hierarchical Topological Architecture
# ═════════════════════════════════════════════════════════════════════════════
fig5 = plt.figure(figsize=(14, 11), facecolor=BG)
ax5  = fig5.add_subplot(111, projection='3d')
style3d(ax5)
ax5.axis('off')

# 3D background fluid
np.random.seed(99)
N_bg = 400
xb = np.random.uniform(-2.6, 2.6, N_bg)
yb = np.random.uniform(-2.6, 2.6, N_bg)
zb = np.random.uniform(-2.6, 2.6, N_bg)
db = np.exp(-(xb**2+yb**2+zb**2)/9)
ax5.scatter(xb, yb, zb, c=db, cmap='Blues', s=5, alpha=0.30, vmin=0, vmax=1)

# 2D walls
walls = [
    [[-2.6,-2.6,-2.0],[2.6,-2.6,-2.0],[2.6,2.6,-2.0],[-2.6,2.6,-2.0]],
    [[-2.6,-2.0,-2.6],[2.6,-2.0,-2.6],[2.6,-2.0,2.6],[-2.6,-2.0,2.6]],
]
for verts in walls:
    ax5.add_collection3d(
        Poly3DCollection([verts], alpha=0.22,
                         facecolor=C_WALL, edgecolor='#4455AA', lw=0.9))

# 1D filaments
filaments = [
    ([-2.6,0,0],[2.6,0,0]),  ([0,-2.6,0],[0,2.6,0]),
    ([0,0,-2.6],[0,0,2.6]),  ([-2.2,-2.2,-2.2],[2.2,2.2,2.2]),
    ([-2.2, 2.2,-2.2],[2.2,-2.2,2.2]),
]
for (x1,y1,z1),(x2,y2,z2) in filaments:
    tf = np.linspace(0, 1, 120)
    xf = x1+(x2-x1)*tf; yf = y1+(y2-y1)*tf; zf = z1+(z2-z1)*tf
    ax5.plot(xf, yf, zf, color=C_FIL, lw=2.6, alpha=0.95, zorder=5)
    ax5.plot(xf, yf, zf, color=C_FIL, lw=6.5, alpha=0.15, zorder=4)

# 0D nodes
nodes = [(0,0,0),(2.2,0,0),(-2.2,0,0),(0,2.2,0),(0,-2.2,0),
         (0,0,2.2),(0,0,-2.2),(-2.2,-2.2,-2.2),(2.2,2.2,2.2),
         (-2.2,2.2,-2.2),(2.2,-2.2,2.2)]
for xn,yn,zn in nodes:
    ax5.scatter([xn],[yn],[zn], color=C_NODE, s=95, zorder=10,
                edgecolors=C_NODE_E, linewidths=1.4)
    ax5.scatter([xn],[yn],[zn], color=C_NODE_E, s=300, alpha=0.16, zorder=9)

ax5.set_title(
    'ECF Hierarchical Topological Architecture — Unified dark sector\n'
    r'0D Micro/Macro-Knots ($\pi_2$) $\oplus$ 1D Torsion Strings ($\pi_1$) $\oplus$ '
    r'2D Chiral Walls ($\pi_0$) $\oplus$ 3D Torsion Fluid  —  [ILLUSTRATIVE]',
    color=C_TEXT, fontsize=12, fontweight='bold', pad=16)

h0D = mlines.Line2D([],[],color=C_NODE, marker='o', ls='None',
                    markersize=9, markeredgecolor=C_NODE_E,
                    label=r'0D Micro/Macro-Knot ($\pi_2$, hedgehog; $M_{\mu K}=6\times10^{24}$ kg)')
h1D = mlines.Line2D([],[],color=C_FIL,  lw=2.6,
                    label=r'1D Torsion String ($\pi_1$, helical; $\mu_{1D}\sim10^{14}$ kg/m)')
h2D = mlines.Line2D([],[],color=C_WALL, lw=8, alpha=0.6,
                    label=r'2D Chiral Wall ($\pi_0$; $\sigma_{2D}\sim10^{49}$ kg/m$^2$; $\beta=0.35^\circ$)')
h3D = mlines.Line2D([],[],color=C_FLUID, lw=6, alpha=0.6,
                    label=r'3D Torsion Fluid (condensate; $w_0=-0.904$, $w_a=-0.153$)')
ax5.legend(handles=[h0D,h1D,h2D,h3D], loc='upper left',
           fontsize=10.5, **LEGEND_KW)

ax5.text2D(0.02, 0.04,
    r'$\pi_2\neq\emptyset$: 0D Micro/Macro-Knots (hedgehog, coagulate/annihilate)'
    '\n'
    r'$\pi_1\neq\emptyset$: 1D Torsion Strings (conical, helical $\vec{J}_5$, reconnect)'
    '\n'
    r'$\pi_0\neq\emptyset$: 2D Chiral Walls (flat, repulsive, birefringence $\beta=0.35^\circ$)'
    '\n'
    r'No $\pi_k$: 3D Torsion Fluid (volume-filling condensate, $P<0$, DESI $4.9\sigma$ vs $\Lambda$CDM)'
    '\n'
    r'[Foundation II §Topological Zoology — ILLUSTRATIVE]',
    transform=ax5.transAxes, fontsize=9.5, color=C_ANNOT,
    va='bottom', bbox=ANNOT_BOX)

ax5.view_init(elev=22, azim=42)
plt.tight_layout()
save(fig5, 'Fig_ECF_Topological_Architecture.png')

print('\nDone — 5 figures generated in', FIGS)
