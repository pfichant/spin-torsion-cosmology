"""
plot_torsion_geometry_schema.py  — v2
Author: Pascal Fichant (2026)

Schematic comparison of Riemannian (GR) and Riemann-Cartan (Einstein-Cartan)
geometries via parallel-transport loops on a curved 2D surface.

Left panel:  torsion-free connection (GR) — parallelogram closes at D.
Right panel: non-zero torsion (ECF) — closure failure D1 ≠ D2, gap ∝ T^λ_μν.

Physical content (F1 extended v2, Sec. 2, Fig. 1; Kibble 1961, Sciama 1964):
  GR:  T^λ_μν = 0  →  parallel transport commutes, parallelogram closes.
  ECF: T^λ_μν ≠ 0  →  closure gap = T^λ_μν dX^μ dY^ν
       Torsion sourced algebraically by spin density (Cartan equation).

Output: figure_torsion_geometry_schema.png (300 dpi)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

matplotlib.rcParams['font.family']      = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'


class Arrow3D(FancyArrowPatch):
    """3D arrow compatible with Matplotlib >= 3.5 via do_3d_projection."""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def _arrow(ax, p0, p1, color, lw=2, ls='-', ms=15):
    ax.add_artist(Arrow3D(
        [p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
        mutation_scale=ms, lw=lw, arrowstyle="-|>",
        color=color, linestyle=ls
    ))


def _label(ax, p, txt, dx=0, dy=-0.12, dz=0):
    ax.text(p[0]+dx, p[1]+dy, p[2]+dz, txt, fontsize=12, fontweight='bold')


def draw_panel(ax, torsion):
    """Draw curved surface and transport loop for GR (torsion=False) or ECF (True)."""
    x = np.linspace(-1, 1, 20)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    Z = 0.3 * X**2

    cmap = plt.cm.Blues if not torsion else plt.cm.Oranges
    ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.55,
                    rstride=2, cstride=2, edgecolor='k', linewidth=0.15)

    # Manifold points (on the surface Z = 0.3 X²)
    A = np.array([-0.5, -0.5, 0.3 * (-0.5)**2])
    B = np.array([-0.5,  0.5, 0.3 * (-0.5)**2])
    C = np.array([ 0.5, -0.5, 0.3 * ( 0.5)**2])
    D_ideal = np.array([0.5, 0.5, 0.3 * (0.5)**2 + 0.05])

    if not torsion:
        # GR: both paths reach the same endpoint D
        _arrow(ax, A, B,       'k')
        _arrow(ax, B, D_ideal, 'k')
        _arrow(ax, A, C,       'k')
        _arrow(ax, C, D_ideal, 'k')

        _label(ax, A,      'A')
        _label(ax, B,      'B')
        _label(ax, C,      'C',  dx=0.06, dy=-0.06)
        _label(ax, D_ideal,'D',  dx=0.06, dy=0)

        ax.set_title("Riemannian Geometry (GR)\nZero Torsion",
                     fontsize=13, pad=18)
        ax.text2D(0.5, 0.01,
                  r"Commutative transport: $T^\lambda{}_{\mu\nu} = 0$",
                  transform=ax.transAxes, ha='center', fontsize=11,
                  bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    else:
        # ECF: path A→B→D1 and A→C→D2 diverge; gap ∝ T^λ_μν
        D1 = D_ideal + np.array([ 0.00, -0.10,  0.05])
        D2 = D_ideal + np.array([ 0.15,  0.10,  0.10])

        _arrow(ax, A, B,  'navy')
        _arrow(ax, B, D1, 'navy')
        _arrow(ax, A, C,  'darkred')
        _arrow(ax, C, D2, 'darkred')
        _arrow(ax, D1, D2, 'red', lw=2.5, ls='--', ms=18)

        _label(ax, A,  'A')
        _label(ax, B,  'B')
        _label(ax, C,  'C',  dx=0.06, dy=-0.06)
        _label(ax, D1, 'D\u2081', dx=-0.18, dy=0)
        _label(ax, D2, 'D\u2082', dx=0.06,  dy=0)

        mid_D = (D1 + D2) / 2
        ax.text(mid_D[0]+0.18, mid_D[1]-0.05, mid_D[2]+0.18,
                r"Closure gap $\propto T^\lambda{}_{\mu\nu}$",
                color='red', fontsize=10, ha='center')

        ax.set_title("Riemann\u2013Cartan Geometry (ECF)\nNon-Zero Torsion",
                     fontsize=13, pad=18)
        ax.text2D(0.5, 0.01,
                  r"Torsion sourced by spin: $T^\lambda{}_{\mu\nu} \neq 0$",
                  transform=ax.transAxes, ha='center', fontsize=11,
                  bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 0.9)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=-58)


# --- Figure assembly ---
fig = plt.figure(figsize=(13, 6.5))
fig.suptitle(
    "Riemannian vs. Riemann\u2013Cartan Geometry: Parallel Transport",
    fontsize=14, fontweight='bold', y=1.00
)

ax1 = fig.add_subplot(121, projection='3d')
draw_panel(ax1, torsion=False)

ax2 = fig.add_subplot(122, projection='3d')
draw_panel(ax2, torsion=True)

# Vertical separator between panels
fig.add_artist(plt.Line2D(
    [0.5, 0.5], [0.05, 0.95],
    transform=fig.transFigure, color='black', linewidth=1.2
))

plt.tight_layout(pad=1.5)
plt.savefig('figure_torsion_geometry_schema.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: figure_torsion_geometry_schema.png")
